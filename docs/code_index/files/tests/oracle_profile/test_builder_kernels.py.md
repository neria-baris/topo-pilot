# `tests/oracle_profile/test_builder_kernels.py`

- Source: [tests/oracle_profile/test_builder_kernels.py](../../../../../tests/oracle_profile/test_builder_kernels.py)
- Kind: python
- Lines: 105

## Module docstring

> BUILDER tests (not independent): hardened kernel invariants from the pre-freeze review.

## Imports

### Internal (repo files)

- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 17, via sys.path edit)

### External (third-party)

- `numpy` (lines 12)
- `pytest` (lines 13)

### Standard library

- `__future__` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(Path(__file__).resolve().parents[2] / 'tools' / 'x4_oracle_profile')` -> `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `E`
- `PI`
- `T`
- `TOK`

## Classes and functions

- **test `test_valid_baseline`** [L25-27]: `def test_valid_baseline()`
- **test `test_kernel_rejects_invalid_model`** [L43-46]: `def test_kernel_rejects_invalid_model(bad)` decorators: @pytest.mark.parametrize('bad', [{'T': np.array([[np.nan, 1.0], [0.25, 0.75]])}, {'E': np.array([[np.inf, 0.1], [0.2, 0.8]])}, {'pi': np.array([-0.1, 1.1])}, {'T': np.eye(3)}, {'E': np.ones((3, 2)) / 2}, {'pi': [[0.5, 0.5]]}, {'T': [[0.5, 0.5], [0.25]]}, {'E': 'abc'}])
- **test `test_infinite_mass_rejected`** [L49-52]: `def test_infinite_mass_rejected()`
- **test `test_posterior_means_contract`** [L55-61]: `def test_posterior_means_contract()`
- **test `test_residual_rows_rejects_nonfinite_and_shape`** [L64-70]: `def test_residual_rows_rejects_nonfinite_and_shape()`
- **test `test_profile_point_and_bootstrap_error_paths`** [L73-88]: `def test_profile_point_and_bootstrap_error_paths()`
- **test `test_percentile_interval_rejects_bad_probs`** [L91-96]: `def test_percentile_interval_rejects_bad_probs()`
- **test `test_malformed_inputs_raise_profile_error`** [L99-105]: `def test_malformed_inputs_raise_profile_error()`

