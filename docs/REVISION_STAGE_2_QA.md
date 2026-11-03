# Full-report revision and release QA — 7 October 2026

The delivered report has **22 main-text pages and 37 total pages**. Cover: Ali Erkan Ocaklı, Data Analysis L-31, matricola 555012, internship contacts Andrea Ciccolo and Valeria Conti Nibali, academic year 2025–2026. The abstract has 301 words. No signature, logo, attendance record or unverified supervisor role was invented.

## Evidence and presentation

- Descriptor diagnostics from the original successful run are retained.
- Complete FES validation: `20261007T102957-e2a462e5`; numerical completeness and coverage do not establish energy units or construction provenance.
- Independent GMM pilot: `20261007T104141-f0143175`; 50 converged fits, fixed 3,000-frame balanced fit sample, 300,003-frame descriptive evaluation. All tested component counts and seeds are retained. No optimal biological family count is claimed.
- Sensitivity figures: `20261007T104846-17f8483c`; PDF/SVG generated from verified source tables. Seed matrices appear in the appendix.
- Conceptual cover: original deterministic vector illustration, explicitly not a molecular structure or observed clustering result.
- Two unchanged browser screenshots from immutable VMD MCP/GROMACS MCP source URLs; provenance and hashes in `report/revision_provenance.json`. These are software evidence, not simulation records.
- Searchable code excerpt and companion repository links are included; Codex assistance is disclosed in Appendix D.

## Checks performed

Full build: `20261007T111251-report-711d8d`. Release QA: `20261007T111345-qa-01d2bf`.

35 tests passed, with no failures or skips; Ruff passed. Successful scientific and figure output hashes were checked. All 34 bibliography entries have matching verification-register records and are cited; no unresolved citations or cross-references were reported by the final build. Numerical formulas distinguish molar energy units, replica normalization, distribution width and uncertainty. The current report makes no empirical equilibrium-weight claim.

All 37 rendered pages were inspected as contact sheets; changed outcomes and code-audit pages were inspected separately at higher resolution. No visible clipping, overlap or missing graphics was found. Short chapter endings retain whitespace. The build has no overfull boxes or missing-character warnings. Two unicode-math compatibility warnings and five underfull-box messages remain recorded in the manifest; these did not produce visible defects. This is not a claim of a warning-free log.

Original Downloads script, descriptor data and complete FES were rehashed against their preserved local copies with exact matches. The historical partial download is no longer at its original location and was not used. These checks and the visual review are recorded in `20261007T111600-release-evidence`. The new optional GMM Snakemake target passed a dry run; it was not executed again merely for workflow integration.

## Release boundary

This is a completed report/software revision with a completed descriptor-only extension. Scientific paper reproduction remains **BLOCKED** by unresolved FES energy units and construction provenance. Paper-DPC robustness, reweighting sensitivity, structural figures, DPA/ShapeGMM and external validation are not presented as completed. No Aβ42 result or Leonardo execution is claimed. RobustCluster is a local Git repository, not a newly published GitHub repository. Supplied raw materials remain excluded from the source archive; the previous release was preserved separately.
