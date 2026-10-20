# `src/topo_pilot/dataset/sampler.py`

- Source: [src/topo_pilot/dataset/sampler.py](../../../../../../src/topo_pilot/dataset/sampler.py)
- Kind: python
- Lines: 80

## Module docstring

> Vectorised HMM sampler: ``z_1 ~ pi``; emit ``w_t ~ E[z_t]``; then ``z_{t+1} ~ T[z_t]``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 7, via package root)

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

- [src/topo_pilot/dataset/__init__.py](__init__.py.md) (line 6, import)
- [src/topo_pilot/dataset/stage.py](stage.py.md) (line 33, import)
- [tests/c1prime/test_b_registry.py](../../../tests/c1prime/test_b_registry.py.md) (line 25, import)
- [tools/x4_circle_history/process_law.py](../../../tools/x4_circle_history/process_law.py.md) (line 131, dynamic)

## Top-level constants

- `_CHUNK`

## Classes and functions

- **function `_cumulative_rows`** [L12-21]: `def _cumulative_rows(P: np.ndarray) -> np.ndarray` - Row-wise CDF with every entry from the last positive probability on set to exactly 1.
- **function `_draw`** [L24-30]: `def _draw(cum: np.ndarray, rows: np.ndarray, u: np.ndarray) -> np.ndarray` - Inverse CDF: for each ``i`` the smallest ``j`` with ``u[i] < cum[rows[i], j]``.
- **class `HMMSampler`** [L33-80] - Samples independent trajectories of ``n_obs = layout.n_obs`` steps.
- **method `HMMSampler.__init__`** [L57-67]: `def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray, layout: SequenceLayout)`
- **method `HMMSampler.sample`** [L69-80]: `def sample(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]` - Draw ``n`` trajectories; returns ``(tokens [n, 33], states [n, 33])``.

