# `tests/learner/conftest.py`

- Source: [tests/learner/conftest.py](../../../../../tests/learner/conftest.py)
- Kind: python
- Lines: 36

## Module docstring

> Module-local fixtures: tiny model / data on CPU.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts.testing import tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 8, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 9, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 10, via package root)

### External (third-party)

- `pytest` (lines 5)

### Standard library

- `dataclasses` (lines 3)

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

- **function `tiny_obs`** [L14-15]: `def tiny_obs()` decorators: @pytest.fixture(scope='session')
- **function `tiny_ds`** [L19-20]: `def tiny_ds(tiny_obs)` decorators: @pytest.fixture(scope='session')
- **function `model_cfg`** [L24-25]: `def model_cfg()` decorators: @pytest.fixture()
- **function `train_cfg`** [L29-31]: `def train_cfg()` decorators: @pytest.fixture()
- **function `seeds`** [L35-36]: `def seeds()` decorators: @pytest.fixture()

