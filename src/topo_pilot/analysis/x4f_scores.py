"""X4-F scores, RBF features, support diagnostics and gate verdict (x4f-exec-v2 §4, §8–§11)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import cdist, pdist

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.x4f_scores"
_ZERO = 1e-12
GATES = ("G1", "G2", "G3", "G4", "G5")


def standardizer(X_fit: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Fit-row mean and population std; columns with std <= 1e-12 get scale 1 (centred only)."""
    X = np.asarray(X_fit, dtype=np.float64)
    sd = X.std(axis=0)
    return X.mean(axis=0), np.where(sd <= _ZERO, 1.0, sd)


def r2_pooled(Y_pred: NDArray, Y_val: NDArray, mean_cal: NDArray) -> tuple[float | None, str]:
    """``1 - SSE / SST`` pooled over coordinates, SST around the calibration mean.

    ``SST <= 1e-12 n q`` gives ``(None, "R2_UNDEFINED_ZERO_VARIANCE")``.
    """
    Y = np.asarray(Y_val, dtype=np.float64)
    P = np.asarray(Y_pred, dtype=np.float64)
    Y2, P2 = Y.reshape(Y.shape[0], -1), P.reshape(P.shape[0], -1)
    sst = float(np.sum((Y2 - np.asarray(mean_cal, float).reshape(1, -1)) ** 2))
    if not sst > _ZERO * Y2.shape[0] * Y2.shape[1]:
        return None, "R2_UNDEFINED_ZERO_VARIANCE"
    return 1.0 - float(np.sum((Y2 - P2) ** 2)) / sst, "ok"


def kl_rows(P: NDArray, Q: NDArray) -> tuple[NDArray[np.float64] | None, str]:
    """``KL(P_i || Q_i)`` in nats per row; ``P = 0`` terms are 0; ``Q = 0 < P`` -> KL_UNDEFINED.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on shape mismatch.
    """
    p, q = np.asarray(P, dtype=np.float64), np.asarray(Q, dtype=np.float64)
    if p.shape != q.shape:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "kl_shapes",
                           f"{p.shape} vs {q.shape}")
    pos = p > 0
    if np.any(pos & (q <= 0)):
        return None, "KL_UNDEFINED"
    terms = np.zeros_like(p)
    terms[pos] = p[pos] * (np.log(p[pos]) - np.log(q[pos]))
    return terms.sum(axis=-1), "ok"


def rbf_bandwidth(X_std_cal: NDArray, rng: np.random.Generator,
                  n_sub: int = 1024) -> tuple[float | None, str]:
    """Median pairwise distance among ``min(n_sub, n)`` rows drawn without replacement."""
    X = np.asarray(X_std_cal, dtype=np.float64)
    idx = rng.choice(X.shape[0], min(n_sub, X.shape[0]), replace=False)
    ell = float(np.median(pdist(X[idx]))) if idx.size > 1 else 0.0
    return (None, "RBF_DEGENERATE") if ell <= _ZERO else (ell, "ok")


def rbf_map(d: int, n_features: int, ell: float,
            rng: np.random.Generator) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """``Omega = N(0,1)^{d x F} / ell`` (drawn first), then ``b ~ U[0, 2 pi)^F``."""
    omega = rng.standard_normal((d, n_features)) / ell
    return omega, rng.uniform(0.0, 2.0 * np.pi, n_features)


def rbf_features(X_std: NDArray, Omega: NDArray, b: NDArray) -> NDArray[np.float64]:
    """Random Fourier features ``sqrt(2/F) cos(X Omega + b)``."""
    return np.sqrt(2.0 / Omega.shape[1]) * np.cos(np.asarray(X_std, float) @ Omega + b)


def ledoit_wolf(X: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ledoit-Wolf (2004) shrinkage of the population covariance toward ``mu_tr I``."""
    A = np.asarray(X, dtype=np.float64)
    n, d = A.shape
    Xc = A - A.mean(axis=0)
    S = Xc.T @ Xc / n
    m = np.trace(S) / d
    F = m * np.eye(d)
    d2 = float(np.sum((S - F) ** 2))
    b2 = float(np.sum([np.sum((np.outer(x, x) - S) ** 2) for x in Xc]) / n ** 2)
    shrink = 0.0 if d2 <= 0 else min(b2, d2) / d2
    return A.mean(axis=0), shrink * F + (1.0 - shrink) * S


def _mahalanobis(X: NDArray, mu: NDArray, prec: NDArray) -> NDArray[np.float64]:
    D = np.asarray(X, float) - mu
    return np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", D, prec, D), 0.0))


def _knn_mean(X: NDArray, ref: NDArray, k: int = 10) -> NDArray[np.float64]:
    dist = cdist(np.asarray(X, float), np.asarray(ref, float))
    return np.sort(dist, axis=1)[:, :k].mean(axis=1)


def support_report(X_cal: NDArray, X_val: NDArray, patched: dict[str, NDArray]) -> dict:
    """Mahalanobis support of patched vectors against the calibration Ledoit-Wolf law.

    Returns ``status``, ``q99_cal``, ``frac_unpatched_val``, ``frac[name]`` (share beyond
    q99_cal) and ``knn_ratio[name]`` (median 10-NN mean distance to calibration, patched over
    unpatched validation; ``"RATIO_UNDEFINED"`` for a zero denominator).
    """
    mu, cov = ledoit_wolf(X_cal)
    eig = np.linalg.eigvalsh(cov)
    if eig.min() <= _ZERO * eig.max():
        return {"status": "SUPPORT_DEGENERATE"}
    prec = np.linalg.inv(cov)
    q99 = float(np.quantile(_mahalanobis(X_cal, mu, prec), 0.99))
    base = float(np.median(_knn_mean(X_val, X_cal)))
    out = {"status": "ok", "q99_cal": q99,
           "frac_unpatched_val": float(np.mean(_mahalanobis(X_val, mu, prec) > q99)),
           "frac": {}, "knn_ratio": "RATIO_UNDEFINED" if base <= 0 else {}}
    for name, Xp in patched.items():
        out["frac"][name] = float(np.mean(_mahalanobis(Xp, mu, prec) > q99))
        if base > 0:
            out["knn_ratio"][name] = float(np.median(_knn_mean(Xp, X_cal))) / base
    return out


def support_gate(frac_primary: float, fracs_random: list[float]) -> bool:
    """``frac_primary <= 0.05`` and ``<= 2 * median(fracs_random)`` (literal at median 0)."""
    return frac_primary <= 0.05 and frac_primary <= 2.0 * float(np.median(fracs_random))


def gate_verdict(per_model: dict[int, dict[str, str]]) -> tuple[str, str]:
    """FEASIBLE iff every gate PASS in every model; NOT_FEASIBLE iff G1 FAIL in some model;
    otherwise INCONCLUSIVE naming the first non-PASS gate (G1 -> G5) and model."""
    for seed in sorted(per_model):
        if per_model[seed].get("G1") == "FAIL":
            return "NOT_FEASIBLE", f"G1 FAIL in model {seed}"
    for gate in GATES:
        for seed in sorted(per_model):
            status = per_model[seed].get(gate, "NOT_RUN")
            if status != "PASS":
                return "INCONCLUSIVE", f"{gate} {status} in model {seed}"
    return "FEASIBLE", "G1-G5 pass in every model"
