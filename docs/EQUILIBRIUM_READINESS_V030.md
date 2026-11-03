# Equilibrium-population prerequisites — 3 November 2026

**Status: BLOCKED before statistical weights or empirical clustering.** The full equilibrium result was requested again, so the available evidence was re-examined rather than merely carrying forward the old status.

## Evidence examined

| Evidence | Finding | What it does not establish |
|---|---|---|
| Complete supplied FES, SHA256 `6fd6c3d7c04e20859cf91abb4765e126e0f3fcb982d3795b643165dde26fa3f4` | Same complete grid as the validated October input; header fields and dimensions inspected again | Header contains no energy-unit or reconstruction declaration |
| Original supplied script, line53 | Uses `KB_KJMOLK=0.008314462618`; consistent with a kJ/mol assumption | An analysis constant is not upstream file metadata |
| Primary paper, printed p6037 | Describes WT-MetaD, sum_hills reconstruction and a replica-averaged FES; hills have a stated kJ/mol height | Does not provide the exact command or combination recipe for the supplied file |
| Author's file-delivery correspondence | The previously authorized Outlook review confirms the script, descriptor and FES were supplied together; the technical-message search yielded no additional unit/combination declaration | No private message or access-bearing link is redistributed; no clarification email was sent |
| Official PLUMED UNITS documentation | kJ/mol is the default, but UNITS can change input/output conventions | A default cannot prove that a particular run used it |
| Supporting-information route | The supplement was located through the public primary-paper archive, but fetching the PDF encountered an access challenge; its content was not inspected in this pass | No SI result or file provenance is inferred from the link alone |

Sources: [primary article in PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13288636/), [publisher](https://pubs.acs.org/doi/10.1021/acs.jpcb.6c01000), [PLUMED UNITS](https://www.plumed.org/doc-v2.9/user-doc/html/_u_n_i_t_s.html). The original locally supplied publisher PDF was also inspected. The main article and software documentation support the estimator; they do not replace provenance of this specific FES.

## Actual checks in this revision

- `20261103T142553-fd935a74`: descriptor validation **SUCCESS**, with a new manifest, configuration, input hashes and execution log.
- `20261103T142651-837817b0`: reproduction prerequisite check using the bounded smoke entry point **BLOCKED**, exit2: FES requires explicit kJ/mol units and a provenance statement.
- No DPC group was fitted, no weight or equilibrium population was calculated. A full production run was not started. The input-validation result is not labelled a completed population analysis.

The unresolved declaration remains unset in the production configuration. It is not replaced with a guessed default. The user's requested full result therefore remains unfinished for a specific scientific reason, while document design and external checker reviews can proceed independently.

## Minimum information needed next

Establish that this exact FES contains the free energy F (rather than an already rescaled bias), its energy unit, and how the three replicas/time interval were combined. A producing PLUMED/sum_hills command plus combination script, or explicit upstream confirmation tied to the filename/hash, can resolve these choices. HILLS/COLVAR and PLUMED settings would additionally permit independent convergence/reconstruction checks.

After that evidence is recorded: validate the numerical inputs; run and inspect bounded smoke clustering; measure resource use; then execute the full published-profile clustering and final-bias estimator with replica-normalized weights, saved frame identities, weighted moments, Kish ESS and replica-aware uncertainty. Successful test fixtures cannot substitute for these empirical outputs.
