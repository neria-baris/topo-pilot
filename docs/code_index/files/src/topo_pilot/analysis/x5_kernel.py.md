# `src/topo_pilot/analysis/x5_kernel.py`

- Source: [src/topo_pilot/analysis/x5_kernel.py](../../../../../../src/topo_pilot/analysis/x5_kernel.py)
- Kind: python
- Lines: 104

## Module docstring

> X5 G1 exact process diagnostics (x5g1-feas-v2 §3): rate, spectrum, mixing bound, integrated
> autocorrelation of state functions, rate-matched diagnostic kernel. Reversible kernels only.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 9, 10)

### Standard library

- `__future__` (lines 4)
- `dataclasses` (lines 7)
- `math` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 84, import)

## Top-level constants

- `_FLOOR`

## Classes and functions

- **function `movement_rate`** [L15-17]: `def movement_rate(T: NDArray, pi: NDArray) -> float` - ``r = sum_z pi_z (1 - T_zz)``.
- **function `is_connected`** [L20-33]: `def is_connected(T: NDArray) -> bool` - Undirected connectivity of ``{i != j : T_ij > 0 or T_ji > 0}``.
- **function `_sym`** [L36-39]: `def _sym(T: NDArray, pi: NDArray) -> NDArray[np.float64]`
- **class `SpectrumReport`** [L43-52] decorators: @dataclass(frozen=True, eq=False) - Descending eigenvalues, ``gap = 1 - lam2``, ``abs_gap = 1 - max(|lam2|, |lam_min|)``,
- **function `spectrum_report`** [L55-67]: `def spectrum_report(T: NDArray, pi: NDArray, eps: float = 0.25) -> SpectrumReport` - Spectrum of a pi-reversible kernel and the bound
- **function `integrated_autocorrelation`** [L70-92]: `def integrated_autocorrelation(T: NDArray, pi: NDArray, g: NDArray) -> tuple[float | None, str]` - Exact integrated autocorrelation time of a state function under a reversible kernel.
- **function `rate_matched_kernel`** [L95-104]: `def rate_matched_kernel(T: NDArray, alpha: float) -> tuple[NDArray[np.float64] | None, str]` - ``I + alpha (T - I)``; ``INVALID_KERNEL`` if alpha <= 0, a negative entry, or a diagonal

