# Project inventory

Initial inspection: 2026-09-21. This inventory describes supplied evidence, not a completed reproduction. Originals are unchanged. Absolute local source locations are stored in the local, untracked provenance manifest; portable identities use SHA256.

| Filename | Purpose / dimensions | Status |
|---|---|---|
| CLUSTERING40_ottimizzato.py | 39,233 bytes; monolithic analysis | Preserved in legacy; AST parsing fails at line 437 (uncommented Italian sentence) |
| input_clustering_ab40.dat | 300,003 rows × 10 columns; 31,137,940 bytes | Three time-reset segments of 100,001 frames each; all values finite |
| acs.jpcb.6c01000.pdf | 12-page publisher PDF; 5,466,024 bytes | Inspected locally; not redistributed in source archive |
| Unconfirmed 525059.crdownload | 35,435,466 bytes | Rejected: 472,467 complete records and one partial record, versus 3,644,101 expected grid points |
| CLUSTERING40_scientific_v2.py | Audited intermediate requested by brief | NOT FOUND; cannot audit its contents or claim its corrections |
| SCIENTIFIC_V2_CHANGELOG.md | Intermediate-version history | NOT FOUND |
| FES_AB_40.dat | Required final-bias FES; 3,644,101 × 5; 273,309,138 bytes | Received 2026-10-07; grid and all 300,003 descriptor queries validated; units/construction still unresolved |
| HILLS, project COLVAR, PLUMED input | Bias reconstruction and provenance | NOT FOUND; generic VMD plugin templates are not simulation evidence |
| Topology / atomic trajectory | Structure extraction and coordinate benchmarks | NOT FOUND |
| Existing numerical results and execution logs | Previous-run evidence | NOT LOCATED in identified project materials |

## Input schema

Original header: `time metad.rbias nalpha nbeta RG SASA ASASA PSASA HBONDSPP HBONNDSPS`.

Canonical names: `time_ps`, `metad_rbias`, `nAlpha`, `nBeta`, `Rg`, `SASA`, `ASASA`, `PSASA`, `HBONDSPP`, `HBONDSPS`. Header spelling is retained in manifests. The second column is not an FES: it is labelled `metad.rbias`. Its generating command and energy units remain unverified.

Each segment runs from 1,000,000 to 3,000,000 in increments of 20. The original script labels time as ps, Rg as nm and SASA as nm². These source-supported interpretations are recorded as provenance assumptions, not independent verification of the simulation setup. The interval includes both endpoints. The source row and per-replica frame indices are zero-based; replica IDs and physical file-line numbers are one-based.

The partial FES header names `alpha antibeta file.free der_alpha der_antibeta`, with nonperiodic axes 0–28 and 0–13, and 2,801 × 1,301 grid points. It ends in the fragment `18.99000`. It must not be repaired, padded, clipped, renamed into a valid input, or used for empirical weights.

## What can be reproduced now

Input validation, source-code audit, descriptor distributions, correlations, PCA diagnostics, and sampling-correlation diagnostics can be generated from the real descriptor table. Analytic fixtures can test numerical machinery, but are never evidence about Aβ40.

Final-bias populations, weighted cluster descriptors, completed paper reproduction, and reweighting sensitivity are BLOCKED by the unit/construction-provenance gate (complete grid recovered 2026-10-07). Molecular representatives and ShapeGMM require actual coordinates. Published Aβ42 findings are literature context only. No Leonardo execution evidence is available.

## Initial environment

The original global Python was 3.14.3; NumPy and SciPy were discoverable, while scikit-learn, pandas, Matplotlib, pytest, PyYAML and Snakemake were absent. LuaLaTeX/Biber were not detected. Implementation uses an isolated Python 3.12 environment and records actual installed versions; these must not be confused with the authors' simulation software.

## File hashes

Implementation update: an isolated Python 3.12.6 environment and a project-local TeX Live 2026 installation now exist. Actual analysis versions appear in run manifests and requirements-lock.txt. The initial dependency gaps above describe the starting point, not the final environment. Report builds record LuaLaTeX/Biber versions separately.

- `CLUSTERING40_ottimizzato.py`: `cfd76ebb6eb2fe193c342587b19cef402c29dabbdf63347d3b481656ae46e579`
- `input_clustering_ab40.dat`: `cc44ee36a80ae7b04fe035f27ee6764323125e16f139a4ddc533a8a9089bfd77`
- `acs.jpcb.6c01000.pdf`: `eaa43b7315a6c81841f23f289602c159f7c7a77a9a1ed524bf391f638be2de53`
- `Unconfirmed 525059.crdownload`: `fdcf3b2e50f37441c86ca1f12fc90bbbe8da018152e6f84f1ebe64a006066b80`

## Complete FES recovered — 2026-10-07

SHA256: `6fd6c3d7c04e20859cf91abb4765e126e0f3fcb982d3795b643165dde26fa3f4`. Unchanged local copy: `data/raw/FES_AB_40.dat`, excluded from Git. The source was supplied by the user after locating Andrea’s 18 September “Clustering Files” SharePoint link. This identifies the transfer source, not the upstream FES construction procedure. Numerical audit: [FES validation](FES_VALIDATION_2026-10-07.md). The historical partial download above remains rejected.

## Independent GMM pilot — 2026-10-07

Descriptor-only feature ablation completed in run `20261007T104141-f0143175`: 50 fitted models, all converged; 3,000 fit rows; 300,003 evaluation rows. This is a separate unweighted extension, not a DPC reproduction or equilibrium analysis. See [pilot report](GMM_ABLATION_PILOT.md).
