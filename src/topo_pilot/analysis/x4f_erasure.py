"""X4-F whitening, oblique linear erasure and matched random families (x4f-exec-v2 §5–§6).

Row convention: histories are rows; a column-action map ``M`` acts on a batch as
``X' = (X - mu) @ M.T + mu``. Population covariances (1/n) throughout.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

OK = "ok"
FEATURES_DEGENERATE = "FEATURES_DEGENERATE"
TARGET_ZERO_VARIANCE = "TARGET_ZERO_VARIANCE"
TARGET_UNCORRELATED = "TARGET_UNCORRELATED"
ERASER_INVALID = "ERASER_INVALID"
ZERO_DISPLACEMENT = "ZERO_DISPLACEMENT"
RANK_EXCEEDS_RETAINED = "RANK_EXCEEDS_RETAINED"
FAMILY_UNMATCHED = "FAMILY_UNMATCHED"
_ZERO = 1e-12


@dataclass(frozen=True, eq=False)
class Whitening:
    """Retained-range whitening: ``W = diag(lam^-1/2) U_keep^T`` ``[k, d]``,
    ``W_pinv = U_keep diag(lam^1/2)`` ``[d, k]``; ``W @ W_pinv = I_k``."""

    mu: NDArray[np.float64]
    U_keep: NDArray[np.float64]
    lam_keep: NDArray[np.float64]
    W: NDArray[np.float64]
    W_pinv: NDArray[np.float64]
    k: int
    status: str


def whiten(X: NDArray, floor: float = 1e-10) -> Whitening:
    """Whitening of ``X [n, d]`` on its retained eigen-range.

    Math
    ----
    ``Sigma = (X - mu)^T (X - mu) / n = U diag(lam) U^T``; keep ``lam_i > floor * lam_max``.
    ``lam_max <= 1e-12`` or ``k = 0`` gives ``FEATURES_DEGENERATE`` (empty arrays, ``k = 0``).
    """
    A = np.asarray(X, dtype=np.float64)
    mu = A.mean(axis=0)
    d = A.shape[1]
    lam, U = np.linalg.eigh((A - mu).T @ (A - mu) / A.shape[0])
    lam_max = float(lam.max()) if lam.size else 0.0
    keep = lam > floor * lam_max if lam_max > _ZERO else np.zeros(d, dtype=bool)
    if not keep.any():
        return Whitening(mu, np.zeros((d, 0)), np.zeros(0), np.zeros((0, d)), np.zeros((d, 0)),
                         0, FEATURES_DEGENERATE)
    U_k, lam_k = U[:, keep], lam[keep]
    return Whitening(mu, U_k, lam_k, (U_k / np.sqrt(lam_k)).T, U_k * np.sqrt(lam_k),
                     int(keep.sum()), OK)


def apply_map(X: NDArray, mu: NDArray, M: NDArray) -> NDArray[np.float64]:
    """``(X - mu) @ M.T + mu`` (column-action map on a batch of rows)."""
    return (np.asarray(X, dtype=np.float64) - mu) @ np.asarray(M).T + mu


def eraser_from_basis(wh: Whitening, Q_s: NDArray) -> tuple[NDArray, NDArray]:
    """``E = W_pinv Q_s Q_s^T W`` and ``M = I - E`` for orthonormal ``Q_s [k, r]``."""
    E = wh.W_pinv @ (Q_s @ Q_s.T) @ wh.W
    return E, np.eye(E.shape[0]) - E


def _rank(A: NDArray, tol: float) -> int:
    s = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(s > tol * s[0])) if s.size and s[0] > 0 else 0


@dataclass(frozen=True, eq=False)
class Eraser:
    """Fitted eraser: ``M, E [d, d]``, ``mu [d]``, lost ``rank``, ``status`` and ``checks``."""

    M: NDArray[np.float64]
    E: NDArray[np.float64]
    mu: NDArray[np.float64]
    rank: int
    status: str
    checks: dict = field(default_factory=dict)


def fit_oblique_eraser(X_cal: NDArray, Z_cal: NDArray, wh: Whitening, rank_tol: float = 1e-8,
                       exact_tol: float = 1e-8, idem_tol: float = 1e-10) -> Eraser:
    """Continuous-target oblique linear eraser on the retained whitening range.

    Math
    ----
    ``G = W Sigma_xz``; ``rho_max = s_max(G) / sqrt(tr Cov Z)``; ``r = #{s > rank_tol s_max}``;
    ``Q_r`` = leading left singular vectors; ``E = W_pinv Q_r Q_r^T W``, ``M = I - E``.
    Checks: idempotence, rank loss = r, exactness ``max|Cov(X', Z)| <= exact_tol max|Sigma_xz|``.

    Shapes
    ------
    ``X_cal [n, d]``, ``Z_cal [n]`` or ``[n, q]``.
    """
    X = np.asarray(X_cal, dtype=np.float64)
    Z = np.asarray(Z_cal, dtype=np.float64).reshape(X.shape[0], -1)
    d = X.shape[1]
    ident = Eraser(np.eye(d), np.zeros((d, d)), wh.mu, 0, wh.status)
    if wh.status != OK:
        return ident
    Zc = Z - Z.mean(axis=0)
    trace_z = float(np.sum(Zc * Zc) / Z.shape[0])
    if trace_z <= _ZERO:
        return Eraser(np.eye(d), np.zeros((d, d)), wh.mu, 0, TARGET_ZERO_VARIANCE)
    S_xz = (X - wh.mu).T @ Zc / X.shape[0]
    U, s, _ = np.linalg.svd(wh.W @ S_xz, full_matrices=False)
    rho = float(s[0] / np.sqrt(trace_z)) if s.size else 0.0
    if rho <= 1e-8:
        return Eraser(np.eye(d), np.zeros((d, d)), wh.mu, 0, TARGET_UNCORRELATED,
                      {"rho_max": rho})
    r = int(np.sum(s > rank_tol * s[0]))
    E, M = eraser_from_basis(wh, U[:, :r])
    Xp = apply_map(X, wh.mu, M)
    resid = (Xp - Xp.mean(axis=0)).T @ Zc / X.shape[0]
    checks = {"rho_max": rho,
              "idempotence": float(np.max(np.abs(M @ M - M))),
              "rank_loss": _rank(E, 1e-8),
              "exactness_ratio": float(np.max(np.abs(resid)) / np.max(np.abs(S_xz))),
              "discarded_residual": float(np.max(np.abs(S_xz - wh.U_keep @ (wh.U_keep.T @ S_xz))))}
    ok = (checks["idempotence"] <= idem_tol * max(1.0, float(np.max(np.abs(M))))
          and checks["rank_loss"] == r and checks["exactness_ratio"] <= exact_tol)
    return Eraser(M, E, wh.mu, r, OK if ok else ERASER_INVALID, checks)


def displacements(X: NDArray, X_prime: NDArray) -> NDArray[np.float64]:
    """Row-wise L2 norms of ``X_prime - X``."""
    return np.linalg.norm(np.asarray(X_prime, dtype=np.float64) - np.asarray(X, float), axis=1)


@dataclass(frozen=True, eq=False)
class Family:
    """Matched random family: accepted draw indices, maps and calibration mean displacements."""

    status: str
    accepted_draws: list[int]
    maps: list[NDArray[np.float64]]
    mean_displacements: list[float]
    target_displacement: float
    n_draws: int
    n_degenerate_draws: int


def random_family(X_cal: NDArray, wh: Whitening, rank: int, target_mean_disp: float,
                  rng_for: Callable[[int], np.random.Generator], n_accept: int = 20,
                  max_draws: int = 10_000, tol: float = 0.05) -> Family:
    """Random rank-``rank`` erasers in the retained range, matched in mean displacement.

    Math
    ----
    Draw ``G_j ~ N(0, 1)^{k x r}``, ``Q, R = qr(G_j)`` (rejected if ``min|diag R| <= 1e-12
    max|diag R|``), ``E_j = W_pinv Q Q^T W``; accept iff ``|D_j - D_t| <= tol D_t`` with
    ``D = mean_i ||x'_i - x_i||``.
    """
    X = np.asarray(X_cal, dtype=np.float64)
    scale = float(np.mean(np.linalg.norm(X - X.mean(axis=0), axis=1)))

    def done(status: str, acc=(), maps=(), disp=(), n=0, deg=0) -> Family:
        return Family(status, list(acc), list(maps), list(disp), float(target_mean_disp), n, deg)

    if not target_mean_disp > _ZERO * scale:
        return done(ZERO_DISPLACEMENT)
    if wh.status != OK:
        return done(wh.status)
    if not 1 <= rank <= wh.k:
        return done(RANK_EXCEEDS_RETAINED)
    acc, maps, disp, deg, j = [], [], [], 0, 0
    for j in range(max_draws):
        Q, R = np.linalg.qr(rng_for(j).standard_normal((wh.k, rank)))
        diag = np.abs(np.diag(R))
        if diag.min() <= _ZERO * diag.max():
            deg += 1
            continue
        _, M = eraser_from_basis(wh, Q)
        D = float(np.mean(displacements(X, apply_map(X, wh.mu, M))))
        if abs(D - target_mean_disp) <= tol * target_mean_disp:
            acc.append(j)
            maps.append(M)
            disp.append(D)
            if len(acc) == n_accept:
                return done(OK, acc, maps, disp, j + 1, deg)
    return done(FAMILY_UNMATCHED, acc, maps, disp, max_draws, deg)


def mismatch_report(d_target: NDArray, d_other: NDArray, scale: float) -> dict:
    """Quantiles of ``d_other`` and per-history ratio ``|d_other - d_t| / d_t`` (rows with
    ``d_t <= 1e-12 scale`` excluded and counted)."""
    dt, do = np.asarray(d_target, float), np.asarray(d_other, float)
    keep = dt > _ZERO * scale
    ratio = np.abs(do[keep] - dt[keep]) / dt[keep]
    q = np.quantile(do, [0.1, 0.5, 0.9]) if do.size else [None] * 3
    return {"q10": float(q[0]), "q50": float(q[1]), "q90": float(q[2]),
            "mismatch_median": float(np.median(ratio)) if ratio.size else None,
            "mismatch_q90": float(np.quantile(ratio, 0.9)) if ratio.size else None,
            "n_excluded": int((~keep).sum())}
