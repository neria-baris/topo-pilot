# `tests/hwsb/test_r_0168_kb_default_store.py`

- Source: [tests/hwsb/test_r_0168_kb_default_store.py](../../../../../tests/hwsb/test_r_0168_kb_default_store.py)
- Kind: python
- Lines: 36

## Module docstring

> Regression D-0168-1 (coordinator 08ad4eaf, job 0168).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 19, via sys.path edit)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../../tools/hwsb/hwsb_driver.py.md) (line 20, via sys.path edit)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 21, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 9)
- `json` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **test `test_run_kb_default_store_reaches_kb0`** [L24-36]: `def test_run_kb_default_store_reaches_kb0(tmp_path, monkeypatch)`

