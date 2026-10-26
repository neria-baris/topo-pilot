# `tests/c2_readout/test_a_partition.py`

- Source: [tests/c2_readout/test_a_partition.py](../../../../../tests/c2_readout/test_a_partition.py)
- Kind: python
- Lines: 347

## Module docstring

> Independent tests, author A (job 0101): T-PARTITION, T-RANDOM, T-ENERGY, T-HEADKERNEL and the
> c2_attrib part of T-BOOT (the C2-M descriptive stream, NEW-5; the indicator form) (C2-FROZEN-v1
> 2.6, 2.8-2.10, 2.12, 6.1, 13.3). The rest of T-BOOT is in test_a_inference.py.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 30, via sys.path edit)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../../tools/c1prime/c1_endpoint.py.md) (line 31, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 32, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 33, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 34, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 35, via sys.path edit)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 17)
- `fractions` (lines 21)
- `math` (lines 19)
- `pathlib` (lines 22)
- `sys` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `QCODE`
- `REPO`
- `VALUES`

## Classes and functions

- **function `_C`** [L46-47]: `def _C(v)`
- **function `_half`** [L50-51]: `def _half(d, v)`
- **function `_geometry`** [L54-61]: `def _geometry(n=40, p=12, seed=1)`
- **function `_stats`** [L64-71]: `def _stats(d, M, dy, P_S, P_G, G, Sigma)`
- **function `_b`** [L74-77]: `def _b(stats, model=1729, draws=2000)`
- **test `test_partition_sums_exactly_and_matches_closed_forms`** [L81-90]: `def test_partition_sums_exactly_and_matches_closed_forms()`
- **test `test_lemma_d1_interventional_identity_and_source_independence`** [L93-108]: `def test_lemma_d1_interventional_identity_and_source_independence()`
- **test `test_lemma_d2_logit_and_log_softmax_forms_agree_when_sum_d_is_zero`** [L111-117]: `def test_lemma_d2_logit_and_log_softmax_forms_agree_when_sum_d_is_zero()`
- **function `_null_fixture`** [L120-125]: `def _null_fixture()`
- **test `test_null_projector_is_the_orthogonal_projector_onto_ker_CM`** [L128-136]: `def test_null_projector_is_the_orthogonal_projector_onto_ker_CM()`
- **test `test_operator_decomposition_sums_and_converts_null_source_variation`** [L139-163]: `def test_operator_decomposition_sums_and_converts_null_source_variation()`
- **test `test_random_subspace_constants_exact`** [L167-175]: `def test_random_subspace_constants_exact()`
- **test `test_rs1_rs2_monte_carlo_against_random_ref`** [L178-204]: `def test_rs1_rs2_monte_carlo_against_random_ref()`
- **test `test_energies_match_definitions_and_isotropic_ratio_is_one_tenth`** [L208-217]: `def test_energies_match_definitions_and_isotropic_ratio_is_one_tenth()`
- **function `_cfix`** [L220-228]: `def _cfix(n=2000, s=1.0, oblique=True)` - Centred-logit fixture: d = (e0 - e1)/2, M columns e0-e1, e2-e3, e4-e5, e6-e7 (p = 4).
- **test `test_cancellation_fixture_energy_blocks_not_used`** [L231-236]: `def test_cancellation_fixture_energy_blocks_not_used()`
- **test `test_orthogonal_movement_fixture_gives_zero_share_low_aligned`** [L239-243]: `def test_orthogonal_movement_fixture_gives_zero_share_low_aligned()`
- **test `test_cauchy_schwarz_bound_holds_and_matches_its_formula`** [L246-255]: `def test_cauchy_schwarz_bound_holds_and_matches_its_formula()`
- **test `test_opposition_fixture_rc4_not_used_with_negative_qualifier_and_licence`** [L258-274]: `def test_opposition_fixture_rc4_not_used_with_negative_qualifier_and_licence()`
- **test `test_circle_code_in_the_head_kernel_is_a_valid_not_used`** [L278-305]: `def test_circle_code_in_the_head_kernel_is_a_valid_not_used()`
- **test `test_cm_descriptive_stream_24_arrays_shared_indices_and_undefined`** [L309-336]: `def test_cm_descriptive_stream_24_arrays_shared_indices_and_undefined()`
- **test `test_indicator_form_sign_and_eligible_row_ratio`** [L339-347]: `def test_indicator_form_sign_and_eligible_row_ratio()`

