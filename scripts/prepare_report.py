"""Import hash-verified real diagnostics; generate all report numerical macros/tables."""
import argparse
import json
from pathlib import Path
import shutil

import pandas as pd

from robustcluster_abeta.manifest import dump_json, sha256

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--manifest", required=True)
args = parser.parse_args()
source = Path(args.manifest).resolve()
manifest = json.loads(source.read_text())
if manifest["status"] != "SUCCESS" or manifest["command"] != "diagnostics":
    raise RuntimeError("Report diagnostics require a successful real diagnostics manifest")
run_id = manifest["run_id"]
source_root = source.parent.parent.parent
for record in manifest["outputs"]:
    path = source_root/record["filename"]
    if sha256(path) != record["sha256"]:
        raise RuntimeError(f"Hash mismatch: {path}")
    if "/figures/" in record["filename"] and path.suffix == ".pdf":
        shutil.copy2(path, ROOT/"report/figures"/path.name)
tables = source_root/"results/tables"/run_id
corr = pd.read_csv(tables/"feature_correlation.csv", index_col=0)
pca = json.loads((tables/"pca.json").read_text())
sampling = pd.read_csv(tables/"sampling_diagnostics.csv")
macros = {
    "DiagnosticRun": run_id,
    "DiagnosticSeconds": f"{manifest['runtime_seconds']:.2f}",
    "DiagnosticMemory": f"{manifest['peak_rss_bytes']/2**20:.1f}",
    "RgSasaCorrelation": f"{corr.loc['Rg','SASA']:.3f}",
    "AlphaBetaCorrelation": f"{corr.loc['nAlpha','nBeta']:.3f}",
    "PCAFirst": f"{100*pca['explained_variance_ratio'][0]:.1f}",
    "PCASecond": f"{100*pca['explained_variance_ratio'][1]:.1f}",
    "PCATwo": f"{100*sum(pca['explained_variance_ratio'][:2]):.1f}",
    "ESSMinimum": f"{sampling.correlation_ess.min():.1f}",
    "ESSMaximum": f"{sampling.correlation_ess.max():.1f}",
    "UnreliableCount": str(int((~sampling.reliable_heuristic).sum())),
    "FrameCount": str(manifest['summary']['frames']),
}
generated = ROOT/"report/generated"
generated.mkdir(exist_ok=True)
(generated/"values.tex").write_text("% Generated from a validated real-data run. Do not edit.\n"+"\n".join(
    f"\\newcommand{{\\{key}}}{{{value}}}" for key, value in macros.items())+"\n")
rows=[]
labels={"nAlpha":r"$n_\alpha$", "nBeta":r"$n_\beta$", "Rg":r"$R_g$", "SASA":"SASA"}
for row in sampling.itertuples():
    rows.append(f"{row.replica_id} & {labels[row.descriptor]} & {row.statistical_inefficiency:.0f} & {row.tau_int_ps/1000:.1f} & {row.correlation_ess:.1f} & {row.half_mean_difference_in_sd:.2f} \\\\")
(generated/"sampling_rows.tex").write_text(
    r"\begin{tabular}{@{}clrrrr@{}}\toprule"+"\n"
    +r"Replica & Descriptor & $g$ & $\tau_{\mathrm{int}}$ (ns) & $N_{\mathrm{eff,corr}}$ & Half shift / SD\\\midrule"+"\n"
    +"\n".join(rows)+"\n"+r"\bottomrule\end{tabular}"+"\n")
environment=[("Python",manifest["python"])]+list(manifest["versions"].items())
(generated/"environment_rows.tex").write_text(
    r"\begin{tabular}{@{}ll@{}}\toprule Component & Version in diagnostic manifest\\\midrule"+"\n"
    +"\n".join(f"{key.replace('_',r'\_')} & {value} \\\\" for key,value in environment)
    +"\n"+r"\bottomrule\end{tabular}"+"\n")
dump_json(ROOT/"report/data_provenance.json", {"source_manifest":str(source.relative_to(source_root)),
    "source_manifest_sha256":sha256(source),"run_id":run_id,"source_commit":manifest["git_commit"],
    "outputs":[{"filename":str(p.relative_to(ROOT)),"sha256":sha256(p)} for folder in [generated,ROOT/"report/figures"] for p in sorted(folder.glob("*")) if p.is_file()]})
print(f"Report numerical content prepared from {run_id}")
