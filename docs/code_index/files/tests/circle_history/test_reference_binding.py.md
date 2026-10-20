# `tests/circle_history/test_reference_binding.py`

- Source: [tests/circle_history/test_reference_binding.py](../../../../../tests/circle_history/test_reference_binding.py)
- Kind: python
- Lines: 215

## Module docstring

> Independent tests (author B) for the v2.4 error_bound corrections: TEST_PLAN item B11, plus the
> ERROR_BOUND.md v2.2 section 8 Taylor bounds and certify_rows "moment_check_max_by_K".

## Imports

### Internal (repo files)

- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 31, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 32, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 33, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 23)
- `pytest` (lines 24)

### Standard library

- `__future__` (lines 13)
- `decimal` (lines 19)
- `fractions` (lines 20)
- `hashlib` (lines 15)
- `itertools` (lines 16)
- `math` (lines 17)
- `pathlib` (lines 21)
- `sys` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `COORDS`
- `E`
- `E2`
- `E6`
- `E_BAD`
- `F`
- `FEATS`
- `HIST`
- `HIST6`
- `KS`
- `PHI`
- `PI`
- `REPO_ROOT`
- `T`

## Classes and functions

- **function `_digest`** [L54-61]: `def _digest(T_, E_, pi_, coords_) -> str` - process_digest recomputed from the written formula (API.md v2.4 item 2).
- **function `_row_bytes`** [L64-65]: `def _row_bytes(row) -> bytes`
- **function `_check`** [L68-69]: `def _check(E_, m_hat, hist=HIST, ks=KS, split='calibration', **kw) -> dict`
- **test `test_process_digest_matches_written_formula_and_binds_every_input`** [L73-91]: `def test_process_digest_matches_written_formula_and_binds_every_input() -> None`
- **test `test_cache_filled_under_one_process_never_hits_under_another`** [L95-112]: `def test_cache_filled_under_one_process_never_hits_under_another() -> None`
- **test `test_cache_only_hits_a_filled_cache`** [L115-121]: `def test_cache_only_hits_a_filled_cache() -> None`
- **test `test_cache_only_miss_raises_before_any_reference`** [L124-134]: `def test_cache_only_miss_raises_before_any_reference() -> None` - With E_BAD the reference itself would fail (impossible suffix); the miss error shows that
- **function `_malformed`** [L143-151]: `def _malformed() -> dict[str, np.ndarray]`
- **test `test_valid_histories_pass_for_signed_and_unsigned_dtypes`** [L154-159]: `def test_valid_histories_pass_for_signed_and_unsigned_dtypes() -> None`
- **test `test_malformed_histories_invalid_before_any_reference_work`** [L163-170]: `def test_malformed_histories_invalid_before_any_reference_work(name: str) -> None` decorators: @pytest.mark.parametrize('name', sorted(_malformed()))
- **function `_gap_cache`** [L174-176]: `def _gap_cache(mx_ref: Decimal) -> dict`
- **test `test_exact_gap_boundary_at_one_over_ten_to_the_ten`** [L179-190]: `def test_exact_gap_boundary_at_one_over_ten_to_the_ten() -> None`
- **test `test_certify_rows_reports_moment_check_by_k`** [L194-201]: `def test_certify_rows_reports_moment_check_by_k() -> None`
- **test `test_taylor_series_bounds_each_parity_separately`** [L205-215]: `def test_taylor_series_bounds_each_parity_separately() -> None`

