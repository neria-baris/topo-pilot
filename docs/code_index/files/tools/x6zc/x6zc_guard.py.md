# `tools/x6zc/x6zc_guard.py`

- Source: [tools/x6zc/x6zc_guard.py](../../../../../tools/x6zc/x6zc_guard.py)
- Kind: python
- Lines: 330

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
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 147, via unique basename) (inside a function)
- `import topo_pilot` -> [src/topo_pilot/__init__.py](../../src/topo_pilot/__init__.py.md) (line 178, via package root) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 212, via unique basename) (inside a function)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 217, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 218, via unique basename) (inside a function)
- `from x6zc_store import _frozen` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 219, via same directory) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 281, via unique basename) (inside a function)
- `from x6zc_pipeline import TOP, licence_values, validate_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 305, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `ctypes` (lines 88, 100, 105, 106)
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
- **function `_pid_alive`** [L81-96]: `def _pid_alive(pid) -> bool`
- **function `_in_job`** [L97-103]: `def _in_job() -> bool`
- **function `_parents`** [L104-123]: `def _parents() -> dict`
- **function `is_ancestor`** [L124-133]: `def is_ancestor(pid) -> bool`
- **function `meter_live`** [L134-145]: `def meter_live(store) -> list`
- **function `identity_problems`** [L146-165]: `def identity_problems(store, fz, disp, job=None) -> list`
- **function `_try`** [L166-171]: `def _try(why, fn) -> list`
- **function `_git`** [L174-176]: `def _git(*args) -> str`
- **function `freeze_problems`** [L177-196]: `def freeze_problems(store, fz) -> list`
- **function `auth_problems`** [L197-205]: `def auth_problems(store) -> list`
- **function `stage_cpu`** [L208-209]: `def stage_cpu(ctx) -> float`
- **function `_job_cpu`** [L210-215]: `def _job_cpu()`
- **function `_begin`** [L216-244]: `def _begin(store, stage, dispatch=None, job=None) -> dict`
- **function `_finish`** [L245-272]: `def _finish(store, ctx, stop=None, n=None) -> int`
- **function `run_guarded`** [L273-286]: `def run_guarded(store, stage, body, dispatch=None, job=None) -> int` - Every attempt writes its record: a setup error, a stop, or any exception (CRASH).
- **function `stats_marker`** [L287-288]: `def stats_marker(store, ctx) -> str`
- **function `budget`** [L291-299]: `def budget(store, ctx=None) -> dict`
- **function `write_invalid`** [L300-301]: `def write_invalid(store, ctx, why) -> str | None`
- **function `write_global`** [L302-330]: `def write_global(store, ctx, ev, why, extra=None) -> str | None` - The report of a global outcome (G-R0, G-R1, G-R2, G-R2′, G-R3) with null cell statistics:

