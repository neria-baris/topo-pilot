"""Process-level representation baselines R2 / R3: spectral embedding of the symbol kernel."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.baselines"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def spectral_embedding(E: NDArray[np.float64], T: NDArray[np.float64],
                       pi: NDArray[np.float64], k: int) -> NDArray[np.float64]:
    """Spectral embedding phi of the symbol transition matrix.

    Math
    ----
    ``M = E^T diag(pi) T E`` (symmetrised as ``(M + M^T)/2``), ``D = diag(row sums of M)``,
    ``L = I - D^{-1/2} M D^{-1/2}``. With ``L v_m = lambda_m v_m`` (ascending), the first
    (trivial, lambda = 0) eigenvector is dropped and ``phi[:, m-1] = D^{-1/2} v_m`` for
    ``m = 2..k+1``: the random-walk (generalised) eigenvectors of ``M``.

    Shapes
    ------
    ``E: [N, V]``, ``T: [N, N]``, ``pi: [N]`` -> ``phi: [V, k] float64``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if ``k`` is not in ``1..V-1``; ``NUMERICAL_FAILURE`` for a symbol with
        zero mass.
    """
    M = E.T @ (pi[:, None] * (T @ E))
    M = 0.5 * (M + M.T)
    V = M.shape[0]
    if not 1 <= k <= V - 1:
        raise _fail(ErrorCode.INVALID_CONFIG, "k", f"k={k} must be in 1..{V - 1}")
    deg = M.sum(axis=1)
    if np.any(deg <= 0.0):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "degree", "a symbol has zero mass in M")
    inv_sqrt = 1.0 / np.sqrt(deg)
    L = np.eye(V) - inv_sqrt[:, None] * M * inv_sqrt[None, :]
    _, vecs = np.linalg.eigh(0.5 * (L + L.T))
    return np.ascontiguousarray(inv_sqrt[:, None] * vecs[:, 1:k + 1], dtype=np.float64)


def r2_points(tokens_hist: NDArray, phi: NDArray[np.float64]) -> NDArray[np.float64]:
    """R2 = ``1/2 [phi(w_32) + phi(w_31)]`` for ``tokens_hist: [M, 32]`` -> ``[M, k]``."""
    tok = np.asarray(tokens_hist).astype(np.int64)
    return 0.5 * (phi[tok[:, 31]] + phi[tok[:, 30]])


def r3_points(tokens_hist: NDArray, phi: NDArray[np.float64]) -> NDArray[np.float64]:
    """R3 = ``mean_t phi(w_t)`` over the history tokens -> ``[M, k]``."""
    tok = np.asarray(tokens_hist).astype(np.int64)
    return phi[tok].mean(axis=1)
