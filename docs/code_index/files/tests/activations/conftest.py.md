# `tests/activations/conftest.py`

- Source: [tests/activations/conftest.py](../../../../../tests/activations/conftest.py)
- Kind: python
- Lines: 102

## Module docstring

> Module-local fixtures: tiny model (real TransformerLM if importable, else a stand-in).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import HistoryIndex, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 12, via package root)
- `from topo_pilot.contracts.testing import tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 13, via package root)
- `from topo_pilot.learner import ModelConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 54, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)
- `torch` (lines 9, 10)

### Standard library

- `__future__` (lines 3)
- `types` (lines 5)

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

- `DATASET_ID`
- `D_MODEL`
- `N_LAYERS`
- `N_PANELS`
- `PANEL_SIZE`
- `V`

## Classes and functions

- **class `StandInLM(nn.Module)`** [L23-49] - Stand-in for ``learner.TransformerLM`` implementing only its public interface.
- **method `StandInLM.__init__`** [L29-37]: `def __init__(self, n_layers: int = N_LAYERS, d_model: int = D_MODEL, vocab: int = V)`
- **method `StandInLM.forward`** [L39-49]: `def forward(self, inputs, return_hooks=())`
- **function `_real_learner`** [L52-57]: `def _real_learner()`
- **function `tiny_model`** [L61-69]: `def tiny_model() -> nn.Module` decorators: @pytest.fixture(scope='session')
- **function `build_index`** [L72-82]: `def build_index(obs, order=None) -> HistoryIndex` - HistoryIndex over ``obs`` rows in ``order`` (default reversed); panels interleaved.
- **function `tiny_obs`** [L86-87]: `def tiny_obs()` decorators: @pytest.fixture(scope='session')
- **function `tiny_index`** [L91-92]: `def tiny_index(tiny_obs) -> HistoryIndex` decorators: @pytest.fixture(scope='session')
- **function `index_builder`** [L96-97]: `def index_builder()` decorators: @pytest.fixture(scope='session')
- **function `standin_cls`** [L101-102]: `def standin_cls()` decorators: @pytest.fixture(scope='session')

