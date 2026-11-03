"""Explicit, serializable feature transformations and seeded disjoint groups."""

import numpy as np
from sklearn.decomposition import PCA

from .validation import InvalidInput, finite


def transform_features(values, representation="minmax"):
    values = finite(values, "features")
    if values.ndim != 2:
        raise InvalidInput("Features must be a matrix")
    span = np.ptp(values, axis=0)
    if np.any(span <= 0):
        raise InvalidInput("Constant features cannot be normalized")
    if representation == "minmax":
        offset = values.min(axis=0)
        return (values-offset)/span, {"kind": representation, "offset": offset.tolist(), "scale": span.tolist()}
    if representation not in {"standardized_pca", "whitened_pca"}:
        raise InvalidInput(f"Unknown representation: {representation}")
    mean, std = values.mean(axis=0), values.std(axis=0)
    standardized = (values-mean)/std
    if np.linalg.matrix_rank(standardized) < values.shape[1]:
        raise InvalidInput("Rank-deficient feature space; PCA whitening is not defined")
    pca = PCA(n_components=values.shape[1], whiten=representation == "whitened_pca", svd_solver="full")
    projected = pca.fit_transform(standardized)
    return projected, {"kind": representation, "offset": mean.tolist(), "scale": std.tolist(), "components": pca.components_.tolist(), "explained_variance": pca.explained_variance_.tolist(), "explained_variance_ratio": pca.explained_variance_ratio_.tolist()}


def make_groups(n_frames, group_size, rng):
    if n_frames < 1 or group_size < 2:
        raise InvalidInput("Invalid frame count or group size")
    shuffled = rng.permutation(n_frames)
    groups = [a.copy() for a in np.array_split(shuffled, np.arange(group_size, n_frames, group_size))]
    # Source-informed small-tail redistribution without the legacy seed-list limit.
    if len(groups) > 1 and len(groups[-1]) <= 10:
        tail = groups.pop()
        for i, index in enumerate(tail):
            groups[i % len(groups)] = np.r_[groups[i % len(groups)], index]
    return groups
