import numpy as np
import pytest

from robustcluster_abeta.fes import read_fes, read_fes_structure
from robustcluster_abeta.io import read_descriptors
from robustcluster_abeta.preprocessing import make_groups, transform_features
from robustcluster_abeta.reweighting import (R_KJ_MOL_K, final_bias_log_weights, normalize_replicas,
                                            time_dependent_log_weights)
from robustcluster_abeta.statistics import (block_bootstrap_population, correlation_diagnostic,
                                          kish_ess, population_summary, weighted_moments)
from robustcluster_abeta.validation import BlockedAnalysis, InvalidInput


def test_replica_identity_and_endpoints(descriptor_file):
    table = read_descriptors(descriptor_file)
    assert table.groupby("replica_id").size().tolist() == [6, 6, 6]
    assert table.source_row.tolist() == list(range(18))
    assert table.source_line.iloc[0] == 2
    assert table.frame_index.tolist() == list(range(6))*3
    assert len(read_descriptors(descriptor_file, interval=(1.4e6, 2.6e6))) == 12


def test_wrong_replica_count(descriptor_file):
    with pytest.raises(InvalidInput, match="Expected 2"):
        read_descriptors(descriptor_file, expected_replicas=2)


@pytest.mark.parametrize("defect", ["nan", "duplicate", "header", "short"])
def test_invalid_descriptors(descriptor_file, defect):
    lines = descriptor_file.read_text().splitlines()
    if defect == "nan":
        fields = lines[1].split()
        fields[3] = "nan"
        lines[1] = " ".join(fields)
    elif defect == "duplicate":
        lines[2] = lines[1]
    elif defect == "header":
        lines[0] = "# unrelated input"
    else:
        lines = lines[:-1]
    descriptor_file.write_text("\n".join(lines))
    with pytest.raises(InvalidInput):
        read_descriptors(descriptor_file)


def test_normalization_and_groups():
    values = np.array([[2, 5], [3, 9], [4, 13]])
    transformed, parameters = transform_features(values)
    np.testing.assert_allclose(transformed, [[0, 0], [.5, .5], [1, 1]])
    assert parameters["offset"] == [2, 5]
    with pytest.raises(InvalidInput):
        transform_features([[1, 1], [1, 2]])
    groups = make_groups(303, 100, np.random.default_rng(42))
    assert sorted(np.concatenate(groups)) == list(range(303))
    assert [len(group) for group in groups] == [101, 101, 101]


def test_bilinear_and_row_order(fes_file):
    grid = read_fes(fes_file, "kJ/mol", "analytic test fixture")
    a, b = np.array([0, .15, 1.7, 3]), np.array([0, .8, 1.2, 2])
    np.testing.assert_allclose(grid.interpolate(a, b), 2*a+3*b+a*b, atol=1e-12)
    lines = fes_file.read_text().splitlines()
    headers = [line for line in lines if line.startswith("#")]
    rows = [line for line in lines if not line.startswith("#")]
    fes_file.write_text("\n".join(headers+rows[::-1]))
    np.testing.assert_allclose(read_fes(fes_file, "kJ/mol", "test").energy, grid.energy)
    with pytest.raises(InvalidInput, match="outside"):
        grid.interpolate([-0.0001], [1])


def test_structural_validation_does_not_assert_units(fes_file):
    grid = read_fes_structure(fes_file)
    assert grid.energy_unit is None
    np.testing.assert_allclose(grid.interpolate([.5], [1.]), [4.5])
    with pytest.raises(BlockedAnalysis, match="explicit kJ/mol"):
        read_fes(fes_file, None, "Received from supervisor")
    with pytest.raises(BlockedAnalysis):
        read_fes(fes_file, "kJ/mol", None)


@pytest.mark.parametrize("defect", ["missing", "duplicate", "nan", "inf", "header", "coordinate"])
def test_reject_bad_fes(fes_file, defect):
    lines = fes_file.read_text().splitlines()
    if defect == "missing":
        lines.pop()
    elif defect == "duplicate":
        lines[-1] = lines[-2]
    elif defect in {"nan", "inf"}:
        fields = lines[-1].split()
        fields[2] = defect
        lines[-1] = " ".join(fields)
    elif defect == "header":
        lines[3] = "#! SET nbins_alpha 8"
    else:
        lines[-1] = "4 2 20"
    fes_file.write_text("\n".join(lines))
    with pytest.raises(InvalidInput):
        read_fes(fes_file, "kJ/mol", "test fixture")


def test_download_and_provenance_gates(fes_file):
    partial = fes_file.with_suffix(".crdownload")
    fes_file.rename(partial)
    with pytest.raises(InvalidInput):
        read_fes(partial, "kJ/mol", "test")
    with pytest.raises(BlockedAnalysis):
        read_fes(fes_file, "kJ/mol", "test")
    with pytest.raises(BlockedAnalysis):
        time_dependent_log_weights([1, 2], 310)


def test_weight_formula_and_replica_equalization():
    energy = np.array([0., 1., 2., 3., 4.])
    replicas = np.array([1, 1, 2, 2, 2])
    logw = final_bias_log_weights(energy)
    np.testing.assert_allclose(logw, -.9*energy/(R_KJ_MOL_K*310))
    within, pooled = normalize_replicas(logw, replicas)
    assert np.isclose(within[replicas == 1].sum(), 1)
    assert np.isclose(pooled[replicas == 2].sum(), .5)
    shifted, _ = normalize_replicas(final_bias_log_weights(energy+1e4), replicas)
    np.testing.assert_allclose(shifted, within, atol=1e-12)
    extreme, _ = normalize_replicas(np.array([-1e6, -1e6-1]), [1, 1])
    assert np.isclose(extreme.sum(), 1)


def test_moments_kish_and_population():
    mean, width = weighted_moments([0, 2], [1, 3])
    assert mean == 1.5
    assert np.isclose(width, np.sqrt(.75))
    assert kish_ess([1, 1, 1]) == 3
    assert np.isclose(kish_ess([1, 3]), 1.6)
    per_replica, summary = population_summary([1, 2, 1, 2], [1, 1, 2, 2], [.25, .75, .5, .5])
    np.testing.assert_allclose(summary["mean"], [.375, .625])
    np.testing.assert_allclose(summary.replica_sem, [.125, .125])
    with pytest.raises(InvalidInput):
        weighted_moments([1, 2], [0, 0])


def test_acf_on_seeded_ar1():
    rng = np.random.default_rng(4)
    noise = rng.normal(size=40000)
    series = np.empty_like(noise)
    series[0] = noise[0]
    for i in range(1, len(series)):
        series[i] = .8*series[i-1]+noise[i]
    acf, diagnostic = correlation_diagnostic(series, 20)
    assert acf[0] == 1
    assert abs(acf[1]-.8) < .03
    assert 6 < diagnostic["statistical_inefficiency"] < 13
    assert diagnostic["tau_int_ps"] == diagnostic["statistical_inefficiency"]*10


def test_bootstrap_does_not_mix_replicas():
    # Each replica occupies a distinct family: every within-replica bootstrap must remain 50:50.
    labels = np.repeat([1, 2], 20)
    intervals, draws = block_bootstrap_population(labels, labels, np.ones(40)/20,
        {1: 5, 2: 5}, np.random.default_rng(123), draws=30)
    np.testing.assert_allclose(draws, .5)
    assert (intervals.bootstrap_low == .5).all()
