"""`OracleStage`: the only place in `oracle` that touches the artifact store."""

from __future__ import annotations

import logging

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    OracleOutputs,
    ProcessDiagnostics,
    TransitionSpec,
    tokens_hash,
)

from ._common import fail
from ._filter import BayesFilter, LastSymbolPosterior
from ._futures import FutureOperator, context_gain

_LOG = logging.getLogger(__name__)
CONSUMER = "oracle"
ANALYSIS_END = 32
OBS_LEN = 33
K_MAX = 3


def _entropy(b: NDArray[np.float64]) -> NDArray[np.float64]:
    """Shannon entropy in nats per row, with ``0 log 0 = 0``."""
    safe = np.where(b > 0, b, 1.0)
    return -(b * np.log(safe)).sum(axis=1)


def _world_family(store: ArtifactStore, artifact_id: str) -> str:
    """``config["family"]`` of the nearest WorldSpec ancestor of ``artifact_id`` ("" if none)."""
    frontier, seen = [artifact_id], set()
    while frontier:
        nxt: list[str] = []
        for aid in frontier:
            for pid in store.meta(aid).parent_ids:
                meta = store.meta(pid)
                if meta.artifact_type == "WorldSpec":
                    return str(meta.config.get("family", ""))
                if pid not in seen:
                    seen.add(pid)
                    nxt.append(pid)
        frontier = nxt
    return ""


class OracleStage:
    """Compute exact-oracle panels and process diagnostics from public artifacts only.

    Math
    ----
    For each HistoryIndex row (history ``w_1..w_32``): ``b32 = b_32``, ``b1 = r_{w_32}``,
    ``q = b_32 T E``, ``q_last = r_{w_32} T E``, ``F2 = b_32 T diag(E[:, i]) T E[:, j]``,
    ``log_evidence = log p(w_{1:32})``. ``G_C = mean KL(q || q_last)``.

    Shapes
    ------
    M = HistoryIndex rows; R_test = test trajectories; outputs as in ``OracleOutputs``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (end != 32, wrong split, V mismatch), ``SAMPLE_ID_MISMATCH``
        (unknown sequence_id, tokens_hash mismatch), ``IMPOSSIBLE_HISTORY``,
        ``NUMERICAL_FAILURE``, and ``LEAKAGE`` if a forbidden artifact were requested.
    """

    def run(self, transition_id: str, emission_id: str, obs_test_id: str,
            history_index_id: str, store: ArtifactStore) -> dict[str, str]:
        """Write one ``OracleOutputs`` and one ``ProcessDiagnostics``; return their ids."""
        trans = store.load(TransitionSpec, transition_id, consumer=CONSUMER)
        emis = store.load(EmissionSpec, emission_id, consumer=CONSUMER)
        obs = store.load(ObservationSet, obs_test_id, consumer=CONSUMER)
        hist = store.load(HistoryIndex, history_index_id, consumer=CONSUMER)
        if obs.split != "test" or obs.V != emis.E.shape[1]:
            raise fail(ErrorCode.ALIGNMENT_ERROR, "inputs", "need a test split with V = E width")
        rows = self._history_rows(obs, hist)
        filt = BayesFilter(trans.T, emis.E, trans.pi)
        last = LastSymbolPosterior(trans.T, emis.E, trans.pi)
        fut = FutureOperator(trans.T, emis.E)
        hist_tokens = obs.tokens[rows, :ANALYSIS_END]
        res = filt.run(hist_tokens)
        b32 = res.b[:, ANALYSIS_END - 1]
        b1 = last.r(hist_tokens[:, -1])
        q_last = last.q_last(hist_tokens[:, -1])
        q = res.q[:, ANALYSIS_END]
        ce_all = filt.run(obs.tokens).ce.astype(np.float32)
        entropy = _entropy(b32)
        oracle = OracleOutputs(
            history_id=hist.history_id, b32=b32, b1=b1, q=q, q_last=q_last,
            belief_entropy=entropy, log_evidence=res.log_evidence,
            F2=fut.F2(b32).astype(np.float32), ce_oracle_all_positions=ce_all)
        diag = ProcessDiagnostics(
            G_C=context_gain(q, q_last), mean_H_b1=float(_entropy(b1).mean()),
            O_singular_values=tuple(tuple(float(x) for x in s)
                                    for s in fut.observability_singular_values(K_MAX)),
            sigma=emis.sigma, world_family=_world_family(store, emission_id))
        parents = [transition_id, emission_id, obs_test_id, history_index_id]
        config = {"transition_id": transition_id, "emission_id": emission_id,
                  "obs_test_id": obs_test_id, "history_index_id": history_index_id}
        ids = {name: store.save(art, config=config, parents=parents, seed_map={},
                                consumer=CONSUMER)
               for name, art in (("oracle", oracle), ("diagnostics", diag))}
        _LOG.info("oracle: %d histories, %d test trajectories, G_C=%.4f",
                  len(rows), obs.n_sequences, diag.G_C)
        return ids

    @staticmethod
    def _history_rows(obs: ObservationSet, hist: HistoryIndex) -> NDArray[np.int64]:
        """Row index in ``obs`` for each history; checks end == 32 and tokens_hash."""
        if obs.tokens.shape[1] != OBS_LEN or np.any(hist.end != ANALYSIS_END):
            raise fail(ErrorCode.ALIGNMENT_ERROR, "history_end", "every history must end at 32")
        order = np.argsort(obs.sequence_id)
        pos = np.searchsorted(obs.sequence_id, hist.sequence_id, sorter=order)
        pos = np.clip(pos, 0, len(order) - 1)
        rows = order[pos]
        if np.any(obs.sequence_id[rows] != hist.sequence_id):
            raise fail(ErrorCode.SAMPLE_ID_MISMATCH, "sequence_id", "history not in test split")
        hashes = [tokens_hash(obs.tokens[r, :ANALYSIS_END]) for r in rows.tolist()]
        if hashes != [str(h) for h in hist.tokens_hash]:
            raise fail(ErrorCode.SAMPLE_ID_MISMATCH, "tokens_hash", "tokens_hash mismatch")
        return rows.astype(np.int64)
