"""PLUMED Cartesian-grid validation and bounded bilinear interpolation."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from .validation import BlockedAnalysis, InvalidInput, finite


@dataclass
class FESGrid:
    alpha: np.ndarray
    beta: np.ndarray
    energy: np.ndarray
    metadata: dict
    energy_unit: str | None

    def interpolate(self, alpha, beta):
        alpha, beta = finite(alpha, "alpha queries"), finite(beta, "beta queries")
        if alpha.shape != beta.shape:
            raise InvalidInput("CV arrays have different shapes")
        query = np.column_stack([alpha.ravel(), beta.ravel()])
        outside = ((query[:, 0] < self.alpha[0]) | (query[:, 0] > self.alpha[-1]) |
                   (query[:, 1] < self.beta[0]) | (query[:, 1] > self.beta[-1]))
        if outside.any():
            raise InvalidInput(f"{outside.sum()} CV queries outside FES grid; clipping is forbidden")
        interpolator = RegularGridInterpolator((self.alpha, self.beta), self.energy,
                                              method="linear", bounds_error=True)
        return interpolator(query).reshape(alpha.shape)


def read_fes(path, energy_unit, provenance):
    """Load a grid for reweighting only after explicit unit/provenance declarations."""
    if Path(path).suffix.lower() == ".crdownload":
        raise InvalidInput("Incomplete-download files are never valid FES inputs")
    if not Path(path).is_file():
        raise BlockedAnalysis(f"Complete FES missing: {path}")
    if energy_unit != "kJ/mol" or not provenance:
        raise BlockedAnalysis("FES requires explicit kJ/mol units and a provenance statement")
    grid = read_fes_structure(path)
    grid.energy_unit = energy_unit
    return grid


def read_fes_structure(path):
    """Validate numerical grid structure without asserting an energy unit.

    A successful structural check does not authorize statistical reweighting.
    Interpolated values retain the source file's unspecified energy unit.
    """
    path = Path(path)
    if path.suffix.lower() == ".crdownload":
        raise InvalidInput("Incomplete-download files are never valid FES inputs")
    if not path.is_file():
        raise BlockedAnalysis(f"Complete FES missing: {path}")
    metadata, fields = {}, None
    with path.open() as stream:
        for line in stream:
            tokens = line.split()
            if tokens[:2] == ["#!", "FIELDS"]:
                if fields is not None:
                    raise InvalidInput("Repeated FIELDS header")
                fields = tokens[2:]
            if tokens[:2] == ["#!", "SET"]:
                if len(tokens) != 4 or tokens[2] in metadata:
                    raise InvalidInput("Malformed or duplicate FES metadata")
                metadata[tokens[2]] = tokens[3]
    if fields is None or fields[:3] != ["alpha", "antibeta", "file.free"]:
        raise InvalidInput("Expected PLUMED FIELDS alpha antibeta file.free")
    axes = []
    for name in fields[:2]:
        try:
            low, high = float(metadata[f"min_{name}"]), float(metadata[f"max_{name}"])
            count = int(metadata[f"nbins_{name}"])
            periodic = metadata[f"periodic_{name}"]
        except (KeyError, ValueError) as exc:
            raise InvalidInput(f"Invalid grid metadata for {name}") from exc
        if periodic != "false" or count < 2 or not np.isfinite([low, high]).all() or low >= high:
            raise InvalidInput("Only finite increasing nonperiodic 2D grids are supported")
        axes.append(np.linspace(low, high, count))
    try:
        data = np.loadtxt(path, comments="#", ndmin=2)
    except ValueError as exc:
        raise InvalidInput(f"Malformed FES row: {exc}") from exc
    finite(data, "FES data, including derivative columns")
    if data.shape != (len(axes[0])*len(axes[1]), len(fields)):
        raise InvalidInput(f"Incomplete or malformed FES: actual shape {data.shape}")
    actual_axes = [np.unique(data[:, i]) for i in range(2)]
    for expected, actual in zip(axes, actual_axes):
        if len(actual) != len(expected) or not np.allclose(actual, expected, atol=5e-9, rtol=0):
            raise InvalidInput("Grid coordinates disagree with PLUMED header")
    order = np.lexsort((data[:, 1], data[:, 0]))
    sorted_data = data[order]
    if np.any(np.all(np.diff(sorted_data[:, :2], axis=0) == 0, axis=1)):
        raise InvalidInput("Duplicate FES grid point")
    grid = sorted_data[:, 2].reshape(len(axes[0]), len(axes[1]))
    return FESGrid(actual_axes[0], actual_axes[1], grid, metadata, None)
