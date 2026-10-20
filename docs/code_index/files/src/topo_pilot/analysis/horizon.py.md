# `src/topo_pilot/analysis/horizon.py`

- Source: [src/topo_pilot/analysis/horizon.py](../../../../../../src/topo_pilot/analysis/horizon.py)
- Kind: python
- Lines: 201

## Module docstring

> Horizon feasibility (part e, X4 Phase B): tangent-kernel audit of Q2 versus Q1.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 10, import)
- [src/topo_pilot/analysis/horizon_pools.py](horizon_pools.py.md) (line 18, import)

## Top-level constants

- `ALLOW_FLOOR`
- `AMPLIFICATION_CAP`
- `CERTIFICATE_MARGIN`
- `FACTOR_CEILING`
- `TOLERANCES`
- `ZERO_FLOOR`
- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L25-26]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `helmert_basis`** [L29-49]: `def helmert_basis(n: int) -> NDArray[np.float64]` - Orthonormal basis ``B [n, n-1]`` of the sum-zero subspace ``{v : sum(v) = 0}``.
- **function `joint_marginals`** [L52-69]: `def joint_marginals(Q2: NDArray, V: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - First- and second-symbol marginals of a lexicographic joint ``Q2 [R, V*V]``.
- **function `hellinger`** [L72-85]: `def hellinger(P: NDArray, Q: NDArray) -> NDArray[np.float64]` - Row-wise Hellinger distance ``||sqrt(p) - sqrt(q)||_2 / sqrt(2)`` in ``[0, 1]``.
- **function `safe_sqrt`** [L88-93]: `def safe_sqrt(P: NDArray) -> NDArray[np.float64]` - ``sqrt(max(P, 0))`` after checking that no entry is below ``-1e-14``.
- **class `ToleranceRow`** [L97-109] decorators: @dataclass(frozen=True) - Tangent audit at one relative tolerance ``tau`` (see :func:`tangent_audit`).
- **class `TangentAudit`** [L113-125] decorators: @dataclass(frozen=True) - Ambient tangent-kernel audit; ``verdict`` in ALLOWS_STABLE / FACTORIZES /
- **function `_row`** [L128-143]: `def _row(U: NDArray, s: NDArray, H: NDArray, G2t: NDArray, s2: NDArray, tau: float) -> ToleranceRow`
- **function `tangent_audit`** [L146-201]: `def tangent_audit(G1: NDArray, G2: NDArray, tolerances: tuple[float, ...] = TOLERANCES) -> TangentAudit` - Does ``G2`` vanish on the sum-zero kernel of ``G1``?

