# `tools/c1prime/c1_cert.py`

- Source: [tools/c1prime/c1_cert.py](../../../../../tools/c1prime/c1_cert.py)
- Kind: python
- Lines: 217

## Module docstring

> C1' numerical certificate core (API.md §5; CERTIFICATE.md; protocol §15.3.2-15.3.7).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 14, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 15, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 16, via unique basename)
- `from c1_records import C1GateFailure, CertificateFlag` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 18, via same directory)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 6)
- `decimal` (lines 8, 11)
- `fractions` (lines 12)
- `hashlib` (lines 9)
- `math` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_cert_guards.py](../../tests/c1prime/test_b_cert_guards.py.md) (line 36, import)
- [tests/c1prime/test_b_cert_oracle.py](../../tests/c1prime/test_b_cert_oracle.py.md) (line 34, import)
- [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 9, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 13, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 10, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 10, import)
- [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 19, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 169, import)

## Top-level constants

- `TWO_M1000`
- `U`
- `U1`
- `ZETA`

## Classes and functions

- **function `gamma`** [L29-31]: `def gamma(n) -> Fraction`
- **function `rho_bar_ref`** [L34-35]: `def rho_bar_ref(L, N, d) -> Fraction`
- **function `up`** [L38-41]: `def up(c) -> float`
- **function `OUT`** [L44-45]: `def OUT(x) -> Fraction`
- **function `osum`** [L48-52]: `def osum(cols) -> np.ndarray`
- **function `supports`** [L55-59]: `def supports(T) -> tuple`
- **function `reference_oracle`** [L62-84]: `def reference_oracle(T, E, pi, tokens32) -> dict` - C0: the ordered float64 reference filter and predictive (certificate only).
- **function `_digest`** [L87-89]: `def _digest(a) -> str`
- **function `p0`** [L92-115]: `def p0(T, E_list, pi) -> dict` - P0 in exact rationals (§15.3.3); not ok -> FAIL_TECHNICAL/IDENTITY.
- **function `p1`** [L118-120]: `def p1(nu_min, finite, nu0) -> np.ndarray`
- **function `discrepancy`** [L123-128]: `def discrepancy(q_hat, q_ref) -> list`
- **function `rho_main`** [L131-135]: `def rho_main(r_h, rho_bar) -> Fraction`
- **function `route_f`** [L138-155]: `def route_f(T, E, pi, tokens32, q_hat) -> list` - §15.3.7 steps 1-4 per history; x > 1/2 -> ok False (FAIL_TECHNICAL/ORACLE, P4).
- **function `measured_log_error`** [L158-173]: `def measured_log_error(q_hat, l_hat) -> list` - M-ln: e_bar per row from correctly rounded 40-digit Decimal ln (§15.3.6).
- **function `_finite_le`** [L176-183]: `def _finite_le(arrays, limit, strict_positive=False) -> bool`
- **function `p2_leaves`** [L186-189]: `def p2_leaves(logits=(), q=(), l=(), scores=(), e_l=(), leaves=()) -> bool`
- **function `a1_selftest`** [L192-217]: `def a1_selftest() -> dict` - The fixed A1 vectors of CERTIFICATE.md §3 (numpy float64 and Python floats).

