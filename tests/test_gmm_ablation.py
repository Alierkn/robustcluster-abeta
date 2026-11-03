import numpy as np
import pytest

from robustcluster_abeta.gmm_ablation import fit_scaler, match_partitions
from robustcluster_abeta.validation import InvalidInput


def test_scaler_uses_fit_rows_only():
    x, p = fit_scaler(np.array([[0.0, 1.0], [2.0, 3.0]]), np.array([[100.0, 101.0]]))
    np.testing.assert_allclose(x, [[99.0, 99.0]])
    assert p["mean"] == [1.0, 2.0]
    with pytest.raises(InvalidInput):
        fit_scaler(np.ones((2, 2)), np.ones((2, 2)))


def test_matching_permutation_and_absent_family():
    result = match_partitions([0, 0, 1, 1], [9, 9, 7, 7])
    assert result["ari"] == 1 and result["matched_fraction"] == 1
    assert all(p["jaccard"] == 1 for p in result["pairs"])
    result = match_partitions([0, 0, 1, 1, 2, 2], [9, 9, 7, 7, 7, 7])
    assert len(result["unmatched_left"]) == 1
    assert result["matched_fraction"] == pytest.approx(4 / 6)


def test_matching_rejects_different_observations():
    with pytest.raises(InvalidInput):
        match_partitions([0, 1], [0])


def test_synthetic_experiment_is_repeatable(tmp_path):
    from robustcluster_abeta.gmm_ablation import experiment
    from robustcluster_abeta.io import SOURCE_COLUMNS
    from robustcluster_abeta.manifest import Run
    from robustcluster_abeta.validation import Budget

    rng = np.random.default_rng(8)
    rows = []
    for replica in range(3):
        for i, t in enumerate(np.linspace(1e6, 3e6, 40)):
            features = 10 + 10 * (i % 2) + rng.normal(0, 0.03, 4)
            rows.append([t, 0, *features, 1, 1, 1, 1])
    source = tmp_path / "synthetic.dat"
    np.savetxt(source, rows, header=" ".join(SOURCE_COLUMNS))
    config = {
        "project_root": str(tmp_path),
        "mode": "robustness_extension",
        "inputs": {"descriptors": str(source)},
        "replicas": 3,
        "interval_ps": [1000000, 3000000],
        "gmm": {
            "fit_per_replica": 20,
            "sampling_seed": 1,
            "master_seeds": [42, 43],
            "components": [2],
            "covariance_type": "full",
            "reg_covar": 1e-6,
            "max_iter": 50,
            "n_init": 1,
            "tol": 0.001,
        },
    }
    runs = []
    for _ in range(2):
        run = Run(config, "synthetic-test")
        summary = experiment(config, run, Budget())
        run.finish("SUCCESS")
        assert summary["converged_models"] == 4
        assert summary["ari_by_k"]["2"]["min"] == 1
        runs.append(np.load(run.path("tables", "assignments.npz")))
    for key in runs[0].files:
        np.testing.assert_array_equal(runs[0][key], runs[1][key])
