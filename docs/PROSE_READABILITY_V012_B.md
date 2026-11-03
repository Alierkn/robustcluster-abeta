# Readability revision — chapters 2–5

Date: 2026-11-03. Comparison baseline: Git commit `6d1fc92`.

Scope: `02_background.tex`, `03_methodology.tex`, `04_audit.tex`, and `05_robustness.tex`. The academic-latex-writer skill's editorial guidance was applied: explain the consequential relationship, retain precise scientific terms, preserve uncertainty and distinguish planned work from completed calculations. No illustrations, equations, numerical settings, citations, headings or labels were changed. No detector score was used to choose wording.

## Editorial changes

The revision replaces compressed or abstract wording with concrete subjects and actions. Brief explanations are added where they help a Data Analysis undergraduate follow the argument: a descriptor-based ensemble, frame identity, numerical overflow, the role of a silhouette coefficient, and the distinction between cluster spread and uncertainty in average relevance. Necessary technical terms remain, including quasi-stationarity, bilinear interpolation, covariance, Wasserstein distance and conditional uncertainty.

Representative examples (plain text excerpts; mathematical expressions and LaTeX commands are omitted where unnecessary):

| Before | After | Reason |
|---|---|---|
| “An ensemble description retains both conformations and their statistical weights.” | “An ensemble describes the conformations a molecule can adopt and the statistical weight of each one.” | Gives the reader a concrete meaning for the central term. |
| “statistical inefficiency describes the resulting inflation of estimator variance” | “statistical inefficiency measures how this dependence increases the variance of an estimate” | Connects the statistical term directly to dependence between observations. |
| “the analyzed interval admits the quasi-stationary interpretation needed for this correction” | “the analyzed interval can be treated as quasi-stationary, with a sufficiently stable bias for this correction to apply” | Explains the assumption without presenting it as verified. |
| “subject to the validity condition that the number of labels lies between two and…” | “when the number of labels lies between two and…, as required for a valid calculation” | Keeps the validity condition while simplifying the sentence. |
| “empirical marginal descriptor distributions” | “the observed distributions of a single descriptor” | Makes the separate one-dimensional comparisons explicit before explaining what the metric misses. |
| “the output includes an explicit overflow/underflow status” | “the output flags overflow or underflow” | Uses a direct verb; the preceding sentence explains what the flags mean. |
| “monotonized by cumulative minima” | “Each retained pair sum is then limited to the smallest pair sum seen so far.” | Describes the same numerical operation in ordinary language. |
| “an orthogonal rotation of standardized variables” | Retained, with the explanation that keeping all components preserves Euclidean distances. | Keeps a precise mathematical term where an approximate synonym would weaken the explanation. |

## Semantic review

- **Background:** ensemble weights, the molecular/molar energy distinction, bias effects, and the limits of descriptor-based clustering remain. The FES explanation retains integration over unrepresented coordinates; it does not suggest averaging free energies. No unbiased kinetics or reconstructed HILLS are claimed.
- **Methodology:** frame identities, interval assumptions, min–max scaling, DPC tie handling, thresholds and stopping conditions remain. The Wasserstein metric still combines separate one-dimensional distances. FES bounds, equal replica weighting, and the fixed-partition scope of the planned bootstrap remain explicit.
- **Audit:** original-file preservation, the line-437 syntax error, the missing V2 evidence, and the difference between code inspection and successful execution remain. The complete grid is still distinguished from verified units and construction provenance.
- **Robustness:** the autocorrelation heuristic and all screening thresholds remain. Kish ESS is still separate from correlation ESS. The completed GMM comparison still uses the same fitting sample and all-frame evaluation; no held-out predictive claim or population confidence interval has been introduced. DPC robustness, reweighting comparisons, DPA, ShapeGMM and external validation keep their existing pending or blocked status.

## Verification performed

A local preservation check compared each chapter with `HEAD` at the stated baseline. All four chapters passed equality checks for:

1. inline mathematics and complete displayed-equation environments;
2. citation commands and citation-key order;
3. chapter/section commands, labels and cross-reference commands;
4. complete figure environments, including captions;
5. ordered numerical tokens.

`git diff --check` passed for the four chapter files. These are prose-preservation checks, not new numerical experiments or software tests. A manual scientific reading was also performed because matching tokens alone cannot establish that prose preserves meaning.

Whitespace-delimited source word counts changed from 4,749 to 4,937 across the four chapters, an increase of 188 words (about 4%). The extra length mainly explains unfamiliar terms; some procedural wording was shortened. These counts include LaTeX source and are not a rendered main-text page count. Compilation and visual pagination review are left to the coordinating editor; no PDF build or Git commit was made by this subtask.
