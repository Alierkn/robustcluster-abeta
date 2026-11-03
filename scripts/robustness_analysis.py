"""Thin entry point with an explicit extension configuration."""
import sys
from robustcluster_abeta.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["robustness", "--config", "config/robustness.yaml", *sys.argv[1:]]))
