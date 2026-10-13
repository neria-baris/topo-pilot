"""Readout-geometry helpers (part d): gauge-free LayerNorm, readout projector, exact split."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

from .pointset import PointSet

_COMPONENT = "analysis.readout"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def _as_f64(a: object, name: str, ndim: int) -> NDArray[np.float64]:
    arr = np.asarray(a, dtype=np.float64)
    if arr.ndim != ndim:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, f"{name}_ndim",
                    f"{name} must be {ndim}-D, got shape {arr.shape}")
    return arr


def _require_finite(arr: NDArray[np.float64], name: str) -> None:
    if not np.all(np.isfinite(arr)):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, f"{name}_finite", f"{name} has non-finite entries")


def ln_gauge_free(Z: NDArray, eps: float = 1e-5) -> NDArray[np.float64]:
    """LayerNorm without its affine part, applied row-wise.

    Math
    ----
    ``u = (z - mean(z)*1) / sqrt(var(z) + eps)`` with the population variance (ddof 0), as in
    ``torch.nn.LayerNorm``.

    Shapes
    ------
    ``Z: [M, d] float64`` (float32 accepted), ``d >= 2`` -> ``U: [M, d] float64``.

    Invariants
    ----------
    Every row of ``U`` has mean 0. ``U(Z + c*1) = U(Z)`` for any per-row shift ``c`` and any
    ``eps``. ``U(alpha*Z) = U(Z)`` for ``alpha > 0`` exactly when ``eps = 0`` (up to ``eps``
    otherwise).

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (``eps < 0``); ``ALIGNMENT_ERROR`` (``Z`` not 2-D, or ``d < 2``);
        ``NUMERICAL_FAILURE`` (non-finite ``Z``, or a zero-variance row with ``eps = 0``).
    """
    if not eps >= 0.0:
        raise _fail(ErrorCode.INVALID_CONFIG, "eps", f"eps must be >= 0, got {eps}")
    z = _as_f64(Z, "Z", 2)
    if z.shape[1] < 2:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "d_min", f"need d >= 2, got shape {z.shape}")
    _require_finite(z, "Z")
    centred = z - z.mean(axis=1, keepdims=True)
    var = np.mean(centred * centred, axis=1, keepdims=True)
    if eps == 0.0 and np.any(var <= 0.0):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "zero_variance",
                    "a row has zero variance and eps = 0")
    return centred / np.sqrt(var + eps)


def readout_projector(gamma: NDArray, W_U: NDArray, rtol: float | None = None
                      ) -> NDArray[np.float64]:
    """Orthogonal projector onto the column space of the readout map ``A``.

    Math
    ----
    ``A = diag(gamma) W_U^T`` in ``R^{d x V}``; thin SVD ``A = Q S R^T``; keep the ``r``
    columns of ``Q`` with ``s_k > tol``, ``tol = rtol * s_max``, default
    ``rtol = max(d, V) * eps_float64`` (the ``numpy.linalg.matrix_rank`` convention);
    ``P = Q_r Q_r^T``. ``A = 0`` gives ``P = 0``.

    Shapes
    ------
    ``gamma: [d]``, ``W_U: [V, d]`` -> ``P: [d, d] float64``.

    Invariants
    ----------
    ``P = P^T``; ``P @ P = P``; ``trace(P) = rank(A)``; ``P A = A``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (shapes); ``NUMERICAL_FAILURE`` (non-finite input);
        ``INVALID_CONFIG`` (``rtol < 0``).
    """
    if rtol is not None and not rtol >= 0.0:
        raise _fail(ErrorCode.INVALID_CONFIG, "rtol", f"rtol must be >= 0, got {rtol}")
    g = _as_f64(gamma, "gamma", 1)
    w = _as_f64(W_U, "W_U", 2)
    d = g.shape[0]
    if w.shape[1] != d:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "shapes",
                    f"gamma has length {d} but W_U has shape {w.shape} (expected [V, {d}])")
    _require_finite(g, "gamma")
    _require_finite(w, "W_U")
    A = g[:, None] * w.T
    Q, s, _ = np.linalg.svd(A, full_matrices=False)
    if rtol is None:
        rtol = max(A.shape) * np.finfo(np.float64).eps
    r = int(np.sum(s > rtol * (s[0] if s.size else 0.0)))
    Qr = Q[:, :r]
    return Qr @ Qr.T


def split_readout(U: NDArray, P: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Split row-vectors into the readout-visible part and the null part.

    Math
    ----
    ``U_visible = U P``, ``U_null = U - U_visible``. With ``logits = u A + beta W_U^T`` and
    ``(I - P) A = 0``, only ``u P`` reaches the logits.

    Shapes
    ------
    ``U: [M, d]``, ``P: [d, d]`` -> two arrays ``[M, d]`` float64.

    Invariants
    ----------
    ``U_visible + U_null = U``; row-wise ``U_visible[i] . U_null[i] = 0`` when ``P`` is an
    orthogonal projector; ``U A`` is unchanged when ``U`` is replaced by ``U_visible``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (``U`` not 2-D, or ``P`` not ``[d, d]`` with ``d = U.shape[1]``).
    """
    u = _as_f64(U, "U", 2)
    p = _as_f64(P, "P", 2)
    if p.shape != (u.shape[1], u.shape[1]):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "shapes",
                    f"U has shape {u.shape} but P has shape {p.shape}")
    visible = u @ p
    return visible, u - visible


def predictive_pointset(logits: NDArray, ids: Sequence[str],
                        space: str = "pred:softmax") -> PointSet:
    """Predictive distributions of a model as a Hellinger point set.

    Math
    ----
    ``p = softmax(logits)`` per row, computed as ``exp(l - max(l)) / sum(...)`` in float64.

    Shapes
    ------
    ``logits: [M, V]``, ``ids``: M strings -> ``PointSet(space, X=p [M, V], D=None,
    ids=list(ids), metric="hellinger")``.

    Invariants
    ----------
    Rows of ``X`` sum to 1 and are non-negative (positive unless exp underflows); adding a
    constant to a logits row changes nothing.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (``logits`` not 2-D, or ``len(ids) != M``); ``NUMERICAL_FAILURE``
        (non-finite logits).
    """
    lg = _as_f64(logits, "logits", 2)
    if len(ids) != lg.shape[0]:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "ids_length",
                    f"{len(ids)} ids for {lg.shape[0]} logits rows")
    _require_finite(lg, "logits")
    e = np.exp(lg - lg.max(axis=1, keepdims=True))
    p = e / e.sum(axis=1, keepdims=True)
    return PointSet(space, p, None, list(ids), "hellinger")
