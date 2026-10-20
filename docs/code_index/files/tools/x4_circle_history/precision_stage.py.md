# `tools/x4_circle_history/precision_stage.py`

- Source: [tools/x4_circle_history/precision_stage.py](../../../../../tools/x4_circle_history/precision_stage.py)
- Kind: python
- Lines: 149

## Module docstring

> Precision and export stage bodies for runner.py (API.md spec v2.4 items 8-10; builder-tested).

## Imports

### Internal (repo files)

- `import stage_records` -> [tools/x4_circle_history/stage_records.py](stage_records.py.md) (line 18, via same directory)
- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 19, via same directory)
- `from scores import history_digests` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 28, via same directory) (inside a function)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 58, via same directory) (inside a function)
- `import precision` -> [tools/x4_circle_history/precision.py](precision.py.md) (line 72, via same directory) (inside a function)
- `from scores import CONTROL_NAMES, angular_instability, control_scores` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 73, via same directory) (inside a function)
- `import precision` -> [tools/x4_circle_history/precision.py](precision.py.md) (line 92, via same directory) (inside a function)
- `from scores import r4_norms, scores, unit_vectors` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 93, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 14)
- `json` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x4_circle_history/runner.py](runner.py.md) (line 283, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 292, import)

## Top-level constants

- none

## Classes and functions

- **function `_load_npz`** [L22-24]: `def _load_npz(path: Path) -> dict`
- **function `_evaluation_rows`** [L27-48]: `def _evaluation_rows(ctx) -> dict`
- **function `_round_up`** [L51-53]: `def _round_up(x: Fraction) -> float`
- **function `_instability_bounds`** [L56-68]: `def _instability_bounds(oracle: dict, model, S: int) -> dict` - bound_K = exact max validation moment gap + moment envelope, rounded up (diagnostic).
- **function `_controls`** [L71-88]: `def _controls(ctx, rows, oracle) -> dict`
- **function `run`** [L91-122]: `def run(ctx) -> dict`
- **function `export_summary`** [L125-149]: `def export_summary(out: Path) -> dict`

