# `tests/analysis/test_x4f_scores.py`

- Source: [tests/analysis/test_x4f_scores.py](../../../../../tests/analysis/test_x4f_scores.py)
- Kind: python
- Lines: 323

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import gate_verdict, kl_rows, ledoit_wolf, r2_pooled, rbf_bandwidth, rbf_features, rbf_map, standardizer, support_gate, support_report` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 11, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)

### External (third-party)

- `numpy` (lines 8)
- `pytest` (lines 9)

### Standard library

- `math` (lines 6)

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

- `GATES`

## Classes and functions

- **function `_pairwise_median`** [L28-30]: `def _pairwise_median(X)`
- **function `_lw_reference`** [L33-43]: `def _lw_reference(X)` - Ledoit and Wolf (2004): population covariance S shrunk toward m*I, m = tr(S)/d, with
- **function `_mahalanobis`** [L46-48]: `def _mahalanobis(X, mu, cov)`
- **test `test_standardizer_population_std_and_zero_floor`** [L53-62]: `def test_standardizer_population_std_and_zero_floor()`
- **test `test_r2_pooled_hand_values_around_calibration_mean`** [L67-72]: `def test_r2_pooled_hand_values_around_calibration_mean()`
- **test `test_r2_pooled_is_pooled_over_coordinates`** [L75-80]: `def test_r2_pooled_is_pooled_over_coordinates()`
- **test `test_r2_pooled_one_dimensional_and_negative`** [L83-89]: `def test_r2_pooled_one_dimensional_and_negative()`
- **test `test_r2_pooled_zero_variance_threshold_scales_with_n_q`** [L92-100]: `def test_r2_pooled_zero_variance_threshold_scales_with_n_q()`
- **test `test_kl_rows_hand_values_in_nats`** [L105-111]: `def test_kl_rows_hand_values_in_nats()`
- **test `test_kl_rows_zero_p_terms_contribute_nothing_even_where_q_is_zero`** [L114-119]: `def test_kl_rows_zero_p_terms_contribute_nothing_even_where_q_is_zero()`
- **test `test_kl_rows_undefined_when_q_zero_where_p_positive`** [L122-125]: `def test_kl_rows_undefined_when_q_zero_where_p_positive()`
- **test `test_kl_rows_shape_mismatch`** [L129-134]: `def test_kl_rows_shape_mismatch(shape_q)` decorators: @pytest.mark.parametrize('shape_q', [(2, 3), (3, 2), (2,)])
- **test `test_rbf_bandwidth_median_rule_hand_value`** [L139-142]: `def test_rbf_bandwidth_median_rule_hand_value()`
- **test `test_rbf_bandwidth_subsample_follows_rng_choice`** [L145-151]: `def test_rbf_bandwidth_subsample_follows_rng_choice()`
- **test `test_rbf_bandwidth_degenerate_for_identical_rows`** [L154-156]: `def test_rbf_bandwidth_degenerate_for_identical_rows()`
- **test `test_rbf_map_draw_order_and_shapes`** [L159-166]: `def test_rbf_map_draw_order_and_shapes()`
- **test `test_rbf_features_formula`** [L169-176]: `def test_rbf_features_formula()`
- **test `test_ledoit_wolf_shrinks_population_covariance_toward_scaled_identity`** [L182-197]: `def test_ledoit_wolf_shrinks_population_covariance_toward_scaled_identity(n, d)` decorators: @pytest.mark.parametrize('n,d', [(300, 5), (10, 20)])
- **test `test_ledoit_wolf_zero_shrinkage_known_answer`** [L200-204]: `def test_ledoit_wolf_zero_shrinkage_known_answer()`
- **function `_support_data`** [L209-212]: `def _support_data(seed=0, n=2000, d=4)`
- **test `test_support_identity_patch_and_planted_shift`** [L215-232]: `def test_support_identity_patch_and_planted_shift()`
- **test `test_support_ratio_undefined_with_duplicated_rows`** [L235-241]: `def test_support_ratio_undefined_with_duplicated_rows()`
- **test `test_support_degenerate_covariance`** [L244-248]: `def test_support_degenerate_covariance()`
- **test `test_support_gate_literal_rule`** [L264-265]: `def test_support_gate_literal_rule(frac, randoms, expected)` decorators: @pytest.mark.parametrize('frac,randoms,expected', [(0.03, [0.02] * 20, True), (0.05, [0.025] * 20, True), (0.051, [0.1] * 20, False), (0.03, [0.01] * 20, False), (0.0, [0.0] * 20, True), (1e-09, [0.0] * 20, False), (1e-09, [0.0] * 11 + [0.5] * 9, False), (0.02, [0.0] * 9 + [0.01] * 11, True), (0.03, [0.0] * 9 + [0.01] * 11, False)])
- **function `_model`** [L273-276]: `def _model(**over)`
- **test `test_verdict_all_pass_is_feasible`** [L279-281]: `def test_verdict_all_pass_is_feasible()`
- **test `test_verdict_g1_fail_is_not_feasible_even_with_inconclusive_gates`** [L284-290]: `def test_verdict_g1_fail_is_not_feasible_even_with_inconclusive_gates()`
- **test `test_verdict_g2_inconclusive_names_g2_and_model`** [L293-297]: `def test_verdict_g2_inconclusive_names_g2_and_model()`
- **test `test_verdict_names_first_gate_in_g1_to_g5_order`** [L300-306]: `def test_verdict_names_first_gate_in_g1_to_g5_order()`
- **test `test_verdict_not_run_after_later_failure_is_inconclusive`** [L309-314]: `def test_verdict_not_run_after_later_failure_is_inconclusive()`
- **test `test_verdict_any_single_non_pass_blocks_feasible`** [L319-323]: `def test_verdict_any_single_non_pass_blocks_feasible(gate, status)` decorators: @pytest.mark.parametrize('gate,status', [('G5', 'NOT_RUN'), ('G4', 'FAIL'), ('G1', 'INCONCLUSIVE'), ('G3', 'INCONCLUSIVE')])

