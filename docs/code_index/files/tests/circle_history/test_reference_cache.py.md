# `tests/circle_history/test_reference_cache.py`

- Source: [tests/circle_history/test_reference_cache.py](../../../../../tests/circle_history/test_reference_cache.py)
- Kind: python
- Lines: 227

## Module docstring

> Independent tests (author B) for reference_cache.py: TEST_PLAN item B12 (spec v2.4).

## Imports

### Internal (repo files)

- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 29, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 30, via sys.path edit)
- `import reference_cache` -> [tools/x4_circle_history/reference_cache.py](../../tools/x4_circle_history/reference_cache.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 21)
- `pytest` (lines 22)

### Standard library

- `__future__` (lines 12)
- `copy` (lines 14)
- `decimal` (lines 18)
- `hashlib` (lines 15)
- `json` (lines 16)
- `pathlib` (lines 19)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `COORDS`
- `E`
- `HIDS`
- `HIST`
- `MISMATCHES`
- `MUTATIONS`
- `PI`
- `REPO_ROOT`
- `SEQ`
- `T`
- `VALUES`
- `_CHANGED_HIST`

## Classes and functions

- **function `_sha_file`** [L48-49]: `def _sha_file(rel: str) -> str`
- **function `_hex`** [L52-53]: `def _hex(row) -> str`
- **function `ident`** [L57-58]: `def ident() -> dict` decorators: @pytest.fixture(scope='module')
- **function `_cache`** [L61-68]: `def _cache(digest: str, rows=range(4), ks=(4, 32)) -> dict`
- **function `_rows`** [L71-75]: `def _rows() -> list[dict]`
- **function `obj`** [L79-81]: `def obj(ident) -> dict` decorators: @pytest.fixture()
- **test `test_identity_fields`** [L84-96]: `def test_identity_fields(ident) -> None`
- **test `test_export_entries_sorted_and_exact`** [L99-106]: `def test_export_entries_sorted_and_exact(ident) -> None`
- **test `test_round_trip_is_exact_without_float`** [L109-117]: `def test_round_trip_is_exact_without_float(ident, obj) -> None`
- **function `_mutations`** [L120-150]: `def _mutations() -> dict`
- **test `test_load_cache_rejects_every_mutation`** [L157-161]: `def test_load_cache_rejects_every_mutation(ident, obj, name: str) -> None` decorators: @pytest.mark.parametrize('name', sorted(MUTATIONS))
- **test `test_load_cache_rejects_a_different_expected_identity`** [L164-173]: `def test_load_cache_rejects_a_different_expected_identity(ident, obj) -> None`
- **function `_verify`** [L177-184]: `def _verify(o, **changes)`
- **test `test_verify_rows_passes_on_the_exact_table`** [L187-191]: `def test_verify_rows_passes_on_the_exact_table(obj) -> None`
- **test `test_verify_rows_rejects_every_mismatch`** [L207-209]: `def test_verify_rows_rejects_every_mismatch(obj, name: str) -> None` decorators: @pytest.mark.parametrize('name', sorted(MISMATCHES))
- **test `test_verify_rows_rejects_missing_record_entry_and_duplicate_record`** [L212-227]: `def test_verify_rows_rejects_missing_record_entry_and_duplicate_record(obj) -> None`

