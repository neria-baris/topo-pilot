# `tests/hwsg/test_b_common.py`

- Source: [tests/hwsg/test_b_common.py](../../../../../tests/hwsg/test_b_common.py)
- Kind: python
- Lines: 64

## Module docstring

> Shared helpers of author B (no tests here). Imports are lazy so collection never fails.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `pytest` (lines 10)

### Standard library

- `__future__` (lines 2)
- `fractions` (lines 7)
- `hashlib` (lines 56)
- `importlib` (lines 4)
- `json` (lines 5)
- `pathlib` (lines 8)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 29: `hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md)
- `import_module` line 30: `dynamic: name`
- `import_module` line 42: `c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md)

### sys.path additions

- line 15: `str(_p)` -> `tools/hwsg`

## Imported by

- [tests/hwsg/test_b_binding.py](test_b_binding.py.md) (line 13, import)
- [tests/hwsg/test_b_guard.py](test_b_guard.py.md) (line 12, import)
- [tests/hwsg/test_b_handoff_oracle.py](test_b_handoff_oracle.py.md) (line 15, import)
- [tests/hwsg/test_b_records.py](test_b_records.py.md) (line 14, import)
- [tests/hwsg/test_b_registry.py](test_b_registry.py.md) (line 16, import)
- [tests/hwsg/test_b_streams.py](test_b_streams.py.md) (line 12, import)
- [tests/hwsg/test_b_train_meter.py](test_b_train_meter.py.md) (line 11, import)
- [tests/hwsg/test_r0257_store_paths.py](test_r0257_store_paths.py.md) (line 12, import)

## Top-level constants

- `ALIASES`
- `CONTRACT`
- `F`
- `GIB`
- `REPO`
- `TAGS`

## Classes and functions

- **function `mod`** [L25-32]: `def mod(alias_or_name)`
- **function `status_of`** [L35-37]: `def status_of(exc) -> str`
- **function `expect_fail`** [L40-47]: `def expect_fail(status_prefix, fn, *a, **k)`
- **function `ok_of`** [L50-52]: `def ok_of(r) -> bool`
- **function `sha_bytes`** [L55-57]: `def sha_bytes(b: bytes) -> str`
- **function `is_incomplete`** [L60-61]: `def is_incomplete(out: dict) -> bool`

