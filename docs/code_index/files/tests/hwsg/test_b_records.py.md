# `tests/hwsg/test_b_records.py`

- Source: [tests/hwsg/test_b_records.py](../../../../../tests/hwsg/test_b_records.py)
- Kind: python
- Lines: 165

## Module docstring

> Author B: sealing, terminal RESULTs, S8 export, markers, barrier, cross inputs, ledger.

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, expect_fail, mod, ok_of` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 14, via same directory)

### External (third-party)

- `numpy` (lines 10)
- `pytest` (lines 11)

### Standard library

- `__future__` (lines 2)
- `hashlib` (lines 4)
- `json` (lines 5)
- `os` (lines 6)
- `pathlib` (lines 8)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- `TERMINAL_KEYS`

## Classes and functions

- **function `_sha`** [L19-20]: `def _sha(p)`
- **function `_events`** [L23-25]: `def _events(wd)`
- **function `_terminal`** [L28-34]: `def _terminal(tmp_path, tag='lo', status='INCONCLUSIVE/NOT_LEARNED')`
- **test `test_terminal_result_keys_exclusive_and_one_stage_complete`** [L37-52]: `def test_terminal_result_keys_exclusive_and_one_stage_complete(tmp_path)`
- **test `test_load_world_hash_checked`** [L55-61]: `def test_load_world_hash_checked(tmp_path)`
- **test `test_registered_world_without_result_is_lineage_not_exclusion`** [L64-68]: `def test_registered_world_without_result_is_lineage_not_exclusion(tmp_path)`
- **test `test_export_g_puts_four_files_in_one_s8_event`** [L71-90]: `def test_export_g_puts_four_files_in_one_s8_event(tmp_path)`
- **test `test_marker_replace_retries_permission_error`** [L93-109]: `def test_marker_replace_retries_permission_error(tmp_path, monkeypatch)`
- **function `_accept`** [L112-116]: `def _accept(wd, name, sha)`
- **function `_e1_accepted`** [L119-126]: `def _e1_accepted(tmp_path, tag)`
- **test `test_release_barrier`** [L129-138]: `def test_release_barrier(tmp_path)`
- **test `test_window_ok`** [L141-151]: `def test_window_ok(tmp_path)`
- **test `test_ledger_append_duplicate_label_refused`** [L154-165]: `def test_ledger_append_duplicate_label_refused(tmp_path)`

