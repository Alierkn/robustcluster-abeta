"""Run provenance. Each immutable run has distinct logs, tables and figures."""

import datetime as dt
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
import uuid
from pathlib import Path

import yaml

from .validation import InvalidInput


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def git_metadata(root):
    """Report this project's Git state; an archive must not inherit its parent's."""
    root = Path(root)
    if not (root / ".git").exists():
        return {"git_commit": None, "git_dirty": None}
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                              capture_output=True, text=True)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                capture_output=True, text=True)
    except FileNotFoundError:
        return {"git_commit": None, "git_dirty": None}
    return {"git_commit": head.stdout.strip() if head.returncode == 0 else None,
            "git_dirty": bool(status.stdout.strip()) if status.returncode == 0 else None}


def load_config(path, profile=None):
    path = Path(path).resolve()
    config = yaml.safe_load(path.read_text())
    if not isinstance(config, dict):
        raise InvalidInput("Configuration must be a mapping")
    root = (path.parent / config.get("project_root", "..")).resolve()
    config["project_root"] = str(root)
    config["config_file"] = str(path)
    config["config_sha256"] = sha256(path)
    if profile:
        config["profile"] = profile
    if config["profile"] not in config["profiles"]:
        raise InvalidInput("Unknown execution profile")
    config["execution"] = dict(config["profiles"][config["profile"]])
    for name in ["descriptors", "fes"]:
        if config["inputs"].get(name):
            config["inputs"][name] = str((root/config["inputs"][name]).resolve())
    return config


class Run:
    def __init__(self, config, command, experiment=None):
        self.config = config
        self.root = Path(config["project_root"])
        self.started = time.monotonic()
        self.id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]
        self.file = self.root/"results/manifests"/f"{self.id}.json"
        self.file.parent.mkdir(parents=True, exist_ok=True)
        versions = {}
        for name in ["numpy", "scipy", "scikit-learn", "pandas", "matplotlib", "robustcluster-abeta"]:
            try:
                versions[name] = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                versions[name] = None
        source_hashes = {str(p.relative_to(self.root)): sha256(p) for p in
                         sorted((self.root/"src").rglob("*.py"))}
        self.data = {"schema_version": 1, "run_id": self.id, "status": "RUNNING", "command": command,
                     "experiment": experiment, "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                     **git_metadata(self.root),
                     "source_sha256": source_hashes, "python": platform.python_version(), "versions": versions,
                     "config": config, "inputs": {}, "outputs": [], "runtime_seconds": None,
                     "peak_rss_bytes": 0}
        dump_json(self.file, self.data)

    def path(self, kind, name):
        path = self.root/"results"/kind/self.id/name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def register_inputs(self):
        for key, filename in self.config["inputs"].items():
            if key in {"descriptors", "fes"} and filename:
                path = Path(filename)
                self.data["inputs"][key] = {"filename": path.name, "exists": path.is_file(),
                                             "sha256": sha256(path) if path.is_file() else None}
        dump_json(self.file, self.data)

    def finish(self, status, message=None):
        if self.data["status"] != "RUNNING":
            raise RuntimeError("Finished manifests cannot be reused")
        self.data["status"] = status
        self.data["message"] = message
        self.data["runtime_seconds"] = time.monotonic()-self.started
        for kind in ["tables", "figures", "logs"]:
            folder = self.root/"results"/kind/self.id
            if folder.exists():
                self.data["outputs"].extend({"filename": str(p.relative_to(self.root)), "sha256": sha256(p)}
                                            for p in sorted(folder.rglob("*")) if p.is_file())
        dump_json(self.file, self.data)
