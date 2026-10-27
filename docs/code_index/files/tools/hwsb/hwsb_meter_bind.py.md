# `tools/hwsb/hwsb_meter_bind.py`

- Source: [tools/hwsb/hwsb_meter_bind.py](../../../../../tools/hwsb/hwsb_meter_bind.py)
- Kind: python
- Lines: 121

## Module docstring

> HWSB meter binding (API.md §10; protocol §6.4 rule 1, §9.1, RC-5).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 11, via same directory)
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

- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 25, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 21, import)

## Top-level constants

- `MEMORY_CAP`

## Classes and functions

- **function `job_paths`** [L24-30]: `def job_paths(job, kind) -> dict`
- **function `bind`** [L33-36]: `def bind(job_id, task_sha256, out, worker_session, temp_root=None) -> None`
- **function `_outside`** [L39-46]: `def _outside(p, root) -> bool`
- **function `_under`** [L49-50]: `def _under(p, base) -> bool`
- **function `placement_ok`** [L53-69]: `def placement_ok(paths, root=hc.ROOT) -> dict`
- **function `effective_settings`** [L72-80]: `def effective_settings() -> dict`
- **function `_pop`** [L83-88]: `def _pop(argv, flag)`
- **function `main`** [L91-117]: `def main() -> int` - --job, --task-sha256, --session, --kind (all required), then the meter argv.

