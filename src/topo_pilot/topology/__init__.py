"""Public API of `topo_pilot.topology` (see SPEC.md): distances and persistent homology."""

from .circular import CircularCoordinates
from .distance import DistancePipeline, DistanceResult
from .metrics import METRIC_REGISTRY, Chord, DistanceMetric, Euclidean, Hellinger, SqrtJS
from .persistence import DiagramResult, PersistenceComputer, PHConfig
from .shapes import NullClouds, SyntheticShapes
from .summaries import Summaries

__all__ = [
    "Chord", "CircularCoordinates", "DiagramResult", "DistanceMetric", "DistancePipeline",
    "DistanceResult", "Euclidean", "Hellinger", "METRIC_REGISTRY", "NullClouds", "PHConfig",
    "PersistenceComputer", "Summaries", "SqrtJS", "SyntheticShapes",
]
