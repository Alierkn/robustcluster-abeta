#!/usr/bin/env bash
# Resource/account/partition/QoS flags must be supplied from a verified allocation.
set -euo pipefail
: "${ROBUSTCLUSTER_PROJECT:?Set the verified project directory}"
: "${ROBUSTCLUSTER_CONFIG:?Set a reviewed full-run config path}"
: "${ROBUSTCLUSTER_PYTHON:?Set the analysis environment Python executable}"
cd "$ROBUSTCLUSTER_PROJECT"
job_tag="${SLURM_JOB_ID:-unsubmitted}"
if [[ "$job_tag" == unsubmitted ]]; then
  echo 'This template must run inside an actual SLURM allocation.' >&2
  exit 2
fi
mkdir -p "results/logs/hpc-${job_tag}"
env | sort | sed -n '/^SLURM_/p' > "results/logs/hpc-${job_tag}/slurm-environment.txt"
if type module >/dev/null 2>&1; then
  module list 2> "results/logs/hpc-${job_tag}/modules.txt"
fi
"$ROBUSTCLUSTER_PYTHON" -m pip freeze > "results/logs/hpc-${job_tag}/packages.txt"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
"$ROBUSTCLUSTER_PYTHON" -m robustcluster_abeta.cli reproduce \
  --config "$ROBUSTCLUSTER_CONFIG" --profile full
