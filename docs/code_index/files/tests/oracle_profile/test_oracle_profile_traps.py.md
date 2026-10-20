# `tests/oracle_profile/test_oracle_profile_traps.py`

- Source: [tests/oracle_profile/test_oracle_profile_traps.py](../../../../../tests/oracle_profile/test_oracle_profile_traps.py)
- Kind: python
- Lines: 271

## Module docstring

> Independent tests of x4_oracle_profile: suffix boundary, orientation traps, symbol permutation
> and error paths (job 0014; API.md section 4 items 2, 3, 4 and 6).

## Imports

### Internal (repo files)

- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](independent_reference.py.md) (line 29, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 14)
- `functools` (lines 15)
- `itertools` (lines 12)
- `pathlib` (lines 16)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `_path` -> `tests/oracle_profile`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BAD_CALLS`
- `E_CANON_EXPECTED`
- `E_F`
- `E_Q`
- `INVERSE_PERM`
- `PI_F`
- `PI_Q`
- `Q`
- `REPO_ROOT`
- `SYMBOL_PERM`
- `TRAPS`
- `T_F`
- `T_Q`
- `VALID`

## Classes and functions

- **function `strings`** [L48-49]: `def strings(length: int) -> list[tuple[int, ...]]`
- **function `exact`** [L53-58]: `def exact(suffix: tuple[int, ...]) -> tuple[Fraction, ...] | None` decorators: @lru_cache(maxsize=None) - Exact posterior of the float model by path enumeration; None when impossible.
- **function `gap`** [L61-62]: `def gap(values, fracs) -> float`
- **function `named`** [L65-66]: `def named(row: tuple[int, ...]) -> tuple[int, ...]`
- **function `prod_one`** [L70-73]: `def prod_one(row: tuple[int, ...], K: int, canonical: bool = False) -> np.ndarray` decorators: @lru_cache(maxsize=None) - Production posterior of one row (canonical tokens with the canonical emission if asked).
- **function `wrong_filter`** [L76-91]: `def wrong_filter(T, E, init, symbols, *, transpose=False, extra_step=False)` - Plain float forward filter with switchable MISTAKES (test-only, never production).
- **function `last`** [L94-95]: `def last(row, K)`
- **function `correct`** [L133-134]: `def correct(row, K, canonical)`
- **test `test_trap_differs_from_enumeration_while_production_matches`** [L138-157]: `def test_trap_differs_from_enumeration_while_production_matches(name)` decorators: @pytest.mark.parametrize('name', sorted(TRAPS)) - Item 3 (a)-(d), plus the two restart traps of item 2.
- **test `test_tokens_before_suffix_have_no_effect`** [L160-174]: `def test_tokens_before_suffix_have_no_effect()` - Item 2: every prefix (even ones making the full row impossible) leaves post_K unchanged.
- **test `test_restart_uses_stationary_pi`** [L177-181]: `def test_restart_uses_stationary_pi()` - Item 2: post_1 of (..., 0) is pi * E[:, 0] normalised, whatever came before.
- **test `test_canonical_emission_is_the_column_permutation`** [L184-191]: `def test_canonical_emission_is_the_column_permutation()` - Item 4.
- **test `test_canonical_filtering_equals_named_filtering`** [L194-210]: `def test_canonical_filtering_equals_named_filtering()` - Item 4: canonical tokens with E_canon == named tokens symbol_perm[canonical] with E_named.
- **test `test_canonical_emission_rejects_non_permutations`** [L218-221]: `def test_canonical_emission_rejects_non_permutations(perm)` decorators: @pytest.mark.parametrize('perm', [[0, 0, 1], [0, 1, 3], [0, 1], [3, 0, 1, 2], [-1, 0, 1], [0.0, 1.5, 2.0], [[0, 1, 2]]], ids=['repeat', 'out_of_range', 'too_short', 'too_long', 'negative', 'non_integer', 'two_d']) - Item 4.
- **test `test_suffix_posterior_error_paths`** [L246-250]: `def test_suffix_posterior_error_paths(name)` decorators: @pytest.mark.parametrize('name', sorted(BAD_CALLS)) - Item 6.
- **test `test_integer_dtypes_and_numpy_integer_K_are_accepted`** [L253-261]: `def test_integer_dtypes_and_numpy_integer_K_are_accepted()`
- **test `test_inputs_are_not_mutated`** [L264-271]: `def test_inputs_are_not_mutated()`

