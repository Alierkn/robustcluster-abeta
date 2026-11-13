"""Weighted family populations under the ASSUMED FES unit, with a unit-sensitivity scenario.

Inputs are SUCCESS manifests only: the `reproduce` run made with
config/paper_reproduction_full_assumed.yaml and the unweighted `cluster` run that fixes the
family numbering. Every output hash is checked before use. All populations are conditional on
the assumption that FES_AB_40.dat is a sum_hills free energy in kJ/mol; the kcal/mol scenario
shows how much the conclusions would change if that assumption were wrong.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import report_style as rs  # noqa: E402

KCAL_TO_KJ = 4.184


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_run(run_id, command):
    manifest_path = ROOT/"results/manifests"/f"{run_id}.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["status"] != "SUCCESS" or manifest["command"] != command:
        raise SystemExit(f"{run_id} is not a successful {command} run")
    for output in manifest["outputs"]:
        if sha256(ROOT/output["filename"]) != output["sha256"]:
            raise SystemExit(f"Hash mismatch for {output['filename']}")
    return manifest, ROOT/"results/tables"/run_id, manifest_path


def populations(log_weights, labels, replicas, families):
    pooled = np.zeros(len(log_weights))
    for replica in np.unique(replicas):
        mask = replicas == replica
        pooled[mask] = np.exp(log_weights[mask]-logsumexp(log_weights[mask]))/len(np.unique(replicas))
    return pd.Series({f: pooled[labels == f].sum() for f in families})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reproduce-run", required=True)
    parser.add_argument("--cluster-run", required=True)
    args = parser.parse_args()
    rs.apply_style()
    rep_manifest, rep_tables, rep_path = load_run(args.reproduce_run, "reproduce")
    if "ASSUMED" not in str(rep_manifest["config"]["inputs"]["fes_provenance"]):
        raise SystemExit("The reproduce run must carry the explicit ASSUMED provenance statement")
    clu_manifest, clu_tables, clu_path = load_run(args.cluster_run, "cluster")

    frames = pd.read_csv(rep_tables/"baseline_frames.csv.gz")
    labels = frames.final_cluster_label.to_numpy()
    reference = np.load(clu_tables/"baseline_labels.npz")["labels"]
    if not np.array_equal(labels, reference):
        raise SystemExit("Reproduce labels differ from the unweighted cluster run")
    unweighted = pd.read_csv(clu_tables/"families_unweighted.csv")
    unweighted = unweighted[unweighted.variant == "baseline"].set_index("family")
    order = unweighted.sort_values("raw_fraction", ascending=False).index.tolist()
    number = {f: i for i, f in enumerate(order, 1)}

    pops = pd.read_csv(rep_tables/"baseline_populations.csv").set_index("cluster")
    per_rep = pd.read_csv(rep_tables/"baseline_replica_populations.csv")
    ess = pd.read_csv(rep_tables/"weight_ess.csv")
    replicas = frames.replica_id.to_numpy()
    logw = frames.raw_log_weight.to_numpy()
    kj = populations(logw, labels, replicas, order)
    if not np.allclose(kj.to_numpy(), pops.loc[order, "mean"].to_numpy(), atol=1e-9):
        raise SystemExit("Recomputed kJ/mol populations do not match the saved run")
    kcal = populations(logw*KCAL_TO_KJ, labels, replicas, order)

    # Figure: raw fraction, weighted population with bootstrap interval and replicas, kcal scenario.
    fig, ax = rs.plt.subplots(figsize=rs.figsize(rs.FULL_WIDTH_MM, 78), layout="constrained")
    for y, family in enumerate(order):
        raw = unweighted.loc[family, "raw_fraction"]
        ax.barh(y, 100*raw, height=.62, color=rs.COOLGREY, edgecolor=rs.GRID, lw=.6, zorder=1)
        reps = per_rep[per_rep.cluster == family].population.to_numpy()*100
        ax.scatter(reps, np.full(len(reps), y), marker="|", s=40, color=rs.TEAL, lw=1.1, zorder=4)
        ax.scatter(100*pops.loc[family, "mean"], y, s=30, color=rs.NAVY, zorder=5)
        ax.scatter(100*kcal[family], y+.24, s=22, marker="D", facecolor="white", edgecolor=rs.AUDIT, lw=1, zorder=6)
    ax.set_yticks(range(len(order)), [f"Family {number[f]}" for f in order])
    ax.invert_yaxis()
    ax.set_xlabel("Share of frames or of statistical weight (%)")
    handles = [rs.plt.Rectangle((0, 0), 1, 1, facecolor=rs.COOLGREY, edgecolor=rs.GRID, label="raw frame fraction"),
               rs.plt.Line2D([], [], color=rs.NAVY, marker="o", markersize=4.5, ls="",
                             label=r"weighted (kJ mol$^{-1}$)"),
               rs.plt.Line2D([], [], color=rs.TEAL, marker="|", ls="", markersize=7, label="single replicas"),
               rs.plt.Line2D([], [], color=rs.AUDIT, marker="D", markerfacecolor="white", ls="", markersize=4.5,
                             label=r"if the file were kcal mol$^{-1}$")]
    ax.legend(handles=handles, loc="lower right", frameon=False)
    rs.save_figure(fig, ROOT/"report/figures/weighted_populations.pdf", creator="scripts/build_weighted_figures.py")

    # Table rows.
    lines = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
             r"Family & Raw & Weighted & Replica range & If kcal\,mol$^{-1}$\\", r"\midrule"]
    for family in order:
        reps = per_rep[per_rep.cluster == family].population
        lines.append(f"{number[family]} & {100*unweighted.loc[family, 'raw_fraction']:.1f} & "
                     f"{100*pops.loc[family, 'mean']:.1f} & {100*reps.min():.1f}--{100*reps.max():.1f} & "
                     f"{100*kcal[family]:.1f}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (ROOT/"report/generated/weighted_rows.tex").write_text(
        "% Generated by scripts/build_weighted_figures.py; values in percent. Do not edit.\n" + "\n".join(lines) + "\n")

    # Macros.
    top_w = pops.loc[order, "mean"].idxmax()
    top3 = pops.loc[order, "mean"].sort_values(ascending=False).head(3).sum()
    shift = (pops.loc[order, "mean"]-unweighted.loc[order, "raw_fraction"]).abs().max()
    unit_shift = (kcal-pops.loc[order, "mean"]).abs().max()
    rank_kj = pops.loc[order, "mean"].rank(ascending=False)
    rank_kcal = kcal.rank(ascending=False)
    weighted = pops.loc[order, "mean"]
    raw = unweighted.loc[order, "raw_fraction"]
    extended = [f for f in order if unweighted.loc[f, "mean_Rg"] > 1.5]
    vanishing = [f for f in order if number[f] in (3, 5, 6, 8, 11)]
    per_replica_vanishing = max(per_rep[(per_rep.replica_id == r) & per_rep.cluster.isin(vanishing)].population.sum()
                                for r in per_rep.replica_id.unique())
    top = pops.loc[order, "mean"].idxmax()
    top_reps = per_rep[per_rep.cluster == top].population
    values = {
        "WExtendedRaw": f"{100*raw[extended].sum():.1f}", "WExtended": f"{100*weighted[extended].sum():.1f}",
        "WExtendedKcal": f"{100*kcal[extended].sum():.1f}",
        "WVanishRaw": f"{100*raw[vanishing].sum():.0f}", "WVanish": f"{100*weighted[vanishing].sum():.1f}",
        "WVanishMaxReplica": f"{100*per_replica_vanishing:.1f}",
        "WTopRepMin": f"{100*top_reps.min():.1f}", "WTopRepMax": f"{100*top_reps.max():.1f}",
        "WFamSevenKcal": f"{100*kcal[[f for f in order if number[f] == 7][0]]:.1f}",
        "WFamTwoKcal": f"{100*kcal[[f for f in order if number[f] == 2][0]]:.1f}",
        "WRun": rep_manifest["run_id"],
        "WTopFamily": number[top_w], "WTopShare": f"{100*pops.loc[top_w, 'mean']:.1f}",
        "WTopThree": f"{100*top3:.1f}",
        "WMaxShift": f"{100*shift:.1f}",
        "WKishMin": f"\\num{{{ess.kish_weight_ess.min():.0f}}}", "WKishMax": f"\\num{{{ess.kish_weight_ess.max():.0f}}}",
        "WUnitShift": f"{100*unit_shift:.1f}",
        "WTopKcal": number[kcal.idxmax()], "WTopKcalShare": f"{100*kcal.max():.1f}",
        "WRankAgree": "yes" if rank_kj.idxmin() == rank_kcal.idxmin() else "no",
        "WBlockMin": f"\\num{{{min(rep_manifest['summary']['block_lengths'].values())}}}",
        "WBlockMax": f"\\num{{{max(rep_manifest['summary']['block_lengths'].values())}}}",
        "WMinutes": f"{rep_manifest['runtime_seconds']/60:.0f}",
    }
    (ROOT/"report/generated/weighted_values.tex").write_text(
        "% Generated by scripts/build_weighted_figures.py. Conditional on the ASSUMED FES unit. Do not edit.\n"
        + "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in values.items()))
    provenance = {
        "assumption": rep_manifest["config"]["inputs"]["fes_provenance"],
        "reproduce_run": {"run_id": rep_manifest["run_id"], "manifest_sha256": sha256(rep_path)},
        "cluster_run": {"run_id": clu_manifest["run_id"], "manifest_sha256": sha256(clu_path)},
        "kish_ess": ess.to_dict("records"),
        "values": values,
        "outputs": {p: sha256(ROOT/p) for p in ["report/figures/weighted_populations.pdf",
                                                 "report/generated/weighted_rows.tex",
                                                 "report/generated/weighted_values.tex"]},
        "style": rs.style_info(),
    }
    (ROOT/"report/weighted_provenance.json").write_text(json.dumps(provenance, indent=2, default=str) + "\n")
    print(json.dumps(values, indent=2))


if __name__ == "__main__":
    main()
