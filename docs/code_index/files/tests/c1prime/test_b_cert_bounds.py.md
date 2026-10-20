# `tests/c1prime/test_b_cert_bounds.py`

- Source: [tests/c1prime/test_b_cert_bounds.py](../../../../../tests/c1prime/test_b_cert_bounds.py)
- Kind: python
- Lines: 297

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-4 items 4, 9 and 14 (row bounds).

## Imports

### Internal (repo files)

- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 25, via package root)
- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../../tools/c1prime/c1_bounds.py.md) (line 33, via sys.path edit)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../../tools/c1prime/c1_endpoint.py.md) (line 34, via sys.path edit)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 35, via sys.path edit)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 36, via sys.path edit)

### External (third-party)

- `numpy` (lines 23)
- `pytest` (lines 24)

### Standard library

- `__future__` (lines 14)
- `decimal` (lines 16, 19)
- `fractions` (lines 20)
- `math` (lines 17)
- `pathlib` (lines 21)
- `sys` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 31: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `U`
- `U1`
- `ZETA`

## Classes and functions

- **function `_up`** [L45-47]: `def _up(c: Fraction) -> float`
- **function `_out`** [L50-51]: `def _out(x) -> Fraction`
- **function `_ring`** [L54-58]: `def _ring(N)`
- **function `_q_ref`** [L61-79]: `def _q_ref(T, E, pi, tok)` - C0 (§15.3.2) in Python floats; returns q^ref [R, V] and min posterior per row.
- **function `sum_ordered`** [L82-86]: `def sum_ordered(xs)`
- **function `_exact_q`** [L89-100]: `def _exact_q(T, E, pi, row)`
- **function `_rho`** [L103-110]: `def _rho(q_hat, q_ref, N, d)` - up(rho_bar_ref + r_h/(1 - r_h)) per row (Theorem 1').
- **function `_e_l`** [L113-123]: `def _e_l(qp, qm, lp, lm)`
- **function `_cols`** [L126-127]: `def _cols(x)`
- **function `_ldec`** [L130-131]: `def _ldec(x: Fraction) -> Decimal`
- **test `test_theorem2_b_G_contains_the_exact_G_and_does_not_blow_up`** [L137-165]: `def test_theorem2_b_G_contains_the_exact_G_and_does_not_blow_up()`
- **test `test_theorem3_b_A_needs_and_is_saved_by_the_omega_term`** [L171-206]: `def test_theorem3_b_A_needs_and_is_saved_by_the_omega_term()`
- **function `_exact_consts`** [L212-218]: `def _exact_consts()`
- **function `_my_bA`** [L221-228]: `def _my_bA(d, Dl, qp, qm, rp, rm, mx, om, c)`
- **test `test_bound_values_follow_the_displayed_shapes_and_include_zeta`** [L231-261]: `def test_bound_values_follow_the_displayed_shapes_and_include_zeta()`
- **function `_leaves`** [L267-268]: `def _leaves(k)`
- **function `_sym_bA`** [L271-274]: `def _sym_bA(consts)`
- **function `_sym_bG`** [L277-280]: `def _sym_bG(consts)`
- **function `_within`** [L283-286]: `def _within(sym, nodes, monomials, degree)`
- **test `test_expression_counts_do_not_exceed_the_section_15_3_5_table`** [L289-297]: `def test_expression_counts_do_not_exceed_the_section_15_3_5_table()`

