"""Part (c) sensitivity variants: alternative distance matrices for S7 (pure, float64)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.topology import Chord, DistancePipeline, Euclidean, Hellinger, SqrtJS

_COMPONENT = "analysis.Sensitivity"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def _matrix(a: object, name: str) -> NDArray[np.float64]:
    arr = np.asarray(a, dtype=np.float64)
    if arr.ndim != 2:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, f"{name}_ndim",
                    f"{name} must be 2-D, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, f"{name}_finite", f"{name} is not finite")
    return arr


class Sensitivity:
    """Distance-matrix variants for the one-factor-at-a-time sensitivity stage (S7).

    Math
    ----
    Activations: ``euclidean`` ``||x_i - x_j||``; ``chord`` ``||x_i/||x_i|| - x_j/||x_j|| ||``;
    ``pca``: centre on the mean of ``X_fit``, project on the top ``pca_dims`` right singular
    vectors of the centred ``X_fit``, then Euclidean. Distributions: ``hellinger``
    ``||sqrt p - sqrt q||_2 / sqrt 2``; ``sqrt_js`` ``sqrt(JSD(p, q))`` (natural log).

    Shapes
    ------
    ``X [M, d]``, ``X_fit [n, d]`` -> ``D [M, M]``; ``P [M, N]`` rows on the simplex ->
    ``D [M, M]``. No deduplication.

    Invariants
    ----------
    ``D`` symmetric with zero diagonal. ``pca`` never fits on ``X`` unless the caller passes it.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (unknown variant, ``pca`` without ``X_fit``, ``pca_dims < 1``,
        ``k`` out of range), ``ALIGNMENT_ERROR`` (column mismatch, not 2-D),
        ``NUMERICAL_FAILURE`` (zero chord row, non-finite, rows not distributions).
    """

    ACTIVATION_VARIANTS = ("euclidean", "chord", "pca")
    DISTRIBUTION_VARIANTS = ("hellinger", "sqrt_js")

    def activation_D(self, X: NDArray, variant: str, X_fit: NDArray | None = None,
                     pca_dims: int = 32) -> NDArray[np.float64]:
        """Distance matrix of activation rows under ``variant`` (see class docstring)."""
        if variant not in self.ACTIVATION_VARIANTS:
            raise _fail(ErrorCode.INVALID_CONFIG, "variant", f"unknown variant {variant!r}")
        X = _matrix(X, "X")
        if variant == "euclidean":
            return Euclidean().pairwise(X)
        if variant == "chord":
            return Chord().pairwise(X)
        if X_fit is None:
            raise _fail(ErrorCode.INVALID_CONFIG, "x_fit", "variant 'pca' needs X_fit")
        if pca_dims < 1:
            raise _fail(ErrorCode.INVALID_CONFIG, "pca_dims", f"pca_dims={pca_dims} < 1")
        X_fit = _matrix(X_fit, "X_fit")
        if X_fit.shape[1] != X.shape[1]:
            raise _fail(ErrorCode.ALIGNMENT_ERROR, "columns",
                        f"X has {X.shape[1]} columns, X_fit has {X_fit.shape[1]}")
        pipe = DistancePipeline(Euclidean(), pca_dims).fit_pca(X_fit)
        return pipe.metric.pairwise((X - pipe.mean_) @ pipe.components_.T)

    def distribution_D(self, P: NDArray, variant: str) -> NDArray[np.float64]:
        """Distance matrix of distribution rows under ``variant`` (Hellinger or sqrt-JS)."""
        if variant not in self.DISTRIBUTION_VARIANTS:
            raise _fail(ErrorCode.INVALID_CONFIG, "variant", f"unknown variant {variant!r}")
        P = _matrix(P, "P")
        metric = Hellinger() if variant == "hellinger" else SqrtJS()
        return metric.pairwise(P)

    @staticmethod
    def head(n: int, k: int) -> NDArray[np.int64]:
        """The first ``k`` row indices ``arange(k)`` of ``n`` rows; ``1 <= k <= n``."""
        if k < 1 or k > n:
            raise _fail(ErrorCode.INVALID_CONFIG, "head_k", f"k={k} outside 1..{n}")
        return np.arange(k, dtype=np.int64)
