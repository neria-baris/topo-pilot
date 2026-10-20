# `src/topo_pilot/process/conductance.py`

- Source: [src/topo_pilot/process/conductance.py](../../../../../../src/topo_pilot/process/conductance.py)
- Kind: python
- Lines: 91

## Module docstring

> Metric-conductance transition kernel on a fixed lattice (X5 G1, x5g1-feas-v2 §2).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from ._geometry import check_state_order, fail` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 16, via relative)
- `from .transition import adjacency, check_support` -> [src/topo_pilot/process/transition.py](transition.py.md) (line 17, via relative)

### External (third-party)

- `numpy` (lines 11, 12)

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/process/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/process/stage.py](stage.py.md) (line 12, import)

## Top-level constants

- none

## Classes and functions

- **class `ConductanceConfig`** [L21-25] decorators: @dataclass(frozen=True) - Warp amplitude ``a`` (|a| < 1) and total off-diagonal mass at ``C_max`` (``move``).
- **function `warp_profile`** [L28-46]: `def warp_profile(dims: tuple[int, int], a: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - Warped circumference profile and horizontal edge lengths.
- **function `conductance_kernel`** [L49-91]: `def conductance_kernel(world: WorldSpec, cfg: ConductanceConfig) -> tuple[TransitionSpec, dict]` - Symmetric lazy kernel from edge conductances ``c = 1 / l^2``.

