# `src/topo_pilot/analysis/x4f_scores.py`

- Source: [src/topo_pilot/analysis/x4f_scores.py](../../../../../../src/topo_pilot/analysis/x4f_scores.py)
- Kind: python
- Lines: 142

## Module docstring

> X4-F scores, RBF features, support diagnostics and gate verdict (x4f-exec-v2 §4, §8–§11).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 5, 6)
- `scipy` (lines 7)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 46, import)
- [tests/c1prime/test_a_eligibility_support.py](../../../tests/c1prime/test_a_eligibility_support.py.md) (line 29, import)
- [tests/c1prime/test_b_decoder.py](../../../tests/c1prime/test_b_decoder.py.md) (line 21, import)
- [tests/c1prime/test_b_fwl.py](../../../tests/c1prime/test_b_fwl.py.md) (line 19, import)
- [tests/k4b/test_b_endpoint.py](../../../tests/k4b/test_b_endpoint.py.md) (line 33, import)
- [tools/c1prime/c1_fit.py](../../../tools/c1prime/c1_fit.py.md) (line 12, import)
- [tools/c1prime/c1_gates.py](../../../tools/c1prime/c1_gates.py.md) (line 9, import)
- [tools/k4b/k4b_decoder.py](../../../tools/k4b/k4b_decoder.py.md) (line 14, import)

## Top-level constants

- `GATES`
- `_COMPONENT`
- `_ZERO`

## Classes and functions

- **function `standardizer`** [L16-20]: `def standardizer(X_fit: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - Fit-row mean and population std; columns with std <= 1e-12 get scale 1 (centred only).
- **function `r2_pooled`** [L23-34]: `def r2_pooled(Y_pred: NDArray, Y_val: NDArray, mean_cal: NDArray) -> tuple[float | None, str]` - ``1 - SSE / SST`` pooled over coordinates, SST around the calibration mean.
- **function `kl_rows`** [L37-54]: `def kl_rows(P: NDArray, Q: NDArray) -> tuple[NDArray[np.float64] | None, str]` - ``KL(P_i || Q_i)`` in nats per row; ``P = 0`` terms are 0; ``Q = 0 < P`` -> KL_UNDEFINED.
- **function `rbf_bandwidth`** [L57-63]: `def rbf_bandwidth(X_std_cal: NDArray, rng: np.random.Generator, n_sub: int = 1024) -> tuple[float | None, str]` - Median pairwise distance among ``min(n_sub, n)`` rows drawn without replacement.
- **function `rbf_map`** [L66-70]: `def rbf_map(d: int, n_features: int, ell: float, rng: np.random.Generator) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - ``Omega = N(0,1)^{d x F} / ell`` (drawn first), then ``b ~ U[0, 2 pi)^F``.
- **function `rbf_features`** [L73-75]: `def rbf_features(X_std: NDArray, Omega: NDArray, b: NDArray) -> NDArray[np.float64]` - Random Fourier features ``sqrt(2/F) cos(X Omega + b)``.
- **function `ledoit_wolf`** [L78-89]: `def ledoit_wolf(X: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - Ledoit-Wolf (2004) shrinkage of the population covariance toward ``mu_tr I``.
- **function `_mahalanobis`** [L92-94]: `def _mahalanobis(X: NDArray, mu: NDArray, prec: NDArray) -> NDArray[np.float64]`
- **function `_knn_mean`** [L97-99]: `def _knn_mean(X: NDArray, ref: NDArray, k: int = 10) -> NDArray[np.float64]`
- **function `support_report`** [L102-123]: `def support_report(X_cal: NDArray, X_val: NDArray, patched: dict[str, NDArray]) -> dict` - Mahalanobis support of patched vectors against the calibration Ledoit-Wolf law.
- **function `support_gate`** [L126-128]: `def support_gate(frac_primary: float, fracs_random: list[float]) -> bool` - ``frac_primary <= 0.05`` and ``<= 2 * median(fracs_random)`` (literal at median 0).
- **function `gate_verdict`** [L131-142]: `def gate_verdict(per_model: dict[int, dict[str, str]]) -> tuple[str, str]` - FEASIBLE iff every gate PASS in every model; NOT_FEASIBLE iff G1 FAIL in some model;

