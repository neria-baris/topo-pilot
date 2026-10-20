# `src/topo_pilot/process/transition.py`

- Source: [src/topo_pilot/process/transition.py](../../../../../../src/topo_pilot/process/transition.py)
- Kind: python
- Lines: 86

## Module docstring

> Transition kernel builder: max-degree lazy walk on the world's 1-skeleton.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from ._geometry import check_state_order, fail` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 12, via relative)

### External (third-party)

- `numpy` (lines 8)

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

- [src/topo_pilot/process/__init__.py](__init__.py.md) (line 16, import)
- [src/topo_pilot/process/conductance.py](conductance.py.md) (line 17, import)
- [src/topo_pilot/process/stage.py](stage.py.md) (line 14, import)
- [tests/d1_seam/test_d1_seam.py](../../../tests/d1_seam/test_d1_seam.py.md) (line 18, import)
- [tests/process/test_transition.py](../../../tests/process/test_transition.py.md) (line 13, import)
- [tests/x2a_stage0/test_x2a_stage0.py](../../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 22, import)

## Top-level constants

- none

## Classes and functions

- **class `TransitionConfig`** [L16-20] decorators: @dataclass(frozen=True) - Config of the transition kernel: ``kind`` and the self-loop floor ``p_stay`` in [0, 1).
- **function `adjacency`** [L23-30]: `def adjacency(world: WorldSpec) -> np.ndarray` - Symmetric 0/1 adjacency ``A [N, N]`` of the world's edge list.
- **function `check_support`** [L33-43]: `def check_support(T: np.ndarray, world: WorldSpec) -> None` - Require ``supp(T)`` within edges and diagonal (contracts cannot check this, D-011).
- **class `TransitionBuilder`** [L46-86] - Builds ``TransitionSpec`` from a world; never sees an emission matrix.
- **method `TransitionBuilder.build`** [L49-86]: `def build(self, world: WorldSpec, cfg: TransitionConfig) -> TransitionSpec` - Max-degree lazy walk.

