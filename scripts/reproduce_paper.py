"""Thin entry point; see robustcluster reproduce --help."""
import sys
from robustcluster_abeta.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["reproduce", *sys.argv[1:]]))
