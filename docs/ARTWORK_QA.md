# Editorial artwork revision — 7 October 2026

The user's supplied editorial illustration inspired tactile print grain, ice-blue paper, navy/teal ink and muted coral accents. Three original assets were generated with the built-in image-generation tool: a complete typeset cover, a conformational-diversity illustration and a qualitative bias-landscape illustration. No diagram code was used to create these artworks. The exact model version was not exposed by the tool, so Image 2.5 execution cannot be verified or claimed.

## Assets and placement

- `report/artwork/cover-editorial-v2.png`: full-page cover, including image-generated typography; standalone first-page PDF alongside it.
- `report/artwork/ensemble-editorial-v2.png`: conceptual flexible-ribbon ensemble.
- `report/artwork/bias-editorial-v2.png`: conceptual accumulating-bias landscape.
- The two interior artworks appear together in the theoretical-background chapter. Captions explicitly identify them as qualitative illustrations, not atomic structures or computed FES data.
- Three searchable source panels use syntax highlighting, line numbers, consistent headings and quiet backgrounds. Companion-code excerpts were extracted from the same immutable GitHub commits as the original screenshots; exact source ranges and hashes are recorded. Only display indentation is suppressed for GROMACS.

## Verification

Final build: `20261007T114536-report-b47c7e`. Release QA: `20261007T114549-qa-6481bb`. The report remains 22 main-text pages / 37 total. 35 tests and Ruff passed. No overfull boxes, unresolved references or missing-character warnings. Existing unicode-math and underfull warnings remain recorded.

Cover, interior-artwork and code-panel pages were rendered and visually inspected. Names, academic year, framing, source line numbers and absence of clipping were checked. The artwork is raster; searchable typeset scientific text, equations, code panels and numerical plots remain separate. Cover text is embedded in the image. Generated image bytes are preserved unchanged, and the build checks their hashes. Scientific analyses were not rerun or altered for this visual revision.

Exact generation prompts: `docs/ARTWORK_PROMPTS.json`. Asset/source provenance: `report/artwork_provenance.json`. Earlier vector cover and design preview are retained as historical artifacts, but are no longer the final cover. The preceding source archive was preserved in the sibling `release-2026-10-07-before-artwork` directory.

## Supplied Messina logo

The student subsequently supplied the institutional logo. Its PNG bytes are preserved as `report/artwork/messina-logo-user-supplied.png`, with SHA256 recorded in artwork provenance. The cover places it at 24 mm without generative reconstruction; circular document clipping hides only the white outer corners. This institutional mark is not covered by the new-code BSD license. The cover with logo is exported separately as `cover-editorial-v3-logo.pdf`; the earlier cover is retained.

The subsequent cover annotation requested a centered logo with a subtle shadow. The final placement is 12 mm wide, centered in the gap between the institutional heading and report category. Original proportions and PNG bytes are unchanged. A rendered-page review confirmed no text overlap. `cover-editorial-v4-centered-logo.pdf` is the current standalone cover; earlier versions are preserved.

The student clarified that center means the physical page center, not the header. The current cover places the unchanged seal at A4 coordinates (105 mm, 148.5 mm), diameter 42 mm, retaining the subtle shadow. It lies over the central artwork and does not cover title or author text. `cover-editorial-v5-page-center-logo.pdf` supersedes the header-centered cover.
