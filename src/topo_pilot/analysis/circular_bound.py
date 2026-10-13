"""Symbol-only optimistic bound for circular agreement (circ-audit-v1, privileged_eval).

The bound is computed in-sample from latent angles: it is an evaluation ceiling for every angle
that depends on the last symbol alone, not a held-out predictor.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.circular_bound"


def symbol_only_bound(theta: ArrayLike, symbols: ArrayLike) -> float:
    """Largest agreement any function of ``symbols`` can reach with ``theta`` on these rows.

    Math
    ----
    ``A* = (1/M) sum_w |sum_{i: s_i = w} exp(i theta_i)|``. For any ``f``,
    ``|mean_i exp(i(f(s_i) - theta_i))| <= A*`` and ``|mean_i exp(i(f(s_i) + theta_i))| <= A*``
    (triangle inequality per symbol group), so ``circular_agreement(f(s), theta) <= A*``; the
    bound is attained by ``f(w) = arg sum_{s_i = w} exp(i theta_i)``.

    Shapes
    ------
    ``theta [M]`` float, ``symbols [M]`` int -> float in ``[0, 1]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (shapes differ, not 1-D, or M = 0), ``NUMERICAL_FAILURE``
        (non-finite angles).
    """
    t = np.asarray(theta, dtype=np.float64)
    s = np.asarray(symbols)
    if t.ndim != 1 or t.shape != s.shape or t.size == 0:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "shapes",
                           f"theta {t.shape} and symbols {s.shape} must be equal non-empty 1-D")
    if not np.all(np.isfinite(t)):
        raise StageFailure(ErrorCode.NUMERICAL_FAILURE, _COMPONENT, "finite", "non-finite theta")
    _, group = np.unique(s, return_inverse=True)
    sums = np.zeros(group.max() + 1, dtype=np.complex128)
    np.add.at(sums, group, np.exp(1j * t))
    return float(min(1.0, np.abs(sums).sum() / t.size))
