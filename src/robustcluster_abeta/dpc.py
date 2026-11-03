"""Iterative density-peaks clustering with auditable acceptance decisions."""

from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_samples

from .validation import Budget, InvalidInput, finite


@dataclass
class DPCResult:
    labels: np.ndarray
    accepted: list
    history: list
    decision: dict


def distance_matrix(values, budget, block=512):
    values = finite(values, "DPC features")
    n = len(values)
    budget.check(n*n*4 + min(block, n)*n*8)
    distance = np.empty((n, n), dtype=np.float32)
    for start in range(0, n, block):
        budget.check()
        distance[start:start+block] = cdist(values[start:start+block], values)
    np.fill_diagonal(distance, 0)
    return distance


def cutoff_density(distance, dc):
    if dc <= 0:
        raise InvalidInput("Cutoff must be positive")
    # Count one row at a time: no N×N float or bool kernel allocation.
    return np.array([np.count_nonzero(row <= dc) for row in distance], dtype=np.int64)


def density_delta(distance, rho):
    order = np.lexsort((np.arange(len(rho)), -rho))
    delta = np.zeros(len(rho))
    parent = np.full(len(rho), -1, dtype=int)
    delta[order[0]] = distance.max()
    for rank, point in enumerate(order[1:], 1):
        preceding = order[:rank]
        target = np.argmin(distance[point, preceding])
        parent[point] = preceding[target]
        delta[point] = distance[point, parent[point]]
    return delta, parent, order


def iterative_dpc(values, config, budget=None):
    values = finite(values, "DPC features")
    budget = budget or Budget()
    minimum = int(config["min_cluster_size"])
    nmax = int(config["nmax"])
    dc = float(config["dc"])
    reduction = float(config["dc_reduction"])
    threshold = float(config["silhouette_threshold"])
    if minimum < 2 or nmax < 2 or dc <= 0 or not 0 < reduction < 1 or not -1 <= threshold <= 1:
        raise InvalidInput("Invalid DPC parameters")
    labels = np.full(len(values), -1, dtype=int)
    accepted, history, decision = [], [], {}
    failures, iteration = 0, 0
    while failures < config["max_no_improve_steps"]:
        budget.check()
        remaining = np.flatnonzero(labels == -1)
        if len(remaining) < minimum:
            break
        iteration += 1
        distance = distance_matrix(values[remaining], budget)
        rho = cutoff_density(distance, dc)
        delta, parent, order = density_delta(distance, rho)
        ranking = np.lexsort((np.arange(len(rho)), -(rho*delta)))
        if iteration == 1:
            decision = {"indices": remaining.tolist(), "rho": rho.tolist(), "delta": delta.tolist()}
        best, good_best, best_centers = None, [], None
        for centers in range(min(nmax, len(remaining)-1), 1, -1):
            budget.check()
            trial = np.full(len(remaining), -1, dtype=int)
            selected = ranking[:centers]
            trial[selected] = np.arange(centers)
            for point in order:
                if trial[point] < 0 and parent[point] >= 0:
                    trial[point] = trial[parent[point]]
            if np.any(trial < 0):
                # Highest-density point should be a center; never use label[-1] as fallback.
                continue
            count = len(np.unique(trial))
            if not 2 <= count < len(trial):
                continue
            sil = silhouette_samples(distance, trial, metric="precomputed")
            good = [label for label in np.unique(trial)
                    if np.count_nonzero(trial == label) >= minimum and
                    sil[trial == label].mean() >= threshold]
            if len(good) > len(good_best):
                best, good_best, best_centers = trial.copy(), good, centers
        history.append({"iteration": iteration, "dc": dc, "remaining": len(remaining),
                        "acceptable_clusters": len(good_best), "selected_centers": best_centers})
        if good_best:
            failures = 0
            for label in good_best:
                members = remaining[best == label]
                labels[members] = len(accepted)
                accepted.append(members)
        else:
            failures += 1
        del distance
        dc *= reduction
        if dc <= np.finfo(float).tiny:
            break
    return DPCResult(labels, accepted, history, decision)
