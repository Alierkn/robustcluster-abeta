"""Replot saved, hash-verified results for the rebuilt report; no model fitting."""
import json
from pathlib import Path
import resource
import sys

import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from robustcluster_abeta.manifest import Run, dump_json, sha256

ROOT = Path(__file__).resolve().parents[1]
source_ids = {"diagnostics": "20260921T011959-583b4421", "gmm": "20261007T104141-f0143175"}
config = {"project_root": str(ROOT), "inputs": {}, "source_runs": source_ids,
          "figure_width_inches": 6.0, "plot_font": "DejaVu Serif",
          "scientific_mode": "saved_results_presentation", "model_fitting": False}
run = Run(config, "editorial-figures")
run.data["script_sha256"] = sha256(__file__)
run.data["source_manifests"] = {}
run.data["font_files"] = {}
dump_json(run.file, run.data)
try:
    for name, ident in source_ids.items():
        path = ROOT / "results/manifests" / f"{ident}.json"
        record = json.loads(path.read_text())
        if record["status"] != "SUCCESS" or record["command"] != ("diagnostics" if name == "diagnostics" else "gmm-ablation"):
            raise ValueError(f"Invalid source status or command: {path}")
        for item in record["outputs"]:
            if sha256(ROOT / item["filename"]) != item["sha256"]:
                raise ValueError(f"Source output changed: {item['filename']}")
        run.data["source_manifests"][name] = {"filename": str(path.relative_to(ROOT)), "sha256": sha256(path)}
    plt.style.use(ROOT / "src/robustcluster_abeta/publication.mplstyle")
    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10, "axes.labelsize": 9.5, "axes.titlesize": 10.5,
                         "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 8.5})
    run.data["resolved_serif"] = Path(font_manager.findfont(font_manager.FontProperties(family="serif"))).name
    run.data["style_sha256"] = sha256(ROOT / "src/robustcluster_abeta/publication.mplstyle")
    dump_json(run.file, run.data)
    diag = ROOT / "results/tables" / source_ids["diagnostics"]
    gmm = ROOT / "results/tables" / source_ids["gmm"]
    corr = pd.read_csv(diag / "feature_correlation.csv", index_col=0)
    pca = json.loads((diag / "pca.json").read_text())
    ratios = np.asarray(pca["explained_variance_ratio"], dtype=float)
    if corr.shape != (4, 4) or not np.isfinite(corr.to_numpy()).all() or not np.isfinite(ratios).all():
        raise ValueError("Invalid diagnostic values")
    if ratios.shape != (4,) or not np.isclose(ratios.sum(), 1):
        raise ValueError("Invalid PCA spectrum")
    ablation = pd.read_csv(gmm / "ablation.csv")
    stability = pd.read_csv(gmm / "seed_stability.csv")
    if len(ablation) != 25 or ablation.duplicated(["k", "seed"]).any() or len(stability) != 100:
        raise ValueError("Unexpected GMM comparison design")
    if not np.isfinite(ablation.ari).all() or not np.isfinite(stability.ari).all():
        raise ValueError("Invalid ARI value")
    colors = ["#173A5E", "#2E6F73", "#A95542"]

    def save(figure, stem):
        for extension in ["pdf", "svg"]:
            figure.savefig(run.path("figures", f"{stem}.{extension}"))
        plt.close(figure)

    fig, axes = plt.subplots(1, 2, figsize=(6, 3.05), layout="constrained")
    labels = [r"$n_\alpha$", r"$n_\beta$", r"$R_g$", "SASA"]
    im = axes[0].imshow(corr.to_numpy(), vmin=-1, vmax=1, cmap="RdBu_r")
    axes[0].set_xticks(range(4), labels)
    axes[0].set_yticks(range(4), labels)
    axes[0].set_title("A  Feature correlations", loc="left")
    for i in range(4):
        for j in range(4):
            val = corr.iloc[i, j]
            axes[0].text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8.5,
                         color="white" if abs(val) > .65 else "#20242A")
    fig.colorbar(im, ax=axes[0], shrink=.65, ticks=[-1, 0, 1], label="Pearson r")
    axes[1].bar(range(1, 5), ratios * 100, color=colors[1], width=.65)
    axes[1].plot(range(1, 5), ratios.cumsum() * 100, "o-", color=colors[0], ms=3.5, label="Cumulative")
    axes[1].set(title="B  Variance explained", xlabel="Principal component", ylabel="Variance (%)",
                xticks=[1, 2, 3, 4], ylim=(0, 105))
    axes[1].title.set_ha("left")
    axes[1].title.set_x(0)
    axes[1].legend(loc="center right")
    save(fig, "rebuild_features")

    acf = pd.read_csv(diag / "autocorrelations.csv")
    if not np.isfinite(acf[["lag_ps", "acf"]].to_numpy()).all():
        raise ValueError("Non-finite ACF plotting data")
    fig, axes = plt.subplots(2, 2, figsize=(6, 4.2), layout="constrained")
    for ax, feature, label in zip(axes.flat, corr.columns, labels):
        for color, (replica, part) in zip(colors, acf[acf.descriptor == feature].groupby("replica_id")):
            ax.plot(part.lag_ps / 1000, part.acf, color=color, label=f"Replica {replica}")
        ax.axhline(0, color=".55", lw=.5)
        ax.set(title=label, xlabel="Biased trajectory lag (ns)", ylabel="Autocorrelation")
    axes[0, 0].legend(loc="upper right")
    save(fig, "rebuild_autocorrelations")

    summary = ablation.groupby("k").ari.agg(["min", "median", "max"])
    fig, axes = plt.subplots(1, 2, figsize=(6, 3.25), layout="constrained")
    for k, group in ablation.groupby("k"):
        axes[0].scatter(k + np.linspace(-.08, .08, len(group)), group.ari, s=15, color=colors[0], alpha=.65)
    axes[0].plot(summary.index, summary["median"], "D-", color=colors[0], ms=4, label="Median of 5 seeds")
    axes[0].set(title="A  Removing SASA", ylabel="ARI between feature sets")
    axes[0].legend(loc="lower right")
    for offset, space, color, label in [(-.08, "four", colors[0], "Four features"), (.08, "three", colors[1], "Without SASA")]:
        grouped = stability[stability.space == space].groupby("k").ari.agg(["min", "median", "max"])
        axes[1].errorbar(grouped.index + offset, grouped["median"],
                         yerr=[grouped["median"] - grouped["min"], grouped["max"] - grouped["median"]],
                         fmt="o", ms=3.5, color=color, capsize=3, label=label)
    axes[1].set(title="B  Changing the seed", ylabel="ARI between initializations")
    axes[1].legend(loc="lower right")
    for ax in axes:
        ax.set(xlabel="GMM components", xticks=[2, 3, 4, 5, 6], ylim=(-.04, 1.04))
        ax.title.set_ha("left")
        ax.title.set_x(0)
    save(fig, "rebuild_gmm")
    dump_json(run.path("tables", "figure_notes.json"), {
        "source_runs": source_ids, "new_fits": 0, "equilibrium_weighting": False,
        "acf": "Saved plotting sequence; no estimator recalculated; lag is biased trajectory time.",
        "gmm": "A: 5 paired seeds and median. B: medians and observed min/max of 10 pairs per feature space; not confidence intervals.",
        "figure_width_inches": 6.0, "font_size_points": 10})
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    run.data["peak_rss_bytes"] = int(usage if sys.platform == "darwin" else usage * 1024)
    run.data["peak_memory_method"] = "Process ru_maxrss high-water mark"
    run.finish("SUCCESS")
except Exception as error:
    run.finish("FAILED", str(error))
    raise
print(run.file)
