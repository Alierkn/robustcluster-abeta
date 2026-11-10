import copy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from conftest import write_fes

from robustcluster_abeta.io import DESCRIPTORS, SOURCE_COLUMNS
from robustcluster_abeta.manifest import Run, load_config, sha256
from robustcluster_abeta.pipeline import cluster_pipeline, reproduce, validate_configuration
from robustcluster_abeta.validation import Budget, InvalidInput

ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize("key,value", [("replicas", 2), ("interval_ps", [0, 3000000])])
def test_reproduction_rejects_changed_replica_or_window(key, value):
    config = load_config(ROOT/"config/paper_reproduction.yaml")
    config[key] = value
    with pytest.raises(InvalidInput, match="Baseline requires"):
        validate_configuration(config)


def test_deterministic_complete_clustering_smoke():
    # Five repeated separated basins give enough local clusters for the source-informed elbow.
    rng = np.random.default_rng(10)
    centers = np.array([[0,0,0,0], [1,1,1,1], [0,1,1,0], [1,0,0,1], [.5,.5,.5,.5]])
    values = np.vstack([rng.normal(center, .012, (90, 4)) for center in centers])
    table = pd.DataFrame(values, columns=DESCRIPTORS[:4])
    table["source_row"] = np.arange(len(table))
    config = load_config(ROOT/"config/robustness.yaml")
    config["execution"].update(group_size=150, max_groups=3)
    config["dpc"].update(min_cluster_size=12, nmax=6, dc=.12)
    first = cluster_pipeline(table, config, 123, Budget())
    second = cluster_pipeline(table, config, 123, Budget())
    np.testing.assert_array_equal(first["labels"], second["labels"])
    assert len(first["labels"]) == len(table)
    assert len(first["accepted"]) >= 5
    assert np.all(first["labels"] >= 1)


def test_manifest_records_failure_and_hashes(tmp_path):
    config = copy.deepcopy(load_config(ROOT/"config/paper_reproduction.yaml"))
    config["project_root"] = str(tmp_path)
    run = Run(config, "validate")
    path = run.path("logs", "failure.txt")
    path.write_text("expected test failure")
    run.finish("FAILED", "intentional fixture")
    assert run.data["status"] == "FAILED"
    assert run.data["outputs"][0]["sha256"] == sha256(path)
    assert run.data["runtime_seconds"] >= 0


def test_synthetic_weighted_pipeline_outputs(tmp_path):
    """End-to-end software fixture; never treated as a biological analysis."""
    rng = np.random.default_rng(88)
    centers = np.array([[0,0,0,0], [1,1,1,1], [0,1,1,0], [1,0,0,1], [.5,.5,.5,.5]])
    raw = np.vstack([rng.normal(center, .012, (90, 4)) for center in centers])
    raw = raw[rng.permutation(len(raw))]*[10, 10, 1, 30]+[1, 1, 1, 30]
    values = np.column_stack([np.tile(np.linspace(1e6, 3e6, 150), 3), np.zeros(450), raw,
                              np.full((450, 4), [12, 18, 10, 100])])
    source = tmp_path/"synthetic.dat"
    np.savetxt(source, values, header=" ".join(SOURCE_COLUMNS))
    fes = write_fes(tmp_path/"synthetic_fes.dat", np.linspace(0, 20, 3), np.linspace(0, 20, 3),
                    lambda a, b: .1*a+.1*b)
    config = load_config(ROOT/"config/robustness.yaml")
    config.update(project_root=str(tmp_path), bootstrap_draws=10)
    config["inputs"].update(descriptors=str(source), fes=str(fes), fes_energy_unit="kJ/mol",
                            fes_provenance="ANALYTIC SOFTWARE TEST ONLY")
    config["execution"].update(group_size=150, max_groups=3)
    config["dpc"].update(min_cluster_size=12, nmax=6, dc=.12)
    run = Run(config, "synthetic_test")
    result = reproduce(config, run, Budget())
    run.finish("SUCCESS")
    frames = pd.read_csv(run.path("tables", "baseline_frames.csv.gz"))
    assert result["frames"] == 450
    assert np.isclose(frames.pooled_weight.sum(), 1)
    np.testing.assert_allclose(frames.groupby("replica_id").replica_normalized_weight.sum(), 1)
    assert (frames.final_cluster_label > 0).all()
    assert run.path("figures", "fig08_cluster_relevance.pdf").is_file()


def test_unweighted_cluster_command_reads_no_fes(tmp_path):
    """Software fixture: clustering runs without a FES and reports only raw fractions."""
    from robustcluster_abeta.pipeline import cluster
    rng = np.random.default_rng(88)
    centers = np.array([[0,0,0,0], [1,1,1,1], [0,1,1,0], [1,0,0,1], [.5,.5,.5,.5]])
    raw = np.vstack([rng.normal(center, .012, (90, 4)) for center in centers])
    raw = raw[rng.permutation(len(raw))]*[10, 10, 1, 30]+[1, 1, 1, 30]
    values = np.column_stack([np.tile(np.linspace(1e6, 3e6, 150), 3), np.zeros(450), raw,
                              np.full((450, 4), [12, 18, 10, 100])])
    source = tmp_path/"synthetic.dat"
    np.savetxt(source, values, header=" ".join(SOURCE_COLUMNS))
    config = load_config(ROOT/"config/robustness.yaml")
    config.update(project_root=str(tmp_path))
    config["inputs"].update(descriptors=str(source), fes=str(tmp_path/"absent_fes.dat"))
    config["execution"].update(group_size=150, max_groups=3)
    config["dpc"].update(min_cluster_size=12, nmax=6, dc=.12)
    run = Run(config, "cluster", "parameters")
    summary = cluster(config, run, Budget(), "parameters")
    run.finish("SUCCESS")
    families = pd.read_csv(run.path("tables", "families_unweighted.csv"))
    assert summary["variants"][0] == "baseline"
    assert not any("weight" in column for column in families.columns)
    for _, part in families.groupby("variant"):
        assert part.frames.sum() == 450
        assert np.isclose(part.raw_fraction.sum(), 1)
    ari = pd.read_csv(run.path("tables", "ari_matrix.csv"), index_col=0)
    assert np.isclose(ari.loc["baseline", "baseline"], 1)


def test_cluster_parameter_changes_require_robustness_mode():
    from robustcluster_abeta.pipeline import _cluster_variants
    config = load_config(ROOT/"config/paper_reproduction.yaml")
    with pytest.raises(InvalidInput):
        _cluster_variants(config, "parameters")
    assert [name for name, *_ in _cluster_variants(config, "baseline")] == ["baseline"]
