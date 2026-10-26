# `src/topo_pilot/process/emission.py`

- Source: [src/topo_pilot/process/emission.py](../../../../../../src/topo_pilot/process/emission.py)
- Kind: python
- Lines: 217

## Module docstring

> Emission builders: overlap (O), axis-permuted (P), full-permuted, identical (N), unique (U).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import EmissionSpec, ErrorCode, SeedTree, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 24, via package root)
- `from ._diagnostics import check_row_multiset, check_symbols_alive, emission_diagnostics` -> [src/topo_pilot/process/_diagnostics.py](_diagnostics.py.md) (line 26, via relative)
- `from ._geometry import check_state_order, fail, point_distances` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 27, via relative)
- `from .centers import CENTER_REGISTRY, check_centers_in_chart` -> [src/topo_pilot/process/centers.py](centers.py.md) (line 28, via relative)

### External (third-party)

- `numpy` (lines 20, 21)
- `scipy` (lines 22)

### Standard library

- `__future__` (lines 14)
- `abc` (lines 16)
- `dataclasses` (lines 17)
- `typing` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/process/__init__.py](__init__.py.md) (line 5, import)
- [src/topo_pilot/process/stage.py](stage.py.md) (line 13, import)
- [tests/process/test_controls.py](../../../tests/process/test_controls.py.md) (line 33, import)
- [tests/x2a_stage0/test_x2a_stage0.py](../../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 21, import)
- [tests/x6_stage0/test_x6_stage0.py](../../../tests/x6_stage0/test_x6_stage0.py.md) (line 376, import)
- [tools/theory_exact/theory_exact3.py](../../../tools/theory_exact/theory_exact3.py.md) (line 20, import)
- [tools/x2a_stage0/x2a_model.py](../../../tools/x2a_stage0/x2a_model.py.md) (line 26, import)

## Top-level constants

- `EMISSION_REGISTRY`
- `WORLD_SCOPE_MASTER`

## Classes and functions

- **class `EmissionConfig`** [L35-43] decorators: @dataclass(frozen=True) - Emission config. ``sigma`` is used by overlap and by the permuted modes (source sigma).
- **class `_Core`** [L47-53] decorators: @dataclass(frozen=True) - Overlap matrix in center order plus the geometry that produced it.
- **function `draw_axis_permutation`** [L56-65]: `def draw_axis_permutation(world: WorldSpec) -> tuple[NDArray[np.int64], NDArray[np.int64]]` - World-scoped ``(sigma_x, sigma_y)``: permutations of ``dims[0]`` and ``dims[1]``.
- **function `axis_state_perm`** [L68-74]: `def axis_state_perm(sx: NDArray[np.int64], sy: NDArray[np.int64], dims: tuple[int, ...]) -> NDArray[np.int64]` - State permutation of P: ``state_perm[x*n1 + y] = sx[x]*n1 + sy[y]``.
- **function `_check_config`** [L77-80]: `def _check_config(world: WorldSpec, cfg: EmissionConfig) -> None`
- **function `_symbol_perm`** [L83-85]: `def _symbol_perm(world: WorldSpec, rng_tree: SeedTree, n_symbols: int) -> NDArray[np.int64]`
- **function `_overlap_core`** [L88-102]: `def _overlap_core(world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> _Core` - ``E[z, j] = softmax_j(-d(z, c_j)^2 / 2 sigma^2)`` in float64 via log-sum-exp.
- **function `_assemble`** [L105-117]: `def _assemble(world: WorldSpec, mode: str, E_centers: NDArray[np.float64], symbol_perm: NDArray[np.int64], coverage: float, *, sigma: float | None = None, centers: NDArray[np.float64] | None = None, strategy: str | None = None, state_perm: NDArray[np.int64] | None = None) -> EmissionSpec` - Apply the symbol naming, compute diagnostics, check symbols, validate.
- **class `EmissionModel(ABC)`** [L120-127] - Variation point: one emission mode. Never receives a transition kernel.
- **method `EmissionModel.build`** [L126-127]: `def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec` decorators: @abstractmethod - Build the ``EmissionSpec`` for ``world`` (shapes ``E [N, V]``, rows sum to 1).
- **class `OverlapGaussian(EmissionModel)`** [L130-144] - O: ``E[z, j] = softmax_j(-d(z, c_j)^2 / 2 sigma^2)``, no truncation, symbols renamed.
- **method `OverlapGaussian.build`** [L140-144]: `def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec`
- **class `_PermutedModel(EmissionModel)`** [L147-164] - Shared logic of the state-permuted controls (composition over the overlap source).
- **method `_PermutedModel._state_perm`** [L151-152]: `def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]` decorators: @abstractmethod - World-scoped state permutation (``E_perm[z] = E_O[perm[z]]``).
- **method `_PermutedModel.build`** [L154-164]: `def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec`
- **class `AxisPermuted(_PermutedModel)`** [L167-178] - P: ``E_P[(x, y)] = E_O[(sx(x), sy(y))]`` with world-scoped ``sx, sy``.
- **method `AxisPermuted._state_perm`** [L176-178]: `def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]`
- **class `FullPermuted(_PermutedModel)`** [L181-188] - Extension: a world-scoped permutation of all N states (breaks product structure).
- **method `FullPermuted._state_perm`** [L186-188]: `def _state_perm(self, world: WorldSpec) -> NDArray[np.int64]`
- **class `Identical(EmissionModel)`** [L191-200] - N: ``E = 1/V`` (world-independent negative control).
- **method `Identical.build`** [L196-200]: `def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec`
- **class `Unique(EmissionModel)`** [L203-213] - U: ``V = N`` and E is a permutation matrix (identity up to symbol names).
- **method `Unique.build`** [L208-213]: `def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec`

