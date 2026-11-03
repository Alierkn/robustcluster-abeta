# Readability revision v0.1.2 — chapters 1 and 6–9

Date: 3 November 2026. Scope: introduction, results, discussion, internship outcomes and conclusions. This pass makes the English more direct and easier for a capable undergraduate to explain. It is a readability edit, not a detector-score intervention or a change of scientific evidence.

The academic-latex-writer guidance was used to preserve claims and qualifications while replacing abstract nouns and administrative phrasing with concrete descriptions. No new personal experience was introduced. The student's confirmed two-sentence GROMACS reflection remains exactly as supplied in the preceding version.

## Examples of substantive changes

| Before | After / reason |
|---|---|
| “The completed work comprises a source audit, tested numerical routines…” | “The completed work includes the code audit, tested analysis routines…” followed by the actual checks and comparison; clearer account of what was done |
| “construction provenance” | “the way it was constructed,” where the meaning can be explained without a specialist provenance term |
| “The table passed the schema, finite-value and interval checks…” | “The table had the expected columns, finite values and interval coverage”; names the checks in ordinary language |
| “high cross-representation agreement” | “agree well both between feature sets and between initializations”; states what is being compared |
| “Two levels of model adequacy remain unresolved” | “There are two further questions about the models”; followed by the local-solution and physical-state limitations |
| “concentration of the weights” | “a few large weights could make estimates depend strongly on a small part of the sample”; explains the statistical concern |
| “The project demonstrates software practices through concrete artifacts” | “The software work is documented through preserved inputs…”; starts with the actual files and records |
| “bounded computational study” | A direct description of the code checks, tested routines and GMM comparison |

Thirty-eight paragraphs were revised. Precise terms such as ARI, PCA, equilibrium probability, component count and initialization are retained where they matter. The revision explains relationships in simpler sentences instead of replacing necessary scientific vocabulary with loose synonyms.

## Meaning preserved

- The completed GMM comparison concerns a biased descriptor sample, includes fitting rows in evaluation and uses one fixed fitting sample.
- Strong Rg–SASA correlation does not establish that SASA may be removed without changing the fitted groups.
- The three-component result remains conditional on the tested fits; it is not a selected biological state count.
- Every correlation ESS estimate fails at least one reliability check. The estimates remain provisional warning indicators, not precise independent-conformation counts.
- A complete FES grid does not verify its energy units, construction or bias convergence.
- Weighted published-workflow reproduction, structural representatives and Leonardo execution remain unperformed.
- Companion source code is not presented as evidence that the supplied trajectories were generated through those interfaces.

## Source checks

Comparison with committed chapter sources confirmed identical numerical literals and their order, numerical macros, citation commands and coverage, chapter/section headings, labels, displayed equations, and figure/table environments. Cross-references still point to the same labels; two sentence-initial forms use `Cref` instead of `cref` for capitalization. The GROMACS reflection was checked for exact preservation.

Whitespace checks passed. Across these five chapter sources, the whitespace-delimited count changed from 2,890 to 2,977 words. The small increase comes mainly from explaining compressed technical phrases. It is not a typeset page-count claim. The coordinator still needs to compile and inspect the complete report after integrating the parallel edits.

No analysis code, numerical output, configuration, bibliography, abstract, preamble or appendix was changed in this subtask. No build, commit or detector test was performed here.
