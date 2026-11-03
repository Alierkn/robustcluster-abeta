# Prose revision for v0.1.1

Date: 3 November 2026. Scope: the nine scientific and internship chapters. This revision improves the argument and explanatory flow. It does not target a detector score, conceal assistance, create personal experiences, or change numerical results. The report's AI-assistance statement lies in the appendix and was not edited in this subtask.

## Reading used

The editor consulted the author-hosted TeX source of Knuth, Larrabee and Roberts, *Mathematical Writing*, Section 1 (particularly points 7–12), and the author-hosted PDF of Boyd and Vandenberghe, *Introduction to Applied Linear Algebra*, Chapter 4, printed pages 69–70 (PDF pages 79–80). Copies were already available in the local editorial-reference workspace from the earlier documented inspection.

The useful lesson from Knuth is to connect definitions and operations through prose that anticipates what a reader needs next. Boyd and Vandenberghe's clustering introduction moves from the object being grouped to the meaning of proximity and then to the limits of a simple example. Here those principles support explanations of descriptor geometry, common frame identities and model-dependent assignments. No textbook sentences or illustrations were copied. This editorial reading is not attributed to the student's internship experience.

Primary sources: [Mathematical Writing](https://www-cs-faculty.stanford.edu/~knuth/klr.html), [VMLS author site](https://web.stanford.edu/~boyd/vmls/).

## Material changes

| Location | Revision | Scientific implication |
|---|---|---|
| Introduction | Organize the opening around grouping molecular configurations; connect the audit to the Rg–SASA ablation question | The actual experiment remains the focus; no new biological objective |
| Background | Explain what an ensemble retains and what global descriptors discard; link denser frame saving to the independence question | Clarifies existing theory without claiming new estimates |
| Methods: identities and scaling | Explain the false comparisons caused by shuffled rows and independently scaled groups | Makes reproducibility choices part of the scientific reasoning |
| Methods: density peaks | Introduce the density ordering before separation and center ranking | Preserves the documented deterministic tie convention |
| Methods: weighted summaries | Distinguish within-family heterogeneity, replica variation and conditional block-resampling intervals through their estimands | Preserves the exact weighting and uncertainty definitions |
| Audit: residual frames | Explain why a rejected local group must not influence discovery but still receives a final label | Clarifies the same correction; original source remains unchanged |
| Robustness | Explain why the fixed sample and paired feature spaces isolate representation/initialization, while BIC and sampling limits remain separate | No claim of held-out validation or sample-selection uncertainty |
| Results | Lead with observations and point to the existing status table, removing redundant execution-history language | All values, ranges, tables and scientific figures are unchanged |
| Discussion | Separate fit adequacy, partition reproducibility, sampling dependence and physical interpretation | Keeps the limits of the GMM pilot explicit without repeating every status warning |
| Internship outcomes | Replace third-person administrative phrases with inspectable examples of scaling, testing and molecular-software interfaces | No invented attendance, personal reaction, learning completion or simulation execution |
| Conclusion | State the conditional SASA-removal result and the concrete provenance needed for the next calculation | Full equilibrium reproduction remains incomplete |

Fifty-four paragraphs were revised. For example, the previous scaling discussion stated that pooling defines a common metric; the revision explains what would happen to the same observation under independent group scaling. The residual-cluster discussion now follows the observation from rejection in local discovery to reassignment in STEP 3. These are explanations of existing implementation choices, not additions to the numerical analysis.

## Evidence consulted

- Current chapter sources and generated numerical macros/tables.
- `src/robustcluster_abeta/gmm_ablation.py`, especially fixed replica-balanced sample selection, fitted standardization, paired representations and label matching.
- `results/tables/20261007T104141-f0143175/summary.json`, containing the recorded 50-fit GMM results and explicit evaluation/independence flags.
- Existing audit and publication-scope records.

## Source verification

A comparison against the preceding committed chapter sources confirmed that displayed equations, citation commands and their order, chapter/section headings and labels are unchanged. One valid cross-reference to the existing status table was added. No numerical table, macro, figure, bibliography record, configuration, or analysis code was edited.

The whitespace-delimited chapter-source count changed from 7,569 to 7,606 words; this is not a typeset word count. `git diff --check -- report/chapters` passed. Final pagination and rendered-page inspection are the coordinator's subsequent build task; this source review alone does not establish them.

## Student-confirmed reflection

After this editorial review, the student reported that learning to use GROMACS was initially difficult but enjoyable. Two sentences in Chapter 8 now convey that experience in the first person. They do not claim a completed simulation, mastery of GROMACS, or a specific technical problem that the student did not describe. The paragraph was added after the fixed abstract excerpt was checked; the checked excerpt itself is unchanged.
