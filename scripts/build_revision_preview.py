"""Build a three-page design sample from verified empirical outputs and original vector art."""

import argparse
import ast
import os
from pathlib import Path
import shutil
import subprocess
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pypdf import PdfReader

from robustcluster_abeta.manifest import Run, sha256, dump_json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--figures-manifest", required=True)
parser.add_argument("--tex-bin", required=True)
args = parser.parse_args()
source = Path(args.figures_manifest).resolve()
data = json.loads(source.read_text())
root = source.parents[2]
if data["status"] != "SUCCESS" or data["command"] != "gmm-figures":
    raise RuntimeError("Verified GMM figures required")
for item in data["outputs"]:
    if sha256(root / item["filename"]) != item["sha256"]:
        raise RuntimeError("Figure evidence changed")
analysis_path = root / data["source_manifest"]
if sha256(analysis_path) != data["source_manifest_sha256"]:
    raise RuntimeError("Analysis manifest changed")
analysis = json.loads(analysis_path.read_text())
run = Run(data["config"], "revision-preview")
run.data["source_manifest"] = str(source.relative_to(root))
run.data["source_manifest_sha256"] = sha256(source)
run.data["script_sha256"] = sha256(__file__)
run.register_inputs()
folder = root / "report/preview"
folder.mkdir(exist_ok=True)
try:
    # Abstract, deterministic curves. No atomic coordinates, energy surface or fitted clusters.
    fig, ax = plt.subplots(figsize=(8, 3.2))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    t = np.linspace(0, 1, 400)
    for i in range(7):
        x = 0.12 + 2.0 * t + 0.15 * np.sin((2 + i % 3) * np.pi * t + i * 0.7)
        y = 1.1 + 0.75 * np.sin((2.3 + i * 0.14) * np.pi * t + i * 0.8) + 0.12 * i
        ax.plot(x, y, color=["#173A5E", "#2E6F73", "#A95542"][i % 3], lw=1.5, alpha=0.75)
    for j in range(4):
        x = 3.15 + j * 0.39
        ax.plot([x, x], [0.4, 2.5], color="#D3DBE2", lw=1)
    for i in range(7):
        vals = (
            0.65
            + np.array(
                [np.sin(i * 0.8), np.cos(i * 0.65), np.sin(i * 0.6 + 0.5), np.cos(i * 0.4 + 0.3)]
            )
            * 0.5
            + i * 0.1
        )
        ax.plot(
            3.15 + np.arange(4) * 0.39,
            vals + 0.5,
            color=["#173A5E", "#2E6F73"][i % 2],
            lw=0.9,
            alpha=0.6,
        )
    for i, width in enumerate([1.05, 0.78, 0.92]):
        y = 0.8 + i * 0.5
        ax.plot([5.55, 6.75], [y, y], color="#D3DBE2", lw=1)
        ax.plot([5.55, 5.55 + width], [y, y], color="#2E6F73", lw=3)
        ax.scatter([5.55 + width], [y], s=14, color="#173A5E")
    for a, b in [(2.3, 2.85), (4.65, 5.2)]:
        ax.annotate(
            "", (b, 1.5), (a, 1.5), arrowprops=dict(arrowstyle="->", color="#173A5E", lw=0.8)
        )
    for x, label in [(1.2, "ENSEMBLE"), (3.73, "DESCRIPTORS"), (6.15, "SENSITIVITY")]:
        ax.text(x, 0.08, label, ha="center", fontsize=9, color="#173A5E", fontfamily="DejaVu Sans")
    ax.set(xlim=(-0.1, 7), ylim=(-0.1, 3))
    ax.axis("off")
    for ext in ["pdf", "svg"]:
        fig.savefig(folder / f"cover_concept.{ext}", bbox_inches="tight")
    plt.close(fig)
    shutil.copy2(
        root / "results/figures" / data["run_id"] / "gmm_sensitivity.pdf",
        folder / "gmm_sensitivity.pdf",
    )
    code = root / "src/robustcluster_abeta/gmm_ablation.py"
    lines = code.read_text().splitlines()
    fn = next(
        n
        for n in ast.parse(code.read_text()).body
        if isinstance(n, ast.FunctionDef) and n.name == "fit_scaler"
    )
    (folder / "fit_scaler.py").write_text("\n".join(lines[fn.lineno - 1 : fn.end_lineno]) + "\n")
    rows = []
    for k, stats in analysis["summary"]["ari_by_k"].items():
        rows.append(f"{k} & {stats['median']:.3f} & {stats['min']:.3f}--{stats['max']:.3f} \\\\")
    (folder / "ablation_rows.tex").write_text(
        r"\begin{tabular}{@{}crr@{}}\toprule Components & Median ARI, four vs three features & Observed range\\\midrule"
        + "\n"
        + "\n".join(rows)
        + "\n"
        + r"\bottomrule\end{tabular}"
        + "\n"
    )
    (folder / "provenance.tex").write_text(
        "\\newcommand{\\AnalysisRun}{" + analysis["run_id"] + "}\n"
    )
    tex = folder / "revision-preview.tex"
    if not tex.exists():
        raise RuntimeError("Preview LaTeX source missing")
    env = dict(os.environ, PATH=str(Path(args.tex_bin).resolve()) + os.pathsep + os.environ["PATH"])
    run.data["latex_source_sha256"] = sha256(tex)
    run.data["asset_sources"] = {str(code.relative_to(root)): sha256(code)}
    run.data["artwork"] = {
        "type": "original conceptual vector",
        "algorithm": "deterministic curves in build_revision_preview.py",
        "empirical": False,
    }
    with run.path("logs", "lualatex.log").open("w") as log:
        for _ in range(2):
            subprocess.run(
                ["lualatex", "-halt-on-error", "-interaction=nonstopmode", "revision-preview.tex"],
                cwd=folder,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=True,
                timeout=90,
            )
    text = (folder / "revision-preview.log").read_text()
    bad = [
        line
        for line in text.splitlines()
        if any(s in line for s in ["Overfull", "Missing character", "undefined"])
    ]
    if bad:
        raise RuntimeError("Preview needs repair: " + repr(bad))
    pdf = folder / "revision-preview.pdf"
    pages = PdfReader(pdf).pages
    if len(pages) != 3:
        raise RuntimeError(f"Expected 3 design-sample pages, got {len(pages)}")
    shutil.copy2(pdf, run.path("figures", "revision-preview.pdf"))
    for item in ["cover_concept.pdf", "cover_concept.svg"]:
        shutil.copy2(folder / item, run.path("figures", item))
    run.data["preview_assets"] = {
        str(p.relative_to(root)): sha256(p)
        for p in folder.iterdir()
        if p.suffix in {".tex", ".pdf", ".svg", ".py"}
    }
    run.data["pages"] = len(pages)
    run.data["tools"] = {
        "lualatex": subprocess.check_output(
            ["lualatex", "--version"], env=env, text=True
        ).splitlines()[0]
    }
    dump_json(
        folder / "provenance.json",
        {
            "analysis_manifest": str(analysis_path.relative_to(root)),
            "figures_manifest": str(source.relative_to(root)),
            "preview_manifest": str(run.file.relative_to(root)),
        },
    )
    run.finish("SUCCESS")
except Exception as exc:
    run.finish("FAILED", str(exc))
    raise
print(pdf)
print(run.file)
