# Independent feature-ablation pilot — 7 October 2026

**Completed original extension; not a paper-reproduction result.** The question was whether removing SASA changes the geometric partition of the available biased Aβ40 descriptors. The protocol was recorded in decision D22 (originally labelled D18; identifier corrected without changing the protocol) and committed as `bd669d2` before execution.

## Experimental design

A fixed, replica-balanced random subset of 3,000 frames (1,000 per replica) was selected using sampling seed 20261007. Means and population standard deviations were fitted on these rows only. The four-feature model used nAlpha, nBeta, Rg and SASA; the ablation retained the first three with identical scaling for shared features. The same fit observations were used throughout.

Full-covariance Gaussian mixture models were fitted at K=2,3,4,5,6, with seeds 42–46. Each fit used one initialization, 500 maximum EM iterations, tolerance 0.001 and covariance regularization 1e-6. Using one initialization deliberately exposes initialization sensitivity; convergence does not establish a global likelihood optimum. Configured local limits were 600 seconds and 4 GiB. Fifty models were fitted; all reported convergence. Observed runtime was 7.01 seconds; sampled process-tree peak RSS was approximately 660.3 MiB.

All 300,003 frames, including the fit sample, were assigned to components for descriptive comparison. This is not held-out generalization testing. The fixed random subset is not asserted to contain independent observations. Each replica contributed equally many fit and evaluation frames; statistical reweighting was not used.

## Observed results

| Components | Median four/three-feature ARI | Range across five paired seeds | Median matched-frame fraction |
|---|---:|---:|---:|
| 2 | 0.690 | 0.188–0.868 | 0.917 |
| 3 | 0.864 | 0.862–0.868 | 0.953 |
| 4 | 0.607 | 0.548–0.622 | 0.793 |
| 5 | 0.531 | 0.382–0.696 | 0.682 |
| 6 | 0.457 | 0.294–0.461 | 0.671 |

Cluster identities were matched by maximizing total frame overlap with a rectangular linear assignment. The matched-frame fraction is distinct from ARI: it measures the fraction retaining corresponding labels after that mapping. Per-pair Jaccard overlaps, differences in raw frame fractions and centroid displacement in the shared standardized three-dimensional space are also saved. Unmatched families are retained rather than silently removed.

Within a feature space, all ten pairs among five seeds were compared separately for each K. For K=3, seed ARIs were 0.994–1.000 with all four features and 0.988–1.000 without SASA. K=2 showed much stronger initialization sensitivity: the corresponding ranges were 0.011–1.000 and 0.067–1.000 (rounded). This helps explain why a single seed could give a misleading impression of representation agreement.

**Interpretation:** the K=3 partitions were comparatively stable in this pilot, while feature and seed sensitivity varied substantially across K. The observed Rg–SASA correlation therefore does not justify treating SASA as universally redundant. K=3 is not established as an optimal biological family count. The data do not establish that Gaussian components correspond to distinct metastable states, nor that their fitted mixture proportions or assigned-frame fractions are equilibrium populations.

Ranges describe the runs performed and are not confidence intervals. BIC is saved within each feature space only; cross-dimensional BIC comparisons are not used. The fixed fit subset means this pilot does not quantify uncertainty from choosing different samples. Temporal block sensitivity, independent fit subsets, production DPC comparisons and weighted relevance sensitivity remain future analyses.

## Traceable outputs and rerun

- Analysis manifest: `results/manifests/20261007T104141-f0143175.json`.
- Input hash, software versions, resolved config, source hashes and resource measurements: in that manifest.
- `frame_identities.csv.gz`: all evaluation identities and the exact fit membership.
- `scaler.json`: fitted scaling and source-row indices.
- `assignments.npz`: named arrays for all 50 fits, in the order of frame_identities.
- `models.csv` / `model_parameters.json`: convergence, within-space BIC and fitted parameters.
- `ablation.csv` / `matched_clusters.csv`: paired representation comparisons.
- `seed_stability.csv`: all within-space pairwise comparisons.
- `raw_populations.csv`: raw label fractions by replica and model; label numbers are model-local.

```bash
robustcluster gmm-ablation --config config/gmm_ablation.yaml
python scripts/build_gmm_figures.py --manifest results/manifests/<successful-analysis-run>.json
```

Plotting verifies the successful source manifest and all output hashes before generating PDF/SVG figures. Every observed component count is shown in the seed matrices; no favorable subset is selected for the overview.

Method references: [scikit-learn Gaussian mixtures](https://scikit-learn.org/stable/modules/mixture.html) and [Adjusted Rand index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html). The estimator is a Gaussian mixture of scalar descriptors, not the coordinate-based ShapeGMM method. Numerical tests use explicitly synthetic data; those tests are not additional Aβ40 experiments.
