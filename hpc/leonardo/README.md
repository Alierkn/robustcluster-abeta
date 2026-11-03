# Leonardo preparation — no execution claimed

Official reference inspected 2026-09-21: [CINECA Leonardo documentation](https://docs.hpc.cineca.it/hpc/leonardo.html). Recheck it before actual submission: resource names, accounting, limits, module stacks and access policies can change.

This repository contains a parameterized CPU analysis template, not evidence that Leonardo was used. No project account, username, partition or QoS is supplied. No job has been submitted by this project. The DPC implementation is CPU-based; a GPU allocation is not justified by this code.

After complete data validation and review of local scaling measurements, set an accessible project working directory, create the verified environment, and select actual account/partition/time/memory/CPU resources from your allocation. Pass scheduler resources as `sbatch` command-line options; the script deliberately does not invent them. Set `ROBUSTCLUSTER_CONFIG` to a reviewed configuration with full execution enabled. Run one seed job at a time unless the aggregate node memory requirement has been checked.

```bash
export ROBUSTCLUSTER_PROJECT=/absolute/path/to/robustcluster-abeta
export ROBUSTCLUSTER_CONFIG=/absolute/path/to/reviewed-config.yaml
export ROBUSTCLUSTER_PYTHON=/absolute/path/to/venv/bin/python
# Supply your verified account, partition and resource flags to sbatch.
sbatch YOUR_VERIFIED_SCHEDULER_FLAGS hpc/leonardo/analysis.slurm
```

Before submission, archive the exact submitted script and config. Actual execution must retain SLURM job IDs, requested/allocated resources, module list, Python/package versions, stdout/stderr, `sacct` job accounting, input hashes and analysis manifests. These records are required before describing any computation as performed on Leonardo. If access has only been introduced conceptually, describe it only after the internship participant confirms that fact.
