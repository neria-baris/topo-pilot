# `tools/c1prime/c1_meter_bind.py`

- Source: [tools/c1prime/c1_meter_bind.py](../../../../../tools/c1prime/c1_meter_bind.py)
- Kind: python
- Lines: 131

## Module docstring

> C1' binding of the unchanged job-0014 meter (API.md §14; protocol §18 field 2; standard
> library only; base interpreter, -I). Rebinds module-level names of meter/controls/winjob: job
> and task digest, store paths, CAP_S = STOP_NEW_S = inf (measure-only), OUTPUT_CAP 16 GiB,
> MEMORY_CAP 12 GiB, WORKER_SESSION (the same identity must own RUN.lock); forces --max-cpu inf
> --max-wall inf; installs a limiter with the owner disk safe-STOP and the op-marker deadline.

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 27, via sys.path edit)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 28, via sys.path edit)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 29, via sys.path edit)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 30, via sys.path edit)
- `import c1_release` -> [tools/c1prime/c1_release.py](c1_release.py.md) (line 110, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 15)
- `json` (lines 17)
- `pathlib` (lines 21)
- `shutil` (lines 18)
- `sys` (lines 19)
- `time` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `[p for p in (str(HERE), str(HERE.parent / 'x4_oracle_profile'), str(HERE.parent / 'x4_circle_history')) if p not in sys.path]` -> `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/c1prime/test_a_release_meter.py](../../tests/c1prime/test_a_release_meter.py.md) (line 34, import)

## Top-level constants

- `CONTRACT`
- `DISK_MIN_FREE`
- `HERE`
- `RES`
- `_LEGACY`

## Classes and functions

- **function `bind`** [L38-48]: `def bind(job_id, task_sha256, out, worker_session) -> None`
- **function `disk_reason`** [L51-59]: `def disk_reason(usage=shutil.disk_usage)`
- **function `make_limiter`** [L62-76]: `def make_limiter(op_marker=None, disk=disk_reason, legacy=None, clock=time.time)`
- **function `_drop`** [L79-82]: `def _drop(args, flag)`
- **function `rewrite_argv`** [L85-91]: `def rewrite_argv(argv) -> list`
- **function `_pop_release`** [L94-101]: `def _pop_release(argv) -> tuple`
- **function `main`** [L104-127]: `def main() -> int`

