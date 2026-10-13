"""X4-F gates G1-G5 for one model (x4f-exec-v2 §4-§10); numbers only, no I/O.

Every fitted object uses calibration rows only; outer validation is read once per score.
"""

from __future__ import annotations

import hashlib

import numpy as np
import torch

from topo_pilot.analysis import (
    apply_map,
    kl_rows,
    leading_components,
    pc_scores,
    r2_pooled,
    rbf_bandwidth,
    rbf_features,
    rbf_map,
    readout_projector,
    standardizer,
)
from topo_pilot.contracts import SeedTree
from topo_pilot.learner import forward_with_patch

from .x4f_data import INDEX, ModelData
from .x4f_probe import nested_ridge

STREAM = "x4f-v1"
N_SHUFFLE, N_RBF = 20, 2048
G1_PRIMARY, G1_R2, G3_LINEAR, G3_RBF_LABEL = 0.50, 0.10, 0.05, 0.25
CONTROLS = ("shuffled_m32", "R1", "m2", "local", "generic")


def gen(*scope) -> np.random.Generator:
    return SeedTree(0).generator(STREAM, *scope)


def _split(d: ModelData, X):
    return X[d.cal], X[d.val]


def probe(d: ModelData, X, Y) -> dict:
    """Nested ridge of ``X -> Y`` (calibration selection, one validation score)."""
    (Xc, Xv), (Yc, Yv) = _split(d, X), _split(d, Y)
    r = nested_ridge(Xc, Yc, d.panel[d.cal], Xv, Yv)
    return {"lam": r.lam, "r2": r.r2, "status": r.r2_status}


def shuffled(d: ModelData, X, Y, target: str) -> dict:
    """20 shuffled-calibration-target refits through the identical pipeline; q95."""
    (Xc, Xv), (Yc, Yv) = _split(d, X), _split(d, Y)
    vals = []
    for k in range(N_SHUFFLE):
        perm = gen("shuffle", target, d.seed, k).permutation(Yc.shape[0])
        vals.append(nested_ridge(Xc, Yc[perm], d.panel[d.cal], Xv, Yv).r2)
    ok = [v for v in vals if v is not None]
    q95 = float(np.quantile(ok, 0.95)) if len(ok) == N_SHUFFLE else None
    return {"values": vals, "q95": q95,
            "status": "ok" if q95 is not None else "SHUFFLE_UNDEFINED"}


def rbf_probe(d: ModelData, Xc_feat, Xv_feat, Yc, Yv) -> dict:
    """RBF random-feature ridge (calibration standardisation and median bandwidth)."""
    mean, scale = standardizer(Xc_feat)
    Xs = (Xc_feat - mean) / scale
    ell, status = rbf_bandwidth(Xs, gen("rbf_bandwidth", d.seed))
    if ell is None:
        return {"r2": None, "status": status, "ell": None}
    omega, b = rbf_map(Xs.shape[1], N_RBF, ell, gen("rbf", d.seed))
    r = nested_ridge(rbf_features(Xs, omega, b), Yc, d.panel[d.cal],
                     rbf_features((Xv_feat - mean) / scale, omega, b), Yv)
    return {"r2": r.r2, "status": r.r2_status, "ell": ell, "lam": r.lam}


def g1(d: ModelData) -> dict:
    """G1-primary, G1-r2 and the descriptive short-context comparators."""
    h, t = d.acts["resid_post_1"], d.targets
    out = {"m32": probe(d, h, t["m32"]), "m32_shuffle": shuffled(d, h, t["m32"], "m32")}
    m32c, r2c = t["m32"][d.cal], t["r2"][d.cal]
    var_m32 = float(np.sum(m32c.var(axis=0)))
    var_r2 = float(np.sum(r2c.var(axis=0)))
    out["var_m32"], out["var_r2"] = var_m32, var_r2
    p, s = out["m32"], out["m32_shuffle"]
    if var_m32 <= 1e-12:
        status = "INCONCLUSIVE:M32_ZERO_VARIANCE"
    elif p["r2"] is None:
        status = "INCONCLUSIVE:R2_UNDEFINED_ZERO_VARIANCE"
    elif s["q95"] is None:
        status = "INCONCLUSIVE:SHUFFLE_UNDEFINED"
    else:
        status = "PASS" if p["r2"] >= G1_PRIMARY and p["r2"] > s["q95"] else "FAIL"
    out["status"] = status
    if var_r2 < 0.01 * var_m32 or var_r2 <= 1e-6:
        out["r2_gate"] = "R2_DROPPED_LOW_VARIANCE"
    else:
        out["r2"] = probe(d, h, t["r2"])
        out["r2_shuffle"] = shuffled(d, h, t["r2"], "r2")
        v, q = out["r2"]["r2"], out["r2_shuffle"]["q95"]
        out["r2_gate"] = ("R2_RECOVERABLE" if v is not None and q is not None
                          and v >= G1_R2 and v > q else "R2_NOT_RECOVERABLE")
    m2v, m32v = t["m2"][d.val], t["m32"][d.val]
    out["cmp_direct_m2"] = r2_pooled(m2v, m32v, m32c.mean(axis=0))
    out["cmp_direct_m1"] = r2_pooled(t["m1"][d.val], m32v, m32c.mean(axis=0))
    out["cmp_affine_m2"] = probe(d, t["m2"], t["m32"])
    out["cmp_affine_m1"] = probe(d, t["m1"], t["m32"])
    out["cmp_m2_plus_h"] = probe(d, np.hstack([t["m2"], h]), t["m32"])
    out["desc_embed"] = probe(d, d.acts["embed"], t["m32"])
    out["desc_resid_post_3"] = probe(d, d.acts["resid_post_3"], t["m32"])
    return out


def weights_hash(model: torch.nn.Module) -> str:
    h = hashlib.sha256()
    for name, p in sorted(model.state_dict().items()):
        h.update(name.encode())
        h.update(p.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def _softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


class ValForward:
    """Frozen model on the validation inputs: base logits, captured hooks, patched runs."""

    def __init__(self, model, d: ModelData):
        self.model = model
        self.inputs = torch.as_tensor(d.inputs[d.val])
        with torch.no_grad():
            out = model(self.inputs, return_hooks=["resid_post_1", "resid_post_3"])
        self.logits = out.logits
        self.h = out.hooks["resid_post_1"][:, INDEX, :]
        self.z3 = out.hooks["resid_post_3"][:, INDEX, :].double().numpy()
        self.p = _softmax(self.logits[:, INDEX, :].double().numpy())

    def patch(self, site: str, repl: np.ndarray):
        return forward_with_patch(self.model, self.inputs, site, INDEX,
                                  torch.as_tensor(repl, dtype=torch.float32)).logits

    def kl(self, logits_I) -> tuple[float | None, str]:
        vals, status = kl_rows(self.p, _softmax(logits_I[:, INDEX, :].double().numpy()))
        return (None if vals is None else float(vals.mean())), status


def final_null(vf: ValForward, model) -> dict:
    """u-space effective-null projection, y' = u' diag(gamma) + beta, float64 algebra."""
    gamma = model.ln_final.weight.detach().double().numpy()
    beta = model.ln_final.bias.detach().double().numpy()
    W_U = model.unembed.weight.detach().double().numpy()
    V = W_U.shape[0]
    P = readout_projector(gamma, (np.eye(V) - np.ones((V, V)) / V) @ W_U)
    if np.trace(P) < 0.5:
        return {"status": "READOUT_DEGENERATE"}
    z = vf.z3
    u = (z - z.mean(axis=1, keepdims=True)) / np.sqrt(z.var(axis=1, keepdims=True) + 1e-5)
    y, y_null = u * gamma + beta, (u @ P) * gamma + beta
    c = lambda L: L - L.mean(axis=1, keepdims=True)  # noqa: E731
    diff = float(np.max(np.abs(c(y_null @ W_U.T) - c(y @ W_U.T))))
    run = vf.patch("ln_final_out", y_null)[:, INDEX, :].double().numpy()
    return {"status": "ok", "centred_diff_f64": diff, "rank_P": float(np.trace(P)),
            "centred_diff_adapter_f32": float(np.max(np.abs(c(run) - c(y @ W_U.T))))}


def g2(d: ModelData, model, vf: ValForward, primary) -> dict:
    """Identity, causality (primary eraser), final-null and frozen-weight checks."""
    before = weights_hash(model)
    h_ext = d.acts["resid_post_1"][d.val]
    out = {"capture_vs_extracted": float(np.max(np.abs(vf.h.double().numpy() - h_ext)))}
    ident = vf.patch("resid_post_1", vf.h.numpy())
    out["identity_index32"] = float((ident[:, INDEX] - vf.logits[:, INDEX]).abs().max())
    out["identity_before32"] = float((ident[:, :INDEX] - vf.logits[:, :INDEX]).abs().max())
    out["identity_kl"], kl_status = vf.kl(ident)
    if primary.status == "ok":
        er = vf.patch("resid_post_1", apply_map(h_ext, primary.mu, primary.M))
        out["primary_before32"] = float((er[:, :INDEX] - vf.logits[:, :INDEX]).abs().max())
    out["final_null"] = final_null(vf, model)
    out["weights_unchanged"] = weights_hash(model) == before
    if out["final_null"]["status"] != "ok" or kl_status != "ok" or primary.status != "ok":
        out["status"] = "INCONCLUSIVE:" + (out["final_null"]["status"] if
                                           out["final_null"]["status"] != "ok" else
                                           kl_status if kl_status != "ok" else primary.status)
        return out
    ok = (out["identity_index32"] <= 1e-5 and out["identity_before32"] <= 1e-7
          and out["primary_before32"] <= 1e-7 and out["final_null"]["centred_diff_f64"] <= 1e-8
          and out["weights_unchanged"])
    out["status"] = "PASS" if ok else "FAIL"
    return out


def control_targets(d: ModelData) -> dict[str, np.ndarray]:
    """Calibration-fitted control targets over all rows (PCs fitted on calibration only)."""
    t = d.targets
    perm = gen("shuffle_eraser", d.seed).permutation(int(d.cal.sum()))
    shuf = t["m32"].copy()
    shuf[np.flatnonzero(d.cal)] = t["m32"][d.cal][perm]
    pcs = {k: pc_scores(t[src], leading_components(t[src][d.cal], 2))
           for k, src in (("R1", "onehot_w32"), ("local", "local"), ("generic", "Q1"))}
    return {"shuffled_m32": shuf, "m2": t["m2"], **pcs}
