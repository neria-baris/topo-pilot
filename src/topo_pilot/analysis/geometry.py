"""GeometryAlignment: the H2 measure Delta-geom (RESEARCH_SUMMARY 7.5)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.stats import spearmanr

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.GeometryAlignment"
MIN_SAME_PAIRS = 200


def _rho(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    return float(spearmanr(a, b)[0])


class GeometryAlignment:
    """Spearman alignment of activation distances with belief distances.

    Math
    ----
    ``Delta = rho_s(d_A, d_B32) - rho_s(d_A, d_B1)`` over upper-triangle pairs ``i < j``;
    repeated on pairs with ``last_symbol[i] == last_symbol[j]``. Never a significance test.

    Shapes
    ------
    ``D_A, D_B32, D_B1``: ``[M, M]`` distance matrices on the same ordered histories;
    ``last_symbol``: ``[M]`` or None.

    Invariants
    ----------
    Fewer than 200 same-last-symbol pairs (or no ``last_symbol``) gives ``same_last_symbol=None``
    and ``status_same="inconclusive"``. On same-last-symbol pairs ``d_B1`` is identically 0 when
    ``b1`` is the last-symbol posterior ``r_{w32}``; a constant ``d_B1`` there carries no ordering,
    so its term is 0 and ``same_last_symbol = rho_s(d_A, d_B32)`` (D-031). Any other constant
    distance vector gives ``nan`` overall and ``same_last_symbol=None`` (status inconclusive).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on shape mismatch.
    """

    def delta_geom(self, D_A, D_B32, D_B1, last_symbol=None) -> dict:
        """Return ``{"all", "same_last_symbol", "n_same_pairs", "status_same"}``."""
        mats = [np.asarray(m, dtype=np.float64) for m in (D_A, D_B32, D_B1)]
        m = mats[0].shape[0]
        if any(x.shape != (m, m) for x in mats):
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "shapes",
                               f"distance matrices differ in shape: {[x.shape for x in mats]}")
        iu = np.triu_indices(m, k=1)
        dA, d32, d1 = (x[iu] for x in mats)
        out = {"all": _rho(dA, d32) - _rho(dA, d1), "same_last_symbol": None,
               "n_same_pairs": 0, "status_same": "inconclusive"}
        if last_symbol is None:
            return out
        ls = np.asarray(last_symbol)
        if ls.shape != (m,):
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "last_symbol",
                               f"last_symbol shape {ls.shape} for M={m}")
        same = (ls[:, None] == ls[None, :])[iu]
        out["n_same_pairs"] = int(same.sum())
        if out["n_same_pairs"] >= MIN_SAME_PAIRS:
            d1_same = d1[same]
            rho_1 = 0.0 if np.ptp(d1_same) == 0.0 else _rho(dA[same], d1_same)
            value = _rho(dA[same], d32[same]) - rho_1
            if np.isfinite(value):
                out["same_last_symbol"] = value
                out["status_same"] = "ok"
        return out
