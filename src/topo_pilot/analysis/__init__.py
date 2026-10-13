"""Public API of `topo_pilot.analysis` (see SPEC.md), parts (a) to (h)."""

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
from .x4f_erasure import (
    Eraser,
    Family,
    Whitening,
    apply_map,
    displacements,
    eraser_from_basis,
    fit_oblique_eraser,
    mismatch_report,
    random_family,
    whiten,
)
from .x4f_scores import (
    gate_verdict,
    kl_rows,
    ledoit_wolf,
    r2_pooled,
    rbf_bandwidth,
    rbf_features,
    rbf_map,
    standardizer,
    support_gate,
    support_report,
)
from .x4f_targets import PCMap, circle_expectation, leading_components, pc_scores
from .x5_context import (
    GC_THRESHOLD,
    context_status,
    percentile_interval,
    x5_overall_verdict,
)
from .x5_kernel import (
    SpectrumReport,
    integrated_autocorrelation,
    is_connected,
    movement_rate,
    rate_matched_kernel,
    spectrum_report,
)

__all__ = [
    "CircularCorrespondence", "DiscriminabilityTable", "Dynamics", "F1Decision", "F1Verdict",
    "GeometryAlignment", "LayerSweep", "PointSet", "Sensitivity", "SigmaCalibrator",
    "SigmaDecision", "SigmaRow", "SpaceBuilder", "belief_angle", "circular_agreement",
    "lattice_angle", "ln_gauge_free", "ph_summary", "predictive_pointset", "r2_points",
    "r3_points", "readout_projector", "require_same_ids", "spectral_embedding", "split_readout",
    "Partners", "PoolScreen", "TangentAudit", "ToleranceRow", "hellinger", "helmert_basis",
    "joint_marginals", "nearest_partners", "overall_verdict", "pair_d2", "practical_verdict",
    "screen_pool", "select_anchors", "strict_verdict", "symbol_only_bound", "tangent_audit",
    "Eraser", "Family", "PCMap", "Whitening", "apply_map", "circle_expectation", "displacements",
    "eraser_from_basis", "fit_oblique_eraser", "gate_verdict", "kl_rows", "leading_components",
    "ledoit_wolf", "mismatch_report", "pc_scores", "r2_pooled", "random_family", "rbf_bandwidth",
    "rbf_features", "rbf_map", "standardizer", "support_gate", "support_report", "whiten",
    "GC_THRESHOLD", "SpectrumReport", "context_status", "integrated_autocorrelation",
    "is_connected", "movement_rate", "percentile_interval", "x5_overall_verdict",
    "rate_matched_kernel", "spectrum_report",
]
