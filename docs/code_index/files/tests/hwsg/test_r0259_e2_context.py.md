# `tests/hwsg/test_r0259_e2_context.py`

- Source: [tests/hwsg/test_r0259_e2_context.py](../../../../../tests/hwsg/test_r0259_e2_context.py)
- Kind: python
- Lines: 85

## Module docstring

> R-0259-1: run_e2 sets ctx["test_acts"] as stage C does, and every ctx key read after H2-FRESH
> is present (API.md section 25).

## Imports

### Internal (repo files)

- `from test_b_common import mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 13, via same directory)

### External (third-party)

- `numpy` (lines 10)

### Standard library

- `__future__` (lines 4)
- `importlib` (lines 6)
- `pathlib` (lines 8)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 69: `k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md)
- `import_module` line 71: `c1_model` -> [tools/c1prime/c1_model.py](../../tools/c1prime/c1_model.py.md)

### sys.path additions

- line 12: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_run_e2_context_reaches_t_pre_endpoint_ratio_and_export`** [L16-85]: `def test_run_e2_context_reaches_t_pre_endpoint_ratio_and_export(tmp_path, monkeypatch)`

