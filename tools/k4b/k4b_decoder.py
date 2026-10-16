"""K4b descriptive suffix decoder (API.md §5; protocol §9.4, §5.6 R13 tolerance).

One-hot canonical w29..w32 (position-major) -> saved standardisation -> random Fourier features
-> nested ridge over five panels -> (cos phi, sin phi). Never gating; no fallback family.
"""

from __future__ import annotations

import k4b_config  # noqa: F401  (sys.path)
import k4b_scores
import numpy as np
from k4b_config import SCOPE

from topo_pilot.analysis.x4f_scores import rbf_bandwidth, rbf_features, rbf_map, standardizer
from topo_pilot.contracts import SeedTree
from topo_pilot.experiment.x4f_probe import nested_ridge
from topo_pilot.prediction.ridge import RidgeProbe

GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)
N_FEATURES, N_SUB = 2048, 1024
SAVED = ("lam", "ell", "mu_in", "s_in", "Omega", "b", "mean_F", "scale_F", "W", "bias",
         "equivalence", "eq_tol", "kappa")


def one_hot_suffix(canon32) -> np.ndarray:
    c = np.asarray(canon32, dtype=np.int64)[:, 28:32]
    X = np.zeros((c.shape[0], 144), dtype=np.float64)
    for p in range(4):
        X[np.arange(c.shape[0]), 36 * p + c[:, p]] = 1.0
    return X


def equivalence_tolerance(Ft, lam, pred) -> tuple:
    """R13 formula: tol = max(1e-10, 64 eps kappa max|pred|), kappa of Xc'Xc + lam I."""
    Ft = np.asarray(Ft, dtype=np.float64)
    Xc = Ft - Ft.mean(axis=0)
    ev = np.linalg.eigvalsh(Xc.T @ Xc + float(lam) * np.eye(Xc.shape[1]))
    kappa = float(ev[-1] / ev[0]) if ev[0] > 0 else float("inf")
    tol = max(1e-10, 64.0 * float(np.finfo(np.float64).eps) * kappa
              * float(np.max(np.abs(pred))))
    return tol, kappa


def _unavailable(reason, **extra) -> dict:
    return dict({"status": "UNAVAILABLE", "reason": reason}, **extra)


def fit(canon32, seq_ids, phi, model) -> dict:
    """Fit on the 2,560 non-landmark cal rows the caller passes (panels by id rank // 512)."""
    X = one_hot_suffix(canon32)
    mu_in, s_in = standardizer(X)
    Xs = (X - mu_in) / s_in
    ell, status = rbf_bandwidth(Xs, SeedTree(0).generator(SCOPE, "suffix_rbf_bw", int(model)),
                                N_SUB)
    if status != "ok" or ell is None or not np.isfinite(ell) or ell <= 0:
        return _unavailable("degenerate bandwidth", ell=ell)
    Omega, b = rbf_map(144, N_FEATURES, ell, SeedTree(0).generator(SCOPE, "suffix_rbf",
                                                                   int(model)))
    F = rbf_features(Xs, Omega, b)
    phi = np.asarray(phi, dtype=np.float64)
    Y = np.column_stack([np.cos(phi), np.sin(phi)])
    ids = np.asarray(seq_ids, dtype=np.int64)
    rank = np.empty(len(ids), dtype=np.int64)
    rank[np.argsort(ids, kind="stable")] = np.arange(len(ids))
    panels = rank // 512
    res = nested_ridge(F, Y, panels, F, Y, GRID)
    mean_F, scale_F = standardizer(F)
    Ft = (F - mean_F) / scale_F
    probe = RidgeProbe([res.lam]).fit(Ft, Y, Ft, Y)
    pred = probe.predict(Ft)
    equivalence = float(np.max(np.abs(pred - np.asarray(res.pred_val))))
    eq_tol, kappa = equivalence_tolerance(Ft, res.lam, pred)
    dec = {"status": "AVAILABLE", "reason": "", "lam": float(res.lam), "ell": float(ell),
           "mu_in": mu_in, "s_in": s_in, "Omega": Omega, "b": b, "mean_F": mean_F,
           "scale_F": scale_F, "W": probe.W, "bias": probe.b, "equivalence": equivalence,
           "eq_tol": eq_tol, "kappa": kappa}
    if equivalence > eq_tol:
        dec.update(status="UNAVAILABLE", reason="equivalence")
    return dec


def predict_phase(dec, canon32) -> np.ndarray:
    if dec.get("status") != "AVAILABLE":
        raise ValueError(f"decoder unavailable: {dec.get('reason')}")
    Xs = (one_hot_suffix(canon32) - dec["mu_in"]) / dec["s_in"]
    Ft = (rbf_features(Xs, dec["Omega"], dec["b"]) - dec["mean_F"]) / dec["scale_F"]
    return k4b_scores.vector_phase(Ft @ dec["W"] + dec["bias"])


def agreement(phi, psi, supported) -> float:
    sup = np.asarray(supported, dtype=bool)
    d = np.asarray(phi, dtype=np.float64)[sup] - np.asarray(psi, dtype=np.float64)[sup]
    return float(np.abs(np.mean(np.exp(1j * d)))) if d.size else float("nan")


def to_arrays(dec) -> dict:
    out = {"status": np.array(dec["status"]), "reason": np.array(dec.get("reason", ""))}
    for k in SAVED:
        if dec.get(k) is not None:
            out[k] = np.asarray(dec[k])
    return out


def from_arrays(a) -> dict:
    dec = {"status": str(a["status"]), "reason": str(a["reason"])}
    for k in SAVED:
        if k in a:
            v = np.asarray(a[k])
            dec[k] = float(v) if v.ndim == 0 else v
    return dec
