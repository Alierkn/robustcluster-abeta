# Rebuild storyboard: visuals, evidence and page structure

Stage 1 planning, 2026-11-03. This document applies to the separate `report-rebuild-2026-11-03` worktree. It does not alter the released report, rerun an experiment, or assert that the proposed page layout has been built. Paths below are repository-relative and identify existing assets.

## Narrative and evidence decisions

The report should lead the reader through a concrete internship problem: understanding the available Aβ40 descriptors, checking the inherited analysis, and testing whether a correlated descriptor can be removed without changing assignments. The original published workflow provides the methodological context. The completed GMM experiment supplies the independent numerical investigation. Research-software practice and the student's confirmed hands-on learning connect these parts.

The October planning record was consulted as a historical outline. Two statements there are now obsolete: a complete FES has since passed grid validation, and the proposed GMM pilot has since completed. The current evidence is the successful manifests below and the v0.1.2 report, not the October plan's pending statuses. No private conversation links or correspondence are reproduced here.

Use one compact evidence-status table near the end of Chapter 1, then explain a limitation beside the result that it qualifies. Chapter 7 should discuss their consequences together. Avoid repeating a full warning list in every chapter. Distinguish a missing input from an algorithm that was implemented but not run, and distinguish both from a completed test on synthetic data.

## Verified source records

| Key | Existing record | What it establishes |
|---|---|---|
| D | `results/manifests/20260921T011959-583b4421.json` | Successful real descriptor diagnostics; unweighted biased sample. Its historical “complete FES missing” message belongs to September and is superseded by F for file availability only. |
| D-repeat | `results/manifests/20260921T013152-c45e6960.json` | Independent diagnostic rerun; the six numerical-table hashes match D. Figure byte hashes can differ because of run metadata. |
| F | `results/manifests/20261007T102957-e2a462e5.json` | Successful complete-grid and descriptor-query validation; no empirical weights or cluster populations. |
| G | `results/manifests/20261007T104141-f0143175.json` | Successful 50-model GMM ablation/seed pilot; fixed 3,000-row fit sample, 300,003 labelled evaluation rows including fit rows. |
| GF | `results/manifests/20261007T104846-17f8483c.json` | Successful GMM figure and summary-table generation from G. |
| W | `results/manifests/20261007T115101-b5fc7418.json` | Corrected workflow arrows; conceptual geometry change only. Supersedes the old workflow artwork, not the descriptor calculations. |
| Q | `results/manifests/20261103T131615-qa-72d4c6.json` | Selected v0.1.2 QA: 36 tests, lint and saved-output checks; this stage has not rerun them. |
| R | `results/manifests/20261103T131528-report-67e955.json` | Selected v0.1.2 build: 22 main-text pages and 38 total. This is a baseline measurement, not the rebuilt report's page count. |

Source-table paths are expanded below. `report/data_provenance.json`, `report/revision_provenance.json` and `report/artwork_provenance.json` record imported-asset hashes. A read-only SHA256 check in this planning stage found all 21 listed imported assets and all 39 outputs across D, F, G, GF and W present and matching their recorded hashes. No scientific rerun was needed for this check.

The ignored raw descriptor table and FES are **not present in this new worktree**. The verified saved outputs and report assets are present. Rebuilding prose and the PDF can use those assets; rerunning data analysis would require separately supplied, hash-matched raw inputs. Do not silently copy, publish or reconstruct missing raw files.

## Main-text visual storyboard

Figure numbers should be assigned only after the actual figure order is settled. Existing file stems are stable asset identities, not a requirement to manufacture missing figures 2–11 from the original wish list.

| Placement and question | Exact existing asset | Source and teaching purpose | Required interpretation |
|---|---|---|---|
| Cover: what is this project? | `report/artwork/cover-editorial-v2.png` plus `report/artwork/messina-logo-user-supplied.png`; approved placement is implemented in `report/report.tex` | `report/artwork_provenance.json`. Reuse the accepted editorial artwork and supplied logo; preserve cover details and academic year 2025–2026. | Conceptual generated artwork, not a molecular image or a measured free-energy landscape. The logo is a separate supplied institutional asset. |
| Chapter 2: why an ensemble and why bias? | `report/artwork/ensemble-editorial-v2.png` and `report/artwork/bias-editorial-v2.png` | `report/artwork_provenance.json`, prompts in `docs/ARTWORK_PROMPTS.json`. One restrained paired illustration near the ensemble/bias explanation. | A visual metaphor only. Link the physical explanation to equations and literature; do not assign atom identities, cluster counts or numerical minima to the artwork. |
| Chapter 3: which stages transform the input into the intended result? | `report/figures/fig01_workflow.pdf` | W; exact generating output `results/figures/20261007T115101-b5fc7418/fig01_workflow.pdf`; generator `scripts/refresh_workflow_figure.py`. Shows data validation, discovery, consensus, assignment and weighting as distinct steps. | An implementation map, not a record that every box completed. Retain corrected boundary-clipped arrows. This existing technical diagram is not a substitute for requested illustration artwork. |
| Chapter 6: why question SASA redundancy? | `report/figures/fig03_feature_diagnostics.pdf` | D; `results/tables/20260921T011959-583b4421/feature_correlation.csv` and `results/tables/20260921T011959-583b4421/pca.json`. Connect correlation and standardized PCA to the feature-ablation question. | Biased-sample geometry. The Rg–SASA correlation is 0.847578… and the first two PCA variance fractions sum to 0.880886…; neither proves that SASA can be removed safely. Use existing generated numerical macros for rounded prose. |
| Chapter 6: how much independent information is present? | `report/figures/sampling_autocorrelations.pdf` | D; `results/tables/20260921T011959-583b4421/autocorrelations.csv`, interpreted with `results/tables/20260921T011959-583b4421/sampling_diagnostics.csv`. Shows persistence and differences among replicas. | All 12 correlation-ESS estimates fail at least one reliability check. The lag axis is biased simulation time; no physical relaxation or transition-rate claim. Explain the flag once in the caption and discussion. |
| Chapter 6: what changes when SASA is removed or initialization changes? | `report/figures/gmm_sensitivity.pdf` | GF → G. Source tables `results/tables/20261007T104141-f0143175/ablation.csv` and `results/tables/20261007T104141-f0143175/seed_stability.csv`; summarized in `results/tables/20261007T104846-17f8483c/ablation_summary.csv`. | The complete tested component-count range is shown. Observed seed ranges are not confidence intervals; evaluation includes fitting observations. GMM components and raw label fractions are not equilibrium conformational families or populations. |
| Chapter 8: how does a small implementation choice protect an analysis? | Searchable listing `report/generated/fit_scaler.py` | Hash in `report/revision_provenance.json`; analysis implementation `src/robustcluster_abeta/gmm_ablation.py`; relevant checks in `tests/test_gmm_ablation.py`. A short code panel can explain fitting a scale once and reusing it. | A real source excerpt, not a screenshot of an invented coding session. This demonstrates a software decision, not a new biological finding or a claim of unaided line-by-line authorship. |

Empirical plots retain PDF vector exports for LaTeX and existing SVG counterparts under their source run directories. Their common style is `src/robustcluster_abeta/publication.mplstyle`; diagnostic generation is in `src/robustcluster_abeta/plotting.py`, and GMM figures in `scripts/build_gmm_figures.py`. A later redesign must regenerate from the same successful source tables with a new figure manifest, not redraw data manually.

## Appendices and reusable supporting evidence

| Asset or table | Exact source | Proposed role |
|---|---|---|
| Replica histograms | `report/figures/raw_descriptor_distributions.pdf`; D source `results/tables/20260921T011959-583b4421/raw_histograms.csv` | Appendix C; main text briefly refers to it when explaining replica differences. Common bin edges and density normalization must remain explicit; no equilibrium correction. |
| Full correlation/ESS table | `report/generated/sampling_rows.tex`; D source `results/tables/20260921T011959-583b4421/sampling_diagnostics.csv` | Appendix C; all 12 rows and reliability flags retained. The main text states the overall outcome and shows the ACF figure. |
| Full seed matrices | `report/figures/gmm_seed_matrices.pdf`; GF → G source `results/tables/20261007T104141-f0143175/seed_stability.csv` | Appendix C; preserve every tested component count. The main figure gives the comparison; this allows the reader to inspect each pair. |
| Numerical GMM summary | `report/generated/gmm_rows.tex`; GF source `results/tables/20261007T104846-17f8483c/ablation_summary.csv` | Appendix C unless a concise main-text table replaces, rather than duplicates, a figure panel. Keep model-local label interpretation. |
| Full FES integrity summary | `results/tables/20261007T102957-e2a462e5/fes_validation.json`; explanatory record `docs/FES_VALIDATION_2026-10-07.md` | Appendix D or a small main-text audit table. Preserve 2,801 × 1,301 grid, 3,644,101 rows, all 300,003 queries in bounds, and the unverified energy-unit/construction boundary. |
| Genuine VMD screenshot | `report/screenshots/vmd-gyration.jpg`; capture record `report/revision_provenance.json` | Software appendix with readable excerpt `report/generated/vmd-mcp-excerpt.py`. Link to the inspected commit's `src/vmd_mcp/server.py`, lines 250–266, at commit `01912595595bf0302124f57559e1e6a22095fb24`. |
| Genuine GROMACS screenshot | `report/screenshots/gromacs-mdrun.jpg`; capture record `report/revision_provenance.json` | Software appendix with readable excerpt `report/generated/gromacs-mcp-excerpt.py`. Link to `src/gromacs_mcp/server.py`, lines 1452–1467, at commit `2c5c957c3f2c047888b63ae258ace3df34cb8773`. |
| Software environment | `report/generated/environment_rows.tex`; D and subsequent run manifests | Appendix F; distinguish analysis-environment versions from the original simulation software. Include public code/download instructions in Appendix E. |

The screenshots are real browser captures of source code, not evidence of an executed MD job. Searchable listings and immutable source links are the reusable content; screenshots serve orientation. Companion repository identities and student-confirmed experience are detailed in `LEARNING_EVIDENCE_MAP.md`.

Appendix A holds the full parameter tables, separating implemented reproduction settings from the completed GMM protocol. Appendix B holds derivations and estimator conventions. Appendix D also holds the detailed audit and assistance/artwork disclosure. Keep these accessible by cross-reference rather than repeating them in the main text.

## Missing visuals and analytical prerequisites

| Requested content | Current evidence | Decision for the rebuild |
|---|---|---|
| Quantitative FES/reweighting illustration | Complete numerical grid validated; energy unit, producing commands and replica-combination procedure unresolved; no empirical weight table | Do not present an equilibrium FES or weighted result. Use the actual grid-validation table and an equation-led explanation. Any later raw-grid plot would need a separately logged plotting run, explicit unspecified units and no equilibrium interpretation. |
| Real DPC decision plot, consensus matrix/dendrogram | Plotting routines and synthetic tests exist; no completed real paper-DPC output selected | No empirical figure. Explain the algorithm with the preserved workflow and equations; synthetic demonstrations must stay unmistakably test fixtures if ever used. |
| Weighted structural/additional-descriptor summaries and relevance | No validated empirical weights or completed corresponding cluster analysis | Omit result panels rather than fill empty placeholders. Raw descriptors do not become weighted summaries by relabelling a caption. |
| Paper-DPC robustness | Planned seed, feature and scaling experiments not completed | Present the completed GMM pilot separately, with its own method and purpose. Do not call its matrices “DPC stability.” |
| Representative structures or ShapeGMM | No verified atomic trajectory, topology or frame mapping | No invented molecular structures or pseudo-renderings. Existing conceptual art remains conceptual. |
| External Aβ40 ensemble and Aβ42 comparison | No completed compatible external analysis or Aβ42 dataset | Literature context and future work only; no numerical comparative panels. |

## Nine-chapter page budget

Page counts below include figures and tables within the main scientific text. Cover, abstract, contents, references and appendices are excluded. The 22-page target allows explanation suitable for a Data Analysis undergraduate; the 20-page fallback shortens background and methods by one page each without shrinking type. Actual pagination must be measured after the rebuild.

| Chapter | Target pages | Reading purpose and visual allocation |
|---|---:|---|
| 1. Introduction and internship objectives | 1 | Biological/computational question, student task, compact contribution/status statement. No broad literature survey repeated later. |
| 2. Scientific and theoretical background | 4 | Ensemble → MD → sampling → WT-MetaD → FES/reweighting → descriptors/clustering. One conceptual illustration pair; equations introduced by the question they answer. |
| 3. Data and computational methodology | 4 | Data identity, interval and units; scaling; three clustering stages; interpolation and replica weighting; fixed-label uncertainty scope. One workflow, not multiple versions. |
| 4. Reproduction and scientific code audit | 2 | The scientifically consequential corrections, evidence boundaries and test strategy. Long defect lists and full test inventory go to appendices. |
| 5. Robustness extension | 2 | Motivation and prespecified completed GMM design; ACF/PCA conventions; concise separation from planned DPC/reweighting alternatives. No result duplication. |
| 6. Results | 4 | Descriptor/PCA, sampling, FES validation and GMM sensitivity in that order. Three main empirical figures; detailed numerical and replica tables in Appendix C. |
| 7. Discussion | 2 | What correlation did and did not predict; seed dependence; implications for reproduction; combined limitations and next decisive analyses. |
| 8. Internship outcomes and skills | 2 | Confirmed GROMACS/VMD/Python learning, companion projects, one readable code panel and a measured personal reflection. Avoid an unverified activity diary. |
| 9. Conclusions and future work | 1 | Answer the actual project question, distinguish completed contribution from the next reproducibility gate, and give concrete next steps. |
| **Total** | **22** | **20-page fallback: Chapters 2 and 3 each use 3 pages.** |

## Typography and visual rules to preserve

- Keep `scrreprt`, LuaLaTeX/Biber, A4, one-sided 11 pt, Libertinus Serif/Sans/Math and the existing 25/23/23/24 mm left/right/top/bottom margins. No new font selection or application migration is needed.
- Keep navy `#173A5E`, teal `#2E6F73`, body ink `#20242A`, cool grey `#F3F5F7` and muted audit accent `#A95542`. Use ordinary prose and whitespace for most hierarchy. Reserve a small number of boxes for one central equation or consequential audit point.
- Preserve the approved 42 mm supplied logo at the exact A4 page center, with the existing restrained shadow and unaltered logo bytes. Do not move it back under the university name. The title-page source, rather than an obsolete preview PDF, defines this composition.
- Use `booktabs`, units in table headers and common numerical precision. Captions explain what is encoded, how it was calculated and the limitation needed to interpret it. Keep the source manifest in provenance records rather than crowding every caption with hashes.
- Preserve vector scientific figures and selectable text/equations/code. Do not turn plots or code into decorative raster images. No fabricated workflow screenshot, molecular rendering or “laboratory” image.
- Reuse disclosed generated art if it serves the explanation. Any later new illustration must use the image-generation tool with saved prompts/provenance; do not substitute a decorative diagram or claim an unexposed model version.
- The existing report is untagged. Metadata, bookmarks and searchable text are useful but do not establish PDF/UA compliance. Preserve that honest accessibility status and perform visual and compiler QA after rebuilding.

Existing source-based design reasoning is in `docs/EDITORIAL_DESIGN_RESEARCH_V011.md` and `docs/TYPOGRAPHY_AND_WRITING.md`. This plan adds no new literature claims or bibliography entries and does not claim Adobe application use.

## Final implementation decision

The planning budget above was a target, not measured output. The final redesign uses 29/26/25/25 mm left/right/top/bottom margins, 11 pt Libertinus body text and a measured 18-page main text. This supersedes the earlier margin recommendation. Three empirical panels were regenerated from the same saved tables by `scripts/build_editorial_figures.py`, run `20261103T135347-e4275730`; no numerical analysis was rerun. Plot labels use embedded DejaVu Serif TrueType fonts while document text and mathematics remain Libertinus. The approved cover, centred logo, conceptual art and corrected workflow are preserved. See `REBUILD_RECORD.md` for selected build/QA evidence.
