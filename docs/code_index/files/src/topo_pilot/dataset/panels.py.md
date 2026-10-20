# `src/topo_pilot/dataset/panels.py`

- Source: [src/topo_pilot/dataset/panels.py](../../../../../../src/topo_pilot/dataset/panels.py)
- Kind: python
- Lines: 58

## Module docstring

> Fixed analysis panels (RESEARCH_SUMMARY 7.1).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, HistoryIndex, ObservationSet, StageFailure, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 7, via package root)
- `from .config import DatasetConfig` -> [src/topo_pilot/dataset/config.py](config.py.md) (line 16, via relative)

### External (third-party)

- `numpy` (lines 5)

### Standard library

- `__future__` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/dataset/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/dataset/stage.py](stage.py.md) (line 31, import)

## Top-level constants

- none

## Classes and functions

- **class `PanelBuilder`** [L19-58] - Draws ``n_panels`` disjoint panels of ``panel_size`` distinct test trajectories.
- **method `PanelBuilder.build`** [L38-58]: `def build(self, test: ObservationSet, cfg: DatasetConfig, rng: np.random.Generator, *, dataset_id: str = '') -> HistoryIndex`

