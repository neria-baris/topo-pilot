# `tools/hwsu/hwsu_meter_bind.py`

- Source: [tools/hwsu/hwsu_meter_bind.py](../../../../../tools/hwsu/hwsu_meter_bind.py)
- Kind: python
- Lines: 120

## Module docstring

> HWSU meter binding (API.md §8; protocol §10.3): thin main over the unchanged K4b binding.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 5, via same directory)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 10, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 11, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 12, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 13, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
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

- none

## Imported by

- [tests/hwsu/test_b_of_meter.py](../../tests/hwsu/test_b_of_meter.py.md) (line 19, import)
- [tests/hwsu/test_b_u2_records.py](../../tests/hwsu/test_b_u2_records.py.md) (line 192, dynamic)
- [tests/hwsu/test_b_u2_records.py](../../tests/hwsu/test_b_u2_records.py.md) (line 203, dynamic)
- [tools/hwsu/u2/hwsu_driver.py](u2/hwsu_driver.py.md) (line 13, import)

## Top-level constants

- `INF`

## Classes and functions

- **function `job_paths`** [L18-28]: `def job_paths(job, kind) -> dict`
- **function `memory_cap`** [L31-35]: `def memory_cap(stage) -> int`
- **function `bind`** [L38-44]: `def bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None`
- **function `child_env_u`** [L47-50]: `def child_env_u(job) -> dict`
- **function `_outside`** [L53-60]: `def _outside(p, root) -> bool`
- **function `placement_ok`** [L63-73]: `def placement_ok(paths, root=uc.ROOT) -> dict`
- **function `effective_settings`** [L76-79]: `def effective_settings() -> dict`
- **function `_pop`** [L82-87]: `def _pop(argv, flag)`
- **function `main`** [L90-116]: `def main() -> int`

