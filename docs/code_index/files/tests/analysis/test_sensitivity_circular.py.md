# `tests/analysis/test_sensitivity_circular.py`

- Source: [tests/analysis/test_sensitivity_circular.py](../../../../../tests/analysis/test_sensitivity_circular.py)
- Kind: python
- Lines: 385

## Module docstring

> Independent tests N13, N20-N25 for SPEC part (c): sensitivity variants, circular correspondence.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import CircularCorrespondence, Sensitivity, belief_angle, circular_agreement, lattice_angle` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts import ActivationSet, ErrorCode, EvalSidecar, HistoryIndex, ObservationSet, OracleOutputs, StageFailure, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 16, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 27, via package root)

### External (third-party)

- `numpy` (lines 5)
- `pytest` (lines 6)
- `scipy` (lines 7)

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

- none

## Top-level constants

- `METRICS`
- `S`

## Classes and functions

- **function `expect_code`** [L34-37]: `def expect_code(code, fn, *args, **kwargs)`
- **function `wrap`** [L40-42]: `def wrap(a)` - Wrap angles to (-pi, pi].
- **test `test_N20_euclidean_equals_cdist`** [L48-52]: `def test_N20_euclidean_equals_cdist()`
- **test `test_N20_chord_equals_normalised_cdist_and_scale_invariant`** [L55-62]: `def test_N20_chord_equals_normalised_cdist_and_scale_invariant()`
- **test `test_N20_pca_full_dims_equals_euclidean`** [L65-70]: `def test_N20_pca_full_dims_equals_euclidean()`
- **test `test_N20_pca_one_dim_matches_hand_singular_vector`** [L73-83]: `def test_N20_pca_one_dim_matches_hand_singular_vector()`
- **test `test_N20_pca_fit_set_defines_projection`** [L86-96]: `def test_N20_pca_fit_set_defines_projection()`
- **function `hand_hellinger`** [L102-103]: `def hand_hellinger(p, q)`
- **function `hand_sqrt_js`** [L106-112]: `def hand_sqrt_js(p, q)`
- **test `test_N21_hand_values_two_point_distributions`** [L115-127]: `def test_N21_hand_values_two_point_distributions()`
- **test `test_N21_bounds_and_disjoint_supports`** [L130-139]: `def test_N21_bounds_and_disjoint_supports()`
- **test `test_N21_head`** [L142-145]: `def test_N21_head()`
- **test `test_N22_agreement_identity`** [L151-154]: `def test_N22_agreement_identity()`
- **test `test_N22_agreement_rotation_invariant`** [L157-161]: `def test_N22_agreement_rotation_invariant()`
- **test `test_N22_agreement_reflection_invariant`** [L164-168]: `def test_N22_agreement_reflection_invariant()`
- **test `test_N22_agreement_hand_four_points`** [L171-177]: `def test_N22_agreement_hand_four_points()`
- **test `test_N22_agreement_independent_uniform_small`** [L180-184]: `def test_N22_agreement_independent_uniform_small()`
- **function `grid_3x2`** [L190-192]: `def grid_3x2()`
- **test `test_N23_lattice_angle_hand_values`** [L195-202]: `def test_N23_lattice_angle_hand_values()`
- **test `test_N23_belief_delta_returns_state_angle`** [L205-211]: `def test_N23_belief_delta_returns_state_angle()`
- **test `test_N23_belief_split_returns_midpoint`** [L214-219]: `def test_N23_belief_split_returns_midpoint()`
- **function `noisy_circle`** [L225-231]: `def noisy_circle(M=120, d=8, noise=0.05, seed=0)`
- **test `test_N24_compare_recovers_true_angle`** [L234-241]: `def test_N24_compare_recovers_true_angle()`
- **test `test_N24_compare_independent_angle_not_significant`** [L244-254]: `def test_N24_compare_independent_angle_not_significant()`
- **test `test_N24_collinear_points_no_h1_class`** [L257-263]: `def test_N24_collinear_points_no_h1_class()`
- **test `test_N25_errors`** [L269-293]: `def test_N25_errors()`
- **test `test_N25_compare_errors`** [L296-305]: `def test_N25_compare_errors()`
- **function `build_store`** [L311-353]: `def build_store(n=6, reverse_oracle=False)`
- **test `test_N13_circular_rows_are_privileged_eval`** [L360-377]: `def test_N13_circular_rows_are_privileged_eval()`
- **test `test_N13_oracle_id_mismatch_raises`** [L380-385]: `def test_N13_oracle_id_mismatch_raises()`

