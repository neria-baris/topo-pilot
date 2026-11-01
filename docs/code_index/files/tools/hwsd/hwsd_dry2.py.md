# `tools/hwsd/hwsd_dry2.py`

- Source: [tools/hwsd/hwsd_dry2.py](../../../../../tools/hwsd/hwsd_dry2.py)
- Kind: python
- Lines: 398

## Module docstring

> hwsd dry-run cases DRD5, DRD7, DRD8-DRD11 (API.md §12; TEST_PLAN §4). Split from hwsd_dry by
> size; DRD5 and DRD7 are re-exported from hwsd_dry by its lazy __getattr__. Every case is
> synthetic: arrays and stores live under test_hwsd-<job>/dry/<case>/ (decision 6).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 16, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 17, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 25, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 26, via same directory)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 27, via same directory)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 28, via same directory)
- `import hwsd_registry` -> [tools/hwsd/hwsd_registry.py](hwsd_registry.py.md) (line 29, via same directory)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 30, via same directory)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](hwsd_statements.py.md) (line 31, via same directory)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 32, via same directory)
- `from hwsd_dry import _job, _res, fresh_fixture` -> [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 33, via same directory)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 5)
- `builtins` (lines 8)
- `fractions` (lines 12)
- `io` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 13)
- `statistics` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 363, import)

## Top-level constants

- `UTC`
- `_K`

## Classes and functions

- **function `_raises`** [L39-44]: `def _raises(fn, status=None) -> bool`
- **function `_r`** [L54-59]: `def _r(kind, i=0, learn=False, bp=None, **kw) -> dict`
- **function `_ev`** [L62-65]: `def _ev(*seqs, **kw) -> dict`
- **function `_st`** [L68-70]: `def _st(ev, d) -> tuple`
- **function `drd5`** [L73-137]: `def drd5(out, ctx) -> dict`
- **function `drd7`** [L141-167]: `def drd7(out, ctx) -> dict`
- **function `_table`** [L172-177]: `def _table(path, n=8, seed=1) -> Path`
- **function `_obl`** [L180-181]: `def _obl(store, name='REGISTRY_OBLIGATION.json', job='DRD8', attempt=1)`
- **function `_rewrite`** [L184-188]: `def _rewrite(store, fn, name='REGISTRY_OBLIGATION.json')`
- **class `_Hook`** [L191-209]
- **method `_Hook.__init__`** [L192-193]: `def __init__(self, token)`
- **method `_Hook.__enter__`** [L195-206]: `def __enter__(self)`
- **method `_Hook.__exit__`** [L208-209]: `def __exit__(self, *e)`
- **function `drd8`** [L212-283]: `def drd8(out, ctx) -> dict`
- **function `drd9`** [L286-313]: `def drd9(out, ctx) -> dict`
- **function `drd10`** [L317-333]: `def drd10(out, ctx) -> dict`
- **function `drd11`** [L337-398]: `def drd11(out, ctx) -> dict`

