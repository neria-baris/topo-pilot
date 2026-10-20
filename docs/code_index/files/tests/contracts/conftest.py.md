# `tests/contracts/conftest.py`

- Source: [tests/contracts/conftest.py](../../../../../tests/contracts/conftest.py)
- Kind: python
- Lines: 113

## Module docstring

> Hand-built small valid instances of every artifact class (independent of the
> implementation).

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 7, via package root)

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

- `BUILDERS`
- `CONSUMER`

## Classes and functions

- **function `_emission`** [L14-22]: `def _emission()`
- **function `make_history_index`** [L25-35]: `def make_history_index(sequence_id=(0, 1, 2, 3), end=(32, 32, 32, 32), panel=(1, 1, 2, 2), panel_size=2, n_panels=2)`
- **function `_dist`** [L38-40]: `def _dist(m=3)`
- **function `_oracle`** [L43-51]: `def _oracle()`
- **function `builders`** [L101-102]: `def builders()` decorators: @pytest.fixture
- **function `fs_store`** [L106-108]: `def fs_store(tmp_path)` decorators: @pytest.fixture
- **function `make_hist`** [L112-113]: `def make_hist()` decorators: @pytest.fixture

