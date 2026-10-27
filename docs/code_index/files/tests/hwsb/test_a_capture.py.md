# `tests/hwsb/test_a_capture.py`

- Source: [tests/hwsb/test_a_capture.py](../../../../../tests/hwsb/test_a_capture.py)
- Kind: python
- Lines: 288

## Module docstring

> HWSB author A: B5 pilot capture at 80 % planned power (protocol §4 B5, refinement 1; DRB10).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 30, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 31, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 32, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 35, via sys.path edit)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 36, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 14)
- `math` (lines 12)
- `pathlib` (lines 15)
- `statistics` (lines 16)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 28: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `M`
- `MISSING`
- `MODELS`
- `REPO`
- `SEED`
- `Z_C`
- `Z_P`

## Classes and functions

- **function `need`** [L52-54]: `def need()`
- **function `F_plan`** [L57-58]: `def F_plan()`
- **function `sd_arg`** [L61-66]: `def sd_arg(values)` - API-AMBIGUITY: b5's sdU_minus may be keyed by j or by (j, "-") (the ladder's sdU keys);
- **function `mde_cfg`** [L69-70]: `def mde_cfg(F, N)`
- **function `b5_ref`** [L73-93]: `def b5_ref(X_minus, D4, sdU, N_C, F, models=MODELS, seed=SEED)`
- **function `assert_b5`** [L96-108]: `def assert_b5(res, ref)`
- **function `planted`** [L112-117]: `def planted()` decorators: @pytest.fixture(scope='module')
- **test `test_reference_z_values_match_contract_report_values`** [L122-126]: `def test_reference_z_values_match_contract_report_values()`
- **test `test_reference_ulp_construction_is_exact`** [L129-135]: `def test_reference_ulp_construction_is_exact()`
- **test `test_constants`** [L140-146]: `def test_constants()`
- **test `test_c_min_formula`** [L151-157]: `def test_c_min_formula(sd, N, D4hat)` decorators: @pytest.mark.parametrize('sd, N, D4hat', [(0.09, 3072, 0.047), (0.2, 6144, 0.031), (0.05, 12288, 0.12)])
- **test `test_c_min_expected_orientation`** [L160-166]: `def test_c_min_expected_orientation()`
- **test `test_c_min_literal_uses_z_one_minus_alpha_only_and_keeps_f_plan`** [L169-177]: `def test_c_min_literal_uses_z_one_minus_alpha_only_and_keeps_f_plan()`
- **test `test_capture_pass_equality_and_one_ulp_below`** [L180-185]: `def test_capture_pass_equality_and_one_ulp_below()`
- **test `test_b5_matches_reference`** [L190-194]: `def test_b5_matches_reference(planted)`
- **test `test_b5_default_seed_is_620214`** [L197-204]: `def test_b5_default_seed_is_620214(planted)`
- **test `test_b5_ulp_boundary_drb10`** [L207-223]: `def test_b5_ulp_boundary_drb10()`
- **test `test_b5_both_pass_status`** [L226-236]: `def test_b5_both_pass_status()`
- **test `test_b5_positive_below_planning_needs_every_model`** [L239-254]: `def test_b5_positive_below_planning_needs_every_model()`
- **test `test_b5_nonpositive_d4hat_is_numerical_failure`** [L258-264]: `def test_b5_nonpositive_d4hat_is_numerical_failure(planted, value)` decorators: @pytest.mark.parametrize('value', [0.0, -0.01])
- **test `test_b5_nonfinite_d4hat_is_numerical_failure`** [L267-274]: `def test_b5_nonfinite_d4hat_is_numerical_failure(planted)`
- **test `test_b5_fallback_n_enters_c_min`** [L277-288]: `def test_b5_fallback_n_enters_c_min(planted)`

