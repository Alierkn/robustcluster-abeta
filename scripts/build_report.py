"""Build the report with LuaLaTeX/Biber and retain a build manifest and log."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import uuid

from pypdf import PdfReader

from robustcluster_abeta.manifest import dump_json, sha256, git_metadata

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tex-bin", type=Path, help="Verified TeX Live binary directory")
args = parser.parse_args()
if args.tex_bin:
    os.environ["PATH"] = str(args.tex_bin.resolve()) + os.pathsep + os.environ.get("PATH", "")
run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-report-" + uuid.uuid4().hex[:6]
manifest_path = ROOT / "results/manifests" / f"{run_id}.json"
log_folder = ROOT / "results/logs" / run_id
log_folder.mkdir(parents=True)
started = time.monotonic()
manifest = {"schema_version": 1, "run_id": run_id, "command": "report-build",
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "RUNNING",
            **git_metadata(ROOT),
            "tools": {}, "inputs": {}, "outputs": []}
dump_json(manifest_path, manifest)
try:
    for tool in ["latexmk", "lualatex", "biber"]:
        executable = shutil.which(tool)
        if not executable:
            raise FileNotFoundError(f"Missing {tool}: add your TeX Live bin directory to PATH")
        version = subprocess.check_output([executable, "--version"], text=True)
        manifest["tools"][tool] = {"path": executable, "version": version.splitlines()[0]}
    provenance = REPORT / "data_provenance.json"
    evidence = json.loads(provenance.read_text())
    source_manifest = ROOT / evidence["source_manifest"]
    if sha256(source_manifest) != evidence["source_manifest_sha256"]:
        raise RuntimeError("Report diagnostic source manifest changed")
    for record in evidence["outputs"]:
        if sha256(ROOT / record["filename"]) != record["sha256"]:
            raise RuntimeError(f"Report input changed: {record['filename']}; rerun prepare_report.py")
    if "workflow_override" in evidence:
        override = evidence["workflow_override"]
        if sha256(ROOT / override["manifest"]) != override["sha256"]:
            raise RuntimeError("Workflow layout manifest changed")
    revision = json.loads((REPORT / "revision_provenance.json").read_text())
    for record in revision["evidence"].values():
        if sha256(ROOT / record["manifest"]) != record["sha256"]:
            raise RuntimeError("Revision evidence manifest changed")
    for record in revision["outputs"]:
        if sha256(ROOT / record["filename"]) != record["sha256"]:
            raise RuntimeError("Revision report asset changed; rerun prepare_revision.py")
    artwork = json.loads((REPORT / "artwork_provenance.json").read_text())
    if sha256(ROOT / artwork["prompt_file"]) != artwork["prompt_sha256"]:
        raise RuntimeError("Artwork prompts changed")
    for record in artwork["outputs"]:
        if sha256(ROOT / record["filename"]) != record["sha256"]:
            raise RuntimeError("Artwork or source excerpt changed")
    paths = [p for p in REPORT.rglob("*") if p.is_file() and "build" not in p.parts
             and p.suffix in {".tex", ".bib", ".json"}]
    paths += list((REPORT / "figures").glob("*.pdf"))
    paths += list((REPORT / "artwork").glob("*.png"))
    paths += list((REPORT / "screenshots").glob("*.jpg"))
    paths += list((REPORT / "generated").glob("*.py"))
    manifest["inputs"] = {str(p.relative_to(ROOT)): sha256(p) for p in sorted(paths)}
    dump_json(manifest_path, manifest)
    command = ["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error",
               "-outdir=build", "report.tex"]
    manifest["build_command"] = command
    with (log_folder / "latexmk.log").open("w") as stream:
        result = subprocess.run(command, cwd=REPORT, stdout=stream, stderr=subprocess.STDOUT,
                                timeout=600, env=os.environ.copy())
    if result.returncode:
        raise RuntimeError(f"LaTeX build failed; inspect {log_folder / 'latexmk.log'}")
    log = (REPORT / "build/report.log").read_text()
    manifest["warnings"] = re.findall(r"[^\n]*(?:Warning|Overfull|Underfull)[^\n]*", log)
    fatal = ["There were undefined references", "Empty bibliography", "Missing character:",
             "Please (re)run Biber", "multiply-defined labels", "multiply defined"]
    if any(message in log for message in fatal) or re.search(r"Citation .+ undefined", log):
        raise RuntimeError("Report has unresolved citation/reference/font warnings")
    aux = (REPORT / "build/report.aux").read_text()
    end = re.search(r"\\newlabel\{mainend\}\{\{[^}]*\}\{(\d+)\}", aux)
    if not end:
        raise RuntimeError("Cannot establish main-text page count")
    manifest["main_text_pages"] = int(end.group(1))
    pdf = REPORT / "build/report.pdf"
    reader = PdfReader(pdf)
    manifest["total_pages"] = len(reader.pages)
    manifest["page_labels"] = reader.page_labels
    manifest["page_target_met"] = 18 <= manifest["main_text_pages"] <= 22
    shutil.copy2(pdf, REPORT / "report.pdf")
    # Keep the actual build product immutable; report/report.pdf is only a convenience copy.
    shutil.copy2(pdf, log_folder / "report.pdf")
    for filename in ["report.log", "report.blg"]:
        candidate = REPORT / "build" / filename
        if candidate.exists():
            shutil.copy2(candidate, log_folder / filename)
    manifest["status"] = "SUCCESS"
except FileNotFoundError as error:
    manifest.update(status="BLOCKED", message=str(error))
except Exception as error:
    manifest.update(status="FAILED", message=str(error))
finally:
    manifest["runtime_seconds"] = time.monotonic() - started
    outputs = sorted(log_folder.glob("*"))
    manifest["outputs"] = [{"filename": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in outputs]
    dump_json(manifest_path, manifest)
print(json.dumps({key: manifest.get(key) for key in
                  ["run_id", "status", "main_text_pages", "total_pages", "message"]}))
raise SystemExit(0 if manifest["status"] == "SUCCESS" else 2)
