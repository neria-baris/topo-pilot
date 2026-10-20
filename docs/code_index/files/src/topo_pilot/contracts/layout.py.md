# `src/topo_pilot/contracts/layout.py`

- Source: [src/topo_pilot/contracts/layout.py](../../../../../../src/topo_pilot/contracts/layout.py)
- Kind: python
- Lines: 72

## Module docstring

> The single source of sequence alignment (DATA_SCHEMAS §3).

## Imports

### Internal (repo files)

- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 9, via relative)

### External (third-party)

- `numpy` (lines 7)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 17, import)

## Top-level constants

- none

## Classes and functions

- **class `SequenceLayout`** [L13-72] decorators: @dataclass(frozen=True) - Alignment between observed symbols, model positions, targets, and oracle quantities.
- **method `SequenceLayout.bos_id`** [L39-41]: `def bos_id(self, V: int) -> int` - Id of the BOS token: ``V`` (the input vocabulary is ``V + 1``).
- **method `SequenceLayout._check`** [L43-48]: `def _check(self, tokens: np.ndarray) -> np.ndarray`
- **method `SequenceLayout.model_inputs`** [L50-57]: `def model_inputs(self, tokens: np.ndarray, V: int) -> np.ndarray` - ``[BOS, w_1..w_32]`` per row: ``[R, 33] -> [R, 33]``, dtype int64.
- **method `SequenceLayout.targets`** [L59-61]: `def targets(self, tokens: np.ndarray) -> np.ndarray` - ``[w_1..w_33]`` per row: ``[R, 33] -> [R, 33]``, dtype int64 (a copy).
- **method `SequenceLayout.history`** [L63-72]: `def history(self, tokens_row: np.ndarray, p: int) -> np.ndarray` - The history seen at position ``p``: ``w_1..w_p`` (empty for ``p = 0``), int64.

