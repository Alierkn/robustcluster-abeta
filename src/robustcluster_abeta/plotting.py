"""Publication figures regenerated exclusively from saved numerical tables."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram

COLORS = ["#173A5E", "#2E6F73", "#A95542"]
LABELS = {"nAlpha": r"$n_\alpha$", "nBeta": r"$n_\beta$", "Rg": r"$R_g$ (nm)",
          "SASA": r"SASA (nm$^2$)", "ASASA": r"A-SASA (nm$^2$)", "PSASA": r"P-SASA (nm$^2$)",
          "HBONDSPP": "Intrapeptide H-bonds", "HBONDSPS": "Peptide–solvent H-bonds"}


def style():
    plt.style.use(Path(__file__).with_name("publication.mplstyle"))


def save(run, figure, name):
    for extension in ["pdf", "svg"]:
        figure.savefig(run.path("figures", f"{name}.{extension}"))
    plt.close(figure)


def workflow(run):
    style()
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.set(xlim=(0, 10), ylim=(0, 4))
    ax.axis("off")
    boxes = [(1.5, 3.25, "Validate descriptors\nSeparate replicas"),
             (5, 3.25, "Scale four features\nRandom disjoint subsets"),
             (8.5, 3.25, "Iterative DPC\nAcceptable clusters"),
             (8.5, 1.85, "Wasserstein consensus\nGlobal centroids"),
             (5, 1.85, "Assign every frame\nSTEP 3"),
             (1.5, 1.85, "Complete FES + weights\nEqual replica mixture"),
             (1.5, .45, "Weighted characterization\nReplica-aware uncertainty"),
             (5, .45, "Independent extensions\nSeeds · features · scaling"),
             (8.5, .45, "Manifest-backed\nfigures and report")]
    labels = []
    for x, y, label in boxes:
        labels.append(ax.text(
            x, y, label, ha="center", va="center", color=COLORS[0], fontsize=8,
            bbox=dict(boxstyle="round,pad=.5,rounding_size=.1", fc="#F3F5F7",
                      ec=COLORS[0], lw=.6),
        ))
    # Resolve the rendered text boxes before clipping connectors to their edges.
    fig.canvas.draw()
    for a, b, source, target in zip(boxes[:-1], boxes[1:], labels[:-1], labels[1:]):
        ax.annotate("", xy=(b[0], b[1]), xytext=(a[0], a[1]),
                    arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=.8,
                                    patchA=source.get_bbox_patch(),
                                    patchB=target.get_bbox_patch(),
                                    shrinkA=4, shrinkB=4))
    save(run, fig, "fig01_workflow")


def plot_diagnostics(run):
    style()
    workflow(run)
    corr = pd.read_csv(run.path("tables", "feature_correlation.csv"), index_col=0)
    pca = json.loads(run.path("tables", "pca.json").read_text())
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), layout="constrained")
    image = axes[0].imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    axes[0].set_xticks(range(4), [LABELS[c] for c in corr.columns], rotation=30)
    axes[0].set_yticks(range(4), [LABELS[c] for c in corr.columns])
    for i in range(4):
        for j in range(4):
            value = corr.iloc[i, j]
            axes[0].text(j, i, f"{value:.2f}", ha="center", va="center", color="white" if abs(value)>.65 else "black", fontsize=8)
    fig.colorbar(image, ax=axes[0], shrink=.8, label="Pearson correlation")
    ratios = np.array(pca["explained_variance_ratio"])
    axes[1].bar(np.arange(1, 5), ratios*100, color=COLORS[1])
    axes[1].plot(np.arange(1, 5), ratios.cumsum()*100, "o-", color=COLORS[0], label="Cumulative")
    axes[1].set(xlabel="Standardized PCA component", ylabel="Explained variance (%)", xticks=[1, 2, 3, 4], ylim=(0, 105))
    axes[1].legend()
    save(run, fig, "fig03_feature_diagnostics")
    acf = pd.read_csv(run.path("tables", "autocorrelations.csv"))
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.1), layout="constrained")
    for ax, feature in zip(axes.flat, corr.columns):
        for color, (replica, part) in zip(COLORS, acf[acf.descriptor == feature].groupby("replica_id")):
            ax.plot(part.lag_ps/1000, part.acf, color=color, label=f"Replica {replica}")
        ax.axhline(0, color="0.6", lw=.5)
        ax.set(title=LABELS[feature], xlabel="Lag along biased trajectory (ns)", ylabel="Autocorrelation")
    axes[0, 0].legend()
    save(run, fig, "sampling_autocorrelations")
    hist = pd.read_csv(run.path("tables", "raw_histograms.csv"))
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.1), layout="constrained")
    for ax, feature in zip(axes.flat, corr.columns):
        for color, (replica, part) in zip(COLORS, hist[hist.descriptor == feature].groupby("replica_id")):
            ax.stairs(part.density, np.r_[part.left, part.right.iloc[-1]], color=color, label=f"Replica {replica}")
        ax.set(xlabel=LABELS[feature], ylabel="Biased-sample density")
    axes[0, 0].legend()
    save(run, fig, "raw_descriptor_distributions")


def plot_reproduction(run):
    style()
    workflow(run)
    fes = np.load(run.path("tables", "fes_grid.npz"))
    fig, ax = plt.subplots(figsize=(5, 3.7), layout="constrained")
    mesh = ax.pcolormesh(1.1*fes["alpha"], 2.5*fes["beta"], fes["energy"].T, shading="auto", cmap="viridis")
    fig.colorbar(mesh, ax=ax, label="Supplied free energy (kJ/mol)")
    ax.set(xlabel=LABELS["nAlpha"], ylabel=LABELS["nBeta"])
    save(run, fig, "fig02_fes")
    algorithm = json.loads(run.path("tables", "baseline_algorithm.json").read_text())
    first = algorithm["decisions"][0]
    fig, ax = plt.subplots(figsize=(5, 3.5), layout="constrained")
    ax.scatter(first["rho"], first["delta"], s=4, color=COLORS[0], rasterized=True)
    ax.set(xlabel=r"Cutoff density $\rho$", ylabel=r"Density separation $\delta$", title="First subset, first DPC iteration")
    save(run, fig, "fig04_density_decision")
    saved = np.load(run.path("tables", "baseline_clustering.npz"))
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), layout="constrained")
    mesh = axes[0].imshow(saved["distance"], cmap="viridis")
    fig.colorbar(mesh, ax=axes[0], label="Norm of marginal Wasserstein distances")
    axes[0].set(xlabel="Accepted local cluster", ylabel="Accepted local cluster")
    dendrogram(saved["linkage"], ax=axes[1], no_labels=True, color_threshold=0, above_threshold_color=COLORS[0])
    axes[1].axhline(algorithm["elbow"]["threshold"], color=COLORS[2], ls="--", label="Elbow cut")
    axes[1].set(xlabel="Accepted local clusters", ylabel="Average-linkage distance")
    axes[1].legend()
    save(run, fig, "fig05_consensus")
    descriptors = pd.read_csv(run.path("tables", "baseline_weighted_descriptors.csv"))
    for filename, features in [("fig06_structural_summary", list(LABELS)[:4]), ("fig07_additional_descriptors", list(LABELS)[4:])]:
        fig, axes = plt.subplots(2, 2, figsize=(7, 4.2), layout="constrained")
        for ax, feature in zip(axes.flat, features):
            part = descriptors[descriptors.descriptor == feature]
            ax.errorbar(part.cluster, part.weighted_mean, yerr=part.weighted_distribution_sd, fmt="o", ms=3, color=COLORS[1])
            ax.set(xlabel="Global cluster ID", ylabel=LABELS[feature])
        save(run, fig, filename)
    populations = pd.read_csv(run.path("tables", "baseline_populations.csv"))
    fig, ax = plt.subplots(figsize=(6, 3.1), layout="constrained")
    ax.bar(populations.cluster, populations["mean"]*100, color=COLORS[1], alpha=.75)
    ax.errorbar(populations.cluster, populations["mean"]*100, yerr=populations.replica_sem*100,
                fmt="none", color=COLORS[0], capsize=3, label="Replica SEM")
    ax.vlines(populations.cluster, populations.bootstrap_low*100, populations.bootstrap_high*100, color=COLORS[2], label="Block-bootstrap 95% interval")
    ax.set(xlabel="Global cluster ID", ylabel="Reweighted relevance (%)")
    ax.legend()
    save(run, fig, "fig08_cluster_relevance")


def plot_stability(run):
    style()
    ari = pd.read_csv(run.path("tables", "ari_matrix.csv"), index_col=0)
    summary = pd.read_csv(run.path("tables", "cluster_stability.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
    image = axes[0].imshow(ari, vmin=-1, vmax=1, cmap="RdBu_r")
    fig.colorbar(image, ax=axes[0], label="Adjusted Rand index")
    axes[0].set(xlabel="Run index", ylabel="Run index")
    for cluster, part in summary.dropna(subset=["reference_cluster"]).groupby("reference_cluster"):
        x = np.full(len(part), cluster)
        axes[1].scatter(x, part.population*100, s=12, alpha=.65, color=COLORS[1])
        axes[1].plot([cluster-.15, cluster+.15], [part.population.mean()*100]*2, color=COLORS[0])
    axes[1].set(xlabel="Matched reference family", ylabel="Reweighted population (%)")
    save(run, fig, "fig09_stability")


def plot_reweighting(run):
    style()
    hist = pd.read_csv(run.path("tables", "reweighting_histograms.csv"))
    fig, axes = plt.subplots(2, 2, figsize=(7, 4), layout="constrained")
    for ax, descriptor in zip(axes.flat, list(LABELS)[:4]):
        for color, (method, part) in zip(COLORS, hist[hist.descriptor == descriptor].groupby("method")):
            ax.stairs(part.probability/(part.right-part.left), np.r_[part.left, part.right.iloc[-1]], color=color, label=method)
        ax.set(xlabel=LABELS[descriptor], ylabel="Reweighted density")
    axes[0, 0].legend()
    save(run, fig, "reweighting_sensitivity")
