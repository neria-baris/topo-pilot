"""ProcessStage: the single place where the process module touches the artifact store."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from topo_pilot.contracts import ArtifactStore, ErrorCode, SeedTree, WorldSpec

from ._geometry import fail
from .emission import EMISSION_REGISTRY, WORLD_SCOPE_MASTER, EmissionConfig
from .transition import TransitionBuilder, TransitionConfig

log = logging.getLogger(__name__)
CONSUMER = "process"
_WORLD_SCOPED_MODES = ("overlap", "axis_permuted", "full_permuted")


class ProcessStage:
    """Loads a stored world, builds a spec, stores it with the world as parent."""

    def run_transition(self, world_id: str, cfg: TransitionConfig, store: ArtifactStore) -> str:
        """Build and save the ``TransitionSpec`` of ``world_id``; returns its artifact id."""
        world = store.load(WorldSpec, world_id, consumer=CONSUMER)
        spec = TransitionBuilder().build(world, cfg)
        aid = store.save(spec, config=asdict(cfg), parents=[world_id], seed_map={},
                         consumer=CONSUMER)
        log.info("process: transition %s for world %s", aid, world_id)
        return aid

    def run_emission(self, world_id: str, cfg: EmissionConfig, seeds: SeedTree,
                     store: ArtifactStore) -> str:
        """Build and save the ``EmissionSpec`` of ``world_id`` for replicate ``seeds.master``.

        The artifact config is the ``EmissionConfig`` fields plus ``replicate`` (the master
        seed, which fixes the symbol names) and, for modes that draw world-scoped randomness,
        ``world_scope_master``.
        """
        if cfg.mode not in EMISSION_REGISTRY:
            raise fail(ErrorCode.INVALID_CONFIG, "mode", f"unknown mode {cfg.mode!r}")
        world = store.load(WorldSpec, world_id, consumer=CONSUMER)
        spec = EMISSION_REGISTRY[cfg.mode]().build(world, cfg, seeds)
        config: dict[str, Any] = {**asdict(cfg), "replicate": seeds.master}
        seed_map = dict(seeds.issued)
        if cfg.mode in _WORLD_SCOPED_MODES:
            config["world_scope_master"] = WORLD_SCOPE_MASTER
            world_tree = SeedTree(WORLD_SCOPE_MASTER)
            world_tree.seed("centers", world.family)
            seed_map.update({f"world_scope/{k}": v for k, v in world_tree.issued.items()})
        aid = store.save(spec, config=config, parents=[world_id], seed_map=seed_map,
                         consumer=CONSUMER)
        log.info("process: emission %s (%s) for world %s", aid, cfg.mode, world_id)
        return aid
