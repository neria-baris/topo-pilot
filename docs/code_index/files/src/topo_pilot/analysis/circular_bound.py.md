# `src/topo_pilot/analysis/circular_bound.py`

- Source: [src/topo_pilot/analysis/circular_bound.py](../../../../../../src/topo_pilot/analysis/circular_bound.py)
- Kind: python
- Lines: 47

## Module docstring

> Symbol-only optimistic bound for circular agreement (circ-audit-v1, privileged_eval).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)

### External (third-party)

- `numpy` (lines 9, 10)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 5, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `symbol_only_bound`** [L17-47]: `def symbol_only_bound(theta: ArrayLike, symbols: ArrayLike) -> float` - Largest agreement any function of ``symbols`` can reach with ``theta`` on these rows.

