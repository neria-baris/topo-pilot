"""Pure emission diagnostics and build-time checks (entropies, factorisation, row multiset)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.special import xlogy

from topo_pilot.contracts import ErrorCode

from ._geometry import fail

QUANTILES = (0.0, 0.25, 0.5, 0.75, 1.0)
MIN_SYMBOL_PROB = 1e-4
FACTORIZE_TOL = 1e-12


def row_entropies(E: NDArray[np.float64]) -> NDArray[np.float64]:
    """Natural-log entropy of every row of ``E [N, V]`` -> ``[N]``."""
    return -xlogy(E, E).sum(axis=1)


def factorizes(E_centers: NDArray[np.float64], dims: tuple[int, ...]) -> bool:
    """Numerical product-structure test on ``E`` with columns in center order ``j = a*k + b``.

    Math
    ----
    Reshape to ``E4 [n0, n1, k, k]``; ``Ex[x, a] = sum_{y,b} E4 / n1``,
    ``Ey[y, b] = sum_{x,a} E4 / n0``; True iff ``max |E4 - Ex[x,a] Ey[y,b]| < 1e-12``.
    False when the shape does not admit the reshape (V not a square, chart not 2-d).
    """
    n_states, n_symbols = E_centers.shape
    k = math.isqrt(n_symbols)
    if len(dims) != 2 or k * k != n_symbols or dims[0] * dims[1] != n_states:
        return False
    E4 = E_centers.reshape(dims[0], dims[1], k, k)
    Ex = E4.sum(axis=(1, 3)) / dims[1]
    Ey = E4.sum(axis=(0, 2)) / dims[0]
    recon = np.einsum("xa,yb->xyab", Ex, Ey)
    return bool(np.max(np.abs(E4 - recon)) < FACTORIZE_TOL)


def emission_diagnostics(E: NDArray[np.float64], E_centers: NDArray[np.float64],
                         dims: tuple[int, ...], coverage_radius: float) -> dict[str, Any]:
    """Diagnostics under the uniform state distribution ``pi = 1/N`` (natural log).

    Math
    ----
    ``p_w = pi E``; ``H_W = -sum p_w log p_w``; ``H_W_given_Z = sum_z pi_z H(E[z])``;
    row-entropy quantiles at 0, .25, .5, .75, 1.

    Shapes
    ------
    ``E [N, V]`` public columns; ``E_centers [N, V]`` same matrix in center order (only used
    for ``factorizes``).
    """
    n_states = E.shape[0]
    pi = np.full(n_states, 1.0 / n_states)
    p_w = pi @ E
    h_rows = row_entropies(E)
    return {
        "H_W_given_Z": float(pi @ h_rows),
        "H_W": float(-xlogy(p_w, p_w).sum()),
        "p_w": [float(v) for v in p_w],
        "coverage_radius": float(coverage_radius),
        "row_entropy_quantiles": [float(v) for v in np.quantile(h_rows, QUANTILES)],
        "factorizes": factorizes(E_centers, dims),
    }


def check_symbols_alive(p_w: NDArray[np.float64]) -> None:
    """Require every ``p_w >= 1e-4``.

    Raises
    ------
    StageFailure
        ``INVALID_SIGMA`` with detail ``dead_symbol``.
    """
    if np.any(np.asarray(p_w) < MIN_SYMBOL_PROB):
        raise fail(ErrorCode.INVALID_SIGMA, "dead_symbol", "dead_symbol")


def check_row_multiset(E_source: NDArray[np.float64], E_permuted: NDArray[np.float64]) -> None:
    """Require the rows of ``E_permuted`` to be a permutation of the rows of ``E_source``.

    Raises
    ------
    StageFailure
        ``NONSTOCHASTIC`` (check ``row_multiset``) otherwise.
    """
    same_shape = E_source.shape == E_permuted.shape
    if not same_shape or not np.array_equal(
            E_source[np.lexsort(E_source.T[::-1])], E_permuted[np.lexsort(E_permuted.T[::-1])]):
        raise fail(ErrorCode.NONSTOCHASTIC, "row_multiset",
                   "permuted rows are not a permutation of the source rows")
