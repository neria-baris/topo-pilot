# `tests/hwsd/test_a_statements.py`

- Source: [tests/hwsd/test_a_statements.py](../../../../../tests/hwsd/test_a_statements.py)
- Kind: python
- Lines: 235

## Module docstring

> Author A (job 0197): statements D1-D6 per model and the aggregate rule (§5.4, §5.5; DRD5).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 21, via sys.path edit)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](../../tools/hwsd/hwsd_statements.py.md) (line 22, via sys.path edit)
- `import test_a_hwsd_ref` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 24, via same directory)
- `from test_a_hwsd_ref import EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 25, via same directory)

### External (third-party)

- `pytest` (lines 23)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 12)
- `math` (lines 9)
- `pathlib` (lines 13)
- `random` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `BEF`
- `BYC`
- `HERE`
- `INIT`
- `M`
- `NE`
- `REPO`
- `TINF`
- `TUNI`

## Classes and functions

- **function `check`** [L32-37]: `def check(res, reading, reason=None, qualifier=None)`
- **function `agg`** [L40-45]: `def agg(statement, tables_by_model)`
- **test `test_d1_every_reading`** [L49-56]: `def test_d1_every_reading()`
- **test `test_d2_chart_at_init_evaluated_first`** [L60-63]: `def test_d2_chart_at_init_evaluated_first()`
- **test `test_d2_no_chart_false_and_final_not_support`** [L66-71]: `def test_d2_no_chart_false_and_final_not_support()`
- **test `test_d2_true_qualifier_uses_unvalidated_rows`** [L74-76]: `def test_d2_true_qualifier_uses_unvalidated_rows()`
- **test `test_d2_qualifier_boundary_exact`** [L79-85]: `def test_d2_qualifier_boundary_exact()`
- **test `test_d2_by_construction_and_unavailable_not_counted`** [L88-90]: `def test_d2_by_construction_and_unavailable_not_counted()`
- **test `test_d2_aggregate`** [L113-117]: `def test_d2_aggregate(tabs, expected)` decorators: @pytest.mark.parametrize('tabs,expected', [((BYC, BYC, BYC), (NE, {'BY_CONSTRUCTION': [J1, J2, J3]})), ((BYC, TINF, TINF), ('TRUE', {})), ((BYC, BYC, TINF), ('TRUE', {})), ((TINF, TUNI, BYC), ('TRUE', {})), ((TINF, TINF, TINF), ('TRUE', {})), ((TUNI, TUNI, BYC), (NE, {'UNINFORMATIVE_PRE_CHART': [J1, J2, J3]})), ((TUNI, TUNI, TUNI), (NE, {'UNINFORMATIVE_PRE_CHART': [J1, J2, J3]})), ((INIT, TINF, TINF), (NE, {'CHART_AT_INIT': [J1]})), ((INIT, BEF, TINF), ('FALSE', {})), ((BEF, BYC, BYC), ('FALSE', {}))])
- **test `test_d2_aggregate_mixed_not_evaluable_names_the_models`** [L120-123]: `def test_d2_aggregate_mixed_not_evaluable_names_the_models()`
- **test `test_d3_per_model_readings`** [L127-136]: `def test_d3_per_model_readings()`
- **test `test_d3_chart_at_init_rc4`** [L139-143]: `def test_d3_chart_at_init_rc4()`
- **test `test_d4_per_model_readings`** [L147-157]: `def test_d4_per_model_readings()`
- **test `test_d5_per_model_readings`** [L161-171]: `def test_d5_per_model_readings()`
- **test `test_d6_loss_on_ok_rows_only`** [L175-178]: `def test_d6_loss_on_ok_rows_only()`
- **test `test_d6_est_only_crossing_is_diagnostic_not_false`** [L181-185]: `def test_d6_est_only_crossing_is_diagnostic_not_false()`
- **test `test_d6_vacuous_and_true_needs_k1_below_K`** [L188-191]: `def test_d6_vacuous_and_true_needs_k1_below_K()`
- **test `test_aggregate_rule_generic`** [L195-201]: `def test_aggregate_rule_generic()`
- **test `test_reasons_are_contract_reasons`** [L204-215]: `def test_reasons_are_contract_reasons()`
- **test `test_random_tables_match_reference`** [L218-235]: `def test_random_tables_match_reference()`

