# `tests/c1prime/test_a_gates.py`

- Source: [tests/c1prime/test_a_gates.py](../../../../../tests/c1prime/test_a_gates.py)
- Kind: python
- Lines: 223

## Module docstring

> Independent tests, author A (job 0026): the gate table, the computation-order rule and the
> stage machinery (TEST_PLAN A-6, first three bullets; protocol section 2.2, section 16 and
> section 18 field 2; API.md section 2 GATE_ORDER, LogitPolicy, PREREQUISITE, begin_stage).

## Imports

### Internal (repo files)

- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 24, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 25, via sys.path edit)

### External (third-party)

- `pytest` (lines 14)

### Standard library

- `__future__` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 22: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `ALLOWED`
- `GATES`
- `MODELS`
- `ORDER`
- `REPO`
- `STAGE_GATES`

## Classes and functions

- **function `restore_prerequisite`** [L52-54]: `def restore_prerequisite(monkeypatch)` decorators: @pytest.fixture(autouse=True) - begin_stage rebinds the shared K4 global; restore it for the other suites.
- **test `test_gate_order_is_the_section_16_order`** [L57-63]: `def test_gate_order_is_the_section_16_order()`
- **test `test_stage_gates_and_required_pass_sets`** [L66-69]: `def test_stage_gates_and_required_pass_sets()`
- **test `test_prerequisite_dict_and_binding`** [L72-77]: `def test_prerequisite_dict_and_binding()`
- **function `policy_at`** [L80-88]: `def policy_at(gate)` - A fresh LogitPolicy advanced through every earlier gate (each begun, then passed).
- **test `test_logit_policy_table`** [L93-100]: `def test_logit_policy_table(gate, kind)` decorators: @pytest.mark.parametrize('gate', GATES) @pytest.mark.parametrize('kind', sorted(ALLOWED))
- **test `test_no_logit_kind_at_calibration_gates_except_the_m0_identity_check`** [L103-111]: `def test_no_logit_kind_at_calibration_gates_except_the_m0_identity_check()`
- **test `test_gates_begin_only_in_order`** [L114-122]: `def test_gates_begin_only_in_order()`
- **test `test_endpoint_logits_never_follow_a_failed_t_pre`** [L125-135]: `def test_endpoint_logits_never_follow_a_failed_t_pre()` - Row 20 not passed: no fresh primary/control logits, and NUM cannot begin.
- **test `test_endpoint_logits_after_t_pre_passes`** [L138-142]: `def test_endpoint_logits_after_t_pre_passes()`
- **function `pass_gates`** [L145-147]: `def pass_gates(out, names)`
- **function `oracle_done`** [L150-154]: `def oracle_done(out, omit=())`
- **function `last_stage_event`** [L157-158]: `def last_stage_event(out)`
- **test `test_begin_stage_accepts_a_complete_prerequisite`** [L161-166]: `def test_begin_stage_accepts_a_complete_prerequisite(tmp_path)`
- **test `test_begin_stage_refuses_a_missing_pass`** [L170-174]: `def test_begin_stage_refuses_a_missing_pass(tmp_path, missing)` decorators: @pytest.mark.parametrize('missing', ['G0', 'N0', 'H5'])
- **test `test_check_pass_set_names_the_prerequisite_gates`** [L177-182]: `def test_check_pass_set_names_the_prerequisite_gates(tmp_path)`
- **test `test_begin_stage_refuses_after_a_recorded_non_pass`** [L185-189]: `def test_begin_stage_refuses_after_a_recorded_non_pass(tmp_path)`
- **test `test_begin_stage_refuses_a_retry`** [L192-198]: `def test_begin_stage_refuses_a_retry(tmp_path)`
- **test `test_begin_stage_refuses_changed_evidence`** [L201-206]: `def test_begin_stage_refuses_changed_evidence(tmp_path)`
- **test `test_begin_stage_refuses_an_uncompleted_prerequisite`** [L209-213]: `def test_begin_stage_refuses_an_uncompleted_prerequisite(tmp_path)`
- **test `test_validation_needs_the_calibration_pass_set`** [L216-223]: `def test_validation_needs_the_calibration_pass_set(tmp_path)`

