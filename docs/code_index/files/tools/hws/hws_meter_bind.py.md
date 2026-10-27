# `tools/hws/hws_meter_bind.py`

- Source: [tools/hws/hws_meter_bind.py](../../../../../tools/hws/hws_meter_bind.py)
- Kind: python
- Lines: 71

## Module docstring

> HWS meter binding (API.md §7; protocol §9.2, §12.1, RC-9).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 14, via same directory)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 15, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 16, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 17, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 18, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `os` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 32, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 170, import)

## Top-level constants

- `MEMORY_CAP`

## Classes and functions

- **function `bind`** [L23-26]: `def bind(job_id, task_sha256, out, worker_session) -> None`
- **function `effective_settings`** [L29-37]: `def effective_settings() -> dict`
- **function `_pop`** [L40-45]: `def _pop(argv, flag)`
- **function `main`** [L48-67]: `def main() -> int` - --job, --task-sha256, --session, --out (all required; choice 30), then the meter argv.

