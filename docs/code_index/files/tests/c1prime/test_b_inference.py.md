# `tests/c1prime/test_b_inference.py`

- Source: [tests/c1prime/test_b_inference.py](../../../../../tests/c1prime/test_b_inference.py)
- Kind: python
- Lines: 246

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-2 part 1 (§12.2-§13, §15.3.2 C7, §3.5).

## Imports

### Internal (repo files)

- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../../tools/c1prime/c1_endpoint.py.md) (line 29, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 30, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 32, via sys.path edit)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 14)
- `fractions` (lines 17)
- `pathlib` (lines 18)
- `sys` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `MODELS`
- `REPO`
- `U`
- `ZETA`

## Classes and functions

- **function `_gamma`** [L41-42]: `def _gamma(n) -> Fraction`
- **function `_tree_mean`** [L45-53]: `def _tree_mean(values) -> float`
- **function `_scalar`** [L56-59]: `def _scalar(x) -> float`
- **function `_model_value`** [L62-77]: `def _model_value(res, model, key)`
- **test `test_ratio_to_mean_reduction`** [L87-91]: `def test_ratio_to_mean_reduction(meanY, meanG, c, expected)` decorators: @pytest.mark.parametrize('meanY,meanG,c,expected', [(0.3, 1.0, 0.1, True), (0.05, 1.0, 0.1, False), (0.1, 1.0, 0.1, False), (0.021, 0.2, 0.1, True), (-0.4, 0.5, 0.1, False), (0.8, 2.5, 0.3, True)])
- **test `test_per_model_status_boundaries`** [L98-99]: `def test_per_model_status_boundaries(L, U_, expected)` decorators: @pytest.mark.parametrize('L,U_,expected', [(0.1, 0.2, 'PASS_j'), (-0.2, -0.1, 'FAIL_j'), (0.0, 0.1, 'INC_j'), (-0.1, 0.0, 'INC_j'), (-0.1, 0.1, 'INC_j'), (0.0, 0.0, 'INC_j'), (5e-324, 1.0, 'PASS_j'), (-1.0, -5e-324, 'FAIL_j')])
- **test `test_overall_rule`** [L106-107]: `def test_overall_rule(statuses, expected)` decorators: @pytest.mark.parametrize('statuses,expected', [(['PASS_j'] * 3, 'PASS'), (['FAIL_j'] * 3, 'FAIL'), (['PASS_j', 'PASS_j', 'INC_j'], 'MIXED'), (['FAIL_j', 'FAIL_j', 'PASS_j'], 'MIXED'), (['INC_j'] * 3, 'MIXED')])
- **test `test_tree_mean_is_the_balanced_pairwise_tree`** [L114-121]: `def test_tree_mean_is_the_balanced_pairwise_tree(n)` decorators: @pytest.mark.parametrize('n', [1, 2, 3, 5, 8, 37, 100])
- **test `test_tree_mean_order_differs_from_left_to_right`** [L124-127]: `def test_tree_mean_order_differs_from_left_to_right()`
- **test `test_tree_mean_within_theorem5_with_cancellation_and_subnormals`** [L130-144]: `def test_tree_mean_within_theorem5_with_cancellation_and_subnormals()`
- **test `test_bootstrap_means_share_one_integers_call_per_draw`** [L150-162]: `def test_bootstrap_means_share_one_integers_call_per_draw()`
- **test `test_h5_wrapper_index_stream_equals_bootstrap_profile`** [L165-172]: `def test_h5_wrapper_index_stream_equals_bootstrap_profile()`
- **test `test_h5_wrapper_uses_the_tree_kernel_on_real_valued_data`** [L175-180]: `def test_h5_wrapper_uses_the_tree_kernel_on_real_valued_data()`
- **test `test_rank_for_protocol_ranks`** [L187-191]: `def test_rank_for_protocol_ranks(p, rank)` decorators: @pytest.mark.parametrize('p,rank', [(0.05, 250), (0.05 / 3, 84), (1 - 0.05 / 3, 4917)])
- **test `test_quantile_with_rank_returns_the_input_element_at_the_rank`** [L195-200]: `def test_quantile_with_rank_returns_the_input_element_at_the_rank(p, rank)` decorators: @pytest.mark.parametrize('p,rank', [(0.05, 250), (0.05 / 3, 84), (1 - 0.05 / 3, 4917)])
- **test `test_rank_check_accepts_order_statistics_and_rejects_others`** [L203-211]: `def test_rank_check_accepts_order_statistics_and_rejects_others()`
- **test `test_quantile_with_rank_rejects_a_wrong_order_statistic`** [L214-226]: `def test_quantile_with_rank_rejects_a_wrong_order_statistic(monkeypatch)`
- **test `test_endpoint_bounds_use_shared_draws_and_ranks_84_and_4917`** [L232-246]: `def test_endpoint_bounds_use_shared_draws_and_ranks_84_and_4917()`

