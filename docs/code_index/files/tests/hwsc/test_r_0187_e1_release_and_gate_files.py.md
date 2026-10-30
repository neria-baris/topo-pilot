# `tests/hwsc/test_r_0187_e1_release_and_gate_files.py`

- Source: [tests/hwsc/test_r_0187_e1_release_and_gate_files.py](../../../../../tests/hwsc/test_r_0187_e1_release_and_gate_files.py)
- Kind: python
- Lines: 95

## Module docstring

> Coordinator-written regression tests for defects D-0187-1 and D-0187-2 (API.md §27).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 18, via sys.path edit)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](../../tools/hwsc/hwsc_driver.py.md) (line 19, via sys.path edit)
- `import hwsc_jobs` -> [tools/hwsc/hwsc_jobs.py](../../tools/hwsc/hwsc_jobs.py.md) (line 20, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 22, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 67, via unique basename) (inside a function)

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

- line 16: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `_store`** [L27-34]: `def _store(tmp_path, monkeypatch)`
- **function `_release`** [L37-43]: `def _release(out, protocol)`
- **function `_gate_writing`** [L46-52]: `def _gate_writing(out, name)`
- **test `test_run_e1_accepts_a_stage_c_release_and_records_its_gate_files`** [L55-62]: `def test_run_e1_accepts_a_stage_c_release_and_records_its_gate_files(tmp_path, monkeypatch)`
- **test `test_run_e1_still_refuses_a_k4b_protocol_release`** [L65-76]: `def test_run_e1_still_refuses_a_k4b_protocol_release(tmp_path, monkeypatch)`
- **test `test_run_e2_records_h1c_e2`** [L79-95]: `def test_run_e2_records_h1c_e2(tmp_path, monkeypatch)`

