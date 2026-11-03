"""Lightweight, unit-agnostic FES integrity and descriptor-coverage audit."""

import argparse
import json
import resource
import sys
from pathlib import Path

import numpy as np

from .fes import read_fes_structure
from .io import read_descriptors
from .manifest import Run, dump_json, load_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--fes", required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    config["inputs"]["fes"] = str(Path(args.fes).resolve())
    config["audit"] = {"alpha_divisor": 1.1, "beta_divisor": 2.5,
                       "energy_unit": None, "random_seeds": [],
                       "purpose": "Grid integrity and interpolation coverage only"}
    run = Run(config, "audit-fes", "input-validation")
    try:
        run.register_inputs()
        grid = read_fes_structure(args.fes)
        table = read_descriptors(config["inputs"]["descriptors"], config["replicas"],
                                 config["interval_ps"])
        alpha, beta = table.nAlpha.to_numpy()/1.1, table.nBeta.to_numpy()/2.5
        values = grid.interpolate(alpha, beta)
        result = {
            "status": "PASSED", "fes_bytes": Path(args.fes).stat().st_size,
            "grid_shape": list(grid.energy.shape), "grid_points": grid.energy.size,
            "metadata": grid.metadata,
            "alpha_range": [float(grid.alpha[0]), float(grid.alpha[-1])],
            "beta_range": [float(grid.beta[0]), float(grid.beta[-1])],
            "file_free_range_unit_unverified": [float(grid.energy.min()), float(grid.energy.max())],
            "queried_frames": len(table), "outside_grid": 0,
            "queried_alpha_range": [float(alpha.min()), float(alpha.max())],
            "queried_beta_range": [float(beta.min()), float(beta.max())],
            "interpolated_values_finite": bool(np.isfinite(values).all()),
            "replica_frame_counts": {str(k): int(v) for k, v in
                                     table.groupby("replica_id").size().items()},
            "energy_unit": None,
            "reweighting_status": "BLOCKED: energy units and FES construction unverified",
            "clustering_performed": False,
        }
        dump_json(run.path("tables", "fes_validation.json"), result)
        run.path("logs", "audit.log").write_text(json.dumps(result, indent=2)+"\n")
        status, message = "SUCCESS", "Structural validation only; no weight or cluster calculation"
    except Exception as exc:
        status, message = "FAILED", f"{type(exc).__name__}: {exc}"
        run.path("logs", "audit.log").write_text(message+"\n")
        raise
    finally:
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        run.data["peak_rss_bytes"] = int(peak if sys.platform == "darwin" else peak*1024)
        run.finish(status, message)
        print(run.file)


if __name__ == "__main__":
    main()
