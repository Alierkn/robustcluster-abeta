# Complete FES validation — 7 October 2026

**PASSED: file/grid integrity and descriptor coverage.** This resolves the missing-complete-file blocker. It does not establish an energy unit, FES convergence or a completed scientific reproduction.

| Check | Observed result |
|---|---|
| Filename / size | FES_AB_40.dat / 273,309,138 bytes |
| SHA256 | `6fd6c3d7c04e20859cf91abb4765e126e0f3fcb982d3795b643165dde26fa3f4` |
| Grid | 2,801 × 1,301 = 3,644,101 points; five columns |
| Fields | alpha, antibeta, file.free, der_alpha, der_antibeta |
| Axes | alpha 0–28; antibeta 0–13; nonperiodic; spacing 0.01 |
| Coverage / duplicates / finite values | Complete header-consistent Cartesian grid; no duplicate points; all five columns finite |
| file.free range | 0–82.213430126, energy unit unverified |
| Descriptor input | 300,003 frames; 100,001 per replica |
| Converted alpha queries | 0.1691136364–23.5778809091, using nAlpha/1.1 |
| Converted beta queries | 0.000180–12.00282, using nBeta/2.5 |
| Bounds | Zero out-of-grid queries; no clipping |
| Bilinear interpolation | All 300,003 interpolated values finite |
| Audit runtime / process peak RSS | 2.075 s / 652,967,936 bytes |

The input descriptor SHA256 remains `cc44ee36a80ae7b04fe035f27ee6764323125e16f139a4ddc533a8a9089bfd77`. The new FES was copied unchanged into ignored `data/raw/`; source and destination hashes agree. The older partial download was not modified or used.

## Evidence and rerun

Run ID: `20261007T102957-e2a462e5`. [Manifest](../results/manifests/20261007T102957-e2a462e5.json), [numeric validation table](../results/tables/20261007T102957-e2a462e5/fes_validation.json), [log](../results/logs/20261007T102957-e2a462e5/audit.log).

```bash
python -m robustcluster_abeta.audit_fes \
  --config config/paper_reproduction.yaml \
  --fes data/raw/FES_AB_40.dat
```

The audit writes a new manifest before validation, records inputs/configuration/software/source hashes, then records success or failure and process peak memory. Success applies only to structural validation. No seeds are needed for this deterministic audit. No frame labels, statistical weights or cluster populations were computed. The full interpolated vector was checked in memory; this audit saves its validation summary, not a per-frame scientific-results table.

## Remaining scientific gate

The supplied script uses `KB_KJMOLK = 0.008314462618` and directly combines this with FES values. This supports **the original implementation's kJ/mol assumption**. The received PLUMED header itself declares no energy unit, and no producing command, PLUMED UNITS setting or replica-combination procedure was supplied. Therefore production configs retain unset FES units/provenance. Establish or explicitly document these before empirical reweighting.

Code validation after separating structure inspection from production unit declarations: **31 pytest tests passed**; Ruff passed. A new analytic test confirms that structural validation leaves units unset while the production loader continues to block unspecified units/provenance. Existing interpolation/invalid-grid tests also passed.

At this validation milestone the PDF and source archive were still the previous release. The later full report revision incorporates these checks; see REVISION_STAGE_2_QA.md. Grid validation alone does not release the blocked weighting analysis.
