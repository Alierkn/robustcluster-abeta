"""Consensus of acceptable clusters using marginal Wasserstein distances."""

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.interpolate import UnivariateSpline
from scipy.spatial.distance import cdist, squareform
from scipy.stats import wasserstein_distance

from .validation import AnalysisFailure, InvalidInput, finite


def wasserstein_matrix(descriptors, clusters):
    descriptors = finite(descriptors, "consensus descriptors")
    if any(len(c) == 0 for c in clusters):
        raise InvalidInput("Consensus cannot contain empty or residual clusters")
    distance = np.zeros((len(clusters), len(clusters)))
    for i, left in enumerate(clusters):
        for j in range(i):
            right = clusters[j]
            marginal = [wasserstein_distance(descriptors[left, f], descriptors[right, f])
                        for f in range(descriptors.shape[1])]
            distance[i, j] = distance[j, i] = np.linalg.norm(marginal)
    return distance


def merge_clusters(distance, smoothing=5.0):
    finite(distance, "consensus distance matrix")
    if len(distance) < 5:
        raise AnalysisFailure("At least five accepted local clusters are required for the cubic elbow heuristic")
    hierarchy = linkage(squareform(distance, checks=True), method="average")
    heights = hierarchy[:, 2]
    if np.ptp(heights) <= 0:
        raise AnalysisFailure("Merge distances have no discernible elbow")
    steps = np.arange(len(heights))
    spline = UnivariateSpline(steps, heights, s=smoothing)
    derivative = spline.derivative(2)(steps)
    stop = int(0.9*len(steps))
    elbow = int(np.argmax(derivative[:stop]))
    threshold = float(heights[elbow])
    groups = fcluster(hierarchy, threshold, criterion="distance")
    return groups, hierarchy, {"elbow_index": elbow, "threshold": threshold,
                               "spline_s": smoothing, "second_derivative": derivative.tolist()}


def assign_frames(features, local_clusters, family_labels, budget=None):
    features = finite(features, "assignment features")
    if not local_clusters or len(local_clusters) != len(family_labels):
        raise AnalysisFailure("No aligned acceptable clusters for final assignment")
    families = np.unique(family_labels)
    centroids = np.vstack([features[np.concatenate([local_clusters[i] for i in
                           np.flatnonzero(family_labels == family)])].mean(axis=0)
                           for family in families])
    assigned = np.empty(len(features), dtype=int)
    for start in range(0, len(features), 8192):
        if budget:
            budget.check()
        assigned[start:start+8192] = families[np.argmin(cdist(features[start:start+8192], centroids), axis=1)]
    return assigned, centroids
