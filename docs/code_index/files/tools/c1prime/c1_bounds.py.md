# `tools/c1prime/c1_bounds.py`

- Source: [tools/c1prime/c1_bounds.py](../../../../../tools/c1prime/c1_bounds.py)
- Kind: python
- Lines: 197

## Module docstring

> C1' row bounds, certified constants and signed guards (API.md §7; CERTIFICATE.md §7-§8;
> protocol §15.3.8-15.3.11). Bounds use only binary + and * in the displayed shapes, on numpy
> arrays (float64, constants up(c)) or on Sym counting values (L5 counts).

## Imports

### Internal (repo files)

- `import c1_cert` -> [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 9, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)

### External (third-party)

- `numpy` (lines 150)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_cert_bounds.py](../../tests/c1prime/test_b_cert_bounds.py.md) (line 33, import)
- [tests/c1prime/test_b_cert_guards.py](../../tests/c1prime/test_b_cert_guards.py.md) (line 35, import)
- [tests/k4b/test_a_decision.py](../../tests/k4b/test_a_decision.py.md) (line 30, import)
- [tests/k4b/test_a_width_b4.py](../../tests/k4b/test_a_width_b4.py.md) (line 26, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 26, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 229, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 263, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 9, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 9, import)
- [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 10, import)
- [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 13, import)
- [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 26, import)

## Top-level constants

- `FLOOR`

## Classes and functions

- **function `bound_constants`** [L15-21]: `def bound_constants() -> dict`
- **function `_sum`** [L24-28]: `def _sum(terms)`
- **function `_rho_bar`** [L31-32]: `def _rho_bar(rho)`
- **function `_eps_d`** [L35-36]: `def _eps_d(d_v, qp_v, qm_v, rbp, rbm, c)`
- **function `b_G`** [L39-47]: `def b_G(d, lam, qp, qm, rho_p, rho_m, e_l, c)` - Theorem 2; d, lam are |d_v|, |lam_v| lists (length V).
- **function `b_A`** [L50-55]: `def b_A(d, Delta, qp, qm, rho_p, rho_m, max_abs_Delta, omega_TE, c)` - Theorem 3; d, Delta are |d_v|, |Delta_v| lists (length V).
- **function `b_Y`** [L58-61]: `def b_Y(Y, bA_T, bA_C_list, A_C_list, c)` - Theorem 4 (Y); Y and A_C entries are absolute values.
- **function `b_Z`** [L64-66]: `def b_Z(Z, bY, G, bG, c)`
- **function `b_Zf`** [L69-71]: `def b_Zf(Zf, bA_full, G, bG, c)`
- **function `B_constant`** [L74-76]: `def B_constant(max_b, max_abs, n) -> Fraction`
- **function `_F`** [L79-80]: `def _F(x) -> Fraction`
- **function `guard_endpoint`** [L83-90]: `def guard_endpoint(L, U, B) -> dict` - (E): per model F = max(B, 1e-9); |L| <= F or |U| <= F -> INCONCLUSIVE/NUMERICAL.
- **function `guard_H5`** [L93-97]: `def guard_H5(lower, B_H) -> str`
- **function `guard_V3`** [L100-106]: `def guard_V3(L_list, B_list) -> str`
- **class `Sym`** [L109-144] - Counting value for L5: nodes, formal monomials (with multiplicity) and degree.
- **method `Sym.__init__`** [L114-115]: `def __init__(self, nodes=0, monomials=1, degree=1)`
- **method `Sym.leaf`** [L118-119]: `def leaf(cls)` decorators: @classmethod
- **method `Sym._as`** [L122-123]: `def _as(x)` decorators: @staticmethod
- **method `Sym.__add__`** [L125-128]: `def __add__(self, other)`
- **method `Sym.__mul__`** [L132-135]: `def __mul__(self, other)`
- **method `Sym.leaves`** [L140-141]: `def leaves(self) -> int` decorators: @property
- **method `Sym.__repr__`** [L143-144]: `def __repr__(self)`
- **function `row_certificate`** [L147-197]: `def row_certificate(ctx, r, idx, batch=512) -> dict` - N0 / H3 row certificate for oracle rows idx of r (§15.3.6-15.3.8): C0 reference and P1

