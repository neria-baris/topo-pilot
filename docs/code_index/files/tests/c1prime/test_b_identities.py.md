# `tests/c1prime/test_b_identities.py`

- Source: [tests/c1prime/test_b_identities.py](../../../../../tests/c1prime/test_b_identities.py)
- Kind: python
- Lines: 287

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-1: the A identities and kernels C4-C6.

## Imports

### Internal (repo files)

- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../../tools/c1prime/c1_endpoint.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 15)
- `decimal` (lines 18)
- `fractions` (lines 19)
- `pathlib` (lines 20)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `ROWS`
- `V`

## Classes and functions

- **function `_fr`** [L39-40]: `def _fr(x) -> Fraction`
- **function `_dec`** [L43-44]: `def _dec(x) -> Decimal`
- **function `_dyadic`** [L47-54]: `def _dyadic(seed, equal_mass=False)` - q = k/4096 and logits = j/64: every product and 36-term sum used below is exact.
- **function `_exact_logit_A`** [L57-59]: `def _exact_logit_A(qp, qm, zp, zm, i) -> Fraction`
- **function `_delta_m`** [L62-63]: `def _delta_m(qp, qm, i) -> Fraction`
- **function `_lse`** [L66-67]: `def _lse(row) -> Decimal`
- **function `_log_softmax`** [L70-77]: `def _log_softmax(z) -> np.ndarray`
- **function `_vec`** [L80-81]: `def _vec(x) -> np.ndarray`
- **test `test_logit_difference_form_is_the_exact_rational_on_dyadic_fixture`** [L87-92]: `def test_logit_difference_form_is_the_exact_rational_on_dyadic_fixture()`
- **test `test_symbol_constant_arm_difference_contributes_half_k_delta_m`** [L96-104]: `def test_symbol_constant_arm_difference_contributes_half_k_delta_m(k)` decorators: @pytest.mark.parametrize('k', [0.375, -2.5, 7.0])
- **test `test_symbol_constant_cancels_exactly_when_masses_are_equal`** [L107-112]: `def test_symbol_constant_cancels_exactly_when_masses_are_equal()`
- **test `test_arm_common_additive_perturbation_cancels_exactly`** [L115-119]: `def test_arm_common_additive_perturbation_cancels_exactly()`
- **test `test_common_inverse_temperature_scales_the_logit_form_exactly`** [L123-129]: `def test_common_inverse_temperature_scales_the_logit_form_exactly(beta)` decorators: @pytest.mark.parametrize('beta', [0.5, 0.75, 2.0])
- **test `test_logit_form_equals_log_softmax_form_exactly_when_sum_d_is_zero`** [L132-141]: `def test_logit_form_equals_log_softmax_form_exactly_when_sum_d_is_zero()`
- **test `test_equal_arms_give_exactly_zero`** [L144-150]: `def test_equal_arms_give_exactly_zero()`
- **function `_masses_fixture`** [L156-161]: `def _masses_fixture(seed, masses, rows=2)`
- **function `_G_dec`** [L164-166]: `def _G_dec(qp_row, qm_row) -> Decimal`
- **test `test_oracle_perfect_readout_gives_G_minus_mass_correction`** [L170-188]: `def test_oracle_perfect_readout_gives_G_minus_mass_correction(masses)` decorators: @pytest.mark.parametrize('masses', [(1.003, 0.998), (1.0, 1.0)])
- **test `test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term`** [L191-206]: `def test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term()`
- **test `test_common_inverse_temperature_identity_for_log_probabilities`** [L211-244]: `def test_common_inverse_temperature_identity_for_log_probabilities(beta, masses)` decorators: @pytest.mark.parametrize('beta,masses', [(0.6, (1.004, 0.997)), (1.7, (1.004, 0.997)), (0.6, (1.0, 1.0))])
- **function `_c5_c6`** [L250-256]: `def _c5_c6(A_T, A_C, G, A_full)`
- **test `test_Y_Z_Zfull_kernels_follow_C5_and_C6_bitwise`** [L259-267]: `def test_Y_Z_Zfull_kernels_follow_C5_and_C6_bitwise()`
- **test `test_frame_mean_is_an_ordered_left_to_right_sum`** [L270-275]: `def test_frame_mean_is_an_ordered_left_to_right_sum()`
- **test `test_zero_patch_contrast_and_scores`** [L278-287]: `def test_zero_patch_contrast_and_scores()`

