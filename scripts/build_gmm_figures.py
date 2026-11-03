"""Build traced vector figures from a successful GMM-ablation run."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from robustcluster_abeta.manifest import Run, dump_json, sha256

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
run = Run(data["config"], "gmm-figures")
run.data["source_manifest"] = str(source.relative_to(root))
run.data["source_manifest_sha256"] = sha256(source)
run.data["script_sha256"] = sha256(__file__)
run.register_inputs()
try:
    plt.style.use(root / "src/robustcluster_abeta/publication.mplstyle")
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
    colors = ["#173A5E", "#2E6F73"]
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 3.05), layout="constrained")
    for k, group in ablation.groupby("k"):
        axs[0].scatter(
            k + np.linspace(-0.09, 0.09, len(group)), group.ari, color=colors[0], s=14, alpha=0.65
        )
    axs[0].plot(
        summary.k, summary.ari_median, color=colors[0], marker="D", ms=4, label="Median (5 seeds)"
    )
    axs[0].set(
        title="A  Agreement after removing SASA",
        xlabel="Number of GMM components",
        ylabel="Adjusted Rand index",
    )
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
            ms=3,
            capsize=3,
            linewidth=0.9,
            label=label,
        )
    axs[1].set(
        title="B  Sensitivity to initialization",
        xlabel="Number of GMM components",
        ylabel="Pairwise seed ARI",
    )
    for ax in axs:
        ax.set_ylim(-0.04, 1.04)
        ax.set_xticks(summary.k)
        ax.legend(loc="lower right", fontsize=7)
    for ext in ["pdf", "svg"]:
        fig.savefig(run.path("figures", f"gmm_sensitivity.{ext}"))
    plt.close(fig)
    seeds = data["config"]["gmm"]["master_seeds"]
    ks = data["config"]["gmm"]["components"]
    fig, axs = plt.subplots(2, len(ks), figsize=(8.3, 3.7), layout="constrained")
    for row, space in enumerate(["four", "three"]):
        for col, k in enumerate(ks):
            matrix = np.full((len(seeds), len(seeds)), np.nan)
            np.fill_diagonal(matrix, 1.0)
            for entry in stability[(stability.space == space) & (stability.k == k)].itertuples():
                i, j = seeds.index(entry.seed_a), seeds.index(entry.seed_b)
                matrix[i, j] = matrix[j, i] = entry.ari
            im = axs[row, col].imshow(matrix, vmin=0, vmax=1, cmap="cividis")
            axs[row, col].set_title(f"k = {k}", fontsize=9)
            axs[row, col].set_xticks(range(len(seeds)), seeds, fontsize=6)
            axs[row, col].set_yticks(range(len(seeds)), seeds, fontsize=6)
            if col == 0:
                axs[row, col].set_ylabel("Four features" if row == 0 else "Without SASA")
    fig.colorbar(im, ax=axs.ravel().tolist(), fraction=0.025, label="ARI")
    for ext in ["pdf", "svg"]:
        fig.savefig(run.path("figures", f"gmm_seed_matrices.{ext}"))
    plt.close(fig)
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
