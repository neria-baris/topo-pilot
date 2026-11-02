# `tools/hwsd/hwsd_summary.py`

- Source: [tools/hwsd/hwsd_summary.py](../../../../../tools/hwsd/hwsd_summary.py)
- Kind: python
- Lines: 312

## Module docstring

> HWSD SUMMARY: bootstraps, bounds, F, the 36-row table, outcome, report (API.md section 8).
> Reused functions are called through their module attributes at call time.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 6, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 11, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 12, via same directory)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 13, via same directory)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 14, via same directory)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](hwsd_statements.py.md) (line 15, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 16, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 17, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 18, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 19, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 8)
- `hashlib` (lines 7)
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

- [tests/hwsd/test_a_bounds.py](../../tests/hwsd/test_a_bounds.py.md) (line 27, import)
- [tests/hwsd/test_a_evaluate.py](../../tests/hwsd/test_a_evaluate.py.md) (line 22, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 327, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 41, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 32, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 207, import)

## Top-level constants

- `SHARED`

## Classes and functions

- **function `_tm`** [L29-30]: `def _tm(x) -> float`
- **function `_checked`** [L33-38]: `def _checked(out, rel, stage)`
- **function `load_scores`** [L41-54]: `def load_scores(out, masters=dc.MASTERS) -> dict`
- **function `_order`** [L57-59]: `def _order(scores)`
- **function `bootstrap_inputs_d`** [L62-76]: `def bootstrap_inputs_d(scores, shared) -> dict`
- **function `main_bootstrap`** [L79-81]: `def main_bootstrap(inputs, seed=None) -> dict`
- **function `strong_bootstrap`** [L84-91]: `def strong_bootstrap(scores, seed=None) -> dict`
- **function `strong_bounds`** [L94-105]: `def strong_bounds(draws_minus, draws_plus) -> dict`
- **function `f_sides`** [L108-113]: `def f_sides(record, Z, n=dc.N) -> tuple`
- **function `control_summary_d`** [L116-117]: `def control_summary_d(draws, controls, bounds) -> dict`
- **function `checkpoint_row`** [L120-153]: `def checkpoint_row(j, step, item, draws, sdraws, Z, controls_summary) -> dict`
- **function `outcome_d`** [L156-168]: `def outcome_d(state) -> dict`
- **class `_Default(dict)`** [L171-173]
- **method `_Default.__missing__`** [L172-173]: `def __missing__(self, key)`
- **function `_step`** [L176-177]: `def _step(table, j, k)`
- **function `fill_templates`** [L180-230]: `def fill_templates(evaluation, table) -> dict`
- **function `_fracs`** [L233-234]: `def _fracs(e) -> dict`
- **function `_shared_inputs`** [L237-242]: `def _shared_inputs(out, shared)`
- **function `_controls_for`** [L245-269]: `def _controls_for(out, scores, shared_bounds)`
- **function `report`** [L272-312]: `def report(out, Z, shared, b4, stage_c=None) -> dict`

