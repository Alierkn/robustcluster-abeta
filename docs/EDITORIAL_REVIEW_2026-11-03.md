# Editorial review — 3 November 2026

## Purpose and scope

This review revises the nine report chapters for a clear, evidence-based undergraduate research voice. It does not attempt to optimize an AI-detector score or conceal assistance. The existing report is an internship research report with a completed descriptor-space experiment and an incomplete reproduction of the published equilibrium analysis; it is not described as an accepted or submission-ready journal article.

The review used the current chapter sources, generated numerical values and GMM table, the correlation and GMM implementation, and the existing project records. No new empirical computation, literature verification, or personal interview was performed. The surrounding report, cover, bibliography and generated scientific outputs were not edited in this subtask.

## Material decisions

| Location | Earlier wording or issue | Revision and reason | Effect on scientific scope |
|---|---|---|---|
| Introduction | Broad question about how much grouping is supported by descriptors | State the actual SASA-removal and initialization question investigated by the GMM pilot | Narrows the question to the completed experiment |
| Methodology, normalization | Sensitivity to a different metric described as being tested in “the extension” | Identify standardization in the GMM protocol and distinguish the unrun DPC scaling experiments | Removes a possible implication that DPC sensitivity has been computed |
| Results status and discussion | “All correlation-estimator reliability checks fail” | Every replica–descriptor series fails **at least one** criterion | Corrects a logical overstatement; unchanged underlying outputs |
| Background and audit | Phrases about a “license to infer,” “an error for its own sake,” and “familiar-looking” plots | Explain the required data, documented correction and source-table linkage directly | Removes rhetorical language without relaxing evidence requirements |
| Results and conclusions | Broad statements about a “reproducible scientific foundation” | Lead with the observed dependence of SASA-ablation agreement on component count and initialization | Gives the reader a concrete empirical conclusion |
| Discussion | General benefits of reproducibility | Name the reusable saved assignments, source tables, and missing FES information | Makes the scope of independent reproduction explicit |
| Internship outcomes | General claims of learning and favorable plots | Describe inspectable software outputs, retained runs and provenance examples | Adds no invented experience, hours or personal reaction |

## Claim-to-evidence boundaries retained

- Strong Rg–SASA correlation motivates a question; it does not establish dispensability of SASA.
- The GMM experiment concerns the biased descriptor sample, evaluates all frames including fit rows, and holds the fit subset fixed. It is not a held-out predictive validation or a source of equilibrium populations.
- Component count was varied by design; the three-component agreement does not select a physical number of states.
- Numerical convergence and seed agreement do not establish a global optimum or kinetic metastability.
- Every provisional correlation ESS estimate is unreliable under at least one configured heuristic. These outputs are diagnostics, not calibrated independent-sample counts or physical relaxation times.
- Complete-grid validation does not establish FES energy units or construction provenance.
- The original script remains unchanged; unavailable Scientific V2 material is not reconstructed.
- The discussion retains the absence of atomic trajectories, external ensemble validation and Leonardo execution.

## Verification performed

A source comparison confirmed that all citation commands/keys, chapter and section headings, labels, and cross-reference commands remain unchanged. The chapter whitespace-delimited word count is 7,569 both before and after the targeted replacements; this is a source-text count, not a typeset report word count. `git diff --check -- report/chapters` passed. Numerical tables, macros, equations, source code and bibliography were not changed.

Compilation, pagination and rendered-page inspection are reserved for the coordinator after all parallel edits are integrated. No claim of a successful revised PDF build is made by this review alone.

## Remaining editorial and publication considerations

1. The report can be evaluated as a documented undergraduate computational project. A journal submission would require a journal-specific scope and format, resolution of the main reproduction blockers or a deliberately narrower methods/descriptor study, and an appropriate scientific review.
2. First-person claims of learning, satisfaction or difficulty should come from the student. This edit makes no such claims on the student's behalf.
3. AI-detector results, if obtained, must name the service, date and exact document version. They should not be presented as evidence of authorship, scientific accuracy or publishability.
4. A final build must recheck that the full main text remains within the agreed 18–22-page range and that the unchanged numerical tables and figure captions remain legible.

## Coordinator integration

The abstract was subsequently revised to state the SASA-removal question, the recorded Rg–SASA correlation and PCA fraction, and the actual GMM design. Its numerical values use existing generated macros. The reproducibility appendix now links to the main package and LaTeX sources. These edits change neither numerical results nor the explicit disclosure of assistance. The detector excerpt remains an immutable pre-revision record.
