# `tools/x6zc/x6zc_stage_bc.py`

- Source: [tools/x6zc/x6zc_stage_bc.py](../../../../../tools/x6zc/x6zc_stage_bc.py)
- Kind: python
- Lines: 228

## Module docstring

> X6ZC stages B and C: B1-B10 on the opened D, the Stage-B gate, and the registered Stage C
> with its sensitivity lines and report (X6ZC-DESIGN-v1 §7-§9; API.md §11.4, §11.6, §20 C-52).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 10, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 14, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 15, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 16, via same directory)
- `from x6zc_pipeline import predict_variants, stage_c_statistics, decide_report, validate_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 19, via same directory)
- `from x6zc_stage_a import _payload, _npz, _record, _begin, _finish, _cache, _spec, _predictor, _children` -> [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 23, via same directory)
- `from x6zc_store import _cj, xwrite, _lines, log_exposure, log_evaluation, rulings, ledger_cpu, _head` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 27, via same directory)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 52, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 5)
- `json` (lines 7)
- `pathlib` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 38, import)

## Top-level constants

- none

## Classes and functions

- **function `_terms`** [L33-40]: `def _terms(pa, pb, A, key, qfn) -> dict`
- **function `_boot`** [L41-49]: `def _boot(terms_by_key, gen, P) -> dict`
- **function `_arm`** [L50-50]: `def _arm(m) -> str`
- **function `stage_b`** [L51-142]: `def stage_b(store=zc.STORE) -> int`
- **function `_ev_base`** [L143-151]: `def _ev_base(store) -> dict`
- **function `stage_c`** [L152-228]: `def stage_c(store=zc.STORE) -> int`

