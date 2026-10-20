# `tests/circle_history/test_error_bound.py`

- Source: [tests/circle_history/test_error_bound.py](../../../../../tests/circle_history/test_error_bound.py)
- Kind: python
- Lines: 398

## Module docstring

> Independent tests (author B) for error_bound.py: B6, B6b, B10 (spec v2.3, ERROR_BOUND v2.1).

## Imports

### Internal (repo files)

- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 26, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 27, via sys.path edit)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 28, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 29, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 9)
- `decimal` (lines 11, 14)
- `fractions` (lines 15)
- `math` (lines 12)
- `pathlib` (lines 16)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `A_COSH`
- `BAD_RELEASES`
- `COORDS`
- `E`
- `E_EXACT`
- `F`
- `HIST`
- `M32_ROW`
- `M4_ROW`
- `PHI`
- `PI`
- `PI_EXACT`
- `REPO_ROOT`
- `T`
- `TAYLOR_N`
- `T_EXACT`
- `XS`
- `X_MAX`
- `_CS`

## Classes and functions

- **function `_u`** [L40-41]: `def _u(n: int) -> Fraction`
- **function `_gamma`** [L44-45]: `def _gamma(k: int, n: int) -> Fraction`
- **function `_beta`** [L48-53]: `def _beta(L: int, S: int) -> Fraction`
- **function `_eps_m`** [L56-58]: `def _eps_m(beta: Fraction, S: int) -> Fraction`
- **function `_eps_v`** [L61-66]: `def _eps_v() -> Fraction`
- **function `_exact_cos_sin`** [L69-85]: `def _exact_cos_sin(x: Fraction, tail: Fraction) -> tuple[Fraction, Fraction]` - Exact rational Taylor partial sums. The loop stops at a term index n > 2|x| + 2 with
- **function `_sqrt3_half`** [L88-91]: `def _sqrt3_half(prec: int) -> Fraction`
- **test `test_u_and_gamma_digits_exact`** [L95-104]: `def test_u_and_gamma_digits_exact() -> None`
- **test `test_feature_posterior_and_moment_envelopes_match_formulas`** [L107-113]: `def test_feature_posterior_and_moment_envelopes_match_formulas() -> None`
- **test `test_trapping_context_settings`** [L117-137]: `def test_trapping_context_settings() -> None`
- **test `test_smallest_valid_forward_product_does_not_trap`** [L140-148]: `def test_smallest_valid_forward_product_does_not_trap() -> None` - Exponent reasoning of section 2: 64 factors of 2^-1074 stay far above 10^Emin.
- **test `test_exact_features_values`** [L157-169]: `def test_exact_features_values() -> None`
- **test `test_exact_features_rejects_bad_coordinates`** [L173-175]: `def test_exact_features_rejects_bad_coordinates(x: float) -> None` decorators: @pytest.mark.parametrize('x', [1.5, 12.0, -1.0, np.nan])
- **test `test_taylor_constants_and_exact_tail_inequalities`** [L179-189]: `def test_taylor_constants_and_exact_tail_inequalities() -> None`
- **test `test_decimal_cos_sin_against_exact_rational_taylor`** [L194-206]: `def test_decimal_cos_sin_against_exact_rational_taylor(x: float) -> None` decorators: @pytest.mark.parametrize('x', [0.0, 0.5, 1.0, math.pi / 2, 3.0, math.pi, 5.123456789, 6.28, 2 * math.pi])
- **test `test_decimal_cos_sin_rejects_outside_analytic_interval`** [L210-212]: `def test_decimal_cos_sin_rejects_outside_analytic_interval(x: float) -> None` decorators: @pytest.mark.parametrize('x', [-1e-12, -0.5, 6.2841, 7.0, math.nan, math.inf, -math.inf])
- **function `_row_reference`** [L220-224]: `def _row_reference(phi: float, eps4: Fraction, eps32: Fraction) -> tuple[Fraction, Fraction]`
- **test `test_row_bound_equals_independently_assembled_fractions`** [L227-243]: `def test_row_bound_equals_independently_assembled_fractions() -> None`
- **function `pipeline`** [L261-267]: `def pipeline()` decorators: @pytest.fixture(scope='module') - The production float pipeline: oracle_moments -> unit_vectors -> scores.
- **function `_ref_row`** [L270-279]: `def _ref_row(row: int, phi: float) -> tuple[Fraction, dict[int, list[Fraction]]]` - Independent reference score and moments for one row (Fractions).
- **function `_certify`** [L282-283]: `def _certify(m4, m32, x_hat, phi=PHI, split='calibration', **kw) -> dict`
- **test `test_pipeline_matches_independent_reference`** [L286-293]: `def test_pipeline_matches_independent_reference(pipeline) -> None`
- **test `test_certify_rows_certifies_exact_pipeline`** [L297-303]: `def test_certify_rows_certifies_exact_pipeline(pipeline, split: str) -> None` decorators: @pytest.mark.parametrize('split', ['calibration', 'validation'])
- **test `test_certify_rows_shifted_score_is_inconclusive`** [L306-317]: `def test_certify_rows_shifted_score_is_inconclusive(pipeline) -> None`
- **test `test_certify_rows_moment_shift_is_fail_technical`** [L321-327]: `def test_certify_rows_moment_shift_is_fail_technical(pipeline, which: str) -> None` decorators: @pytest.mark.parametrize('which', ['m4', 'm32'])
- **test `test_certify_rows_operational_range_and_nonfinite_fail_technical`** [L330-341]: `def test_certify_rows_operational_range_and_nonfinite_fail_technical(pipeline) -> None`
- **test `test_reference_check_rows_pass_and_fail`** [L345-357]: `def test_reference_check_rows_pass_and_fail(pipeline) -> None`
- **function `_auth`** [L361-364]: `def _auth(**changes) -> object`
- **test `test_scoring_lock_precedes_any_computation`** [L374-387]: `def test_scoring_lock_precedes_any_computation(kind: str) -> None` decorators: @pytest.mark.parametrize('kind', sorted(BAD_RELEASES))
- **test `test_scoring_authority_unlocks_scoring`** [L390-398]: `def test_scoring_authority_unlocks_scoring(pipeline) -> None`

