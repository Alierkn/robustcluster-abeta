# Contributing

Contributions should make a scientific claim easier to check or a computation easier to reproduce. Begin with the [code guide](docs/CODE_GUIDE.md), [method audit](METHOD_AUDIT.md) and [open questions](docs/OPEN_QUESTIONS.md).

## Before making a change

1. Identify whether the change reproduces the published method, corrects an implementation defect, or introduces an extension. Do not silently move an extension into the baseline.
2. State the affected assumption, input and observable behavior. For a scientific change, add a decision-log entry with its source and expected effect.
3. Keep supplied source files, raw inputs and existing run outputs unchanged. Do not edit historical manifests to make a later run appear to have happened earlier.

## Development checks

Follow the environment setup in the README. From the repository root:

```bash
python -m pytest -q
python -m ruff check src tests scripts
```

Add a focused numerical or behavioral test for an algorithmic change. Analytic surfaces, known partitions and explicitly synthetic fixtures are appropriate software tests; never present them as Aβ40 measurements. Documentation-only changes need link and example review rather than a new test that merely mirrors prose.

Use `numpy.random.default_rng` with recorded seeds. Validate inputs before computation; fail clearly on invalid values or missing provenance. Keep scientific settings in configuration files. Expensive experiments need explicit resource budgets and a new run manifest. A successful smoke fixture does not justify an empirical or biological conclusion.

## Proposed changes

A useful pull request describes:

- the concrete problem and resulting behavior;
- whether scientific interpretation changes;
- the evidence or source supporting the choice;
- tests or actual analysis runs performed;
- remaining limitations and any changed input/output contract.

Report numerical bugs with the smallest shareable example, expected result, observed result, environment and run ID. A synthetic reproducer is preferable to uploading restricted simulation data. Do not post credentials, personal correspondence or data without redistribution permission in issues.

## Figures and report

Generate scientific plots from recorded tables through the code. Preserve the producing manifest and output hashes. Captions must distinguish observation, interpretation and conceptual illustration. Rebuild the report after editing LaTeX, then inspect the changed pages for overflow, labeling and readable figure text. Cite verified sources near the claims they support.

AI-assisted editing or coding does not replace verification. Do not optimize prose for detector scores or add invented personal experiences. Record substantive assistance and retain author review of scientific statements.
