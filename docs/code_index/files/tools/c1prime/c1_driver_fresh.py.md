# `tools/c1prime/c1_driver_fresh.py`

- Source: [tools/c1prime/c1_driver_fresh.py](../../../../../tools/c1prime/c1_driver_fresh.py)
- Kind: python
- Lines: 179

## Module docstring

> C1' stage driver, part 4: the fresh stage S7 (protocol §16 rows 20-22, §12.3, §13, §15.3.11).
> T-PRE runs every pre-scoring check on the fresh rows before any fresh primary/control A, Y or Z
> exists; NUM certifies; ENDPOINT decides. Implemented in job 0026; never run on data in job 0026.

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 9, via same directory)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 10, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 11, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](c1_data.py.md) (line 12, via same directory)
- `import c1_driver` -> [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 13, via same directory)
- `import c1_driver_cal` -> [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 14, via same directory)
- `import c1_driver_late` -> [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 15, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 16, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](c1_fit.py.md) (line 17, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 18, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 20, via unique basename)
- `from c1_records import begin_stage` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 21, via same directory)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 5)
- `json` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 261, import)

## Top-level constants

- `MODELS`

## Classes and functions

- **class `_SubStop(Exception)`** [L26-29]
- **method `_SubStop.__init__`** [L27-29]: `def __init__(self, name, status)`
- **function `flat_oracle`** [L32-37]: `def flat_oracle(r) -> dict`
- **function `_check`** [L40-43]: `def _check(sub, name, res) -> None`
- **function `tpre`** [L46-109]: `def tpre(ctx, H) -> dict`
- **function `_summ`** [L112-113]: `def _summ(sub) -> dict`
- **function `_m1`** [L116-123]: `def _m1(S) -> dict`
- **function `num`** [L126-156]: `def num(ctx, H) -> dict`
- **function `endpoint`** [L159-169]: `def endpoint(ctx, H) -> dict`
- **function `run_fresh`** [L172-179]: `def run_fresh(ctx) -> None`

