"""Thin I/O layer of the prediction module (the only file that touches the store)."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    BaselineOutputs,
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    StageFailure,
)

from .ngram import NGramBaseline

_LOG = logging.getLogger(__name__)
_CONSUMER = "prediction"
_COMPONENT = "prediction.PredictionStage"
_GRID = (1e-3, 1e-2, 1e-1, 0.5, 1.0)


class PredictionStage:
    """Reads/writes artifacts for the prediction module (consumer ``"prediction"``)."""

    def run_baselines(self, obs_train_id: str, obs_dev_id: str, obs_test_id: str,
                      history_index_id: str, store: ArtifactStore) -> list[str]:
        """Fit unigram and bigram (additive, alpha chosen on dev) and save ``BaselineOutputs``.

        Histories are ``test.tokens[:, :32]`` of the indexed trajectories, in HistoryIndex order.
        Returns ids ``[order 1, order 2]``.

        Raises
        ------
        JOIN_CARDINALITY : an indexed sequence is not in the test set.
        ALIGNMENT_ERROR : an indexed history does not end at position 32.
        """
        train = store.load(ObservationSet, obs_train_id, consumer=_CONSUMER)
        dev = store.load(ObservationSet, obs_dev_id, consumer=_CONSUMER)
        test = store.load(ObservationSet, obs_test_id, consumer=_CONSUMER)
        index = store.load(HistoryIndex, history_index_id, consumer=_CONSUMER)
        histories = self._histories(test, index)
        parents = [obs_train_id, obs_dev_id, obs_test_id, history_index_id]
        ids = []
        for order in (1, 2):
            model = NGramBaseline(order, "additive").fit(train)
            alpha = model.select_smoothing(dev, _GRID)
            art = BaselineOutputs(ngram_order=order, smoothing=f"additive:{alpha!r}",
                                  history_id=index.history_id, probs=model.predict(histories))
            config: dict[str, Any] = {"ngram_order": order, "smoothing": "additive",
                                      "alpha": alpha, "grid": list(_GRID)}
            ids.append(store.save(art, config=config, parents=parents, seed_map={},
                                  consumer=_CONSUMER))
            _LOG.info("baseline order=%d alpha=%r saved %s", order, alpha, ids[-1])
        return ids

    @staticmethod
    def _histories(test: ObservationSet, index: HistoryIndex) -> np.ndarray:
        if np.any(index.end != 32):
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, _COMPONENT, "history_end",
                               "baselines need histories ending at position 32")
        row_of = {int(s): i for i, s in enumerate(test.sequence_id)}
        try:
            rows = [row_of[int(s)] for s in index.sequence_id]
        except KeyError as exc:
            raise StageFailure(ErrorCode.JOIN_CARDINALITY, _COMPONENT, "sequence_join",
                               f"sequence {exc} not in test set") from None
        return test.tokens[np.array(rows, dtype=np.int64), :32].astype(np.int64)

    def run_metrics(self, activation_set_id: str, oracle_id: str, store: ArtifactStore) -> str:
        """Not implemented until wave W4."""
        raise NotImplementedError("W4")

    def run_probes(self, activation_set_ids: list[str], oracle_id: str, split_spec: Any,
                   store: ArtifactStore) -> str:
        """Not implemented here: probe I/O lives in ``experiment`` stage S7 (D-047), because dev
        beliefs need the oracle kernels and this module depends on ``contracts`` only."""
        raise NotImplementedError("probe I/O is in experiment S7 (D-047)")
