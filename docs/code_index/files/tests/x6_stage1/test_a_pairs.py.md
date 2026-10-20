# `tests/x6_stage1/test_a_pairs.py`

- Source: [tests/x6_stage1/test_a_pairs.py](../../../../../tests/x6_stage1/test_a_pairs.py)
- Kind: python
- Lines: 400

## Module docstring

> Author A: T-PAIR and T-BETA (X6S1-FROZEN-v1 §2.3, §10.2 T2-T5, T7, §14.3; API.md §4.2, §7).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 23, via sys.path edit)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../../tools/x6_stage1/x6s1_pairs.py.md) (line 24, via sys.path edit)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 25, via sys.path edit)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../../tools/x6_stage0/x6_exact.py.md) (line 29, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 30, via sys.path edit)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 6)
- `collections` (lines 12)
- `fractions` (lines 13)
- `functools` (lines 14)
- `hashlib` (lines 8)
- `math` (lines 9)
- `pathlib` (lines 15)
- `random` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`
- line 28: `str(REPO / 'tools' / 'x6_stage0')` -> `tools/x6_stage0`

## Imported by

- none

## Top-level constants

- `LETTERS`
- `REPO`

## Classes and functions

- **function `_bump`** [L39-46]: `def _bump(k, u, v, d=1)`
- **function `my_counts`** [L50-59]: `def my_counts(n_max: int) -> tuple` decorators: @lru_cache(maxsize=None)
- **function `enumerate_classes`** [L62-74]: `def enumerate_classes(n: int) -> dict` - Every anchor-avoiding n-step path from the anchor, grouped by (v_t, kappa).
- **function `my_preds`** [L77-86]: `def my_preds(counts, m, v, k)`
- **function `my_sample`** [L89-100]: `def my_sample(counts, v_t, kappa, n, rnd)` - §2.3 backward sampler: randrange(c_m) per step, cumulative weights in NEIGHBOURS order.
- **function `my_segment`** [L103-111]: `def my_segment(row, t)`
- **function `my_r_ord`** [L114-116]: `def my_r_ord(row, t) -> bool`
- **function `walks`** [L119-127]: `def walks(n_rows: int, seed: int) -> np.ndarray` - Synthetic positive-probability histories: random walk, a random cue at the anchor.
- **function `pool`** [L131-132]: `def pool()` decorators: @lru_cache(maxsize=None)
- **function `short_tables`** [L136-137]: `def short_tables()` decorators: @lru_cache(maxsize=None)
- **function `ord_rows`** [L140-141]: `def ord_rows(tokens, t)`
- **function `cue_frac`** [L144-146]: `def cue_frac(q)`
- **function `dot`** [L149-150]: `def dot(a, b)`
- **function `sub`** [L153-154]: `def sub(a, b)`
- **test `test_tables_equal_independent_dp_and_validate`** [L158-169]: `def test_tables_equal_independent_dp_and_validate()`
- **test `test_sampler_law_exhaustively_uniform_n_le_6`** [L172-181]: `def test_sampler_law_exhaustively_uniform_n_le_6()`
- **test `test_predecessors_sum_to_class_count`** [L184-191]: `def test_predecessors_sum_to_class_count()`
- **test `test_sample_segment_equals_independent_backward_sampler`** [L194-205]: `def test_sample_segment_equals_independent_backward_sampler()`
- **test `test_segment_parse_and_r_ord`** [L208-224]: `def test_segment_parse_and_r_ord()`
- **test `test_partner_seed_is_registered_stream`** [L227-230]: `def test_partner_seed_is_registered_stream()`
- **test `test_partner_key_probability_validity_and_determinism`** [L233-251]: `def test_partner_key_probability_validity_and_determinism()`
- **test `test_partners_batch_rows_and_padding`** [L254-263]: `def test_partners_batch_rows_and_padding()`
- **test `test_partner_full_tables_t32`** [L267-276]: `def test_partner_full_tables_t32()` decorators: @pytest.mark.slow
- **function `_law`** [L280-281]: `def _law(cue3, rest=0.0625)`
- **test `test_pair_terms_hand_values`** [L284-300]: `def test_pair_terms_hand_values()`
- **test `test_beta_fsum_and_exact_agree_t7`** [L303-312]: `def test_beta_fsum_and_exact_agree_t7()`
- **function `_parikh_function_law`** [L315-321]: `def _parikh_function_law(tokens, t)` - A synthetic predictor that is a function of the R_Parikh key only (Lemma P1).
- **test `test_lemma_p1_exact_zero_and_oracle_normalisation`** [L324-339]: `def test_lemma_p1_exact_zero_and_oracle_normalisation()`
- **test `test_q8_difference_on_r_ord_rows_t5`** [L342-347]: `def test_q8_difference_on_r_ord_rows_t5()`
- **function `_segment_only_f`** [L350-353]: `def _segment_only_f(seg)` - Any rational function of the segment tokens alone (no cue, no prefix).
- **test `test_lemma_p2_zero_in_expectation_over_uniform_y`** [L356-376]: `def test_lemma_p2_zero_in_expectation_over_uniform_y()`
- **test `test_lemma_p2_scope_prefix_cue_counterexample`** [L379-400]: `def test_lemma_p2_scope_prefix_cue_counterexample()` - L-E5: a predictor that combines the segment with a prefix cue is not covered by P2.

