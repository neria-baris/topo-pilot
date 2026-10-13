"""Futures, observability and context gain (pure kernels)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode

from ._common import as_model, check_rows_sum_to_one, fail

_BELIEF_TOL = 1e-10


class FutureOperator:
    """Exact one- and two-step futures from a belief ``b`` and the observability spectrum.

    Math
    ----
    ``F1 = b T E``; ``F2[i, j] = b T diag(E[:, i]) T E[:, j]`` (joint law of the next two symbols).
    Strings: ``G_1 = T E``; ``G_j = [T diag(E[:, s]) G_{j-1}]_s`` (columns blocked by first
    symbol), so ``b G_j`` lists ``P(next j symbols = s)``. ``O_k`` stacks ``G_j^T`` for ``j <= k``.

    Shapes
    ------
    ``b: [R, N]`` rows sum to 1; ``F1: [R, V]``; ``F2: [R, V, V]``; ``O_k: [sum_j V^j, N]``.

    Raises
    ------
    StageFailure
        ``NUMERICAL_FAILURE`` if a belief row or an output does not sum to 1 within 1e-10;
        ``ALIGNMENT_ERROR`` for wrong belief width or ``k_max < 1``.
    """

    def __init__(self, T: np.ndarray, E: np.ndarray) -> None:
        self.T, self.E, _ = as_model(T, E, None)
        self.TE = self.T @ self.E

    def _beliefs(self, b: np.ndarray) -> NDArray[np.float64]:
        arr = np.asarray(b, dtype=np.float64)
        if arr.ndim != 2 or arr.shape[1] != self.T.shape[0]:
            raise fail(ErrorCode.ALIGNMENT_ERROR, "belief_shape", f"b has shape {arr.shape}")
        if not np.all(np.isfinite(arr)) or np.any(np.abs(arr.sum(1) - 1.0) > _BELIEF_TOL):
            raise fail(ErrorCode.NUMERICAL_FAILURE, "belief_sums", "belief rows not normalised")
        return arr

    def F1(self, b: np.ndarray) -> NDArray[np.float64]:
        """Next-symbol law ``b T E``, ``[R, V]``."""
        out = self._beliefs(b) @ self.TE
        check_rows_sum_to_one(out, "F1_sums")
        return out

    def F2(self, b: np.ndarray) -> NDArray[np.float64]:
        """Two-step joint ``F2[r, i, j] = b T diag(E[:, i]) T E[:, j]``, ``[R, V, V]``."""
        beliefs = self._beliefs(b)
        out = np.einsum("rm,mi,mj->rij", beliefs @ self.T, self.E, self.TE, optimize=True)
        check_rows_sum_to_one(out.reshape(out.shape[0], -1), "F2_sums")
        if np.max(np.abs(out.sum(axis=2) - beliefs @ self.TE), initial=0.0) > 1e-12:
            raise fail(ErrorCode.NUMERICAL_FAILURE, "F2_marginal", "sum_j F2 differs from F1")
        return out

    def observability_matrices(self, k_max: int) -> list[NDArray[np.float64]]:
        """``[O_1, ..., O_{k_max}]``; ``O_k`` has rows = strings of length ``<= k``, cols = N."""
        if k_max < 1:
            raise fail(ErrorCode.ALIGNMENT_ERROR, "k_max", "k_max must be >= 1")
        g = self.TE
        blocks = [g.T]
        out = [np.vstack(blocks)]
        for _ in range(2, k_max + 1):
            g = np.hstack([self.T @ (self.E[:, [s]] * g) for s in range(self.E.shape[1])])
            blocks.append(g.T)
            out.append(np.vstack(blocks))
        return out

    def observability_singular_values(self, k_max: int = 3) -> list[NDArray[np.float64]]:
        """Singular values of ``O_k`` (descending, unthresholded) for ``k = 1..k_max``."""
        return [np.linalg.svd(o, compute_uv=False) for o in self.observability_matrices(k_max)]


def context_gain(q_C: np.ndarray, q_last: np.ndarray) -> float:
    """Mean over rows of ``KL(q_C || q_last)`` in nats.

    Math
    ----
    ``G_C = mean_r sum_v q_C[r,v] (log q_C[r,v] - log q_last[r,v])``; terms with ``q_C = 0`` are 0.

    Shapes
    ------
    ``q_C, q_last: [R, V]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on shape mismatch; ``NUMERICAL_FAILURE`` if ``q_last = 0`` where
        ``q_C > 0`` or inputs are non-finite.
    """
    p, r = np.asarray(q_C, dtype=np.float64), np.asarray(q_last, dtype=np.float64)
    if p.shape != r.shape or p.ndim != 2 or p.shape[0] == 0:
        raise fail(ErrorCode.ALIGNMENT_ERROR, "gain_shapes", f"{p.shape} vs {r.shape}")
    if not (np.all(np.isfinite(p)) and np.all(np.isfinite(r))):
        raise fail(ErrorCode.NUMERICAL_FAILURE, "gain_finite", "non-finite predictive")
    support = p > 0
    if np.any(r[support] <= 0):
        raise fail(ErrorCode.NUMERICAL_FAILURE, "gain_support", "q_last = 0 where q_C > 0")
    terms = np.zeros_like(p)
    terms[support] = p[support] * (np.log(p[support]) - np.log(r[support]))
    return float(terms.sum(axis=1).mean())
