# Complete report rebuild — v0.2.0

The abstract and nine chapters were written afresh around the internship's actual learning sequence, the supplied Aβ40 materials and the completed descriptor investigation. The previous v0.1.2 report remains preserved in Git and the earlier release. This is an editorial and research-software presentation release; no new simulation or fitted model was produced.

## Completed stages

| Stage | Work completed | Evidence |
|---|---|---|
| Learning map | Separate programme context, confirmed GROMACS/VMD/Python use, personal MCP projects and logged results | `LEARNING_EVIDENCE_MAP.md` |
| Scientific story | Introduce the problem, explain theory/methods, audit inherited choices, present the completed GMM question, discuss limitations and learning | Nine chapter sources under `report/chapters/` |
| Visual design | 11 pt Libertinus text/math; serif chapter headings, sans section headings; 29/26/25/25 mm margins; approved cover and centred 42 mm seal | `report/preamble.tex`, `report/report.tex` |
| Empirical figures | Replot correlation/PCA, ACF and GMM comparisons from verified saved tables, with larger labels and explicit range semantics | Figure run `20261103T135347-e4275730` |
| Code and tables | Searchable real code panel, genuine companion-source screenshots, explicit numerical test examples and detailed correlation table | Chapters 4/8 and Appendices C/G |
| Build | LuaLaTeX/Biber; **18 main-text pages, 35 total** | `20261103T140226-report-575524` |
| Software QA | **36 tests passed**; Ruff passed; output hashes and bibliography reconciled | `20261103T140300-qa-9861c8` |
| PDF/source review | All page overviews; result/learning pages at reading size; font/link/source checks; independent scientific review | `results/editorial_review/rebuild/review.json` |

The report cites 32 entries from the unchanged 34-entry verified bibliography. Two unused entries remain in the source register; no irrelevant citations were added to preserve a historical count. No unresolved citations, internal destinations, missing glyphs, overfull or underfull boxes were found. The two previously documented unicode-math compatibility warnings remain. The PDF has embedded Unicode-mapped fonts and bookmarks, but remains untagged; no PDF/UA claim is made.

## Scientific and learning review

The numerical statements were compared with the saved diagnostics/GMM tables and macros. The review retained the separate meanings of biased trajectory time, approximate correlation ESS, initialization ranges, raw component fractions and equilibrium population estimates. The added interpolation/weighting examples describe existing tests, not new molecular data.

The student confirms using GROMACS, VMD and Python and creating VMD MCP/GROMACS MCP as personal projects. Their GROMACS reflection is retained without inventing commands, tutorials or production trajectories. The projects are described through inspected source functions and commit-specific links, separately from the descriptor experiment. Existing assistance and generated-art disclosures remain.

The original downloaded script, descriptor table and complete FES were rehashed; all match the preserved recorded values. Numerical implementation/configuration/test files are unchanged except for package version metadata. The bibliography source, institutional logo and artwork are also unchanged. Full equilibrium reproduction remains **BLOCKED** by unresolved FES energy units and construction provenance. No Aβ42, structural-trajectory, Leonardo, or new detector result is claimed.

## Figure preflight correction

The first new plotting run, `20261103T134659-ba59eb37`, produced the intended numerical panels but Poppler reported a font-type/embedded-font mismatch for its OpenType plot fonts. Its files and manifest are retained as development evidence, and are not selected for publication. The replacement run uses embedded DejaVu Serif TrueType plot labels; Poppler font inspection and rendering complete without warnings. Document text and mathematics remain Libertinus.

This decision follows the actual preflight finding and Matplotlib's documented font-format considerations: [official font documentation](https://matplotlib.org/stable/users/explain/text/fonts.html). The source-based textbook/Adobe principles were already researched in `../EDITORIAL_DESIGN_RESEARCH_V011.md`; no Adobe application execution or complete reading of those textbooks is claimed.

## Reuse and interpretation

The final source is `report/`; the isolated `report-next/` draft is excluded from distribution. `report/rebuild_provenance.json` links selected source manifests and imported assets. The new plotting script creates an immutable run and does not overwrite the selected report assets. Compilation from included assets requires no raw simulation inputs.

Historical detector reviews apply only to their stored excerpts. The rebuilt text was not submitted to a detector, and no authorship certification or journal acceptance is implied. The intended standard is a scientifically defensible, readable undergraduate internship report with inspectable code and evidence.
