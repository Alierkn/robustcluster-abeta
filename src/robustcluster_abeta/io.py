"""Strict descriptor parsing with immutable source-frame identity."""

from pathlib import Path

import numpy as np
import pandas as pd

from .validation import BlockedAnalysis, InvalidInput, finite

SOURCE_COLUMNS = ["time", "metad.rbias", "nalpha", "nbeta", "RG", "SASA", "ASASA", "PSASA", "HBONDSPP", "HBONNDSPS"]
COLUMNS = ["time_ps", "metad_rbias", "nAlpha", "nBeta", "Rg", "SASA", "ASASA", "PSASA", "HBONDSPP", "HBONDSPS"]
FEATURES = ["nAlpha", "nBeta", "Rg", "SASA"]
DESCRIPTORS = FEATURES + ["ASASA", "PSASA", "HBONDSPP", "HBONDSPS"]


def read_descriptors(path, expected_replicas=3, interval=(1e6, 3e6)):
    path = Path(path)
    if not path.is_file():
        raise BlockedAnalysis(f"Descriptor input missing: {path}")
    if path.suffix == ".crdownload":
        raise InvalidInput("Partial downloads cannot be descriptor inputs")
    header, source_lines = None, []
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                if header is None:
                    header = stripped.lstrip("# ").split()
                continue
            source_lines.append(line_number)
    if header != SOURCE_COLUMNS:
        raise InvalidInput(f"Unexpected descriptor header: {header!r}")
    try:
        values = np.loadtxt(path, comments="#", ndmin=2)
    except ValueError as exc:
        raise InvalidInput(f"Malformed descriptor row: {exc}") from exc
    finite(values, "descriptor table")
    if values.shape[1] != len(COLUMNS):
        raise InvalidInput("Expected exactly 10 columns")
    cuts = np.r_[0, np.flatnonzero(np.diff(values[:, 0]) < 0) + 1, len(values)]
    if len(cuts) - 1 != expected_replicas:
        raise InvalidInput(f"Expected {expected_replicas} replicas, found {len(cuts)-1}")
    low, high = interval
    if not np.isfinite([low, high]).all() or low >= high:
        raise InvalidInput("Invalid analysis interval")
    table = pd.DataFrame(values, columns=COLUMNS)
    table.insert(0, "source_row", np.arange(len(table)))
    table.insert(1, "source_line", source_lines)
    table["replica_id"] = 0
    table["frame_index"] = 0
    for replica, (start, stop) in enumerate(zip(cuts[:-1], cuts[1:]), 1):
        times = values[start:stop, 0]
        if len(times) < 2 or np.any(np.diff(times) <= 0):
            raise InvalidInput(f"Replica {replica}: times must strictly increase")
        if times[0] > low or times[-1] < high:
            raise InvalidInput(f"Replica {replica} does not cover requested interval")
        table.loc[start:stop-1, "replica_id"] = replica
        table.loc[start:stop-1, "frame_index"] = np.arange(stop-start)
    selected = table.loc[table.time_ps.between(low, high)].copy().reset_index(drop=True)
    if selected.groupby("replica_id").size().min() < 2:
        raise InvalidInput("Insufficient frames within requested interval")
    if (selected[DESCRIPTORS] < 0).any().any():
        raise InvalidInput("Structural descriptors must be nonnegative")
    selected.attrs["original_header"] = header
    selected.attrs["units_status"] = "time/length/area from source script; rbias units unverified"
    return selected
