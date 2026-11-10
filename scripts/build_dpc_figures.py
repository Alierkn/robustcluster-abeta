"""Figures and LaTeX rows for the unweighted DPC runs on the real Aβ40 descriptors.

Reads only SUCCESS manifests of the `robustcluster cluster` command and their saved tables;
every output hash is checked against its manifest before use. Family sizes are raw frame
fractions of the biased sample, never equilibrium populations.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
sys.path.insert(0, str(ROOT/"src"))
import report_style as rs  # noqa: E402
from robustcluster_abeta.io import read_descriptors  # noqa: E402


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_run(run_id):
    manifest_path = ROOT/"results/manifests"/f"{run_id}.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["status"] != "SUCCESS" or manifest["command"] != "cluster":
        raise SystemExit(f"{run_id} is not a successful cluster run")
    for output in manifest["outputs"]:
        if sha256(ROOT/output["filename"]) != output["sha256"]:
            raise SystemExit(f"Hash mismatch for {output['filename']}")
    tables = ROOT/"results/tables"/run_id
    return manifest, tables, manifest_path


def family_order(families):
    """Display order: largest raw frame fraction first."""
    return families.sort_values("raw_fraction", ascending=False).family.tolist()


def landscape_figure(full_tables, out):
    families = pd.read_csv(full_tables/"families_unweighted.csv")
    families = families[families.variant == "baseline"].set_index("family")
    labels = np.load(full_tables/"baseline_labels.npz")["labels"]
    table = read_descriptors(ROOT/"data/raw/input_clustering_ab40.dat", 3, [1000000, 3000000])
    if len(table) != len(labels):
        raise SystemExit("Label count differs from the descriptor table")
    order = family_order(families.reset_index())
    fig, axes = rs.plt.subplots(1, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 74), layout="constrained")
    panels = [("Rg", "SASA", r"$R_g$ (nm)", r"SASA (nm$^2$)", "Compactness and exposure"),
              ("nAlpha", "nBeta", r"$n_\alpha$", r"$n_\beta$", "Secondary structure")]
    background = rs.cmap_segment(rs.CMAP_SEQUENTIAL, 0.02, 0.35)
    for ax, (x, y, xl, yl, title), letter in zip(axes, panels, "AB"):
        ax.hexbin(table[x], table[y], gridsize=55, bins="log", cmap=background, mincnt=1,
                  linewidths=0, rasterized=True)
        for number, family in enumerate(order, 1):
            row = families.loc[family]
            size = 1400*row.raw_fraction
            ax.scatter(row[f"mean_{x}"], row[f"mean_{y}"], s=size, color=rs.NAVY, alpha=.78,
                       edgecolor="white", linewidth=.8, zorder=5)
            ax.annotate(str(number), (row[f"mean_{x}"], row[f"mean_{y}"]), ha="center", va="center",
                        color="white", fontsize=6.5, fontweight="bold", zorder=6)
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        rs.panel_label(ax, letter, title)
    for fraction in (.05, .15):
        axes[1].scatter([], [], s=1400*fraction, color=rs.NAVY, alpha=.78, edgecolor="white",
                        label=f"{fraction:.0%} of frames")
    axes[1].legend(loc="upper right", frameon=False, labelspacing=1.4, borderpad=1.0)
    rs.save_figure(fig, out, creator="scripts/build_dpc_figures.py")
    return order


def _rows(tables, kind):
    ari = pd.read_csv(tables/"ari_matrix.csv", index_col=0)
    fams = pd.read_csv(tables/"families_unweighted.csv").groupby("variant").family.nunique()
    reference = ari.index[0]
    return {name: (float(ari.loc[reference, name]), int(fams[name])) for name in ari.columns[1:]}, int(fams[reference])


def sensitivity_figure(seed_tables, param_tables, out, medium_seeds=None, medium_params=None):
    fig, ax = rs.plt.subplots(figsize=rs.figsize(rs.FULL_WIDTH_MM, 66), layout="constrained")
    full_seeds, ref_fams = _rows(seed_tables, "Seed")
    full_params, _ = _rows(param_tables, "Parameter")
    med_seeds = _rows(medium_seeds, "Seed")[0] if medium_seeds else {}
    med_params = _rows(medium_params, "Parameter")[0] if medium_params else {}
    pretty = {"dc_x0.9": r"$d_c\times0.9$", "dc_x1.1": r"$d_c\times1.1$",
              "silhouette_0.25": "silhouette 0.25", "silhouette_0.35": "silhouette 0.35",
              "min_size_200": "min. size 200", "min_size_400": "min. size 400"}
    rows = [("Seed", f"seed {i}", name, full_seeds[name], med_seeds.get(name)) for i, name in enumerate(full_seeds, 1)]
    rows += [("Parameter", pretty.get(n, n), n, full_params[n], med_params.get(n)) for n in full_params]
    for y, (kind, label, _, full, medium) in enumerate(rows):
        colour = rs.NAVY if kind == "Seed" else rs.TEAL
        ax.hlines(y, 0, full[0], color=rs.GRID, lw=1)
        if medium:
            ax.scatter(medium[0], y, s=26, facecolor="white", edgecolor=colour, lw=1, zorder=3)
        ax.scatter(full[0], y, s=34, color=colour, zorder=4)
        ax.text(1.02, y, f"{full[0]:.2f}  ({full[1]} families)", va="center",
                fontsize=rs.FONT_SIZES["annotation"], color=rs.MUTED)
    ax.set_yticks(range(len(rows)), [r[1] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.32)
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_xlabel(f"ARI with the reference partition (seed 42, published parameters, {ref_fams} families)")
    split = sum(r[0] == "Seed" for r in rows) - .5
    ax.axhline(split, color=rs.CODE_COMMENT, lw=.6, ls=":")
    handles = [rs.plt.Line2D([], [], marker="o", ls="", color=rs.INK, markersize=5, label="full profile"),
               rs.plt.Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=rs.INK,
                             markersize=5, label="medium profile")]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncols=2, bbox_to_anchor=(0, 1.0))
    rs.save_figure(fig, out, creator="scripts/build_dpc_figures.py")
    return [(r[0], r[1], r[3][0], r[3][1], None if r[4] is None else r[4][0]) for r in rows]


def family_rows(full_tables, order, out):
    families = pd.read_csv(full_tables/"families_unweighted.csv")
    families = families[families.variant == "baseline"].set_index("family")
    lines = [r"\begin{tabular}{@{}lrrrrrrr@{}}", r"\toprule",
             r"Family & Frames & \multicolumn{3}{c}{Fraction by replica} & $\bar n_\alpha$ & $\bar n_\beta$ & $\bar R_g$ (nm) / SASA (nm$^2$)\\",
             r"\cmidrule(lr){3-5}", r" & (all) & 1 & 2 & 3 & & & \\", r"\midrule"]
    for i, family in enumerate(order, 1):
        r = families.loc[family]
        lines.append(f"{i} & {r.raw_fraction:.1%} & {r.raw_fraction_replica_1:.1%} & {r.raw_fraction_replica_2:.1%} & "
                     f"{r.raw_fraction_replica_3:.1%} & {r.mean_nAlpha:.1f} & {r.mean_nBeta:.1f} & "
                     f"{r.mean_Rg:.2f} / {r.mean_SASA:.1f}\\\\".replace("%", r"\%"))
    lines += [r"\bottomrule", r"\end{tabular}"]
    out.write_text("% Generated by scripts/build_dpc_figures.py from a SUCCESS cluster manifest. Do not edit.\n"
                   + "\n".join(lines) + "\n")


def write_values(runs, rows, wasserstein_ari, out):
    full_manifest, full_tables, _ = runs["full-run"]
    algorithm = json.loads((full_tables/"baseline_algorithm.json").read_text())
    families = pd.read_csv(full_tables/"families_unweighted.csv")
    families = families[families.variant == "baseline"]
    spread = (families[[f"raw_fraction_replica_{i}" for i in (1, 2, 3)]].max(axis=1)
              - families[[f"raw_fraction_replica_{i}" for i in (1, 2, 3)]].min(axis=1))
    seeds = [r for r in rows if r[0] == "Seed"]
    params = [r for r in rows if r[0] == "Parameter"]
    medium = runs.get("medium-seeds-run")
    medium_fams = None
    if medium:
        medium_fams = int(pd.read_csv(medium[1]/"families_unweighted.csv").groupby("variant").family.nunique().iloc[0])
    values = {
        "DPCRun": full_manifest["run_id"],
        "DPCFamilies": int(families.family.nunique()),
        "DPCLocalClusters": algorithm["accepted_local_clusters"],
        "DPCGroups": algorithm["group_count"],
        "DPCMinutes": f"{full_manifest['runtime_seconds']/60:.0f}",
        "DPCMemory": f"{full_manifest['peak_rss_bytes']/2**30:.1f}",
        "DPCLargest": f"{100*families.raw_fraction.max():.1f}",
        "DPCSmallest": f"{100*families.raw_fraction.min():.1f}",
        "DPCMaxReplicaSpread": f"{100*spread.max():.1f}",
        "DPCSeedARIMin": f"{min(r[2] for r in seeds):.2f}", "DPCSeedARIMax": f"{max(r[2] for r in seeds):.2f}",
        "DPCSeedFamMin": min(r[3] for r in seeds), "DPCSeedFamMax": max(r[3] for r in seeds),
        "DPCParamARIMin": f"{min(r[2] for r in params):.2f}", "DPCParamARIMax": f"{max(r[2] for r in params):.2f}",
        "DPCParamFamMin": min(r[3] for r in params), "DPCParamFamMax": max(r[3] for r in params),
        "DPCWassersteinARI": f"{wasserstein_ari:.2f}",
        "DPCMediumFamilies": medium_fams if medium_fams is not None else "--",
    }
    out.write_text("% Generated by scripts/build_dpc_figures.py from SUCCESS cluster manifests. Do not edit.\n"
                   + "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in values.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-run", required=True)
    parser.add_argument("--seeds-run", required=True)
    parser.add_argument("--params-run", required=True)
    parser.add_argument("--wasserstein-run", required=True)
    parser.add_argument("--medium-seeds-run")
    parser.add_argument("--medium-params-run")
    args = parser.parse_args()
    rs.apply_style()
    runs = {k: load_run(getattr(args, k.replace("-", "_"))) for k in ["full-run", "seeds-run", "params-run", "wasserstein-run"]}
    if runs["full-run"][0]["config"]["execution"]["group_size"] != 30000:
        print("warning: --full-run is not the published full profile")
    figures = ROOT/"report/figures"
    order = landscape_figure(runs["full-run"][1], figures/"dpc_families.pdf")
    medium = {k: load_run(getattr(args, k.replace("-", "_"))) for k in ["medium-seeds-run", "medium-params-run"]
              if getattr(args, k.replace("-", "_"))}
    runs.update(medium)
    rows = sensitivity_figure(runs["seeds-run"][1], runs["params-run"][1], figures/"dpc_sensitivity.pdf",
                              medium.get("medium-seeds-run", (None, None))[1], medium.get("medium-params-run", (None, None))[1])
    family_rows(runs["full-run"][1], order, ROOT/"report/generated/dpc_family_rows.tex")
    wass = pd.read_csv(runs["wasserstein-run"][1]/"ari_matrix.csv", index_col=0)
    full = runs["full-run"][0]
    provenance = {
        "runs": {k: {"run_id": v[0]["run_id"], "manifest_sha256": sha256(v[2]),
                     "runtime_seconds": v[0]["runtime_seconds"], "peak_rss_bytes": v[0]["peak_rss_bytes"],
                     "summary": v[0]["summary"]} for k, v in runs.items()},
        "full_profile": full["config"]["execution"],
        "wasserstein_normalized_ari": float(wass.loc["baseline", "normalized"]),
        "sensitivity_rows": [list(map(str, r)) for r in rows],
        "outputs": {p: sha256(ROOT/p) for p in ["report/figures/dpc_families.pdf", "report/figures/dpc_sensitivity.pdf",
                                                  "report/generated/dpc_family_rows.tex"]},
        "style": rs.style_info(),
    }
    write_values(runs, rows, float(wass.loc["baseline", "normalized"]), ROOT/"report/generated/dpc_values.tex")
    provenance["outputs"]["report/generated/dpc_values.tex"] = sha256(ROOT/"report/generated/dpc_values.tex")
    (ROOT/"report/dpc_provenance.json").write_text(json.dumps(provenance, indent=2, default=str) + "\n")
    print(json.dumps({k: v for k, v in provenance.items() if k in ("wasserstein_normalized_ari", "outputs")}, indent=2))


if __name__ == "__main__":
    main()
