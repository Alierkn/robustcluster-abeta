# Internship learning and evidence map

Stage 1 planning, 2026-11-03. This map supports a new report in the separate rebuild worktree. It distinguishes evidence about learning from evidence about calculations. A missing run log does not invalidate the student's account of using a tool; a statement of hands-on use does not establish a particular simulation result.

The student now explicitly confirms hands-on use of **GROMACS, VMD and Python**, and that they personally created **GROMACS MCP and VMD MCP**. The student also confirms that learning GROMACS was initially difficult but enjoyable. These statements may support a first-person learning account. They do not specify a simulation system, duration, machine, version, tutorial completion, or unaided authorship of every source line.

The earlier local learning/storyboard record was consulted for programme context. This public-facing map includes no private chat URLs, access-bearing links, email quotations, or correspondence chronology. It does not treat assistant-written drafts as proof of an activity.

## Evidence categories

| Category | Meaning | Appropriate use in the report |
|---|---|---|
| **P — Programme / assigned material** | The educational programme included a topic or supplied material. This does not, by itself, establish reading completion or practical mastery. | Describe the internship's planned learning sequence. Use “the programme covered” or “the supplied material introduced.” |
| **U — Student-confirmed activity or reflection** | A direct statement by the student about use, creation or experience. | Attribute that activity or reflection to the student at the specificity actually confirmed. Do not demand a computational log for a subjective learning experience. |
| **A — Inspectable artifact** | Source code, documentation, screenshot, a preserved input or a configuration exists. | Explain its design and inspectable behavior. Code presence does not establish successful execution. |
| **L — Logged result** | A successful run, output table, figure or test record supports the stated operation. | Report exactly the calculation or check performed, with its scope and provenance. This is not automatic evidence that it was performed unaided or that a biological interpretation is valid. |
| **M — Missing specific evidence** | A proposed scientific or experiential claim exceeds the available statements/artifacts/logs. | Omit the unsupported detail, identify a prerequisite, or leave it as future work. Do not label an entire tool-learning experience unverified when U supports it. |

These categories can coexist. They are not an ordered score for the student's skill.

## Learning sequence and claim limits

| Topic/activity | Available evidence | Defensible report content | Detail not currently supported |
|---|---|---|---|
| Amino acids, peptide bonds, folding and intrinsic disorder | P: earlier local planning record summarizes supplied introductory material; scientific context has published references in the report. | Explain why an IDP is studied as an ensemble and how this motivated descriptor analysis. Describe the programme's biological starting point. | Completion dates for every reading, laboratory attendance, experiments, or a claim that every textbook was read in full. |
| Force fields, MD and dihedral angles | P: supplied slides/readings summarized in prior planning. U: hands-on GROMACS and VMD use now confirmed. | Connect the underlying concepts to the tools the student used. Distinguish a simulation model from the observations extracted from it. | A named tutorial system, independently prepared force field, equilibration protocol or completed production trajectory unless separately documented. |
| GROMACS practice | U: hands-on use; learning was initially challenging but enjoyable. A: companion repository and inspected `mdrun_start` source. | A brief first-person account of learning the interface and the confirmed reflection; a separate code explanation of command construction and captured output. | Exact commands personally executed, system size, simulation duration, successful Aβ40 production runs, or validation of a specific physical model. |
| VMD practice | U: hands-on use. A: companion repository with descriptor and rendering interfaces; preserved gyration source excerpt. | State that the student used VMD and explain its role in viewing/analysing molecular configurations. Use the source excerpt to discuss atom selection and frame-indexed measurements. | A particular loaded trajectory, saved molecular image, atom selection, or validated Aβ40 coordinate analysis without the corresponding artifact. Do not invent a representative structure. |
| Python scientific analysis | U: hands-on use. A/L: modular package, numerical fixtures, descriptor diagnostics and GMM experiment. | Describe the work with tabular descriptors, scaling, fitting, comparison and plotting. Use one small code example to connect implementation to statistical meaning. | An inference that all analysis was unaided, or that the student independently wrote every inherited/new line. Preserve the existing assistance and contributor statements. |
| Creation of VMD MCP and GROMACS MCP | U: student personally created both projects. A: public repositories, preserved source excerpts and genuine browser screenshots. | “I created VMD MCP and GROMACS MCP…” is supported, followed by a concrete explanation of their interfaces. Acknowledge repository contributor history and actual tool assistance normally. | Their use to generate the supplied Aβ40 trajectories, a completed integrated RobustCluster pipeline, or a successful execution of every exposed tool. |
| WT-MetaD and final-bias weighting | P/A: primary paper, method map and implemented equations/tests. L: complete-grid validation, not empirical reweighting. | Explain the conceptual distinction between biased frame frequency and equilibrium probability; describe tested interpolation and weight calculations. | Running the original metadynamics simulation, rebuilding its bias without HILLS, validated energy units, weighted family populations or physical kinetics. |
| Descriptor correlation, PCA and temporal sampling | L: successful run `20260921T011959-583b4421`; matching numerical tables in `20260921T013152-c45e6960`. | Discuss the observed geometry, why Rg/SASA redundancy was questioned, and why saved rows need not be independent. | Interpreting all 12 flagged ESS estimates as precise independent-sample counts, equilibrium convergence, or physical relaxation times. |
| Independent GMM feature-removal study | L: `20261007T104141-f0143175`, 50 converged fits, saved assignments and comparisons; GF figure run. | Explain the question, fixed fit sample, seeds, assignments and what changed when SASA was removed. Report a completed original extension separate from DPC reproduction. | Optimal biological cluster number, held-out predictive performance, confidence intervals from seed ranges, equilibrium component populations, or completed production DPC robustness. |
| Scientific software and reproducibility | A/L: configs, manifests, tests and source-linked figures; v0.1.2 QA `20261103T131615-qa-72d4c6` reports 36 tests and lint success. | Describe practices that make an analysis inspectable: preserving originals, explicit validation, recording failures and fitting transforms once. | That passing tests establishes biological truth, or that planning-stage checks reran the complete scientific pipeline. |
| HPC / Leonardo | A: configurable submission template and official-documentation reference. M: no Leonardo execution logs or job IDs. | Describe the template and HPC concepts only at the level evidenced by the project. | Claimed job submission, allocation, personal account, compute hours or calculations attributed to Leonardo. Even “introduced during my internship” needs a confirmed experience if used in first person. |
| LaTeX, illustrations and report preparation | A: source, existing generated-art provenance and successful v0.1.2 build. | Explain the delivered scientific document and reproducible source. Keep conceptual art distinct from empirical figures. | Attributing all typesetting/artwork to unaided student work, saying Adobe was used when only guidance was consulted, or claiming a particular unexposed image-model version. |

## Inspectable companion-project examples

| Project | Public source and preserved artifact | What the example can teach |
|---|---|---|
| VMD MCP | [Repository](https://github.com/Alierkn/vmd-mcp); [inspected gyration excerpt](https://github.com/Alierkn/vmd-mcp/blob/01912595595bf0302124f57559e1e6a22095fb24/src/vmd_mcp/server.py#L250-L266); `report/generated/vmd-mcp-excerpt.py`; `report/screenshots/vmd-gyration.jpg` | How a structured request becomes a Tcl operation, how atom selection/mass weighting affects the measurement, and how frame-indexed values return to a client. The inspected function documents angstrom units; comparison with the nanometre-labelled descriptor table needs a verified conversion and compatible atom definitions. |
| GROMACS MCP | [Repository](https://github.com/Alierkn/gromacs-mcp); [inspected background-run excerpt](https://github.com/Alierkn/gromacs-mcp/blob/2c5c957c3f2c047888b63ae258ace3df34cb8773/src/gromacs_mcp/server.py#L1452-L1467); `report/generated/gromacs-mcp-excerpt.py`; `report/screenshots/gromacs-mdrun.jpg` | Why argument construction, paths, subprocess execution and output capture matter in a scientific interface. Source inspection explains orchestration, not a successful MD trajectory or scientific validation. |

The commit links identify historical source actually inspected. This stage did not refresh their remote HEADs or run either companion server. Source and screenshot hashes are in `report/artwork_provenance.json` and `report/revision_provenance.json`. Their licenses and attribution remain separate from the new RobustCluster code license.

## Proposed Chapter 8 writing structure

1. **From course methods to molecular data:** one paragraph connecting the programme's biological/MD topics to confirmed GROMACS, VMD and Python practice. The student's GROMACS reflection fits here in two direct sentences.
2. **What implementation made clearer:** explain one specific learning relationship supported by the analysis, such as dependent trajectory rows or fixed feature scaling. Describe the operation and consequence rather than claiming an undocumented personal revelation.
3. **The two tools the student created:** attribute the MCP projects explicitly to the student, describe each through an inspected function, and link to full public source. Keep screenshots and longer listings in the software appendix.
4. **What the project now enables:** summarize inspectable code and results and name the next scientific prerequisite. Do not repeat the whole scientific-status table or suggest that all proposed extensions ran.

Suggested factual wording, to adapt rather than treat as a compulsory script:

> During the internship, I used GROMACS, VMD and Python. Learning to use GROMACS was demanding at first, but I enjoyed becoming more familiar with it. I also created VMD MCP and GROMACS MCP, which expose selected molecular-software operations through structured requests.

This paragraph stays within the student's confirmation. Specific sessions, commands, screenshots of molecular work, dates, or quantitative simulation claims should be added only when the student supplies them or an existing artifact supports them. The surrounding scientific prose should use the evidence records above rather than first-person claims about undocumented activity.

## Stage-1 check boundary

The inventory, selected manifests, source figures/tables, provenance files, current learning chapter and earlier planning record were inspected. Stored hash checks passed for the selected imported assets and successful analytical output sets; details are in `VISUAL_AND_EVIDENCE_MAP.md`. No new test suite, MD calculation, clustering run, report build, remote repository refresh or literature verification was performed in this planning stage.
