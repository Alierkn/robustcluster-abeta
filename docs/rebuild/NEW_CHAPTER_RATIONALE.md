# New report argument: introduction, results, discussion, learning and conclusions

Date: 3 November 2026. Five chapters were drafted from blank files under `report-next/` in the separate reconstruction worktree. The released `report/` sources are unchanged. The academic-latex-writer guidance was applied to explanatory flow, claim scope and scientific clarity. This stage reconstructs the argument; it does not optimize detector scores or change numerical analysis.

## New argument structure

| Chapter | Organizing question | New structure | Approximate prose words |
|---|---|---|---:|
| 1. Introduction and internship objectives | What changes when a familiar numerical table represents a biased molecular ensemble? | Begin with rows, dependence and interpretation; connect the learning programme to ensembles; introduce the Aβ40 materials; formulate three questions about reconstruction, diagnostics and SASA removal. | 558 |
| 6. Results | What do the completed calculations actually show? | Start with a compact scope table; establish valid inputs; move from descriptor relationships to temporal dependence, then to the controlled GMM comparison. Read cross-feature and within-feature agreement together. | 659 |
| 7. Discussion | What can the feature comparison tell us, and what would make the next comparison stronger? | Explain why global correlation cannot determine clustering; separate initialization variation from fitting-sample sensitivity; connect the independent experiment to the published workflow; discuss sampling and weighting. | 533 |
| 8. Internship outcomes and skills | How did molecular concepts, practical software use and analysis connect? | Confirmed learning context and GROMACS reflection; one concrete analysis example; personally created MCP projects explained through source behavior; reusable outcomes. | 596 |
| 9. Conclusions and future work | What is established and what should happen next? | State the code and GMM contributions; give the FES provenance prerequisite; sequence bounded reproduction and distinct structural/reweighting extensions. | 274 |

Total: approximately 2,620 prose words. Counts exclude headings, figure/table environments, citations, cross-references and link destinations. These are source-level estimates, not a typeset page count. Chapters 1 and 7 have three sections; chapters 6 and 8 have four. The short conclusion is continuous prose.

The argument no longer follows a sequence of software-audit disclaimers. Limitations appear where they change the interpretation: biased observations in the introduction, unreliable ESS in the sampling result, fixed fitting observations in the GMM discussion, and absent provenance before the next reproduction step. Captions retain enough scope to be read independently.

## Confirmed personal account

First person is confined to Chapter 8. The following confirmed reflection is retained exactly:

> Learning to use GROMACS was one of the more challenging parts of the internship for me. I found the process demanding at first, but I also enjoyed becoming more familiar with the software.

The newly confirmed practical use of GROMACS, VMD and Python and personal creation of VMD MCP and GROMACS MCP are stated directly. No commands, systems, simulation durations, attendance events or specific learning episodes were invented. Contributor histories remain acknowledged; the report makes no sole-authorship claim.

## Evidence and semantic checks

| Statement family | Evidence basis | Boundary preserved |
|---|---|---|
| Internship contacts, degree and learning sequence | User-provided information and documented programme | Assigned topics are not presented as proof of mastery. |
| Practical software use and MCP creation | Student confirmation supplied for this stage | No trajectory is attributed to these interfaces. |
| MCP functions and units | Previously inspected commit-specific source excerpts | Available code is distinct from execution evidence; unit and atom-selection compatibility remain necessary. |
| Descriptor dimensions and FES grid | Existing inventory and saved validation | A complete numerical grid does not establish energy units or the FES construction. |
| Correlation, PCA, ESS and timing/memory values | Existing generated macros | ESS remains provisional; memory sampling scope is stated; no new analyses are claimed. |
| GMM agreement and convergence | Existing recorded pilot and generated GMM table | One fitting sample, biased observations, evaluation including fitting rows; no equilibrium or physical-state-count claim. |
| Reproduction and structural extensions | Existing implementation and input inventory | Full empirical DPC/reweighting and representative structures remain incomplete. |
| Leonardo | Existing submission template | No Leonardo jobs or execution claimed. |

The result chapter preserves the original numerical scope: three segments of 100,001 rows; a 2,801 × 1,301 FES grid; 50 GMM fits; three-component cross-feature ARI 0.862–0.868; median matched agreement approximately 95.3%; within-space ranges 0.994–1.000 and 0.988–1.000. The two-component within-space minima remain 0.011 and 0.067. The generated table is included directly rather than copied into a new manually maintained table.

Existing citation keys only: `barducci2008`, `barker2022`, `borthakur2025`, `cadenelli2026`, `grossfield2019`, `michaud2011`, `plumed2019`, `sasmal2024`, `vanderlee2014`, `wratten2021`. No bibliography metadata was created.

## Integration checks

Chapter 6 defines `tab:status`, `fig:features`, `fig:acf`, `fig:gmm` and `tab:gmm`. It expects appendix labels `fig:rawdistributions` and `fig:seedmatrices`. Figures use the existing validated assets `fig03_feature_diagnostics.pdf`, `sampling_autocorrelations.pdf` and `gmm_sensitivity.pdf`; the GMM table uses `generated/gmm_rows.tex`. Existing generated values and revision values supply all numerical macros. The software appendix should retain its immutable source links for the MCP excerpts.

A source check confirmed existing citation keys, balanced braces, figure asset existence, exact preservation of the confirmed reflection, one chapter per file, and absence of trailing whitespace. The released report has no tracked changes. No build, commit, new empirical calculation or external detector check was performed in this subtask. Final layout, bibliography and cross-reference checks belong to the coordinator's complete report build.
