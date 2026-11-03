# Reading structure revision: methods and audit

Date: 3 November 2026. Scope: `report/chapters/03_methodology.tex` and `report/chapters/04_audit.tex` in the v0.3.0 worktree. The academic-latex-writer skill guided the prose review. The shared `protocolsteps` environment was agreed with the design agent before editing. No numerical analysis, detector optimization, build or commit was performed by this editorial task.

## Implemented changes

### Chapter 3: a protocol where order matters

The iterative DPC paragraph is now a five-step protocol: generate candidates, apply quality filters, choose a candidate, continue on the remainder, and stop discovery. Definitions of density, separation and density-tie ordering remain in the preceding prose. The protocol replaces the original sequence rather than repeating it.

Preserved details include the initial cutoff of 1.3, candidate counts from 10 down to 2, minimum cluster size 300, silhouette threshold 0.3, preference for the earlier/higher-centre candidate when acceptance counts tie, cutoff factor 0.9, the five-unsuccessful-iterations stop, and residual assignment in STEP 3. The density count still includes the point itself. Local-frame-position ties and the maximum-distance convention for the first point are unchanged.

This is a presentation change: the equations, feature normalization, Wasserstein definition, all-frame assignment, FES interpolation and weighting sections remain unchanged. No implication of completed equilibrium analysis was introduced.

### Chapter 4: compare corrections, explain verification

The four paragraphs describing methodological corrections become one two-column table: supplied-script behaviour and correction/consequence. It makes input parsing, rejected-cluster handling, FES lookup and weighting directly comparable. The random-seed-list limitation remains in prose because changing the random generator also changes the exact legacy subsets. The FES numerical/provenance distinction is stated immediately afterward.

The former verification table repeated the surrounding interpolation and weight examples. It is replaced by two run-in explanations: an interpolation problem with an independently known answer, and a normalized-weight invariant. The row-order, missing/duplicate point, out-of-bounds, energy-shift, unequal-replica-size, relabelling and fitted-scaler checks are all retained. Synthetic end-to-end/GMM/autoregressive fixtures and the archive-provenance test remain explicit software checks. The 36-test release count is unchanged.

The new table is `tab:auditcorrections`. The old `tab:verification` label had no references elsewhere and was removed with its redundant table. Existing chapter and section headings are unchanged.

## Review recommendations for other chapters

These were sent to the coordinator; they are not edits by this task.

- Chapter 1, original lines 17–19: a short numbered set of aims can distinguish the reconstruction, descriptor and feature-removal questions. Retain one closing scope paragraph rather than attaching a disclaimer to each aim.
- Chapter 5, original lines 33–35: show fitting and evaluation as a compact protocol with all constants. Optional future comparisons can be organized by the input each requires; do not blur their unperformed status.
- Chapter 6, original lines 63–67: separate the meanings of cross-feature and within-feature comparisons before the numeric findings; avoid repeating the whole analysis-status table in the closing sentence.
- Chapter 8, original lines 24–26: compare the VMD and GROMACS interfaces in parallel, with one shared paragraph on execution evidence, selections and units. Keep the confirmed personal reflection as continuous prose.

## Source-level checks

Compared with the pre-edit sources, chapter/section headings, citation commands, displayed equations, and figure environments are unchanged. Scientific numerical literals are unchanged; the only additional numeric source token is a table-column width. Braces and environment syntax were checked, and `git diff --check` passed for the two chapters. All FES/weighting blocks remain in force. The Scientific V2 unavailability statement is unchanged. No experience or result was added.

The coordinator must check table fit and page balance in the complete PDF build after the design changes. No claim of rendered-page validation is made here.
