"""Biased-stream correlation diagnostics and replica-aware weighted statistics."""

import numpy as np
import pandas as pd
from scipy.fft import irfft, next_fast_len, rfft

from .validation import AnalysisFailure, InvalidInput, finite


def weighted_moments(values, weights):
    values, weights = finite(values), finite(weights, "weights")
    if values.shape != weights.shape or values.ndim != 1 or np.any(weights < 0) or weights.sum() <= 0:
        raise InvalidInput("Aligned 1D values and nonnegative nonzero weights required")
    normalized = weights/weights.sum()
    mean = np.dot(normalized, values)
    variance = np.dot(normalized, (values-mean)**2)
    return float(mean), float(np.sqrt(max(variance, 0)))


def kish_ess(weights):
    weights = finite(weights, "ESS weights")
    if np.any(weights < 0) or weights.max() <= 0:
        raise InvalidInput("Nonnegative nonzero weights required")
    stable = weights/weights.max()
    return float(stable.sum()**2/np.dot(stable, stable))


def correlation_diagnostic(values, spacing):
    values = finite(values, "correlation series")
    if len(values) < 4 or spacing <= 0:
        raise InvalidInput("Correlation needs at least four regularly spaced observations")
    centered = values-values.mean()
    if np.dot(centered, centered) == 0:
        raise InvalidInput("Autocorrelation is undefined for a constant series")
    n = len(values)
    size = next_fast_len(2*n)
    spectrum = rfft(centered, size)
    covariance = irfft(spectrum*spectrum.conjugate(), size)[:n]/n
    acf = covariance/covariance[0]
    pairs = acf[1:1+2*((n-1)//2)].reshape(-1, 2).sum(axis=1)
    stop = np.flatnonzero(pairs <= 0)
    limit = int(stop[0]) if len(stop) else len(pairs)
    positive = np.minimum.accumulate(pairs[:limit])
    inefficiency = max(1.0, float(1+2*positive.sum()))
    drift = abs(values[:n//2].mean()-values[n//2:].mean())/values.std()
    reliable = bool(n >= 50*inefficiency and len(stop) and drift <= 0.25)
    return acf, {"raw_frames": n, "statistical_inefficiency": inefficiency,
                 "tau_int_frames": inefficiency/2, "tau_int_ps": spacing*inefficiency/2,
                 "correlation_ess": n/inefficiency, "integration_lag": 2*limit,
                 "half_mean_difference_in_sd": drift, "reliable_heuristic": reliable,
                 "interpretation": "biased-stream sampling diagnostic; not physical kinetics"}


def population_summary(labels, replicas, replica_weights):
    labels, replicas = np.asarray(labels), np.asarray(replicas)
    weights = finite(replica_weights, "replica weights")
    if labels.shape != replicas.shape or weights.shape != labels.shape:
        raise InvalidInput("Population arrays must have identical frame alignment")
    if np.any(labels < 0) or np.any(weights < 0):
        raise InvalidInput("Final labels and weights cannot be negative")
    rows = []
    for replica in np.unique(replicas):
        mask = replicas == replica
        if not np.isclose(weights[mask].sum(), 1):
            raise InvalidInput("Replica weights must each sum to one")
        for cluster in np.unique(labels):
            rows.append({"replica_id": int(replica), "cluster": int(cluster),
                         "population": float(weights[mask & (labels == cluster)].sum())})
    per_replica = pd.DataFrame(rows)
    summary = per_replica.groupby("cluster").population.agg(["mean", "std", "count"]).reset_index()
    summary["replica_sem"] = summary["std"]/np.sqrt(summary["count"])
    return per_replica, summary


def block_bootstrap_population(labels, replicas, weights, block_lengths, rng, draws=500, budget=None):
    labels, replicas, weights = np.asarray(labels), np.asarray(replicas), finite(weights)
    if draws < 2 or not (labels.shape == replicas.shape == weights.shape):
        raise InvalidInput("Invalid bootstrap dimensions or number of draws")
    if labels.ndim != 1 or np.any(labels < 0) or np.any(weights < 0):
        raise InvalidInput("Bootstrap requires assigned 1D labels and nonnegative weights")
    families = np.unique(labels)
    records = np.zeros((draws, len(families)))
    unique = np.unique(replicas)
    for replica in unique:
        indices = np.flatnonzero(replicas == replica)
        block = int(block_lengths[int(replica)])
        n = len(indices)
        if not 1 <= block <= n:
            raise InvalidInput("Bootstrap block length outside replica bounds")
        for iteration in range(draws):
            if budget:
                budget.check()
            starts = rng.integers(0, n-block+1, size=int(np.ceil(n/block)))
            sampled = indices[(starts[:, None]+np.arange(block)).ravel()[:n]]
            selected_weights = weights[sampled]
            total = selected_weights.sum()
            if total <= 0:
                raise AnalysisFailure("A resampled replica has zero representable weight")
            for column, family in enumerate(families):
                records[iteration, column] += selected_weights[labels[sampled] == family].sum()/total/len(unique)
    lower, upper = np.quantile(records, [0.025, 0.975], axis=0)
    return pd.DataFrame({"cluster": families, "bootstrap_low": lower, "bootstrap_high": upper}), records
