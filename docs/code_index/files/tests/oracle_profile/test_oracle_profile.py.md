# `tests/oracle_profile/test_oracle_profile.py`

- Source: [tests/oracle_profile/test_oracle_profile.py](../../../../../tests/oracle_profile/test_oracle_profile.py)
- Kind: python
- Lines: 242

## Module docstring

> Independent tests of x4_oracle_profile suffix posteriors (job 0014, API.md section 4).

## Imports

### Internal (repo files)

- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](independent_reference.py.md) (line 30, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 15)
- `functools` (lines 16)
- `itertools` (lines 13)
- `pathlib` (lines 17)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `_path` -> `tests/oracle_profile`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `COORDS`
- `E_F`
- `E_Q`
- `PI_F`
- `PI_Q`
- `Q`
- `REPO_ROOT`
- `TOL_PROD`
- `T_F`
- `T_Q`

## Classes and functions

- **function `exact_stationary`** [L45-62]: `def exact_stationary(T: list[list[Fraction]]) -> list[Fraction]` - Solve pi T = pi, sum(pi) = 1 exactly by Gauss-Jordan elimination over Fractions.
- **function `strings`** [L71-73]: `def strings(length: int) -> list[tuple[int, ...]]` - All V**length observation strings.
- **function `has_double_two`** [L76-77]: `def has_double_two(s: tuple[int, ...]) -> bool`
- **function `exact`** [L81-86]: `def exact(suffix: tuple[int, ...]) -> tuple[Fraction, ...] | None` decorators: @lru_cache(maxsize=None) - Exact posterior of the float model (inputs converted exactly); None when impossible.
- **function `gap`** [L89-91]: `def gap(values, fracs) -> float` - max_s |values[s] - fracs[s]| computed exactly, returned as float.
- **function `production`** [L94-95]: `def production(rows, K)`
- **function `indep_features`** [L98-100]: `def indep_features(coords) -> np.ndarray`
- **test `test_hmm_is_asymmetric_with_exact_nonuniform_stationary_pi`** [L103-112]: `def test_hmm_is_asymmetric_with_exact_nonuniform_stationary_pi()`
- **test `test_impossible_strings_are_exactly_those_with_two_consecutive_twos`** [L115-121]: `def test_impossible_strings_are_exactly_those_with_two_consecutive_twos()`
- **test `test_production_matches_exhaustive_enumeration`** [L124-141]: `def test_production_matches_exhaustive_enumeration()` - Item 1: every string of length L <= 4 and every K in 1..L; impossible suffixes raise.
- **test `test_rows_are_normalised_and_nonnegative`** [L144-151]: `def test_rows_are_normalised_and_nonnegative()` - Item 5.
- **test `test_hand_computed_known_answers`** [L154-172]: `def test_hand_computed_known_answers()` - Exact rational model (T_Q, E_Q, PI_Q): posteriors derived by hand.
- **test `test_decimal_reference_matches_enumeration`** [L175-190]: `def test_decimal_reference_matches_enumeration()` - Items 1 and 12: decimal forward summation vs exact path enumeration on every suffix.
- **test `test_decimal_precision_context_is_honoured`** [L193-206]: `def test_decimal_precision_context_is_honoured()` - Item 12: >= 60 significant digits are carried; a lower request is refused.
- **test `test_decimal_circular_mean_matches_exact_mean`** [L209-222]: `def test_decimal_circular_mean_matches_exact_mean()` - Item 12: decimal circular mean vs the exact Fraction mean of the enumerated posterior.
- **test `test_posterior_means_matches_suffix_posterior_and_reference`** [L225-242]: `def test_posterior_means_matches_suffix_posterior_and_reference()` - posterior_means = suffix_posterior @ features for every K; vs the decimal reference.

