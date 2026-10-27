# `tests/hwsb/test_a_outcomes.py`

- Source: [tests/hwsb/test_a_outcomes.py](../../../../../tests/hwsb/test_a_outcomes.py)
- Kind: python
- Lines: 360

## Module docstring

> HWSB author A: outcomes, licences, HANDOFF blindness and B7 (protocol §5.1, §5.2, §6.1, RC-6;
> §4 B7; DRB11).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 28, via sys.path edit)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 29, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 10)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 25: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CLAUSES`
- `CONTRACT`
- `FORBIDDEN`
- `KEYS`
- `LIC`
- `MISSING`
- `NO_STATEMENT`
- `PASS_FILL`
- `REPO`

## Classes and functions

- **function `need`** [L59-61]: `def need()`
- **function `state`** [L64-70]: `def state(**kw)` - An all-PASS state (API §6.5 keys); keyword arguments override.
- **class `NA(dict)`** [L73-75]
- **method `NA.__missing__`** [L74-75]: `def __missing__(self, key)`
- **function `fill_ref`** [L78-82]: `def fill_ref(head, fill, oc, models_text=None)`
- **test `test_reference_contract_licences_carry_protocol_clauses`** [L87-96]: `def test_reference_contract_licences_carry_protocol_clauses()`
- **test `test_all_pass_is_hwsb_pass`** [L101-104]: `def test_all_pass_is_hwsb_pass()`
- **test `test_recorded_technical_failure_beats_everything`** [L112-120]: `def test_recorded_technical_failure_beats_everything(fail, expected)` decorators: @pytest.mark.parametrize('fail, expected', [('FAIL_TECHNICAL/NONFINITE', 'FAIL_TECHNICAL/NONFINITE'), ('LINEAGE', 'FAIL_TECHNICAL/LINEAGE'), ('FAIL_TECHNICAL/KNOWN_CASE', 'FAIL_TECHNICAL/KNOWN_CASE')])
- **test `test_b1_inconclusive_is_numerical_failure`** [L123-127]: `def test_b1_inconclusive_is_numerical_failure()`
- **test `test_b8a_and_b9a_failures_even_when_b1_fails`** [L130-142]: `def test_b8a_and_b9a_failures_even_when_b1_fails()`
- **test `test_incomplete_before_any_scientific_outcome`** [L145-151]: `def test_incomplete_before_any_scientific_outcome()`
- **test `test_not_learned_with_k`** [L156-161]: `def test_not_learned_with_k(b1, k)` decorators: @pytest.mark.parametrize('b1, k', [({A: 'FAIL', B: 'PASS'}, 1), ({A: 'PASS', B: 'FAIL'}, 1), ({A: 'FAIL', B: 'FAIL'}, 2)])
- **test `test_no_circle_with_criterion_and_models`** [L170-176]: `def test_no_circle_with_criterion_and_models(b4, outcome, models)` decorators: @pytest.mark.parametrize('b4, outcome, models', [({A: 'C0_CAL', B: 'PASS'}, 'HWSB_NO_CIRCLE/C0_CAL', [A]), ({A: 'PASS', B: 'C0_VAL'}, 'HWSB_NO_CIRCLE/C0_VAL', [B]), ({A: 'C0_VAL', B: 'C0_CAL'}, 'HWSB_NO_CIRCLE/C0_VAL', [A, B]), ({B: 'C0_CAL', A: 'C0_VAL'}, 'HWSB_NO_CIRCLE/C0_VAL', [A, B])])
- **test `test_underpowered_ladder_before_capture`** [L179-184]: `def test_underpowered_ladder_before_capture()`
- **test `test_underpowered_capture_and_annotation`** [L188-192]: `def test_underpowered_capture_and_annotation(positive)` decorators: @pytest.mark.parametrize('positive', [True, False])
- **test `test_pass_needs_every_gate`** [L195-201]: `def test_pass_needs_every_gate()`
- **test `test_unmatched_state_is_returned_not_raised`** [L204-207]: `def test_unmatched_state_is_returned_not_raised()`
- **test `test_licence_pass_filled`** [L215-223]: `def test_licence_pass_filled()`
- **test `test_licence_missing_field_is_na`** [L226-231]: `def test_licence_missing_field_is_na()`
- **test `test_licence_not_learned`** [L234-242]: `def test_licence_not_learned()`
- **test `test_licence_no_circle_uses_head_template`** [L245-256]: `def test_licence_no_circle_uses_head_template()`
- **test `test_licence_underpowered_with_annotation`** [L260-271]: `def test_licence_underpowered_with_annotation(positive)` decorators: @pytest.mark.parametrize('positive', [False, True])
- **test `test_licence_no_statement`** [L277-280]: `def test_licence_no_statement(outcome)` decorators: @pytest.mark.parametrize('outcome', ['FAIL_TECHNICAL/LAW_BOUND', 'FAIL_TECHNICAL/REGISTRY', 'FAIL_TECHNICAL/OUTCOME', 'FAIL_TECHNICAL/NUMERICAL', 'INCONCLUSIVE/RESOURCE_OR_AUTHORITY'])
- **test `test_licence_from_outcome_end_to_end`** [L283-287]: `def test_licence_from_outcome_end_to_end()`
- **function `full_fields`** [L292-293]: `def full_fields()`
- **test `test_check_handoff_accepts_clean_record`** [L296-301]: `def test_check_handoff_accepts_clean_record()`
- **test `test_check_handoff_refuses_forbidden_key_at_any_depth`** [L305-312]: `def test_check_handoff_refuses_forbidden_key_at_any_depth(key)` decorators: @pytest.mark.parametrize('key', FORBIDDEN)
- **test `test_check_handoff_refuses_extra_top_level_key`** [L315-319]: `def test_check_handoff_refuses_extra_top_level_key()`
- **test `test_handoff_record_keeps_exactly_the_contract_keys`** [L322-326]: `def test_handoff_record_keeps_exactly_the_contract_keys()`
- **test `test_handoff_record_refuses_missing_key_and_nested_forbidden`** [L329-337]: `def test_handoff_record_refuses_missing_key_and_nested_forbidden()`
- **test `test_b7_forecasts`** [L342-352]: `def test_b7_forecasts()`
- **test `test_b7_without_measurements_is_unavailable`** [L355-360]: `def test_b7_without_measurements_is_unavailable()`

