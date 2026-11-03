"""Unweighted descriptor-space GMM sensitivity; never an equilibrium estimator."""

import itertools
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

from .io import FEATURES, read_descriptors
from .manifest import dump_json
from .validation import AnalysisFailure, InvalidInput, finite


def fit_scaler(fit_values, values):
    fit_values, values = finite(fit_values), finite(values)
    mean, scale = fit_values.mean(axis=0), fit_values.std(axis=0)
    if np.any(scale <= 0):
        raise InvalidInput("Constant fit feature")
    return (values - mean) / scale, {"mean": mean.tolist(), "scale": scale.tolist()}


def match_partitions(left, right):
    """Match by maximum overlap; absent families remain unmatched."""
    left, right = np.asarray(left), np.asarray(right)
    if left.ndim != 1 or left.shape != right.shape or not left.size:
        raise InvalidInput("Partitions must share nonempty frame identities")
    a, ai = np.unique(left, return_inverse=True)
    b, bi = np.unique(right, return_inverse=True)
    overlap = np.zeros((len(a), len(b)), dtype=int)
    np.add.at(overlap, (ai, bi), 1)
    rows, cols = linear_sum_assignment(-overlap)
    pairs = []
    for i, j in zip(rows, cols):
        intersection = int(overlap[i, j])
        union = int(overlap[i].sum() + overlap[:, j].sum() - intersection)
        pairs.append(
            {
                "left": int(a[i]),
                "right": int(b[j]),
                "overlap": intersection,
                "jaccard": intersection / union,
            }
        )
    return {
        "ari": float(adjusted_rand_score(left, right)),
        "matched_fraction": float(overlap[rows, cols].sum() / len(left)),
        "pairs": pairs,
        "unmatched_left": sorted(set(a.tolist()) - set(a[rows].tolist())),
        "unmatched_right": sorted(set(b.tolist()) - set(b[cols].tolist())),
    }


def experiment(config, run, budget):
    if config["mode"] != "robustness_extension":
        raise InvalidInput("GMM analysis is an extension only")
    spec = config["gmm"]
    if spec["fit_per_replica"] < 2 or not spec["master_seeds"]:
        raise InvalidInput("Require fit observations and model seeds")
    if len(set(spec["master_seeds"])) != len(spec["master_seeds"]):
        raise InvalidInput("Duplicate model seeds")
    table = read_descriptors(
        config["inputs"]["descriptors"], config["replicas"], config["interval_ps"]
    )
    rng = np.random.default_rng(spec["sampling_seed"])
    fit = []
    for _, part in table.groupby("replica_id"):
        if len(part) < spec["fit_per_replica"]:
            raise InvalidInput("Requested fit count exceeds available replica frames")
        fit.extend(rng.choice(part.index.to_numpy(), spec["fit_per_replica"], replace=False))
    fit = np.sort(fit)
    fit_flag = np.zeros(len(table), dtype=bool)
    fit_flag[fit] = True
    identities = table[["source_row", "source_line", "replica_id", "frame_index", "time_ps"]].copy()
    identities["used_for_fit"] = fit_flag
    identities.to_csv(run.path("tables", "frame_identities.csv.gz"), index=False)
    raw = table[FEATURES].to_numpy()
    standardized, scaling = fit_scaler(raw[fit], raw)
    dump_json(
        run.path("tables", "scaler.json"),
        dict(scaling, features=FEATURES, fit_source_rows=table.source_row.to_numpy()[fit].tolist()),
    )
    labels, convergence, model_rows, populations, parameters = {}, {}, [], [], []
    for k in spec["components"]:
        if not isinstance(k, int) or not 2 <= k < len(fit):
            raise InvalidInput("Invalid component count")
        for seed in spec["master_seeds"]:
            for space, columns in [("four", [0, 1, 2, 3]), ("three", [0, 1, 2])]:
                budget.check()
                x = standardized[:, columns]
                model = GaussianMixture(
                    n_components=k,
                    random_state=int(seed),
                    covariance_type=spec["covariance_type"],
                    reg_covar=spec["reg_covar"],
                    max_iter=spec["max_iter"],
                    n_init=spec["n_init"],
                    tol=spec["tol"],
                )
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always", ConvergenceWarning)
                    model.fit(x[fit])
                budget.check()
                predicted = model.predict(x).astype(np.int16)
                key = f"{space}_k{k}_seed{seed}"
                labels[key], convergence[key] = predicted, bool(model.converged_)
                model_rows.append(
                    {
                        "space": space,
                        "k": k,
                        "seed": seed,
                        "converged": bool(model.converged_),
                        "iterations": model.n_iter_,
                        "fit_bic": model.bic(x[fit]),
                        "observed_components": len(np.unique(predicted)),
                        "warnings": "; ".join(str(w.message) for w in caught),
                    }
                )
                parameters.append(
                    {
                        "key": key,
                        "weights": model.weights_.tolist(),
                        "means_standardized": model.means_.tolist(),
                        "covariances_standardized": model.covariances_.tolist(),
                    }
                )
                for replica, part in table.groupby("replica_id"):
                    lab = predicted[part.index]
                    for cluster in range(k):
                        populations.append(
                            {
                                "space": space,
                                "k": k,
                                "seed": seed,
                                "replica_id": replica,
                                "label": cluster,
                                "raw_fraction": float(np.mean(lab == cluster)),
                            }
                        )
                print(
                    f"{key}: converged={model.converged_}, iterations={model.n_iter_}", flush=True
                )
    np.savez_compressed(run.path("tables", "assignments.npz"), **labels)
    pd.DataFrame(model_rows).to_csv(run.path("tables", "models.csv"), index=False)
    pd.DataFrame(populations).to_csv(run.path("tables", "raw_populations.csv"), index=False)
    dump_json(run.path("tables", "model_parameters.json"), parameters)
    comparisons, overlaps, stability = [], [], []
    for k in spec["components"]:
        for seed in spec["master_seeds"]:
            a, b = f"four_k{k}_seed{seed}", f"three_k{k}_seed{seed}"
            if not (convergence[a] and convergence[b]):
                continue
            match = match_partitions(labels[a], labels[b])
            comparisons.append(
                {
                    "k": k,
                    "seed": seed,
                    "ari": match["ari"],
                    "matched_fraction": match["matched_fraction"],
                }
            )
            for pair in match["pairs"]:
                ma, mb = labels[a] == pair["left"], labels[b] == pair["right"]
                ca, cb = standardized[ma, :3].mean(axis=0), standardized[mb, :3].mean(axis=0)
                overlaps.append(
                    dict(
                        k=k,
                        seed=seed,
                        **pair,
                        centroid_shift_shared_standardized=float(np.linalg.norm(ca - cb)),
                        fraction_difference=float(mb.mean() - ma.mean()),
                    )
                )
            for label in match["unmatched_left"]:
                overlaps.append(dict(k=k, seed=seed, left=label, right=-1, unmatched=True))
            for label in match["unmatched_right"]:
                overlaps.append(dict(k=k, seed=seed, left=-1, right=label, unmatched=True))
        for space in ["four", "three"]:
            for s1, s2 in itertools.combinations(spec["master_seeds"], 2):
                a, b = f"{space}_k{k}_seed{s1}", f"{space}_k{k}_seed{s2}"
                if convergence[a] and convergence[b]:
                    stability.append(
                        {
                            "space": space,
                            "k": k,
                            "seed_a": s1,
                            "seed_b": s2,
                            "ari": float(adjusted_rand_score(labels[a], labels[b])),
                        }
                    )
    if not comparisons:
        raise AnalysisFailure("No converged paired models; no valid ablation comparison")
    comparison = pd.DataFrame(comparisons)
    comparison.to_csv(run.path("tables", "ablation.csv"), index=False)
    pd.DataFrame(overlaps).to_csv(run.path("tables", "matched_clusters.csv"), index=False)
    pd.DataFrame(stability).to_csv(run.path("tables", "seed_stability.csv"), index=False)
    summary = {
        "frames": len(table),
        "fit_frames": len(fit),
        "models": len(model_rows),
        "converged_models": sum(convergence.values()),
        "paired_comparisons": len(comparison),
        "evaluation": "all frames, including fit",
        "independence_claim": False,
        "equilibrium_weights": False,
        "ari_by_k": {
            str(k): {
                "min": float(g.ari.min()),
                "median": float(g.ari.median()),
                "max": float(g.ari.max()),
            }
            for k, g in comparison.groupby("k")
        },
    }
    dump_json(run.path("tables", "summary.json"), summary)
    budget.check()
    return summary
