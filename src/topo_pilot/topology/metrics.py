"""Pairwise distance metrics on rows of an array (pure kernels)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import cdist

from topo_pilot.contracts import ErrorCode, StageFailure

_DIST_TOL = 1e-9


def _fail(code: ErrorCode, component: str, check: str, detail: str) -> StageFailure:
    return StageFailure(code=code, component=f"topology.{component}", check=check, detail=detail)


def _check_matrix(X: NDArray[np.float64], component: str) -> NDArray[np.float64]:
    X = np.asarray(X, dtype=np.float64)
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise _fail(ErrorCode.NUMERICAL_FAILURE, component, "shape",
                    f"expected [M,F], got {X.shape}")
    if not np.all(np.isfinite(X)):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, component, "finite", "non-finite entries")
    return X


def _check_distributions(X: NDArray[np.float64], component: str) -> None:
    if np.any(X < -_DIST_TOL):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, component, "non_distribution", "negative entries")
    if np.any(np.abs(X.sum(axis=1) - 1.0) > _DIST_TOL):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, component, "non_distribution",
                    "rows do not sum to 1 within 1e-9")


def _finish(D: NDArray[np.float64]) -> NDArray[np.float64]:
    D = 0.5 * (D + D.T)
    np.fill_diagonal(D, 0.0)
    return D


class DistanceMetric(ABC):
    """Pairwise distance between the rows of ``X``.

    Math
    ----
    ``D[i, j] = d(X[i], X[j])`` for the metric ``d`` of the concrete class.

    Shapes
    ------
    ``X: [M, F] float64`` -> ``D: [M, M] float64``, symmetric, zero diagonal, ``D >= 0``.

    Raises
    ------
    StageFailure
        ``NUMERICAL_FAILURE`` when the rows are not valid for the metric.
    """

    name: ClassVar[str]

    @abstractmethod
    def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        """Return the [M, M] distance matrix of the rows of ``X``."""


class Euclidean(DistanceMetric):
    """Euclidean distance ``||x - y||_2``."""

    name: ClassVar[str] = "euclidean"

    def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        X = _check_matrix(X, "Euclidean")
        return _finish(cdist(X, X))


class Chord(DistanceMetric):
    """Euclidean distance between L2-normalised rows. A zero row raises ``zero_vector``."""

    name: ClassVar[str] = "chord"

    def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        X = _check_matrix(X, "Chord")
        norms = np.linalg.norm(X, axis=1)
        if np.any(norms == 0.0):
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "Chord", "zero_vector", "zero_vector")
        U = X / norms[:, None]
        return _finish(cdist(U, U))


class Hellinger(DistanceMetric):
    """Hellinger distance ``||sqrt p - sqrt q||_2 / sqrt 2``; rows must be distributions."""

    name: ClassVar[str] = "hellinger"

    def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        X = _check_matrix(X, "Hellinger")
        _check_distributions(X, "Hellinger")
        R = np.sqrt(np.clip(X, 0.0, None))
        return _finish(cdist(R, R) / np.sqrt(2.0))


def _entropy_rows(P: NDArray[np.float64]) -> NDArray[np.float64]:
    logs = np.log(np.where(P > 0, P, 1.0))
    return -(P * logs).sum(axis=-1)


class SqrtJS(DistanceMetric):
    """Square root of the Jensen-Shannon divergence (natural log); rows are distributions.

    Math
    ----
    ``JS(p, q) = H((p+q)/2) - (H(p) + H(q))/2`` with ``H(x) = -sum x log x``, ``0 log 0 = 0``;
    ``d = sqrt(max(JS, 0))``.
    """

    name: ClassVar[str] = "sqrt_js"

    def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        X = _check_matrix(X, "SqrtJS")
        _check_distributions(X, "SqrtJS")
        P = np.clip(X, 0.0, None)
        H = _entropy_rows(P)
        D = np.empty((P.shape[0], P.shape[0]), dtype=np.float64)
        for i in range(P.shape[0]):
            D[i] = _entropy_rows(0.5 * (P[i][None, :] + P)) - 0.5 * (H[i] + H)
        return _finish(np.sqrt(np.clip(D, 0.0, None)))


METRIC_REGISTRY: dict[str, type[DistanceMetric]] = {
    cls.name: cls for cls in (Euclidean, Chord, Hellinger, SqrtJS)
}
