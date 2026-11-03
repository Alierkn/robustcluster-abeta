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
