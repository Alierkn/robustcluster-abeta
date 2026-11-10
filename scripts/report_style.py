"""Single visual system for every data figure in the internship report.

Import from any figure script (``sys.path`` must contain ``scripts/``)::

    import report_style as rs

    rs.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=rs.figsize(rs.FULL_WIDTH_MM, 70), layout="constrained")
    rs.panel_label(axes[0], "A", "Feature correlations")
    rs.panel_label(axes[1], "B", "Variance explained")
    rs.save_figure(fig, "report/figures/example.pdf")

Design rules (journal practice: Nature final-artwork guide, eLife and PLOS figure guidance):

* One sans-serif family for all figure text: Libertinus Sans, the report's heading face.
  Sizes are fixed for the *final* printed size (figures are drawn at their real width, so no
  LaTeX scaling): ticks/legends 7.5 pt, axis labels 8 pt, panel titles 8.5 pt, panel letters
  9.5 pt bold. Nothing smaller than 7 pt.
* Panel letters are upper-case, bold, navy (like the report's sans section headings) and are
  aligned to the outer top-left corner of each panel *including* its tick and axis labels;
  letters in one row share a baseline.
* Thin (0.6 pt) left/bottom spines, outward ticks, no top/right spines, no background fills,
  no gratuitous grids or 3-D effects.
* Colour: in-palette, colour-blind-aware. Categories use navy / teal / terracotta which
  differ in both hue and lightness; continuous data use a single-hue-family sequential map
  (light -> teal -> navy, monotonic lightness) or a diverging terracotta <-> navy map with a
  neutral cool-grey centre. Never rainbow/jet, never the matplotlib default cycle.
* Output is vector PDF with fonts embedded as TrueType (Type 42) subsets and deterministic
  metadata (no CreationDate), so identical inputs give byte-identical files.

Font embedding note: Libertinus ships as OpenType/CFF. Matplotlib's ``pdf.fonttype = 42``
writes a ``CIDFontType2``/``FontFile2`` (TrueType) dictionary, so embedding a CFF font
directly produces a structurally inconsistent PDF (poppler: "Mismatch between font type and
embedded font file"). ``register_fonts`` therefore converts the CFF outlines to quadratic
TrueType outlines once (fontTools ``cu2qu``, 1/1000 em tolerance -- visually lossless) into
matplotlib's cache directory and registers those. The converted files never leave the cache;
only per-figure subsets are embedded in the PDFs, which the SIL OFL permits. If Libertinus
Sans cannot be found, the documented fallback is DejaVu Sans (bundled with matplotlib, a
native TrueType font), and ``style_info()["font"]["fallback"]`` records that it was used.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

__all__ = [
    "NAVY", "TEAL", "INK", "COOLGREY", "AUDIT", "CODE_COMMENT", "MUTED", "GRID", "LIGHT_TEAL",
    "PALETTE", "CATEGORICAL", "REPLICA_COLORS",
    "CMAP_SEQUENTIAL", "CMAP_SEQUENTIAL_R", "CMAP_DIVERGING", "CMAP_QUALITATIVE", "cmap_segment",
    "FULL_WIDTH_MM", "ONE_HALF_WIDTH_MM", "SINGLE_WIDTH_MM", "FULL_WIDTH_IN", "ONE_HALF_WIDTH_IN",
    "SINGLE_WIDTH_IN", "FONT_SIZES", "mm", "figsize",
    "register_fonts", "apply_style", "panel_label", "finalize", "save_figure", "style_info",
]

STYLE_VERSION = "1.0.0"

# ---------------------------------------------------------------- palette (report preamble.tex)
NAVY = "#173A5E"
TEAL = "#2E6F73"
INK = "#20242A"
COOLGREY = "#F3F5F7"
AUDIT = "#A95542"          # terracotta accent, used for audit / caution marks
CODE_COMMENT = "#667B88"   # blue-grey used for spines and secondary annotation
MUTED = "#5B6670"          # secondary text
GRID = "#DDE3E7"           # hairline grids, if any
LIGHT_TEAL = "#8DBDB8"
PALETTE = {"navy": NAVY, "teal": TEAL, "ink": INK, "coolgrey": COOLGREY, "audit": AUDIT,
           "code_comment": CODE_COMMENT, "muted": MUTED, "grid": GRID, "light_teal": LIGHT_TEAL}
CATEGORICAL = [NAVY, TEAL, AUDIT, CODE_COMMENT, LIGHT_TEAL]
REPLICA_COLORS = CATEGORICAL[:3]

# Sequential: near-white cool grey -> pale teal -> teal -> navy -> deep navy. CIE L* decreases
# monotonically (about 97 -> 13), so the map reads correctly in greyscale and for CVD viewers.
CMAP_SEQUENTIAL = LinearSegmentedColormap.from_list(
    "report_seq", ["#F4F7F7", "#D2E5E2", LIGHT_TEAL, "#4F8E8E", TEAL, NAVY, "#0B1D30"], N=256)
CMAP_SEQUENTIAL_R = CMAP_SEQUENTIAL.reversed("report_seq_r")
# Diverging: terracotta (negative) <-> cool grey (zero) <-> navy (positive); symmetric lightness.
CMAP_DIVERGING = LinearSegmentedColormap.from_list(
    "report_div", ["#66291C", AUDIT, "#D9A99C", COOLGREY, "#9DB3C8", "#3D6488", NAVY], N=256)
for _cmap in (CMAP_SEQUENTIAL, CMAP_SEQUENTIAL_R, CMAP_DIVERGING, CMAP_DIVERGING.reversed("report_div_r")):
    if _cmap.name not in matplotlib.colormaps:
        matplotlib.colormaps.register(_cmap)
CMAP_QUALITATIVE = ListedColormap(CATEGORICAL, name="report_cat")


def cmap_segment(cmap=None, low: float = 0.0, high: float = 0.86, name: str | None = None) -> ListedColormap:
    """Sub-range of an in-palette map, e.g. to stop the sequential map at navy instead of near-black
    when many values sit at the maximum (similarity matrices)."""
    import numpy as np

    cmap = cmap or CMAP_SEQUENTIAL
    return ListedColormap(cmap(np.linspace(low, high, 256)), name=name or f"{cmap.name}_{low:g}_{high:g}")

# ---------------------------------------------------------------- geometry
FULL_WIDTH_MM = 155.0       # report text block (KOMA, 29 + 26 mm margins on A4)
ONE_HALF_WIDTH_MM = 110.0
SINGLE_WIDTH_MM = 75.0
FULL_WIDTH_IN = FULL_WIDTH_MM / 25.4
ONE_HALF_WIDTH_IN = ONE_HALF_WIDTH_MM / 25.4
SINGLE_WIDTH_IN = SINGLE_WIDTH_MM / 25.4

FONT_SIZES = {"tick": 7.5, "legend": 7.5, "annotation": 7.5, "label": 8.0, "title": 8.5,
              "panel": 9.5, "minimum": 7.0}


def mm(value: float) -> float:
    """Millimetres to inches."""
    return value / 25.4


def figsize(width_mm: float = FULL_WIDTH_MM, height_mm: float = 70.0) -> tuple[float, float]:
    """Figure size in inches from millimetres (the figure is drawn at its printed size)."""
    return (mm(width_mm), mm(height_mm))


# ---------------------------------------------------------------- fonts
_FACES = {"regular": "LibertinusSans-Regular.otf", "bold": "LibertinusSans-Bold.otf",
          "italic": "LibertinusSans-Italic.otf"}
_CONVERTER = "cu2qu-1e-3em-v1"
_STATE: dict = {}


def _candidate_dirs() -> list[Path]:
    here = Path(__file__).resolve()
    dirs = []
    if os.environ.get("REPORT_STYLE_FONT_DIR"):
        dirs.append(Path(os.environ["REPORT_STYLE_FONT_DIR"]))
    # The project's verified TeX Live tree (see README / report build instructions).
    for parent in here.parents:
        dirs.append(parent / "work/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts")
    kpse = shutil.which("kpsewhich")
    if kpse:
        try:
            found = subprocess.run([kpse, _FACES["regular"]], capture_output=True, text=True,
                                   timeout=20).stdout.strip()
            if found:
                dirs.append(Path(found).parent)
        except (OSError, subprocess.SubprocessError):
            pass
    dirs += [Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/usr/share/fonts/opentype/libertinus"),
             Path("/usr/share/fonts/OTF"), Path.home() / ".local/share/fonts"]
    return dirs


def _find_libertinus() -> dict[str, Path] | None:
    for directory in _candidate_dirs():
        paths = {face: directory / name for face, name in _FACES.items()}
        if all(p.is_file() for p in paths.values()):
            return paths
    return None


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _cff_to_truetype(src: Path, dst: Path) -> None:
    """Convert CFF outlines to quadratic TrueType outlines (deterministic, timestamp kept)."""
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib import TTFont, newTable

    font = TTFont(src, recalcTimestamp=False)
    if "glyf" in font:
        shutil.copyfile(src, dst)
        return
    units = font["head"].unitsPerEm
    glyph_set, order = font.getGlyphSet(), font.getGlyphOrder()
    glyphs = {}
    for name in order:
        pen = TTGlyphPen(glyph_set)
        glyph_set[name].draw(Cu2QuPen(pen, units / 1000.0, reverse_direction=True))
        glyphs[name] = pen.glyph()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder, glyf.glyphs = order, glyphs
    for tag in ("CFF ", "CFF2", "VORG"):
        if tag in font:
            del font[tag]
    font["maxp"] = maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    for attr in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs",
                 "maxStackElements", "maxSizeOfInstructions", "maxComponentElements"):
        setattr(maxp, attr, 0)
    maxp.maxZones = 1
    font["head"].glyphDataFormat = 0
    post = font["post"]
    post.formatType, post.extraNames, post.mapping, post.glyphOrder = 2.0, [], {}, order
    font.sfntVersion = "\x00\x01\x00\x00"
    tmp = dst.with_suffix(".tmp")
    font.save(tmp)
    os.replace(tmp, dst)


def register_fonts() -> dict:
    """Register Libertinus Sans (TrueType-converted) with matplotlib; return font provenance."""
    if "font" in _STATE:
        return _STATE["font"]
    sources = _find_libertinus()
    info: dict = {"family": "DejaVu Sans", "fallback": True, "files": {}}
    if sources is None:
        warnings.warn("Libertinus Sans not found; report_style falls back to DejaVu Sans "
                      "(set REPORT_STYLE_FONT_DIR to the libertinus-fonts directory).", stacklevel=2)
    else:
        try:
            cache = Path(matplotlib.get_cachedir()) / "report_style_fonts"
            cache.mkdir(parents=True, exist_ok=True)
            for face, src in sources.items():
                digest = _sha256(src)
                dst = cache / f"{src.stem}-{digest[:16]}-{_CONVERTER}.ttf"
                if not dst.exists():
                    _cff_to_truetype(src, dst)
                font_manager.fontManager.addfont(str(dst))
                info["files"][face] = {"source": src.name, "source_sha256": digest,
                                       "embedded_as": "TrueType (Type 42 subset)", "converter": _CONVERTER,
                                       "converted_sha256": _sha256(dst)}
            info.update(family="Libertinus Sans", fallback=False)
        except Exception as error:  # pragma: no cover - documented fallback path
            warnings.warn(f"Libertinus Sans conversion failed ({error}); using DejaVu Sans.", stacklevel=2)
            info = {"family": "DejaVu Sans", "fallback": True, "files": {}, "error": str(error)}
    _STATE["font"] = info
    return info


# ---------------------------------------------------------------- rcParams
def _rc(family: str) -> dict:
    fs = FONT_SIZES
    rc = {
        "font.family": "sans-serif", "font.sans-serif": [family, "DejaVu Sans"],
        "font.size": fs["label"],
        "mathtext.fontset": "custom", "mathtext.rm": family, "mathtext.sf": family,
        "mathtext.it": f"{family}:italic", "mathtext.bf": f"{family}:bold",
        # No bold-italic face exists; map bfit/cal/tt explicitly so no font lookup ever falls back.
        "mathtext.bfit": f"{family}:bold", "mathtext.cal": family, "mathtext.tt": "DejaVu Sans Mono",
        "mathtext.fallback": "stixsans", "mathtext.default": "it",
        "axes.titlesize": fs["title"], "axes.titleweight": "normal", "axes.titlecolor": INK,
        "axes.titlelocation": "left", "axes.titlepad": 4.0,
        "axes.labelsize": fs["label"], "axes.labelcolor": INK, "axes.labelpad": 3.0,
        "axes.edgecolor": CODE_COMMENT, "axes.linewidth": 0.6, "axes.facecolor": "white",
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
        "axes.axisbelow": True, "axes.unicode_minus": True,
        "axes.prop_cycle": matplotlib.cycler(color=CATEGORICAL),
        "axes.formatter.use_mathtext": True, "axes.formatter.limits": (-4, 5),
        "grid.color": GRID, "grid.linewidth": 0.5,
        "xtick.labelsize": fs["tick"], "ytick.labelsize": fs["tick"],
        "xtick.color": CODE_COMMENT, "ytick.color": CODE_COMMENT,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 2.8, "ytick.major.size": 2.8, "xtick.minor.size": 1.6, "ytick.minor.size": 1.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.minor.width": 0.5, "ytick.minor.width": 0.5,
        "xtick.major.pad": 2.5, "ytick.major.pad": 2.5,
        "lines.linewidth": 1.1, "lines.markersize": 3.5, "lines.markeredgewidth": 0.6,
        "patch.linewidth": 0.6, "hatch.linewidth": 0.5,
        "errorbar.capsize": 2.5,
        "legend.fontsize": fs["legend"], "legend.title_fontsize": fs["legend"], "legend.frameon": False,
        "legend.handlelength": 1.6, "legend.handletextpad": 0.5, "legend.borderaxespad": 0.3,
        "legend.labelspacing": 0.35, "legend.columnspacing": 1.2,
        "image.cmap": "report_seq", "image.interpolation": "nearest",
        "figure.facecolor": "white", "figure.dpi": 150,
        "figure.constrained_layout.h_pad": 0.03, "figure.constrained_layout.w_pad": 0.03,
        "figure.constrained_layout.hspace": 0.04, "figure.constrained_layout.wspace": 0.04,
        "savefig.dpi": 600, "savefig.bbox": "standard", "savefig.pad_inches": 0.0,
        "savefig.facecolor": "white", "savefig.transparent": False,
        "pdf.fonttype": 42, "pdf.compression": 9, "ps.fonttype": 42,
        "svg.fonttype": "none", "svg.hashsalt": "report-style",
        "text.color": INK, "text.usetex": False,
    }
    return rc


def apply_style() -> str:
    """Apply the report style globally; return the font family actually used."""
    family = register_fonts()["family"]
    plt.rcdefaults()
    plt.rcParams.update(_rc(family))
    return family


# ---------------------------------------------------------------- panel letters
def panel_label(ax, letter: str, title: str | None = None, *, title_color: str = INK) -> None:
    """Label a panel: bold navy letter at the panel's outer top-left, optional title.

    The title is left-aligned with the axes spine. The letter is placed by ``finalize`` (called
    by ``save_figure``) at the left edge of the panel's tight bounding box -- i.e. left of the
    y tick and axis labels -- on the title's baseline, so letters align across rows/columns.
    """
    ax._report_title = ax.set_title(title if title else " ", loc="left", color=title_color,
                                    fontsize=FONT_SIZES["title"])
    ax._report_panel_letter = letter  # read by finalize()


def finalize(fig) -> None:
    """Run the layout once, freeze it and place panel letters. Idempotent."""
    if getattr(fig, "_report_finalized", False):
        return
    labelled = [ax for ax in fig.axes if getattr(ax, "_report_panel_letter", None)]
    fig.canvas.draw()  # executes constrained layout
    if not labelled:
        fig._report_finalized = True
        return
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    placements = []
    for ax in labelled:
        title = ax._report_title
        title_text = title.get_text()
        baseline = inv.transform(title.get_window_extent(renderer).p0)[1]
        # Outer left edge of the panel: spine, y tick labels and y axis label.
        lefts = [ax.get_window_extent(renderer).x0]
        if ax.yaxis.get_visible():
            ybox = ax.yaxis.get_tightbbox(renderer)
            if ybox is not None:
                lefts.append(ybox.x0)
        x0 = inv.transform((min(lefts), 0))[0]
        placements.append([ax, x0, baseline, title_text])
    # Share one x per column (axes with nearly equal left spine) and one baseline per row.
    def _group(values, tol):
        groups = []
        for v in sorted(set(values)):
            if groups and v - groups[-1][-1] <= tol:
                groups[-1].append(v)
            else:
                groups.append([v])
        return {v: min(g) for g in groups for v in g}
    spines_x = [p[0].get_position().x0 for p in placements]
    col_of = _group(spines_x, 0.02)
    col_x = {}
    for p, sx in zip(placements, spines_x):
        col_x[col_of[sx]] = min(col_x.get(col_of[sx], 1.0), p[1])
    tops = [p[0].get_position().y1 for p in placements]
    row_of = _group(tops, 0.02)
    row_y = {}
    for p, top in zip(placements, tops):
        row_y[row_of[top]] = min(row_y.get(row_of[top], 1.0), p[2])
    fig.set_layout_engine("none")
    for p, sx, top in zip(placements, spines_x, tops):
        ax = p[0]
        x = max(col_x[col_of[sx]], 0.0)
        fig.text(x, row_y[row_of[top]], ax._report_panel_letter, ha="left", va="baseline",
                 fontsize=FONT_SIZES["panel"], fontweight="bold", color=NAVY)
        # Keep the title clear of the letter when the y labels are very narrow.
        if p[3].strip():
            letter_right = x + mm(3.4) / fig.get_figwidth()
            if ax.get_position().x0 < letter_right:
                ax._report_title.set_x((letter_right - ax.get_position().x0) / ax.get_position().width)
    fig._report_finalized = True


# ---------------------------------------------------------------- saving
def save_figure(fig, path, *, formats=None, creator: str | None = None, close: bool = True) -> list[Path]:
    """Write vector output with embedded fonts and deterministic metadata.

    ``path`` may have a suffix (``.pdf``/``.svg``); ``formats`` adds further suffixes, e.g.
    ``formats=("pdf", "svg")``. PDF metadata has no CreationDate/ModDate; SVG has no Date and
    a fixed hash salt, so re-running on identical inputs yields byte-identical files.
    """
    finalize(fig)
    path = Path(path)
    suffixes = list(formats) if formats else [path.suffix.lstrip(".") or "pdf"]
    written = []
    for ext in suffixes:
        target = path.with_suffix(f".{ext}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if ext == "pdf":
            meta = {"Creator": creator or "report_style.py", "Producer": f"matplotlib {matplotlib.__version__}",
                    "CreationDate": None, "ModDate": None}
        elif ext == "svg":
            meta = {"Creator": creator or "report_style.py", "Date": None}
        else:
            meta = {}
        with plt.rc_context({"svg.hashsalt": "report-style"}):
            fig.savefig(target, format=ext, metadata=meta)
        written.append(target)
    if close:
        plt.close(fig)
    return written


def style_info() -> dict:
    """Provenance record of the style (for manifests)."""
    font = register_fonts()
    return {"module": "scripts/report_style.py", "style_version": STYLE_VERSION,
            "module_sha256": _sha256(Path(__file__)), "font": font, "font_sizes_pt": FONT_SIZES,
            "widths_mm": {"full": FULL_WIDTH_MM, "one_half": ONE_HALF_WIDTH_MM, "single": SINGLE_WIDTH_MM},
            "colormaps": {"sequential": "report_seq", "sequential_reversed": "report_seq_r",
                          "diverging": "report_div"},
            "pdf_fonttype": 42, "matplotlib": matplotlib.__version__}
