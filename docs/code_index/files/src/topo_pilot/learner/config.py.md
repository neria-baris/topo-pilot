# `src/topo_pilot/learner/config.py`

- Source: [src/topo_pilot/learner/config.py](../../../../../../src/topo_pilot/learner/config.py)
- Kind: python
- Lines: 50

## Module docstring

> Frozen configuration dataclasses of the learner (SPEC public API).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
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

- [src/topo_pilot/learner/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/learner/model.py](model.py.md) (line 15, import)
- [src/topo_pilot/learner/multihorizon.py](multihorizon.py.md) (line 20, import)
- [src/topo_pilot/learner/stage.py](stage.py.md) (line 22, import)
- [src/topo_pilot/learner/trainer.py](trainer.py.md) (line 17, import)
- [tests/c2_readout/test_a_readout.py](../../../tests/c2_readout/test_a_readout.py.md) (line 34, import)
- [tools/c2_nd/nd_dry.py](../../../tools/c2_nd/nd_dry.py.md) (line 39, import)

## Top-level constants

- none

## Classes and functions

- **class `ModelConfig`** [L10-29] decorators: @dataclass(frozen=True) - Decoder-only transformer hyper-parameters.
- **class `TrainConfig`** [L33-50] decorators: @dataclass(frozen=True) - Optimisation hyper-parameters (RESEARCH_SUMMARY section 6).

