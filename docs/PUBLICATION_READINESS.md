# Scientific scope and publication readiness

Status reviewed: 3 November 2026. This document distinguishes a well-documented research deliverable from a completed journal submission. It is not a claim of peer review, journal acceptance or successful reproduction of the primary study.

## Current contribution

The defensible contribution is an audited, modular analysis implementation together with real descriptor diagnostics and a separate feature-ablation experiment. The work can support an undergraduate internship report and a research-software portfolio because the reader can inspect inputs, decisions, code, tests and numerical outputs.

The descriptor-only GMM pilot asks a bounded question: does removing SASA change the partition, and how does that comparison depend on initialization and component count? Its 50 converged fits are evidence for sensitivity within that experiment. They are not estimates of equilibrium populations, a validation of Gaussian components as molecular states, or proof that three components are biologically optimal.

## Evidence map

| Claim | Supporting material | Limit |
|---|---|---|
| Descriptor inputs can be parsed reproducibly | [Inventory](PROJECT_INVENTORY.md), parsing tests, diagnostic manifest | Input provenance and descriptor definitions still constrain interpretation |
| The recovered FES is numerically complete and covers queried CVs | [FES validation](FES_VALIDATION_2026-10-07.md) | Energy units and generating/replica-combination procedure remain unresolved |
| Features and initialization affect the GMM partition | [Pilot protocol and saved results](GMM_ABLATION_PILOT.md) | Fixed fit subset, five seeds per condition, biased descriptors, no independent validation |
| Core implementation behaves as intended on specified cases | [Tests](../tests), [QA record](FINAL_QA.md) | Tests cannot establish validity of the physical model or published-workflow reproduction |
| Report figures and tables can be traced to outputs | [Release manifest](../release_manifest.json), [reproduction instructions](../REPRODUCIBILITY.md) | Regenerating a report from saved outputs is distinct from rerunning the science |

## What a journal-oriented study still needs

1. **A focused research question.** Choose whether the manuscript concerns an audited reproduction, descriptor sensitivity, or research software. The internship report's broad teaching structure is not itself a journal article structure.
2. **Resolved physical provenance.** Obtain the FES energy units, construction and replica-combination procedure; establish `metad.rbias` units before a time-dependent reweighting comparison. Document rather than infer missing simulation parameters.
3. **Completed baseline and suitable comparisons.** Execute the published-workflow implementation after the evidence gates are met, inspect failure cases and compare methods on identical frame identities. Clarify STEP-2 scaling with the paper/source authors if possible.
4. **A stronger uncertainty design.** Test independent fitting subsets and temporal block choices. Keep uncertainty in the fitted partition, weighting and FES construction separate. Five seeds on one fixed fitting subset do not quantify all sources of variation.
5. **Appropriate biological support.** Atomic representatives or independent experimental comparisons require compatible structural data, definitions and licenses. Do not infer molecular contacts or aggregation mechanisms from scalar descriptors alone.
6. **Authorship, access and venue decisions.** Confirm contributions with internship contacts, choose a suitable venue, check its actual policies and arrange lawful data access. No journal, author list, endorsement or data license is assumed here.

These are scientific requirements, not presentation defects that typography or fluent wording can resolve. The report may be submitted as an honest account of the work completed while these questions remain open.

## Editorial standard

A statement should tell the reader what was measured, what comparison was made and what the result supports. Methods should name the transformations and numerical choices needed to reproduce them. Discussion should distinguish an observed pattern from its possible explanation.

The report uses numbered cross-references, consistent mathematical notation, units, restrained tables and traceable scientific plots. Qualitative editorial illustrations are labeled separately from numerical results. The university seal indicates the report's institutional context, not institutional approval of a scientific claim.

AI-detector percentages are not a measure of scientific quality or proof of authorship. Any external detector result must be tied to the exact text version, service and date tested. Editing should improve argument, precision and the student's accountable understanding; it should not introduce errors or invented experience to manipulate a detector.

## Reading order for a reviewer

Read the report's results and discussion, then the [method map](PAPER_METHOD_MAP.md), [GMM pilot](GMM_ABLATION_PILOT.md), [code guide](CODE_GUIDE.md) and [open questions](OPEN_QUESTIONS.md). Use the selected manifests to check individual observations. This makes both the contribution and its limits reviewable without treating software tests as biological validation.
