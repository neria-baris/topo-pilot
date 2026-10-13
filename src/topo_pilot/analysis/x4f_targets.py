"""X4-F targets (part g; x4f-exec-v2 §2): belief circle expectations and calibration PCs."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "analysis.x4f_targets"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def circle_expectation(b: NDArray, x: NDArray, period: float) -> NDArray[np.float64]:
    """Belief expectation of the circle point of a lattice coordinate.

    Math
    ----
    ``m_i = sum_z b_iz (cos(2 pi x_z / period), sin(2 pi x_z / period))``.

    Shapes
    ------
    ``b: [n, N]``, ``x: [N]`` -> ``[n, 2]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (width mismatch), ``INVALID_CONFIG`` (period <= 0).
    """
    B = np.asarray(b, dtype=np.float64)
    xs = np.asarray(x, dtype=np.float64)
    if B.ndim != 2 or xs.ndim != 1 or B.shape[1] != xs.size:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "shapes", f"b {B.shape} vs x {xs.shape}")
    if not period > 0:
        raise _fail(ErrorCode.INVALID_CONFIG, "period", f"period={period}")
    ang = 2.0 * np.pi * xs / period
    return B @ np.column_stack([np.cos(ang), np.sin(ang)])


@dataclass(frozen=True, eq=False)
class PCMap:
    """Calibration principal components: ``mean [q]``, ``components [q, c]`` (columns)."""

    mean: NDArray[np.float64]
    components: NDArray[np.float64]


def leading_components(Z_cal: NDArray, n_components: int) -> PCMap:
    """Leading eigenvectors of the population covariance of ``Z_cal``.

    Math
    ----
    ``C = (Z - z_bar)^T (Z - z_bar) / n``; columns are eigenvectors by descending eigenvalue;
    each column's largest-magnitude entry is made positive (deterministic sign).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if ``n_components`` is not in ``1..q``.
    """
    Z = np.asarray(Z_cal, dtype=np.float64)
    if Z.ndim != 2 or not 1 <= n_components <= Z.shape[1]:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "n_components",
                    f"n_components={n_components} for Z {Z.shape}")
    mean = Z.mean(axis=0)
    C = (Z - mean).T @ (Z - mean) / Z.shape[0]
    vals, vecs = np.linalg.eigh(C)
    comps = vecs[:, np.argsort(vals)[::-1][:n_components]]
    rows = np.argmax(np.abs(comps), axis=0)
    comps = comps * np.sign(comps[rows, np.arange(comps.shape[1])])
    return PCMap(mean=mean, components=comps)


def pc_scores(Z: NDArray, pc: PCMap) -> NDArray[np.float64]:
    """``(Z - pc.mean) @ pc.components`` -> ``[n, c]``."""
    return (np.asarray(Z, dtype=np.float64) - pc.mean) @ pc.components
