# `src/topo_pilot/analysis/circular.py`

- Source: [src/topo_pilot/analysis/circular.py](../../../../../../src/topo_pilot/analysis/circular.py)
- Kind: python
- Lines: 242

## Module docstring

> Part (c) circular correspondence: agreement of circular coordinates with a latent angle.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, EvalSidecar, MetricRow, StageFailure, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 13, via package root)
- `from topo_pilot.topology import CircularCoordinates` -> [src/topo_pilot/topology/__init__.py](../topology/__init__.py.md) (line 21, via package root)
- `from .spaces import SpaceBuilder` -> [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 23, via relative)

### External (third-party)

- `numpy` (lines 9, 10)
- `scipy` (lines 11)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 4, import)

## Top-level constants

- `_COMPONENT`
- `_SPACE`

## Classes and functions

- **function `_fail`** [L29-30]: `def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure`
- **function `circular_agreement`** [L33-62]: `def circular_agreement(phi: ArrayLike, theta: ArrayLike) -> float` - Rotation- and reflection-invariant agreement of two angle vectors.
- **function `_axis_coords`** [L65-71]: `def _axis_coords(coords: NDArray, axis: int, period: float) -> NDArray[np.float64]`
- **function `lattice_angle`** [L74-95]: `def lattice_angle(coords: NDArray, states: ArrayLike, axis: int, period: float) -> NDArray[np.float64]` - Angle of each state along one lattice axis.
- **function `belief_angle`** [L98-127]: `def belief_angle(b: NDArray, coords: NDArray, axis: int, period: float) -> NDArray[np.float64]` - Circular mean of each belief along one lattice axis.
- **class `CircularCorrespondence`** [L130-242] - Do the circular coordinates of an activation cloud track a latent angle?
- **method `CircularCorrespondence.__init__`** [L155-157]: `def __init__(self, coeff_p: int = 47, n_perm: int = 1000)`
- **method `CircularCorrespondence.compare`** [L159-181]: `def compare(self, D: NDArray, theta: NDArray, rng: np.random.Generator) -> dict` - Circular coordinates of ``D`` against ``theta`` with a permutation null.
- **method `CircularCorrespondence._states`** [L183-199]: `def _states(self, store: ArtifactStore, builder: SpaceBuilder, activation_set_id: str, sidecar_id: str, ids: list[str], panel: int) -> NDArray[np.int64]`
- **method `CircularCorrespondence.run`** [L201-233]: `def run(self, store: ArtifactStore, activation_set_id: str, sidecar_id: str, world_id: str, oracle_id: str, hook: str, panel: int, rng: np.random.Generator, axis: int = 0, control_axis: int = 1, **row_fields) -> list[MetricRow]` - Compare the circular coordinates of a panel cloud with latent angles (privileged_eval).
- **method `CircularCorrespondence._row`** [L236-242]: `def _row(run_id: str, hook: str, panel: int, name: str, value: float | None, row_fields: dict) -> MetricRow` decorators: @staticmethod

