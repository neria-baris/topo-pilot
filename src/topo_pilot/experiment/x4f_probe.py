"""X4-F nested ridge (x4f-exec-v2 §4): inner leave-one-panel-out selection, calibration refit,
one outer-validation score.

The ridge is the affine RidgeProbe estimator (centre on fit rows, ``W = (Xc^T Xc + lam I)^-1
Xc^T Yc``, ``b = y_bar - x_bar W``) on fit-row-standardised features, solved by one Cholesky
factorisation per grid value. Outer-validation arrays are not read before the refit.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import cho_factor, cho_solve

from topo_pilot.analysis import r2_pooled, standardizer

GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)


@dataclass(frozen=True, eq=False)
class NestedResult:
    """Selected ``lam``, outer-validation ``r2`` (None + status if undefined), validation
    predictions and the mean inner-fold MSE per grid value."""

    lam: float
    r2: float | None
    r2_status: str
    pred_val: NDArray[np.float64]
    fold_mse: dict[float, float] = field(default_factory=dict)


def _ridge_path(X_fit: NDArray, Y_fit: NDArray, grid: tuple[float, ...],
                checkpoint=lambda _: None):
    """Standardise on ``X_fit`` and return ``(mean, scale, y_bar, [W_lam])``."""
    mean, scale = standardizer(X_fit)
    Xs = (X_fit - mean) / scale
    x_bar, y_bar = Xs.mean(axis=0), Y_fit.mean(axis=0)
    Xc, Yc = Xs - x_bar, Y_fit - y_bar
    gram, cross = Xc.T @ Xc, Xc.T @ Yc
    eye = np.eye(gram.shape[0])
    Ws = []
    for lam in grid:
        checkpoint(f"ridge solve {lam}")
        Ws.append(cho_solve(cho_factor(gram + lam * eye), cross))
        checkpoint(f"ridge solve {lam} complete")
    return mean, scale, x_bar, y_bar, Ws


def _predict(X: NDArray, mean, scale, x_bar, y_bar, W) -> NDArray[np.float64]:
    return ((X - mean) / scale - x_bar) @ W + y_bar


def nested_ridge(X_cal: NDArray, Y_cal: NDArray, panel_cal: NDArray, X_val: NDArray,
                 Y_val: NDArray, grid: tuple[float, ...] = GRID,
                 checkpoint=lambda _: None) -> NestedResult:
    """Leave-one-panel-out selection over calibration panels, refit, score once.

    Ties of the mean fold MSE resolve to the larger lambda.
    """
    X = np.asarray(X_cal, dtype=np.float64)
    Y = np.asarray(Y_cal, dtype=np.float64).reshape(X.shape[0], -1)
    panels = np.asarray(panel_cal)
    mse = {lam: [] for lam in grid}
    for p in sorted(set(panels.tolist())):
        checkpoint(f"ridge fold {p}")
        held = panels == p
        stats = _ridge_path(X[~held], Y[~held], grid, checkpoint)
        for lam, W in zip(grid, stats[4]):
            pred = _predict(X[held], *stats[:4], W)
            mse[lam].append(float(np.mean((pred - Y[held]) ** 2)))
    fold_mse = {lam: float(np.mean(v)) for lam, v in mse.items()}
    best = min(fold_mse.values())
    lam = max(lam for lam, v in fold_mse.items() if v == best)
    stats = _ridge_path(X, Y, (lam,), checkpoint)
    Xv = np.asarray(X_val, dtype=np.float64)
    pred = _predict(Xv, *stats[:4], stats[4][0])
    Yv = np.asarray(Y_val, dtype=np.float64).reshape(Xv.shape[0], -1)
    r2, status = r2_pooled(pred, Yv, Y.mean(axis=0))
    checkpoint("ridge validation complete")
    return NestedResult(lam, r2, status, pred, fold_mse)
