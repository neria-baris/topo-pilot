# `tools/x4_circle_history/op_guard.py`

- Source: [tools/x4_circle_history/op_guard.py](../../../../../tools/x4_circle_history/op_guard.py)
- Kind: python
- Lines: 111

## Module docstring

> Native-operation wall guard, child side (API.md spec v2.4 item 7; builder-tested).

## Imports

### Internal (repo files)

- `from errors import Unresolved` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 17, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 15)
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

- [tests/circle_history/test_builder_v24_runtime.py](../../tests/circle_history/test_builder_v24_runtime.py.md) (line 25, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 37, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 29, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 29, import)
- [tests/k4b/test_b_rerun.py](../../tests/k4b/test_b_rerun.py.md) (line 26, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 20, import)
- [tools/c1prime/c1_meter_bind.py](../c1prime/c1_meter_bind.py.md) (line 29, import)
- [tools/hws/hws_meter_bind.py](../hws/hws_meter_bind.py.md) (line 17, import)
- [tools/hwsb/hwsb_meter_bind.py](../hwsb/hwsb_meter_bind.py.md) (line 18, import)
- [tools/hwsc/hwsc_meter_bind.py](../hwsc/hwsc_meter_bind.py.md) (line 19, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 24, import)
- [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 20, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 106, import)
- [tools/x4_circle_history/meter_bind.py](meter_bind.py.md) (line 49, import)

## Top-level constants

- `LOG`
- `MARKER`

## Classes and functions

- **function `_utc`** [L23-24]: `def _utc() -> str`
- **function `write_marker`** [L27-30]: `def write_marker(out: Path, record: dict) -> None`
- **function `_log`** [L33-35]: `def _log(out: Path, record: dict) -> None`
- **function `timed_factory`** [L38-71]: `def timed_factory(out: Path, wall_s: float, clock=time.monotonic, wall_clock=time.time)`
- **function `overdue`** [L74-90]: `def overdue(marker_path: Path, now_epoch: float)` - Kill reason if the marker shows an active operation past its deadline, else None.
- **function `archive_stale`** [L93-111]: `def archive_stale(out: Path)` - Move a stale ACTIVE marker (killed attempt) to operations/KILLED_<seq>.json; return path.

