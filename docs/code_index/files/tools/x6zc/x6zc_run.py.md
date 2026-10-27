# `tools/x6zc/x6zc_run.py`

- Source: [tools/x6zc/x6zc_run.py](../../../../../tools/x6zc/x6zc_run.py)
- Kind: python
- Lines: 95

## Module docstring

> X6ZC run: the CLI (API.md §11.5). It re-exports the store, pipeline, dry-run, guard and stage
> modules (API.md §1, §20 C-52, C-54), so every API name stays reachable as zr.<name>. Torch-heavy
> X6S1 modules are imported lazily inside the functions that need them.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 14, via same directory)
- `from x6zc_store import _utc, _sha, _norm, _js, _cj, xwrite, _append, _lines, log_exposure, guard, log_evaluation, write_stage, write_ruling, rulings, x6s1_inventory, inventory_equal, env_check, closure_diff, _hit, master_fresh, meter_bind_check, BIND_TEMPLATE, bind_template, ledger_cpu, pause_check, _head, _frozen` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 18, via same directory)
- `from x6zc_pipeline import predict_variants, stage_c_statistics, _f4, licence_values, decide_report, TOP, CELL_KEYS, _OUTS, _outcome_ok, validate_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 25, via same directory)
- `from x6zc_dry import Planted, sd_parse, _jitter, _pool, _ev, dry, se_qstar` -> [tools/x6zc/x6zc_dry.py](x6zc_dry.py.md) (line 30, via same directory)
- `from x6zc_guard import MAILBOX, DISPATCH_KEYS, PREDECESSOR, MARKER, technical, restartable, _attempts, _dirs, _record, refusal, dispatch_record, meter_live, identity_problems, freeze_problems, auth_problems, stage_cpu, _begin, _finish, run_guarded, stats_marker, budget, write_invalid` -> [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 33, via same directory)
- `from x6zc_stage_a import RUN, _x6, _payload, _checked, _npz, _x6json, _latest, _prov, a1_provenance, a1_check, _A2_ROW, a2_check, stage_a, _stage_a, _cache, _spec, _predictor, _Memo, _children, chunk` -> [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 39, via same directory)
- `from x6zc_stage_bc import _terms, _boot, _arm, stage_b, _stage_b, _ev_base, stage_c, _stage_c` -> [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 44, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `argparse` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6zc/test_x6zc_decide.py](../../tests/x6zc/test_x6zc_decide.py.md) (line 18, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 20, import)

## Top-level constants

- none

## Classes and functions

- **function `main`** [L48-93]: `def main(argv=None) -> int`

