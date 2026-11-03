# Scientific method audit

The authoritative comparison is docs/PAPER_METHOD_MAP.md. This is an audit of the supplied original and the new modular implementation; Scientific V2 is unavailable.

| Finding | Evidence | Resolution |
|---|---|---|
| Original script cannot parse | Un-commented sentence at line 437 | Preserve source; modular replacement only |
| Replica truncation can hide extra segments | Original slices replicas[:3] | Require exactly the configured count |
| Fixed seed list fails when groups exceed 17 | Original indexes a fixed list | SeedSequence/default_rng; record changed random stream |
| Residual frames enter consensus as generic clusters | Original collects every local label | Acceptable clusters only; residuals assigned in STEP 3 |
| Generic/global labels may reuse integer values | Generic label does not advance next_label | Explicit accepted-member arrays and isolated run identities |
| Large cutoff kernel allocation | (D<=dc).astype(float) | Row-wise count_nonzero |
| Distance matrix initially float64 then copied | cdist then astype(float32) | Bounded cdist blocks into preallocated float32 matrix |
| Silhouettes recompute geometry | silhouette_samples(X, labels) | Reuse validated precomputed distances; record float32 distance convention |
| FES header ignored, nearest lookup and NaN fallback | load_fes_grid/build_weights | Strict grid, finite/bounds checks; linear interpolation |
| Unequal replica contributions possible | Global shifted weights pooled | Normalize each replica then average |
| Descriptor summaries are unweighted | np.mean/np.std inside weighted section | Explicit weighted mean and distribution SD |
| SEM assumes independent frames | std/sqrt(N) | Replica SEM and separately labelled block-bootstrap uncertainty |

For 30,000 frames, a float32 distance matrix alone uses 3.35 GiB. A float64 matrix uses 6.71 GiB. These are allocation estimates, not measured full-run memory. Eliminating a floating cutoff kernel saves a further potential 6.71 GiB. O(N²) storage and repeated silhouette computations remain material costs. No claim of asymptotic improvement is made.

The source's norm of marginal one-dimensional Wasserstein distances is not a joint four-dimensional Wasserstein distance. Raw scaling mixes descriptor units and may emphasize SASA; the normalized alternative is an extension, not an undocumented baseline correction. Density ties, small-tail redistribution and the elbow heuristic are source-informed, explicitly recorded choices.
