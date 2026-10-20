# `tests/x6_stage1/test_a_numerics.py`

- Source: [tests/x6_stage1/test_a_numerics.py](../../../../../tests/x6_stage1/test_a_numerics.py)
- Kind: python
- Lines: 374

## Module docstring

> Author A: T-LOGTAB, T-EB and T-STAT (X6S1-FROZEN-v1 §4.7, §7.3-§7.5, §10.2 T14-T16/T21/T27,
> §14.3; API.md §7 score/qstar, §8, §9 learned_*).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 23, via sys.path edit)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 24, via sys.path edit)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 25, via sys.path edit)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](../../tools/x6_stage1/x6s1_decide.py.md) (line 26, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 30, via sys.path edit)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 7)
- `decimal` (lines 12)
- `fractions` (lines 13)
- `functools` (lines 14)
- `itertools` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 15)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`
- line 29: `str(REPO / 'tools' / 'x6_stage0')` -> `tools/x6_stage0`

## Imported by

- none

## Top-level constants

- `CASES`
- `EPS`
- `G8_LO`
- `G8_S`
- `REPO`

## Classes and functions

- **function `D`** [L38-41]: `def D(fr, prec)`
- **function `ref_ln`** [L44-47]: `def ref_ln(x, prec=110)`
- **function `ref_xlnx`** [L50-53]: `def ref_xlnx(x, prec=140)`
- **function `my_qvals`** [L56-61]: `def my_qvals()`
- **function `nearest`** [L64-67]: `def nearest(f, ref)` - f is the float64 nearest to the Decimal ref (both neighbours are no closer).
- **test `test_qvals_independent_set`** [L71-72]: `def test_qvals_independent_set()`
- **test `test_table_entries_against_independent_decimal`** [L76-87]: `def test_table_entries_against_independent_decimal(kind)` decorators: @pytest.mark.parametrize('kind', ['ln', 'qlnq'])
- **function `small_tables`** [L91-92]: `def small_tables()` decorators: @lru_cache(maxsize=None)
- **test `test_log_tables_small_q_complete_and_correctly_rounded`** [L95-109]: `def test_log_tables_small_q_complete_and_correctly_rounded()`
- **test `test_score_e_row_check_against_80_digit_decimal`** [L112-133]: `def test_score_e_row_check_against_80_digit_decimal()` - §7.4 item 3 / T15: |x_hat - X| <= 1e-13 with X recomputed in 80-digit Decimal.
- **test `test_full_log_tables_spot_checks`** [L137-141]: `def test_full_log_tables_spot_checks()` decorators: @pytest.mark.slow
- **function `my_U`** [L145-154]: `def my_U(xbar, zbar, n, delta, B=17, prec=100)` - Theorem EB (§7.3), delta1 = delta2 = delta/2, plain high-precision evaluation.
- **test `test_eb_bound_outward_against_independent_decimal`** [L165-169]: `def test_eb_bound_outward_against_independent_decimal(xbar, zbar, n, delta)` decorators: @pytest.mark.parametrize('xbar,zbar,n,delta', CASES)
- **test `test_eb_constants_registered_table`** [L172-182]: `def test_eb_constants_registered_table()`
- **test `test_eb_monotone_in_xbar_and_zbar`** [L185-190]: `def test_eb_monotone_in_xbar_and_zbar()`
- **test `test_eb_exact_coverage_two_point_laws`** [L194-209]: `def test_eb_exact_coverage_two_point_laws(delta)` decorators: @pytest.mark.parametrize('delta', [Fraction(1, 10), Fraction(1, 160)]) - X in {0, B}: pair types (both 0, mixed, both B) are trinomial; P(mu <= U) >= 1 - delta.
- **test `test_outward_inputs_exact`** [L212-220]: `def test_outward_inputs_exact()`
- **test `test_eb_report_is_outward_bound_without_separation_term`** [L223-234]: `def test_eb_report_is_outward_bound_without_separation_term()`
- **function `full_row_law`** [L238-243]: `def full_row_law(N, inf)`
- **function `two_stage_by_hand`** [L246-255]: `def two_stage_by_hand(N, n_inf)`
- **test `test_two_stage_bootstrap_equals_full_row_multinomial`** [L258-268]: `def test_two_stage_bootstrap_equals_full_row_multinomial()`
- **test `test_cord_draws_replays_registered_scheme_and_common_indices`** [L271-285]: `def test_cord_draws_replays_registered_scheme_and_common_indices()`
- **test `test_ctrl_max_is_taken_inside_each_draw`** [L288-300]: `def test_ctrl_max_is_taken_inside_each_draw()`
- **test `test_boot_means_beta_and_stream`** [L303-321]: `def test_boot_means_beta_and_stream()`
- **test `test_quantile_wrapper_levels`** [L324-330]: `def test_quantile_wrapper_levels()`
- **test `test_tail_diagnostics_d1_d2`** [L333-350]: `def test_tail_diagnostics_d1_d2()`
- **test `test_gate_pass_fail_unresolved`** [L353-374]: `def test_gate_pass_fail_unresolved()`

