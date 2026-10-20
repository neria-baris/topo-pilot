# `tests/k4b/test_a_transport_bound.py`

- Source: [tests/k4b/test_a_transport_bound.py](../../../../../tests/k4b/test_a_transport_bound.py)
- Kind: python
- Lines: 150

## Module docstring

> K4b author A, correction round 2 (ruling R25): k4b_cert.transport_bound (API.md §7).

## Imports

### Internal (repo files)

- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 27, via sys.path edit)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 28, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 29, via sys.path edit)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](../../tools/x4_oracle_profile/inputs.py.md) (line 37, via sys.path edit) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 38, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 14)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `FLOOR`
- `GRID40`
- `REPO`

## Classes and functions

- **function `law_args`** [L36-47]: `def law_args()` decorators: @pytest.fixture(scope='module')
- **function `real`** [L51-54]: `def real(law_args)` decorators: @pytest.fixture(scope='module')
- **test `test_real_status_bounded_and_reused_keys_kept`** [L59-65]: `def test_real_status_bounded_and_reused_keys_kept(real)`
- **test `test_real_z_bound_is_exact_fraction_of_exact_upper`** [L68-74]: `def test_real_z_bound_is_exact_fraction_of_exact_upper(real)`
- **test `test_real_z_bound_sanity_band`** [L77-79]: `def test_real_z_bound_sanity_band(real)`
- **test `test_real_downstream_margin_and_f_plan`** [L82-89]: `def test_real_downstream_margin_and_f_plan(real)`
- **function `_dummy`** [L94-96]: `def _dummy()`
- **function `_patch`** [L99-108]: `def _patch(monkeypatch, report)`
- **function `_bounded`** [L111-113]: `def _bounded(exact)`
- **test `test_synthetic_exact_upper_gives_exact_fraction`** [L120-132]: `def test_synthetic_exact_upper_gives_exact_fraction(monkeypatch, exact, want)` decorators: @pytest.mark.parametrize('exact,want', [('3/7', Fraction(3, 7)), (f'{212 * 10 ** 26 + 1}/{GRID40}', Fraction(212 * 10 ** 26 + 1, GRID40))])
- **test `test_synthetic_non_bounded_raises_identity`** [L136-140]: `def test_synthetic_non_bounded_raises_identity(monkeypatch, status)` decorators: @pytest.mark.parametrize('status', ['UNAVAILABLE', 'bounded', 'INVALID'])
- **test `test_real_kernel_unavailable_raises_identity`** [L143-150]: `def test_real_kernel_unavailable_raises_identity()` - Unpatched: coords that are not the documented 12x12 lattice make the reused kernel

