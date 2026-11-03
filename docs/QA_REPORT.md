# Release quality audit

Audit date: 2026-09-21. This is an audited software and incomplete scientific-report release, not a completed reproduction of the paper.

## Executed checks

- Fresh Python 3.12 environment installed from requirements-lock.txt, followed by the local package. Thirty tests passed, with zero failures, errors or skips. Ruff passed. Detailed commands, JUnit results and hashes are retained in release-qa manifest `20260921T013338-qa-8359de`.
- The actual Snakemake workflow completed validation and descriptor diagnostics locally, with one core. Its log is `results/logs/workflow-verification.log`. Diagnostic tables from the fresh environment exactly match the report's selected run, as checked in `results/logs/fresh_diagnostics_comparison.json`.
- All scientific run output hashes checked successfully, including the logs explaining blocked stages. Original Downloads materials and preserved local copies retain their inventory SHA256 values. No original source was edited.
- All 34 bibliography entries are in the verified literature register and are cited. No unresolved bibliography or cross-reference warnings remain in the final LuaLaTeX/Biber build. Publisher issue-year versus online-publication-year differences are explicit in the literature matrix.
- The final report has 21 main-text pages, 34 pages overall: five front-matter pages, 21 main-text pages, two bibliography pages and six appendix pages. Cover/person-specific placeholders remain intentional.

## Scientific and equation review

Checked the distinction between molar R and molecular k_B, the negative FES sign and WT scaling factor, additive-FES-constant invariance, replica-wise normalization, equal mixture masses, weighted central moments, Kish ESS, and the separation of correlation ESS from reweighted ESS. No formula is used to infer unbiased kinetics. Replica SEM, descriptor distribution width and conditional block-bootstrap intervals are labelled separately. Raw marginal-Wasserstein scaling remains source-informed; normalized distances and PCA are extensions.

The report's numerical prose and sampling table are generated from the selected successful diagnostic manifest. Its empirical claims are confined to validation, unweighted distributions, correlation, PCA and biased-stream ACF diagnostics. All 12 correlation estimates fail the reliability heuristic. No weighted populations, real clustering stability, molecular structures, Aβ42 results or Leonardo executions are asserted. Synthetic results appear only as descriptions of software tests.

## LaTeX and visual review

All 34 rendered pages were reviewed at overview scale, with closer inspection of the empirical figure and sampling-table pages. The report uses Libertinus, vector scientific figures, restrained colour, booktabs tables and consistent captions. No clipped figures, overfull boxes, missing glyphs or unresolved citations remain. Prose was reviewed for unsupported claims, unit consistency and repeated/ambiguous terminology; no external grammar-checking service was used.

Two package interoperability warnings remain: unicode-math chooses the mathtools bracket definitions and replaces its colon commands. The affected commands are not used by the report equations. Five underfull-box messages arise from narrow parameter-table text; visual inspection found no lost content. These warnings are retained in the log rather than suppressed.

Early draft builds included a failed compilation and successful drafts whose report.pdf output path was mutable. Their manifests remain historical evidence; the old draft PDFs are not claimed available. The selected final build, `20260921T013332-report-0c0ec5`, retains an immutable PDF snapshot and passed its output-hash checks. The user-facing `report/report.pdf` matches that snapshot.

## Limits of the release gates

Passing tests validates the implemented behavior on the specified fixtures. It does not establish simulation convergence, independent physical replicas, correct upstream descriptor units or the provenance of a missing FES. GitHub CI is configured but has not run on a remote service. No medium/full empirical DPC run, HPC job, or optional external benchmark was performed. See OPEN_QUESTIONS.md for the evidence needed to complete the scientific work.
