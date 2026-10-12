"""Pure summary functions on persistence diagrams."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _bars(diag, dim: int, finite_only: bool = True) -> NDArray[np.float64]:
    rows = np.asarray(getattr(diag, "rows", diag), dtype=np.float64).reshape(-1, 4)
    bars = rows[rows[:, 0] == dim][:, 1:3]
    return bars[np.isfinite(bars[:, 1])] if finite_only else bars


class Summaries:
    """Summaries of a ``DiagramResult`` (or an ``[n, 4]`` rows array); all are pure.

    Math
    ----
    For H_dim bars ``(b, d)``: ``S = max (d - b) / s`` over finite bars (0 if none);
    ``pi_max = max d / b`` over finite bars with ``b > 0`` (0 if none); top-k persistences
    ``d - b`` in decreasing order, zero padded; Betti curve ``beta(t) = #{b <= t < d}``
    (infinite bars count as alive).
    """

    @staticmethod
    def S(diag, dim: int, scale_s: float) -> float:
        """Max finite persistence in ``dim`` divided by ``scale_s``; 0.0 if none or ``s <= 0``."""
        bars = _bars(diag, dim)
        if len(bars) == 0 or not scale_s > 0:
            return 0.0
        return float((bars[:, 1] - bars[:, 0]).max() / scale_s)

    @staticmethod
    def pi_max(diag, dim: int) -> float:
        """Max death/birth over finite bars with birth > 0 (bars born at 0 ignored); 0.0 if none."""
        bars = _bars(diag, dim)
        bars = bars[bars[:, 0] > 0]
        return float((bars[:, 1] / bars[:, 0]).max()) if len(bars) else 0.0

    @staticmethod
    def top_k_persistence(diag, dim: int, k: int = 3) -> NDArray[np.float64]:
        """The ``k`` largest finite persistences in ``dim``, decreasing, zero padded to ``[k]``."""
        bars = _bars(diag, dim)
        pers = np.sort(bars[:, 1] - bars[:, 0])[::-1][:k]
        return np.concatenate([pers, np.zeros(k - len(pers))]).astype(np.float64)

    @staticmethod
    def betti_curve(diag, dim: int, grid: NDArray[np.float64]) -> NDArray[np.float64]:
        """Number of ``dim``-bars alive at each ``t`` in ``grid`` (birth <= t < death), float64."""
        bars = _bars(diag, dim, finite_only=False)
        t = np.asarray(grid, dtype=np.float64)[:, None]
        return ((bars[None, :, 0] <= t) & (t < bars[None, :, 1])).sum(axis=1).astype(np.float64)
