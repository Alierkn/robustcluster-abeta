"""Manifest-backed analysis orchestration; no work occurs at import time."""

import copy
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .consensus import assign_frames, merge_clusters, wasserstein_matrix
from .dpc import iterative_dpc
from .fes import read_fes
from .io import DESCRIPTORS, FEATURES, read_descriptors
from .manifest import dump_json, sha256
from .preprocessing import make_groups, transform_features
from .reweighting import frame_weights, normalize_replicas, time_dependent_log_weights
from .stability import ari_matrix, compare_partitions
from .statistics import (block_bootstrap_population, correlation_diagnostic, kish_ess,
                         population_summary, weighted_moments)
from .validation import AnalysisFailure, BlockedAnalysis, InvalidInput


def read_table(config):
    return read_descriptors(config["inputs"]["descriptors"], config["replicas"], config["interval_ps"])


def validate_configuration(config):
    if config["mode"] not in {"paper_reproduction", "robustness_extension"}:
        raise InvalidInput("Unknown scientific mode")
    if config["mode"] == "paper_reproduction":
        if config["replicas"] != 3 or config["interval_ps"] != [1000000, 3000000]:
            raise InvalidInput("Baseline requires three replicas and the 1–3 microsecond interval")
        if config["features"] != FEATURES or config["representation"] != "minmax" or config["wasserstein"] != "raw":
            raise InvalidInput("Baseline feature/scaling changes require robustness_extension mode")
        required = {"nmax": 10, "min_cluster_size": 300, "silhouette_threshold": 0.3,
                    "dc": 1.3, "dc_reduction": 0.9, "max_no_improve_steps": 5}
        if config["dpc"] != required or config["temperature_K"] != 310 or config["gamma_bias"] != 10:
            raise InvalidInput("Published parameters differ; declare a robustness extension instead")
    execution = config["execution"]
    if not execution["enabled"]:
        raise BlockedAnalysis("Full execution is held until resource estimates are reviewed")
    if execution["max_seconds"] <= 0 or execution["max_memory_gib"] <= 0:
        raise InvalidInput("Resource limits must be positive")


def validate(config, run, budget):
    table = read_table(config)
    summary = []
    for replica, part in table.groupby("replica_id", sort=True):
        summary.append({"replica_id": int(replica), "frames": len(part), "start_ps": part.time_ps.min(),
                        "end_ps": part.time_ps.max(), "spacing_ps": np.diff(part.time_ps).min(),
                        "uniform_spacing": bool(np.allclose(np.diff(part.time_ps), np.diff(part.time_ps)[0]))})
    pd.DataFrame(summary).to_csv(run.path("tables", "input_validation.csv"), index=False)
    dump_json(run.path("tables", "input_schema.json"), {"header": table.attrs["original_header"],
                                                        "units_status": table.attrs["units_status"],
                                                        "shape": list(table.shape)})
    return {"frames": len(table), "replicas": len(summary), "fes_validated": False}


def diagnostics(config, run, budget):
    table = read_table(config)
    values = table[FEATURES].to_numpy()
    correlations = table[FEATURES].corr()
    correlations.to_csv(run.path("tables", "feature_correlation.csv"))
    _, pca = transform_features(values, "standardized_pca")
    dump_json(run.path("tables", "pca.json"), pca)
    table.groupby("replica_id")[DESCRIPTORS].agg(["count", "mean", "std", "min", "max"]).to_csv(run.path("tables", "raw_descriptors.csv"))
    estimates, acfs, histograms = [], [], []
    for feature in DESCRIPTORS:
        edges = np.histogram_bin_edges(table[feature], bins=60)
        for replica, part in table.groupby("replica_id"):
            counts, _ = np.histogram(part[feature], bins=edges)
            for left, right, count in zip(edges[:-1], edges[1:], counts):
                histograms.append({"descriptor": feature, "replica_id": int(replica), "left": left,
                                   "right": right, "count": int(count), "density": count/len(part)/(right-left)})
    pd.DataFrame(histograms).to_csv(run.path("tables", "raw_histograms.csv"), index=False)
    for replica, part in table.groupby("replica_id"):
        spacing = np.diff(part.time_ps)
        if not np.allclose(spacing, spacing[0], rtol=1e-8, atol=1e-8):
            raise InvalidInput("ACF requires uniform sampling; resampling is not performed implicitly")
        for feature in FEATURES:
            budget.check()
            acf, estimate = correlation_diagnostic(part[feature].to_numpy(), spacing[0])
            estimate.update(replica_id=int(replica), descriptor=feature)
            estimates.append(estimate)
            # Display the first half of the observation window with bounded plot density;
            # the estimator above uses the full un-decimated autocorrelation sequence.
            for lag in np.unique(np.linspace(0, len(acf)//2, min(len(acf)//2+1, 2001), dtype=int)):
                acfs.append({"replica_id": int(replica), "descriptor": feature,
                             "lag_frames": lag, "lag_ps": lag*spacing[0], "acf": acf[lag]})
    pd.DataFrame(estimates).to_csv(run.path("tables", "sampling_diagnostics.csv"), index=False)
    pd.DataFrame(acfs).to_csv(run.path("tables", "autocorrelations.csv"), index=False)
    from .plotting import plot_diagnostics
    plot_diagnostics(run)
    return {"frames": len(table), "interpretation": "unweighted biased-stream diagnostics",
            "weights": "BLOCKED: complete FES missing; rbias provenance unverified"}


def cluster_pipeline(table, config, seed, budget):
    feature_names = config["features"]
    raw = table[feature_names].to_numpy()
    features, transform = transform_features(raw, config["representation"])
    sequence = np.random.SeedSequence(int(seed))
    child = sequence.spawn(1)[0]
    groups = make_groups(len(table), config["execution"]["group_size"], np.random.default_rng(child))
    maximum = config["execution"]["max_groups"]
    chosen = groups if maximum is None else groups[:maximum]
    accepted, histories, decisions = [], [], []
    for number, indices in enumerate(chosen):
        budget.check()
        result = iterative_dpc(features[indices], config["dpc"], budget)
        accepted.extend(indices[cluster] for cluster in result.accepted)
        histories.extend(dict(group=number, **row) for row in result.history)
        decisions.append(dict(group=number, source_rows=table.source_row.to_numpy()[indices].tolist(), **result.decision))
    if not accepted:
        raise AnalysisFailure("No acceptable local clusters; no consensus or population estimate produced")
    if config["wasserstein"] == "raw":
        consensus_values = raw
    elif config["wasserstein"] == "normalized":
        consensus_values, _ = transform_features(raw, "minmax")
    else:
        raise InvalidInput("Wasserstein mode must be raw or normalized")
    distances = wasserstein_matrix(consensus_values, accepted)
    families, hierarchy, elbow = merge_clusters(distances, config["consensus"]["spline_s"])
    labels, centers = assign_frames(features, accepted, families, budget)
    return {"labels": labels, "centroids": centers, "accepted": accepted, "local_families": families,
            "distance": distances, "linkage": hierarchy, "elbow": elbow, "transform": transform,
            "histories": histories, "decisions": decisions, "group_count": len(chosen),
            "training_frames": sum(map(len, chosen)), "child_spawn_key": list(child.spawn_key)}


def load_weighted_inputs(config):
    # Validate FES first, before spending time clustering; never use rbias as a substitute.
    fes = read_fes(config["inputs"]["fes"], config["inputs"]["fes_energy_unit"], config["inputs"]["fes_provenance"])
    table = read_table(config)
    weights = frame_weights(table, fes, config["temperature_K"], config["gamma_bias"])
    return table, weights, fes


def save_partition(run, prefix, table, weights, result):
    joined = weights.copy()
    joined["final_cluster_label"] = result["labels"]
    joined.to_csv(run.path("tables", f"{prefix}_frames.csv.gz"), index=False)
    np.savez_compressed(run.path("tables", f"{prefix}_clustering.npz"), labels=result["labels"],
                        centroids=result["centroids"], distance=result["distance"], linkage=result["linkage"])
    dump_json(run.path("tables", f"{prefix}_algorithm.json"),
              {key: result[key] for key in ["elbow", "transform", "histories", "decisions", "group_count", "training_frames", "child_spawn_key"]})
    per_replica, relevance = population_summary(result["labels"], table.replica_id, weights.replica_normalized_weight)
    per_replica.to_csv(run.path("tables", f"{prefix}_replica_populations.csv"), index=False)
    relevance.to_csv(run.path("tables", f"{prefix}_populations.csv"), index=False)
    summaries = []
    for cluster in np.unique(result["labels"]):
        mask = result["labels"] == cluster
        for descriptor in DESCRIPTORS:
            mean, width = weighted_moments(table[descriptor].to_numpy()[mask], weights.pooled_weight.to_numpy()[mask])
            summaries.append({"cluster": int(cluster), "descriptor": descriptor, "weighted_mean": mean,
                              "weighted_distribution_sd": width, "raw_frames": int(mask.sum())})
    pd.DataFrame(summaries).to_csv(run.path("tables", f"{prefix}_weighted_descriptors.csv"), index=False)
    return relevance


def reproduce(config, run, budget):
    table, weights, fes = load_weighted_inputs(config)
    result = cluster_pipeline(table, config, config["master_seed"], budget)
    relevance = save_partition(run, "baseline", table, weights, result)
    block_lengths, ess_rows = {}, []
    for replica, part in table.groupby("replica_id"):
        spacing = np.diff(part.time_ps)
        if not np.allclose(spacing, spacing[0]):
            raise InvalidInput("Uniform time spacing required for bootstrap block selection")
        estimates = [correlation_diagnostic(part[f].to_numpy(), spacing[0])[1] for f in FEATURES]
        block_lengths[int(replica)] = min(len(part), max(1, int(np.ceil(2*max(e["statistical_inefficiency"] for e in estimates)))))
        ess_rows.append({"replica_id": int(replica), "raw_frames": len(part),
                         "kish_weight_ess": kish_ess(weights.loc[part.index, "replica_normalized_weight"]),
                         "block_length": block_lengths[int(replica)],
                         "all_correlation_estimates_reliable": all(e["reliable_heuristic"] for e in estimates)})
    boot_rng = np.random.default_rng(np.random.SeedSequence(config["master_seed"], spawn_key=(1,)))
    intervals, draws = block_bootstrap_population(result["labels"], table.replica_id,
        weights.replica_normalized_weight.to_numpy(), block_lengths, boot_rng, config["bootstrap_draws"], budget)
    relevance.merge(intervals, on="cluster").to_csv(run.path("tables", "baseline_populations.csv"), index=False)
    pd.DataFrame(ess_rows).to_csv(run.path("tables", "weight_ess.csv"), index=False)
    np.save(run.path("tables", "population_bootstrap.npy"), draws)
    np.savez_compressed(run.path("tables", "fes_grid.npz"), alpha=fes.alpha, beta=fes.beta, energy=fes.energy)
    from .plotting import plot_reproduction
    plot_reproduction(run)
    return {"families": len(np.unique(result["labels"])), "frames": len(table), "seed": config["master_seed"],
            "block_lengths": block_lengths, "bootstrap_scope": "fixed fitted partition and fixed supplied FES; within-replica moving blocks"}


def robustness(config, run, budget, experiment):
    if config["mode"] != "robustness_extension":
        raise InvalidInput("Robustness command requires robustness_extension mode")
    if experiment in {"dpa", "shapegmm", "external_validation"}:
        raise BlockedAnalysis(f"{experiment} is a deferred optional benchmark; no results claimed")
    table, weights, _ = load_weighted_inputs(config)
    if experiment in {"seeds", "seed-pilot"}:
        count = config.get("seed_pilot_count", 5) if experiment == "seed-pilot" else config["execution"]["seeds"]
        seeds = [config["master_seed"]] + [int(s.generate_state(1)[0]) for s in
                  np.random.SeedSequence(config["master_seed"]).spawn(count-1)]
        variants = [(f"seed_{seed}", config, seed) for seed in seeds]
    elif experiment == "features":
        variants = [("baseline", config, config["master_seed"])]
        for name, features, representation in [
            ("without_sasa", ["nAlpha", "nBeta", "Rg"], "minmax"),
            ("without_rg", ["nAlpha", "nBeta", "SASA"], "minmax"),
            ("standardized_pca", FEATURES, "standardized_pca"),
            ("whitened_pca", FEATURES, "whitened_pca")]:
            variant = copy.deepcopy(config)
            variant.update(features=features, representation=representation)
            variants.append((name, variant, config["master_seed"]))
    elif experiment == "wasserstein":
        normalized = copy.deepcopy(config)
        normalized["wasserstein"] = "normalized"
        variants = [("raw", config, config["master_seed"]), ("normalized", normalized, config["master_seed"])]
    elif experiment == "reweighting":
        # No clustering until optional rbias provenance gate also passes.
        logw = time_dependent_log_weights(table.metad_rbias, config["temperature_K"],
                   config["inputs"]["rbias_energy_unit"], config["inputs"]["rbias_provenance"])
        result = cluster_pipeline(table, config, config["master_seed"], budget)
        save_partition(run, "final_bias", table, weights, result)
        alternative = weights.copy()
        alternative["replica_normalized_weight"], alternative["pooled_weight"] = normalize_replicas(logw, table.replica_id)
        alternative["raw_log_weight"] = logw
        # Avoid leaving final-bias raw weights associated with the alternative formula.
        with np.errstate(over="ignore", under="ignore"):
            raw = np.exp(logw)
        status = np.where(np.isinf(raw), "overflow", np.where(raw == 0, "underflow", "representable"))
        raw[~np.isfinite(raw)] = np.nan
        alternative["raw_weight"], alternative["raw_weight_status"] = raw, status
        save_partition(run, "time_dependent", table, alternative, result)
        histograms = []
        for feature in FEATURES:
            edges = np.histogram_bin_edges(table[feature], bins=60)
            for name, weighted in [("final_bias", weights), ("time_dependent", alternative)]:
                probability, _ = np.histogram(table[feature], bins=edges, weights=weighted.pooled_weight)
                for left, right, prob in zip(edges[:-1], edges[1:], probability):
                    histograms.append(dict(descriptor=feature, method=name, left=left, right=right, probability=prob))
        pd.DataFrame(histograms).to_csv(run.path("tables", "reweighting_histograms.csv"), index=False)
        from .plotting import plot_reweighting
        plot_reweighting(run)
        return {"comparison": "same fitted partition, two explicitly distinct weight estimators"}
    else:
        raise InvalidInput(f"Unknown robustness experiment: {experiment}")
    results, populations = [], []
    for name, variant, seed in variants:
        budget.check()
        result = cluster_pipeline(table, variant, seed, budget)
        population = save_partition(run, name, table, weights, result)
        populations.append(population)
        results.append(result)
    partitions = [result["labels"] for result in results]
    names = [variant[0] for variant in variants]
    pd.DataFrame(ari_matrix(partitions), index=names, columns=names).to_csv(run.path("tables", "ari_matrix.csv"))
    rows = []
    # Centroids for cross-representation comparisons are computed in the same original units.
    raw = table[FEATURES].to_numpy()
    scale = np.ptp(raw, axis=0)
    for name, result, population in zip(names, results, populations):
        ari, matches = compare_partitions(partitions[0], result["labels"])
        for record in matches.to_dict("records"):
            a, b = record["reference_cluster"], record["other_cluster"]
            row = dict(record, variant=name, ari=ari, population=0.0, centroid_distance=None)
            if pd.notna(b):
                row["population"] = float(population.loc[population.cluster == b, "mean"].iloc[0])
            if pd.notna(a) and pd.notna(b):
                ca, cb = raw[partitions[0] == a].mean(axis=0), raw[result["labels"] == b].mean(axis=0)
                row["centroid_distance"] = float(np.linalg.norm((ca-cb)/scale))
            rows.append(row)
    pd.DataFrame(rows).to_csv(run.path("tables", "cluster_stability.csv"), index=False)
    from .plotting import plot_stability
    plot_stability(run)
    identity_path = run.path("tables", "frame_identity.csv")
    table[["replica_id", "source_row", "frame_index", "time_ps"]].to_csv(identity_path, index=False)
    return {"variants": names, "master_seeds": [int(v[2]) for v in variants],
            "frame_identity_sha256": sha256(identity_path),
            "centroid_distance_units": "Euclidean in pooled baseline min-max descriptor space"}


def rebuild_figures(config, run, budget, source_manifest):
    source = Path(source_manifest)
    manifest = json.loads(source.read_text())
    if manifest["status"] != "SUCCESS":
        raise InvalidInput("Figures may only be rebuilt from a SUCCESS manifest")
    source_root = source.parent.parent.parent
    import shutil
    for output in manifest["outputs"]:
        path = source_root/output["filename"]
        if sha256(path) != output["sha256"]:
            raise InvalidInput(f"Output hash mismatch: {path.name}")
        if "/tables/" in output["filename"]:
            shutil.copy2(path, run.path("tables", path.name))
    command = manifest["command"]
    from .plotting import plot_diagnostics, plot_reproduction, plot_reweighting, plot_stability
    if command == "diagnostics":
        plot_diagnostics(run)
    elif command == "reproduce":
        plot_reproduction(run)
    elif command == "robustness":
        (plot_reweighting if manifest["experiment"] == "reweighting" else plot_stability)(run)
    else:
        raise InvalidInput("Source run has no supported scientific figures")
    return {"source_manifest": source.name, "source_manifest_sha256": sha256(source)}
