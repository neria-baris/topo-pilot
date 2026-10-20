# `tools/c1prime/c1_endpoint.py`

- Source: [tools/c1prime/c1_endpoint.py](../../../../../tools/c1prime/c1_endpoint.py)
- Kind: python
- Lines: 131

## Module docstring

> C1' crossed contrast, inference and decision (API.md §11; protocol §11-§13; §15.3.2 C4-C7).
> A, Y, Z and Z_full use the prescribed ordered elementwise kernels; bootstrap means use the tree
> kernel with one shared index draw per bootstrap replicate; ranks are verified at run time.

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 10, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 11, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](c1_means.py.md) (line 12, via same directory)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 14, via unique basename)
- `from oracle_profile import percentile_interval` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 15, via unique basename)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 8)
- `math` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_cert_bounds.py](../../tests/c1prime/test_b_cert_bounds.py.md) (line 34, import)
- [tests/c1prime/test_b_identities.py](../../tests/c1prime/test_b_identities.py.md) (line 31, import)
- [tests/c1prime/test_b_inference.py](../../tests/c1prime/test_b_inference.py.md) (line 29, import)
- [tests/c1prime/test_b_precision.py](../../tests/c1prime/test_b_precision.py.md) (line 28, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 278, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 12, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 16, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 15, import)

## Top-level constants

- `P_HIGH`
- `P_LOW`

## Classes and functions

- **function `_osum_dot`** [L21-25]: `def _osum_dot(x, y) -> np.ndarray`
- **function `A_hat`** [L28-32]: `def A_hat(d, z_plus, z_minus) -> np.ndarray` - C4: Delta = z+ - z-, A = 0.5 * osum_v(d_v * Delta_v) (canonical order, caller-gathered).
- **function `Y_hat`** [L35-39]: `def Y_hat(A_T, A_C_list) -> np.ndarray`
- **function `Z_hat`** [L42-43]: `def Z_hat(Y, G) -> np.ndarray`
- **function `Zfull_hat`** [L46-47]: `def Zfull_hat(A_full, G) -> np.ndarray`
- **function `A_logsoftmax`** [L50-53]: `def A_logsoftmax(qp, qm, lp_plus, lp_minus) -> np.ndarray` - The log-softmax definition (secondary quantities and checks only).
- **function `endpoint_bounds`** [L56-63]: `def endpoint_bounds(Z_by_model, seed=520503, draws=5000) -> dict`
- **function `per_model_status`** [L66-69]: `def per_model_status(L, U) -> str`
- **function `overall`** [L72-76]: `def overall(statuses) -> str`
- **function `v3`** [L79-85]: `def v3(Zfull_by_model, B_V3, seed) -> dict`
- **function `h5`** [L88-95]: `def h5(G, B_H, seed) -> dict`
- **function `ladder`** [L98-115]: `def ladder(Z_val, G_val, models=c1_config.MODELS) -> dict`
- **function `k_blocks`** [L118-120]: `def k_blocks(N_test, f_val) -> int`
- **function `fresh_fraction_ok`** [L123-125]: `def fresh_fraction_ok(f_test, f_val) -> bool`
- **function `ratio_reduction`** [L128-131]: `def ratio_reduction(meanY, meanG, c) -> bool`

