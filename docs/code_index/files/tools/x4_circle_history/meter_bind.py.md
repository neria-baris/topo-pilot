# `tools/x4_circle_history/meter_bind.py`

- Source: [tools/x4_circle_history/meter_bind.py](../../../../../tools/x4_circle_history/meter_bind.py)
- Kind: python
- Lines: 265

## Module docstring

> Job binding for the reused job-0014 meter (standard library only; base interpreter, -I).

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 47, via sys.path edit)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 48, via sys.path edit)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](op_guard.py.md) (line 49, via same directory)
- `import release` -> [tools/x4_circle_history/release.py](release.py.md) (line 50, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 34)
- `json` (lines 36)
- `pathlib` (lines 40)
- `shutil` (lines 37)
- `sys` (lines 38)
- `time` (lines 39)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 44: `str(HERE)` -> `tools/x4_circle_history`
- line 45: `str(ORACLE_TOOLS)` -> `tools/x4_oracle_profile`

## Imported by

- [tests/circle_history/test_builder_guards.py](../../tests/circle_history/test_builder_guards.py.md) (line 24, import)
- [tests/circle_history/test_builder_runtime.py](../../tests/circle_history/test_builder_runtime.py.md) (line 21, import)
- [tests/circle_history/test_builder_v24_runtime.py](../../tests/circle_history/test_builder_v24_runtime.py.md) (line 24, import)
- [tests/circle_history/test_builder_v25.py](../../tests/circle_history/test_builder_v25.py.md) (line 23, import)

## Top-level constants

- `CONTRACT`
- `DISK_MIN_FREE`
- `HERE`
- `MARGIN_S`
- `MEASURE_ONLY`
- `ORACLE_TOOLS`
- `_LEGACY_LIMIT`

## Classes and functions

- **function `bind`** [L59-75]: `def bind(job_id: str, task_sha256: str, out: Path, finalization: bool = False) -> None` - Point the unchanged modules at this job and store (module-level names only).
- **function `measure_only`** [L78-79]: `def measure_only() -> bool`
- **function `stage_caps`** [L82-91]: `def stage_caps(rel: dict | None) -> dict`
- **function `stage_spent`** [L94-100]: `def stage_spent(ledger_path: Path, stage: str) -> float`
- **function `disk_reason`** [L103-112]: `def disk_reason(usage=shutil.disk_usage)` - Owner disk safe-STOP: a reason when C: or X: free space is below its threshold.
- **function `make_stage_limiter`** [L115-143]: `def make_stage_limiter(stage_cap: float, spent: float, own_cpu=None, legacy=None, op_marker=None, op_clock=time.time, disk=disk_reason)` - Limiter for meter.limit_reason: stage spent + child + supervisor + tail < stage cap, the
- **function `sync_ledger_caps`** [L146-197]: `def sync_ledger_caps(ledger_path: Path) -> bool` - Apply the recorded CONTRACT allocation and CPU policy to the ledger metadata (entries
- **function `_pop`** [L200-206]: `def _pop(args: list, flag: str, has_value: bool = True)`
- **function `rewrite_argv`** [L209-256]: `def rewrite_argv(argv: list[str]) -> list[str]` - Extract --stage/--release/--finalization, bind, install limiter, return meter argv.
- **function `main`** [L259-261]: `def main() -> int`

