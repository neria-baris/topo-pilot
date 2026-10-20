# `tests/d2a/test_a_pad.py`

- Source: [tests/d2a/test_a_pad.py](../../../../../tests/d2a/test_a_pad.py)
- Kind: python
- Lines: 74

## Module docstring

> Independent T-PAD test (job 0028, author A), from D2A-FROZEN-v1 sections 2.2 and 11.4 and
> tools/d2a/API.md only: padding a constructed history after t changes no activation, next-symbol
> logit or joint logit at model positions <= t. Tiny MultiHorizonLM (4 layers, so every hook
> including resid_post_3 exists), CPU, eval mode.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 16, via package root)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 17, via package root)
- `from topo_pilot.learner.multihorizon import MultiHorizonLM` -> [src/topo_pilot/learner/multihorizon.py](../../src/topo_pilot/learner/multihorizon.py.md) (line 18, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 25, via sys.path edit)
- `import d2a_world` -> [tools/d2a/d2a_world.py](../../tools/d2a/d2a_world.py.md) (line 26, via sys.path edit)

### External (third-party)

- `numpy` (lines 12)
- `pytest` (lines 13)
- `torch` (lines 14)

### Standard library

- `__future__` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO_ROOT.joinpath(*_parts))` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CFG`
- `REPO_ROOT`

## Classes and functions

- **function `_histories`** [L34-38]: `def _histories()`
- **function `model`** [L42-46]: `def model()` decorators: @pytest.fixture(scope='module')
- **test `test_T_PAD_padding_after_t_changes_nothing_up_to_t`** [L50-74]: `def test_T_PAD_padding_after_t_changes_nothing_up_to_t(name, model)` decorators: @pytest.mark.parametrize('name', list(_histories()))

