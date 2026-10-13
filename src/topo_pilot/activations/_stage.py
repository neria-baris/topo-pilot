"""I/O layer of the activations module (the only place that touches the store)."""

from __future__ import annotations

import logging
from typing import Sequence

import numpy as np

from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
    HistoryIndex,
    ObservationSet,
)

from ._extractor import ActivationExtractor

_CONSUMER = "activations"
_LOG = logging.getLogger(__name__)


class ActivationStage:
    """Load checkpoint, test observations and history index; save an ``ActivationSet``.

    Only those three artifacts are read (consumer ``"activations"``); privileged artifacts such
    as ``EvalSidecar`` are refused by the store with ``LEAKAGE``.
    """

    def __init__(self, batch_size: int = 256, device: str = "auto"):
        self.batch_size = batch_size
        self.device = device

    def run(self, checkpoint_id: str, obs_test_id: str, history_index_id: str,
            hooks: Sequence[str], panels: Sequence[int] | None, store: ArtifactStore) -> str:
        """Extract and store activations; return the ``ActivationSet`` artifact id.

        Config: ``{hooks, panels (sorted list or "all"), checkpoint_id}``; parents:
        ``[checkpoint_id, obs_test_id, history_index_id]``.

        Raises
        ------
        StageFailure
            Anything raised by the store or by :meth:`ActivationExtractor.extract`.
        """
        from topo_pilot.learner import load_model

        ckpt = store.load(Checkpoint, checkpoint_id, consumer=_CONSUMER)
        obs = store.load(ObservationSet, obs_test_id, consumer=_CONSUMER)
        index = store.load(HistoryIndex, history_index_id, consumer=_CONSUMER)
        model = load_model(ckpt)
        extractor = ActivationExtractor(hooks, self.batch_size, self.device)
        A, logits, ids = extractor.extract(model, obs, index, panels)
        art = ActivationSet(hooks=tuple(hooks), source="model",
                            history_id=np.array(ids, dtype="<U16"), A=A, logits=logits,
                            checkpoint_id=checkpoint_id)
        config = {"hooks": list(hooks),
                  "panels": "all" if panels is None else sorted(int(p) for p in panels),
                  "checkpoint_id": checkpoint_id}
        out = store.save(art, config=config,
                         parents=[checkpoint_id, obs_test_id, history_index_id],
                         seed_map={}, consumer=_CONSUMER)
        _LOG.info("activations: %d histories x %d hooks -> %s", len(ids), len(hooks), out)
        return out
