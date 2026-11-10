"""Build traced vector figures from a successful GMM-ablation run."""

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from robustcluster_abeta.manifest import Run, dump_json, sha256

sys.path.insert(0, str(Path(__file__).resolve().parent))
import report_style as rs  # noqa: E402

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--manifest", required=True)
args = parser.parse_args()
source = Path(args.manifest).resolve()
data = json.loads(source.read_text())
if data["status"] != "SUCCESS" or data["command"] != "gmm-ablation":
    raise RuntimeError("Successful GMM ablation evidence required")
root = source.parents[2]
for item in data["outputs"]:
    if sha256(root / item["filename"]) != item["sha256"]:
        raise RuntimeError("Source output hash mismatch")
# Outputs go to this checkout (the source run may record another project_root).
run = Run({**data["config"], "project_root": str(root)}, "gmm-figures")
run.data["source_manifest"] = str(source.relative_to(root))
run.data["source_manifest_sha256"] = sha256(source)
run.data["script_sha256"] = sha256(__file__)
run.register_inputs()
try:
    rs.apply_style()
    run.data["style"] = rs.style_info()
    tables = root / "results/tables" / data["run_id"]
    ablation = pd.read_csv(tables / "ablation.csv")
    stability = pd.read_csv(tables / "seed_stability.csv")
    models = pd.read_csv(tables / "models.csv")
    summary = (
        ablation.groupby("k")
        .agg(
            ari_min=("ari", "min"),
            ari_median=("ari", "median"),
            ari_max=("ari", "max"),
            matched_median=("matched_fraction", "median"),
        )
        .reset_index()
    )
    summary.to_csv(run.path("tables", "ablation_summary.csv"), index=False)
    colors = [rs.NAVY, rs.TEAL]

    def save(figure, stem):
        rs.save_figure(figure, run.path("figures", f"{stem}.pdf"), formats=("pdf", "svg"),
                       creator="scripts/build_gmm_figures.py")

    fig, axs = plt.subplots(1, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 66), layout="constrained", sharey=True)
    for k, group in ablation.groupby("k"):
        axs[0].scatter(
            k + np.linspace(-0.09, 0.09, len(group)), group.ari, color=colors[0], s=11, alpha=0.55, linewidths=0
        )
    axs[0].plot(
        summary.k, summary.ari_median, color=colors[0], marker="D", ms=3.8, label="Median (5 seeds)"
    )
    axs[0].set(xlabel="Number of GMM components", ylabel="Adjusted Rand index")
    rs.panel_label(axs[0], "A", "Agreement after removing SASA")
    for offset, (space, label, color) in zip(
        [-0.08, 0.08], [("four", "Four features", colors[0]), ("three", "Without SASA", colors[1])]
    ):
        sub = stability[stability.space == space].groupby("k").ari.agg(["min", "median", "max"])
        axs[1].errorbar(
            sub.index + offset,
            sub["median"],
            yerr=[sub["median"] - sub["min"], sub["max"] - sub["median"]],
            color=color,
            marker="o",
            ms=3.5,
            linewidth=0.9,
            label=label,
        )
    axs[1].set(xlabel="Number of GMM components")
    rs.panel_label(axs[1], "B", "Sensitivity to initialization")
    for ax in axs:
        ax.set_ylim(-0.04, 1.04)
        ax.set_xticks(summary.k)
        ax.legend(loc="lower right")
    save(fig, "gmm_sensitivity")
    seeds = data["config"]["gmm"]["master_seeds"]
    ks = data["config"]["gmm"]["components"]
    matrix_cmap = rs.cmap_segment(high=0.86)  # ARI = 1 maps to navy, not near-black
    fig, axs = plt.subplots(2, len(ks), figsize=rs.figsize(rs.FULL_WIDTH_MM, 70), layout="constrained",
                            sharex=True, sharey=True)
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, wspace=0.02, hspace=0.03)
    for row, space in enumerate(["four", "three"]):
        for col, k in enumerate(ks):
            ax = axs[row, col]
            matrix = np.full((len(seeds), len(seeds)), np.nan)
            np.fill_diagonal(matrix, 1.0)
            for entry in stability[(stability.space == space) & (stability.k == k)].itertuples():
                i, j = seeds.index(entry.seed_a), seeds.index(entry.seed_b)
                matrix[i, j] = matrix[j, i] = entry.ari
            im = ax.imshow(matrix, vmin=0, vmax=1, cmap=matrix_cmap)
            ax.set_xticks(range(len(seeds)), seeds)
            ax.set_yticks(range(len(seeds)), seeds)
            ax.tick_params(length=0, pad=1.5)
            for side in ("left", "bottom"):
                ax.spines[side].set_visible(False)
            if row == 0:
                ax.set_title(f"$k$ = {k}", loc="center")
            if col == 0:
                ax.set_ylabel(("Four features" if row == 0 else "Without SASA") + "\nseed")
            if row == 1:
                ax.set_xlabel("seed")
    cbar = fig.colorbar(im, ax=axs.ravel().tolist(), fraction=0.025, pad=0.01, aspect=22, ticks=[0, 0.5, 1])
    cbar.set_label("Pairwise ARI")
    cbar.outline.set_linewidth(0.4)
    save(fig, "gmm_seed_matrices")
    # BIC is tabulated within each feature space only, not used for cross-dimensional selection.
    models.groupby(["space", "k"]).fit_bic.agg(["min", "median", "max"]).to_csv(
        run.path("tables", "bic_within_space.csv")
    )
    dump_json(
        run.path("tables", "figure_notes.json"),
        {
            "sensitivity": "Panel A: five seed-paired comparisons, dots and median. Panel B: ten pairwise comparisons per feature space, median and observed min/max; not confidence intervals.",
            "matrices": "All k values shown; diagonal is identity; no selection of a best biological cluster count.",
            "source_run": data["run_id"],
            "equilibrium_interpretation": False,
        },
    )
    run.finish("SUCCESS")
except Exception as exc:
    run.finish("FAILED", str(exc))
    raise
print(run.file)
