# `src/topo_pilot/prediction/stage.py`

- Source: [src/topo_pilot/prediction/stage.py](../../../../../../src/topo_pilot/prediction/stage.py)
- Kind: python
- Lines: 82

## Module docstring

> Thin I/O layer of the prediction module (the only file that touches the store).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, BaselineOutputs, ErrorCode, HistoryIndex, ObservationSet, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from .ngram import NGramBaseline` -> [src/topo_pilot/prediction/ngram.py](ngram.py.md) (line 19, via relative)

### External (third-party)

- `numpy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `logging` (lines 5)
- `typing` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/prediction/__init__.py](__init__.py.md) (line 6, import)

## Top-level constants

- `_COMPONENT`
- `_CONSUMER`
- `_GRID`
- `_LOG`

## Classes and functions

- **class `PredictionStage`** [L27-82] - Reads/writes artifacts for the prediction module (consumer ``"prediction"``).
- **method `PredictionStage.run_baselines`** [L30-59]: `def run_baselines(self, obs_train_id: str, obs_dev_id: str, obs_test_id: str, history_index_id: str, store: ArtifactStore) -> list[str]` - Fit unigram and bigram (additive, alpha chosen on dev) and save ``BaselineOutputs``.
- **method `PredictionStage._histories`** [L62-72]: `def _histories(test: ObservationSet, index: HistoryIndex) -> np.ndarray` decorators: @staticmethod
- **method `PredictionStage.run_metrics`** [L74-76]: `def run_metrics(self, activation_set_id: str, oracle_id: str, store: ArtifactStore) -> str` - Not implemented until wave W4.
- **method `PredictionStage.run_probes`** [L78-82]: `def run_probes(self, activation_set_ids: list[str], oracle_id: str, split_spec: Any, store: ArtifactStore) -> str` - Not implemented here: probe I/O lives in ``experiment`` stage S7 (D-047), because dev

