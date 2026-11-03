# Figure catalogue and evidence status

The report numbers only figures actually included. The requested project figure IDs below are stable file identifiers, not a claim that every planned figure has been produced. All empirical figures are generated from source tables; the workflow is a code-generated conceptual diagram.

| Requested ID | Content / file stem | Current empirical status |
|---|---|---|
| 1 | `fig01_workflow` | Generated conceptual workflow |
| 2 | `fig02_fes` | BLOCKED for equilibrium interpretation: complete grid recovered and validated, but energy units and construction provenance unresolved; plotting tested with a fixture |
| 3 | `fig03_feature_diagnostics` | Generated from real unweighted descriptor correlation and PCA tables |
| 4 | `fig04_density_decision` | BLOCKED for real data; fixture-tested plotting |
| 5 | `fig05_consensus` | BLOCKED for real data; fixture-tested plotting |
| 6 | `fig06_structural_summary` | BLOCKED for real data; fixture-tested plotting |
| 7 | `fig07_additional_descriptors` | BLOCKED for real data; fixture-tested plotting |
| 8 | `fig08_cluster_relevance` | BLOCKED for real data; fixture-tested plotting |
| 9 | `fig09_stability` | BLOCKED for paper-DPC robustness; separate real GMM seed/feature pilot completed (see below) |
| 10 | Molecular representatives | BLOCKED: no atomic trajectory/topology/frame map |
| 11 | External Aβ40 comparison | Deferred; no compatible external analysis completed |
| Additional | `raw_descriptor_distributions` | Generated real unweighted histograms |
| Additional | `sampling_autocorrelations` | Generated real biased-stream ACF diagnostics; all correlation-ESS estimates flagged unreliable |

The report imports run `20260921T011959-583b4421`. `report/data_provenance.json` records its manifest hash and every imported figure/generated table hash. PDF and SVG exports share one Matplotlib style. The fresh-environment Snakemake run independently produced the same numerical diagnostic tables in `20260921T013152-c45e6960`; run-specific figure metadata need not be byte-identical.

## Completed GMM extension (separate from planned paper-DPC figures)

`report/figures/gmm_seed_matrices.pdf` and the GMM figures referenced by Chapters 5–6 are generated from the independent 50-fit pilot. See `report/revision_provenance.json` and `docs/GMM_ABLATION_PILOT.md` for their exact source manifests. They represent descriptor-space agreement and biased frame frequencies, not equilibrium populations.
