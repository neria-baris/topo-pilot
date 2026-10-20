# `tests/analysis/test_readout.py`

- Source: [tests/analysis/test_readout.py](../../../../../tests/analysis/test_readout.py)
- Kind: python
- Lines: 382

## Module docstring

> Independent tests N14-N19 for the readout-geometry helpers (SPEC part (d), WX4).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import PointSet, ln_gauge_free, predictive_pointset, readout_projector, split_readout` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 12, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `hand_ln`** [L17-22]: `def hand_ln(Z, eps)` - Reference LayerNorm without affine part (population variance).
- **function `unit_var_rows`** [L25-30]: `def unit_var_rows(M, d, seed)` - Random rows rescaled so that each row has population variance exactly 1.
- **function `build_A`** [L33-34]: `def build_A(gamma, W_U)`
- **function `is_projector`** [L37-38]: `def is_projector(P, tol=1e-10)`
- **function `expect_code`** [L41-44]: `def expect_code(code, fn, *args, **kwargs)`
- **test `test_N14_ln_gauge_free_affine_invariance`** [L51-58]: `def test_N14_ln_gauge_free_affine_invariance(alpha)` decorators: @pytest.mark.parametrize('alpha', [0.3, 1.0, 7.5])
- **test `test_N14_ln_gauge_free_shift_exact_with_eps`** [L61-68]: `def test_N14_ln_gauge_free_shift_exact_with_eps()`
- **test `test_N14_ln_gauge_free_scaling_with_eps_is_an_eps_rescaling`** [L72-77]: `def test_N14_ln_gauge_free_scaling_with_eps_is_an_eps_rescaling(alpha)` decorators: @pytest.mark.parametrize('alpha', [0.3, 1.0, 7.5])
- **test `test_N14_ln_gauge_free_not_scale_invariant_with_eps_at_small_variance`** [L80-83]: `def test_N14_ln_gauge_free_not_scale_invariant_with_eps_at_small_variance()`
- **test `test_N14_ln_gauge_free_rows_have_mean_zero_and_shape`** [L86-91]: `def test_N14_ln_gauge_free_rows_have_mean_zero_and_shape()`
- **test `test_N14_ln_gauge_free_hand_computed_row`** [L94-102]: `def test_N14_ln_gauge_free_hand_computed_row()`
- **test `test_N14_ln_gauge_free_matches_reference_and_accepts_float32`** [L105-110]: `def test_N14_ln_gauge_free_matches_reference_and_accepts_float32()`
- **function `_check_projector`** [L116-129]: `def _check_projector(gamma, W_U)`
- **test `test_N15_readout_projector_full_rank`** [L132-138]: `def test_N15_readout_projector_full_rank()`
- **test `test_N15_readout_projector_rank_deficient_duplicate_rows`** [L141-149]: `def test_N15_readout_projector_rank_deficient_duplicate_rows()`
- **test `test_N15_readout_projector_gamma_with_zeros`** [L152-161]: `def test_N15_readout_projector_gamma_with_zeros()`
- **test `test_N15_readout_projector_gamma_zeros_make_rank_drop`** [L164-172]: `def test_N15_readout_projector_gamma_zeros_make_rank_drop()`
- **test `test_N15_readout_projector_zero_A_gives_zero_P`** [L175-178]: `def test_N15_readout_projector_zero_A_gives_zero_P()`
- **test `test_N15_readout_projector_accepts_float32`** [L181-188]: `def test_N15_readout_projector_accepts_float32()`
- **function `_setup_split`** [L194-201]: `def _setup_split(seed=0, d=16, V=5, M=20)`
- **test `test_N16_split_readout_sums_and_orthogonality`** [L204-211]: `def test_N16_split_readout_sums_and_orthogonality()`
- **test `test_N16_split_readout_vector_already_visible_has_zero_null`** [L214-220]: `def test_N16_split_readout_vector_already_visible_has_zero_null()`
- **test `test_N16_split_readout_null_part_is_invisible`** [L223-226]: `def test_N16_split_readout_null_part_is_invisible()`
- **function `_tiny_model`** [L232-240]: `def _tiny_model(seed, d=16, V=5, M=30, zero_gamma_idx=())`
- **function `_logits`** [L243-244]: `def _logits(U, gamma, beta, W_U)`
- **test `test_N17_tiny_model_visible_part_reproduces_logits`** [L248-257]: `def test_N17_tiny_model_visible_part_reproduces_logits(zero_idx)` decorators: @pytest.mark.parametrize('zero_idx', [(), (2,), (0, 5, 9)])
- **test `test_N17_tiny_model_against_hand_layernorm`** [L260-265]: `def test_N17_tiny_model_against_hand_layernorm()`
- **function `hand_softmax`** [L271-274]: `def hand_softmax(L)`
- **test `test_N18_predictive_pointset_known_answer`** [L277-286]: `def test_N18_predictive_pointset_known_answer()`
- **test `test_N18_predictive_pointset_rows_sum_to_one_and_match_hand_softmax`** [L289-298]: `def test_N18_predictive_pointset_rows_sum_to_one_and_match_hand_softmax()`
- **test `test_N18_predictive_pointset_row_shift_invariant_and_stable`** [L301-310]: `def test_N18_predictive_pointset_row_shift_invariant_and_stable()`
- **test `test_N18_predictive_pointset_custom_space_and_float32`** [L313-318]: `def test_N18_predictive_pointset_custom_space_and_float32()`
- **test `test_N19_ln_gauge_free_errors`** [L324-334]: `def test_N19_ln_gauge_free_errors()`
- **test `test_N19_ln_gauge_free_zero_variance_row`** [L337-343]: `def test_N19_ln_gauge_free_zero_variance_row()`
- **test `test_N19_readout_projector_errors`** [L346-359]: `def test_N19_readout_projector_errors()`
- **test `test_N19_split_readout_errors`** [L362-369]: `def test_N19_split_readout_errors()`
- **test `test_N19_predictive_pointset_errors`** [L372-382]: `def test_N19_predictive_pointset_errors()`

