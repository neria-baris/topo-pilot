# `tools/x6zc/x6zc_pipeline.py`

- Source: [tools/x6zc/x6zc_pipeline.py](../../../../../tools/x6zc/x6zc_pipeline.py)
- Kind: python
- Lines: 124

## Module docstring

> X6ZC pipeline: the pure Stage-C functions shared by Stage C, the sensitivity lines and the dry
> run, the licence values, decide_report and the report schema (API.md §11.4, §11.6, §20 C-52).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 10, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 14, via unique basename)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 5)
- `math` (lines 7)
- `re` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6zc/x6zc_dry.py](x6zc_dry.py.md) (line 22, import)
- [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 266, import)
- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 25, import)
- [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 27, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 20, import)

## Top-level constants

- `CELL_KEYS`
- `TOP`
- `_OUTS`

## Classes and functions

- **function `predict_variants`** [L20-23]: `def predict_variants(pred, arrays_by_family) -> dict`
- **function `stage_c_statistics`** [L24-63]: `def stage_c_statistics(outputs, arrays_by_family, qstar_fn, gen, drop_pairs=None, drop_clusters=None) -> dict`
- **function `_f4`** [L64-64]: `def _f4(x) -> str`
- **function `licence_values`** [L65-88]: `def licence_values(cell, stats, dc, ev) -> dict`
- **function `decide_report`** [L89-98]: `def decide_report(stats, ev_base, census=None) -> dict`
- **function `_outcome_ok`** [L107-109]: `def _outcome_ok(o) -> bool`
- **function `validate_report`** [L110-124]: `def validate_report(report) -> list`

