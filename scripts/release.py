"""Create a source archive without private source materials or build caches."""

import datetime as dt
import json
from pathlib import Path
import subprocess
import zipfile

from robustcluster_abeta.manifest import dump_json, sha256

ROOT = Path(__file__).resolve().parents[1]
archive = ROOT.parent / "robustcluster-abeta-source.zip"
records = []
for path in sorted((ROOT / "results/manifests").glob("*.json")):
    if path.name == "local_provenance.json":
        continue
    value = json.loads(path.read_text())
    records.append({"filename": str(path.relative_to(ROOT)), "sha256": sha256(path),
                    "command": value.get("command"), "experiment": value.get("experiment"),
                    "status": value["status"]})
qa = [r for r in records if r["command"] == "release-qa"][-1]
if qa["status"] != "SUCCESS":
    raise RuntimeError("Most recent release QA did not pass")
report = [r for r in records if r["command"] == "report-build" and r["status"] == "SUCCESS"][-1]
build = json.loads((ROOT / report["filename"]).read_text())
manifest = {"project": "RobustCluster-Aβ", "version": "0.1.1",
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "scientific_reproduction_status": "BLOCKED",
            "release_status": "REPORT_WITH_DESCRIPTOR_EXTENSION_AND_BLOCKED_EQUILIBRIUM_REPRODUCTION",
            "completed": ["source inventory and method audit", "modular numerical implementation",
                          "analytic and synthetic tests", "real descriptor validation/correlation/PCA/ACF diagnostics",
                          "complete FES grid and descriptor-coverage validation",
                          "independent 50-fit real-data GMM sensitivity pilot",
                          "vector figures and source tables", "personalized LuaLaTeX/Biber report",
                          "generated editorial cover/illustrations, searchable source panels and genuine code screenshots", "isolated-environment release QA"],
            "blocked": ["complete final-bias reproduction: FES energy units and construction provenance unresolved",
                        "paper-DPC seed/feature/Wasserstein robustness: FES provenance gate",
                        "time-dependent weight comparison: FES and rbias provenance",
                        "Scientific V2 audit: file unavailable", "structural analysis: coordinates unavailable"],
            "deferred_optional": ["DPA", "ShapeGMM", "external Aβ40 validation"],
            "hpc_jobs_submitted": 0, "abeta42_analyses_performed": 0,
            "report": {"filename": "report/report.pdf", "sha256": sha256(ROOT / "report/report.pdf"),
                       "main_text_pages": build["main_text_pages"], "total_pages": build["total_pages"]},
            "selected_report_manifest": report, "selected_qa_manifest": qa,
            "run_manifests": records,
            "historical_report_note": "Early draft build manifests referenced a mutable report.pdf. They are retained as historical logs, superseded by the selected immutable build snapshot; their old PDFs are not claimed available.",
            "source_archive_exclusions": ["raw descriptor data", "legacy supplied script", "publisher PDF",
                                          "complete and partial FES inputs", "local provenance paths", "Git/runtime/build caches"]}
target = ROOT / "release_manifest.json"
# Package tracked files plus the newly generated release manifest. This is an audited allowlist.
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
files = [ROOT / name for name in tracked if name and name != "release_manifest.json"]
for path in files:
    relative = path.relative_to(ROOT)
    if relative.parts[:2] == ("data", "raw") and path.name != ".gitkeep":
        raise RuntimeError("Raw input unexpectedly tracked; refusing archive")
    if path.name in {"CLUSTERING40_ottimizzato.py", "local_provenance.json"} or "build" in relative.parts:
        raise RuntimeError(f"Excluded source unexpectedly tracked: {relative}")
manifest["archived_files"] = [{"filename": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in files]
dump_json(target, manifest)
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
    for path in files + [target]:
        output.write(path, "robustcluster-abeta/" + str(path.relative_to(ROOT)))
# The archive's own checksum must remain external to avoid self-reference.
(ROOT.parent / "robustcluster-abeta-source.zip.sha256").write_text(f"{sha256(archive)}  {archive.name}\n")
print(json.dumps({"archive": str(archive), "sha256": sha256(archive), "files": len(files) + 1,
                  "scientific_reproduction": "BLOCKED"}))
