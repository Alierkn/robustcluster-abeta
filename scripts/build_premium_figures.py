"""Build descriptive premium figures directly from the two supplied raw inputs.

Figures (vector PDF, 155 mm wide = the report text block, drawn with scripts/report_style.py:
Libertinus Sans, 7.5-9.5 pt at final size, in-palette colormaps):

* descriptor_landscape.pdf  pooled, UNWEIGHTED 2D log-density of Rg vs SASA and nAlpha vs nBeta
* fes_map.pdf               supplied FES grid shifted to min = 0 (energy unit unverified) with the
                            coverage of the 300,003 converted descriptor queries overlaid
* rg_timeseries.pdf         per-replica Rg along the biased trajectory with a rolling mean

Nothing here reweights, clusters or simulates data. Every number is recomputed from
data/raw/input_clustering_ab40.dat and data/raw/FES_AB_40.dat and written, with input
SHA256 hashes, to premium_figures_provenance.json in the output directory.
"""

import argparse
import datetime as dt
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))  # use this worktree's loaders, not an installed copy
sys.path.insert(0, str(ROOT / "scripts"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import scipy  # noqa: E402
from matplotlib.colors import BoundaryNorm, LogNorm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib import patheffects  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from scipy.ndimage import gaussian_filter  # noqa: E402
from scipy.spatial import ConvexHull  # noqa: E402

from robustcluster_abeta.fes import read_fes_structure  # noqa: E402
from robustcluster_abeta.io import read_descriptors  # noqa: E402

import report_style as rs  # noqa: E402

# Documented hashes (docs/FES_VALIDATION_2026-10-07.md, docs/EQUILIBRIUM_READINESS_V030.md).
EXPECTED_SHA256 = {
    "descriptors": "cc44ee36a80ae7b04fe035f27ee6764323125e16f139a4ddc533a8a9089bfd77",
    "fes": "6fd6c3d7c04e20859cf91abb4765e126e0f3fcb982d3795b643165dde26fa3f4",
}
INTERVAL_PS = (1_000_000.0, 3_000_000.0)  # inclusive analysis window
ALPHA_DIVISOR, BETA_DIVISOR = 1.1, 2.5  # CV conversion used for FES queries
TEXT_WIDTH_IN = rs.FULL_WIDTH_IN

NAVY, TEAL, INK, AUDIT = rs.NAVY, rs.TEAL, rs.INK, rs.AUDIT
SPINE, MUTED = rs.CODE_COMMENT, rs.MUTED
REPLICA_COLORS = rs.REPLICA_COLORS
DENSITY_CMAP = rs.CMAP_SEQUENTIAL      # light = few frames, deep navy = many
FES_CMAP = rs.CMAP_SEQUENTIAL_R        # deep navy = low relative F, light = high
FS = rs.FONT_SIZES


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def apply_style():
    """Shared report style (scripts/report_style.py); figures are drawn at their final width."""
    rs.apply_style()


def save(fig, path):
    rs.save_figure(fig, path, creator="scripts/build_premium_figures.py")


def hpd_levels(density, masses):
    """Density thresholds whose super-level sets hold the requested probability mass."""
    flat = np.sort(density.ravel())[::-1]
    cumulative = np.cumsum(flat) / flat.sum()
    return [float(flat[np.searchsorted(cumulative, m)]) for m in masses]


def descriptor_landscape(frames, out, stats):
    pairs = [("Rg", "SASA", r"$R_g$ (nm)", r"SASA (nm$^2$)", ("A", "Compaction and exposure"), "lower right"),
             ("nAlpha", "nBeta", r"$n_\alpha$", r"$n_\beta$", ("B", "Secondary structure"), "upper right")]
    fig, axes = plt.subplots(1, 2, figsize=(TEXT_WIDTH_IN, 2.85), layout="constrained")
    fig.get_layout_engine().set(w_pad=0.04, wspace=0.08)
    gridsize = 48
    counts = []
    for ax, (x, y, *_rest) in zip(axes, pairs):  # first pass: shared colour scale
        hb = ax.hexbin(frames[x], frames[y], gridsize=gridsize, mincnt=1)
        counts.append(hb.get_array().max())
        hb.remove()
    norm = LogNorm(vmin=1, vmax=max(counts))
    landscape = {}
    for ax, (x, y, xlabel, ylabel, title, corner) in zip(axes, pairs):
        hb = ax.hexbin(frames[x], frames[y], gridsize=gridsize, mincnt=1, cmap=DENSITY_CMAP,
                       norm=norm, linewidths=0.2, edgecolors="face")
        r = float(np.corrcoef(frames[x], frames[y])[0, 1])
        per_replica = {int(k): float(np.corrcoef(g[x], g[y])[0, 1]) for k, g in frames.groupby("replica_id")}
        top = corner.startswith("upper")
        ax.text(0.97, 0.95 if top else 0.05, f"pooled Pearson $r$ = {r:.3f}\n$n$ = {len(frames):,} frames"
                .replace("-", "\u2212"), transform=ax.transAxes, ha="right", va="top" if top else "bottom",
                fontsize=FS["annotation"], color=INK, linespacing=1.3,
                bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none", alpha=0.85))
        ax.set(xlabel=xlabel, ylabel=ylabel)
        rs.panel_label(ax, *title)
        ax.margins(0.02)
        landscape[f"{x}_vs_{y}"] = {"pooled_pearson_r": r, "per_replica_pearson_r": per_replica,
                                    "max_frames_per_hexagon": int(hb.get_array().max()),
                                    "occupied_hexagons": int(hb.get_array().size)}
    cbar = fig.colorbar(hb, ax=axes, shrink=0.9, pad=0.015, aspect=30)
    cbar.set_label("Frames per hexagon (log scale)")
    cbar.outline.set_linewidth(0.4)
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    save(fig, out / "descriptor_landscape.pdf")
    stats["descriptor_landscape"] = {"hexbin_gridsize": gridsize, "weighting": "none (unweighted biased sample)",
                                     **landscape}


def fes_map(frames, grid, out, stats, stride):
    energy = grid.energy - grid.energy.min()  # relative F, still in the file's unverified unit
    a_plot, b_plot, f_plot = grid.alpha[::stride], grid.beta[::stride], energy[::stride, ::stride]
    alpha_q = frames.nAlpha.to_numpy() / ALPHA_DIVISOR
    beta_q = frames.nBeta.to_numpy() / BETA_DIVISOR
    outside = int(((alpha_q < grid.alpha[0]) | (alpha_q > grid.alpha[-1]) |
                   (beta_q < grid.beta[0]) | (beta_q > grid.beta[-1])).sum())
    fmax = float(energy.max())
    levels = np.arange(0, np.ceil(fmax / 4) * 4 + 4, 4.0)

    fig, ax = plt.subplots(figsize=(TEXT_WIDTH_IN, 3.2), layout="constrained")
    cs = ax.contourf(a_plot, b_plot, f_plot.T, levels=levels, cmap=FES_CMAP,
                     norm=BoundaryNorm(levels, FES_CMAP.N), antialiased=True)
    cs.set_edgecolor("face")
    ax.contour(a_plot, b_plot, f_plot.T, levels=levels[::5][1:], colors=SPINE, linewidths=0.3, alpha=0.6)

    # Coverage of the converted descriptor queries: smoothed 2D histogram, highest-density regions.
    bin_w = 0.2
    edges_a = np.arange(grid.alpha[0], grid.alpha[-1] + bin_w, bin_w)
    edges_b = np.arange(grid.beta[0], grid.beta[-1] + bin_w, bin_w)
    hist, _, _ = np.histogram2d(alpha_q, beta_q, bins=[edges_a, edges_b])
    smooth = gaussian_filter(hist, sigma=1.0)
    masses = [0.5, 0.9, 0.99]
    thresholds = hpd_levels(smooth, masses)
    centres_a = 0.5 * (edges_a[:-1] + edges_a[1:])
    centres_b = 0.5 * (edges_b[:-1] + edges_b[1:])
    styles = {0.99: (":", 0.9), 0.9: ("--", 0.9), 0.5: ("-", 1.1)}
    for mass, level in sorted(zip(masses, thresholds), key=lambda t: t[1]):
        ls, lw = styles[mass]
        ax.contour(centres_a, centres_b, smooth.T, levels=[level], colors=AUDIT, linestyles=ls, linewidths=lw)
    points = np.column_stack([alpha_q, beta_q])
    hull = ConvexHull(points)
    loop = np.r_[hull.vertices, hull.vertices[:1]]
    ax.plot(points[loop, 0], points[loop, 1], color=INK, lw=0.6, ls=(0, (5, 1.5, 1, 1.5)), alpha=0.85)

    i, j = np.unravel_index(np.argmin(energy), energy.shape)
    ax.plot(grid.alpha[i], grid.beta[j], marker="+", ms=7, mew=1.1, color="white")
    ax.annotate("grid minimum\n(F = 0)", (grid.alpha[i], grid.beta[j]), xytext=(4.0, 1.3),
                fontsize=FS["annotation"], color="white", ha="left", va="center",
                path_effects=[patheffects.withStroke(linewidth=1.6, foreground=NAVY)],
                arrowprops=dict(arrowstyle="-", color="white", lw=0.6, shrinkA=1, shrinkB=4))

    ax.set(xlim=(grid.alpha[0], grid.alpha[-1]), ylim=(grid.beta[0], grid.beta[-1]),
           xlabel=r"FES $\alpha$ coordinate  ($n_\alpha$ / 1.1)",
           ylabel=r"FES $\beta$ coordinate  ($n_\beta$ / 2.5)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    ax.set_title("Supplied free-energy grid and descriptor-query coverage")
    cbar = fig.colorbar(cs, ax=ax, pad=0.015, shrink=0.93, aspect=24, ticks=np.arange(0, levels[-1] + 1, 20))
    cbar.set_label("Relative F (file units, unverified)")
    cbar.outline.set_linewidth(0.4)
    handles = [Line2D([], [], color=AUDIT, ls="-", lw=1.1, label="50% of frames"),
               Line2D([], [], color=AUDIT, ls="--", lw=0.9, label="90% of frames"),
               Line2D([], [], color=AUDIT, ls=":", lw=0.9, label="99% of frames"),
               Line2D([], [], color=INK, ls=(0, (5, 1.5, 1, 1.5)), lw=0.6, label="Convex hull, all frames")]
    leg = ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.995, 0.9), title="Unweighted query coverage",
                    title_fontsize=FS["legend"], fontsize=FS["legend"], frameon=True, framealpha=0.94, edgecolor=SPINE,
                    borderpad=0.55, handlelength=2.4)
    leg.get_frame().set_linewidth(0.5)
    leg.get_title().set_color(INK)
    ax.text(0.988, 0.972, "Visual of the input file \u00b7 energy unit unverified \u00b7 not an equilibrium result",
            transform=ax.transAxes, ha="right", va="top", fontsize=FS["annotation"], color=AUDIT, style="italic",
            bbox=dict(boxstyle="round,pad=0.3,rounding_size=0.12", fc="white", ec="none", alpha=0.9))
    save(fig, out / "fes_map.pdf")

    frac_low = {f"grid_fraction_F_le_{v}": float((energy <= v).mean()) for v in (10, 20, 40)}
    stats["fes_map"] = {
        "grid_shape_alpha_by_beta": list(energy.shape),
        "alpha_range": [float(grid.alpha[0]), float(grid.alpha[-1])],
        "beta_range": [float(grid.beta[0]), float(grid.beta[-1])],
        "file_free_min": float(grid.energy.min()), "file_free_max": float(grid.energy.max()),
        "shift_applied": float(-grid.energy.min()) + 0.0, "relative_F_max": fmax,
        "grid_fraction_at_max_plateau": float(np.isclose(energy, fmax).mean()),
        **frac_low,
        "minimum_location_alpha_beta": [float(grid.alpha[i]), float(grid.beta[j])],
        "energy_unit": "unverified (file declares none)",
        "plot_stride": stride, "plotted_grid_shape": list(f_plot.shape),
        "contour_levels": [float(levels[0]), float(levels[-1]), float(levels[1] - levels[0])],
        "query_conversion": "alpha = nAlpha/1.1, beta = nBeta/2.5",
        "query_alpha_range": [float(alpha_q.min()), float(alpha_q.max())],
        "query_beta_range": [float(beta_q.min()), float(beta_q.max())],
        "queries_outside_grid": outside,
        "coverage_histogram_bin": bin_w, "coverage_smoothing_sigma_bins": 1.0,
        "coverage_hpd_masses": masses,
        "convex_hull_vertices": int(len(hull.vertices)), "convex_hull_area": float(hull.volume),
        "convex_hull_fraction_of_grid_area": float(hull.volume / ((grid.alpha[-1] - grid.alpha[0]) *
                                                                  (grid.beta[-1] - grid.beta[0]))),
    }


def rg_timeseries(frames, out, stats, window):
    fig = plt.figure(figsize=(TEXT_WIDTH_IN, 3.55), layout="constrained")
    fig.get_layout_engine().set(h_pad=0.02, hspace=0.0, wspace=0.01)
    gs = fig.add_gridspec(3, 2, width_ratios=[7.2, 1])
    ylim = (0.85, float(np.ceil(frames.Rg.max() * 10) / 10) + 0.05)
    bins = np.arange(0.85, ylim[1] + 0.02, 0.02)
    per_replica, first_ax, axes_ts, hist_axes, first_h = {}, None, [], [], None
    dt_ps = float(np.unique(np.round(np.diff(frames[frames.replica_id == 1].time_ps), 6))[0])
    for row, (replica, part) in enumerate(frames.groupby("replica_id")):
        color = REPLICA_COLORS[row]
        ax = fig.add_subplot(gs[row, 0], sharex=first_ax, sharey=first_ax)
        first_ax = first_ax or ax
        axh = fig.add_subplot(gs[row, 1], sharey=ax, sharex=first_h)
        first_h = first_h or axh
        t_us = part.time_ps.to_numpy() / 1e6
        rolling = part.Rg.rolling(window, center=True, min_periods=window).mean()
        ax.plot(t_us, part.Rg, color=color, lw=0.25, alpha=0.38, rasterized=True)
        ax.plot(t_us, rolling, color=color, lw=1.15)
        ax.text(0.008, 0.9, f"Replica {replica}", transform=ax.transAxes, ha="left", va="top",
                fontsize=FS["label"], fontweight="bold", color=color)
        ax.set_ylim(*ylim)
        ax.set_yticks([1.0, 2.0, 3.0])
        ax.grid(axis="y", color=rs.GRID, lw=0.4)
        ax.set_axisbelow(True)
        if row < 2:
            ax.tick_params(labelbottom=False)
        axh.hist(part.Rg, bins=bins, orientation="horizontal", color=color, alpha=0.75, density=True,
                 histtype="stepfilled", lw=0)
        axh.axhline(part.Rg.median(), color=INK, lw=0.6, ls="--")
        axh.tick_params(labelleft=False, labelbottom=row == 2)
        axh.spines["left"].set_visible(False)
        axh.tick_params(axis="y", length=0)
        if row == 2:
            axh.set_xlabel("Density")
        axh.set_xticks([0, 2, 4])
        axes_ts.append(ax)
        hist_axes.append(axh)
        per_replica[int(replica)] = {
            "frames": int(len(part)), "time_ps_range": [float(part.time_ps.min()), float(part.time_ps.max())],
            "Rg_mean_nm": float(part.Rg.mean()), "Rg_median_nm": float(part.Rg.median()),
            "Rg_sd_nm": float(part.Rg.std(ddof=1)), "Rg_min_nm": float(part.Rg.min()),
            "Rg_max_nm": float(part.Rg.max()),
            "rolling_mean_range_nm": [float(rolling.min()), float(rolling.max())]}
    axes_ts[1].set_ylabel(r"$R_g$ (nm)")
    axes_ts[2].set_xlabel(r"Biased trajectory time ($\mu$s, source-labelled)")
    axes_ts[0].set_xlim(INTERVAL_PS[0] / 1e6, INTERVAL_PS[1] / 1e6)
    axes_ts[0].set_title("Radius of gyration along each replica")
    key = [Line2D([], [], color=MUTED, lw=0.5, alpha=0.6, label="every frame"),
           Line2D([], [], color=MUTED, lw=1.15, label=f"{window * dt_ps / 1000:g} ns centred rolling mean")]
    axes_ts[0].legend(handles=key, loc="upper right", ncol=2, frameon=False,
                      handlelength=1.8, columnspacing=1.2, borderaxespad=0.2)
    hist_axes[0].text(hist_axes[0].get_xlim()[1] * 0.98, per_replica[1]["Rg_median_nm"] + 0.08, "median",
                      ha="right", va="bottom", fontsize=FS["minimum"], color=INK)
    save(fig, out / "rg_timeseries.pdf")
    stats["rg_timeseries"] = {"frame_spacing_ps": dt_ps, "rolling_window_frames": window,
                              "rolling_window_ns": window * dt_ps / 1000, "rolling": "centred, full window only",
                              "marginal": "unweighted density histogram, bin 0.02 nm; dashed = median",
                              "per_replica": per_replica}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "report/figures"), help="output directory (default report/figures)")
    parser.add_argument("--descriptors", default=str(ROOT / "data/raw/input_clustering_ab40.dat"))
    parser.add_argument("--fes", default=str(ROOT / "data/raw/FES_AB_40.dat"))
    parser.add_argument("--fes-stride", type=int, default=4, help="grid downsampling for plotting only")
    parser.add_argument("--rolling-window", type=int, default=1000, help="rolling-mean window in frames")
    parser.add_argument("--skip-timeseries", action="store_true")
    parser.add_argument("--allow-hash-mismatch", action="store_true",
                        help="continue even if inputs differ from the documented SHA256 hashes")
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    inputs = {}
    for key, path in [("descriptors", args.descriptors), ("fes", args.fes)]:
        digest = sha256(path)
        match = digest == EXPECTED_SHA256[key]
        shown = Path(path).absolute()
        inputs[key] = {"path": str(shown.relative_to(ROOT)) if shown.is_relative_to(ROOT) else str(shown),
                       "resolved_path": str(Path(path).resolve()), "bytes": Path(path).stat().st_size,
                       "sha256": digest, "matches_documented_sha256": match}
        if not match and not args.allow_hash_mismatch:
            raise SystemExit(f"{key}: SHA256 {digest} differs from documented {EXPECTED_SHA256[key]}")

    frames = read_descriptors(args.descriptors, expected_replicas=3, interval=INTERVAL_PS)
    grid = read_fes_structure(args.fes)
    apply_style()
    stats = {"descriptor_input": {
        "frames_in_interval": int(len(frames)), "interval_ps_inclusive": list(INTERVAL_PS),
        "frames_per_replica": {int(k): int(v) for k, v in frames.groupby("replica_id").size().items()},
        "replica_detection": "time resets in the source file (robustcluster_abeta.io.read_descriptors)",
        "weighting": "none; biased WT-MetaD sample"}}
    descriptor_landscape(frames, out, stats)
    fes_map(frames, grid, out, stats, args.fes_stride)
    outputs = ["descriptor_landscape.pdf", "fes_map.pdf"]
    if not args.skip_timeseries:
        rg_timeseries(frames, out, stats, args.rolling_window)
        outputs.append("rg_timeseries.pdf")

    provenance = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "script": "scripts/build_premium_figures.py", "script_sha256": sha256(__file__),
        "command": " ".join([Path(sys.argv[0]).name] + sys.argv[1:]),
        "scientific_scope": ("Descriptive only. Unweighted biased sample; no reweighting, clustering, "
                             "populations or equilibrium interpretation. FES energy unit unverified."),
        "inputs": inputs, "statistics": stats,
        "outputs": {name: {"sha256": sha256(out / name), "bytes": (out / name).stat().st_size} for name in outputs},
        "figure_width_mm": rs.FULL_WIDTH_MM, "style": rs.style_info(),
        "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
                     "matplotlib": matplotlib.__version__, "scipy": scipy.__version__},
        "runtime_seconds": round(time.monotonic() - started, 2),
    }
    (out / "premium_figures_provenance.json").write_text(json.dumps(provenance, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"inputs": inputs, "statistics": stats, "outputs": provenance["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
