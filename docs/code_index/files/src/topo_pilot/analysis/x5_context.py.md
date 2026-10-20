# `src/topo_pilot/analysis/x5_context.py`

- Source: [src/topo_pilot/analysis/x5_context.py](../../../../../../src/topo_pilot/analysis/x5_context.py)
- Kind: python
- Lines: 52

## Module docstring

> X5 G1 context gate and verdict precedence (x5g1-feas-v2 §5, §8).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `math` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 59, import)

## Top-level constants

- `GC_THRESHOLD`

## Classes and functions

- **function `percentile_interval`** [L15-18]: `def percentile_interval(values: NDArray) -> tuple[float, float]` - ``np.quantile(values, [0.025, 0.975], method="linear")``.
- **function `context_status`** [L21-30]: `def context_status(lo: float, hi: float, valid: bool = True) -> str` - PASS iff ``lo >= 0.03``; FAIL iff ``hi < 0.03`` (a valid G_C of 0 included);
- **function `x5_overall_verdict`** [L33-52]: `def x5_overall_verdict(arms: dict[str, dict], global_failed: list[str], global_inconclusive: list[str]) -> tuple[str, str]` - Precedence FAILED > INCONCLUSIVE > WEAK_CONTEXT > FEASIBLE (a weak arm never conceals an

