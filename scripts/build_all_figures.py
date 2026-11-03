"""Rebuild figures from a hash-verified successful analysis manifest."""
import sys
from robustcluster_abeta.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["figures", *sys.argv[1:]]))
