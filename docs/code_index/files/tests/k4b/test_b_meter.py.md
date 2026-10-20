# `tests/k4b/test_b_meter.py`

- Source: [tests/k4b/test_b_meter.py](../../../../../tests/k4b/test_b_meter.py)
- Kind: python
- Lines: 303

## Module docstring

> Author B, K4b TEST_PLAN B19 and B20: the actual meter bindings (controls, meter, winjob values
> after bind; --max-cpu inf --max-wall inf; op_guard deadline per operation, not per stage; child
> TEMP/TMP/TMPDIR on X:; worker session and RUN.lock identity from the release) and the limiter
> order: STOP/INVALID keep reason and state; HOLD alone never kills, a resource reason may kill
> under HOLD with the HOLD state returned; legacy (latch processing) runs exactly once per poll;
> ordinary overdue and disk failures, including unreadable free space.

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 26, via sys.path edit)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 27, via sys.path edit)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 28, via sys.path edit)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 29, via sys.path edit)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 30, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)

### External (third-party)

- `pytest` (lines 24)

### Standard library

- `__future__` (lines 10)
- `argparse` (lines 12)
- `collections` (lines 13)
- `os` (lines 14)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `DISK_REASON`
- `INF`
- `METER_NAMES`
- `REPO`
- `TEMP`

## Classes and functions

- **function `preserved`** [L41-48]: `def preserved(monkeypatch)` decorators: @pytest.fixture - Record every module global bind() may rebind, so monkeypatch restores it afterwards.
- **test `test_bind_sets_every_registered_value`** [L53-66]: `def test_bind_sets_every_registered_value(tmp_path, preserved)`
- **test `test_run_lock_identity_follows_the_release_session`** [L69-75]: `def test_run_lock_identity_follows_the_release_session(tmp_path, preserved)`
- **test `test_rewrite_argv_forces_infinite_cpu_and_wall`** [L83-90]: `def test_rewrite_argv_forces_infinite_cpu_and_wall(argv)` decorators: @pytest.mark.parametrize('argv', [['meter.py', '--label', 'S3', '--max-cpu', '600', '--max-wall', '3600'], ['meter.py', '--max-wall', '10', '--label', 'S3'], ['meter.py', '--label', 'S3']])
- **test `test_child_env_temp_on_x_and_single_thread`** [L93-103]: `def test_child_env_temp_on_x_and_single_thread()`
- **test `test_child_env_default_copies_os_environ`** [L106-110]: `def test_child_env_default_copies_os_environ()`
- **test `test_main_without_valid_release_never_runs_the_meter`** [L113-128]: `def test_main_without_valid_release_never_runs_the_meter(tmp_path, preserved)`
- **test `test_op_guard_deadline_is_per_operation`** [L131-152]: `def test_op_guard_deadline_is_per_operation(tmp_path)`
- **class `Legacy`** [L157-163]
- **method `Legacy.__init__`** [L158-159]: `def __init__(self, result)`
- **method `Legacy.__call__`** [L161-163]: `def __call__(self, ledger, child, args, active_wall, polls, mailboxes)`
- **class `Disk`** [L166-172]
- **method `Disk.__init__`** [L167-168]: `def __init__(self, reason)`
- **method `Disk.__call__`** [L170-172]: `def __call__(self)`
- **function `overdue_marker`** [L178-181]: `def overdue_marker(tmp_path)`
- **function `poll`** [L184-185]: `def poll(lim, polls=8)`
- **test `test_stop_and_invalid_keep_precedence_over_overdue_and_disk`** [L190-196]: `def test_stop_and_invalid_keep_precedence_over_overdue_and_disk(tmp_path, control)` decorators: @pytest.mark.parametrize('control', [('STOP: owner STOP file', controls.STOP), ('INVALID: control unreadable', controls.INVALID)])
- **test `test_hold_without_resource_failure_never_kills`** [L199-206]: `def test_hold_without_resource_failure_never_kills(tmp_path)`
- **test `test_hold_with_overdue_operation_kills_and_keeps_hold`** [L209-216]: `def test_hold_with_overdue_operation_kills_and_keeps_hold(tmp_path)`
- **test `test_hold_with_disk_failure_kills_and_keeps_hold`** [L219-225]: `def test_hold_with_disk_failure_kills_and_keeps_hold()`
- **test `test_ordinary_overdue_beats_disk_and_returns_control_state`** [L228-235]: `def test_ordinary_overdue_beats_disk_and_returns_control_state(tmp_path)`
- **test `test_not_yet_overdue_and_disk_only_every_eighth_poll`** [L238-245]: `def test_not_yet_overdue_and_disk_only_every_eighth_poll(tmp_path)`
- **test `test_default_legacy_is_the_original_meter_limit_reason`** [L248-260]: `def test_default_legacy_is_the_original_meter_limit_reason(tmp_path, preserved)`
- **function `usage_of`** [L265-268]: `def usage_of(free)`
- **test `test_disk_minima_registered`** [L271-272]: `def test_disk_minima_registered()`
- **test `test_disk_reason_none_at_or_above_minimum`** [L275-277]: `def test_disk_reason_none_at_or_above_minimum()`
- **test `test_disk_reason_below_minimum`** [L281-286]: `def test_disk_reason_below_minimum(drive, low)` decorators: @pytest.mark.parametrize('drive,low', [('C:\\', 1999999999), ('X:\\', 29999999999)])
- **test `test_disk_reason_unreadable_free_space`** [L289-298]: `def test_disk_reason_unreadable_free_space()`
- **test `test_output_cap_reason_is_a_resource_stop`** [L301-303]: `def test_output_cap_reason_is_a_resource_stop()`

