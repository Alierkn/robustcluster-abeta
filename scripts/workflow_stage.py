"""Snakemake adapter; success pointers refer to verified immutable run manifests."""
import argparse
import json
from pathlib import Path

from robustcluster_abeta.cli import execute
from robustcluster_abeta.manifest import dump_json, load_config, sha256

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=["validate", "diagnostics", "reproduce", "robustness", "gmm-ablation"])
parser.add_argument("--config", required=True)
parser.add_argument("--pointer", required=True)
parser.add_argument("--experiment")
args = parser.parse_args()
config = load_config(args.config)
folder = Path(config["project_root"])/"results/manifests"
before = set(folder.glob("*.json"))
code = execute(config, args.stage, args.experiment)
if code:
    raise SystemExit(code)
new = set(folder.glob("*.json"))-before
matches = [p for p in new if json.loads(p.read_text()).get("command") == args.stage]
if len(matches) != 1:
    raise RuntimeError("Ambiguous concurrent workflow outputs; inspect manifests")
pointer = Path(args.pointer)
pointer.parent.mkdir(parents=True, exist_ok=True)
dump_json(pointer, {"manifest": str(matches[0].relative_to(Path(config["project_root"]))),
                    "sha256": sha256(matches[0])})
