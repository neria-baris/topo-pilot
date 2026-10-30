# `tests/hwsc/test_r_0177_meter_tempdir.py`

- Source: [tests/hwsc/test_r_0177_meter_tempdir.py](../../../../../tests/hwsc/test_r_0177_meter_tempdir.py)
- Kind: python
- Lines: 35

## Module docstring

> Regression D-0177-1 (coordinator 08ad4eaf, job 0177).

## Imports

### Internal (repo files)

- `import hwsc_meter_bind` -> [tools/hwsc/hwsc_meter_bind.py](../../tools/hwsc/hwsc_meter_bind.py.md) (line 18, via sys.path edit)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 19, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `pathlib` (lines 12)
- `subprocess` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **test `test_child_env_creates_temp_and_child_uses_it`** [L22-35]: `def test_child_env_creates_temp_and_child_uses_it(tmp_path, monkeypatch)`

