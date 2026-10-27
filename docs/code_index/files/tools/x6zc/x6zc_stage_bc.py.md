# `tools/x6zc/x6zc_stage_bc.py`

- Source: [tools/x6zc/x6zc_stage_bc.py](../../../../../tools/x6zc/x6zc_stage_bc.py)
- Kind: python
- Lines: 234

## Module docstring

> X6ZC stages B and C: B1-B10 on the opened D, the Stage-B gate, and the registered Stage C
> with its sensitivity lines and report (X6ZC-DESIGN-v1 §7-§9; API.md §11.4, §11.6, §20 C-52,
> C-54).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 11, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 15, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 16, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 17, via same directory)
- `from x6zc_pipeline import predict_variants, stage_c_statistics, decide_report, validate_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 20, via same directory)
- `from x6zc_stage_a import _payload, _npz, _cache, _spec, _predictor, _children` -> [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 24, via same directory)
- `from x6zc_guard import _record, _finish, run_guarded, stage_cpu, stats_marker, budget` -> [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 27, via same directory)
- `from x6zc_store import _cj, xwrite, _lines, log_exposure, log_evaluation, rulings, _head` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 31, via same directory)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 58, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 6)
- `json` (lines 8)
- `pathlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 44, import)

## Top-level constants

- none

## Classes and functions

- **function `_terms`** [L37-44]: `def _terms(pa, pb, A, key, qfn) -> dict`
- **function `_boot`** [L45-53]: `def _boot(terms_by_key, gen, P) -> dict`
- **function `_arm`** [L54-54]: `def _arm(m) -> str`
- **function `stage_b`** [L55-56]: `def stage_b(store=zc.STORE, dispatch=None, job=None) -> int`
- **function `_stage_b`** [L57-149]: `def _stage_b(store, ctx) -> int`
- **function `_ev_base`** [L150-158]: `def _ev_base(store) -> dict`
- **function `stage_c`** [L159-160]: `def stage_c(store=zc.STORE, dispatch=None, job=None) -> int`
- **function `_stage_c`** [L161-234]: `def _stage_c(store, ctx) -> int`

