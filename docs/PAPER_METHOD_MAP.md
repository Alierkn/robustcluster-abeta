# Paper-to-implementation method map

Authority: Cadenelli et al., J. Phys. Chem. B 130 (2026), 6035–6046, DOI [10.1021/acs.jpcb.6c01000](https://pubs.acs.org/doi/10.1021/acs.jpcb.6c01000). Page references below use printed page numbers. Scientific V2 is unavailable for **every row**: no V2 comparison is asserted.

| Step / paper evidence | Mathematical specification | Original implementation | Final implementation / validation | Remaining ambiguity |
|---|---|---|---|---|
| Replicas / interval, pp. 6036–6037 | Three replicas; 1–3 μs retained | Time resets; takes first three without exact-count check | Strict header/time/replica validation; identity preservation; endpoint tests | Generating trajectory identifiers absent |
| Descriptor scaling, p. 6037 | α=nα/1.1; β=nβ/2.5 | Same conversions | Explicit CV conversion and bounds tests | Exact upstream descriptor commands absent |
| Feature normalization, pp. 6038, 6041–6043 | Four dimensionless descriptors | Pooled min–max scaling | Source-informed pooled min–max; constant-feature rejection | Paper does not fully specify normalization estimator |
| Random groups, p. 6043 | Approximately 30,000 frames per subset | Fixed global seeds; limited to 10 groups | Local RNG streams, disjoint groups, documented small-tail redistribution | Exact author random draws unavailable |
| DPC, pp. 6038, 6043 | ρi=Σj 1(Dij≤dc); δi distance to earlier higher-ranked density point; centers ranked by ρδ | Cutoff density includes self; density ties depend on sort | Deterministic density/frame tie order; scan 10→2; precomputed silhouettes | Equal-density policy is a documented numerical convention |
| Acceptance, p. 6038 | Mean silhouette≥0.3; N≥300; dc initially 1.3, ×0.9; stop after five failed iterations | Same thresholds, but residuals given generic cluster labels | Residual label −1; acceptance-only consensus; explicit no-cluster error | Tie among equally acceptable center counts follows descending scan |
| Wasserstein, p. 6038 | d(A,B)=[Σf W1(Af,Bf)²]½ | Uses physical/raw descriptors | Reproduction retains raw source convention; normalized extension separate; analytic tests | Published STEP-2 scaling unresolved; not joint 4-D optimal transport |
| Hierarchical cut, pp. 6038, 6043 | Average linkage; elbow of merge-distance curve | Cubic smoothing spline s=5, maximum second derivative in first 90% | Source-informed heuristic, diagnostics saved; reject insufficient merges | Exact published elbow prescription unspecified |
| STEP 3, p. 6043 | Assign every frame to closest global centroid | One pass in normalized feature space | One pass using accepted-member centroids; deterministic ties; residual assignment tests | Not iterative k-means; centroids not subsequently refitted |
| FES interpolation, p. 6037 | Bilinear F(α,β) | Nearest point; NaN fallback; silent boundary selection | Validated PLUMED Cartesian grid; bounds_error=True; analytic bilinear tests | Complete grid recovered and validated 7 October; energy unit and replica-averaging recipe unresolved |
| Final-bias weights, eqs. 2–7 | log wi=−(1−1/γ)F/(RT) | Global log-shift and pooled normalization | Log-sum-exp within replica, then equal replica mixture; constant-offset tests | Energy units and FES generation must be declared with evidence |
| Cluster relevance, p. 6038 | Rk=(1/3)Σr Σi∈k wr,i | Pooled unnormalized weights | Separate replica populations, mean, replica SEM, block-bootstrap CI | Published cluster-specific uncertainty less explicit than histogram SEM |
| Structural characterization, Fig. 6–7 | Weighted mean and width | Arithmetic mean/std despite weighted relevance | Weighted central second moment; width distinct from estimation error | Confirm exact published width convention |

The final pipeline is a documented reproduction with corrections; it is not a claim of bitwise equivalence to the supplied script. Report each source-informed choice. Any later V2 file is preserved unchanged and adds an evidence column without retroactively rewriting provenance.
