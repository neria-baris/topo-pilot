# `src/topo_pilot/process/_geometry.py`

- Source: [src/topo_pilot/process/_geometry.py](../../../../../../src/topo_pilot/process/_geometry.py)
- Kind: python
- Lines: 95

## Module docstring

> Pure geometry helpers shared by the process builders (no I/O, no randomness).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 5, 6)

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

- [src/topo_pilot/process/_diagnostics.py](_diagnostics.py.md) (line 14, import)
- [src/topo_pilot/process/centers.py](centers.py.md) (line 14, import)
- [src/topo_pilot/process/conductance.py](conductance.py.md) (line 16, import)
- [src/topo_pilot/process/emission.py](emission.py.md) (line 27, import)
- [src/topo_pilot/process/stage.py](stage.py.md) (line 11, import)
- [src/topo_pilot/process/transition.py](transition.py.md) (line 12, import)
- [tests/d1_seam/test_d1_seam.py](../../../tests/d1_seam/test_d1_seam.py.md) (line 17, import)
- [tests/hws/test_b_worlds.py](../../../tests/hws/test_b_worlds.py.md) (line 38, import)
- [tests/process/test_geometry.py](../../../tests/process/test_geometry.py.md) (line 11, import)
- [tests/x2a_stage0/test_x2a_stage0.py](../../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 20, import)
- [tests/x6_stage0/test_x6_stage0.py](../../../tests/x6_stage0/test_x6_stage0.py.md) (line 375, import)
- [tools/hws/hws_worlds.py](../../../tools/hws/hws_worlds.py.md) (line 30, import)

## Top-level constants

- `COMPONENT`

## Classes and functions

- **function `fail`** [L13-15]: `def fail(code: ErrorCode, check: str, detail: str) -> StageFailure` - Build a ``StageFailure`` attributed to the process module.
- **function `is_x_periodic`** [L18-47]: `def is_x_periodic(world: WorldSpec) -> bool` - True if axis 0 is glued with period ``dims[0]``, read from the complex, not the name.
- **function `check_state_order`** [L50-64]: `def check_state_order(world: WorldSpec) -> None` - Require ``coords[x * dims[1] + y] == (x, y)`` (state order equals vertex-id order).
- **function `point_distances`** [L67-95]: `def point_distances(world: WorldSpec, points: NDArray[np.float64], metric: str = 'flat') -> NDArray[np.float64]` - Distances ``d(z, p)`` from every state to every point of ``points``.

