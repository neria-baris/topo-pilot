# `tests/c2_nd/test_a_identity.py`

- Source: [tests/c2_nd/test_a_identity.py](../../../../../tests/c2_nd/test_a_identity.py)
- Kind: python
- Lines: 293

## Module docstring

> Author A (job 0121): T-N1, T-LNSCALE, T-LEAK and T-DOSE.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 21, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 24, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 25, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 26, via sys.path edit)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](../../tools/c2_nd/nd_decoy.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 12)
- `pathlib` (lines 13)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `REPO`
- `VARIANT_NAMES`

## Classes and functions

- **function `_centre`** [L33-34]: `def _centre(v)`
- **function `_frame`** [L37-50]: `def _frame(seed, n=256)` - Random readout M (8 x 31), oblique GLS projectors with a random SPD Sigma, two arms.
- **function `_half_dot`** [L53-54]: `def _half_dot(d, v)`
- **function `_row_ok`** [L57-58]: `def _row_ok(got, want, tol, scale)`
- **test `test_n1_subtraction_direct_arm_and_energies`** [L62-91]: `def test_n1_subtraction_direct_arm_and_energies()`
- **test `test_n1_comp_arm_is_reverse_interchange`** [L94-101]: `def test_n1_comp_arm_is_reverse_interchange()`
- **test `test_n1_shares_sum_to_one`** [L104-110]: `def test_n1_shares_sum_to_one()`
- **test `test_n1_stream_arrays_and_sign_flips`** [L113-160]: `def test_n1_stream_arrays_and_sign_flips()`
- **test `test_n1_mirrored_bounds_on_a_shared_stream`** [L163-174]: `def test_n1_mirrored_bounds_on_a_shared_stream()`
- **test `test_lnscale_split_is_exact`** [L178-197]: `def test_lnscale_split_is_exact()`
- **test `test_lnscale_sigma_formula`** [L200-206]: `def test_lnscale_sigma_formula()`
- **test `test_leak_equals_refit_code_share_of_dnull`** [L210-227]: `def test_leak_equals_refit_code_share_of_dnull()`
- **test `test_kappa_leak_and_canonical_angles`** [L230-251]: `def test_kappa_leak_and_canonical_angles()`
- **function `_psi_dose`** [L255-256]: `def _psi_dose(psi, rho)`
- **test `test_dose_exact_fractions`** [L259-270]: `def test_dose_exact_fractions()`
- **test `test_dose_head_edit_on_a_synthetic_readout`** [L273-293]: `def test_dose_head_edit_on_a_synthetic_readout()`

