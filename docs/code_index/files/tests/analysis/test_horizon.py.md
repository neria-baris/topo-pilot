# `tests/analysis/test_horizon.py`

- Source: [tests/analysis/test_horizon.py](../../../../../tests/analysis/test_horizon.py)
- Kind: python
- Lines: 191

## Module docstring

> Part (e) horizon feasibility: known answers and properties (X4 Phase B, protocol x4b-v1 §8).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import hellinger, helmert_basis, joint_marginals, nearest_partners, overall_verdict, pair_d2, practical_verdict, screen_pool, select_anchors, strict_verdict, tangent_audit` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `from topo_pilot.analysis import Partners` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 161, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)

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

- none

## Classes and functions

- **function `_maps`** [L23-27]: `def _maps(T, E)` - Hand-written G1 = T E and lexicographic joint G2 (block i = T diag(E[:, i]) T E).
- **function `_stochastic`** [L30-32]: `def _stochastic(rng, n, m)`
- **function `_path`** [L35-38]: `def _path()`
- **test `test_helmert_basis_orthonormal_sum_zero`** [L41-47]: `def test_helmert_basis_orthonormal_sum_zero()`
- **test `test_constant_emissions_factorize_and_have_no_gap`** [L50-58]: `def test_constant_emissions_factorize_and_have_no_gap()`
- **test `test_four_state_path_known_answer`** [L61-68]: `def test_four_state_path_known_answer()`
- **test `test_constructed_factorization_is_detected`** [L71-78]: `def test_constructed_factorization_is_detected()`
- **test `test_generic_hmm_has_certificate_and_tolerance_rows`** [L81-88]: `def test_generic_hmm_has_certificate_and_tolerance_rows()`
- **test `test_symbol_permutation_invariance`** [L91-101]: `def test_symbol_permutation_invariance()`
- **test `test_joint_order_and_marginals_catch_bT2E_and_transposed_order`** [L104-116]: `def test_joint_order_and_marginals_catch_bT2E_and_transposed_order()`
- **test `test_hellinger_bounds_and_negative_error`** [L119-125]: `def test_hellinger_bounds_and_negative_error()`
- **test `test_select_anchors_is_deterministic_and_order_free`** [L128-136]: `def test_select_anchors_is_deterministic_and_order_free()`
- **test `test_nearest_partners_excludes_self_duplicates_and_other_symbols`** [L139-148]: `def test_nearest_partners_excludes_self_duplicates_and_other_symbols()`
- **test `test_screen_pool_and_pair_d2`** [L151-165]: `def test_screen_pool_and_pair_d2()`
- **test `test_practical_verdict_two_of_three_rule`** [L178-179]: `def test_practical_verdict_two_of_three_rule(statuses, expected)` decorators: @pytest.mark.parametrize('statuses,expected', [({'test': 'WITNESS', 'a': 'WITNESS', 'b': 'WITNESS', 'c': 'UNDERCOVERED'}, 'GAP'), ({'test': 'WITNESS', 'a': 'WITNESS', 'b': 'NO_MATERIAL_GAP', 'c': 'NO_MATERIAL_GAP'}, 'INCONCLUSIVE'), ({'test': 'NO_MATERIAL_GAP', 'a': 'NO_MATERIAL_GAP', 'b': 'NO_MATERIAL_GAP', 'c': 'UNDERCOVERED'}, 'NO_GAP'), ({'test': 'NO_MATERIAL_GAP', 'a': 'NO_MATERIAL_GAP', 'b': 'NO_MATERIAL_GAP', 'c': 'WITNESS'}, 'INCONCLUSIVE'), ({'test': 'UNDERCOVERED', 'a': 'WITNESS', 'b': 'WITNESS', 'c': 'WITNESS'}, 'INCONCLUSIVE')])
- **test `test_overall_and_strict_verdicts`** [L182-191]: `def test_overall_and_strict_verdicts()`

