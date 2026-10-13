"""Horizon feasibility (part e, X4 Phase B): tangent-kernel audit of Q2 versus Q1.

Pure linear algebra on numeric future maps; no store, oracle or fitting. Row-vector convention:
a belief ``b [N]`` gives ``Q1 = b G1 [V]`` and the joint ``Q2 = b G2 [V*V]`` (index ``i*V + j``).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.horizon"
TOLERANCES = (1e-8, 1e-10, 1e-12)
ALLOW_FLOOR = 1e-6
FACTOR_CEILING = 1e-10
AMPLIFICATION_CAP = 1e3
CERTIFICATE_MARGIN = 1e-6
ZERO_FLOOR = 1e-12


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def helmert_basis(n: int) -> NDArray[np.float64]:
    """Orthonormal basis ``B [n, n-1]`` of the sum-zero subspace ``{v : sum(v) = 0}``.

    Math
    ----
    Column ``k`` (1-based) is ``(1, ..., 1, -k, 0, ..., 0) / sqrt(k (k + 1))`` with ``k`` ones,
    so ``B^T B = I`` and ``1^T B = 0`` exactly in real arithmetic.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if ``n < 2``.
    """
    if n < 2:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "helmert_n", f"n={n} < 2")
    B = np.zeros((n, n - 1))
    for k in range(1, n):
        B[:k, k - 1] = 1.0
        B[k, k - 1] = -float(k)
        B[:, k - 1] /= np.sqrt(k * (k + 1.0))
    return B


def joint_marginals(Q2: NDArray, V: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """First- and second-symbol marginals of a lexicographic joint ``Q2 [R, V*V]``.

    Math
    ----
    ``first[r, i] = sum_j Q2[r, i*V + j]`` (equals Q1); ``second[r, j] = sum_i Q2[r, i*V + j]``
    (equals ``b T^2 E``, not Q1).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if the width is not ``V*V``.
    """
    arr = np.asarray(Q2, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] != V * V:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "joint_width", f"shape {arr.shape}, V={V}")
    cube = arr.reshape(arr.shape[0], V, V)
    return cube.sum(axis=2), cube.sum(axis=1)


def hellinger(P: NDArray, Q: NDArray) -> NDArray[np.float64]:
    """Row-wise Hellinger distance ``||sqrt(p) - sqrt(q)||_2 / sqrt(2)`` in ``[0, 1]``.

    Entries in ``[-1e-14, 0)`` are treated as 0; anything more negative raises.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on shape mismatch; ``NUMERICAL_FAILURE`` on entries below -1e-14.
    """
    p, q = np.asarray(P, dtype=np.float64), np.asarray(Q, dtype=np.float64)
    if p.shape != q.shape:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "hellinger_shapes", f"{p.shape} vs {q.shape}")
    return np.linalg.norm(safe_sqrt(p) - safe_sqrt(q), axis=-1) / np.sqrt(2.0)


def safe_sqrt(P: NDArray) -> NDArray[np.float64]:
    """``sqrt(max(P, 0))`` after checking that no entry is below ``-1e-14``."""
    arr = np.asarray(P, dtype=np.float64)
    if arr.size and float(arr.min()) < -1e-14:
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "negative_probability", f"min {arr.min():.3e}")
    return np.sqrt(np.clip(arr, 0.0, None))


@dataclass(frozen=True)
class ToleranceRow:
    """Tangent audit at one relative tolerance ``tau`` (see :func:`tangent_audit`)."""

    tau: float
    rank_H: int
    null_dim: int
    null_residual: float
    rank_G2: int
    D_singular_values: tuple[float, ...]
    rho: float
    conditioning: float
    gap: float | None
    amplification: float


@dataclass(frozen=True)
class TangentAudit:
    """Ambient tangent-kernel audit; ``verdict`` in ALLOWS_STABLE / FACTORIZES /
    TOLERANCE_DEPENDENT; ``factor_conditioned`` only meaningful for FACTORIZES."""

    H_singular_values: tuple[float, ...]
    G2_singular_values: tuple[float, ...]
    basis_orthonormality: float
    basis_sum: float
    certificate_ratio: float | None
    certificate: bool
    rows: tuple[ToleranceRow, ...]
    verdict: str
    factor_conditioned: bool


def _row(U: NDArray, s: NDArray, H: NDArray, G2t: NDArray, s2: NDArray, tau: float) -> ToleranceRow:
    r = int(np.sum(s > tau * s[0])) if s.size and s[0] > 0 else 0
    U0 = U[:, r:]
    D = U0.T @ G2t
    dsv = np.linalg.svd(D, compute_uv=False) if D.size else np.zeros(0)
    top2 = float(s2[0]) if s2.size else 0.0
    rho = float(dsv[0] / top2) if dsv.size and top2 > 0 else 0.0
    pinv = np.linalg.pinv(H, rcond=tau) if r else np.zeros(H.T.shape)
    return ToleranceRow(
        tau=tau, rank_H=r, null_dim=int(U0.shape[1]),
        null_residual=float(np.linalg.norm(U0.T @ H, 2)) if U0.size else 0.0,
        rank_G2=int(np.sum(s2 > tau * top2)) if top2 > 0 else 0,
        D_singular_values=tuple(float(x) for x in dsv), rho=rho,
        conditioning=float(s[0] / s[r - 1]) if r else float("inf"),
        gap=float(s[r - 1] / s[r]) if 0 < r < s.size and s[r] > 0 else None,
        amplification=float(np.linalg.norm(pinv @ G2t, 2)) if r else 0.0)


def tangent_audit(G1: NDArray, G2: NDArray,
                  tolerances: tuple[float, ...] = TOLERANCES) -> TangentAudit:
    """Does ``G2`` vanish on the sum-zero kernel of ``G1``?

    Math
    ----
    ``B`` = Helmert basis, ``H = B^T G1``, full SVD ``H = U S V^T``. At relative tolerance ``tau``
    ``U0`` holds the left singular vectors past rank ``r_tau = #{s_i > tau s_1}``, spanning
    ``ker(H^T)``; ``D = U0^T B^T G2``; ``rho = sigma_max(D) / sigma_max(B^T G2)``. ALLOWS_STABLE
    iff ``rho >= 1e-6`` at every tau; FACTORIZES iff ``rho <= 1e-10`` at every tau (conditioned
    iff the amplification ``||H^+ B^T G2||_2 <= 1e3``); else TOLERANCE_DEPENDENT. Certificate:
    rows of G1 sum to 1, so ``rank(H) <= V - 1``; ``sigma_V(B^T G2)/sigma_1 >= 1e-6`` proves
    ``rank(B^T G2) > rank(H)``, hence no factorization. A tangent map whose largest singular
    value is at most ``1e-12`` times the ambient map's norm is treated as exactly zero.

    Shapes
    ------
    ``G1: [N, V]``, ``G2: [N, W]`` (``W = V*V`` for the joint).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` for mismatched rows; ``NUMERICAL_FAILURE`` for non-finite input.
    """
    g1, g2 = np.asarray(G1, dtype=np.float64), np.asarray(G2, dtype=np.float64)
    if g1.ndim != 2 or g2.ndim != 2 or g1.shape[0] != g2.shape[0]:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "maps_shape", f"{g1.shape} vs {g2.shape}")
    if not (np.all(np.isfinite(g1)) and np.all(np.isfinite(g2))):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "maps_finite", "non-finite future map")
    B = helmert_basis(g1.shape[0])
    H, G2t = B.T @ g1, B.T @ g2
    U, s, _ = np.linalg.svd(H, full_matrices=True)
    s2 = np.linalg.svd(G2t, compute_uv=False)
    # degenerate guard: a tangent map below ZERO_FLOOR x its ambient norm is exactly zero
    # (a relative tolerance is undefined for a zero matrix, where it would rank rounding noise)
    if s.size and s[0] <= ZERO_FLOOR * np.linalg.norm(g1, 2):
        s = np.zeros_like(s)
    if s2.size and s2[0] <= ZERO_FLOOR * np.linalg.norm(g2, 2):
        s2, G2t = np.zeros_like(s2), np.zeros_like(G2t)
    rows = tuple(_row(U, s, H, G2t, s2, tau) for tau in tolerances)
    V = g1.shape[1]
    cert = float(s2[V - 1] / s2[0]) if s2.size >= V and s2[0] > 0 else None
    if all(r.rho >= ALLOW_FLOOR for r in rows):
        verdict = "ALLOWS_STABLE"
    elif all(r.rho <= FACTOR_CEILING for r in rows):
        verdict = "FACTORIZES"
    else:
        verdict = "TOLERANCE_DEPENDENT"
    return TangentAudit(
        H_singular_values=tuple(float(x) for x in s),
        G2_singular_values=tuple(float(x) for x in s2),
        basis_orthonormality=float(np.max(np.abs(B.T @ B - np.eye(B.shape[1])))),
        basis_sum=float(np.max(np.abs(B.sum(axis=0)))),
        certificate_ratio=cert, certificate=cert is not None and cert >= CERTIFICATE_MARGIN,
        rows=rows, verdict=verdict,
        factor_conditioned=all(r.amplification <= AMPLIFICATION_CAP for r in rows))
