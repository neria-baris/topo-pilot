"""Public API of `topo_pilot.world` (see SPEC.md and README.md)."""

from .complex import CubicalComplex
from .config import WorldConfig
from .identification import Identification
from .lattice import CylinderBuilder, QuotientLatticeBuilder, SquareBuilder
from .metrics import FlatQuotientMetric, GraphGeodesicMetric, Metric
from .registry import WORLD_REGISTRY, WorldBuilder, build_world, register_world
from .stage import WorldStage

__all__ = [
    "CubicalComplex", "CylinderBuilder", "FlatQuotientMetric", "GraphGeodesicMetric",
    "Identification", "Metric", "QuotientLatticeBuilder", "SquareBuilder", "WORLD_REGISTRY",
    "WorldBuilder", "WorldConfig", "WorldStage", "build_world", "register_world",
]
