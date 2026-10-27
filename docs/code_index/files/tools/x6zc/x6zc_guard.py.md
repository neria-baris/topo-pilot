# `tools/x6zc/x6zc_guard.py`

- Source: [tools/x6zc/x6zc_guard.py](../../../../../tools/x6zc/x6zc_guard.py)
- Kind: python
- Lines: 363

## Module docstring

> X6ZC guard: the stage harness shared by stages A, B and C (job 0137; API.md §20 C-54). The
> dispatch record and mailbox identities, the live meter, the frozen-implementation binding, the
> environment check with the thread exemption, the in-stage CPU measure, the attempt directories
> with the G2 rerun limit, the crash record, the Stage-C statistics marker and the G-R1 INVALID
> report (X6ZC-DESIGN-v1 §6 A1 item 6, §9.1, §13, §15; rulings R-0134-3..5).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 18, via same directory)
- `from x6zc_store import _utc, _sha, _norm, _cj, xwrite, _lines, write_stage, x6s1_inventory, inventory_equal, env_check, closure_diff, meter_bind_check, ledger_cpu, pause_check, _head, rulings` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 22, via same directory)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 180, via unique basename) (inside a function)
- `import topo_pilot` -> [src/topo_pilot/__init__.py](../../src/topo_pilot/__init__.py.md) (line 211, via package root) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 245, via unique basename) (inside a function)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 250, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 251, via unique basename) (inside a function)
- `from x6zc_store import _frozen` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 252, via same directory) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 314, via unique basename) (inside a function)
- `from x6zc_pipeline import TOP, licence_values, validate_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 338, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `ctypes` (lines 82, 83, 103, 104, 116, 117, 128, 129)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 16)
- `subprocess` (lines 12)
- `sys` (lines 13)
- `time` (lines 14)
- `traceback` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 33, import)
- [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 33, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 27, import)

## Top-level constants

- `C`
- `DISPATCH_KEYS`
- `MAILBOX`
- `MARKER`
- `PREDECESSOR`

## Classes and functions

- **function `technical`** [L32-33]: `def technical(stop) -> bool`
- **function `restartable`** [L34-36]: `def restartable(stop) -> bool`
- **function `_name`** [L39-39]: `def _name(stage, k) -> str`
- **function `_attempts`** [L40-46]: `def _attempts(store, stage) -> list`
- **function `_dirs`** [L47-48]: `def _dirs(store, stage) -> list`
- **function `_record`** [L49-51]: `def _record(store, stage) -> tuple`
- **function `refusal`** [L52-73]: `def refusal(store, stage) -> str | None`
- **function `dispatch_record`** [L76-80]: `def dispatch_record(path=None) -> dict`
- **function `_k32`** [L81-95]: `def _k32()`
- **function `_pid_alive`** [L96-112]: `def _pid_alive(pid) -> bool`
- **function `in_job`** [L113-126]: `def in_job(pid=None) -> bool`
- **function `_parents`** [L127-145]: `def _parents() -> dict`
- **function `chain_below`** [L146-155]: `def chain_below(pid) -> list | None`
- **function `is_ancestor`** [L156-157]: `def is_ancestor(pid) -> bool`
- **function `under_meter_job`** [L158-165]: `def under_meter_job(pid) -> bool` - C-57: the meter (job-0014, sha-pinned) starts its command suspended, assigns it to its job
- **function `meter_live`** [L166-178]: `def meter_live(store) -> list`
- **function `identity_problems`** [L179-198]: `def identity_problems(store, fz, disp, job=None) -> list`
- **function `_try`** [L199-204]: `def _try(why, fn) -> list`
- **function `_git`** [L207-209]: `def _git(*args) -> str`
- **function `freeze_problems`** [L210-229]: `def freeze_problems(store, fz) -> list`
- **function `auth_problems`** [L230-238]: `def auth_problems(store) -> list`
- **function `stage_cpu`** [L241-242]: `def stage_cpu(ctx) -> float`
- **function `_job_cpu`** [L243-248]: `def _job_cpu()`
- **function `_begin`** [L249-277]: `def _begin(store, stage, dispatch=None, job=None) -> dict`
- **function `_finish`** [L278-305]: `def _finish(store, ctx, stop=None, n=None) -> int`
- **function `run_guarded`** [L306-319]: `def run_guarded(store, stage, body, dispatch=None, job=None) -> int` - Every attempt writes its record: a setup error, a stop, or any exception (CRASH).
- **function `stats_marker`** [L320-321]: `def stats_marker(store, ctx) -> str`
- **function `budget`** [L324-332]: `def budget(store, ctx=None) -> dict`
- **function `write_invalid`** [L333-334]: `def write_invalid(store, ctx, why) -> str | None`
- **function `write_global`** [L335-363]: `def write_global(store, ctx, ev, why, extra=None) -> str | None` - The report of a global outcome (G-R0, G-R1, G-R2, G-R2′, G-R3) with null cell statistics:

