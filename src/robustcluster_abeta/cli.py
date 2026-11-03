"""Bounded subprocess execution with durable success/failure/block manifests."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

import psutil

from .manifest import Run, dump_json, load_config


def worker(manifest_path):
    from . import pipeline
    from .validation import BlockedAnalysis, Budget
    data = json.loads(Path(manifest_path).read_text())
    run = object.__new__(Run)
    run.config = data["config"]
    run.root = Path(run.config["project_root"])
    run.id = data["run_id"]
    budget = Budget(run.config["execution"]["max_seconds"], run.config["execution"]["max_memory_gib"])
    status, message, summary = "SUCCESS", None, {}
    try:
        pipeline.validate_configuration(run.config)
        command = data["command"]
        if command == "gmm-ablation":
            from .gmm_ablation import experiment
            summary = experiment(run.config, run, budget)
        elif command == "robustness":
            summary = pipeline.robustness(run.config, run, budget, data["experiment"])
        elif command == "figures":
            summary = pipeline.rebuild_figures(run.config, run, budget, data["source_manifest"])
        else:
            summary = getattr(pipeline, command)(run.config, run, budget)
    except BlockedAnalysis as exc:
        status, message = "BLOCKED", str(exc)
    except Exception as exc:
        status, message = "FAILED", f"{type(exc).__name__}: {exc}"
        traceback.print_exc()
    dump_json(run.path("logs", "outcome.json"), {"status": status, "message": message, "summary": summary})
    print(json.dumps({"status": status, "message": message, "summary": summary}), flush=True)
    return {"SUCCESS": 0, "BLOCKED": 2, "FAILED": 3}[status]


def execute(config, command, experiment=None, source_manifest=None):
    run = Run(config, command, experiment)
    run.data["source_manifest"] = source_manifest
    run.register_inputs()
    environment = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                       MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0")
    reason = None
    peak = 0
    try:
        with run.path("logs", "execution.log").open("w") as log:
            log.write(json.dumps({"run_id": run.id, "command": command, "config": config}) + "\n")
            log.flush()
            process = subprocess.Popen([sys.executable, "-m", "robustcluster_abeta.cli", "_worker", str(run.file)],
                                       stdout=log, stderr=subprocess.STDOUT, env=environment)
            monitored = psutil.Process(process.pid)
            while process.poll() is None:
                try:
                    members = [monitored] + monitored.children(recursive=True)
                    rss = sum(member.memory_info().rss for member in members if member.is_running())
                    peak = max(peak, rss)
                except psutil.NoSuchProcess:
                    pass
                elapsed = time.monotonic()-run.started
                if elapsed > config["execution"]["max_seconds"]:
                    reason = "Recorded runtime budget exceeded"
                if peak > config["execution"]["max_memory_gib"]*2**30:
                    reason = "Recorded process-tree memory budget exceeded"
                if reason:
                    for child in monitored.children(recursive=True):
                        child.kill()
                    process.kill()
                    process.wait()
                    break
                time.sleep(0.1)
        outcome_path = run.path("logs", "outcome.json")
        if reason:
            outcome = {"status": "FAILED", "message": reason, "summary": {}}
        elif outcome_path.exists():
            outcome = json.loads(outcome_path.read_text())
            if process.returncode != 0 and outcome["status"] == "SUCCESS":
                outcome.update(status="FAILED", message="Worker exited nonzero despite success outcome")
        else:
            outcome = {"status": "FAILED", "message": f"Worker exited {process.returncode} without outcome", "summary": {}}
        run.data["peak_rss_bytes"] = peak
        run.data["resource_measurement"] = "process-tree RSS sampled every 0.1 s; may miss shorter peaks"
        run.data["summary"] = outcome["summary"]
        run.finish(outcome["status"], outcome["message"])
    except BaseException as exc:
        if "process" in locals() and process.poll() is None:
            process.kill()
            process.wait()
        if run.data["status"] == "RUNNING":
            run.finish("FAILED", f"Supervisor interrupted: {exc}")
        raise
    print(f"{run.data['status']}: {run.file}")
    if run.data.get("message"):
        print(run.data["message"])
    return {"SUCCESS": 0, "BLOCKED": 2, "FAILED": 3}[run.data["status"]]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "_worker":
        return worker(argv[1])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "diagnostics", "reproduce", "robustness", "figures", "gmm-ablation"])
    parser.add_argument("--config", default="config/paper_reproduction.yaml")
    parser.add_argument("--profile", choices=["smoke", "medium", "full"])
    parser.add_argument("--experiment", choices=["seeds", "seed-pilot", "features", "wasserstein", "reweighting", "dpa", "shapegmm", "external_validation"])
    parser.add_argument("--source-manifest")
    args = parser.parse_args(argv)
    if args.command == "robustness" and not args.experiment:
        parser.error("robustness requires --experiment")
    if args.command == "figures" and not args.source_manifest:
        parser.error("figures requires --source-manifest")
    config = load_config(args.config, args.profile)
    return execute(config, args.command, args.experiment, args.source_manifest)


if __name__ == "__main__":
    raise SystemExit(main())
