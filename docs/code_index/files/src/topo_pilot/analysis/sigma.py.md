# `src/topo_pilot/analysis/sigma.py`

- Source: [src/topo_pilot/analysis/sigma.py](../../../../../../src/topo_pilot/analysis/sigma.py)
- Kind: python
- Lines: 95

## Module docstring

> SigmaCalibrator: the pre-registered sigma selection rule (RESEARCH_SUMMARY section 4).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 6)
- `math` (lines 5)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 32, import)

## Top-level constants

- none

## Classes and functions

- **class `SigmaRow`** [L13-21] decorators: @dataclass(frozen=True) - Calibration measurements for one (sigma, world) pair (V symbols).
- **class `SigmaDecision`** [L25-31] decorators: @dataclass(frozen=True) - Outcome: ``status`` in ``ok | weak_context | stop_H3``; ``sigma`` is None on stop.
- **class `SigmaCalibrator`** [L34-95] - Select sigma by the first-passing rule with a weak-context fallback.
- **method `SigmaCalibrator.__init__`** [L51-56]: `def __init__(self, min_entropy: float = math.log(2.0), min_gc: float = 0.1, min_p_factor: float = 0.5, fallback_gc: float = 0.03)`
- **method `SigmaCalibrator._row_failures`** [L58-66]: `def _row_failures(self, r: SigmaRow) -> list[str]`
- **method `SigmaCalibrator.select`** [L68-95]: `def select(self, rows: Sequence[SigmaRow]) -> SigmaDecision` - Apply the rule to rows ordered by candidate priority (see class docstring).

