# `tests/hwsd/test_c_continue.py`

- Source: [tests/hwsd/test_c_continue.py](../../../../../tests/hwsd/test_c_continue.py)
- Kind: python
- Lines: 71

## Module docstring

> Coordinator 080a3e03 (job 0208, owner addendum 42).

## Imports

### Internal (repo files)

- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](../../tools/hwsd/hwsd_driver.py.md) (line 15, via sys.path edit)
- `import hwsd_jobs` -> [tools/hwsd/hwsd_jobs.py](../../tools/hwsd/hwsd_jobs.py.md) (line 16, via sys.path edit)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](../../tools/hwsd/hwsd_known.py.md) (line 17, via sys.path edit)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](../../tools/hwsd/hwsd_records.py.md) (line 18, via sys.path edit)

### External (third-party)

- `pytest` (lines 19)

### Standard library

- `__future__` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **class `_Stop(Exception)`** [L22-23]
- **test `test_cli_passes_continue`** [L27-40]: `def test_cli_passes_continue(cmd, tmp_path, monkeypatch)` decorators: @pytest.mark.parametrize('cmd', ['kd', 'sample', 'summary'])
- **test `test_cli_without_continue_passes_none`** [L43-48]: `def test_cli_without_continue_passes_none(tmp_path, monkeypatch)`
- **test `test_run_kd_hands_cont_to_the_pause_check`** [L51-61]: `def test_run_kd_hands_cont_to_the_pause_check(tmp_path, monkeypatch)`
- **test `test_sample_and_summary_wrappers_honour_a_continuation`** [L64-71]: `def test_sample_and_summary_wrappers_honour_a_continuation(tmp_path, monkeypatch)`

