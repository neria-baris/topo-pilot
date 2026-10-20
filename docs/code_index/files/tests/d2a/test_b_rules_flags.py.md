# `tests/d2a/test_b_rules_flags.py`

- Source: [tests/d2a/test_b_rules_flags.py](../../../../../tests/d2a/test_b_rules_flags.py)
- Kind: python
- Lines: 292

## Module docstring

> Independent tests (author B, job 0028): T-RULES, the per-model and per-contrast flag functions
> of ``d2a_decide`` (learned, stage1_decision, arm_value, carries, low_increment, beta2_pass,
> precision_ok, c_hor, c_len, pipeline_null_ok).

## Imports

### Internal (repo files)

- `import d2a_decide` -> [tools/d2a/d2a_decide.py](../../tools/d2a/d2a_decide.py.md) (line 25, via sys.path edit)

### External (third-party)

- `pytest` (lines 18)

### Standard library

- `__future__` (lines 11)
- `itertools` (lines 13)
- `math` (lines 14)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO / _sub)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `EPS`
- `GAIN`
- `LOSS`
- `NAN`
- `NULL_KEYS`
- `PASS_ARGS`
- `REPO`

## Classes and functions

- **test `test_learned_pass_at_exact_boundaries`** [L34-36]: `def test_learned_pass_at_exact_boundaries()`
- **test `test_learned_defined_fail_on_any_single_condition`** [L47-50]: `def test_learned_defined_fail_on_any_single_condition(slot, value)` decorators: @pytest.mark.parametrize('slot, value', [(0, 0.3 - EPS), (1, 0.15 - EPS), (2, 0.2 - EPS), (3, 0.0), (3, -0.01), (0, -0.5)])
- **test `test_learned_undefined_statistic_is_unresolved_not_fail`** [L54-57]: `def test_learned_undefined_statistic_is_unresolved_not_fail(slot)` decorators: @pytest.mark.parametrize('slot', range(4))
- **test `test_learned_undefined_with_another_failing_condition_is_still_unresolved`** [L60-63]: `def test_learned_undefined_with_another_failing_condition_is_still_unresolved()`
- **test `test_learned_single_none_statistic_of_present_model_is_unresolved`** [L67-71]: `def test_learned_single_none_statistic_of_present_model_is_unresolved(slot)` decorators: @pytest.mark.parametrize('slot', range(4))
- **test `test_learned_four_none_is_unresolved_unless_model_status_says_missing_or_invalid`** [L74-79]: `def test_learned_four_none_is_unresolved_unless_model_status_says_missing_or_invalid()`
- **function `_ref_stage1`** [L84-89]: `def _ref_stage1(v1, v2)`
- **test `test_stage1_decision_all_branches`** [L94-95]: `def test_stage1_decision_all_branches(v1, v2)` decorators: @pytest.mark.parametrize('v1, v2', list(itertools.product(('PASS', 'FAIL', 'UNRESOLVED'), repeat=2)))
- **test `test_stage1_named_branches`** [L98-102]: `def test_stage1_named_branches()`
- **function `_ref_arm`** [L107-112]: `def _ref_arm(values)`
- **test `test_arm_value_exhaustive`** [L117-118]: `def test_arm_value_exhaustive(values)` decorators: @pytest.mark.parametrize('values', [list(v) for v in itertools.product(('PASS', 'FAIL', 'UNRESOLVED', None), repeat=4)])
- **test `test_arm_value_named_cases`** [L131-132]: `def test_arm_value_named_cases(values, expected)` decorators: @pytest.mark.parametrize('values, expected', [(['PASS', 'PASS', 'PASS', 'FAIL'], 'TRUE'), (['PASS', 'PASS', 'PASS', None], 'TRUE'), (['PASS', 'PASS', 'UNRESOLVED', 'FAIL'], 'UNRESOLVED'), (['PASS', 'PASS', 'UNRESOLVED', None], 'UNRESOLVED'), (['PASS', 'PASS', None, None], 'FALSE'), (['PASS', 'UNRESOLVED', None, None], 'FALSE'), (['UNRESOLVED'] * 4, 'UNRESOLVED'), ([None] * 4, 'FALSE')])
- **test `test_carries`** [L148-149]: `def test_carries(d, d_lo, expected)` decorators: @pytest.mark.parametrize('d, d_lo, expected', [(0.15, 0.05 + EPS, True), (0.15, 0.05, False), (0.15 - EPS, 0.1, False), (0.6, 0.4, True), (None, 0.1, False), (0.3, None, False), (None, None, False), (NAN, 0.1, False), (0.3, NAN, False)])
- **test `test_low_increment`** [L156-157]: `def test_low_increment(d, expected)` decorators: @pytest.mark.parametrize('d, expected', [(0.05 - EPS, True), (0.05, False), (0.0, True), (-0.3, True), (0.2, False), (None, False), (NAN, False)])
- **test `test_beta2_pass`** [L164-165]: `def test_beta2_pass(b, lo, expected)` decorators: @pytest.mark.parametrize('b, lo, expected', [(0.3, 0.15, True), (0.3 - EPS, 0.2, False), (0.4, 0.15 - EPS, False), (1.2, 0.9, True), (None, 0.2, False), (0.5, None, False), (NAN, 0.2, False)])
- **test `test_precision_ok`** [L183-184]: `def test_precision_ok(args, expected)` decorators: @pytest.mark.parametrize('args, expected', [((0.03, 0.03, 0.05, 0.05), True), ((0.01, 0.02, 0.04, 0.0), True), ((0.03 + EPS, 0.03, 0.05, 0.05), False), ((0.03, 0.03 + EPS, 0.05, 0.05), False), ((0.03, 0.03, 0.05 + EPS, 0.05), False), ((0.03, 0.03, 0.05, 0.05 + EPS), False), ((0.05, 0.03, 0.03, 0.03), False), ((0.03, 0.05, 0.03, 0.03), False), ((None, 0.01, 0.01, 0.01), False), ((0.01, 0.01, 0.01, None), False), ((0.01, NAN, 0.01, 0.01), False)])
- **test `test_c_hor`** [L204-205]: `def test_c_hor(mean, p2_5, per_seed, expected)` decorators: @pytest.mark.parametrize('mean, p2_5, per_seed, expected', [(0.1, 1e-12, [0.1, 0.1, 0.1, 0.1], 'SUPPORTED'), (0.1, 0.01, [0.15, 0.15, 0.1, -0.0], 'SUPPORTED'), (0.1 - EPS, 0.01, [0.1, 0.1, 0.1, 0.1], 'NOT_SUPPORTED'), (0.2, 0.0, [0.2, 0.2, 0.2, 0.2], 'NOT_SUPPORTED'), (0.1, 0.01, [0.2, 0.2, 0.0, 0.0], 'NOT_SUPPORTED'), (0.25, 0.05, [0.5, 0.5, -0.1, 0.0], 'NOT_SUPPORTED'), (None, 0.05, [0.2] * 4, 'UNRESOLVED'), (0.2, None, [0.2] * 4, 'UNRESOLVED'), (0.2, 0.05, None, 'UNRESOLVED'), (0.2, 0.05, [0.2, 0.2, 0.2, None], 'UNRESOLVED'), (0.2, 0.05, [0.2, 0.2, 0.2, NAN], 'UNRESOLVED'), (NAN, 0.05, [0.2] * 4, 'UNRESOLVED'), (0.2, NAN, [0.2] * 4, 'UNRESOLVED')])
- **test `test_c_len_gain_and_loss_at_boundaries`** [L214-216]: `def test_c_len_gain_and_loss_at_boundaries()`
- **test `test_c_len_not_detected`** [L228-229]: `def test_c_len_not_detected(args)` decorators: @pytest.mark.parametrize('args', [(0.1 - EPS, 0.01, 0.5, [0.1, 0.1, 0.1, 0.1]), (0.1, 0.0, 0.5, [0.1, 0.1, 0.1, 0.1]), (0.1, 0.01, 0.5, [0.2, 0.2, 0.0, 0.0]), (-0.1 + EPS, -0.5, -0.01, [-0.1] * 4), (-0.1, -0.5, 0.0, [-0.1] * 4), (-0.1, -0.5, -0.01, [-0.2, -0.2, 0.0, 0.0]), (0.0, -0.1, 0.1, [0.01, -0.01, 0.02, -0.02])])
- **test `test_c_len_precision_failure_overrides_every_result`** [L233-235]: `def test_c_len_precision_failure_overrides_every_result(base)` decorators: @pytest.mark.parametrize('base', [GAIN, LOSS, (0.0, -0.1, 0.1, [0.0] * 4)])
- **test `test_c_len_missing_input_is_unresolved`** [L239-242]: `def test_c_len_missing_input_is_unresolved(slot)` decorators: @pytest.mark.parametrize('slot', range(4))
- **test `test_c_len_missing_or_undefined_seed_is_unresolved`** [L245-247]: `def test_c_len_missing_or_undefined_seed_is_unresolved()`
- **test `test_c_len_nan_mean_or_interval_endpoint_is_unresolved`** [L252-256]: `def test_c_len_nan_mean_or_interval_endpoint_is_unresolved(base, slot)` decorators: @pytest.mark.parametrize('slot', range(3)) @pytest.mark.parametrize('base', [GAIN, LOSS])
- **function `_upper`** [L264-267]: `def _upper(value, changes=None)`
- **test `test_pipeline_null_passes_at_boundary`** [L270-272]: `def test_pipeline_null_passes_at_boundary()`
- **test `test_pipeline_null_any_single_check_fails`** [L277-279]: `def test_pipeline_null_any_single_check_fails(key, bad)` decorators: @pytest.mark.parametrize('key', NULL_KEYS) @pytest.mark.parametrize('bad', [0.02 + EPS, 0.5, None, NAN])
- **test `test_pipeline_null_needs_all_four_checks`** [L282-285]: `def test_pipeline_null_needs_all_four_checks()`
- **test `test_pipeline_null_mean_below_threshold_does_not_rescue`** [L288-292]: `def test_pipeline_null_mean_below_threshold_does_not_rescue()`

