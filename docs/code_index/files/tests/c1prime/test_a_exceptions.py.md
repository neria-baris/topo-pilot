# `tests/c1prime/test_a_exceptions.py`

- Source: [tests/c1prime/test_a_exceptions.py](../../../../../tests/c1prime/test_a_exceptions.py)
- Kind: python
- Lines: 213

## Module docstring

> Independent tests, author A (job 0026): the exception mapping of protocol section 16
> conventions (v4 review fix 5) and the generic C1 gate boundary run_c1_gate (TEST_PLAN A-6, third
> bullet; API.md section 2 classify_exception, C1GateFailure, CertificateFlag, C1Stop).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 30, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 32, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 33, via sys.path edit)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 34, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 35, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 36, via sys.path edit)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 37, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 11)
- `decimal` (lines 13, 16)
- `pathlib` (lines 17)
- `re` (lines 14)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 28: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `CASES`
- `KINDS`
- `REASONS`
- `REPO`

## Classes and functions

- **function `full`** [L46-55]: `def full(status, reason)`
- **function `caught`** [L58-63]: `def caught(fn)`
- **function `failure`** [L66-67]: `def failure(code, detail='detail text')`
- **function `gate_failed_with_status`** [L70-73]: `def gate_failed_with_status(status)`
- **function `reference_value_error`** [L76-78]: `def reference_value_error()`
- **function `decimal_underflow`** [L81-85]: `def decimal_underflow()`
- **function `decimal_invalid_operation`** [L88-92]: `def decimal_invalid_operation()`
- **test `test_fixtures_raise_what_they_claim`** [L123-126]: `def test_fixtures_raise_what_they_claim()`
- **test `test_classify_exception`** [L130-132]: `def test_classify_exception(name, make, expected)` decorators: @pytest.mark.parametrize('name, make, expected', CASES, ids=[c[0] for c in CASES])
- **test `test_other_stage_failures_keep_code_and_message`** [L137-141]: `def test_other_stage_failures_keep_code_and_message(code)` decorators: @pytest.mark.parametrize('code', [ErrorCode.IMPOSSIBLE_HISTORY, ErrorCode.ALIGNMENT_ERROR, ErrorCode.CHECKSUM_MISMATCH])
- **test `test_run_c1_gate_records_and_stops`** [L145-161]: `def test_run_c1_gate_records_and_stops(tmp_path, name, make, expected)` decorators: @pytest.mark.parametrize('name, make, expected', CASES, ids=[c[0] for c in CASES])
- **function `innermost_name`** [L164-170]: `def innermost_name(exc)`
- **test `test_operation_is_the_originating_function`** [L173-182]: `def test_operation_is_the_originating_function(tmp_path)`
- **test `test_returned_pass_dict_is_recorded_and_returned`** [L185-189]: `def test_returned_pass_dict_is_recorded_and_returned(tmp_path)`
- **test `test_returned_non_pass_dict_stops_the_cohort`** [L193-199]: `def test_returned_non_pass_dict_stops_the_cohort(tmp_path, status)` decorators: @pytest.mark.parametrize('status', ['INCONCLUSIVE/ELIGIBILITY', 'FAIL_TECHNICAL/LINEAGE'])
- **test `test_status_of_splits_full_strings`** [L202-205]: `def test_status_of_splits_full_strings()`
- **test `test_c1stop_carries_gate_status_reason`** [L208-213]: `def test_c1stop_carries_gate_status_reason()`

