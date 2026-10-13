"""Closed-form ridge probe (part c). Pure numpy."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "prediction.RidgeProbe"


def _as2d(a: np.ndarray) -> NDArray[np.float64]:
    a = np.asarray(a, dtype=np.float64)
    return a[:, None] if a.ndim == 1 else a


class RidgeProbe:
    """Affine ridge regression ``Y ~ X W + b`` with an unpenalised intercept.

    Math
    ----
    With fit-row means ``x_bar, y_bar`` and centred ``Xc, Yc``:
    ``W = (Xc^T Xc + lam I)^-1 Xc^T Yc``, ``b = y_bar - x_bar W``. ``lam`` is the grid value
    minimising MSE on the validation rows (earliest on ties).

    Shapes
    ------
    ``X [n, d]``, ``Y [n]`` or ``[n, k]``; ``score`` returns pooled ``mse`` and ``r2``
    (``1 - SS_res / SS_tot`` with per-column means, summed over columns).

    Raises
    ------
    LEAKAGE (check ``probe_split``) : ``"test"`` appears in ``splits`` passed to ``fit``.
    INVALID_CONFIG : empty or negative lambda grid. ALIGNMENT_ERROR : unfitted / bad shapes.
    """

    def __init__(self, lambdas: Sequence[float]) -> None:
        if len(lambdas) == 0 or any(lam < 0 for lam in lambdas):
            raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "lambdas", "need >= 0 grid")
        self.lambdas = tuple(float(lam) for lam in lambdas)
        self.lam: float | None = None
        self.W: NDArray[np.float64] | None = None
        self.b: NDArray[np.float64] | None = None

    @staticmethod
    def _solve(Xc: NDArray[np.float64], Yc: NDArray[np.float64], lam: float) -> NDArray[np.float64]:
        gram = Xc.T @ Xc + lam * np.eye(Xc.shape[1])
        return np.linalg.lstsq(gram, Xc.T @ Yc, rcond=None)[0]

    def fit(self, X_fit: np.ndarray, Y_fit: np.ndarray, X_val: np.ndarray, Y_val: np.ndarray,
            splits: tuple[str, str] = ("dev_fit", "dev_val")) -> RidgeProbe:
        """Fit on the fit rows for every lambda; keep the lambda with least validation MSE."""
        if "test" in splits:
            raise StageFailure(ErrorCode.LEAKAGE, _COMPONENT, "probe_split",
                               f"probe fit received splits {splits!r}")
        X, Y, Xv, Yv = _as2d(X_fit), _as2d(Y_fit), _as2d(X_val), _as2d(Y_val)
        if X.shape[0] != Y.shape[0] or Xv.shape[0] != Yv.shape[0] or X.shape[1] != Xv.shape[1]:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "shapes", "row/col mismatch")
        x_bar, y_bar = X.mean(axis=0), Y.mean(axis=0)
        best_mse = np.inf
        for lam in self.lambdas:
            W = self._solve(X - x_bar, Y - y_bar, lam)
            b = y_bar - x_bar @ W
            mse = float(np.mean((Xv @ W + b - Yv) ** 2))
            if self.W is None or mse < best_mse:
                best_mse, self.W, self.b, self.lam = mse, W, b, lam
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Affine prediction ``[n, k]``."""
        if self.W is None or self.b is None:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "fitted", "not fitted")
        return _as2d(X) @ self.W + self.b

    def score(self, X: np.ndarray, Y: np.ndarray) -> dict[str, float]:
        """Return ``{"mse": ..., "r2": ...}`` (no KL on raw ridge output)."""
        Y2 = _as2d(Y)
        resid = self.predict(X) - Y2
        ss_tot = float(np.sum((Y2 - Y2.mean(axis=0)) ** 2))
        ss_res = float(np.sum(resid**2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        return {"mse": float(np.mean(resid**2)), "r2": r2}
