"""Public API of `topo_pilot.analysis` (see SPEC.md), part (a): spaces, sigma, discriminability."""

from .discriminability import DiscriminabilityTable
from .pointset import PointSet, ph_summary, require_same_ids
from .sigma import SigmaCalibrator, SigmaDecision, SigmaRow
from .spaces import SpaceBuilder

__all__ = [
    "DiscriminabilityTable", "PointSet", "SigmaCalibrator", "SigmaDecision", "SigmaRow",
    "SpaceBuilder", "ph_summary", "require_same_ids",
]
