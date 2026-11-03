"""Shared validation and explicit scientific failure states."""

import time
from dataclasses import dataclass, field

import numpy as np
import psutil


class InvalidInput(ValueError):
    """An available input violates the declared analysis contract."""


class BlockedAnalysis(RuntimeError):
    """Required data, provenance or an enabled execution profile is unavailable."""


class AnalysisFailure(RuntimeError):
    """Valid data could not support the requested estimator."""


class ResourceLimit(AnalysisFailure):
    """Recorded runtime or memory limit was exceeded."""


def finite(values, name="values"):
    array = np.asarray(values, dtype=float)
    if array.size == 0 or not np.isfinite(array).all():
        raise InvalidInput(f"{name} must be nonempty and finite")
    return array


@dataclass
class Budget:
    max_seconds: float = 1800
    max_memory_gib: float = 8
    started: float = field(default_factory=time.monotonic)

    def check(self, additional_bytes=0):
        if time.monotonic() - self.started > self.max_seconds:
            raise ResourceLimit(f"Runtime exceeds {self.max_seconds:g} seconds")
        rss = psutil.Process().memory_info().rss
        if rss + additional_bytes > self.max_memory_gib * 2**30:
            raise ResourceLimit("Current RSS plus requested allocation exceeds memory budget")
