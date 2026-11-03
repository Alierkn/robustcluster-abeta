# Academic presentation decisions — 3 November 2026

The report remains a curricular internship report, not a facsimile of a journal article. The publication-inspired choices below support reading and inspection; no journal acceptance, endorsement or author experience is implied. Existing cover artwork and the centred 42 mm supplied seal are retained.

## Sources actually inspected

| Source | Inspected material | Decision used here |
|---|---|---|
| Knuth, Larrabee and Roberts, *Mathematical Writing* | Author-hosted TeX manuscript, Section 1, points 1–12; author bibliographic page | Introduce symbols in prose, connect equations through explanation, avoid empty transitions, and give a reason for the next step. No wording copied. |
| Boyd and Vandenberghe, *Introduction to Applied Linear Algebra* | Author-hosted PDF, printed pp.69–71 (PDF pp.79–81), including visual inspection of pp.69–70 | Use a single readable column, a clear heading hierarchy, a nearby caption and a concrete interpretation of clustering. Retain the distinction between an illustrative grouping and a justified scientific state count. |
| Simon Fear, *Publication quality tables in LaTeX* | booktabs manual, Sections 1–2, pp.1–3 | Preserve horizontal rules with hierarchy, units in headers and no vertical rules. |

Primary links: [Mathematical Writing](https://www-cs-faculty.stanford.edu/~knuth/klr.html), [VMLS author site](https://web.stanford.edu/~boyd/vmls/), [booktabs manual](https://tug.ctan.org/macros/latex/contrib/booktabs/booktabs.pdf).

Only these sections were consulted; the project does not claim that the student read the complete books. These are editorial design references, not new sources for the biological results; they are therefore recorded here rather than added to the scientific bibliography. Downloaded reference books are not redistributed in the repository.

## LaTeX choices

The existing KOMA-Script `scrreprt`, A4, 11 pt, Libertinus Serif/Sans/Math and restrained navy/teal palette already support this approach. Preserve those choices instead of importing journal branding. Body text remains selectable; mathematical expressions and code panels remain searchable; scientific plots retain their vector sources. The generated cover is explicitly labelled as artwork in the provenance notes and is not an empirical molecular structure.

This revision adds live source-code and LaTeX links to the reproducibility appendix and sharpens chapter prose. It preserves all numerical outputs, equations and the separate evidence categories. Source-code screenshots are accompanied by searchable snippets and links to the inspected commits. The actual current repository is linked separately from those historical companion projects.

## Review boundaries

External AI-detector classifications concern only the exact submitted abstract excerpt. They are not a scientific quality gate. Academic Writing Toolkit reviewed the revised Chapter 7 LaTeX source for paragraph logic and conservative British-English spelling; it reported zero issues for each. This deterministic check is neither peer review nor a full-report review. Its exact input and outputs are saved in `results/editorial_review/academic_toolkit_discussion.json`.
