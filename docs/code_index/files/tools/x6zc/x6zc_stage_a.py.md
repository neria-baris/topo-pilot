# `tools/x6zc/x6zc_stage_a.py`

- Source: [tools/x6zc/x6zc_stage_a.py](../../../../../tools/x6zc/x6zc_stage_a.py)
- Kind: python
- Lines: 241

## Module docstring

> X6ZC stage A and the model chunk children: shared stage begin/finish, the A1 records audit,
> the A2 code audit, stage A (A-audit, A3, K0, the q* cache, K1-K3/F1, A4) and the Stage-B/C
> chunk child (X6ZC-DESIGN-v1 §6; API.md §11.4, §20 C-52). Runs only after FREEZE and AUTH.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 16, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 20, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 21, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 22, via same directory)
- `from x6zc_pipeline import predict_variants` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 25, via same directory)
- `from x6zc_store import _utc, _sha, _cj, xwrite, _append, _lines, log_exposure, write_stage, x6s1_inventory, inventory_equal, env_check, closure_diff, meter_bind_check, ledger_cpu, pause_check, _head, _frozen` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 28, via same directory)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 56, via unique basename) (inside a function)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](../x6_stage1/x6s1_decide.py.md) (line 90, via unique basename) (inside a function)
- `import x6s1_stage_pre` -> [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 131, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 206, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 207, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 13)
- `io` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 14)
- `re` (lines 10)
- `sys` (lines 11)
- `time` (lines 12)

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
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 23, import)

## Top-level constants

- `RUN`
- `_A2_ROW`

## Classes and functions

- **function `_x6`** [L37-37]: `def _x6(rel) -> Path`
- **function `_payload`** [L38-43]: `def _payload(store, stage, rel, sha, purpose) -> bytes`
- **function `_npz`** [L44-46]: `def _npz(data) -> dict`
- **function `_dirs`** [L47-51]: `def _dirs(store, stage) -> list`
- **function `_record`** [L52-54]: `def _record(store, stage) -> tuple`
- **function `_begin`** [L55-66]: `def _begin(store, stage) -> dict`
- **function `_finish`** [L67-81]: `def _finish(store, ctx, stop=None, n=None) -> int`
- **function `_find`** [L82-85]: `def _find(obj, key) -> list`
- **function `_passes`** [L86-88]: `def _passes(obj, name) -> bool`
- **function `a1_check`** [L89-118]: `def a1_check(closure) -> dict`
- **function `a2_check`** [L120-129]: `def a2_check() -> dict`
- **function `stage_a`** [L130-188]: `def stage_a(store=zc.STORE) -> int`
- **function `_cache`** [L189-192]: `def _cache(store) -> zc.QStarCache`
- **function `_spec`** [L193-198]: `def _spec(m) -> tuple`
- **function `_predictor`** [L199-201]: `def _predictor(m) -> se.ModelPredictor`
- **class `_Memo`** [L202-204]
- **method `_Memo.__init__`** [L203-203]: `def __init__(self, rows)`
- **method `_Memo.__call__`** [L204-204]: `def __call__(self, tokens, t)`
- **function `_children`** [L205-218]: `def _children(store, stage, names, out_dir) -> dict`
- **function `chunk`** [L219-241]: `def chunk(stage, model, out, store=zc.STORE) -> int`

