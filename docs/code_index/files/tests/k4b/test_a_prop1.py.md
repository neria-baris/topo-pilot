# `tests/k4b/test_a_prop1.py`

- Source: [tests/k4b/test_a_prop1.py](../../../../../tests/k4b/test_a_prop1.py)
- Kind: python
- Lines: 194

## Module docstring

> K4b author A, TEST_PLAN A1 (protocol §1.2, §11.4): Proposition 1 by exact enumeration.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `pytest` (lines 18)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 13)
- `functools` (lines 14)
- `itertools` (lines 15)
- `pathlib` (lines 16)
- `random` (lines 11)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `C`
- `E`
- `PI`
- `REPO`
- `T`

## Classes and functions

- **function `solve`** [L38-48]: `def solve(A, b)`
- **function `stationary`** [L51-55]: `def stationary(Tm)`
- **function `forward`** [L61-66]: `def forward(start, obs)` - alpha_t(z) = P(w_1..w_t, z_t = z): emit first, transitions between emissions.
- **function `mean_of`** [L69-72]: `def mean_of(a)`
- **function `law`** [L76-84]: `def law(start, restart, k, length=L)` decorators: @lru_cache(maxsize=None) - Rows (w, P(w), r_k(w)) over every history of the given length.
- **function `expect`** [L87-88]: `def expect(rows, g)`
- **function `random_table`** [L91-94]: `def random_table(seed, k)`
- **test `test_hmm_is_asymmetric_stationary_and_positive`** [L97-103]: `def test_hmm_is_asymmetric_stationary_and_positive()`
- **test `test_history_law_sums_to_one`** [L106-110]: `def test_history_law_sums_to_one()`
- **test `test_residual_is_not_identically_zero`** [L113-115]: `def test_residual_is_not_identically_zero()`
- **test `test_random_suffix_table_has_zero_expectation`** [L119-122]: `def test_random_suffix_table_has_zero_expectation(seed)` decorators: @pytest.mark.parametrize('seed', range(8))
- **test `test_suffix_identity_holds_for_other_suffix_lengths`** [L126-129]: `def test_suffix_identity_holds_for_other_suffix_lengths(k)` decorators: @pytest.mark.parametrize('k', [1, 2, 3])
- **test `test_conditional_residual_vanishes_given_each_suffix`** [L132-139]: `def test_conditional_residual_vanishes_given_each_suffix()`
- **test `test_rotated_and_reflected_suffix_fields_stay_zero`** [L142-150]: `def test_rotated_and_reflected_suffix_fields_stay_zero()` - Gauge invariance: a rotation or reflection of a suffix-only field is suffix-only.
- **test `test_constant_field_is_zero`** [L153-156]: `def test_constant_field_is_zero()`
- **test `test_prefix_dependent_field_is_nonzero`** [L159-167]: `def test_prefix_dependent_field_is_nonzero()`
- **test `test_field_mixing_suffix_and_residual_sign_is_nonzero`** [L170-181]: `def test_field_mixing_suffix_and_residual_sign_is_nonzero()` - A suffix table multiplied by a residual-sign indicator is no longer suffix-only.
- **test `test_nonstationary_start_breaks_the_identity`** [L184-194]: `def test_nonstationary_start_breaks_the_identity()` - Sanity of the enumerator: with z1 from a non-stationary start and the suffix filter

