"""Public API of `topo_pilot.analysis` (see SPEC.md), parts (a) to (d)."""

from .baselines import r2_points, r3_points, spectral_embedding
from .circular import CircularCorrespondence, belief_angle, circular_agreement, lattice_angle
from .discriminability import DiscriminabilityTable
from .dynamics import Dynamics, LayerSweep
from .f1 import F1Decision, F1Verdict
from .geometry import GeometryAlignment
from .pointset import PointSet, ph_summary, require_same_ids
from .readout import ln_gauge_free, predictive_pointset, readout_projector, split_readout
from .sensitivity import Sensitivity
from .sigma import SigmaCalibrator, SigmaDecision, SigmaRow
from .spaces import SpaceBuilder

__all__ = [
    "CircularCorrespondence", "DiscriminabilityTable", "Dynamics", "F1Decision", "F1Verdict",
    "GeometryAlignment", "LayerSweep", "PointSet", "Sensitivity", "SigmaCalibrator",
    "SigmaDecision", "SigmaRow", "SpaceBuilder", "belief_angle", "circular_agreement",
    "lattice_angle", "ln_gauge_free", "ph_summary", "predictive_pointset", "r2_points",
    "r3_points", "readout_projector", "require_same_ids", "spectral_embedding", "split_readout",
]
