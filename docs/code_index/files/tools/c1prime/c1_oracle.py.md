# `tools/c1prime/c1_oracle.py`

- Source: [tools/c1prime/c1_oracle.py](../../../../../tools/c1prime/c1_oracle.py)
- Kind: python
- Lines: 274

## Module docstring

> C1' donors, symmetry and closed-form checks, the canonical oracle, G, covariates,
> eligibility and the Decimal reference helpers (API.md §4; protocol §3, §4, §15.3.7).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 11, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 12, via unique basename)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 13, via unique basename)
- `from c1_records import CertificateFlag` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 15, via same directory)
- `from oracle_profile import circle_features` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 16, via unique basename)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 18, via package root)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 4)
- `decimal` (lines 6, 8)
- `fractions` (lines 9)
- `hashlib` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_eligibility_support.py](../../tests/c1prime/test_a_eligibility_support.py.md) (line 27, import)
- [tests/c1prime/test_a_oracle.py](../../tests/c1prime/test_a_oracle.py.md) (line 30, import)
- [tests/c1prime/test_a_oracle_named.py](../../tests/c1prime/test_a_oracle_named.py.md) (line 28, import)
- [tests/c1prime/test_b_cert_bounds.py](../../tests/c1prime/test_b_cert_bounds.py.md) (line 35, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 32, import)
- [tests/c2_readout/test_a_readout.py](../../tests/c2_readout/test_a_readout.py.md) (line 28, import)
- [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 15, import)
- [tools/c1prime/c1_data.py](c1_data.py.md) (line 11, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 16, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 16, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 18, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 19, import)
- [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 23, import)
- [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 19, import)
- [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_pre.py](../c2_readout/c2_stage_pre.py.md) (line 18, import)

## Top-level constants

- `A_H3`
- `N_SIDE_X`
- `WATCHED`
- `_TE_CACHE`

## Classes and functions

- **function `F`** [L25-31]: `def F(x) -> Fraction` - Exact rational of a float, Decimal, int or Fraction; tolerance floats via their repr.
- **function `tol`** [L34-35]: `def tol(x) -> Fraction`
- **function `tau`** [L39-41]: `def tau(canonical, k) -> np.ndarray`
- **function `donors`** [L44-51]: `def donors(canon32) -> tuple`
- **function `rho_index`** [L54-58]: `def rho_index(coords, k) -> np.ndarray`
- **function `symmetry_report`** [L61-76]: `def symmetry_report(T, E, pi, coords) -> dict`
- **function `closed_form_b32`** [L79-84]: `def closed_form_b32(b31, T, E, w32, rho) -> np.ndarray`
- **function `closed_form_tolerance`** [L87-92]: `def closed_form_tolerance(eps_sym, delta=2e-12)`
- **function `rel_agree`** [L95-106]: `def rel_agree(xhat, xref, tol_) -> bool`
- **function `interval_rule`** [L109-122]: `def interval_rule(xhat, xtilde, beta, a=2e-12) -> str` - §3.4 three-way rule against I_v = [x~/(1+beta), x~/(1-beta)], exact rationals.
- **function `run_oracle`** [L126-129]: `def run_oracle(T, E, pi, tokens32) -> dict`
- **function `_osum_dot`** [L132-136]: `def _osum_dot(x, y) -> np.ndarray`
- **function `G_hat`** [L139-143]: `def G_hat(qp, qm) -> tuple`
- **function `named_from_canonical`** [L146-150]: `def named_from_canonical(x, perm) -> np.ndarray`
- **function `canonical_from_named_cols`** [L153-154]: `def canonical_from_named_cols(x, perm) -> np.ndarray`
- **function `G_named`** [L157-158]: `def G_named(d, lam, perm) -> np.ndarray`
- **function `_y`** [L162-163]: `def _y(coords) -> np.ndarray`
- **function `y_marginal`** [L166-169]: `def y_marginal(b, coords) -> np.ndarray`
- **function `m32`** [L172-173]: `def m32(b, coords) -> np.ndarray`
- **function `nuisance`** [L176-180]: `def nuisance(b, coords) -> np.ndarray`
- **function `s_max`** [L183-184]: `def s_max(s_cal) -> float`
- **function `eligible`** [L187-189]: `def eligible(sp, sm, smax, le_H, le_Hp, le_Hm) -> np.ndarray`
- **function `eligible_fraction`** [L192-194]: `def eligible_fraction(mask) -> float`
- **function `kappa_nu`** [L197-201]: `def kappa_nu(nu_p, nu_m, nu_nat_cal, elig_cal) -> float`
- **function `leakage_active`** [L204-205]: `def leakage_active(kappa) -> bool`
- **function `_flags_check`** [L209-212]: `def _flags_check(ctx) -> None`
- **function `decimal_posterior60`** [L215-222]: `def decimal_posterior60(T, E, pi, suffix) -> list` - Replica (provenance: K4 error_bound._reference_posterior, 8 lines) with C1's §16 mapping:
- **function `_decimal_TE`** [L228-240]: `def _decimal_TE(T, E, digits) -> list`
- **function `decimal_predictive`** [L243-249]: `def decimal_predictive(b, T, E, digits=60) -> list`
- **function `decimal_reference`** [L252-261]: `def decimal_reference(T, E, pi, h32) -> dict`
- **function `decimal_G`** [L264-268]: `def decimal_G(q_p, q_m) -> Decimal`
- **function `h3_compare`** [L271-274]: `def h3_compare(x_hat, x_dec, p1_ok, beta) -> str`

