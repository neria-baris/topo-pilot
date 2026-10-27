# `tests/c2_nd/test_a_decoy_maths.py`

- Source: [tests/c2_nd/test_a_decoy_maths.py](../../../../../tests/c2_nd/test_a_decoy_maths.py)
- Kind: python
- Lines: 310

## Module docstring

> Author A (job 0121): T-MOVE (Lemma DC4), T-GAIN (Lemma DG) and T-ILLUSION (MD-9).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 19, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 22, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 23, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 24, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 25, via sys.path edit)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](../../tools/c2_nd/nd_decoy.py.md) (line 26, via sys.path edit)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](../../tools/c2_nd/nd_driver.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `D_KEYS`
- `GAINS`
- `K0`
- `REPO`

## Classes and functions

- **function `_mx`** [L34-35]: `def _mx(x)`
- **function `_centre`** [L38-39]: `def _centre(v)`
- **function `_base`** [L42-50]: `def _base(seed)`
- **function `_dx_policy`** [L53-56]: `def _dx_policy()`
- **function `_bounds`** [L59-61]: `def _bounds(arrays, seed, alpha, j=1729, draws=2000)`
- **test `test_move_null_basis_and_move_map`** [L65-91]: `def test_move_null_basis_and_move_map()`
- **test `test_move_rank_deficient_is_construction`** [L94-104]: `def test_move_rank_deficient_is_construction()`
- **test `test_move_prediction_identities_and_adapter`** [L107-130]: `def test_move_prediction_identities_and_adapter()`
- **test `test_move_ols_gls_equivariance`** [L133-150]: `def test_move_ols_gls_equivariance()`
- **test `test_move_ledoit_wolf_equivariance`** [L153-163]: `def test_move_ledoit_wolf_equivariance()`
- **function `_gain_world`** [L171-192]: `def _gain_world(seed=811, n=512)`
- **function `_gain_run`** [L195-208]: `def _gain_run(w, Gx_mult, Gy_mult)` - D arrays, bounds and d_model at every gain; Y1' active iff V3y' passes (C2 y_active).
- **test `test_gain_scaling_of_arrays_and_bounds`** [L211-225]: `def test_gain_scaling_of_arrays_and_bounds()`
- **test `test_gain_decisions_do_not_depend_on_g`** [L228-246]: `def test_gain_decisions_do_not_depend_on_g()`
- **function `_illusion`** [L250-258]: `def _illusion(seed=901, n=256)`
- **test `test_illusion_operator_decomposition_is_report_only_arithmetic`** [L261-271]: `def test_illusion_operator_decomposition_is_report_only_arithmetic()`
- **test `test_illusion_decoy_built_with_J_fails_m0d_and_dx`** [L274-289]: `def test_illusion_decoy_built_with_J_fails_m0d_and_dx()`
- **test `test_illusion_euclidean_projector_decoy_still_has_null_code_readout`** [L292-310]: `def test_illusion_euclidean_projector_decoy_still_has_null_code_readout()`

