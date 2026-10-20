# `tools/d1_seam/d1_seam_checks.py`

- Source: [tools/d1_seam/d1_seam_checks.py](../../../../../tools/d1_seam/d1_seam_checks.py)
- Kind: python
- Lines: 335

## Module docstring

> D-1 seam check part 2 (D1-FROZEN-v1 + addenda; API.md): G4 float cross-check, G5 Decimal
> reference, G6 controls, and run (S0 re-check, mandatory-preflight rule, stop rules, report.json,
> model.npz). Imports part 1; part 1 re-exports these names (addendum 2).

## Imports

### Internal (repo files)

- `import d1_seam` -> [tools/d1_seam/d1_seam.py](d1_seam.py.md) (line 16, via same directory)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 17, via unique basename)
- `from topo_pilot.oracle import BayesFilter, FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 20, via package root)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 5)
- `decimal` (lines 12)
- `fractions` (lines 13)
- `hashlib` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 14)
- `subprocess` (lines 9)
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

- [tools/d1_seam/d1_seam.py](d1_seam.py.md) (line 400, import)

## Top-level constants

- `BASE_COMMIT`
- `BOUND`
- `GATES`
- `NS`
- `PLANNING`
- `TOL`
- `_FILES`
- `_SHA`

## Classes and functions

- **function `_f`** [L53-54]: `def _f(x)`
- **function `_row`** [L57-59]: `def _row(h)`
- **function `gate_G4`** [L62-152]: `def gate_G4(enum)` - Unchanged BayesFilter/FutureOperator against the exact G2 enumeration and the witnesses.
- **function `_dec`** [L155-158]: `def _dec(q)`
- **function `gate_G5`** [L161-181]: `def gate_G5()` - job-0014 Decimal reference (digits 80, Decimal inputs from exact strings), 650 histories.
- **function `gate_G6`** [L184-244]: `def gate_G6()` - Controls N1, N2, N3 (full K = 8 enumerations), L1, L2 and P1 (§5.2 G6).
- **function `_git`** [L247-249]: `def _git(*args)`
- **function `s0_check`** [L252-262]: `def s0_check()`
- **function `_jsonable`** [L265-274]: `def _jsonable(x)`
- **function `run`** [L277-329]: `def run(out_dir, preflight)` - Mandatory preflight, S0, then G0..G6 in order; stop at the first FAIL or INVALID.

