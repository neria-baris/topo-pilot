# `tests/hwsc/test_r_0192_output_cap.py`

- Source: [tests/hwsc/test_r_0192_output_cap.py](../../../../../tests/hwsc/test_r_0192_output_cap.py)
- Kind: python
- Lines: 29

## Module docstring

> Coordinator-written regression test for defect D-0192-1 (API.md §28): the meter's output cap
> applies to the whole out directory (for store jobs, all of hwsc-store with its three registries),
> so it is read from CONTRACT resources.output_cap_bytes (16 GiB), not fixed at 4 GiB.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 13, via sys.path edit)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 14, via unique basename)
- `import hwsc_meter_bind` -> [tools/hwsc/hwsc_meter_bind.py](../../tools/hwsc/hwsc_meter_bind.py.md) (line 15, via sys.path edit)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 16, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 17, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 18, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `pathlib` (lines 8)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **test `test_output_cap_comes_from_the_contract`** [L21-29]: `def test_output_cap_comes_from_the_contract(tmp_path, monkeypatch)`

