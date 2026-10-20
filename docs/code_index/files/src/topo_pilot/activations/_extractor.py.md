# `src/topo_pilot/activations/_extractor.py`

- Source: [src/topo_pilot/activations/_extractor.py](../../../../../../src/topo_pilot/activations/_extractor.py)
- Kind: python
- Lines: 142

## Module docstring

> Gradient-free extraction of hook activations and logits at the analysis position.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, HistoryIndex, ObservationSet, SequenceLayout, StageFailure, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 20, via package root)

### External (third-party)

- `numpy` (lines 7)
- `torch` (lines 8)

### Standard library

- `__future__` (lines 3)
- `typing` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/activations/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/activations/_stage.py](_stage.py.md) (line 18, import)

## Top-level constants

- `_COMPONENT`
- `_TOL`

## Classes and functions

- **function `_fail`** [L26-27]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `valid_hook_names`** [L30-32]: `def valid_hook_names(n_layers: int) -> tuple[str, ...]` - Hook names of a model with ``n_layers`` blocks (learner SPEC).
- **function `resolve_device`** [L35-39]: `def resolve_device(device: str) -> torch.device` - ``"auto"`` is CUDA if available, else CPU; anything else is passed to torch.
- **class `ActivationExtractor`** [L42-142] - Extract ``A [M, K, d]`` and ``logits [M, V]`` at position ``end`` (= 32) of each history.
- **method `ActivationExtractor.__init__`** [L63-68]: `def __init__(self, hooks: Sequence[str], batch_size: int = 256, device: str = 'auto')`
- **method `ActivationExtractor._select_rows`** [L71-74]: `def _select_rows(index: HistoryIndex, panels: Sequence[int] | None) -> np.ndarray` decorators: @staticmethod
- **method `ActivationExtractor._align`** [L77-93]: `def _align(obs: ObservationSet, index: HistoryIndex, rows: np.ndarray) -> np.ndarray` decorators: @staticmethod - Obs row numbers for the selected index rows, verifying end and token digest.
- **method `ActivationExtractor.extract`** [L95-135]: `def extract(self, model: TransformerLM, obs_test: ObservationSet, index: HistoryIndex, panels: Sequence[int] | None = None) -> tuple[np.ndarray, np.ndarray, list[str]]` - Extract activations and logits for the (filtered) histories, in index order.
- **method `ActivationExtractor._verify_plain`** [L138-142]: `def _verify_plain(model: TransformerLM, x: torch.Tensor, logits: torch.Tensor) -> None` decorators: @staticmethod

