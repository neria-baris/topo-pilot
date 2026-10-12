"""Distance pipeline: optional PCA, pairwise metric, deduplication, scale ``s``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure, Status

from .metrics import DistanceMetric

DEDUP_TOL = 1e-12


@dataclass(frozen=True, eq=False)
class DistanceResult:
    """Deduplicated distance matrix (pure result; persisted later as ``DistanceArtifact``).

    Shapes
    ------
    ``D: [M', M'] float64``; ``point_ids``: ids of the kept representatives;
    ``dedup_map: [M] int64`` with ``dedup_map[i]`` = row of original point ``i`` in ``D``.

    Invariants
    ----------
    ``scale_s`` = 95th percentile of positive off-diagonal distances (raw units), 0 if none.
    ``status`` is ``Status.COLLAPSED`` iff ``M' == 1``, else ``Status.OK``.
    """

    D: NDArray[np.float64]
    point_ids: tuple[str, ...]
    dedup_map: NDArray[np.int64]
    scale_s: float
    status: Status


def scale_of(D: NDArray[np.float64]) -> float:
    """95th percentile (linear interpolation) of the positive upper-triangle distances."""
    vals = D[np.triu_indices_from(D, k=1)]
    vals = vals[vals > 0.0]
    return float(np.quantile(vals, 0.95)) if vals.size else 0.0


def deduplicate(D: NDArray[np.float64]) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """Merge points at distance <= 1e-12 (first occurrence is the representative).

    Returns
    -------
    keep : [M'] indices of representatives (increasing); dedup_map : [M] row in the reduced D.
    """
    M = D.shape[0]
    dedup_map = np.full(M, -1, dtype=np.int64)
    keep: list[int] = []
    for i in range(M):
        if dedup_map[i] >= 0:
            continue
        group = (D[i] <= DEDUP_TOL) & (dedup_map < 0)
        dedup_map[group] = len(keep)
        keep.append(i)
    return np.asarray(keep, dtype=np.int64), dedup_map


class DistancePipeline:
    """``X -> (optional PCA) -> metric -> dedup -> DistanceResult``.

    Math
    ----
    PCA: ``Z = (X - mu) V_k`` with ``mu`` and the top-``k`` right singular vectors ``V_k`` of
    the centred fit set. Then ``D = metric.pairwise(Z)``.

    Shapes
    ------
    ``X: [M, F]``; ``ids``: M strings.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (PCA not fitted / too many dims / id count), ``NUMERICAL_FAILURE``
        (from the metric).
    """

    def __init__(self, metric: DistanceMetric, pca_dims: int | None = None):
        self.metric = metric
        self.pca_dims = pca_dims
        self.mean_: NDArray[np.float64] | None = None
        self.components_: NDArray[np.float64] | None = None

    def fit_pca(self, X_fit: NDArray[np.float64]) -> "DistancePipeline":
        """Fit PCA on ``X_fit`` (the caller passes dev data only). No-op if ``pca_dims`` is None."""
        if self.pca_dims is None:
            return self
        X = np.asarray(X_fit, dtype=np.float64)
        if X.ndim != 2 or not 1 <= self.pca_dims <= min(X.shape):
            raise StageFailure(ErrorCode.INVALID_CONFIG, "topology.DistancePipeline", "pca_dims",
                               f"pca_dims={self.pca_dims} invalid for fit shape {X.shape}")
        self.mean_ = X.mean(axis=0)
        _, _, vt = np.linalg.svd(X - self.mean_, full_matrices=False)
        self.components_ = vt[: self.pca_dims]
        return self

    def _project(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        if self.pca_dims is None:
            return X
        if self.components_ is None or self.mean_ is None:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "topology.DistancePipeline",
                               "pca_unfitted", "fit_pca must be called before compute")
        if X.shape[1] != self.components_.shape[1]:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "topology.DistancePipeline",
                               "pca_features", "feature dimension differs from the PCA fit")
        return (X - self.mean_) @ self.components_.T

    def compute(self, X: NDArray[np.float64], ids: Sequence[str]) -> DistanceResult:
        """Return the deduplicated distance matrix, ids, dedup map, scale and status."""
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2 or len(ids) != X.shape[0]:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "topology.DistancePipeline", "ids",
                               "ids must match the rows of a 2-D X")
        D_full = self.metric.pairwise(self._project(X))
        keep, dedup_map = deduplicate(D_full)
        D = np.ascontiguousarray(D_full[np.ix_(keep, keep)])
        status = Status.COLLAPSED if keep.size == 1 else Status.OK
        scale = 0.0 if keep.size == 1 else scale_of(D)
        return DistanceResult(D, tuple(str(ids[k]) for k in keep), dedup_map, scale, status)
