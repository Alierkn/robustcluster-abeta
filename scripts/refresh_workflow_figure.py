"""Regenerate only the conceptual workflow, preserving numerical run evidence."""

import json
from pathlib import Path
import shutil

from robustcluster_abeta.manifest import Run, dump_json, sha256
from robustcluster_abeta.plotting import workflow

ROOT = Path(__file__).resolve().parents[1]
run = Run({"project_root": str(ROOT), "inputs": {}, "purpose": "workflow layout only"},
          "workflow-figure")
try:
    workflow(run)
    run.finish("SUCCESS")
except Exception as error:
    run.finish("FAILED", str(error))
    raise
destination = ROOT / "report/figures/fig01_workflow.pdf"
shutil.copy2(run.path("figures", "fig01_workflow.pdf"), destination)
provenance = ROOT / "report/data_provenance.json"
record = json.loads(provenance.read_text())
for item in record["outputs"]:
    if item["filename"] == str(destination.relative_to(ROOT)):
        item["sha256"] = sha256(destination)
        break
else:
    raise RuntimeError("Workflow figure missing from report provenance")
record["workflow_override"] = {"manifest": str(run.file.relative_to(ROOT)),
                               "sha256": sha256(run.file),
                               "reason": "Clip arrows to actual box boundaries; no numerical changes"}
dump_json(provenance, record)
print(run.id)
