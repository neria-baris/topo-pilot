# `tests/dataset/conftest.py`

- Source: [tests/dataset/conftest.py](../../../../../tests/dataset/conftest.py)
- Kind: python
- Lines: 50

## Module docstring

> Module-local fixtures: a tiny stored process (world, T, E) built by hand.

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 6, via package root)
- `from topo_pilot.dataset import DatasetConfig` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 7, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)

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

- **function `make_emission`** [L10-15]: `def make_emission(E: np.ndarray, pi: np.ndarray, perm, sigma: float = 0.5) -> C.EmissionSpec` - EmissionSpec with hand-filled diagnostics; ``perm[j]`` = public id of canonical symbol j.
- **function `tiny_cfg`** [L19-20]: `def tiny_cfg() -> DatasetConfig` decorators: @pytest.fixture
- **function `process`** [L24-34]: `def process()` decorators: @pytest.fixture - ``(store, transition_id, emission_id, E_canon)`` with an identity symbol permutation.
- **function `add_emission`** [L38-50]: `def add_emission(process)` decorators: @pytest.fixture - Factory: store an emission whose canonical form ``E[:, perm]`` equals ``E_canon``.

