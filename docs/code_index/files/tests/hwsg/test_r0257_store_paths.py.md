# `tests/hwsg/test_r0257_store_paths.py`

- Source: [tests/hwsg/test_r0257_store_paths.py](../../../../../tests/hwsg/test_r0257_store_paths.py)
- Kind: python
- Lines: 56

## Module docstring

> R-0257-1: run_e2 hands the STORE (not the world folder) to the reused stage-C functions that
> read the store-level registry/K-REG2.json (API.md section 24).

## Imports

### Internal (repo files)

- `from test_b_common import mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 12, via same directory)

### External (third-party)

- `numpy` (lines 9)

### Standard library

- `__future__` (lines 4)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_run_e2_passes_store_to_release_b_and_h2_fresh`** [L15-56]: `def test_run_e2_passes_store_to_release_b_and_h2_fresh(tmp_path, monkeypatch)`

