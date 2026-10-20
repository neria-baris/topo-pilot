# `src/topo_pilot/process/_diagnostics.py`

- Source: [src/topo_pilot/process/_diagnostics.py](../../../../../../src/topo_pilot/process/_diagnostics.py)
- Kind: python
- Lines: 98

## Module docstring

> Pure emission diagnostics and build-time checks (entropies, factorisation, row multiset).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from ._geometry import fail` -> [src/topo_pilot/process/_geometry.py](_geometry.py.md) (line 14, via relative)

### External (third-party)

- `numpy` (lines 8, 9)
- `scipy` (lines 10)

### Standard library

- `__future__` (lines 3)
- `math` (lines 5)
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

- [src/topo_pilot/process/emission.py](emission.py.md) (line 26, import)
- [tests/process/test_controls.py](../../../tests/process/test_controls.py.md) (line 32, import)
- [tests/process/test_overlap.py](../../../tests/process/test_overlap.py.md) (line 18, import)

## Top-level constants

- `FACTORIZE_TOL`
- `MIN_SYMBOL_PROB`
- `QUANTILES`

## Classes and functions

- **function `row_entropies`** [L21-23]: `def row_entropies(E: NDArray[np.float64]) -> NDArray[np.float64]` - Natural-log entropy of every row of ``E [N, V]`` -> ``[N]``.
- **function `factorizes`** [L26-43]: `def factorizes(E_centers: NDArray[np.float64], dims: tuple[int, ...]) -> bool` - Numerical product-structure test on ``E`` with columns in center order ``j = a*k + b``.
- **function `emission_diagnostics`** [L46-71]: `def emission_diagnostics(E: NDArray[np.float64], E_centers: NDArray[np.float64], dims: tuple[int, ...], coverage_radius: float) -> dict[str, Any]` - Diagnostics under the uniform state distribution ``pi = 1/N`` (natural log).
- **function `check_symbols_alive`** [L74-83]: `def check_symbols_alive(p_w: NDArray[np.float64]) -> None` - Require every ``p_w >= 1e-4``.
- **function `check_row_multiset`** [L86-98]: `def check_row_multiset(E_source: NDArray[np.float64], E_permuted: NDArray[np.float64]) -> None` - Require the rows of ``E_permuted`` to be a permutation of the rows of ``E_source``.

