# Open questions and blocked analyses

| ID | Question / missing evidence | Consequence | Resolution criterion |
|---|---|---|---|
| Q01 | FES energy units (complete file recovered and validated 2026-10-07) | Missing-file blocker resolved; reweighting still BLOCKED pending unit/provenance declaration | Grid/hash/coverage passed; source code assumes kJ/mol, header has no units; upstream confirmation remains needed |
| Q02 | How was the replica-averaged FES constructed? | Cannot independently reconstruct or verify bias convergence | Original HILLS, sum_hills commands and replica combination procedure |
| Q03 | STEP-2 raw versus normalized scales | Raw mode is source-informed, not verified author equivalence | Author code or explicit methods clarification |
| Q04 | Scientific V2 and changelog missing | Intermediate audit BLOCKED | Original files supplied; hash and inspect without modification |
| Q05 | metad.rbias provenance, units, offset calculation | Optional time-dependent comparison BLOCKED | PLUMED settings/logs or documented generating procedure |
| Q06 | Exact cluster uncertainty/width convention | Width, replica SEM and bootstrap CI kept distinct | SI or author clarification |
| Q07 | Atomic frames/topology and indexing map | Molecular representatives, contacts and ShapeGMM BLOCKED | Compatible coordinates and verified descriptor/frame mapping |
| Q08 | Aβ42 data absent | No Aβ42 computational results | Separate independently validated dataset |
| Q09 | Exact supervisory titles and completed personal activities | Student/degree/matricola/names and academic year 2025–2026 supplied and incorporated in the full report | Distinguish assigned activities from completed personal work |
| Q10 | Original-code/data redistribution rights | Public release excludes raw materials by default | Documented permission or applicable license |
| Q11 | Leonardo access or execution | Templates only; no claimed usage | Real job IDs, logs, account/module/resource evidence |
| Q12 | External ensemble compatibility | External validation optional and deferred | Accessible licensed data plus matched descriptor definitions |
| Q13 | Source-labelled time/length/area units | Recorded assumptions in diagnostics | Upstream analysis commands or metadata |

No unresolved item is filled with inferred simulation settings or fabricated results. Bibliographic uncertainty stays outside references.bib until verified.

## 3 November 2026 follow-up

The requested equilibrium-population analysis prompted a new review of the complete FES header, source code, primary paper and technical correspondence. None supplied an explicit energy-unit and replica-combination declaration for this exact file. New descriptor validation succeeded; the reproduction preflight stopped as BLOCKED before clustering or weighting. Q01/Q02/Q05 remain open. See [the evidence and run records](EQUILIBRIUM_READINESS_V030.md) and the [unsent provenance questions](FES_PROVENANCE_REQUEST.md). No email was sent.
