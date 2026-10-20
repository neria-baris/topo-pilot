# `tests/c1prime/test_b_fwl.py`

- Source: [tests/c1prime/test_b_fwl.py](../../../../../tests/c1prime/test_b_fwl.py)
- Kind: python
- Lines: 211

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-3 part 1: FWL, F1, whitening, forced states.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis.x4f_scores import ledoit_wolf` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 19, via package root)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 27, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 28, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `D`
- `DEGENERATE`
- `REPO`
- `TWO_PI`

## Classes and functions

- **function `_status`** [L37-38]: `def _status(res) -> str`
- **function `_onehot`** [L41-44]: `def _onehot(w) -> np.ndarray`
- **function `_f`** [L47-48]: `def _f(phi) -> np.ndarray`
- **function `_truth`** [L51-63]: `def _truth(seed, per_symbol=6, phase='free')`
- **function `_fit`** [L66-67]: `def _fit(t, a=None)`
- **test `test_fwl_design_column_order`** [L70-74]: `def test_fwl_design_column_order()`
- **test `test_fwl_recovers_a_known_B_noiselessly`** [L77-88]: `def test_fwl_recovers_a_known_B_noiselessly()`
- **test `test_joint_fwl_is_not_sequential_residualisation`** [L91-101]: `def test_joint_fwl_is_not_sequential_residualisation()`
- **test `test_fwl_matches_the_frisch_waugh_lovell_formula_with_noise`** [L104-115]: `def test_fwl_matches_the_frisch_waugh_lovell_formula_with_noise()`
- **test `test_standardise_nuisance_population_sd_and_constant_columns`** [L118-124]: `def test_standardise_nuisance_population_sd_and_constant_columns()`
- **test `test_f1_symbol_determined_phase_is_degenerate`** [L130-138]: `def test_f1_symbol_determined_phase_is_degenerate()`
- **function `_with_B`** [L141-146]: `def _with_B(fit, s1, s2)`
- **function `good_fit`** [L150-151]: `def good_fit()` decorators: @pytest.fixture(scope='module')
- **test `test_f1_rank_and_condition_boundaries`** [L159-162]: `def test_f1_rank_and_condition_boundaries(good_fit, edit, expected)` decorators: @pytest.mark.parametrize('edit,expected', [({'cond': 100000000.0}, 'PASS'), ({'cond': float(np.nextafter(100000000.0, np.inf))}, DEGENERATE), ({'rank': 40}, DEGENERATE)])
- **test `test_f1_singular_value_boundaries`** [L169-170]: `def test_f1_singular_value_boundaries(good_fit, s1, s2, expected)` decorators: @pytest.mark.parametrize('s1,s2,expected', [(1.0, 1.01e-06, 'PASS'), (1.0, 9.9e-07, DEGENERATE), (0.0, 0.0, DEGENERATE), (2.0, 3.0, 'PASS')])
- **test `test_whitening_is_the_symmetric_inverse_root_of_ledoit_wolf`** [L176-188]: `def test_whitening_is_the_symmetric_inverse_root_of_ledoit_wolf()`
- **test `test_whitening_degenerate_covariance`** [L191-193]: `def test_whitening_degenerate_covariance()`
- **test `test_residual_keeps_the_phase_term`** [L196-202]: `def test_residual_keeps_the_phase_term()`
- **test `test_forced_state_is_a_plus_B_times_the_phase_difference`** [L205-211]: `def test_forced_state_is_a_plus_B_times_the_phase_difference()`

