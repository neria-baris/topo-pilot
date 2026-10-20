# `src/topo_pilot/analysis/__init__.py`

- Source: [src/topo_pilot/analysis/__init__.py](../../../../../../src/topo_pilot/analysis/__init__.py)
- Kind: python
- Lines: 113

## Module docstring

> Public API of `topo_pilot.analysis` (see SPEC.md), parts (a) to (h).

## Imports

### Internal (repo files)

- `from .baselines import r2_points, r3_points, spectral_embedding` -> [src/topo_pilot/analysis/baselines.py](baselines.py.md) (line 3, via relative)
- `from .circular import CircularCorrespondence, belief_angle, circular_agreement, lattice_angle` -> [src/topo_pilot/analysis/circular.py](circular.py.md) (line 4, via relative)
- `from .circular_bound import symbol_only_bound` -> [src/topo_pilot/analysis/circular_bound.py](circular_bound.py.md) (line 5, via relative)
- `from .discriminability import DiscriminabilityTable` -> [src/topo_pilot/analysis/discriminability.py](discriminability.py.md) (line 6, via relative)
- `from .dynamics import Dynamics, LayerSweep` -> [src/topo_pilot/analysis/dynamics.py](dynamics.py.md) (line 7, via relative)
- `from .f1 import F1Decision, F1Verdict` -> [src/topo_pilot/analysis/f1.py](f1.py.md) (line 8, via relative)
- `from .geometry import GeometryAlignment` -> [src/topo_pilot/analysis/geometry.py](geometry.py.md) (line 9, via relative)
- `from .horizon import TangentAudit, ToleranceRow, hellinger, helmert_basis, joint_marginals, tangent_audit` -> [src/topo_pilot/analysis/horizon.py](horizon.py.md) (line 10, via relative)
- `from .horizon_pools import Partners, PoolScreen, nearest_partners, overall_verdict, pair_d2, practical_verdict, screen_pool, select_anchors, strict_verdict` -> [src/topo_pilot/analysis/horizon_pools.py](horizon_pools.py.md) (line 18, via relative)
- `from .pointset import PointSet, ph_summary, require_same_ids` -> [src/topo_pilot/analysis/pointset.py](pointset.py.md) (line 29, via relative)
- `from .readout import ln_gauge_free, predictive_pointset, readout_projector, split_readout` -> [src/topo_pilot/analysis/readout.py](readout.py.md) (line 30, via relative)
- `from .sensitivity import Sensitivity` -> [src/topo_pilot/analysis/sensitivity.py](sensitivity.py.md) (line 31, via relative)
- `from .sigma import SigmaCalibrator, SigmaDecision, SigmaRow` -> [src/topo_pilot/analysis/sigma.py](sigma.py.md) (line 32, via relative)
- `from .spaces import SpaceBuilder` -> [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 33, via relative)
- `from .x4f_erasure import Eraser, Family, Whitening, apply_map, displacements, eraser_from_basis, fit_oblique_eraser, mismatch_report, random_family, whiten` -> [src/topo_pilot/analysis/x4f_erasure.py](x4f_erasure.py.md) (line 34, via relative)
- `from .x4f_scores import gate_verdict, kl_rows, ledoit_wolf, r2_pooled, rbf_bandwidth, rbf_features, rbf_map, standardizer, support_gate, support_report` -> [src/topo_pilot/analysis/x4f_scores.py](x4f_scores.py.md) (line 46, via relative)
- `from .x4f_targets import PCMap, circle_expectation, leading_components, pc_scores` -> [src/topo_pilot/analysis/x4f_targets.py](x4f_targets.py.md) (line 58, via relative)
- `from .x5_context import GC_THRESHOLD, context_status, percentile_interval, x5_overall_verdict` -> [src/topo_pilot/analysis/x5_context.py](x5_context.py.md) (line 59, via relative)
- `from .x5_endpoint import X5_DELAY, X5_GRID, X5_THRESHOLD, BootstrapResult, DiffBounds, GridEvent, PairEvidence, cohort_verdict, dev_auc, difference_bounds, grid_event, pair_evidence, pair_flags, paired_bootstrap_endpoint, pass_sequence, quantile_inverted_cdf, ratio_curve` -> [src/topo_pilot/analysis/x5_endpoint.py](x5_endpoint.py.md) (line 65, via relative)
- `from .x5_kernel import SpectrumReport, integrated_autocorrelation, is_connected, movement_rate, rate_matched_kernel, spectrum_report` -> [src/topo_pilot/analysis/x5_kernel.py](x5_kernel.py.md) (line 84, via relative)

### External (third-party)

- none

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py](../../../docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py.md) (line 6, import)
- [src/topo_pilot/experiment/circ_audit.py](../experiment/circ_audit.py.md) (line 22, import)
- [src/topo_pilot/experiment/s2.py](../experiment/s2.py.md) (line 17, import)
- [src/topo_pilot/experiment/s4_analysis.py](../experiment/s4_analysis.py.md) (line 18, import)
- [src/topo_pilot/experiment/s6.py](../experiment/s6.py.md) (line 28, import)
- [src/topo_pilot/experiment/s7_circular.py](../experiment/s7_circular.py.md) (line 19, import)
- [src/topo_pilot/experiment/s7_sensitivity.py](../experiment/s7_sensitivity.py.md) (line 25, import)
- [src/topo_pilot/experiment/x4.py](../experiment/x4.py.md) (line 27, import)
- [src/topo_pilot/experiment/x4_inputs.py](../experiment/x4_inputs.py.md) (line 19, import)
- [src/topo_pilot/experiment/x4b.py](../experiment/x4b.py.md) (line 15, import)
- [src/topo_pilot/experiment/x4b2_run.py](../experiment/x4b2_run.py.md) (line 19, import)
- [src/topo_pilot/experiment/x4b_audit.py](../experiment/x4b_audit.py.md) (line 12, import)
- [src/topo_pilot/experiment/x4b_run.py](../experiment/x4b_run.py.md) (line 22, import)
- [src/topo_pilot/experiment/x4f_damage.py](../experiment/x4f_damage.py.md) (line 8, import)
- [src/topo_pilot/experiment/x4f_data.py](../experiment/x4f_data.py.md) (line 16, import)
- [src/topo_pilot/experiment/x4f_gates.py](../experiment/x4f_gates.py.md) (line 13, import)
- [src/topo_pilot/experiment/x4f_probe.py](../experiment/x4f_probe.py.md) (line 17, import)
- [src/topo_pilot/experiment/x4f_run.py](../experiment/x4f_run.py.md) (line 22, import)
- [src/topo_pilot/experiment/x5g1_main.py](../experiment/x5g1_main.py.md) (line 19, import)
- [src/topo_pilot/experiment/x5g1_oracle.py](../experiment/x5g1_oracle.py.md) (line 10, import)
- [src/topo_pilot/experiment/x5g1_run.py](../experiment/x5g1_run.py.md) (line 15, import)
- [src/topo_pilot/experiment/x5g1_verify.py](../experiment/x5g1_verify.py.md) (line 23, import)
- [src/topo_pilot/experiment/x5g1t_config.py](../experiment/x5g1t_config.py.md) (line 17, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](../experiment/x5g1t_stages_eval.py.md) (line 23, import)
- [src/topo_pilot/experiment/x5g1t_train.py](../experiment/x5g1t_train.py.md) (line 11, import)
- [tests/analysis/test_baselines_dynamics.py](../../../tests/analysis/test_baselines_dynamics.py.md) (line 7, import)
- [tests/analysis/test_circular_bound.py](../../../tests/analysis/test_circular_bound.py.md) (line 5, import)
- [tests/analysis/test_f1_rule.py](../../../tests/analysis/test_f1_rule.py.md) (line 7, import)
- [tests/analysis/test_geometry.py](../../../tests/analysis/test_geometry.py.md) (line 6, import)
- [tests/analysis/test_horizon.py](../../../tests/analysis/test_horizon.py.md) (line 5, import)
- [tests/analysis/test_horizon.py](../../../tests/analysis/test_horizon.py.md) (line 161, import)
- [tests/analysis/test_readout.py](../../../tests/analysis/test_readout.py.md) (line 5, import)
- [tests/analysis/test_sensitivity_circular.py](../../../tests/analysis/test_sensitivity_circular.py.md) (line 9, import)
- [tests/analysis/test_sigma_calibrator.py](../../../tests/analysis/test_sigma_calibrator.py.md) (line 5, import)
- [tests/analysis/test_spaces.py](../../../tests/analysis/test_spaces.py.md) (line 4, import)
- [tests/analysis/test_x4f_erasure.py](../../../tests/analysis/test_x4f_erasure.py.md) (line 10, import)
- [tests/analysis/test_x4f_erasure_family.py](../../../tests/analysis/test_x4f_erasure_family.py.md) (line 11, import)
- [tests/analysis/test_x4f_family_maintenance.py](../../../tests/analysis/test_x4f_family_maintenance.py.md) (line 5, import)
- [tests/analysis/test_x4f_scores.py](../../../tests/analysis/test_x4f_scores.py.md) (line 11, import)
- [tests/analysis/test_x4f_targets.py](../../../tests/analysis/test_x4f_targets.py.md) (line 9, import)
- [tests/analysis/test_x5_context.py](../../../tests/analysis/test_x5_context.py.md) (line 16, import)
- [tests/analysis/test_x5_kernel.py](../../../tests/analysis/test_x5_kernel.py.md) (line 16, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 7, import)
- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 95, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 20, import)
- [tools/d2a/d2a_eval.py](../../../tools/d2a/d2a_eval.py.md) (line 14, import)
- [tools/d2a/d2a_targets.py](../../../tools/d2a/d2a_targets.py.md) (line 18, import)
- [tools/d2a/d2a_world.py](../../../tools/d2a/d2a_world.py.md) (line 17, import)

## Top-level constants

- none

## Classes and functions

- none

