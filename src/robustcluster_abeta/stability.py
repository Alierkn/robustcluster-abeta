"""Partition comparisons that retain frame identity and unmatched families."""

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import adjusted_rand_score

from .validation import InvalidInput


def aligned_partitions(reference_ids, reference, other_ids, other):
    reference_ids, other_ids = np.asarray(reference_ids), np.asarray(other_ids)
    if len(np.unique(reference_ids)) != len(reference_ids) or len(np.unique(other_ids)) != len(other_ids):
        raise InvalidInput("Duplicate frame identities in partition comparison")
    if len(reference_ids) != len(other_ids) or set(reference_ids) != set(other_ids):
        raise InvalidInput("Partitions must cover exactly the same frame identities")
    other = pd.Series(np.asarray(other), index=other_ids).loc[reference_ids].to_numpy()
    return np.asarray(reference), other


def compare_partitions(reference, other):
    reference, other = np.asarray(reference), np.asarray(other)
    if reference.shape != other.shape or reference.ndim != 1 or len(reference) == 0:
        raise InvalidInput("Aligned nonempty partitions required")
    left, right = np.unique(reference), np.unique(other)
    overlap = np.array([[np.count_nonzero((reference == a) & (other == b)) for b in right] for a in left])
    rows, cols = linear_sum_assignment(-overlap)
    matches = []
    matched_left, matched_right = set(), set()
    for row, col in zip(rows, cols):
        if overlap[row, col] == 0:
            continue
        a, b = left[row], right[col]
        union = np.count_nonzero((reference == a) | (other == b))
        matches.append({"reference_cluster": int(a), "other_cluster": int(b),
                        "intersection": int(overlap[row, col]), "jaccard": overlap[row, col]/union,
                        "status": "matched"})
        matched_left.add(a)
        matched_right.add(b)
    for a in left:
        if a not in matched_left:
            matches.append({"reference_cluster": int(a), "other_cluster": None, "intersection": 0,
                            "jaccard": 0.0, "status": "reference_unmatched"})
    for b in right:
        if b not in matched_right:
            matches.append({"reference_cluster": None, "other_cluster": int(b), "intersection": 0,
                            "jaccard": 0.0, "status": "other_unmatched"})
    return float(adjusted_rand_score(reference, other)), pd.DataFrame(matches)


def ari_matrix(partitions):
    return np.array([[adjusted_rand_score(a, b) for b in partitions] for a in partitions])
