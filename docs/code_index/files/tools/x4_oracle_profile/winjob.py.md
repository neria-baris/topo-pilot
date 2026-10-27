# `tools/x4_oracle_profile/winjob.py`

- Source: [tools/x4_oracle_profile/winjob.py](../../../../../tools/x4_oracle_profile/winjob.py)
- Kind: python
- Lines: 175

## Module docstring

> Win32 Job Object / process-time helpers for meter.py (ctypes, declared signatures).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `ctypes` (lines 5, 6)
- `time` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_release_meter.py](../../tests/c1prime/test_a_release_meter.py.md) (line 38, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 39, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 30, import)
- [tools/c1prime/c1_meter_bind.py](../c1prime/c1_meter_bind.py.md) (line 30, import)
- [tools/c2_nd/store_template/nd_meter_bind.py](../c2_nd/store_template/nd_meter_bind.py.md) (line 67, import)
- [tools/d2a/d2a_decide.py](../d2a/d2a_decide.py.md) (line 344, import)
- [tools/d2a/process_tree.py](../d2a/process_tree.py.md) (line 13, import)
- [tools/hws/hws_dry.py](../hws/hws_dry.py.md) (line 173, import)
- [tools/hws/hws_meter_bind.py](../hws/hws_meter_bind.py.md) (line 18, import)
- [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 21, import)
- [tools/x4_oracle_profile/meter.py](meter.py.md) (line 29, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 390, import)

## Top-level constants

- `MEMORY_CAP`
- `_FT`

## Classes and functions

- **class `BasicAccounting(ctypes.Structure)`** [L12-22]
- **class `BasicLimit(ctypes.Structure)`** [L25-36]
- **class `ExtendedLimit(ctypes.Structure)`** [L39-47]
- **class `PidList(ctypes.Structure)`** [L50-51]
- **class `MemoryCounters(ctypes.Structure)`** [L54-67]
- **class `MeterError(RuntimeError)`** [L99-100]
- **function `_check`** [L103-105]: `def _check(ok, what: str) -> None`
- **function `process_cpu_s`** [L108-111]: `def process_cpu_s(handle) -> float`
- **function `own_cpu_s`** [L114-115]: `def own_cpu_s() -> float`
- **function `_query`** [L118-124]: `def _query(job, info_class: int, info) -> None`
- **function `job_cpu`** [L127-130]: `def job_cpu(job) -> tuple[float, float, int]`
- **function `job_peak_working_set`** [L133-150]: `def job_peak_working_set(job, seen: dict) -> None` - Peak working set of every live job process (polled; exited processes keep the last).
- **function `make_job`** [L153-164]: `def make_job()`
- **function `terminate_and_drain`** [L167-175]: `def terminate_and_drain(job, timeout_s: float = 30.0) -> bool` - Terminate every job process and wait (bounded) until none is active.

