# `tools/x6zc/x6zc_stage_a.py`

- Source: [tools/x6zc/x6zc_stage_a.py](../../../../../tools/x6zc/x6zc_stage_a.py)
- Kind: python
- Lines: 278

## Module docstring

> X6ZC stage A and the model chunk children: the A1 records audit, the A2 code audit, stage A
> (A-audit, A3, K0, the q* cache, K1-K3/F1, A4) and the Stage-B/C chunk child (X6ZC-DESIGN-v1 §6;
> API.md §11.4, §20 C-52, C-54). Stage begin/finish live in x6zc_guard. Runs only after FREEZE
> and AUTH.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 18, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 22, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 23, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 24, via same directory)
- `from x6zc_pipeline import predict_variants` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 27, via same directory)
- `from x6zc_store import _utc, _sha, _cj, xwrite, _append, _lines, log_exposure` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 30, via same directory)
- `from x6zc_guard import _dirs, _record, _begin, _finish, run_guarded` -> [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 33, via same directory)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](../x6_stage1/x6s1_decide.py.md) (line 100, via unique basename) (inside a function)
- `import x6s1_stage_pre` -> [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 154, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 232, via unique basename) (inside a function)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 233, via unique basename) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 253, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 21)
- `torch` (lines 254)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 15)
- `io` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `os` (lines 251)
- `pathlib` (lines 16)
- `re` (lines 12)
- `sys` (lines 13)
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

- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 39, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 24, import)

## Top-level constants

- `RUN`
- `_A2_ROW`

## Classes and functions

- **function `_x6`** [L40-40]: `def _x6(rel) -> Path`
- **function `_payload`** [L41-46]: `def _payload(store, stage, rel, sha, purpose) -> bytes`
- **function `_checked`** [L47-51]: `def _checked(r) -> bytes`
- **function `_npz`** [L52-54]: `def _npz(data) -> dict`
- **function `_x6json`** [L55-57]: `def _x6json(rel) -> tuple`
- **function `_latest`** [L58-59]: `def _latest(lines, gate) -> dict`
- **function `_prov`** [L60-88]: `def _prov(m, rep, gl, pools, echo) -> dict`
- **function `a1_provenance`** [L89-98]: `def a1_provenance(rep) -> dict`
- **function `a1_check`** [L99-139]: `def a1_check(store, closure) -> dict`
- **function `a2_check`** [L141-150]: `def a2_check() -> dict`
- **function `stage_a`** [L151-152]: `def stage_a(store=zc.STORE, dispatch=None, job=None) -> int`
- **function `_stage_a`** [L153-210]: `def _stage_a(store, ctx) -> int`
- **function `_cache`** [L211-214]: `def _cache(store) -> zc.QStarCache`
- **function `_spec`** [L215-220]: `def _spec(m) -> tuple`
- **function `_predictor`** [L221-223]: `def _predictor(m) -> se.ModelPredictor`
- **class `_Memo`** [L224-226]
- **method `_Memo.__init__`** [L225-225]: `def __init__(self, rows)`
- **method `_Memo.__call__`** [L226-226]: `def __call__(self, tokens, t)`
- **function `_children`** [L227-249]: `def _children(store, stage, names, out_dir, ctx) -> dict` - <= MAX_CHILDREN chunk children per batch under sr.supervise, which classifies the mailbox
- **function `chunk`** [L250-278]: `def chunk(stage, model, out, store=zc.STORE) -> int`

