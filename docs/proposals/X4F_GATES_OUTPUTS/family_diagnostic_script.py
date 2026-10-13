"""Descriptive diagnostic (job 0003): mean displacements of the SAME 10,000 seeded F-primary draws
that x4f_run tried; no criterion, verdict or fitted object changes."""
import json, sys, time
from pathlib import Path
import numpy as np
from topo_pilot.analysis import apply_map, displacements, eraser_from_basis, fit_oblique_eraser, whiten
from topo_pilot.contracts import ActivationSet, ArtifactStore, LocalFSBackend, SeedTree
from topo_pilot.experiment.x4b import ReadThroughBackend
from topo_pilot.experiment.x4f_data import load_model_data
main_root, out_root, tables = map(Path, sys.argv[1:4])
t0 = time.process_time()
store = ArtifactStore(ReadThroughBackend(LocalFSBackend(main_root), LocalFSBackend(out_root / "store")))
prov = json.loads((tables / "inputs.json").read_text(encoding="utf-8"))
out = {}
for seed in (1729, 2718, 3141):
    ids = {r["role"].split("[")[0]: r["artifact_id"] for r in prov if r["role"].endswith(f"[{seed}]")}
    d = load_model_data(store, ids, ids["dev_activations"], seed)
    h = d.acts["resid_post_1"][d.cal]
    wh = whiten(h)
    prim = fit_oblique_eraser(h, d.targets["m32"][d.cal], wh)
    target = float(np.mean(displacements(h, apply_map(h, wh.mu, prim.M))))
    D = []
    for j in range(10_000):
        Q, R = np.linalg.qr(SeedTree(0).generator("x4f-v1", "random_eraser", "F-primary", seed, j).standard_normal((wh.k, prim.rank)))
        _, M = eraser_from_basis(wh, Q)
        D.append(float(np.mean(displacements(h, apply_map(h, wh.mu, M)))))
    D = np.array(D)
    lam = np.sort(wh.lam_keep)[::-1]
    out[seed] = {"target_mean_disp": target, "random_mean_disp_quantiles": dict(zip(
        ["min", "q01", "q50", "q99", "max"], map(float, np.quantile(D, [0, .01, .5, .99, 1])))),
        "ratio_target_to_random_max": target / float(D.max()),
        "n_within_5pct": int(np.sum(np.abs(D - target) <= 0.05 * target)),
        "eig_top5": lam[:5].tolist(), "eig_mean": float(lam.mean()), "k": wh.k}
out["cpu_s"] = round(time.process_time() - t0, 2)
out["note"] = "descriptive only; same seeded draws as x4f_run F-primary; no verdict change"
(tables / "family_diagnostic.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
