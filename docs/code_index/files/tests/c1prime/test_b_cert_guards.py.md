# `tests/c1prime/test_b_cert_guards.py`

- Source: [tests/c1prime/test_b_cert_guards.py](../../../../../tests/c1prime/test_b_cert_guards.py)
- Kind: python
- Lines: 212

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-4 items 10, 11 and 13 (plus OUT and osum).

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../../tools/c1prime/c1_bounds.py.md) (line 35, via sys.path edit)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../../tools/c1prime/c1_cert.py.md) (line 36, via sys.path edit)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 15)
- `ast` (lines 17)
- `fractions` (lines 23)
- `importlib` (lines 18)
- `inspect` (lines 19)
- `math` (lines 20)
- `pathlib` (lines 24)
- `sys` (lines 21)
- `textwrap` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 211: `dynamic: module`

### sys.path additions

- line 33: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `FORBIDDEN`
- `KERNELS`
- `MODELS`
- `NUM`
- `REPO`
- `U`
- `U1`
- `ZETA`

## Classes and functions

- **function `_status`** [L47-48]: `def _status(res) -> str`
- **function `_gamma`** [L51-52]: `def _gamma(n) -> Fraction`
- **function `_out`** [L55-56]: `def _out(x) -> Fraction`
- **test `test_exact_constants`** [L62-72]: `def test_exact_constants()`
- **test `test_up_is_the_smallest_float_not_below_c`** [L78-82]: `def test_up_is_the_smallest_float_not_below_c(c)` decorators: @pytest.mark.parametrize('c', [Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), U1, _gamma(36), Fraction(1, 10), Fraction(3, 10), ZETA, 1 / (1 - U), Fraction(10 ** 20 + 1), Fraction(1, 10 ** 300)])
- **test `test_up_of_floats_and_bound_constants`** [L85-88]: `def test_up_of_floats_and_bound_constants()`
- **test `test_OUT_is_exact`** [L91-93]: `def test_OUT_is_exact()`
- **test `test_osum_is_left_to_right`** [L96-101]: `def test_osum_is_left_to_right()`
- **test `test_B_constant_uses_tree_depth_plus_one`** [L109-111]: `def test_B_constant_uses_tree_depth_plus_one(n, depth)` decorators: @pytest.mark.parametrize('n,depth', [(1, 0), (2, 1), (3, 2), (4096, 12), (4097, 13), (16384, 14), (20480, 15)])
- **function `_endpoint`** [L117-118]: `def _endpoint(L, U_, B)`
- **function `_models`** [L121-122]: `def _models(*values)`
- **test `test_endpoint_guard_far_from_zero_passes_with_either_sign`** [L125-127]: `def test_endpoint_guard_far_from_zero_passes_with_either_sign()`
- **test `test_endpoint_guard_floor_is_exactly_ten_to_minus_nine`** [L130-136]: `def test_endpoint_guard_floor_is_exactly_ten_to_minus_nine()`
- **test `test_endpoint_guard_binding_B_and_equality`** [L139-144]: `def test_endpoint_guard_binding_B_and_equality()`
- **test `test_h5_guard`** [L157-158]: `def test_h5_guard(lower, B_H, expected)` decorators: @pytest.mark.parametrize('lower,B_H,expected', [(0.5, Fraction(1, 10 ** 12), 'PASS'), (0.5, Fraction(0.5) - Fraction(1, 100), NUM), (0.5, Fraction(0.5) - Fraction(1, 100) - Fraction(1, 10 ** 40), 'PASS'), (0.005, Fraction(1, 100) - Fraction(0.005), 'INCONCLUSIVE/HEADROOM'), (0.005, Fraction(1, 100) - Fraction(0.005) + Fraction(1, 10 ** 40), NUM), (0.01, Fraction(0), NUM), (0.01 + 2e-09, Fraction(0), 'PASS'), (0.01 - 2e-09, Fraction(0), 'INCONCLUSIVE/HEADROOM')])
- **test `test_v3_guard`** [L170-171]: `def test_v3_guard(L, B, expected)` decorators: @pytest.mark.parametrize('L,B,expected', [([0.3, 0.2, 0.1], [Fraction(1, 10 ** 12)] * 3, 'PASS'), ([0.3, -0.2, 0.1], [Fraction(1, 10 ** 12)] * 3, 'INCONCLUSIVE/MODEL_HEADROOM'), ([0.3, 5e-10, 0.1], [Fraction(0)] * 3, NUM), ([0.3, 5e-10, -0.1], [Fraction(0)] * 3, 'INCONCLUSIVE/MODEL_HEADROOM'), ([0.25, 0.3, 0.3], [Fraction(0.25), Fraction(0), Fraction(0)], NUM), ([-0.25, 0.3, 0.3], [Fraction(0.25), Fraction(0), Fraction(0)], 'INCONCLUSIVE/MODEL_HEADROOM')])
- **function `_violations`** [L188-206]: `def _violations(func) -> list`
- **test `test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction`** [L210-212]: `def test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction(module, name)` decorators: @pytest.mark.parametrize('module,name', KERNELS)

