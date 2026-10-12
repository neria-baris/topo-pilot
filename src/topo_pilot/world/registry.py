"""World builder ABC, registry, and the validated `build_world` entry point."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Mapping

from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec

from .complex import CubicalComplex, check_boundary_closed
from .config import WorldConfig
from .metrics import check_flat_bounds


class WorldBuilder(ABC):
    """Builds a :class:`WorldSpec` for one family.

    Attributes
    ----------
    family : registry key.
    expected_betti : ``{p: (beta_0, beta_1, ...)}`` the builder promises over GF(p).
    """

    family: ClassVar[str]
    expected_betti: ClassVar[Mapping[int, tuple[int, ...]]]

    @abstractmethod
    def build(self, cfg: WorldConfig) -> WorldSpec:
        """Return the world for ``cfg`` (deterministic; no RNG)."""


WORLD_REGISTRY: dict[str, type[WorldBuilder]] = {}


def register_world(cls: type[WorldBuilder]) -> type[WorldBuilder]:
    """Class decorator registering ``cls`` under ``cls.family``; returns ``cls``."""
    WORLD_REGISTRY[cls.family] = cls
    return cls


def build_world(cfg: WorldConfig) -> WorldSpec:
    """Registry dispatch followed by full validation.

    Math
    ----
    Runs ``spec.validate()``, checks ``d_{k-1} d_k = 0`` over Z on ``spec.cells`` (D-011) and,
    for a flat ``dist``, ``dist <= dist_graph + 1e-9`` and ``dist >= dist_graph / sqrt(D)``.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (unknown family), ``BETTI_MISMATCH`` (incl. ``boundary_not_closed``),
        ``INVALID_GLUE``, ``NON_METRIC``.
    """
    if cfg.family not in WORLD_REGISTRY:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "world.build_world", "family",
                           f"unknown world family {cfg.family!r}; known: {sorted(WORLD_REGISTRY)}")
    spec = WORLD_REGISTRY[cfg.family]().build(cfg)
    spec.validate()
    check_boundary_closed(CubicalComplex(spec.n_states, spec.cells))
    if spec.metric == "flat":
        check_flat_bounds(spec.dist, spec.dist_graph, len(spec.dims))
    return spec
