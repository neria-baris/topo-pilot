"""Fixed analysis panels (RESEARCH_SUMMARY 7.1)."""

from __future__ import annotations

import numpy as np

from topo_pilot.contracts import (
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    StageFailure,
    make_history_id,
    tokens_hash,
)

from .config import DatasetConfig


class PanelBuilder:
    """Draws ``n_panels`` disjoint panels of ``panel_size`` distinct test trajectories.

    Math: ``perm = rng.permutation(R)``; panel ``k`` (1-based) is
    ``perm[(k-1)*S : k*S]``; each row is the history ``w_1..w_end`` of that trajectory, with
    ``tokens_hash = contracts.tokens_hash(tokens[row, :end])`` and
    ``history_id = make_history_id(dataset_id, sequence_id, end, tokens_hash)``.

    Shapes: output arrays all have length ``M = n_panels * panel_size``, rows sorted by
    (panel, position within panel = drawn order).

    Invariants: selection uses only the rng and ``R`` (no latent information).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if ``R < n_panels * panel_size`` or ``end`` is not in ``1..33``.
    """

    def build(self, test: ObservationSet, cfg: DatasetConfig, rng: np.random.Generator,
              *, dataset_id: str = "") -> HistoryIndex:
        m = cfg.n_panels * cfg.panel_size
        r = test.n_sequences
        if r < m or not 1 <= cfg.analysis_position <= test.tokens.shape[1]:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "dataset.PanelBuilder", "panel_sizes",
                               f"{r} test trajectories for {cfg.n_panels}x{cfg.panel_size} "
                               f"panels, end={cfg.analysis_position}")
        rows = rng.permutation(r)[:m]
        end = cfg.analysis_position
        seq = test.sequence_id[rows]
        hashes = [tokens_hash(test.tokens[i, :end]) for i in rows]
        ids = [make_history_id(dataset_id, s, end, h) for s, h in zip(seq.tolist(), hashes)]
        panel = np.repeat(np.arange(1, cfg.n_panels + 1, dtype=np.int64), cfg.panel_size)
        index = HistoryIndex(
            dataset_id=dataset_id, history_id=np.array(ids, dtype="<U16"),
            sequence_id=seq.astype(np.int64), end=np.full(m, end, dtype=np.int64), panel=panel,
            tokens_hash=np.array(hashes, dtype="<U16"), panel_size=cfg.panel_size,
            n_panels=cfg.n_panels)
        index.validate()
        return index
