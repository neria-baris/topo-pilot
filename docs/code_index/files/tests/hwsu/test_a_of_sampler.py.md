# `tests/hwsu/test_a_of_sampler.py`

- Source: [tests/hwsu/test_a_of_sampler.py](../../../../../tests/hwsu/test_a_of_sampler.py)
- Kind: python
- Lines: 275

## Module docstring

> Author A (job 0198): the exact conditional prefix sampler (protocol §2.1, Lemma P0, §5.1
> KS-PAIR; DRO2). Expected values are computed here, independently, by exact enumeration in
> Fractions on the CONTRACT_OF ``dry_run.ks_pair_chain`` (non-reversible, L = 8, suffix 4).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 15, via sys.path edit)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../../tools/hwsu/hwsu_pairs.py.md) (line 16, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 17, via unique basename)
- `from topo_pilot.dataset import sampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 20, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 9)
- `itertools` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `COND`
- `E_ZERO`
- `JOINT`
- `P`
- `PREFIXES`
- `P_S`
- `REPO`
- `SAMPLER`
- `SUFFIXES`

## Classes and functions

- **function `_chain`** [L27-33]: `def _chain()`
- **function `obj`** [L40-41]: `def obj(m)`
- **function `flt`** [L44-46]: `def flt(m)`
- **function `joint_law`** [L49-57]: `def joint_law(T, E, pi, length)` - P(w_1..w_length) for every word, exact forward recursion (no backward message).
- **function `implied_law`** [L67-80]: `def implied_law(bridge, T_rev, E)` - API §2.1: Σ_{z1..zP} bridge[zP] Π E[z_t, w'_t] Π_{t=2..P} T_rev[z_t, z_{t-1}].
- **function `my_beta`** [L83-95]: `def my_beta(s)` - β_P(z) = P(w_{P+1..L} = s | z_P = z), by direct enumeration of z_{P+1..L}.
- **function `my_time_reversal`** [L98-99]: `def my_time_reversal(T, pi)`
- **function `status_of_raise`** [L102-105]: `def status_of_raise(fn, *a, **k)`
- **test `test_time_reversal_exact_and_differs_from_T`** [L109-119]: `def test_time_reversal_exact_and_differs_from_T()`
- **test `test_check_process_accepts_chain_and_refuses_bad_pi`** [L122-130]: `def test_check_process_accepts_chain_and_refuses_bad_pi()`
- **test `test_backward_messages_and_bridge_exact`** [L134-141]: `def test_backward_messages_and_bridge_exact()`
- **test `test_implied_prefix_law_equals_bayes_conditional`** [L145-150]: `def test_implied_prefix_law_equals_bayes_conditional(s)` decorators: @pytest.mark.parametrize('s', SUFFIXES)
- **test `test_arm2_marginal_equals_process_law`** [L153-159]: `def test_arm2_marginal_equals_process_law()` - (c) Σ_s P(s)·P_impl(prefix | s) = P(w_1..w_8) for every word (Lemma P0 (i)).
- **test `test_planted_defective_samplers_are_caught`** [L162-172]: `def test_planted_defective_samplers_are_caught()` - (d) T in place of T~, and π in place of the bridge (β dropped): each fails (b).
- **test `test_sample_prefix_frequencies_within_4se`** [L176-194]: `def test_sample_prefix_frequencies_within_4se()`
- **function `_replay`** [L198-214]: `def _replay(T, E, pi, arm1, rng)` - API §2.2, step by step, with test-side float kernels.
- **test `test_draw_order_and_uniform_count`** [L217-228]: `def test_draw_order_and_uniform_count()`
- **test `test_rows_are_paired_by_index_not_sorted`** [L231-236]: `def test_rows_are_paired_by_index_not_sorted()`
- **test `test_zero_probability_column_never_drawn`** [L243-249]: `def test_zero_probability_column_never_drawn()`
- **test `test_bridge_refuses_impossible_suffix`** [L252-258]: `def test_bridge_refuses_impossible_suffix()`
- **test `test_suffix_equal_flags_a_changed_suffix_cell`** [L261-266]: `def test_suffix_equal_flags_a_changed_suffix_cell()`
- **test `test_float_kernels_match_exact_kernels`** [L269-275]: `def test_float_kernels_match_exact_kernels()`

