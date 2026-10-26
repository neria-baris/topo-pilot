# `tests/c2_readout/test_a_readout.py`

- Source: [tests/c2_readout/test_a_readout.py](../../../../../tests/c2_readout/test_a_readout.py)
- Kind: python
- Lines: 390

## Module docstring

> Independent tests, author A (job 0101): T-READOUT, T-ORDER and T-GLS part 1 (Lemmas G1-G3,
> the whitened-design fixtures, "B in the nuisance span"; G1 in the v2 whitened form, D-0104-2)
> (C2-FROZEN-v2 2.1, 2.3, 2.5, 13.3).
> T-GLS part 2 (GLS-REF) is in test_a_gls.py.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 27, via sys.path edit)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 28, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 29, via sys.path edit)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 30, via sys.path edit)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 31, via sys.path edit)
- `from topo_pilot.learner.config import ModelConfig` -> [src/topo_pilot/learner/config.py](../../src/topo_pilot/learner/config.py.md) (line 34, via package root)
- `from topo_pilot.learner.model import TransformerLM` -> [src/topo_pilot/learner/model.py](../../src/topo_pilot/learner/model.py.md) (line 35, via package root)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)
- `torch` (lines 32)

### Standard library

- `__future__` (lines 15)
- `pathlib` (lines 18)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `BOS`
- `DEG`
- `REPO`

## Classes and functions

- **function `_helmert_ref`** [L41-47]: `def _helmert_ref(n)`
- **function `_model`** [L50-60]: `def _model(gamma=None, seed=0)`
- **function `_ln`** [L63-67]: `def _ln(model, x)`
- **test `test_helmert_formula_orthonormal_and_orthogonal_to_ones`** [L71-77]: `def test_helmert_formula_orthonormal_and_orthogonal_to_ones()`
- **test `test_readout_basis_is_positive_diagonal_qr_of_diag_gamma_helmert`** [L80-98]: `def test_readout_basis_is_positive_diagonal_qr_of_diag_gamma_helmert()`
- **test `test_lemma_R_reconstruction_and_closed_logits`** [L101-121]: `def test_lemma_R_reconstruction_and_closed_logits()`
- **test `test_rank_rule_one_zero_gamma_keeps_rank_two_zeros_do_not`** [L125-131]: `def test_rank_rule_one_zero_gamma_keeps_rank_two_zeros_do_not(zeros, rank, ok)` decorators: @pytest.mark.parametrize('zeros, rank, ok', [((17,), 127, True), ((17, 90), 126, False)])
- **test `test_layernorm_eps_scale_not_removed_but_u_minus_beta_in_U0`** [L134-152]: `def test_layernorm_eps_scale_not_removed_but_u_minus_beta_in_U0()`
- **function `_perm`** [L156-160]: `def _perm()`
- **function `_perm_involutive`** [L163-166]: `def _perm_involutive()`
- **function `_scatter`** [L169-173]: `def _scatter(x, perm)`
- **function `_patch_inverse`** [L176-180]: `def _patch_inverse(monkeypatch)`
- **test `test_permutation_fixture_is_non_involutive`** [L183-188]: `def test_permutation_fixture_is_non_involutive()`
- **test `test_d_named_scatters_canonical_into_named_order`** [L191-194]: `def test_d_named_scatters_canonical_into_named_order()`
- **test `test_contraction_identity_and_the_wrong_conversion_differs`** [L197-205]: `def test_contraction_identity_and_the_wrong_conversion_differs()`
- **test `test_an_involutive_permutation_hides_the_direction_error`** [L208-212]: `def test_an_involutive_permutation_hides_the_direction_error()`
- **test `test_symbol_order_b_accepts_correct_map_rejects_inverse`** [L215-218]: `def test_symbol_order_b_accepts_correct_map_rejects_inverse(monkeypatch)`
- **test `test_symbol_order_a_accepts_correct_map_rejects_inverse`** [L221-228]: `def test_symbol_order_a_accepts_correct_map_rejects_inverse()`
- **test `test_symbol_order_c_accepts_correct_map_rejects_inverse`** [L231-236]: `def test_symbol_order_c_accepts_correct_map_rejects_inverse(monkeypatch)`
- **test `test_two_route_accepts_correct_map_rejects_inverse`** [L239-247]: `def test_two_route_accepts_correct_map_rejects_inverse()`
- **function `_seq`** [L250-254]: `def _seq(values)`
- **test `test_two_route_cancellation_and_zero_rows_new7`** [L257-280]: `def test_two_route_cancellation_and_zero_rows_new7()`
- **function `_problem`** [L283-288]: `def _problem(p=12, K=1, seed=0, spread=1.0)`
- **test `test_g1_identities_and_closed_form`** [L293-312]: `def test_g1_identities_and_closed_form(K)` decorators: @pytest.mark.parametrize('K', [1, 2, 3])
- **test `test_euclidean_variant_still_excludes_gamma`** [L315-324]: `def test_euclidean_variant_still_excludes_gamma()`
- **test `test_g2_interchange_takes_code_from_arm1_and_the_rest_from_arm2`** [L327-339]: `def test_g2_interchange_takes_code_from_arm1_and_the_rest_from_arm2()`
- **test `test_g3_monte_carlo_within_state_covariance_vanishes`** [L342-358]: `def test_g3_monte_carlo_within_state_covariance_vanishes()`
- **test `test_rank_deficient_nuisance_plus_code_block_is_degenerate`** [L362-367]: `def test_rank_deficient_nuisance_plus_code_block_is_degenerate()`
- **test `test_b_in_the_nuisance_span_is_degenerate`** [L370-374]: `def test_b_in_the_nuisance_span_is_degenerate()`
- **test `test_conditioning_above_1e8_with_a_well_conditioned_fwl_design`** [L377-390]: `def test_conditioning_above_1e8_with_a_well_conditioned_fwl_design()`

