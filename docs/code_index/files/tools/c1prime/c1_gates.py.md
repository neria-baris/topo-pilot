# `tools/c1prime/c1_gates.py`

- Source: [tools/c1prime/c1_gates.py](../../../../../tools/c1prime/c1_gates.py)
- Kind: python
- Lines: 115

## Module docstring

> C1' damage, leakage, support, registration and adequacy gates (API.md §10; protocol §7-§10).
> All operational (not certified): fractions, inverted_cdf quantiles, inequalities as written.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 6, via same directory)
- `from topo_pilot.analysis.x4f_scores import r2_pooled` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 7)

### Standard library

- `__future__` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_eligibility_support.py](../../tests/c1prime/test_a_eligibility_support.py.md) (line 26, import)
- [tests/c1prime/test_b_gates.py](../../tests/c1prime/test_b_gates.py.md) (line 25, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 14, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 17, import)

## Top-level constants

- `M2`

## Classes and functions

- **function `D_w`** [L15-18]: `def D_w(w_nat, w_pm_list) -> float`
- **function `D_y`** [L21-24]: `def D_y(y_nat, y_pm_list, tr_cov) -> float`
- **function `leakage`** [L27-30]: `def leakage(y_p, y_m, nu_p, nu_m) -> float`
- **function `m2`** [L33-47]: `def m2(Dw_T, Dy_T, Dw_C_list, Dy_C_list, L_T=None, active=False) -> dict`
- **function `mahalanobis`** [L50-54]: `def mahalanobis(a, w, zt, fit, white) -> np.ndarray`
- **function `q99`** [L57-58]: `def q99(DM_cal) -> float`
- **function `frac_beyond`** [L61-63]: `def frac_beyond(DM, q) -> float`
- **function `m3`** [L66-73]: `def m3(F_S, F_D, F_T, F_C_list, Sup) -> dict`
- **function `wrap`** [L76-79]: `def wrap(x) -> np.ndarray` - Angle to (-pi, pi].
- **function `_med`** [L82-83]: `def _med(x) -> float`
- **function `v1`** [L86-95]: `def v1(phi_p, phi_m, m32_p, m32_m) -> dict`
- **function `v2`** [L98-107]: `def v2(phi_s, phi_pm, phi_T_pm) -> dict`
- **function `m4`** [L110-115]: `def m4(w_pred, w_true, y_pred, y_true, y_mean_cal) -> dict`

