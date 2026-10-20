# `src/topo_pilot/activations/_stage.py`

- Source: [src/topo_pilot/activations/_stage.py](../../../../../../src/topo_pilot/activations/_stage.py)
- Kind: python
- Lines: 65

## Module docstring

> I/O layer of the activations module (the only place that touches the store).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ActivationSet, ArtifactStore, Checkpoint, HistoryIndex, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from ._extractor import ActivationExtractor` -> [src/topo_pilot/activations/_extractor.py](_extractor.py.md) (line 18, via relative)
- `from topo_pilot.learner import load_model` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 47, via package root) (inside a function)

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

- [src/topo_pilot/activations/__init__.py](__init__.py.md) (line 4, import)

## Top-level constants

- `_CONSUMER`
- `_LOG`

## Classes and functions

- **class `ActivationStage`** [L24-65] - Load checkpoint, test observations and history index; save an ``ActivationSet``.
- **method `ActivationStage.__init__`** [L31-33]: `def __init__(self, batch_size: int = 256, device: str = 'auto')`
- **method `ActivationStage.run`** [L35-65]: `def run(self, checkpoint_id: str, obs_test_id: str, history_index_id: str, hooks: Sequence[str], panels: Sequence[int] | None, store: ArtifactStore) -> str` - Extract and store activations; return the ``ActivationSet`` artifact id.

