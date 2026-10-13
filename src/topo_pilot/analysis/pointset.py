"""PointSet value, id alignment check and the pure PH summary helper."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure, Status
from topo_pilot.topology import (
    DistanceMetric,
    DistancePipeline,
    Euclidean,
    Hellinger,
    PersistenceComputer,
    PHConfig,
    Summaries,
)

_COMPONENT = "analysis.PointSet"


@dataclass(frozen=True, eq=False)
class PointSet:
    """A labelled point cloud in one comparison space.

    Shapes
    ------
    ``X: [M, F] float64`` or None; ``D: [M, M] float64`` or None (at least one is given);
    ``ids``: M strings (history_ids, or state ids for world / emission).

    Invariants
    ----------
    ``space`` is one of ``world | emission | belief32 | belief1 | future1 | future2 |
    act:<hook> | base:R0..R3 | null:iso | null:cov |
    pred:softmax | x4:V0..V5``; ``metric`` is ``hellinger``, ``euclidean`` or ``flat`` (a given D).
    """

    space: str
    X: NDArray[np.float64] | None
    D: NDArray[np.float64] | None
    ids: list[str]
    metric: str


def require_same_ids(a: PointSet, b: PointSet) -> None:
    """Raise ``SAMPLE_ID_MISMATCH`` unless both sets have the identical ordered id list."""
    if list(a.ids) != list(b.ids):
        raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, _COMPONENT, "same_ids",
                           f"{a.space} ({len(a.ids)} ids) and {b.space} ({len(b.ids)} ids) "
                           "do not share the identical ordered id list")


def _metric(name: str) -> DistanceMetric:
    if name == "hellinger":
        return Hellinger()
    if name in ("euclidean", "flat"):
        return Euclidean()
    raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "metric", f"unknown metric {name!r}")


def _dedup_given_D(D: NDArray[np.float64]) -> NDArray[np.float64]:
    """Merge points at distance <= 1e-12 in a given D (first occurrence kept)."""
    seen = np.zeros(D.shape[0], dtype=bool)
    keep = []
    for i in range(D.shape[0]):
        if not seen[i]:
            keep.append(i)
            seen |= D[i] <= 1e-12
    return np.ascontiguousarray(D[np.ix_(keep, keep)])


def _scale(D: NDArray[np.float64]) -> float:
    vals = D[np.triu_indices_from(D, k=1)]
    vals = vals[vals > 0.0]
    return float(np.quantile(vals, 0.95)) if vals.size else 0.0


def ph_summary(pointset: PointSet, maxdim: int = 1) -> dict:
    """Persistent-homology summary of one point set.

    Math
    ----
    ``D`` = pairwise metric of ``X`` (or the given ``D``), duplicates merged, ``s`` = 95th
    percentile of positive distances, ``S = max finite H1 persistence / s`` (0 if none).

    Returns
    -------
    dict with ``S_H1`` (float), ``scale_s`` (float), ``status`` (``Status`` value string) and
    ``n_points`` (points after deduplication). A collapsed cloud gives ``S_H1 = 0`` and status
    ``"collapsed"``; a censored diagram propagates ``"censored"``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (neither X nor D) and any code raised by ``topology``.
    """
    if pointset.X is not None:
        res = DistancePipeline(_metric(pointset.metric)).compute(pointset.X, pointset.ids)
        D, scale, status = res.D, res.scale_s, res.status
    elif pointset.D is not None:
        D = _dedup_given_D(np.asarray(pointset.D, dtype=np.float64))
        scale = 0.0 if D.shape[0] == 1 else _scale(D)
        status = Status.COLLAPSED if D.shape[0] == 1 else Status.OK
    else:
        raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "empty", "neither X nor D given")
    if status is Status.COLLAPSED:
        return {"S_H1": 0.0, "scale_s": 0.0, "status": Status.COLLAPSED.value, "n_points": 1}
    diag = PersistenceComputer(PHConfig(maxdim=maxdim)).diagrams(D)
    return {"S_H1": Summaries.S(diag, 1, scale), "scale_s": scale, "status": diag.status.value,
            "n_points": int(D.shape[0])}
