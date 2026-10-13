"""SpaceBuilder: reference comparison spaces on the same histories (consumer "analysis")."""

from __future__ import annotations

from typing import Literal

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    HistoryIndex,
    OracleOutputs,
    StageFailure,
    WorldSpec,
)
from topo_pilot.topology import NullClouds

from .pointset import PointSet

_COMPONENT = "analysis.SpaceBuilder"
_CONSUMER = "analysis"
_F2_TOL = 1e-4


def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail, aid)


class SpaceBuilder:
    """Builds :class:`PointSet` objects from stored artifacts.

    Math
    ----
    World: D = ``WorldSpec.dist`` over N states. Emission: rows of E. Beliefs: b^(32) / b^(1)
    rows of one panel. Futures: F1 = q (= q_32 = b32 T E), F2 = flattened ``[M, V*V]`` joint of
    the next two symbols, renormalised only when ``|row sum - 1| <= 1e-4``.

    Shapes
    ------
    Oracle rows follow the ``HistoryIndex`` order over all panels (D-020); a panel selects
    ``HistoryIndex.panel == panel`` and its ids are that panel's ``history_id`` values.

    Raises
    ------
    StageFailure
        ``MISSING_PARENT`` (oracle without HistoryIndex parent), ``SAMPLE_ID_MISMATCH``
        (oracle ids differ from the index), ``ARTIFACT_MISSING`` (no F2, empty panel),
        ``NUMERICAL_FAILURE`` (F2 rows far from 1), ``INVALID_CONFIG`` (bad option).
    """

    def __init__(self, store: ArtifactStore):
        self._store = store
        self._cache: dict[str, tuple[OracleOutputs, HistoryIndex]] = {}

    def world(self, world_id: str) -> PointSet:
        """The N states with the world distance as D, metric ``flat``."""
        spec = self._store.load(WorldSpec, world_id, consumer=_CONSUMER)
        D = np.asarray(spec.dist, dtype=np.float64)
        return PointSet("world", None, D, [str(i) for i in range(D.shape[0])], "flat")

    def emission(self, emission_id: str) -> PointSet:
        """The N rows of E as distributions, metric Hellinger."""
        spec = self._store.load(EmissionSpec, emission_id, consumer=_CONSUMER)
        E = np.asarray(spec.E, dtype=np.float64)
        return PointSet("emission", E, None, [str(i) for i in range(E.shape[0])], "hellinger")

    def _oracle(self, oracle_id: str) -> tuple[OracleOutputs, HistoryIndex]:
        if oracle_id in self._cache:
            return self._cache[oracle_id]
        parents = self._store.meta(oracle_id).parent_ids
        index_id = next((p for p in parents
                         if self._store.meta(p).artifact_type == "HistoryIndex"), None)
        if index_id is None:
            raise _fail(ErrorCode.MISSING_PARENT, "history_index",
                        "oracle artifact has no HistoryIndex parent", oracle_id)
        out = self._store.load(OracleOutputs, oracle_id, consumer=_CONSUMER)
        index = self._store.load(HistoryIndex, index_id, consumer=_CONSUMER)
        if list(map(str, out.history_id)) != list(map(str, index.history_id)):
            raise _fail(ErrorCode.SAMPLE_ID_MISMATCH, "oracle_vs_index",
                        "oracle rows are not in HistoryIndex order", oracle_id)
        self._cache[oracle_id] = (out, index)
        return out, index

    def _panel_rows(self, oracle_id: str, panel: int):
        out, index = self._oracle(oracle_id)
        mask = np.asarray(index.panel) == panel
        if not mask.any():
            raise _fail(ErrorCode.ARTIFACT_MISSING, "panel", f"panel {panel} has no histories",
                        oracle_id)
        return out, mask, [str(h) for h in np.asarray(index.history_id)[mask]]

    def beliefs(self, oracle_id: str, which: Literal["b32", "b1"], panel: int) -> PointSet:
        """Belief rows b^(32) or b^(1) of one panel, metric Hellinger."""
        if which not in ("b32", "b1"):
            raise _fail(ErrorCode.INVALID_CONFIG, "which", f"which={which!r}")
        out, mask, ids = self._panel_rows(oracle_id, panel)
        X = np.asarray(getattr(out, which), dtype=np.float64)[mask]
        return PointSet("belief32" if which == "b32" else "belief1", X, None, ids, "hellinger")

    def futures(self, oracle_id: str, horizon: Literal[1, 2], panel: int) -> PointSet:
        """Next-symbol predictive F1 (= q) or flattened two-step F2 of one panel."""
        if horizon not in (1, 2):
            raise _fail(ErrorCode.INVALID_CONFIG, "horizon", f"horizon={horizon!r}")
        out, mask, ids = self._panel_rows(oracle_id, panel)
        if horizon == 1:
            return PointSet("future1", np.asarray(out.q, dtype=np.float64)[mask], None, ids,
                            "hellinger")
        if out.F2 is None:
            raise _fail(ErrorCode.ARTIFACT_MISSING, "F2", "oracle has no F2", oracle_id)
        X = np.asarray(out.F2, dtype=np.float64)[mask]
        X = X.reshape(X.shape[0], -1)
        sums = X.sum(axis=1, keepdims=True)
        if not np.all(np.abs(sums - 1.0) <= _F2_TOL):
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "F2_rows_sum", "F2 row sums off by > 1e-4",
                        oracle_id)
        return PointSet("future2", X / sums, None, ids, "hellinger")

    def null(self, like: PointSet, kind: Literal["iso", "cov"], rng) -> PointSet:
        """Gaussian null cloud with the same M and feature dimension as ``like`` (Euclidean)."""
        if like.X is None:
            raise _fail(ErrorCode.INVALID_CONFIG, "null_like", "reference has no feature matrix X")
        if kind == "iso":
            X = NullClouds.isotropic(like.X.shape[0], like.X.shape[1], rng)
        elif kind == "cov":
            X = NullClouds.covariance_matched(like.X, rng)
        else:
            raise _fail(ErrorCode.INVALID_CONFIG, "kind", f"kind={kind!r}")
        return PointSet(f"null:{kind}", X, None, list(like.ids), "euclidean")
