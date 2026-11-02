# `tests/hwsd/test_c_continue.py`

- Source: [tests/hwsd/test_c_continue.py](../../../../../tests/hwsd/test_c_continue.py)
- Kind: python
- Lines: 200

## Module docstring

> Coordinator 080a3e03 (jobs 0208, 0210; owner addendum 42).

## Imports

### Internal (repo files)

- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](../../tools/hwsd/hwsd_driver.py.md) (line 17, via sys.path edit)
- `import hwsd_jobs` -> [tools/hwsd/hwsd_jobs.py](../../tools/hwsd/hwsd_jobs.py.md) (line 18, via sys.path edit)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](../../tools/hwsd/hwsd_known.py.md) (line 19, via sys.path edit)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](../../tools/hwsd/hwsd_records.py.md) (line 20, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 98, via unique basename) (inside a function)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](../../tools/hwsd/hwsd_bind.py.md) (line 99, via sys.path edit) (inside a function)
- `import hwsd_dry` -> [tools/hwsd/hwsd_dry.py](../../tools/hwsd/hwsd_dry.py.md) (line 100, via sys.path edit) (inside a function)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 144, via sys.path edit) (inside a function)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 166, via unique basename) (inside a function)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 195, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 101)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 7)
- `hashlib` (lines 142)
- `json` (lines 9)
- `os` (lines 164)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 15: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **class `_Stop(BaseException)`** [L24-25]
- **test `test_cli_passes_continue`** [L29-42]: `def test_cli_passes_continue(cmd, tmp_path, monkeypatch)` decorators: @pytest.mark.parametrize('cmd', ['kd', 'sample', 'summary'])
- **test `test_cli_without_continue_passes_none`** [L45-50]: `def test_cli_without_continue_passes_none(tmp_path, monkeypatch)`
- **test `test_run_kd_hands_cont_to_the_pause_check`** [L53-63]: `def test_run_kd_hands_cont_to_the_pause_check(tmp_path, monkeypatch)`
- **test `test_sample_and_summary_wrappers_honour_a_continuation`** [L66-73]: `def test_sample_and_summary_wrappers_honour_a_continuation(tmp_path, monkeypatch)`
- **test `test_kd1_passes_when_ident_d_returns`** [L76-93]: `def test_kd1_passes_when_ident_d_returns(tmp_path, monkeypatch)`
- **test `test_kd_end_to_end_with_stub_items_leaves_no_arrays_in_store`** [L96-134]: `def test_kd_end_to_end_with_stub_items_leaves_no_arrays_in_store(tmp_path, monkeypatch)` - R-0209-2: KD4 runs unbound with output outside the store; KD closes with an obligation.
- **test `test_reservation_end_accepts_a_root_relative_obligation`** [L140-159]: `def test_reservation_end_accepts_a_root_relative_obligation(rel, ended, tmp_path)` decorators: @pytest.mark.parametrize('rel,ended', [('hwsu-store/REGISTRY_OBLIGATION_OF.json', True), ('REGISTRY_OBLIGATION_OF.json', True), ('other/REGISTRY_OBLIGATION_OF.json', False)]) - R-0213-1: track U names the obligation relative to the root (J8 leaves it open).
- **test `test_timed_factory_d_matches_op_guard_and_retries_a_refused_replace`** [L162-190]: `def test_timed_factory_d_matches_op_guard_and_retries_a_refused_replace(tmp_path, monkeypatch)` - R-0216-1: the hwsd timed wrapper writes the op_guard records; survives a refused replace.
- **test `test_archived_score_arrays_are_classified`** [L193-200]: `def test_archived_score_arrays_are_classified(tmp_path)` - R-0216-2: arrays archived to superseded/<job>-a<k>/ keep their name-rule class.

