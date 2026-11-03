import numpy as np
import pytest

from robustcluster_abeta.consensus import assign_frames, merge_clusters, wasserstein_matrix
from robustcluster_abeta.dpc import cutoff_density, density_delta, iterative_dpc
from robustcluster_abeta.stability import aligned_partitions, compare_partitions
from robustcluster_abeta.validation import AnalysisFailure, Budget, InvalidInput, ResourceLimit


def test_cutoff_and_density_ties():
    distances = np.array([[0, 1, 3], [1, 0, 2], [3, 2, 0]], dtype=np.float32)
    rho = cutoff_density(distances, 1)
    np.testing.assert_array_equal(rho, [2, 2, 1])
    delta, parent, order = density_delta(distances, rho)
    np.testing.assert_array_equal(order, [0, 1, 2])
    np.testing.assert_array_equal(parent, [-1, 0, 1])
    np.testing.assert_array_equal(delta, [3, 1, 2])


def test_residual_exclusion_and_step3():
    # Index 4 is a deliberately distant residual and must not move either centroid.
    features = np.array([[0., 0.], [.1, 0], [1, 1], [.9, 1], [10, 10]])
    accepted = [np.array([0, 1]), np.array([2, 3])]
    labels, centers = assign_frames(features, accepted, np.array([1, 2]))
    np.testing.assert_allclose(centers, [[.05, 0], [.95, 1]])
    np.testing.assert_array_equal(labels, [1, 1, 2, 2, 2])
    with pytest.raises(AnalysisFailure):
        assign_frames(features, [], [])


def test_wasserstein_is_marginal_norm():
    values = np.array([[0., 0.], [1, 1], [2, 3], [3, 4]])
    distance = wasserstein_matrix(values, [np.array([0, 1]), np.array([2, 3])])
    np.testing.assert_allclose(distance[0, 1], np.sqrt(2**2+3**2))
    with pytest.raises(AnalysisFailure, match="five"):
        merge_clusters(distance)


def test_label_permutation_unmatched_and_identity():
    ari, matches = compare_partitions([1, 1, 2, 2], [9, 9, 8, 8])
    assert ari == 1
    assert (matches.jaccard == 1).all()
    _, split = compare_partitions([1, 1, 2, 2], [9, 9, 8, 7])
    assert (split.status == "other_unmatched").sum() == 1
    a, b = aligned_partitions([10, 11], [1, 2], [11, 10], [9, 8])
    assert b.tolist() == [8, 9]
    with pytest.raises(InvalidInput):
        aligned_partitions([10, 11], [1, 2], [11, 12], [9, 8])


def test_dpc_deterministic_analytic_clusters():
    # Synthetic software fixture only; three separated point clouds.
    rng = np.random.default_rng(9)
    values = np.vstack([rng.normal(center, .02, (50, 2)) for center in [[0, 0], [1, 1], [2, 0]]])
    config = dict(nmax=4, min_cluster_size=20, silhouette_threshold=.3, dc=.15,
                  dc_reduction=.9, max_no_improve_steps=5)
    first, second = iterative_dpc(values, config), iterative_dpc(values, config)
    np.testing.assert_array_equal(first.labels, second.labels)
    assert len(first.accepted) == 3
    accepted = np.concatenate(first.accepted)
    assert len(np.unique(accepted)) == len(accepted)
    assert len(accepted) + np.count_nonzero(first.labels == -1) == len(values)
    assigned, _ = assign_frames(values, first.accepted, np.arange(1, 4))
    assert len(assigned) == len(values)
    assert np.all(assigned > 0)


def test_resource_guard():
    with pytest.raises(ResourceLimit):
        Budget(max_seconds=-1).check()
    with pytest.raises(ResourceLimit):
        Budget(max_memory_gib=.0001).check()
