# `tests/c1prime/test_b_cert_oracle.py`

- Source: [tests/c1prime/test_b_cert_oracle.py](../../../../../tests/c1prime/test_b_cert_oracle.py)
- Kind: python
- Lines: 379

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-4 items 1-3, 6, 12, 13 (oracle side).

## Imports

### Internal (repo files)

- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 26, via package root)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../../tools/c1prime/c1_cert.py.md) (line 34, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 35, via sys.path edit)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 36, via sys.path edit)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 37, via sys.path edit)

### External (third-party)

- `numpy` (lines 24)
- `pytest` (lines 25)

### Standard library

- `__future__` (lines 15)
- `decimal` (lines 17, 20)
- `fractions` (lines 21)
- `math` (lines 18)
- `pathlib` (lines 22)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 32: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `TWO_M1000`
- `U`
- `U1`

## Classes and functions

- **function `_ring`** [L46-52]: `def _ring(N, stay=0.5)`
- **function `_hmm`** [L55-60]: `def _hmm(N, V, kind, seed)`
- **function `_support`** [L63-65]: `def _support(T) -> int`
- **function `_c0`** [L68-108]: `def _c0(T, E, pi, tok, include_zeros=False)` - The C0 expressions of §15.3.2 in Python floats (IEEE binary64, no FMA).
- **function `_exact`** [L111-124]: `def _exact(T, E, pi, row)` - Exact b*_32 and literal q* = b*_32 T E (stored weights read as exact rationals).
- **function `_mag`** [L127-133]: `def _mag(approx, exact) -> Fraction` - A rational upper bound of max |log(approx/exact)|: log r <= r - 1, -log r <= 1/r - 1.
- **function `_up`** [L136-138]: `def _up(c: Fraction) -> float`
- **test `test_reference_oracle_is_C0_bitwise_and_obeys_theorem1`** [L146-162]: `def test_reference_oracle_is_C0_bitwise_and_obeys_theorem1(N, V, kind, seed)` decorators: @pytest.mark.parametrize('N,V,kind,seed', [(4, 3, 'ring', 1), (7, 4, 'dense', 2), (12, 5, 'ring', 3), (12, 3, 'dense', 4)])
- **test `test_skipping_zero_transition_entries_is_bitwise_neutral`** [L165-171]: `def test_skipping_zero_transition_entries_is_bitwise_neutral()`
- **test `test_rho_bar_ref_constants`** [L174-177]: `def test_rho_bar_ref_constants()`
- **test `test_measured_discrepancy_contains_the_exact_error`** [L183-196]: `def test_measured_discrepancy_contains_the_exact_error()`
- **test `test_p4_boundary_and_a_discrepancy_above_one_half`** [L199-215]: `def test_p4_boundary_and_a_discrepancy_above_one_half()`
- **function `_route_f_hmm`** [L221-223]: `def _route_f_hmm()`
- **function `_my_route_f_r`** [L226-233]: `def _my_route_f_r(T, E, pi, h, q_hat) -> Fraction`
- **function `_frac`** [L236-237]: `def _frac(x) -> Fraction`
- **test `test_route_f_is_taken_when_p1_fails_and_bounds_the_exact_error`** [L240-256]: `def test_route_f_is_taken_when_p1_fails_and_bounds_the_exact_error()`
- **test `test_route_f_rejects_x_above_one_half`** [L259-267]: `def test_route_f_rejects_x_above_one_half()`
- **test `test_p1_is_an_exact_rational_threshold`** [L270-274]: `def test_p1_is_an_exact_rational_threshold()`
- **function `_mln`** [L280-289]: `def _mln(q, ell)`
- **test `test_measured_log_error_matches_forty_digit_ln_and_grows_with_injected_error`** [L292-304]: `def test_measured_log_error_matches_forty_digit_ln_and_grows_with_injected_error()`
- **test `test_decimal_trap_in_m_ln_is_fail_technical_numerical`** [L307-312]: `def test_decimal_trap_in_m_ln_is_fail_technical_numerical()`
- **function `_cylinder`** [L318-330]: `def _cylinder()`
- **test `test_p0_constants_in_exact_rationals`** [L333-345]: `def test_p0_constants_in_exact_rationals()`
- **function `_edit`** [L348-351]: `def _edit(arr, index, value)`
- **test `test_p0_failures`** [L356-374]: `def test_p0_failures(case)` decorators: @pytest.mark.parametrize('case', ['not_identical', 'E_zero', 'T_zero_diag', 'pi_zero', 'T_negative', 'E_below_floor', 'E_tiny_ok'])
- **test `test_a1_selftest_holds_on_this_platform`** [L377-379]: `def test_a1_selftest_holds_on_this_platform()`

