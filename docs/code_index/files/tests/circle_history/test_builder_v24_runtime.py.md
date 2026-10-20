# `tests/circle_history/test_builder_v24_runtime.py`

- Source: [tests/circle_history/test_builder_v24_runtime.py](../../../../../tests/circle_history/test_builder_v24_runtime.py)
- Kind: python
- Lines: 222

## Module docstring

> BUILDER tests (not independent) for spec v2.4 items 7, 11, 12 and 13: native-operation wall
> guard (op_guard + meter_bind limiter, one short real metered kill on a temporary store), disk
> safe-STOP, ledger allocation sync, dependency manifest and numerical identity. Injected clocks;
> nothing waits 180 s. See BUILDER_TESTS.md.

## Imports

### Internal (repo files)

- `import env_identity` -> [tools/x4_circle_history/env_identity.py](../../tools/x4_circle_history/env_identity.py.md) (line 23, via sys.path edit)
- `import meter_bind` -> [tools/x4_circle_history/meter_bind.py](../../tools/x4_circle_history/meter_bind.py.md) (line 24, via sys.path edit)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 25, via sys.path edit)
- `from errors import Unresolved` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 26, via sys.path edit)
- `import freeze_bind` -> [tools/x4_circle_history/freeze_bind.py](../../tools/x4_circle_history/freeze_bind.py.md) (line 193, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 214)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 13)
- `subprocess` (lines 10)
- `sys` (lines 11)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BASE_PYTHON`
- `CHILD`
- `DRIVER`
- `REPO`
- `TOOL`

## Classes and functions

- **function `_events`** [L31-32]: `def _events(out)`
- **test `test_timed_records_start_end_and_marker`** [L35-40]: `def test_timed_records_start_end_and_marker(tmp_path)`
- **test `test_timed_error_is_logged_and_reraised`** [L43-47]: `def test_timed_error_is_logged_and_reraised(tmp_path)`
- **test `test_timed_post_return_check_with_injected_clock`** [L50-55]: `def test_timed_post_return_check_with_injected_clock(tmp_path)`
- **function `_marker`** [L58-63]: `def _marker(tmp_path, started, deadline=180.0, state='active')`
- **test `test_limiter_kills_overdue_operation_only`** [L66-77]: `def test_limiter_kills_overdue_operation_only(tmp_path)`
- **test `test_disk_safe_stop_reason`** [L80-95]: `def test_disk_safe_stop_reason()`
- **test `test_archive_stale_marker`** [L98-102]: `def test_archive_stale_marker(tmp_path)`
- **function `_ledger`** [L105-114]: `def _ledger(caps, entries)`
- **test `test_ledger_allocation_sync_preserves_entries`** [L117-132]: `def test_ledger_allocation_sync_preserves_entries(tmp_path)`
- **function `_synthetic_mailbox`** [L157-167]: `def _synthetic_mailbox(tmp_path)` - Hermetic control inputs for the unchanged job-0014 controls (job 0021 revision).
- **test `test_real_meter_kills_overdue_marked_operation`** [L170-189]: `def test_real_meter_kills_overdue_marked_operation(tmp_path)`
- **test `test_frozen_files_bind_project_dependencies`** [L192-199]: `def test_frozen_files_bind_project_dependencies()`
- **test `test_unfrozen_project_module_detected`** [L202-210]: `def test_unfrozen_project_module_detected()`
- **test `test_numerical_identity_record_is_deterministic`** [L213-222]: `def test_numerical_identity_record_is_deterministic()`

