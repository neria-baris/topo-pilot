# `tests/k4b/test_a_lemma_n.py`

- Source: [tests/k4b/test_a_lemma_n.py](../../../../../tests/k4b/test_a_lemma_n.py)
- Kind: python
- Lines: 269

## Module docstring

> K4b author A, TEST_PLAN A3, A5, A8 (protocol §5.2, §5.3; CERTIFICATE §1, §3).

## Imports

### Internal (repo files)

- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 27, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 28, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 29, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 8)
- `decimal` (lines 13)
- `fractions` (lines 14)
- `math` (lines 10)
- `pathlib` (lines 15)
- `random` (lines 11)
- `sys` (lines 12)

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

- `D80`
- `ONE_D`
- `REPO`
- `THREE_HALVES`

## Classes and functions

- **function `dec2`** [L36-37]: `def dec2(x, y)`
- **function `ref_k`** [L40-41]: `def ref_k(s, D=D80)`
- **function `ref_norm_bound`** [L44-48]: `def ref_norm_bound(n_hat, M32, M4, e4, e32)`
- **function `covers`** [L51-54]: `def covers(n, B, s_star)` - Exact test of |n - sqrt(s_star)| <= B by squares.
- **function `eps`** [L58-59]: `def eps()` decorators: @pytest.fixture(scope='module')
- **test `test_isqrt_zero`** [L64-66]: `def test_isqrt_zero()`
- **test `test_isqrt_perfect_squares_are_exact`** [L69-73]: `def test_isqrt_perfect_squares_are_exact()`
- **test `test_isqrt_sqrt2_digits_and_bracket`** [L76-81]: `def test_isqrt_sqrt2_digits_and_bracket()`
- **test `test_isqrt_tiny_values`** [L84-89]: `def test_isqrt_tiny_values()`
- **test `test_isqrt_bracket_property_random`** [L92-98]: `def test_isqrt_bracket_property_random()`
- **test `test_norm_bound_s_zero`** [L103-111]: `def test_norm_bound_s_zero(eps)`
- **test `test_norm_bound_exact_pythagorean`** [L114-122]: `def test_norm_bound_exact_pythagorean(eps)`
- **test `test_norm_bound_adversarial_n_hat`** [L126-131]: `def test_norm_bound_adversarial_n_hat(eps, n_hat)` decorators: @pytest.mark.parametrize('n_hat', [0.0, -0.5, 2.0, 1e+308, 5e-324, 0.49999999, 0.25])
- **test `test_norm_bound_irrational_norms`** [L135-145]: `def test_norm_bound_irrational_norms(eps, pair)` decorators: @pytest.mark.parametrize('pair', [('1', '1'), ('0.1', '0.1'), ('-0.7', '0.2'), ('1.3', '-0.9')])
- **test `test_norm_bound_tiny_values`** [L148-157]: `def test_norm_bound_tiny_values(eps)`
- **test `test_norm_bound_covers_perturbed_true_residual`** [L160-173]: `def test_norm_bound_covers_perturbed_true_residual()` - Lemma N soundness: every r* within eps4 + eps32 per coordinate of r~ is covered.
- **test `test_norm_bound_other_K_uses_its_envelope`** [L176-181]: `def test_norm_bound_other_K_uses_its_envelope(eps)`
- **test `test_envelopes_match_error_bound`** [L186-193]: `def test_envelopes_match_error_bound(eps)`
- **test `test_phase_bound_at_K_equals_row_bound`** [L197-206]: `def test_phase_bound_at_K_equals_row_bound(eps, K)` decorators: @pytest.mark.parametrize('K', [1, 2])
- **test `test_phase_bound_closed_form_at_phi_zero`** [L210-217]: `def test_phase_bound_closed_form_at_phi_zero(eps, K)` decorators: @pytest.mark.parametrize('K', [1, 2])
- **test `test_phase_bound_K1_K2_differ_by_envelopes`** [L220-225]: `def test_phase_bound_K1_K2_differ_by_envelopes(eps)`
- **test `test_phase_bound_detects_a_wrong_score`** [L228-232]: `def test_phase_bound_detects_a_wrong_score(eps)`
- **test `test_phase_bound_refuses_phase_outside_domain`** [L235-240]: `def test_phase_bound_refuses_phase_outside_domain(eps)`
- **test `test_cap_constant_and_boundary`** [L245-251]: `def test_cap_constant_and_boundary()`
- **test `test_cap_is_exact_not_float`** [L254-260]: `def test_cap_is_exact_not_float()`
- **test `test_p2_analogue`** [L263-269]: `def test_p2_analogue()`

