# `tools/k4b/k4b_meter_bind.py`

- Source: [tools/k4b/k4b_meter_bind.py](../../../../../tools/k4b/k4b_meter_bind.py)
- Kind: python
- Lines: 148

## Module docstring

> K4b meter binding (API.md §12.2; protocol §11.7, RC11).

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 17, via same directory)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 18, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 19, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 20, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 21, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](k4b_release.py.md) (line 123, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 9)
- `os` (lines 11)
- `pathlib` (lines 15)
- `shutil` (lines 12)
- `sys` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 35, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 27, import)
- [tests/hwsc/test_b_guard_meter.py](../../tests/hwsc/test_b_guard_meter.py.md) (line 33, import)
- [tests/hwsc/test_r_0177_meter_tempdir.py](../../tests/hwsc/test_r_0177_meter_tempdir.py.md) (line 19, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 27, import)
- [tools/hws/hws_dry.py](../hws/hws_dry.py.md) (line 171, import)
- [tools/hws/hws_meter_bind.py](../hws/hws_meter_bind.py.md) (line 15, import)
- [tools/hwsb/hwsb_meter_bind.py](../hwsb/hwsb_meter_bind.py.md) (line 16, import)
- [tools/hwsc/hwsc_dry3.py](../hwsc/hwsc_dry3.py.md) (line 18, import)
- [tools/hwsc/hwsc_meter_bind.py](../hwsc/hwsc_meter_bind.py.md) (line 17, import)

## Top-level constants

- `DISK_MIN_FREE`
- `INF`
- `LEGACY_LIMIT`
- `RESOURCE_MARKS`
- `TEMP_ROOT`

## Classes and functions

- **function `bind`** [L30-43]: `def bind(job_id, task_sha256, out, worker_session) -> None`
- **function `disk_reason`** [L46-54]: `def disk_reason(usage=shutil.disk_usage, minima=DISK_MIN_FREE)`
- **function `make_limiter`** [L57-74]: `def make_limiter(op_marker, disk=disk_reason, legacy=None, clock=time.time)`
- **function `rewrite_argv`** [L77-92]: `def rewrite_argv(argv) -> list`
- **function `child_env`** [L95-101]: `def child_env(job, base=None) -> dict`
- **function `classify_stop`** [L104-110]: `def classify_stop(reason, state) -> str`
- **function `_pop`** [L113-118]: `def _pop(argv, flag)`
- **function `main`** [L121-144]: `def main() -> int` - --release (required), --kind (A|B), --task-sha256, --session; then the meter argv.

