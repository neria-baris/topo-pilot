"""Public API of `topo_pilot.analysis` (see SPEC.md), parts (a) to (e)."""

from .baselines import r2_points, r3_points, spectral_embedding
from .circular import CircularCorrespondence, belief_angle, circular_agreement, lattice_angle
from .circular_bound import symbol_only_bound
from .discriminability import DiscriminabilityTable
from .dynamics import Dynamics, LayerSweep
from .f1 import F1Decision, F1Verdict
from .geometry import GeometryAlignment
from .horizon import (
    TangentAudit,
    ToleranceRow,
    hellinger,
    helmert_basis,
    joint_marginals,
    tangent_audit,
)
from .horizon_pools import (
    Partners,
    PoolScreen,
    nearest_partners,
    overall_verdict,
    pair_d2,
    practical_verdict,
    screen_pool,
    select_anchors,
    strict_verdict,
)
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
    "Partners", "PoolScreen", "TangentAudit", "ToleranceRow", "hellinger", "helmert_basis",
    "joint_marginals", "nearest_partners", "overall_verdict", "pair_d2", "practical_verdict",
    "screen_pool", "select_anchors", "strict_verdict", "symbol_only_bound", "tangent_audit",
]
