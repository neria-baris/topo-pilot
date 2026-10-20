# `tests/dataset/test_panels.py`

- Source: [tests/dataset/test_panels.py](../../../../../tests/dataset/test_panels.py)
- Kind: python
- Lines: 58

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 13, via package root)
- `from topo_pilot.dataset import DatasetConfig, HMMSampler, PanelBuilder` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 14, via package root)

### External (third-party)

- `numpy` (lines 1)
- `pytest` (lines 2)

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `_test_obs`** [L19-23]: `def _test_obs(r: int) -> ObservationSet`
- **function `_panel_rng`** [L26-27]: `def _panel_rng()`
- **test `test_D05_panels_disjoint_distinct_and_reproducible`** [L30-49]: `def test_D05_panels_disjoint_distinct_and_reproducible()`
- **test `test_panel_config_sizes_and_too_few_trajectories`** [L52-58]: `def test_panel_config_sizes_and_too_few_trajectories()`

