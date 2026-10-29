# `tests/hwsc/test_a_k4b_known_bound.py`

- Source: [tests/hwsc/test_a_k4b_known_bound.py](../../../../../tests/hwsc/test_a_k4b_known_bound.py)
- Kind: python
- Lines: 398

## Module docstring

> Author A (job 0176): KC8, K4b's own known cases at the bound constants.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 30, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 31, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 32, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 33, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 34, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 35, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 36, via unique basename)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 11)
- `decimal` (lines 18)
- `fractions` (lines 19)
- `hashlib` (lines 13)
- `itertools` (lines 14)
- `json` (lines 15)
- `math` (lines 16)
- `pathlib` (lines 20)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `C3`
- `D80`
- `E3`
- `K4B_MODELS`
- `LN_CASES`
- `M`
- `PI3`
- `REPO`
- `R_ROWS`
- `S3`
- `SEEDS_C`
- `STAGE_C`
- `SUP`
- `T3`
- `U_SUP`
- `_HWSC`

## Classes and functions

- **function `bound`** [L47-53]: `def bound()` decorators: @pytest.fixture
- **function `stationary`** [L66-77]: `def stationary(T)`
- **function `filt`** [L83-89]: `def filt(obs)` - Forward filter restarted at pi: (P(obs), posterior mean of c(z_last)).
- **function `enumerate_r`** [L92-98]: `def enumerate_r(L, K)`
- **test `test_stationary_law`** [L101-104]: `def test_stationary_law(bound)`
- **test `test_proposition1_suffix_only_zero`** [L108-126]: `def test_proposition1_suffix_only_zero(bound, L, K)` decorators: @pytest.mark.parametrize('L, K', [(6, 1), (6, 2), (6, 4), (5, 4)])
- **function `qsqrt`** [L137-140]: `def qsqrt(x)`
- **function `norm`** [L143-144]: `def norm(r)`
- **function `dot`** [L147-148]: `def dot(u, r)`
- **function `endpoints`** [L151-155]: `def endpoints()`
- **test `test_theorem_a_every_completion_in_bracket`** [L158-176]: `def test_theorem_a_every_completion_in_bracket(bound)`
- **test `test_theorem_a_no_gaps_rotation_path`** [L179-198]: `def test_theorem_a_no_gaps_rotation_path(bound)`
- **test `test_endpoint_arrays_match_exact`** [L201-211]: `def test_endpoint_arrays_match_exact(bound)`
- **test `test_isqrt_bracket_values`** [L219-220]: `def test_isqrt_bracket_values(bound, s, D, k)` decorators: @pytest.mark.parametrize('s, D, k', [(Fr(0), D80, 0), (Fr(1, 4), D80, D80 // 2), (Fr(2), 10, 14), (Fr(1, 10 ** 170), D80, 0), (Fr(9, 16), 10 ** 3, 750)])
- **test `test_isqrt_bracket_property`** [L224-226]: `def test_isqrt_bracket_property(bound, s)` decorators: @pytest.mark.parametrize('s', [Fr(1, 3), Fr(2), Fr(10 ** 6 + 1, 7), Fr(1, 10 ** 161), Fr(5, 4)])
- **function `ref_bn`** [L229-234]: `def ref_bn(n_hat, M32, M4, e4, e32)`
- **function `within`** [L237-239]: `def within(sq, lo, hi)` - lo <= sqrt(sq) <= hi, exactly (sq >= 0).
- **test `test_lemma_n_norm_bound`** [L254-261]: `def test_lemma_n_norm_bound(bound, n_hat, M32, M4)` decorators: @pytest.mark.parametrize('n_hat, M32, M4', LN_CASES)
- **test `test_lemma_n_zero_and_square_brackets`** [L264-269]: `def test_lemma_n_zero_and_square_brackets(bound)`
- **test `test_cap_and_margin`** [L274-279]: `def test_cap_and_margin(bound)`
- **test `test_f_plan_formula_and_dominance`** [L282-293]: `def test_f_plan_formula_and_dominance(bound)`
- **test `test_decision_boundaries`** [L298-324]: `def test_decision_boundaries(bound)`
- **test `test_ranks`** [L329-334]: `def test_ranks(bound)`
- **test `test_bounds_ranks_on_bound_endpoint_seed`** [L337-359]: `def test_bounds_ranks_on_bound_endpoint_seed(bound)`
- **test `test_write_sealed_stage_c_protocol`** [L364-381]: `def test_write_sealed_stage_c_protocol(bound, tmp_path)`
- **test `test_chart_equality_inside_binding`** [L384-387]: `def test_chart_equality_inside_binding(bound)`
- **test `test_binding_restored_after_exit`** [L390-398]: `def test_binding_restored_after_exit()`

