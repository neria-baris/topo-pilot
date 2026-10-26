# `tests/hws/test_a_identities.py`

- Source: [tests/hws/test_a_identities.py](../../../../../tests/hws/test_a_identities.py)
- Kind: python
- Lines: 400

## Module docstring

> Author A (job 0119): identities on a tiny rational HMM by exact enumeration (TEST_PLAN §2).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 28, via sys.path edit)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../../tools/hws/hws_oracle.py.md) (line 29, via sys.path edit)
- `import hws_exact` -> [tools/hws/hws_exact.py](../../tools/hws/hws_exact.py.md) (line 30, via sys.path edit)
- `from topo_pilot.oracle import context_gain` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 31, via package root)
- `from topo_pilot.world.config import WorldConfig` -> [src/topo_pilot/world/config.py](../../src/topo_pilot/world/config.py.md) (line 83, via package root) (inside a function)
- `from topo_pilot.world.registry import build_world` -> [src/topo_pilot/world/registry.py](../../src/topo_pilot/world/registry.py.md) (line 84, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `decimal` (lines 15)
- `fractions` (lines 16)
- `functools` (lines 17)
- `itertools` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 18)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `HWS_DIR` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `C2`
- `EC16`
- `HWS_DIR`
- `LABELS`
- `REPO`
- `S2`
- `SIZES`
- `TOL_DEC`

## Classes and functions

- **function `_t8`** [L47-56]: `def _t8()` - 8 * T: stay 4/8, x-neighbours 1/8 each (periodic), y-neighbour 2/8. Symmetric.
- **function `_e16`** [L59-62]: `def _e16()` - 16 * E' with E'[:, 2g + b] = sum over i with g(i) = g of E_centres[:, 2i + b].
- **function `_dec`** [L68-69]: `def _dec(f)`
- **function `_den`** [L72-73]: `def _den(t)`
- **function `_kget`** [L76-78]: `def _kget(d, k)` - API-AMBIGUITY: dicts 'D[K]' may be keyed by int K or by str(K).
- **function `_proc`** [L82-98]: `def _proc()` decorators: @lru_cache(maxsize=1)
- **function `_dot`** [L101-102]: `def _dot(m, r)`
- **function `_norm2`** [L105-106]: `def _norm2(m)`
- **function `_exact`** [L110-237]: `def _exact()` decorators: @lru_cache(maxsize=1)
- **function `_flags`** [L240-244]: `def _flags(obj)` - Every nested {"value", "pass"} record of a result dict.
- **function `_idx`** [L247-248]: `def _idx(s)`
- **test `test_fixture_is_a_valid_rational_process`** [L251-256]: `def test_fixture_is_a_valid_rational_process()`
- **test `test_i1_suffix_functions_have_zero_covariance_with_r_k`** [L259-263]: `def test_i1_suffix_functions_have_zero_covariance_with_r_k()`
- **test `test_i1_fails_for_a_prefix_dependent_function`** [L266-270]: `def test_i1_fails_for_a_prefix_dependent_function()`
- **test `test_i3_v_k_identity_and_monotone`** [L273-277]: `def test_i3_v_k_identity_and_monotone()`
- **test `test_i2_i4_and_d4_positive`** [L280-287]: `def test_i2_i4_and_d4_positive()`
- **test `test_gain_identities_kl_rows_equal_entropy_differences`** [L290-300]: `def test_gain_identities_kl_rows_equal_entropy_differences()`
- **test `test_proposition_f_for_three_suffix_predictors`** [L303-308]: `def test_proposition_f_for_three_suffix_predictors()`
- **test `test_rowwise_pinsker`** [L311-314]: `def test_rowwise_pinsker()`
- **test `test_enumerate_histories_order_and_probabilities`** [L317-325]: `def test_enumerate_histories_order_and_probabilities()`
- **test `test_exact_expectations_matches_the_fraction_values`** [L328-343]: `def test_exact_expectations_matches_the_fraction_values()`
- **test `test_row_arrays_on_every_history`** [L346-362]: `def test_row_arrays_on_every_history()`
- **test `test_kl_rows_zero_support_convention_and_entropy_rows`** [L365-373]: `def test_kl_rows_zero_support_convention_and_entropy_rows()`
- **test `test_kl_rows_numerical_failures`** [L377-388]: `def test_kl_rows_numerical_failures(bad)` decorators: @pytest.mark.parametrize('bad', ['zero_q', 'nan_p', 'inf_q'])
- **test `test_kl_rows_mean_equals_context_gain_on_random_rows`** [L391-399]: `def test_kl_rows_mean_equals_context_gain_on_random_rows()`

