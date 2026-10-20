# `src/topo_pilot/world/complex.py`

- Source: [src/topo_pilot/world/complex.py](../../../../../../src/topo_pilot/world/complex.py)
- Kind: python
- Lines: 215

## Module docstring

> Cubical complex: signed boundary matrices over Z, exact ranks and Betti numbers over GF(p).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7)
- `scipy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `typing` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/world/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/world/lattice.py](lattice.py.md) (line 12, import)
- [src/topo_pilot/world/metrics.py](metrics.py.md) (line 16, import)
- [src/topo_pilot/world/registry.py](registry.py.md) (line 10, import)
- [tools/d1_seam/d1_seam.py](../../../tools/d1_seam/d1_seam.py.md) (line 20, import)
- [tools/x2a_stage0/x2a_model.py](../../../tools/x2a_stage0/x2a_model.py.md) (line 27, import)
- [tools/x6_stage0/x6_model.py](../../../tools/x6_stage0/x6_model.py.md) (line 25, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L15-16]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `rank_mod_p`** [L19-48]: `def rank_mod_p(matrix: np.ndarray, p: int) -> int` - Rank of an integer matrix over GF(p) by Gaussian elimination on dense ``int64``.
- **function `_is_prime`** [L51-52]: `def _is_prime(p: int) -> bool`
- **function `_face_table`** [L55-66]: `def _face_table(k: int) -> list[tuple[int, list[int]]]` - For a k-cube: ``[(sign, corner indices)]`` of its 2k facets.
- **function `_perm_sign`** [L69-78]: `def _perm_sign(perm: list[int]) -> int`
- **function `_relative_orientation`** [L81-105]: `def _relative_orientation(face: tuple[int, ...], stored: tuple[int, ...], m: int) -> int` - Sign of the cube symmetry taking the vertex tuple ``face`` to ``stored`` (m-cubes).
- **class `CubicalComplex`** [L108-204] - Cells of dim 0..3 as ordered vertex tuples (a k-cube has 2**k vertices, in local
- **method `CubicalComplex.__init__`** [L134-149]: `def __init__(self, n_vertices: int, cells: Mapping[int, np.ndarray])`
- **method `CubicalComplex.top_dim`** [L152-154]: `def top_dim(self) -> int` decorators: @property - Highest cell dimension K.
- **method `CubicalComplex.boundary_matrix`** [L156-160]: `def boundary_matrix(self, k: int) -> sp.csr_matrix` - Signed integer boundary ``d_k`` of shape ``[n_{k-1}, n_k]`` (cached).
- **method `CubicalComplex._build_boundary`** [L162-182]: `def _build_boundary(self, k: int) -> sp.csr_matrix`
- **method `CubicalComplex.betti`** [L184-194]: `def betti(self, p: int = 2) -> tuple[int, ...]` - Betti numbers ``(beta_0..beta_K)`` over GF(p), p prime.
- **method `CubicalComplex.euler_characteristic`** [L196-198]: `def euler_characteristic(self) -> int` - ``sum_k (-1)^k n_k``.
- **method `CubicalComplex.one_skeleton`** [L200-204]: `def one_skeleton(self) -> np.ndarray` - ``int32[E, 2]`` edges, canonical ``(lo, hi)``, unique, lexicographically sorted.
- **function `check_boundary_closed`** [L207-215]: `def check_boundary_closed(cx: CubicalComplex) -> None` - Require ``d_{k-1} d_k = 0`` over Z for all k.

