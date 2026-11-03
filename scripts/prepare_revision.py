"""Import successful, hash-verified revision evidence into the full report."""

import json
from pathlib import Path
import shutil
from robustcluster_abeta.manifest import sha256, dump_json

ROOT = Path(__file__).resolve().parents[1]
ids = {
    "gmm": "20261007T104141-f0143175",
    "figures": "20261007T104846-17f8483c",
    "fes": "20261007T102957-e2a462e5",
    "preview": "20261007T105122-c040f192",
}
records = {}
for name, run_id in ids.items():
    p = ROOT / "results/manifests" / f"{run_id}.json"
    value = json.loads(p.read_text())
    if value["status"] != "SUCCESS":
        raise RuntimeError("Evidence must be successful")
    for out in value["outputs"]:
        if sha256(ROOT / out["filename"]) != out["sha256"]:
            raise RuntimeError("Evidence changed")
    records[name] = {"manifest": str(p.relative_to(ROOT)), "sha256": sha256(p)}
figures = ROOT / "report/figures"
for name in ["gmm_sensitivity.pdf", "gmm_seed_matrices.pdf"]:
    shutil.copy2(ROOT / "results/figures" / ids["figures"] / name, figures / name)
shutil.copy2(
    ROOT / "results/figures" / ids["preview"] / "cover_concept.pdf", figures / "cover_concept.pdf"
)
gmm = json.loads((ROOT / records["gmm"]["manifest"]).read_text())
generated = ROOT / "report/generated"
values = {
    "GMMModels": str(gmm["summary"]["models"]),
    "GMMSeconds": f"{gmm['runtime_seconds']:.2f}",
    "GMMMemory": f"{gmm['peak_rss_bytes'] / 2**20:.1f}",
    "GMMRun": ids["gmm"],
}
(generated / "revision_values.tex").write_text(
    "\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in values.items()) + "\n"
)
shutil.copy2(ROOT / "report/preview/ablation_rows.tex", generated / "gmm_rows.tex")
shutil.copy2(ROOT / "report/preview/fit_scaler.py", generated / "fit_scaler.py")
assets = [
    figures / name for name in ["cover_concept.pdf", "gmm_sensitivity.pdf", "gmm_seed_matrices.pdf"]
]
assets += [generated / name for name in ["revision_values.tex", "gmm_rows.tex", "fit_scaler.py"]]
assets += list((ROOT / "report/screenshots").glob("*.jpg"))
screenshots = {
    "vmd-gyration.jpg": "https://github.com/Alierkn/vmd-mcp/blob/01912595595bf0302124f57559e1e6a22095fb24/src/vmd_mcp/server.py#L242-L278",
    "gromacs-mdrun.jpg": "https://github.com/Alierkn/gromacs-mcp/blob/2c5c957c3f2c047888b63ae258ace3df34cb8773/src/gromacs_mcp/server.py#L1441-L1479",
}
dump_json(
    ROOT / "report/revision_provenance.json",
    {
        "evidence": records,
        "screenshots": {
            "captured_date": "2026-10-07",
            "method": "Actual Chrome viewport capture using Computer Use; unchanged JPEG bytes",
            "sources": screenshots,
        },
        "outputs": [{"filename": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in assets],
    },
)
print("Verified revision evidence imported")
