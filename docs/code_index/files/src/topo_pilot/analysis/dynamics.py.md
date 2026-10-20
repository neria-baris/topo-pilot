# `src/topo_pilot/analysis/dynamics.py`

- Source: [src/topo_pilot/analysis/dynamics.py](../../../../../../src/topo_pilot/analysis/dynamics.py)
- Kind: python
- Lines: 77

## Module docstring

> Dynamics (checkpoint-order null) and the minimal LayerSweep.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)
- `from .pointset import PointSet, ph_summary` -> [src/topo_pilot/analysis/pointset.py](pointset.py.md) (line 11, via relative)
- `from .spaces import SpaceBuilder` -> [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 12, via relative)

### External (third-party)

- `numpy` (lines 7)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 7, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_first_third_share`** [L17-22]: `def _first_third_share(values: np.ndarray) -> float`
- **class `Dynamics`** [L25-57] - Descriptive checkpoint-order permutation null (not a replicate-level test).
- **method `Dynamics.checkpoint_order_null`** [L47-57]: `def checkpoint_order_null(self, values, n_perm: int, rng) -> dict` - Return ``{"statistic", "p_value"}``.
- **class `LayerSweep`** [L60-77] - Secondary analysis: S_H1 for every hook and for the concatenation of all hooks.
- **method `LayerSweep.run`** [L69-77]: `def run(self, activation_set_id: str, panel: int, store: ArtifactStore) -> list[dict]` - Sweep all hooks of one ActivationSet on one panel.

