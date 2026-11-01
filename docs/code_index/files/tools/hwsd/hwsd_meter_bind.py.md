# `tools/hwsd/hwsd_meter_bind.py`

- Source: [tools/hwsd/hwsd_meter_bind.py](../../../../../tools/hwsd/hwsd_meter_bind.py)
- Kind: python
- Lines: 130

## Module docstring

> HWSD meter binding (API.md §13; protocol §11.3; DRD12).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 11, via same directory)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 16, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 17, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 18, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 19, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 9)
- `os` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 19, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 39, import)

## Top-level constants

- `INF`

## Classes and functions

- **function `job_paths`** [L24-30]: `def job_paths(job, kind) -> dict`
- **function `memory_cap`** [L33-37]: `def memory_cap(stage) -> int`
- **function `bind`** [L40-46]: `def bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None`
- **function `_outside`** [L49-56]: `def _outside(p, root) -> bool`
- **function `_under`** [L59-60]: `def _under(p, base) -> bool`
- **function `placement_ok`** [L63-75]: `def placement_ok(paths, root=dc.ROOT) -> dict`
- **function `child_env_d`** [L78-82]: `def child_env_d(job) -> dict` - k4b_meter_bind.child_env(job) with its TEMP folder created (the D-0177-1 fix).
- **function `effective_settings`** [L85-88]: `def effective_settings() -> dict`
- **function `_pop`** [L91-96]: `def _pop(argv, flag)`
- **function `main`** [L99-126]: `def main() -> int` - --job, --task-sha256, --session, --kind, --stage (all required), then the meter argv.

