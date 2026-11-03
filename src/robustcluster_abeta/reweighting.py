"""Final-bias and explicitly gated time-dependent statistical weights."""

import numpy as np
import pandas as pd
from scipy.special import logsumexp

from .validation import BlockedAnalysis, InvalidInput, finite

R_KJ_MOL_K = 0.008314462618


def final_bias_log_weights(energy, temperature=310.0, gamma=10.0):
    energy = finite(energy, "interpolated FES")
    if not np.isfinite([temperature, gamma]).all() or temperature <= 0 or gamma <= 1:
        raise InvalidInput("Require T>0 and WT bias factor gamma>1")
    return -(1-1/gamma)*energy/(R_KJ_MOL_K*temperature)


def time_dependent_log_weights(rbias, temperature, units=None, provenance=None):
    if units != "kJ/mol" or not provenance:
        raise BlockedAnalysis("metad.rbias units and generating provenance must be established")
    if not np.isfinite(temperature) or temperature <= 0:
        raise InvalidInput("Temperature must be positive")
    return finite(rbias, "metad.rbias")/(R_KJ_MOL_K*temperature)


def normalize_replicas(log_weights, replicas):
    log_weights = finite(log_weights, "log weights")
    replicas = np.asarray(replicas)
    if replicas.shape != log_weights.shape or log_weights.ndim != 1:
        raise InvalidInput("Weights and replica IDs must be aligned 1D arrays")
    if pd.isna(replicas).any():
        raise InvalidInput("Missing replica identity")
    normalized = np.empty_like(log_weights)
    unique = np.unique(replicas)
    for replica in unique:
        mask = replicas == replica
        normalized[mask] = np.exp(log_weights[mask]-logsumexp(log_weights[mask]))
    return normalized, normalized/len(unique)


def frame_weights(table, fes, temperature=310.0, gamma=10.0):
    result = table[["replica_id", "source_row", "source_line", "frame_index", "time_ps"]].copy()
    result["alpha_cv"] = table.nAlpha.to_numpy()/1.1
    result["beta_cv"] = table.nBeta.to_numpy()/2.5
    result["interpolated_F_kJ_mol"] = fes.interpolate(result.alpha_cv, result.beta_cv)
    logw = final_bias_log_weights(result.interpolated_F_kJ_mol, temperature, gamma)
    result["raw_log_weight"] = logw
    with np.errstate(over="ignore", under="ignore"):
        raw = np.exp(logw)
    status = np.full(len(raw), "representable", dtype=object)
    status[raw == 0] = "underflow"
    status[~np.isfinite(raw)] = "overflow"
    raw[~np.isfinite(raw)] = np.nan  # Explicit missing CSV value with status, never used downstream.
    result["raw_weight"] = raw
    result["raw_weight_status"] = status
    result["replica_normalized_weight"], result["pooled_weight"] = normalize_replicas(logw, table.replica_id)
    return result
