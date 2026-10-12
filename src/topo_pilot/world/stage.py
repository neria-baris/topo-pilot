"""The only I/O class of `world`: builds a WorldSpec and saves it to the artifact store."""

from __future__ import annotations

import logging
from dataclasses import fields

from topo_pilot.contracts import ArtifactStore

from .config import WorldConfig
from .registry import build_world

_LOG = logging.getLogger(__name__)


class WorldStage:
    """Build and persist a world (deterministic; no RNG, empty seed map, no parents)."""

    def run(self, cfg: WorldConfig, store: ArtifactStore) -> str:
        """Build ``cfg``, save the :class:`WorldSpec` and return its artifact id.

        Invariants
        ----------
        Identical ``cfg`` gives the identical id (content addressing).

        Raises
        ------
        StageFailure
            Any ``build_world`` error, or a store error.
        """
        spec = build_world(cfg)
        config = {f.name: getattr(cfg, f.name) for f in fields(cfg)}
        config["dims"] = list(cfg.dims)
        config["params"] = dict(cfg.params)
        aid = store.save(spec, config=config, parents=[], seed_map={}, consumer="world")
        _LOG.info("world %s dims=%s saved as %s", cfg.family, tuple(cfg.dims), aid)
        return aid
