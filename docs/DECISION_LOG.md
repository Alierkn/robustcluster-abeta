# Decision log

| ID | Decision | Why / expected effect | Category / source |
|---|---|---|---|
| D01 | Keep originals byte-for-byte; implement in modules | Preserve historical evidence, including syntax defect | Audit; user brief |
| D02 | Do not fabricate Scientific V2 | Missing file cannot substantiate an audit | Audit; inventory |
| D03 | Exclude partial FES entirely | Missing grid cells invalidate weights | Correction; paper p.6037 / inventory |
| D04 | Use raw marginal-Wasserstein norm in reproduction | Matches supplied code; scaling ambiguity remains visible | Source-informed reproduction; original section 6 |
| D05 | Exclude residuals from consensus; assign all frames in STEP 3 | Align with acceptable-only published workflow | Correction; paper p.6043 |
| D06 | Bilinear FES interpolation and independent replica normalization | Align estimator with published description | Correction; paper p.6037 |
| D07 | Weighted means and population distribution widths | Avoid raw-descriptor statistics under weighted headings | Correction; paper Fig.6–7 |
| D08 | Local default_rng/SeedSequence and stable ties | Reproducible execution; different draws than legacy RandomState | Software correction, explicitly non-bitwise |
| D09 | Correlation ESS describes biased observation stream | Avoid unsupported physical-kinetic interpretation | Robustness extension; WT-MetaD theory |
| D10 | Bounds: smoke/medium locally; full held | Respect accepted compute budget | User-selected execution policy |
| D11 | BSD-3-Clause for new code only | Separate new work from supplied materials' rights | User-selected licensing policy |
| D12 | No empirical final-bias analysis without complete FES | Prevent a superficially complete reproduction | User scientific gate |
| D13 | Original header units are assumptions | Source script supplies units; provenance unavailable | Audit; Q13 |
| D14 | Optional DPA/ShapeGMM/external validation disabled | Do not imply unperformed benchmarks | Extension/future work |
| D15 | Positive paired-lag ACF truncation; require N ≥ 50g and half-window shift ≤ 0.25 SD | Conservative diagnostic heuristic; all real estimates are flagged, not treated as physical correlation times | Extension; sampling-quality literature; statistics.py |
| D16 | Bootstrap blocks of ceil(2 max g), capped at replica length; 500 draws | Preserve within-replica dependence while keeping replicas equally weighted; intervals conditional on fitted labels and supplied FES | Extension; statistics.py; limitations explicit |
| D17 | Keep DPC thresholds unchanged for PCA/ablation experiments | Measure sensitivity to changed geometry, not an optimized replacement | Extension; config/robustness.yaml |
| D18 | Require at least five accepted local clusters and non-flat linkage heights for the cubic elbow | Fail when source-informed elbow cannot be evaluated; heuristic remains an unresolved methodological choice | Source-informed reproduction; original code |
| D19 | Reject changed replica count/window in reproduction mode | Prevent accidental silent departures from the published target | Reproduction contract; user brief |
| D20 | Retain report PDFs inside unique build log directories | Keep final build evidence immutable while providing report/report.pdf as a convenience copy | Reproducibility correction; initial draft builds used a mutable PDF path and are explicitly superseded |

## D21 — 2026-10-07: separate structural FES validation from energy-unit declaration

The complete download is validated without assigning a unit. `read_fes_structure` retains `energy_unit=None`; production `read_fes` still requires explicit kJ/mol and provenance. This is a validation correction, not a change to the published estimator. Source: received FES header and original script line 53 (kJ/mol/K constant). Expected effect: resolve file-completeness and bounds questions while avoiding conversion of a source-code assumption into verified simulation metadata. Copy the validated file locally without altering or publicly redistributing the source.

## D22 — 2026-10-07: bounded GMM feature-ablation pilot, predefined before execution

Question: does removing SASA change partitions of the supplied biased descriptors? Use a fixed, replica-balanced random fit subset of 1,000 frames per replica (sampling seed 20261007), shared by all models. Fit standardization on those rows only. Compare full-covariance GMMs on four features and nAlpha+nBeta+Rg, k=2–6, seeds 42–46, n_init=1, reg_covar=1e-6, tol=1e-3, max_iter=500. GMM random_state uses explicitly recorded local integer seeds; sampling uses default_rng. Evaluate all original frames, including fit rows: descriptive stability, not held-out prediction or independent-sample inference. Fit sample selection stays fixed to isolate initialization/representation sensitivity; it does not remove time correlation. Missing/empty families remain visible. BIC stays within feature space and is not used to assert a biological cluster count. No FES or equilibrium weights used.

Classification: original robustness extension, prompted by the instructor's independent-analysis objective. This is not the paper DPC baseline and not ShapeGMM. Expected effect: quantify partition disagreement attributable to representation and initialization, rather than infer SASA redundancy from correlation alone. Preregistered local config: config/gmm_ablation.yaml; runtime/memory bound: 600 s / 4 GiB. Interpretation: median/range over seeds, not confidence intervals. Sources: scikit-learn GaussianMixture and adjusted_rand_score official documentation; full protocol in the configuration and module.

Editorial correction: the 7 October entries were initially labelled D17/D18, duplicating existing identifiers. They are now D21/D22; the preregistered content and commit remain unchanged.

## D23 — 2026-11-03: editorial review and shareable repository

User requested external AI checks, academic editing and a downloadable GitHub repository. Record detector results only against their exact input; do not optimize prose to conceal assistance. Tighten the actual scientific argument and retain the disclosure. Create a fresh public history from the audited tracked-file snapshot, excluding supplied raw data, third-party original script, publisher PDFs and private correspondence. Preserve immutable public evidence and its hashes; some historical manifests contain non-secret local runtime paths. The report includes the supplied academic cover details by the user's request. Public repository: https://github.com/Alierkn/robustcluster-abeta. No new scientific experiments are implied by this editorial release.

## D24 — 2026-11-03: textbook-informed editorial refinement

Apply explanatory sequencing from inspected Knuth, Boyd–Vandenberghe and ISLP sections; use Adobe style and preflight guidance as design principles within the existing LaTeX pipeline. Revise the nine chapters and abstract, retaining equations, numerical outputs and assistance disclosure. Apply paragraph-break controls and left-aligned captions centrally. Do not introduce a rigid baseline grid or claim tagged-PDF accessibility. External detectors are checked once per service on a fixed revised excerpt; neither returns Human, and that outcome is preserved. This is an editorial/software-metadata release, not a new biological analysis.

### D25 — Student-confirmed GROMACS learning reflection

On 3 November 2026 the student described learning to use GROMACS as initially difficult but enjoyable. Chapter 8 now conveys that experience in two first-person sentences. This is a personal reflection supplied by the student, not a new computational result or evidence of a completed molecular simulation. No numerical method changed; the fixed detector excerpt is unchanged. The final PDF was rebuilt and the two affected pages visually checked.

### D26 — Undergraduate readability without changing scientific claims

The student requested a more natural explanation after the v0.1.1 detector results. The new edit replaces compressed and administrative phrases with concrete explanations and keeps technical terms where precision requires them. The confirmed GROMACS reflection is unchanged; no further personal history is inferred. This is an editorial revision, not a reproduction or robustness experiment. It follows the existing academic writing guidance and the student's stated level and purpose. Equations, numerical outputs and uncertainty limits remain fixed. The intended effect is easier reading and explanation in an internship context, without a promised detector outcome.

The first two revised abstract paragraphs were fixed before one attempt per external checker. Sapling returned 100.0% AI. GPTZero required registration for further scans; its stale background display is not recorded as a current result. The exact evidence is in `AI_CHECKER_REVIEW_REVISION3.md`. No score-driven rewrite followed those observations.
