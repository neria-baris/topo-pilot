# `tools/x4_oracle_profile/meter.py`

- Source: [tools/x4_oracle_profile/meter.py](../../../../../tools/x4_oracle_profile/meter.py)
- Kind: python
- Lines: 355

## Module docstring

> CPU-metering supervisor for job 0014 (standard library only; Windows Job Objects).

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](controls.py.md) (line 28, via same directory)
- `from winjob import CREATE_SUSPENDED, JOB_ACCOUNTING, JOB_EXTENDED, BasicAccounting, ExtendedLimit, MeterError, _check, _query, job_cpu, job_peak_working_set, k32, make_job, ntdll, own_cpu_s, process_cpu_s, terminate_and_drain, wt` -> [tools/x4_oracle_profile/winjob.py](winjob.py.md) (line 29, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 16)
- `argparse` (lines 18)
- `json` (lines 19)
- `os` (lines 20)
- `pathlib` (lines 24)
- `subprocess` (lines 21)
- `sys` (lines 22)
- `time` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(Path(__file__).resolve().parent)` -> `tools/x4_oracle_profile`

## Imported by

- [tests/c1prime/test_a_release_meter.py](../../tests/c1prime/test_a_release_meter.py.md) (line 37, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 28, import)
- [tools/c1prime/c1_meter_bind.py](../c1prime/c1_meter_bind.py.md) (line 28, import)
- [tools/c2_nd/store_template/nd_meter_bind.py](../c2_nd/store_template/nd_meter_bind.py.md) (line 66, import)
- [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 19, import)
- [tools/x4_circle_history/meter_bind.py](../x4_circle_history/meter_bind.py.md) (line 48, import)

## Top-level constants

- `ACTIVE`
- `EMERGENCY`
- `FAULTS`
- `LEDGER`
- `LOCK`
- `LOG_DIR`
- `OUT`
- `OUTPUT_CAP`
- `TAIL_ALLOWANCE_S`
- `THREAD_VARS`
- `WORKER_SESSION`

## Classes and functions

- **function `output_bytes`** [L69-70]: `def output_bytes() -> int`
- **function `atomic_json`** [L73-78]: `def atomic_json(path: Path, obj) -> None`
- **function `limit_reason`** [L81-94]: `def limit_reason(ledger, child, args, active_wall, polls, mailboxes) -> tuple` - (kill reason or None, control state). HOLD never kills; STOP/INVALID always do.
- **function `_launch`** [L97-111]: `def _launch(cmd, out, err, job, state, fault)`
- **function `supervise`** [L114-170]: `def supervise(cmd, args, ledger, state, mailboxes) -> dict` - Run cmd in the job; return only after the job has NO active process.
- **function `error_entry`** [L173-190]: `def error_entry(base, exc, state) -> dict`
- **function `finalise`** [L193-227]: `def finalise(ledger: dict, index: int, entry: dict, fault: str | None) -> None`
- **function `load_ledger`** [L230-234]: `def load_ledger() -> dict`
- **function `lock_refusal`** [L237-252]: `def lock_refusal(args) -> str | None` - Reason to refuse (charged as a REFUSED entry), or None.
- **function `parse`** [L255-278]: `def parse() -> argparse.Namespace`
- **function `main`** [L281-351]: `def main() -> int`

