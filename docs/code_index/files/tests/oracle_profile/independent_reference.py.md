# `tests/oracle_profile/independent_reference.py`

- Source: [tests/oracle_profile/independent_reference.py](../../../../../tests/oracle_profile/independent_reference.py)
- Kind: python
- Lines: 176

## Module docstring

> Independent numerical reference for x4_oracle_profile suffix posteriors (job 0014).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 27)

### Standard library

- `__future__` (lines 20)
- `decimal` (lines 23)
- `fractions` (lines 24)
- `itertools` (lines 22)
- `typing` (lines 25)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_exceptions.py](../c1prime/test_a_exceptions.py.md) (line 34, import)
- [tests/c1prime/test_b_cert_oracle.py](../c1prime/test_b_cert_oracle.py.md) (line 37, import)
- [tests/circle_history/test_builder_v24_stages.py](../circle_history/test_builder_v24_stages.py.md) (line 102, import)
- [tests/circle_history/test_error_bound.py](../circle_history/test_error_bound.py.md) (line 28, import)
- [tests/circle_history/test_scores_precision.py](../circle_history/test_scores_precision.py.md) (line 27, import)
- [tests/d1_seam/test_d1_seam.py](../d1_seam/test_d1_seam.py.md) (line 30, import)
- [tests/oracle_profile/test_oracle_profile.py](test_oracle_profile.py.md) (line 30, import)
- [tests/oracle_profile/test_oracle_profile_traps.py](test_oracle_profile_traps.py.md) (line 29, import)
- [tests/x6_stage0/test_x6_stage0_dp.py](../x6_stage0/test_x6_stage0_dp.py.md) (line 29, import)
- [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 13, import)
- [tools/d1_seam/d1_seam_checks.py](../../tools/d1_seam/d1_seam_checks.py.md) (line 17, import)
- [tools/x2a_stage0/x2a_mc.py](../../tools/x2a_stage0/x2a_mc.py.md) (line 16, import)
- [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 23, import)
- [tools/x4_circle_history/live_context.py](../../tools/x4_circle_history/live_context.py.md) (line 35, import)
- [tools/x4_oracle_profile/validation.py](../../tools/x4_oracle_profile/validation.py.md) (line 15, import)
- [tools/x6_stage0/x6_run.py](../../tools/x6_stage0/x6_run.py.md) (line 21, import)

## Top-level constants

- `MIN_DIGITS`
- `_MEAN_DIGITS`

## Classes and functions

- **function `_matrix`** [L33-38]: `def _matrix(values: Any, name: str) -> list[list[Any]]` - Read a 2-D input (numpy array or nested sequence) into a list of rows of scalars.
- **function `_vector`** [L41-46]: `def _vector(values: Any, name: str) -> list[Any]` - Read a 1-D input into a list of scalars.
- **function `_check_shapes`** [L49-56]: `def _check_shapes(T: list[list[Any]], E: list[list[Any]], pi: list[Any]) -> tuple[int, int]` - Return (S, V) after checking T [S, S], E [S, V], pi [S].
- **function `_symbols`** [L59-67]: `def _symbols(suffix: Any, n_symbols: int) -> list[int]` - Read the suffix as a non-empty list of Python ints in 0 .. V-1.
- **function `_as_fraction`** [L70-76]: `def _as_fraction(x: Any) -> Fraction` - Exact conversion: Fractions and ints kept, everything else via float (exact binary value).
- **function `_as_decimal`** [L79-83]: `def _as_decimal(x: Any) -> Decimal` - Exact conversion Decimal(float(x)) as required by API.md section 3.
- **function `decimal_suffix_posterior`** [L86-122]: `def decimal_suffix_posterior(T: Any, E: Any, pi: Any, suffix: Any, digits: int = MIN_DIGITS) -> list[Decimal]` - Suffix posterior by unnormalised forward summation in decimal arithmetic.
- **function `decimal_circular_mean`** [L125-144]: `def decimal_circular_mean(posterior: Sequence[Decimal], features: Any) -> tuple[Decimal, Decimal]` - Posterior circular mean ``sum_s posterior[s] * features[s]`` in decimal arithmetic.
- **function `enumerate_posterior`** [L147-176]: `def enumerate_posterior(T: Any, E: Any, pi: Any, suffix: Any) -> list[Fraction]` - Suffix posterior by exhaustive enumeration of all S**K state paths, in exact Fractions.

