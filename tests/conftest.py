from pathlib import Path

import numpy as np
import pytest

from robustcluster_abeta.io import SOURCE_COLUMNS


@pytest.fixture
def descriptor_file(tmp_path):
    values = []
    for replica in range(3):
        for frame in range(6):
            values.append([1e6+frame*4e5, -frame, 1+frame*.1+replica, 2+frame*.2,
                           1+frame*.02, 30+frame, 10+frame, 15+frame, 8+frame, 100+frame])
    path = tmp_path/"descriptors.dat"
    np.savetxt(path, values, header="\t".join(SOURCE_COLUMNS))
    return path


def write_fes(path, alpha=None, beta=None, function=None):
    alpha = np.linspace(0, 3, 4) if alpha is None else alpha
    beta = np.linspace(0, 2, 3) if beta is None else beta
    function = (lambda a, b: 2*a+3*b+a*b) if function is None else function
    header = ["#! FIELDS alpha antibeta file.free"]
    for name, axis in [("alpha", alpha), ("antibeta", beta)]:
        header.extend([f"#! SET min_{name} {axis[0]}", f"#! SET max_{name} {axis[-1]}",
                       f"#! SET nbins_{name} {len(axis)}", f"#! SET periodic_{name} false"])
    rows = [f"{a:.9f} {b:.9f} {function(a,b):.12f}" for a in alpha for b in beta]
    Path(path).write_text("\n".join(header+rows)+"\n")
    return path


@pytest.fixture
def fes_file(tmp_path):
    return write_fes(tmp_path/"fes.dat")
