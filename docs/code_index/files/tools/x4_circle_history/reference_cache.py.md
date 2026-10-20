# `tools/x4_circle_history/reference_cache.py`

- Source: [tools/x4_circle_history/reference_cache.py](../../../../../tools/x4_circle_history/reference_cache.py)
- Kind: python
- Lines: 125

## Module docstring

> Persisted exact reference moments (API.md spec v2.4 item 3; ERROR_BOUND.md v2.2 section 8).

## Imports

### Internal (repo files)

- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 17, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 32, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 10)
- `decimal` (lines 13)
- `hashlib` (lines 12)
- `pathlib` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime_registry/test_registry_builder.py](../../tests/c1prime_registry/test_registry_builder.py.md) (line 39, import)
- [tests/circle_history/test_reference_cache.py](../../tests/circle_history/test_reference_cache.py.md) (line 31, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 87, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 116, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 151, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 171, import)

## Top-level constants

- `HERE`
- `SCHEMA`
- `SOURCES`

## Classes and functions

- **function `identity`** [L30-42]: `def identity(T, E, pi, coords) -> dict` - Process, exact-feature and reference-source identities of a cache.
- **function `history_hex`** [L45-52]: `def history_hex(canonical32) -> list[str]` - int64-bytes hex per row; integer dtype, shape [n, 32] and nonnegative checked first.
- **function `export_cache`** [L55-61]: `def export_cache(cache: dict, ident: dict, rows: list) -> dict` - JSON-able cache: identity, row table and sorted exact entries.
- **function `_finite_decimal`** [L64-73]: `def _finite_decimal(text) -> Decimal`
- **function `load_cache`** [L76-94]: `def load_cache(obj: dict, ident_expected: dict) -> dict` - Rebuild {(digest, K, bytes): (Mx, My)} after verifying schema, identity and entries.
- **function `row_record`** [L97-106]: `def row_record(model, split, panel, history_id, sequence_id, canonical32) -> dict` - The row-table record export_cache stores for one model and split.
- **function `verify_rows`** [L109-125]: `def verify_rows(obj, model, split, panel, history_id, sequence_id, canonical32, Ks=(4, 32))` - Invalid unless the stored row table for (model, split) equals the reloaded rows exactly

