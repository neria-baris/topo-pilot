# `tools/hwsc/hwsc_meter_bind.py`

- Source: [tools/hwsc/hwsc_meter_bind.py](../../../../../tools/hwsc/hwsc_meter_bind.py)
- Kind: python
- Lines: 137

## Module docstring

> HWSC meter binding (API.md §9; protocol §8.3, RC-13; DRC13).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 12, via same directory)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 17, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 18, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 19, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 20, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `os` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_guard_meter.py](../../tests/hwsc/test_b_guard_meter.py.md) (line 28, import)
- [tests/hwsc/test_r_0177_meter_tempdir.py](../../tests/hwsc/test_r_0177_meter_tempdir.py.md) (line 18, import)
- [tests/hwsc/test_r_0192_output_cap.py](../../tests/hwsc/test_r_0192_output_cap.py.md) (line 14, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 15, import)

## Top-level constants

- `CAPS`
- `INF`

## Classes and functions

- **function `job_paths`** [L26-32]: `def job_paths(job, kind) -> dict`
- **function `memory_cap`** [L35-39]: `def memory_cap(stage) -> int`
- **function `bind`** [L42-48]: `def bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None`
- **function `_outside`** [L51-58]: `def _outside(p, root) -> bool`
- **function `_under`** [L61-62]: `def _under(p, base) -> bool`
- **function `placement_ok`** [L65-78]: `def placement_ok(paths, root=cc.ROOT) -> dict`
- **function `effective_settings`** [L81-84]: `def effective_settings() -> dict`
- **function `_pop`** [L87-92]: `def _pop(argv, flag)`
- **function `child_env_c`** [L95-103]: `def child_env_c(job) -> dict` - k4b_meter_bind.child_env(job) with its TEMP folder created (D-0177-1).
- **function `main`** [L106-133]: `def main() -> int` - --job, --task-sha256, --session, --kind, --stage (all required), then the meter argv.

