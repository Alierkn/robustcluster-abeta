"""Run release checks in the active (preferably fresh) Python environment."""

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET

from robustcluster_abeta.manifest import dump_json, sha256, git_metadata

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--originals-dir", type=Path)
args = parser.parse_args()
run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-qa-" + uuid.uuid4().hex[:6]
folder = ROOT / "results/logs" / run_id
folder.mkdir(parents=True)
path = ROOT / "results/manifests" / f"{run_id}.json"
started = time.monotonic()
manifest = {"run_id": run_id, "command": "release-qa", "status": "RUNNING",
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "python_executable": sys.executable, "checks": {}, "outputs": [],
            **git_metadata(ROOT)}
dump_json(path, manifest)
try:
    for name, command in [
        ("pytest", [sys.executable, "-m", "pytest", "-q", f"--junitxml={folder / 'tests.xml'}"]),
        ("ruff", [sys.executable, "-m", "ruff", "check", "src", "tests", "scripts"]),
    ]:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=300)
        (folder / f"{name}.log").write_text(result.stdout + result.stderr)
        manifest["checks"][name] = {"returncode": result.returncode, "command": command}
        if result.returncode:
            raise RuntimeError(f"{name} failed")
    suite = ET.parse(folder / "tests.xml").getroot().find("testsuite")
    manifest["checks"]["test_counts"] = dict(suite.attrib)
    originals = {"CLUSTERING40_ottimizzato.py": "cfd76ebb6eb2fe193c342587b19cef402c29dabbdf63347d3b481656ae46e579",
                 "input_clustering_ab40.dat": "cc44ee36a80ae7b04fe035f27ee6764323125e16f139a4ddc533a8a9089bfd77",
                 "acs.jpcb.6c01000.pdf": "eaa43b7315a6c81841f23f289602c159f7c7a77a9a1ed524bf391f638be2de53",
                 "Unconfirmed 525059.crdownload": "fdcf3b2e50f37441c86ca1f12fc90bbbe8da018152e6f84f1ebe64a006066b80"}
    if args.originals_dir:
        for name, expected in originals.items():
            if sha256(args.originals_dir / name) != expected:
                raise RuntimeError(f"Original hash changed: {name}")
        manifest["checks"]["original_hashes"] = originals
    else:
        manifest["checks"]["original_hashes"] = "NOT CHECKED: supply --originals-dir"
    for name, folder_name in [("CLUSTERING40_ottimizzato.py", "legacy"),
                               ("input_clustering_ab40.dat", "data/raw")]:
        local = ROOT / folder_name / name
        if local.exists() and sha256(local) != originals[name]:
            raise RuntimeError(f"Preserved copy changed: {name}")
    bib = (ROOT / "report/references.bib").read_text()
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    literature = json.loads((ROOT / "docs/literature.json").read_text())
    verified = {r["key"] for r in literature if r["verified"]}
    if keys != verified:
        raise RuntimeError("Bibliography and verification matrix differ")
    sources = "\n".join(p.read_text() for p in (ROOT / "report").rglob("*.tex") if "build" not in p.parts)
    cited = set()
    for match in re.findall(r"\\(?:auto|text|paren)?cite\{([^}]+)\}", sources):
        cited.update(match.split(","))
    if cited - keys:
        raise RuntimeError(f"Unresolved bibliography keys: {cited - keys}")
    manifest["checks"]["bibliography"] = {"verified_entries": len(keys), "cited_entries": len(cited),
                                            "uncited_entries": sorted(keys - cited)}
    run_records = []
    for candidate in sorted((ROOT / "results/manifests").glob("*.json")):
        if candidate == path or candidate.name == "local_provenance.json":
            continue
        record = json.loads(candidate.read_text())
        if record.get("command") in {"validate", "diagnostics", "reproduce", "robustness", "figures", "audit-fes", "gmm-ablation", "gmm-figures", "revision-preview", "workflow-figure", "editorial-figures"}:
            if record["status"] == "RUNNING":
                raise RuntimeError(f"Unfinished analysis: {candidate.name}")
            for output in record["outputs"]:
                if sha256(ROOT / output["filename"]) != output["sha256"]:
                    raise RuntimeError(f"Analysis output mismatch: {output['filename']}")
            run_records.append({"manifest": candidate.name, "status": record["status"]})
    manifest["checks"]["analysis_output_integrity"] = run_records
    reports = [p for p in sorted((ROOT / "results/manifests").glob("*.json"))
               if json.loads(p.read_text()).get("command") == "report-build"
               and json.loads(p.read_text()).get("status") == "SUCCESS"]
    selected = reports[-1]
    report = json.loads(selected.read_text())
    for output in report["outputs"]:
        if sha256(ROOT / output["filename"]) != output["sha256"]:
            raise RuntimeError("Selected report build output changed")
    snapshots = [r for r in report["outputs"] if r["filename"].endswith("/report.pdf")]
    if len(snapshots) != 1 or sha256(ROOT / "report/report.pdf") != snapshots[0]["sha256"]:
        raise RuntimeError("Convenience report differs from immutable build snapshot")
    if not report["page_target_met"] or any(any(term in w for term in ["Overfull", "multiply-defined", "multiply defined"]) for w in report["warnings"]):
        raise RuntimeError("Report page target or layout warning gate failed")
    manifest["checks"]["report"] = {"manifest": str(selected.relative_to(ROOT)), "sha256": sha256(selected),
                                      "main_text_pages": report["main_text_pages"],
                                      "warnings": report["warnings"]}
    manifest["status"] = "SUCCESS"
except Exception as error:
    manifest.update(status="FAILED", message=str(error))
finally:
    manifest["runtime_seconds"] = time.monotonic() - started
    manifest["outputs"] = [{"filename": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in sorted(folder.glob("*"))]
    dump_json(path, manifest)
print(json.dumps({"run_id": run_id, "status": manifest["status"], "message": manifest.get("message")}))
raise SystemExit(0 if manifest["status"] == "SUCCESS" else 3)
