"""Replot saved, hash-verified results for the rebuilt report; no model fitting."""
import json
from pathlib import Path
import resource
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from robustcluster_abeta.manifest import Run, dump_json, sha256

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import report_style as rs  # noqa: E402
source_ids = {"diagnostics": "20260921T011959-583b4421", "gmm": "20261007T104141-f0143175"}
config = {"project_root": str(ROOT), "inputs": {}, "source_runs": source_ids,
          "figure_width_inches": round(rs.FULL_WIDTH_IN, 4), "plot_font": "Libertinus Sans (scripts/report_style.py)",
          "layout_revision": "v0.4.0-report-style", "scientific_mode": "saved_results_presentation", "model_fitting": False}
run = Run(config, "editorial-figures")
run.data["script_sha256"] = sha256(__file__)
run.data["source_manifests"] = {}
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
    rs.apply_style()
    run.data["style"] = rs.style_info()
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
    colors = rs.REPLICA_COLORS
    labels = [r"$n_\alpha$", r"$n_\beta$", r"$R_g$", "SASA"]
    units = {"nAlpha": r"$n_\alpha$", "nBeta": r"$n_\beta$", "Rg": r"$R_g$ (nm)", "SASA": r"SASA (nm$^2$)"}

    def save(figure, stem):
        rs.save_figure(figure, run.path("figures", f"{stem}.pdf"), formats=("pdf", "svg"),
                       creator="scripts/build_editorial_figures.py")

    fig, axes = plt.subplots(1, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 66), layout="constrained",
                             gridspec_kw={"width_ratios": [1.12, 1]})
    fig.get_layout_engine().set(wspace=0.08)
    im = axes[0].imshow(corr.to_numpy(), vmin=-1, vmax=1, cmap=rs.CMAP_DIVERGING)
    axes[0].set_xticks(range(4), labels)
    axes[0].set_yticks(range(4), labels)
    axes[0].tick_params(length=0)
    for side in ("left", "bottom"):
        axes[0].spines[side].set_visible(False)
    rs.panel_label(axes[0], "A", "Feature correlations")
    for i in range(4):
        for j in range(4):
            val = corr.iloc[i, j]
            axes[0].text(j, i, f"{val:.2f}".replace("-", "\u2212"), ha="center", va="center",
                         fontsize=rs.FONT_SIZES["annotation"], color="white" if abs(val) > .55 else rs.INK)
    cbar = fig.colorbar(im, ax=axes[0], shrink=.82, aspect=18, ticks=[-1, -.5, 0, .5, 1], pad=0.03)
    cbar.set_label("Pearson $r$")
    cbar.outline.set_linewidth(0.4)
    axes[1].bar(range(1, 5), ratios * 100, color=rs.TEAL, width=.62, label="Per component")
    axes[1].plot(range(1, 5), ratios.cumsum() * 100, "o-", color=rs.NAVY, ms=3.5, label="Cumulative")
    axes[1].set(xlabel="Principal component", ylabel="Variance explained (%)", xticks=[1, 2, 3, 4], ylim=(0, 105))
    rs.panel_label(axes[1], "B", "Variance explained")
    axes[1].legend(loc="center right")
    save(fig, "rebuild_features")

    acf = pd.read_csv(diag / "autocorrelations.csv")
    if not np.isfinite(acf[["lag_ps", "acf"]].to_numpy()).all():
        raise ValueError("Non-finite ACF plotting data")
    fig, axes = plt.subplots(2, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM * .95, 98), layout="constrained",
                             sharex=True, sharey=True)
    for index, (ax, feature, label) in enumerate(zip(axes.flat, corr.columns, labels)):
        for color, (replica, part) in zip(colors, acf[acf.descriptor == feature].groupby("replica_id")):
            ax.plot(part.lag_ps / 1000, part.acf, color=color, label=f"Replica {replica}")
        ax.axhline(0, color=rs.CODE_COMMENT, lw=.5, zorder=0)
        rs.panel_label(ax, "ABCD"[index], label)
    for ax in axes[1]:
        ax.set_xlabel("Biased trajectory lag (ns)")
    for ax in axes[:, 0]:
        ax.set_ylabel("Autocorrelation")
    axes[0, 1].legend(loc="upper right")
    save(fig, "rebuild_autocorrelations")

    summary = ablation.groupby("k").ari.agg(["min", "median", "max"])
    fig, axes = plt.subplots(1, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 68), layout="constrained", sharey=True)
    for k, group in ablation.groupby("k"):
        axes[0].scatter(k + np.linspace(-.08, .08, len(group)), group.ari, s=11, color=rs.NAVY, alpha=.55,
                        linewidths=0, label="Paired seed" if k == ablation.k.min() else None)
    axes[0].plot(summary.index, summary["median"], "D-", color=rs.NAVY, ms=3.8, label="Median of 5 seeds")
    axes[0].set_ylabel("Adjusted Rand index")
    rs.panel_label(axes[0], "A", "Removing SASA (four vs three features)")
    axes[0].legend(loc="lower right")
    for offset, space, color, label in [(-.08, "four", rs.NAVY, "Four features"), (.08, "three", rs.TEAL, "Without SASA")]:
        grouped = stability[stability.space == space].groupby("k").ari.agg(["min", "median", "max"])
        axes[1].errorbar(grouped.index + offset, grouped["median"],
                         yerr=[grouped["median"] - grouped["min"], grouped["max"] - grouped["median"]],
                         fmt="o", ms=3.5, color=color, elinewidth=.9, label=label)
    rs.panel_label(axes[1], "B", "Changing the seed (pairwise)")
    axes[1].legend(loc="lower right")
    for ax in axes:
        ax.set(xlabel="GMM components", xticks=[2, 3, 4, 5, 6], ylim=(-.04, 1.04))
    save(fig, "rebuild_gmm")

    hist = pd.read_csv(diag / "raw_histograms.csv")
    if not np.isfinite(hist[["left", "right", "density"]].to_numpy()).all():
        raise ValueError("Non-finite histogram plotting data")
    fig, axes = plt.subplots(2, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 100), layout="constrained")
    for index, (ax, feature) in enumerate(zip(axes.flat, corr.columns)):
        for color, (replica, part) in zip(colors, hist[hist.descriptor == feature].groupby("replica_id")):
            ax.stairs(part.density, np.r_[part.left, part.right.iloc[-1]], color=color, lw=1.0,
                      label=f"Replica {replica}")
        ax.set(xlabel=units[feature], ylabel="Biased-sample density")
        ax.set_ylim(bottom=0)
        rs.panel_label(ax, "ABCD"[index])
    axes[0, 0].legend(loc="upper right")
    save(fig, "raw_descriptor_distributions")
    dump_json(run.path("tables", "figure_notes.json"), {
        "source_runs": source_ids, "new_fits": 0, "equilibrium_weighting": False,
        "acf": "Saved plotting sequence; no estimator recalculated; lag is biased trajectory time.",
        "gmm": "A: 5 paired seeds and median. B: medians and observed min/max of 10 pairs per feature space; not confidence intervals.",
        "raw_descriptor_distributions": "Saved per-replica histogram table (raw_histograms.csv) of the diagnostics run; replotted only.",
        "figure_width_mm": rs.FULL_WIDTH_MM, "font_sizes_points": rs.FONT_SIZES})
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    run.data["peak_rss_bytes"] = int(usage if sys.platform == "darwin" else usage * 1024)
    run.data["peak_memory_method"] = "Process ru_maxrss high-water mark"
    run.finish("SUCCESS")
except Exception as error:
    run.finish("FAILED", str(error))
    raise
print(run.file)
