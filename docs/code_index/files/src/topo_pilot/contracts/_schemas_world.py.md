# `src/topo_pilot/contracts/_schemas_world.py`

- Source: [src/topo_pilot/contracts/_schemas_world.py](../../../../../../src/topo_pilot/contracts/_schemas_world.py)
- Kind: python
- Lines: 211

## Module docstring

> World and process artifacts: WorldSpec, TransitionSpec, EmissionSpec (DATA_SCHEMAS §2).

## Imports

### Internal (repo files)

- `from . import _checks` -> [src/topo_pilot/contracts/_checks.py](_checks.py.md) (line 11, via relative)
- `from .base import Artifact, array_field, optional_array_field` -> [src/topo_pilot/contracts/base.py](base.py.md) (line 12, via relative)
- `from .errors import ErrorCode` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 13, via relative)

### External (third-party)

- `numpy` (lines 9)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 5)
- `dataclasses` (lines 6)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 24, import)

## Top-level constants

- `EMISSION_DIAGNOSTIC_KEYS`
- `EMISSION_MODES`
- `MIN_SYMBOL_PROB`

## Classes and functions

- **class `WorldSpec(Artifact)`** [L22-108] decorators: @dataclass(frozen=True, eq=False) - A latent world: states, the cubical complex defining the surface, metrics, homology.
- **method `WorldSpec.n_states`** [L62-64]: `def n_states(self) -> int` decorators: @property - Number of states N.
- **method `WorldSpec.validate`** [L66-81]: `def validate(self) -> None`
- **method `WorldSpec._validate_cells`** [L83-108]: `def _validate_cells(self, n: int) -> None`
- **function `_n_components`** [L111-122]: `def _n_components(n: int, edges: np.ndarray) -> int`
- **class `TransitionSpec(Artifact)`** [L126-157] decorators: @dataclass(frozen=True, eq=False) - Transition kernel ``T[i, j] = P(z_{t+1} = j | z_t = i)`` (``[N, N] float64``) and ``pi [N]``.
- **method `TransitionSpec.validate`** [L143-157]: `def validate(self) -> None`
- **class `EmissionSpec(Artifact)`** [L161-211] decorators: @dataclass(frozen=True, eq=False) - Emission matrix ``E[z, w] = P(w_t = w | z_t = z)`` (``[N, V] float64``).
- **method `EmissionSpec.validate`** [L185-211]: `def validate(self) -> None`

