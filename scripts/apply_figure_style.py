"""Install report-style figures into report/figures and record figure_style_provenance.json.

The figures are re-drawn (never re-computed) by the existing builders, all of which now import
scripts/report_style.py:

* scripts/build_premium_figures.py  -> fes_map, descriptor_landscape, rg_timeseries
  (raw inputs, SHA256-checked; written to a staging directory with its own provenance JSON)
* scripts/build_editorial_figures.py -> rebuild_features, rebuild_autocorrelations, rebuild_gmm,
  raw_descriptor_distributions (saved diagnostics/GMM tables; run manifest in results/manifests)
* scripts/build_gmm_figures.py       -> gmm_seed_matrices (saved GMM-ablation tables)

Older provenance files (data_provenance.json, revision_provenance.json, rebuild_provenance.json,
figures/premium_figures_provenance.json) are left byte-identical. This script writes a NEW file,
report/figure_style_provenance.json, listing for every replaced asset the hash it supersedes and
the new hash; scripts/build_report.py accepts a superseded hash only through that record.

Usage:
    python scripts/apply_figure_style.py --premium-dir DIR --editorial-manifest M1 --gmm-manifest M2
"""

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from robustcluster_abeta.manifest import dump_json, sha256  # noqa: E402

import report_style as rs  # noqa: E402

FIGURES = ROOT / "report/figures"
OLD_PROVENANCE = ["report/data_provenance.json", "report/revision_provenance.json",
                  "report/rebuild_provenance.json", "report/figures/premium_figures_provenance.json"]
PREMIUM = {"fes_map.pdf": "data/raw/FES_AB_40.dat + data/raw/input_clustering_ab40.dat",
           "descriptor_landscape.pdf": "data/raw/input_clustering_ab40.dat",
           "rg_timeseries.pdf": "data/raw/input_clustering_ab40.dat"}
EDITORIAL = {"rebuild_features": "results/tables/20260921T011959-583b4421/{feature_correlation.csv,pca.json}",
             "rebuild_autocorrelations": "results/tables/20260921T011959-583b4421/autocorrelations.csv",
             "rebuild_gmm": "results/tables/20261007T104141-f0143175/{ablation.csv,seed_stability.csv}",
             "raw_descriptor_distributions": "results/tables/20260921T011959-583b4421/raw_histograms.csv"}
GMM = {"gmm_seed_matrices": "results/tables/20261007T104141-f0143175/seed_stability.csv"}


def previous_records():
    """Hashes the old provenance files hold for each report asset (first occurrence wins)."""
    known = {}
    for rel in OLD_PROVENANCE:
        path = ROOT / rel
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        outputs = data.get("outputs", [])
        if isinstance(outputs, dict):  # premium provenance: {name: {sha256, bytes}}
            outputs = [{"filename": f"report/figures/{name}", "sha256": r["sha256"]} for name, r in outputs.items()]
        for record in outputs + data.get("assets", []):
            known.setdefault(record["filename"], {})[rel] = record["sha256"]
    return known


def verified_manifest(path, command):
    path = Path(path).resolve()
    data = json.loads(path.read_text())
    if data["status"] != "SUCCESS" or data["command"] != command:
        raise SystemExit(f"{path}: not a successful {command} run")
    for item in data["outputs"]:
        if sha256(ROOT / item["filename"]) != item["sha256"]:
            raise SystemExit(f"{item['filename']}: hash differs from {path.name}")
    return path, data


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--premium-dir", required=True, type=Path)
    parser.add_argument("--editorial-manifest", required=True)
    parser.add_argument("--gmm-manifest", required=True)
    args = parser.parse_args()
    known = previous_records()
    premium_dir = args.premium_dir.resolve()
    premium_prov = json.loads((premium_dir / "premium_figures_provenance.json").read_text())
    jobs = []
    for name, source in PREMIUM.items():
        if sha256(premium_dir / name) != premium_prov["outputs"][name]["sha256"]:
            raise SystemExit(f"{name}: staged file differs from its premium provenance")
        jobs.append((premium_dir / name, name, "scripts/build_premium_figures.py",
                     {"provenance": str((premium_dir / "premium_figures_provenance.json").relative_to(ROOT)),
                      "provenance_sha256": sha256(premium_dir / "premium_figures_provenance.json")}, source))
    for manifest, command, stems, script in [(args.editorial_manifest, "editorial-figures", EDITORIAL,
                                              "scripts/build_editorial_figures.py"),
                                             (args.gmm_manifest, "gmm-figures", GMM,
                                              "scripts/build_gmm_figures.py")]:
        path, data = verified_manifest(manifest, command)
        run = {"manifest": str(path.relative_to(ROOT)), "manifest_sha256": sha256(path)}
        for stem, source in stems.items():
            for ext in ("pdf", "svg"):
                staged = ROOT / "results/figures" / data["run_id"] / f"{stem}.{ext}"
                if ext == "svg" and not (FIGURES / staged.name).exists():
                    continue  # only replace SVG twins that the report folder already carries
                jobs.append((staged, staged.name, script, run, source))

    records = []
    for staged, name, script, run, source in jobs:
        target = FIGURES / name
        rel = str(target.relative_to(ROOT))
        before = sha256(target) if target.exists() else None
        shutil.copyfile(staged, target)
        after = sha256(target)
        records.append({"filename": rel, "sha256": after, "supersedes_sha256": before,
                        "changed": before != after, "superseded_in": known.get(rel, {}),
                        "built_by": script, "build_record": run, "data_source": source,
                        "included_in_report": name.endswith(".pdf")})
    provenance = {
        "schema_version": 1,
        "purpose": ("Unified journal-style figure system (scripts/report_style.py). Figures are re-drawn "
                    "from the same verified inputs/saved tables; no numerical result is recomputed "
                    "differently, no data are added. Earlier provenance JSONs are unchanged; this file "
                    "records the superseded and new hashes."),
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/apply_figure_style.py", "script_sha256": sha256(__file__),
        "style": rs.style_info(),
        "untouched": ["report/artwork/*", "report/screenshots/*", "report/figures/cover_concept.pdf",
                      "report/figures/fig01_workflow.pdf", "report/figures/fig03_feature_diagnostics.pdf",
                      "report/figures/sampling_autocorrelations.pdf", "report/figures/gmm_sensitivity.pdf"],
        "outputs": records,
    }
    dump_json(ROOT / "report/figure_style_provenance.json", provenance)
    print(json.dumps([{k: r[k] for k in ("filename", "changed", "sha256")} for r in records], indent=1))


if __name__ == "__main__":
    main()
