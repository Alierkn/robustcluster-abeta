# Publication-informed reading structures — v0.3.0

Research and implementation date: 2026-11-03. This revision studies actual open scientific-publication PDFs, in addition to the earlier textbook and Adobe documentation research. It applies their useful reading structures to a curricular internship report; it does not reproduce journal branding or claim journal acceptance. Scientific meaning, evidence gates and the approved cover remain independent of visual design.

## Primary publications actually inspected

The PDFs were retrieved from their publishers, rendered locally, and the pages below were visually inspected at readable resolution. Only the listed pages and nearby passages were examined for this design review; this is not a claim that the student read each complete publication. Publisher-page text alone was not used as evidence of a visual inspection.

| Publication and primary PDF | Exact inspection scope | Page observations and transfer |
|---|---|---|
| Pedregosa et al., *Scikit-learn: Machine Learning in Python*, JMLR 12, 2825–2830 (2011). [Publisher article](https://www.jmlr.org/papers/v12/pedregosa11a.html); [publisher PDF](https://www.jmlr.org/papers/volume12/pedregosa11a/pedregosa11a.pdf). | PDF pp. 3–4, printed pp. 2827–2828: project vision, underlying technologies, code design, Table 1 and discussion of performance. | The single-column text uses concise topic leads within paragraphs. A full-width numerical table has horizontal rules, a compact note and a nearby caption; surrounding prose explains the comparison. Transfer: keep sustained explanation in prose and use a real comparison table when entries share the same questions. Avoid turning every implementation detail into a large box. |
| Grossfield et al., *Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations* [Article v1.0], Living J. Comp. Mol. Sci. 1(1), 5067 (2019). [Publisher PDF](https://livecomsjournal.org/index.php/livecoms/article/download/v1i1e5067/913/2595); [DOI](https://doi.org/10.33011/livecoms.1.1.5067). | PDF/printed pp. 6–7: full-width best-practices checklist, followed by a two-column page containing Figure 1, its caption and Section 4. | The checklist page separates actionable checks from explanatory discussion. The next page pairs a small scientific figure with a detailed caption and ordinary prose. A strong heading introduces a new question without changing the whole document's type system. Transfer: a short numbered protocol for sequential decisions, and a small number of paired explanations where direct comparison helps. Retain full-width equations and prose elsewhere. |
| Sandve et al., *Ten Simple Rules for Reproducible Computational Research*, PLOS Computational Biology 9(10), e1003285 (2013), an editorial. [Publisher article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285); [publisher PDF](https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1003285&type=printable). | PDF/printed p. 2, covering Rules 1–6 and their explanatory text; adjacent publisher information verified the article identity. | The page uses three narrow columns, bold sans-serif action headings and serif prose. Headings allow scanning while paragraphs provide the reasoning. Transfer: stronger section hierarchy and action-led protocol steps. The three-column page itself is too narrow for this report's long expressions, source paths and tables, so it is not copied. |

These are three different scientific-publication forms: a research-software paper, a methods/best-practices guide and an editorial. They are not presented as three empirical Aβ studies or as new scientific support for the project's results. Their value here is the observed relationship between content and layout.

## A coherent mixed layout

Variety should follow the reader's task. A formula needs connected explanation; a sequential method benefits from numbered steps; parallel checks benefit from a table; two closely related interpretations may benefit from short side-by-side panels. Changing columns at arbitrary intervals would create decoration without improving the argument.

| Report location | Recommended structure | Why it belongs there |
|---|---|---|
| Introduction | Brief prose followed by a short, explicit list of aims | Readers can locate the project questions before meeting the detailed methods. The list replaces a dense enumeration; it should not repeat the following paragraphs. |
| Scientific background and discussion | Normal single-column prose with full-width equations | Definitions, assumptions and conclusions need a continuous reading order. The conceptual illustration pair retains its explicit generated-art status. |
| DPC method | `protocolsteps` for the ordered candidate/accept/remove/reduce/stop operations | Numbering exposes the sequence and makes thresholds easy to find. Definitions and tie rules remain in prose before the list. |
| Scientific audit | `booktabs`/`tabularx` comparisons of original behaviour versus correction, and test intervention versus expected invariant | Each row answers the same questions. Explain the important consequence after the table rather than repeating every cell as prose. |
| GMM design | A short protocol or compact design table, followed by evaluation scope | Fixed sample, shared scaling, component counts and seeds form a real procedure. Keep the distinction between convergence and agreement visible. |
| Results | Vector figure groups with nearby captions; at most one short pair of interpretation panels | A pair may distinguish feature removal from seed changes, or observation from its justified implication. It must not separate a figure from the paragraph that introduces it. |
| Internship/software account | A short comparison of VMD MCP and GROMACS MCP, plus one readable source excerpt | Direct comparison is useful because the tools have different roles. Confirmed learning remains prose; source code does not imply an executed simulation. |

The manuscript should not become a sequence of cards. Tables, steps and paired panels replace suitable text structures; they do not add another layer of summaries around unchanged prose. A comparison panel is limited to roughly 60–80 words per side, avoiding long displayed equations or deeply nested lists. Use at most a few panel pairs across the main text.

## Implemented preamble changes

The design subtask supplied the preamble; the coordinating editor integrated the chapter structures and refined pagination. The final hierarchy below reflects that integrated review.

- Retained A4, one-sided `scrreprt` at 11 pt and Libertinus Serif/Sans/Math. The current 29/26/25/25 mm left/right/top/bottom margins are unchanged.
- Added a modest `\linespread{1.04}`. With the 11 pt KOMA-Script base this gives approximately 14.1 pt body leading. The final build should confirm reading comfort and pagination; line spacing is not a way to disguise missing content.
- Strengthened chapter titles to 22/26 pt serif and section titles to 12.2/15 pt sans. Chapter numbers are teal, and each chapter opening receives a short fine teal rule. The navy/teal/ink/grey/audit palette is unchanged.
- Kept left-aligned small captions, with navy bold labels and ink caption text. Increased the consistent figure/caption gap to 7 pt.
- Added a page-breakable `protocolsteps` list with teal numerical labels, unchanged body size and restrained spacing. No tinted container is required.
- Added `comparisonpanel{Heading}`, a top-aligned minipage with a small heading and fine rule. It occupies 48% of the current line width, leaving a clear gutter for a pair. It has no background or border frame.
- Preserved existing code-listing styles, mathematics, bibliography setup, metadata and header/footer content. The cover lives in `report.tex`, which this subtask did not edit: the supplied 42 mm logo remains at the physical page centre.

### Interfaces for chapter integration

Sequential methods use an ordinary no-argument environment:

```latex
\begin{protocolsteps}
  \item \textbf{Define the candidate.} State the operation and its parameters.
  \item \textbf{Apply the criterion.} State the decision and its consequence.
\end{protocolsteps}
```

Short parallel explanations use two top-aligned panels:

```latex
\par\addvspace{8pt}\noindent
\begin{comparisonpanel}{First question}
A short explanation tied to the actual evidence.
\end{comparisonpanel}\hfill
\begin{comparisonpanel}{Second question}
A comparable explanation with the same level of detail.
\end{comparisonpanel}
\par\addvspace{8pt}
```

Panels are minipages and cannot split across a page. If they become long, restore normal prose or use a table. Native `tabularx` with `booktabs` remains the preferred table interface; do not add vertical rules, coloured row bands or small type merely to squeeze in more text.

## Coordination and acceptance checks

The methods editor is integrating protocol steps into Chapter 3 and comparison tables into Chapter 4. The coordinating editor decides whether aims, GMM design, results and companion-project sections benefit from the remaining structures. The design environment itself carries no analytical status and does not alter data, figures, model parameters or scientific claims.

Before accepting the new PDF:

1. Confirm that lists and tables preserve their original operations, thresholds, qualifications and citation coverage.
2. Inspect chapter openings, long headings, panel pairs, table notes and the figure/caption relationship at actual reading size. Check that structured material does not strand a heading or interrupt a short paragraph.
3. Check compiler warnings, references, fonts and the main-text page target. Retain 11 pt body text; resolve awkward pages by placement and editing rather than shrinking the whole report.
4. Confirm that conceptual/generated artwork, empirical plots and genuine code screenshots still have distinct provenance. No new illustration was generated in this design subtask.
5. Record any external AI-checker result against the exact revised text submitted. Layout changes do not establish human authorship or predict a detector score. The design was not optimized against a detector result.

No Adobe application was used in this subtask. No full report build, test-suite run or commit was performed before source coordination; `git diff --check` passed for the preamble. These are implemented design primitives awaiting integrated PDF inspection, not a claim that every proposed arrangement has passed visual QA.

## Inspected-reference traceability

Reference PDFs and rendered inspection pages are kept in the local research working directory `work/design-references-v030`, outside the source repository. They are not packaged as project assets. SHA256 values identify the copies visually inspected:

| Local reference | SHA256 |
|---|---|
| `jmlr.pdf` | `1c338a6b3c6c1dcafda3990a8098b8b50dd6c77616361396fb75f6822c6e0778` |
| `livecoms.pdf` | `9e11c8c6908411ef7d67c9f93e4a7eab7de26c660400283c8a148fd2f75c61a9` |
| `plos.pdf` | `35648a3880bdd8bf30e8212a3847b7bd35f504ee5ccbd1ad3856d206acd181db` |

## Integrated pagination refinement

The final chapter size is 22/26 pt, with ragged-right titles and no word hyphenation. Audit-table columns are ragged right; references and the long parameter table use conventional small type while the main body remains 11 pt. Float barriers keep the earlier diagnostic figure from interrupting the next scientific question. A concise introduction and discussion remove stranded paragraphs without deleting a result or assumption. These adjustments followed inspection of the integrated PDF, not a detector score.
