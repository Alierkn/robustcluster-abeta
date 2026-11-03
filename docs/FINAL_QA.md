# Current release v0.2.0 — complete report reconstruction

Selected report: `20261103T140226-report-575524` — **SUCCESS, 18 main-text pages / 35 total**. Selected local release QA: `20261103T140300-qa-9861c8` — **SUCCESS, 36 tests**, lint, bibliography and output integrity. Report SHA256: `e24d2415a840d0e44fc3589ac1fbfe9e502a364bda422773cea9ae2aa1efc34b`.

The abstract and all nine chapters were written afresh. Learning evidence now reflects the student's confirmed GROMACS/VMD/Python use and personally created MCP projects. Three new vector panels replot existing numerical tables; there were no new empirical fits or biological claims. Original script/data/FES hashes match, and the selected build's source hashes match the delivered files. The unchanged bibliography contains 34 verified entries; 32 are cited.

All 35 pages were visually reviewed as overviews; PDF pages 18, 19 and 21 were also inspected at reading size. Fonts are embedded and Unicode-mapped; Poppler rendering reports no warnings. Internal PDF destinations resolve. No missing characters, unresolved citations, duplicate labels or overfull/underfull boxes remain. The two existing benign unicode-math warnings and the untagged-PDF accessibility limit remain documented. Earlier plot files with an embedding warning were rejected for publication and superseded, not silently altered.

Details: `rebuild/REBUILD_RECORD.md`; machine-readable review and page overviews: `results/editorial_review/rebuild/`. Full equilibrium reproduction is still blocked by FES units/construction provenance. No new AI-detector check was performed; the historical scores below do not apply to this rewritten report.

---

# Previous release v0.1.2 — undergraduate readability

Selected report build: `20261103T131528-report-67e955` — SUCCESS, **22 main-text pages, 38 total**. Selected local release QA: `20261103T131615-qa-72d4c6` — SUCCESS, **36 tests**, lint, bibliography and saved-output integrity.

The abstract and all nine chapters received a prose review for clear undergraduate-level explanation. A source comparison against `6d1fc92` confirms unchanged chapter equations, numerical literals, citation sequence, headings, labels, and complete figure/table environments. Manual review checked the meaning of the rewritten explanations, including FES marginalization and the separate meanings of cluster width and replica SEM. The confirmed GROMACS reflection and the assistance disclosure are unchanged. No numerical algorithm, configuration, empirical output or original supplied file was edited.

All 38 pages were viewed in contact sheets. The abstract, dense methods, GMM method, discussion and internship/code pages (PDF pages 2, 12, 17, 24 and 25) were inspected at reading size. No clipping, collisions or missing assets were observed. Fonts are embedded and Unicode-mapped. The build has no unresolved citations or labels, missing glyphs, or overfull/underfull boxes. Two existing benign unicode-math compatibility warnings remain. The PDF remains untagged; no PDF/UA claim is made.

The fixed 135-word abstract excerpt received **Sapling 100.0% AI**. **GPTZero is BLOCKED** by its free-scan/sign-up gate, with no verified score for the current excerpt. The stale background display is explicitly excluded from the result. These are not full-report authorship findings. Evidence is in `AI_CHECKER_REVIEW_REVISION3.md`; the excerpt was not rewritten after the scores were observed.

Detailed wording examples: `PROSE_READABILITY_V012.md`, `PROSE_READABILITY_V012_A.md`, and `PROSE_READABILITY_V012_B.md`. Machine-readable source and PDF checks are under `results/editorial_review/revision3/`. The preceding v0.1.1 delivery and its checker records remain preserved. Older audits below describe their own selected builds.

---

# Previous release v0.1.1 — textbook-informed refinement

Selected report: `20261103T130123-report-145074` — SUCCESS, 22 main-text / 38 total pages. Selected local QA: `20261103T130142-qa-4635a6` — SUCCESS, 36 tests, lint, bibliography and output hashes. Numerical algorithms and saved scientific outputs are unchanged; version metadata is incremented to 0.1.1.

All pages were inspected as overviews; dense methods, discussion and figure pages were checked at reading size. Captions share left alignment; paragraph opening/closing lines are kept with adjacent text. A visually dense methods page prompted a coordinate check: its body-to-footer gap is 32.24 pt, the minimum across checked pages, so no extra manual page break was introduced. No overfull/underfull boxes, missing glyphs, duplicate labels or unresolved citations remain. The two existing benign math-package warnings persist.

The PDF remains untagged; language metadata, bookmarks and searchable text do not establish PDF/UA compliance. Adobe guidance informed reusable styles and preflight, not an Adobe application execution. Detailed primary-source inspection is in `EDITORIAL_DESIGN_RESEARCH_V011.md`.

The revised fixed excerpt received Sapling 99.9% AI and GPTZero 100% AI; neither returned Human. These are not full-report or authorship results. Exact records are in `AI_CHECKER_REVIEW_REVISION2.md`. No prose was changed in response to those scores. The student subsequently confirmed that learning to use GROMACS was initially challenging but enjoyable. Two first-person sentences now convey that experience in Chapter 8. No specific simulation or technical achievement was inferred. The fixed abstract excerpt is unchanged.

After the student-confirmed addition, the report was rebuilt and release QA repeated. Extracted text changed only on PDF pages 25–26; both were inspected at reading size and retain clear margins and an intact code panel. Pagination is unchanged.

The previous release and the October delivery remain preserved. Earlier QA records below retain their historical scope.

---

# Current editorial release — 3 November 2026

- Selected report build: `20261103T122345-report-96156c` — SUCCESS, 22 main-text pages, 38 total.
- Selected local release QA: `20261103T122434-qa-4193d6` — SUCCESS, 36 tests, lint, bibliography and saved-output integrity.
- All 38 pages reviewed as contact sheets; revised abstract and reproducibility appendix inspected at reading size. Fonts are embedded and Unicode mapped. No unresolved citations, duplicate labels, missing characters or overfull/underfull boxes remain. Two benign unicode-math/mathtools compatibility warnings remain documented.
- An earlier integration build produced a 3.29 pt overfull GitHub link in Appendix E. QA rejected it (`20261103T122301-qa-cd6038`); a shorter descriptive hyperlink fixed the issue. Failed evidence is retained.
- Existing scientific outputs and cover composition are unchanged. The abstract uses recorded values; all nine chapters received targeted editorial corrections. New code and LaTeX availability links are in Appendix E.
- External detector review covers only its saved pre-revision 154-word excerpt, not this revised report; see `AI_CHECKER_REVIEW.md`. The revised discussion received two deterministic Academic Writing Toolkit checks with no reported issues.
- Source/publication boundary is documented in `PUBLIC_RELEASE.md`. The old 7 October delivery was preserved outside the repository before updating the convenience files.

The following section is the earlier October audit record, retained as history. Its archive rebuild and hashes apply to that release, not a new November clean-environment installation.

---

# Final delivery audit — 7 October 2026

**Final report: 22 main-text pages, 38 total pages.** The additional appendix page records the completed GMM experiment settings separately from the implemented reproduction parameters. Cover: the supplied Messina seal remains at the physical page center, 42 mm wide, with a restrained shadow.

## Selected evidence

| Check | Evidence | Result |
|---|---|---|
| LuaLaTeX/Biber build | `20261007T123134-report-9de5e7` | Successful; main-text target met |
| Release tests / lint / hashes / bibliography | `20261007T123503-qa-9b5c8c` | 36 tests passed; Ruff passed; 34 registered verified references, all cited |
| Source integrity, saved GMM summaries, PDF links/fonts | `20261007T121345-final-audit-3a53e7` | Successful |
| Original data and script | SHA256 comparison against Downloads originals | Exact matches for descriptor input, original script and complete FES |
| Numerical result consistency | GMM model and comparison tables vs summary | 50 converged fits; every ARI median and range agrees |
| PDF navigation | Internal destinations / URI structure | No unresolved internal destination; external URL syntax checked |
| Typography | `pdffonts` and final LaTeX log | Fonts embedded and Unicode-mapped; no missing characters or overfull/underfull boxes |

## Editorial corrections

- Removed redundant punctuation after figure/table numbers and standardized PDF metadata to the actual title, author, academic year and English language.
- Clarified the distinction between FES grid validation and unverified energy/construction provenance; described block bootstrap as an uncertainty extension.
- Separated the GMM parameter table from the unexecuted reproduction settings and checked its seeds, sample sizes and numerical thresholds against the successful manifest.
- Corrected repeated table-label handling and strengthened the build gate to reject multiply-defined labels.
- Retained the user's accepted cover placement, supplied logo, generated illustrations, corrected workflow arrows and searchable code panels.

All pages were visually reviewed as contact sheets; final parameter pages and the cover/workflow/code regions were inspected at larger scale during revision. No clipping, collision or missing graphics was observed. Short chapter-ending pages retain intentional whitespace. The prose was reviewed for consistency between observation, interpretation and future work; no new biological conclusions were added.

Two recorded unicode-math/mathtools compatibility warnings remain, concerning bracket and colon command definitions. They do not affect the equations used here. The final build has no unresolved citations, undefined or duplicate references, missing characters, or overfull/underfull box warnings. Earlier build logs, including an intermediate duplicate-label warning, are retained as historical evidence and are superseded by the selected build.

## Scientific and release boundary

This is a completed report and research-software delivery with completed descriptor diagnostics, FES structural validation and an independent GMM extension. Full final-bias paper reproduction remains **BLOCKED** by unresolved FES units and construction provenance. Paper-DPC robustness, time-dependent reweighting, molecular representatives, Aβ42, external-ensemble comparisons and Leonardo execution are not claimed as completed.

The 34-reference verification register was reconciled with the unchanged bibliography; this audit did not repeat live publisher verification. URLs were checked for PDF integrity, not live remote availability. The report can be compiled from the preserved assets without access to raw simulation inputs. Scientific reruns require the separately obtained, hash-matched raw data. Raw materials and executable runtimes are excluded from the source archive. The source archive includes historical manifests and build evidence; the final release manifest selects the current PDF and QA records.

## Extracted-source build verification

A source archive was extracted into a fresh directory without `.git` or raw inputs. The report rebuilt with the existing isolated Python and TeX runtimes; all 38 extracted page texts match the delivered report. The extracted-source release check also passed all 36 tests, lint and integrity checks. Evidence: `20261007T124239-archive-review-e6ff4f`. This checks source portability within the verified environment, not installation of dependencies on another machine.

The first verification harness incorrectly followed the virtualenv executable symlink into the incompatible global Python environment. Its failed import logs were retained. Repeating the check with the actual virtualenv executable succeeded. Missing Git metadata is now recorded as null instead of aborting a report build or inheriting an unrelated parent repository's commit; a regression test covers that case.
