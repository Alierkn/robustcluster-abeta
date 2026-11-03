# Reproduction and build instructions

## 1. Verify the evidence

Read docs/PROJECT_INVENTORY.md. Obtain the original descriptor file and compare its SHA256 before placing it in data/raw. Preserve Scientific V2 unchanged if it becomes available. Do not rename or repair a .crdownload into an analysis input. Store provenance evidence separately from mutable analysis products.

## 2. Install the tested environment

Use Python 3.12 and a project virtual environment. Install requirements-lock.txt, then `pip install --no-deps -e .`. The lock records actual package versions, not the authors' GROMACS/PLUMED versions. Linux/macOS package availability can differ; test a new platform and save its manifest rather than claiming bitwise equivalence across platforms.

Run `pytest -q` and `ruff check src tests scripts`. Analytic and synthetic fixtures are explicitly marked in tests; none stands in for missing Aβ40 observations. Preserve the test log and JUnit output with a release.

## 3. Lightweight diagnostics

Run `robustcluster validate --config config/paper_reproduction.yaml`, then `robustcluster diagnostics --config config/robustness.yaml`. Alternatively, `snakemake -s workflows/Snakefile --cores 1` runs these stages in dependency order. Successful workflow pointers refer to immutable manifest files. Do not interpret file presence alone as analysis success.

Diagnostics save correlations, standardized PCA, raw histograms, per-replica moments, autocorrelations and approximate sampling ESS. Correlation-time reliability requires a positive truncation point, at least 50 estimated statistical inefficiencies within the window, and a half-window mean shift no larger than 0.25 standard deviations. These conservative heuristics do not establish equilibrium. The autocorrelation estimator uses all lags; plotting decimates the first half-window only.

## 4. Unblock weighted reproduction

The recovered FES has passed complete-grid and CV-coverage validation (docs/FES_VALIDATION_2026-10-07.md). For another input, supply a complete FES with PLUMED grid metadata and all finite cells. Record its verified energy units (`kJ/mol`) and generating/replica-combination procedure in config inputs. The pipeline will not infer energy units merely from a filename. Run smoke first. Review its fitted families, rejected frames, runtime and measured memory. Medium remains a feasibility experiment. Full requires a reviewed config with full.enabled true; retain all recorded scientific parameters.

Use `robustcluster reproduce --config CONFIG --profile smoke`. The resulting frame table retains source identity, CV conversions, FES values, raw log weights, raw-weight numerical status, replica-normalized and pooled weights, and final labels. Raw exponential overflow is represented as a missing raw_weight plus an explicit flag; it never enters normalization. Weighted descriptor standard deviations describe ensemble spread; they are not confidence intervals.

## 5. Independent robustness experiments

Use the robustness config and select `seeds`, `seed-pilot`, `features`, `wasserstein`, or `reweighting`. Seed comparisons rerun group sampling, DPC, consensus and final assignment. Features include the required no-SASA ablation, optional no-Rg ablation, full standardized PCA and whitened PCA. The same numerical DPC thresholds are retained, so PCA comparisons test metric/scale sensitivity rather than selecting an optimized alternative. The pilot uses five seeds. Full count is configurable from 20 to 50; no full result exists in this release.

Matched family populations are variability across fitted partitions, not independent equilibrium estimates. Unmatched clusters remain explicit. Bootstrap uncertainty in reproduction is conditional on the fitted partition and supplied FES: contiguous blocks are resampled independently within each replica, with each resampled replica renormalized. Default block length is twice the largest estimated inefficiency among the four descriptors, rounded upward and capped at the replica length. Reliability flags and block lengths are saved. This does not include FES reconstruction uncertainty or bias nonstationarity.

The rbias comparison additionally requires documented `metad.rbias` units and generation provenance. It uses exp(rbias/RT) and never replaces final-bias weighting. DPA, ShapeGMM and external validation are explicitly deferred optional stages.

## 6. Regenerate figures and report

`robustcluster figures --config config/robustness.yaml --source-manifest PATH` checks the source manifest status and every output hash, then creates a fresh figure-generation run. `scripts/prepare_report.py --manifest PATH` imports tables and figures from a successful diagnostics run and creates traceable LaTeX macros. `scripts/build_report.py --tex-bin PATH` runs LuaLaTeX/Biber through latexmk. Use a TeX Live installation with the packages listed in report/preamble.tex; never silently substitute another engine or font.

The local TeX toolchain was installed under the task's work directory; the source archive does not bundle executable runtimes. The build script accepts a different verified TeX bin directory. Publication-style figures are saved as PDF/SVG. Bibliography metadata is checked against publisher records and official documentation in docs/literature.json; no live network access is required to compile the delivered sources.

## 7. Release audit

Run `python scripts/verify_release.py --originals-dir /path/to/originals` from a fresh environment; it saves pytest/JUnit and lint logs, compares original hashes, checks the bibliography verification register, checks scientific output hashes and validates the latest report build. Inspect the rendered PDF separately and record the visual review. Commit the coherent source and outputs, then run `python scripts/release.py`. The archive uses Git's tracked-file allowlist and excludes raw/legacy inputs and runtime caches. Its checksum is in a separate `.sha256` file to avoid self-reference. The release manifest distinguishes successful, blocked and historical failed stages. Source availability and passing tests do not establish successful paper reproduction.

Each final report build retains its own immutable PDF under its run log directory. `report/report.pdf` is a convenience copy. Early draft report manifests used this mutable copy as an output; their superseded PDFs are not claimed to be retained. The selected final build and all empirical scientific outputs pass output-hash checks.

## Independent descriptor-only GMM pilot

`robustcluster gmm-ablation --config config/gmm_ablation.yaml` uses no FES. The supervisor enforces the recorded 600-second / 4-GiB limits and writes a unique manifest. Exact fit identities, scaling, all model parameters and labels are retained. See docs/GMM_ABLATION_PILOT.md for interpretation and limitations. Figures can be rebuilt with `python scripts/build_gmm_figures.py --manifest results/manifests/<run>.json`. The three-page design sample has its own build script, source manifests and LaTeX files under report/preview; it is retained as an intermediate design artifact. The revised full report incorporates this evidence.

## Rebuild the delivered revision

The delivered source includes immutable numerical outputs, so report compilation does not require redistributing raw inputs. With the tested Python environment active:

```bash
python scripts/build_report.py --tex-bin /absolute/path/to/texlive/bin/platform
python scripts/verify_release.py
```

The historical asset-import helper `prepare_revision.py` selects the documented successful GMM, FES, figure and preview manifests and checks every output hash before importing assets. It does not rerun or silently select newer analyses. To publish a new scientific revision, explicitly update these selections after reviewing its successful runs. For v0.2.0, `report/rebuild_provenance.json` additionally locks imported assets and the new figure run. Do not run historical import helpers on the final source without updating and reviewing this record. The actual screenshots are preserved assets; reproducing the report uses those captures, not a live GitHub page. `report/revision_provenance.json` records their commit-specific URLs and hashes. Build diagnostics and an immutable PDF are retained for each build.

The optional `--originals-dir` release-check argument verifies all four historical source files when they remain available at that location. Without it, preserved local script/data copies are still checked when present; absence of the original-download folder is explicitly recorded. The public source archive excludes both the complete and partial FES, the descriptor input and supplied legacy script.

## Editorial illustration assets

The final cover and two conceptual artworks are preserved PNG assets under `report/artwork/`. `docs/ARTWORK_PROMPTS.json` records the exact prompts and built-in tool; the tool did not expose a verifiable model-version identifier. Recompilation uses the saved images, not stochastic regeneration. `report/artwork_provenance.json` records image and source-excerpt hashes; the report builder verifies them before compiling. Scientific plots remain generated from recorded numerical tables. The source excerpts retain exact source text, with presentation-only indentation suppression for the GROMACS panel. No code screenshot was repainted by a generative model.

The workflow drawing can be regenerated independently with `python scripts/refresh_workflow_figure.py`. It clips connectors to actual rendered box boundaries, saves PDF/SVG under a new manifest and updates only the report workflow asset. Numerical diagnostic outputs are preserved.

Report builds and validation also work from an extracted source archive without `.git`. In that case commit and dirty-state metadata are explicitly null; file hashes and selected historical manifests retain the evidence trail. An unrelated enclosing repository is never used as this project's Git identity. The release-packaging command itself still requires a Git checkout because it uses tracked files as its allowlist.

## Regenerate the v0.2.0 figure layout

```bash
python scripts/build_editorial_figures.py
```

This reads the selected successful diagnostic/GMM manifests, verifies every source-output hash, checks the table structure and writes three PDF/SVG pairs to a new immutable run directory. It does not fit new models or change `report/`. The selected delivered run is `20261103T135347-e4275730`. Plot labels use DejaVu Serif TrueType; the LaTeX document uses Libertinus. Inspect a regenerated run before copying its three figure pairs into `report/figures` and updating the selected source-manifest and asset hashes in `report/rebuild_provenance.json`. A different font or Matplotlib release can change file bytes without changing plotted numerical values; record that environment rather than claiming byte-identical rendering.

The isolated `report-next/` draft was used during editing and is not part of the source archive. Historical draft manifests/PDFs are retained as development evidence; only the final `report/` source and selected release build define the delivered document.
