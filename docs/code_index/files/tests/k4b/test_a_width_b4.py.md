# `tests/k4b/test_a_width_b4.py`

- Source: [tests/k4b/test_a_width_b4.py](../../../../../tests/k4b/test_a_width_b4.py)
- Kind: python
- Lines: 202

## Module docstring

> K4b author A, TEST_PLAN A12 (v2) and A13 (protocol §7.6, §5.5 item 4, §6 B4-VAL).

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../../tools/c1prime/c1_bounds.py.md) (line 26, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 27, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 28, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 29, via sys.path edit)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 13)
- `inspect` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `KEYS`
- `MODELS`
- `NDRAW`
- `REPO`
- `Z`

## Classes and functions

- **function `f_plan`** [L39-40]: `def f_plan()` decorators: @pytest.fixture(scope='module')
- **function `ref_width`** [L43-54]: `def ref_width(D_bar, e, F)`
- **function `wcounts`** [L57-58]: `def wcounts(res)`
- **function `endpoint_arrays`** [L61-72]: `def endpoint_arrays(seed, n=3072)` - Synthetic X-+ = C -+ D per model, with A, u.r and |r| drawn at random.
- **function `designed_e`** [L75-82]: `def designed_e()` - Columns as in the projection tests: fail set range(1000) for every model and side.
- **test `test_width_signature_never_takes_C_bar`** [L87-89]: `def test_width_signature_never_takes_C_bar()`
- **test `test_width_matches_reference`** [L92-96]: `def test_width_matches_reference(f_plan)`
- **test `test_width_at_zero_equals_registered_exclusion_projection`** [L99-104]: `def test_width_at_zero_equals_registered_exclusion_projection(f_plan)`
- **test `test_width_D_shift_on_designed_draws`** [L107-114]: `def test_width_D_shift_on_designed_draws(f_plan)` - Success draws have e+ + q+ + F = 0.0091 and e- + q- - F = -0.0091, so a shift by
- **test `test_width_monotone_in_D_bar`** [L117-126]: `def test_width_monotone_in_D_bar(f_plan)`
- **test `test_width_invariant_to_C_bar`** [L129-145]: `def test_width_invariant_to_C_bar(f_plan)`
- **function `_guard`** [L150-151]: `def _guard(r4n, Bn, seed, n)`
- **test `test_b4_guard_pass`** [L154-162]: `def test_b4_guard_pass()`
- **test `test_b4_guard_headroom`** [L165-168]: `def test_b4_guard_headroom()`
- **test `test_b4_guard_numerical_band`** [L171-176]: `def test_b4_guard_numerical_band()`
- **test `test_b4_guard_matches_reused_kernels`** [L180-191]: `def test_b4_guard_matches_reused_kernels(seed)` decorators: @pytest.mark.parametrize('seed', [610102, 610104])
- **test `test_fresh_b4_low_basis`** [L196-202]: `def test_fresh_b4_low_basis(value, Bn)` decorators: @pytest.mark.parametrize('value,Bn', [(0.0625, Fr(1, 10 ** 12)), (0.0078125, Fr(1, 10 ** 12)), (0.01, Fr(1, 10 ** 12)), (0.0625, Fr(1, 10))]) - FRESH_B4_LOW (implementation choice 7) is set iff the guard status is not PASS, i.e.

