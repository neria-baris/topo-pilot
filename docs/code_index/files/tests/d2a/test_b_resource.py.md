# `tests/d2a/test_b_resource.py`

- Source: [tests/d2a/test_b_resource.py](../../../../../tests/d2a/test_b_resource.py)
- Kind: python
- Lines: 366

## Module docstring

> Independent tests (author B, job 0028): T-RESOURCE for ``d2a_train`` (dispatch identity, meter
> binding, supervisor, budgets, disk floors, STOP/HOLD propagation) plus RUNS, WAVES and Limits.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 26, via package root)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 33, via sys.path edit)
- `from d2a_train import D2AStop` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 34, via sys.path edit)

### External (third-party)

- `pytest` (lines 23)

### Standard library

- `__future__` (lines 10)
- `collections` (lines 19, 20)
- `dataclasses` (lines 12)
- `hashlib` (lines 13)
- `json` (lines 14)
- `math` (lines 15)
- `pathlib` (lines 21)
- `re` (lines 16)
- `sys` (lines 17)
- `types` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 31: `str(REPO / _sub)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CHILDREN`
- `DIGEST`
- `REPO`
- `TASK_MD`

## Classes and functions

- **test `test_runs_are_the_fourteen_registered_models`** [L44-47]: `def test_runs_are_the_fourteen_registered_models()`
- **test `test_waves_follow_the_fixed_order`** [L50-60]: `def test_waves_follow_the_fixed_order()`
- **test `test_training_and_model_configs`** [L63-66]: `def test_training_and_model_configs()`
- **test `test_limits_defaults_are_the_s6_values`** [L69-77]: `def test_limits_defaults_are_the_s6_values()`
- **function `_mailbox`** [L82-98]: `def _mailbox(tmp_path, *, command='RUN_NEXT', req_job=JOB, req_digest=DIGEST, json_digest=DIGEST, task_md=TASK_MD, lock_session=SESSION)`
- **test `test_verify_identity_accepts_the_correct_identity`** [L101-103]: `def test_verify_identity_accepts_the_correct_identity(tmp_path)`
- **test `test_verify_identity_rejects_each_wrong_identity`** [L117-123]: `def test_verify_identity_rejects_each_wrong_identity(tmp_path, call, build)` decorators: @pytest.mark.parametrize('call, build', [({'job_id': '0029'}, {}), ({'task_sha256': '0' * 64}, {}), ({'session': 'someone-else'}, {}), ({}, {'command': 'STOP'}), ({}, {'req_job': '0029'}), ({}, {'req_digest': 'F' * 64}), ({}, {'json_digest': 'E' * 64}), ({}, {'task_md': TASK_MD + b'tampered'}), ({}, {'lock_session': 'another-session'})])
- **test `test_verify_identity_fails_closed_without_a_lock`** [L126-130]: `def test_verify_identity_fails_closed_without_a_lock(tmp_path)`
- **function `_fakes`** [L135-145]: `def _fakes(tmp_path)`
- **test `test_bind_meter_sets_exactly_the_section_11_3_names`** [L148-172]: `def test_bind_meter_sets_exactly_the_section_11_3_names(tmp_path)`
- **class `Procs`** [L177-184]
- **method `Procs.__init__`** [L178-179]: `def __init__(self, cpu, mem)`
- **method `Procs.supervisor`** [L181-184]: `def supervisor(self, limits=None)`
- **function `_status`** [L187-192]: `def _status(reason)`
- **function `_poll`** [L195-199]: `def _poll(reason)`
- **test `test_supervisor_quiet_when_every_limit_is_met_exactly`** [L205-210]: `def test_supervisor_quiet_when_every_limit_is_met_exactly()`
- **test `test_supervisor_model_cpu_kills_only_that_child`** [L213-219]: `def test_supervisor_model_cpu_kills_only_that_child()`
- **test `test_supervisor_process_memory_kills_only_that_child`** [L222-228]: `def test_supervisor_process_memory_kills_only_that_child()`
- **test `test_supervisor_stage_budget_kills_all`** [L232-242]: `def test_supervisor_stage_budget_kills_all(cpu2, over)` decorators: @pytest.mark.parametrize('cpu2, over', [(50.0, True), (40.0, False)])
- **test `test_supervisor_total_budget_kills_all`** [L246-255]: `def test_supervisor_total_budget_kills_all(cpu3, over)` decorators: @pytest.mark.parametrize('cpu3, over', [(5.0, True), (4.0, False)])
- **test `test_supervisor_reasons_record_the_polling_interval`** [L258-264]: `def test_supervisor_reasons_record_the_polling_interval()`
- **test `test_admit`** [L275-277]: `def test_admit(spent_stage, spent_total, need, ok)` decorators: @pytest.mark.parametrize('spent_stage, spent_total, need, ok', [(50200.0, 50200.0, 200.0, True), (50200.0, 50200.0, 200.5, False), (0.0, 114 * HOUR - 100.0, 150.0, False), (0.0, 114 * HOUR - 150.0, 150.0, True)])
- **test `test_stage_and_total_spent_on_a_synthetic_ledger`** [L280-292]: `def test_stage_and_total_spent_on_a_synthetic_ledger()`
- **function `_usage`** [L300-311]: `def _usage(free_c, free_x, broken='')`
- **test `test_disk_reason`** [L321-327]: `def test_disk_reason(free_c, free_x, broken, stop)` decorators: @pytest.mark.parametrize('free_c, free_x, broken, stop', [(2000000000, 30000000000, '', False), (1999999999, 30000000000, '', True), (2000000000, 29999999999, '', True), (10 ** 12, 10 ** 13, 'C', True), (10 ** 12, 10 ** 13, 'X', True)])
- **function `_classify`** [L332-340]: `def _classify(states)`
- **test `test_boundary_continue_returns_at_once`** [L343-347]: `def test_boundary_continue_returns_at_once()`
- **test `test_boundary_hold_waits_then_continues`** [L350-354]: `def test_boundary_hold_waits_then_continues()`
- **test `test_boundary_stop_and_invalid_raise`** [L359-366]: `def test_boundary_stop_and_invalid_raise(state, holds)` decorators: @pytest.mark.parametrize('state', ['STOP', 'INVALID']) @pytest.mark.parametrize('holds', [0, 2])

