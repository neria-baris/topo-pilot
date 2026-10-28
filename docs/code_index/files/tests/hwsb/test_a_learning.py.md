# `tests/hwsb/test_a_learning.py`

- Source: [tests/hwsb/test_a_learning.py](../../../../../tests/hwsb/test_a_learning.py)
- Kind: python
- Lines: 360

## Module docstring

> HWSB author A: B1, B2, B3 on planted predictives (protocol §4 B1-B3; DRB5).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 29, via sys.path edit)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../../tools/hws/hws_oracle.py.md) (line 30, via sys.path edit)
- `from topo_pilot.prediction.metrics import PredictiveMetrics` -> [src/topo_pilot/prediction/metrics.py](../../src/topo_pilot/prediction/metrics.py.md) (line 32, via package root)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 35, via sys.path edit)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 36, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 13)
- `math` (lines 11)
- `pathlib` (lines 14)
- `statistics` (lines 15)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 27: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `MISSING`
- `REPO`
- `TOL`

## Classes and functions

- **function `need`** [L47-49]: `def need()`
- **function `stop_status`** [L52-53]: `def stop_status(excinfo)`
- **function `dirichlet`** [L56-59]: `def dirichlet(rng, n)`
- **function `q`** [L63-65]: `def q()` decorators: @pytest.fixture(scope='module')
- **function `kl_ref`** [L68-72]: `def kl_ref(p, q_)` - Independent mean-free KL per row: sum_v p (log p - log q) with math.log and fsum.
- **function `marg_ref`** [L75-82]: `def marg_ref(x)` - Circular marginal by an explicit loop: label a sums the six symbols v = 6a + b.
- **function `forcing_ref`** [L85-94]: `def forcing_ref(q_full, q_base, p, z)`
- **function `assert_forcing`** [L97-106]: `def assert_forcing(res, ref)`
- **function `exact_boundary_rows`** [L109-121]: `def exact_boundary_rows(rng)` - Rows with captured == 0.8 exactly in float64 (k of n rows predicted by q1, 5k = n).
- **test `test_reference_z_b23_value`** [L126-129]: `def test_reference_z_b23_value()`
- **test `test_reference_marginal_matches_reused`** [L132-138]: `def test_reference_marginal_matches_reused(q)`
- **test `test_reference_kl_matches_reused`** [L141-143]: `def test_reference_kl_matches_reused(q)`
- **test `test_reference_boundary_construction`** [L146-150]: `def test_reference_boundary_construction()`
- **test `test_softmax64_bitwise_s3_formula`** [L155-164]: `def test_softmax64_bitwise_s3_formula()`
- **test `test_to_canonical_random_perm_exact`** [L167-176]: `def test_to_canonical_random_perm_exact()`
- **test `test_model_equal_to_q_reindexes_to_q`** [L179-184]: `def test_model_equal_to_q_reindexes_to_q(q)`
- **function `_two_col`** [L189-193]: `def _two_col(x)` - A row [x - 0.5, 0.5]: both entries and the sum x are exact in float64.
- **test `test_check_rows_boundary_at_tolerance`** [L196-214]: `def test_check_rows_boundary_at_tolerance()`
- **test `test_check_rows_refuses_nan_negative_inf`** [L218-223]: `def test_check_rows_refuses_nan_negative_inf(row)` decorators: @pytest.mark.parametrize('row', [[float('nan'), 1.0], [-0.1, 1.1], [float('inf'), 0.0]])
- **test `test_b1_oracle_model_captures_all`** [L228-234]: `def test_b1_oracle_model_captures_all(q)`
- **test `test_b1_last_symbol_model_captures_nothing`** [L237-242]: `def test_b1_last_symbol_model_captures_nothing(q)`
- **test `test_b1_regret_and_gc_match_reference`** [L245-261]: `def test_b1_regret_and_gc_match_reference(q)`
- **test `test_b1_equality_at_point_eight_passes_and_just_below_fails`** [L264-278]: `def test_b1_equality_at_point_eight_passes_and_just_below_fails()`
- **test `test_b1_inconclusive_when_gc_at_floor`** [L281-291]: `def test_b1_inconclusive_when_gc_at_floor(q)`
- **test `test_z_b23_constant`** [L296-299]: `def test_z_b23_constant()`
- **test `test_forcing_suffix_model_has_zero_gain`** [L302-311]: `def test_forcing_suffix_model_has_zero_gain(q)`
- **test `test_forcing_oracle_model_has_positive_lower_bound`** [L314-322]: `def test_forcing_oracle_model_has_positive_lower_bound(q)`
- **test `test_forcing_general_and_explicit_z`** [L325-330]: `def test_forcing_general_and_explicit_z(q)`
- **test `test_forcing_ratio_undefined_without_gain`** [L333-337]: `def test_forcing_ratio_undefined_without_gain(q)`
- **test `test_b3_is_forcing_on_circular_marginals`** [L340-353]: `def test_b3_is_forcing_on_circular_marginals(q)`
- **test `test_b3_suffix_model_zero_and_oracle_positive`** [L356-360]: `def test_b3_suffix_model_zero_and_oracle_positive(q)`

