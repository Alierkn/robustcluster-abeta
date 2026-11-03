# Editorial and publication-design research — v0.1.1

Research date: 2026-11-03. Scope: English scientific exposition, textbook page composition, and official Adobe publication-design guidance. This is a source-based editorial review, not evidence that Adobe software was used to produce the report. The production system remains LuaLaTeX and Biber.

The purpose is to make the argument easier to follow and the pages easier to read. A polished document cannot establish that missing calculations were completed, or establish human authorship from its appearance. No detector score is an editorial acceptance criterion. The report's existing disclosures of writing assistance and generated illustration provenance should remain.

## Sources and actual inspection scope

The three author-hosted texts below were inspected in the stated sections only. This is not a claim to have read the complete books. Recommendations are original applications to this report; no page design or textbook prose is reproduced.

| Primary source | Material actually inspected | Transferable principle |
|---|---|---|
| Donald E. Knuth, Tracy Larrabee and Paul M. Roberts, *Mathematical Writing* (1989), [author page](https://www-cs-faculty.stanford.edu/~knuth/klr.html), [author TeX manuscript](https://www-cs-faculty.stanford.edu/~knuth/papers/mathwriting.tex.gz) | Section 1, introductory advice and numbered points 1–12 in the manuscript. | Integrate symbols and equations into complete prose; introduce notation when it becomes necessary; make the purpose of the next step apparent. Parallel arguments benefit from parallel sentence structures. |
| Stephen Boyd and Lieven Vandenberghe, *Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares* (2018), [author site](https://web.stanford.edu/~boyd/vmls/), [book PDF](https://web.stanford.edu/~boyd/vmls/vmls.pdf) | Chapter 4 opening and §4.1, printed pp. 69–71 (PDF pp. 79–81); Figure 4.1 and its surrounding explanation. | Establish what the objects and distances represent before introducing an algorithm. The simple example is followed immediately by its limitations: real data may have overlapping groups and an uncertain cluster count. |
| Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani and Jonathan Taylor, *An Introduction to Statistical Learning with Applications in Python* (2023), [author site](https://www.statlearning.com/), [author-hosted download route](https://hastie.su.domains/ISLP/ISLP_website.pdf.download.html) | Chapter 2, §2.2.1, printed pp. 30–31 (PDF pp. 40–41), including Figure 2.10; printed p. 30 also inspected as a rendered page. Additional excerpts around printed pp. 35 and 37 were consulted for context. | Explain what each plotted quantity measures and follow the comparison through to its inferential limit. The page uses a quiet hierarchy and ordinary paragraphs rather than repeated callout boxes. |
| Adobe InDesign, [Create and edit text styles](https://helpx.adobe.com/indesign/desktop/format-and-style-text/text-styles/create-and-edit-text-styles.html) | Official guidance on paragraph and character styles, editing styles, and synchronizing styles across documents. | Centralized semantic styles make consistency maintainable. Change the governing style rather than repairing each instance manually. |
| Adobe InCopy, [Format paragraphs](https://helpx.adobe.com/incopy/desktop/format-text/paragraph-formatting/formatting-paragraphs.html) | “Ways to control paragraph breaks,” Keep Options, and optical margin alignment. This is InCopy guidance, not a claim about an InDesign tool being run. | Keep headings with following text and avoid isolated opening or closing lines. Prefer an editorial or paragraph-level correction over arbitrary blank space. |
| Adobe InDesign, [Use a baseline grid](https://helpx.adobe.com/indesign/desktop/layout-and-grid-tools/grids/use-a-baseline-grid.html) | Grid setup, relation to leading, and document/text-frame grid behavior. | A baseline grid serves alignment across columns and spreads. Its functional purpose matters more than mechanically adopting it in a single-column mathematical report. |
| Adobe InDesign, [Accessible PDFs](https://helpx.adobe.com/indesign/desktop/interactive-elements-and-forms/forms-and-pdfs/accessible-pdfs.html) | Guidance on document structure, reading order, alternative text, metadata, navigation, and tags. | Searchable text and attractive typography are insufficient to establish accessibility. Logical structure and nonvisual access require separate validation. |
| Adobe InDesign, [Configure and use the Preflight panel](https://helpx.adobe.com/indesign/desktop/print/preflight/configure-and-use-the-preflight-panel.html) | Error checking, profiles, and examples including fonts, links, overset text, and image resolution. | Turn repeated production checks into an explicit release procedure. Visual inspection complements automated checks; neither substitutes for the other. |

The Adobe pages were accessed on the research date. The ISLP author download page redirected to an author-linked Google Drive PDF. Local reference copies are research working files, not assets to redistribute in the project archive.

## Application to scientific writing

### Build the explanation around the question

An undergraduate report can be technically mature without adopting an inflated expert persona. For each substantive result, the reader should be able to identify the question, the calculation, the observed quantity, and the conclusion that quantity supports. A paragraph need not announce these categories explicitly.

For example, the useful starting point for the SASA experiment is the observed relation between size and solvent exposure. The subsequent question is whether removing SASA changes assignments under a specified descriptor-space model. Reporting the seed dependence then answers a concrete question; it does not need a generic declaration that “robustness is essential.”

This adapts the explanatory sequencing found in the inspected textbooks. It does **not** import their scientific claims into this project. In particular, ISLP's supervised training/test-error example is not a justification for treating the present all-frame ARI comparison as a held-out predictive evaluation. The report correctly identifies that distinction in Chapter 5.

### Make equations do explanatory work

Use a sentence to identify the role of a formula, define its symbols nearby, and explain the consequential assumption. For the final-bias expression, the important consequence is the redistribution of statistical mass under the stated approximation. For replica normalization, it is the equal contribution of independent replicas. For Kish ESS, it is weight concentration, with dependence addressed separately.

Do not repeat a long caution after every equation. State a limitation where it changes interpretation and preserve a consolidated status table. Equally, do not remove the limits merely to make the prose appear more confident. These recommendations apply Knuth's mathematical exposition advice to the report's actual estimators.

### Keep the student contribution verifiable

The contribution should be described through preserved inputs, executable checks, reproducible tables, and the independent sensitivity experiment. Personal statements of learning should be limited to experience the student can confirm. No stylistic rewrite should invent laboratory participation, Leonardo execution, independent discovery, or an earlier implementation history. The existing distinction between geometric descriptor analysis and equilibrium population inference is a strength to retain.

## Current design versus proposed changes

The repository's current `report/preamble.tex`, chapter sources and existing `report/report.pdf` were inspected. Changes made concurrently by the main editor are marked as requiring final build verification.

| Area | Already present | Recommendation and risk |
|---|---|---|
| Page and type system | A4, 11 pt, restrained margins, Libertinus text/math, single-column body, `microtype`. | Retain. The inspected textbook pages support legibility and hierarchy, not a requirement to imitate their fonts or margins. Do not shrink body text to recover pages. |
| Reusable styles | Centralized heading, caption, code-panel, palette and bibliography settings. | Retain and edit centrally. This already implements the organizational principle behind Adobe paragraph styles. Avoid scattered local font changes and negative spacing. |
| Paragraph breaks | KOMA-Script heading handling; widow/club/display-widow penalties have been added during this revision. | Rebuild and inspect page bottoms and displayed equations. Strong penalties can move material to another page; reduce them if they create excessive blank space. Do not make every paragraph unbreakable. |
| Baseline rhythm | Common body typography and consistent heading/caption spacing. | Keep this flexible arrangement. A rigid baseline grid would complicate equations, tables and floats without the cross-column benefit described by Adobe. |
| Figures and captions | Empirical plots are code-generated; editorial artwork is identified as conceptual; captions use a common style. | Preserve the distinction. Make captions identify the observation, encoding and interpretation boundary. No synthetic molecular drawing should stand in for a missing representative structure. |
| Code presentation | Styled, selectable LaTeX listings complement visual code presentations. | Keep executable source links and readable listings as the primary means of reuse. Screenshots may orient a reader but cannot replace the code or its provenance. |
| Navigation and metadata | Hyperlinks, bookmarks, title/author/subject/keywords and `en-GB` language metadata. | Retain. The inspected existing PDF has `/Lang` but no `/StructTreeRoot` or `/MarkInfo`; it must not be described as a verified tagged or PDF/UA-compliant document. |
| Cover | Project artwork and the supplied institutional logo are already integrated. | Preserve the approved composition. A cover revision is not needed to apply the researched body-text principles. Keep institutional graphics distinct from generated art. |
| Production QA | A working LuaLaTeX/Biber build and report QA infrastructure exist. | Reuse them after edits; check pagination, fonts, citations, overfull boxes, image legibility, cross-references and source links. This is an Adobe-inspired preflight concept, not an Adobe execution claim. |

## Release checks for this editorial revision

1. Check that every revised claim still resolves to its source, test, table or successful manifest. Rewording must not turn a planned stage into a completed experiment.
2. Rebuild using the existing toolchain. Inspect bibliography warnings, missing glyphs, overfull boxes, detached headings, isolated paragraph lines and displaced floats.
3. Inspect a page overview and the actual pages containing equations, dense tables, code panels and the cover. A warning-free compiler log does not guarantee a balanced page.
4. Confirm the main-text page count after typography changes. Recover excess length by removing duplication or improving float placement, not by making the body type smaller.
5. Verify that selectable code and repository links remain available. Keep the disclosure of assisted writing and conceptual generated artwork.
6. Record the accessibility limitation. Tagged-PDF remediation needs a separate reading-order and assistive-technology audit; introducing untested tagging packages at release time is not a low-risk cosmetic change.

These checks improve the report's scientific readability and production reliability. They do not constitute peer review, journal acceptance, or a certification of authorship.

## Reference-copy traceability

The following SHA256 values identify the local texts actually inspected. They identify downloaded research copies, not new project data or redistributable assets.

| Working file | SHA256 |
|---|---|
| `mathwriting.tex` (decompressed author manuscript) | `361bb640be032fc65f0b75cbc1048cf9189c429f1508f2c68221e28ef7ff91fe` |
| `vmls.pdf` | `254738c8763f6c6fc29c0a837884bc58deca7c3e762e5ec79068208ac7214362` |
| `islp.pdf` | `278d3bdd49a8a480c2ff8e03245822caad8a3a48e81afd6d039c52c8fc13ad60` |
