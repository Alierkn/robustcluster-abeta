# Code guide

This guide connects the research questions to the executable files. The package is the source of truth; scripts provide entry points and the report describes recorded outputs.

## Entry points

| Task | Command or source | Required evidence |
|---|---|---|
| Inspect available commands | `robustcluster --help` | Installed package |
| Validate descriptor input | `robustcluster validate --config config/paper_reproduction.yaml` | Authorized descriptor file |
| Correlation, PCA and sampling diagnostics | `robustcluster diagnostics --config config/robustness.yaml` | Valid descriptors |
| Published-workflow implementation | `robustcluster reproduce --config config/paper_reproduction.yaml --profile smoke` | Descriptors, complete FES, verified energy units and provenance |
| Independent GMM feature ablation | `robustcluster gmm-ablation --config config/gmm_ablation.yaml` | Valid descriptors; no FES |
| DPC robustness experiments | `robustcluster robustness --config config/robustness.yaml --experiment seed-pilot` | Same evidence gates as reproduction |
| Rebuild recorded diagnostic figures | `robustcluster figures --config config/robustness.yaml --source-manifest PATH` | Successful source manifest and matching output hashes |
| Compile report | `python scripts/build_report.py --tex-bin PATH` | Saved report assets and LuaLaTeX/Biber toolchain |

Other robustness experiment names are `seeds`, `features`, `wasserstein` and `reweighting`. The last additionally requires verified `metad.rbias` units and provenance. DPA, ShapeGMM and external validation remain disabled optional stages, not completed benchmarks.

## Module responsibilities

All links below lead to inspectable source, including docstrings and the actual numerical choices.

| Module | Responsibility |
|---|---|
| [io.py](../src/robustcluster_abeta/io.py) | Parse ten-column descriptors, detect replica resets, retain original row/line/frame/time identities and apply the analysis interval |
| [preprocessing.py](../src/robustcluster_abeta/preprocessing.py) | Feature scaling/representations and seeded disjoint group construction |
| [dpc.py](../src/robustcluster_abeta/dpc.py) | Pairwise distances, cutoff density, density-peak assignment and iterative quality filtering |
| [consensus.py](../src/robustcluster_abeta/consensus.py) | Marginal Wasserstein distances, source-informed elbow heuristic, pooled family centroids and all-frame assignment |
| [fes.py](../src/robustcluster_abeta/fes.py) | PLUMED grid checks and bounded bilinear interpolation; structural validation separate from authorization to reweight |
| [reweighting.py](../src/robustcluster_abeta/reweighting.py) | Final-bias log weights, optional time-dependent weights and independent per-replica normalization |
| [statistics.py](../src/robustcluster_abeta/statistics.py) | Weighted moments, Kish ESS, autocorrelation diagnostics, replica population summaries and block bootstrap |
| [stability.py](../src/robustcluster_abeta/stability.py) | Frame alignment, ARI and overlap-based family matching |
| [gmm_ablation.py](../src/robustcluster_abeta/gmm_ablation.py) | Separate descriptor-only GMM experiment, shared fit rows and recorded scaling/model parameters |
| [pipeline.py](../src/robustcluster_abeta/pipeline.py) | Scientific stage composition, mode validation and evidence gates |
| [cli.py](../src/robustcluster_abeta/cli.py) | Subprocess supervision, resource limits and explicit exit status |
| [manifest.py](../src/robustcluster_abeta/manifest.py) | Configuration resolution, file hashing, source/environment records and run completion |
| [validation.py](../src/robustcluster_abeta/validation.py) | Finite-value checks, explicit scientific/software errors and budgets |
| [plotting.py](../src/robustcluster_abeta/plotting.py) | Reproducible plots using [one publication style](../src/robustcluster_abeta/publication.mplstyle) |
| [audit_fes.py](../src/robustcluster_abeta/audit_fes.py) | Standalone numerical FES grid and descriptor-coverage audit |

## Numerical contracts to retain

**Frame identity.** Compare partitions only after confirming identical frame identities. Labels have meaning within a fitted partition; integer equality across independent fits is not evidence of the same family.

**Consensus.** Only accepted local clusters enter consensus. Residual frames are excluded at that stage, then every analysis frame is assigned to its nearest global centroid. The consensus metric combines independent one-dimensional Wasserstein distances; it is not a joint four-dimensional Wasserstein distance. Raw descriptor scaling is a documented source-informed baseline where published details remain ambiguous.

**Free energy.** `.crdownload` inputs, missing or duplicate grid cells, nonfinite values and out-of-grid queries fail explicitly. No silent clipping is allowed. Numerical grid completeness does not establish the physical units or construction of an FES.

**Weights.** For molar energies in kJ/mol, the code uses the molar gas constant and `log(w) = -(1 - 1/gamma) F / (R T)`. Normalization uses log-sum-exp within each replica before equal replica pooling. Unrepresentable raw exponentials receive explicit status flags and are not used for normalization.

**Uncertainty.** Weighted standard deviations describe distribution width. Replica SEM, block-bootstrap intervals, seed variation, correlation ESS and Kish weight ESS answer different questions and must retain distinct labels. Biased trajectory time is not unbiased physical kinetics.

## Tracing a result

Start from a successful file in [results/manifests](../results/manifests). Check its configuration, input hashes and recorded outputs. Match the figure to its numerical source and verify the output hashes before interpretation. `BLOCKED` means a required input or provenance condition was unavailable; `FAILED` means the attempted stage did not complete successfully. Neither produces evidence for a scientific result.

The report imports explicitly selected historical analyses. Running a new experiment does not automatically replace the report's evidence. See [reproduction instructions](../REPRODUCIBILITY.md) before promoting a new result.

## Where to look for tests

- [Numerical tests](../tests/test_numerics.py): parsing, scaling, FES structure/interpolation, weights, moments and sampling/partition utilities.
- [Clustering tests](../tests/test_clustering.py): DPC, residual handling, consensus and assignment behavior.
- [Pipeline tests](../tests/test_pipeline.py): deterministic synthetic smoke and end-to-end synthetic weighting.
- [GMM tests](../tests/test_gmm_ablation.py): fit-only scaling and matched labels.
- [Archive provenance test](../tests/test_archive_provenance.py): an extracted archive must not inherit an unrelated parent repository's Git identity.

## Companion projects and preserved code

[**VMD MCP**](https://github.com/Alierkn/vmd-mcp) and [**GROMACS MCP**](https://github.com/Alierkn/gromacs-mcp) are separate companion repositories. The report uses commit-specific source excerpts and genuine screenshots recorded in [revision provenance](../report/revision_provenance.json). They are not required to run this package, and their presence does not establish a molecular-dynamics execution for this project. Consult each repository's own license before reuse.

The supplied `CLUSTERING40_ottimizzato.py` is preserved unchanged locally, including its syntax error, and excluded from public redistribution. See [legacy/README.md](../legacy/README.md). Scientific V2 was unavailable; no substitute intermediate history has been created.
