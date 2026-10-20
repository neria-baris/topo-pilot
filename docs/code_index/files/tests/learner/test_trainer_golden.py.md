# `tests/learner/test_trainer_golden.py`

- Source: [tests/learner/test_trainer_golden.py](../../../../../tests/learner/test_trainer_golden.py)
- Kind: python
- Lines: 109

## Module docstring

> T-GOLD (D2A-FROZEN-v1 §4.6): the default Trainer path is byte-identical to golden values
> generated at commit A by the unchanged Trainer, for two configurations at one and two intra-op
> threads (one inter-op thread). Each case runs in its own subprocess so the thread settings are
> applied before any torch work. Regenerate (commit A only): python test_trainer_golden.py --write

## Imports

### Internal (repo files)

- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 24, via package root) (inside a function)
- `from d1_seam import float_model` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 42, via sys.path edit) (inside a function)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 44, via package root) (inside a function)
- `from topo_pilot.dataset import HMMSampler, PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 45, via package root) (inside a function)
- `from topo_pilot.learner import Trainer, serialise_state` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 46, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 39, 82)
- `torch` (lines 35, 83)

### Standard library

- `__future__` (lines 7)
- `hashlib` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 15)
- `platform` (lines 12)
- `subprocess` (lines 13)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 41: `str(REPO / 'tools' / 'd1_seam')` -> `tools/d1_seam`

## Imported by

- none

## Top-level constants

- `CASES`
- `GOLDEN`
- `HERE`
- `REPO`

## Classes and functions

- **function `_configs`** [L23-31]: `def _configs(name)`
- **function `_worker`** [L34-69]: `def _worker(name: str, n: int) -> dict`
- **function `_run_case`** [L72-78]: `def _run_case(name: str, n: int) -> dict`
- **function `_environment`** [L81-91]: `def _environment() -> dict`
- **test `test_default_trainer_matches_golden`** [L94-98]: `def test_default_trainer_matches_golden()`

