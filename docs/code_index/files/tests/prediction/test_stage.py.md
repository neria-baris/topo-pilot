# `tests/prediction/test_stage.py`

- Source: [tests/prediction/test_stage.py](../../../../../tests/prediction/test_stage.py)
- Kind: python
- Lines: 74

## Module docstring

> R05 (stage part): run_baselines wiring, split use, saved artifacts.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import BaselineOutputs, HistoryIndex, ObservationSet, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 13, via package root)
- `from topo_pilot.prediction import NGramBaseline, PredictionStage` -> [src/topo_pilot/prediction/__init__.py](../../src/topo_pilot/prediction/__init__.py.md) (line 14, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

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

- **function `retarget`** [L19-21]: `def retarget(obs, split)`
- **function `build`** [L24-39]: `def build(store)`
- **test `test_R05_run_baselines_uses_train_for_fit_dev_for_select`** [L42-67]: `def test_R05_run_baselines_uses_train_for_fit_dev_for_select(monkeypatch)`
- **test `test_run_metrics_and_probes_deferred`** [L70-74]: `def test_run_metrics_and_probes_deferred()`

