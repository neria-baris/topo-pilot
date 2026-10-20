# `tests/experiment/test_x5g1t_runtime.py`

- Source: [tests/experiment/test_x5g1t_runtime.py](../../../../../tests/experiment/test_x5g1t_runtime.py)
- Kind: python
- Lines: 353

## Module docstring

> Independent tests written from the API contract only (X5_G1_TRAINING_API.md §5 and §8
> "Runtime"; protocol x5g1-train-v3 §8), before reading ``x5g1t_runtime``.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x5g1t_runtime` -> [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md) (line 18, via package root)
- `from topo_pilot.experiment.x5g1_controls import StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 19, via package root)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 14)
- `time` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `KIND`

## Classes and functions

- **function `_put`** [L26-28]: `def _put(mailbox: Path, name: str, content) -> None`
- **function `mb`** [L32-37]: `def mb(tmp_path: Path) -> Path` decorators: @pytest.fixture - A mailbox that allows running: only a valid request.json.
- **function `_action`** [L40-44]: `def _action(mailbox: Path) -> str`
- **test `test_controlstate_is_namedtuple`** [L50-55]: `def test_controlstate_is_namedtuple(mb: Path) -> None`
- **test `test_stop_file_is_stop_with_owner_reason`** [L58-62]: `def test_stop_file_is_stop_with_owner_reason(mb: Path) -> None`
- **test `test_stop_file_beats_worker_hold`** [L65-69]: `def test_stop_file_beats_worker_hold(mb: Path) -> None`
- **test `test_request_stop_command`** [L72-74]: `def test_request_stop_command(mb: Path) -> None`
- **test `test_request_missing_or_bad_fails_closed`** [L80-85]: `def test_request_missing_or_bad_fails_closed(mb: Path, content) -> None` decorators: @pytest.mark.parametrize('content', [None, '{not json', '', '[1, 2]', '"RUN_NEXT"', {'command': 'PAUSE'}, {'command': 'run_next'}, {'command': None}, {}])
- **test `test_worker_control_commands`** [L91-93]: `def test_worker_control_commands(mb: Path, command: str, expected: str) -> None` decorators: @pytest.mark.parametrize('command, expected', [('STOP', 'STOP'), ('WAIT_USAGE_RESET', 'HOLD'), ('CONTINUE', 'CONTINUE')])
- **test `test_worker_control_malformed_or_unknown_is_stop`** [L98-100]: `def test_worker_control_malformed_or_unknown_is_stop(mb: Path, content) -> None` decorators: @pytest.mark.parametrize('content', ['{oops', '', '[]', '"STOP"', {'command': 'PAUSE'}, {'command': 'wait_usage_reset'}])
- **test `test_worker_control_missing_is_allowed`** [L103-105]: `def test_worker_control_missing_is_allowed(mb: Path) -> None`
- **test `test_runtime_state_wait_is_hold`** [L108-110]: `def test_runtime_state_wait_is_hold(mb: Path) -> None`
- **test `test_runtime_state_other_modes_are_noop`** [L115-117]: `def test_runtime_state_other_modes_are_noop(mb: Path, mode: str) -> None` decorators: @pytest.mark.parametrize('mode', ['WORKING', 'WAITING', 'USAGE_READY'])
- **test `test_runtime_state_unknown_mode_is_stop`** [L122-124]: `def test_runtime_state_unknown_mode_is_stop(mb: Path, mode: str) -> None` decorators: @pytest.mark.parametrize('mode', ['RUNNING', 'IDLE', 'CONTINUE', 'STOP', 'anything'])
- **test `test_runtime_state_malformed_is_stop`** [L128-130]: `def test_runtime_state_malformed_is_stop(mb: Path, content: str) -> None` decorators: @pytest.mark.parametrize('content', ['{bad', '', '[1]', '42'])
- **test `test_claude_usage_unavailable_is_no_hold`** [L135-137]: `def test_claude_usage_unavailable_is_no_hold(mb: Path) -> None`
- **test `test_claude_usage_malformed_is_stop`** [L141-145]: `def test_claude_usage_malformed_is_stop(mb: Path, content) -> None` decorators: @pytest.mark.parametrize('content', [{'observability': 'UNAVAILABLE'}, '{garbage'])
- **test `test_stop_beats_hold_from_any_source`** [L150-165]: `def test_stop_beats_hold_from_any_source(mb: Path, stop_src: str, hold_src: str) -> None` decorators: @pytest.mark.parametrize('stop_src', ['file', 'request', 'worker', 'worker_bad', 'state_bad']) @pytest.mark.parametrize('hold_src', ['worker', 'state'])
- **test `test_both_holds_give_hold_with_reasons`** [L168-173]: `def test_both_holds_give_hold_with_reasons(mb: Path) -> None`
- **class `Script`** [L179-197] - A fake ``sleep`` that applies one mailbox mutation per call and records audits.
- **method `Script.__init__`** [L182-186]: `def __init__(self, mailbox: Path, audit_path: Path, steps, clock=None) -> None`
- **method `Script.__call__`** [L188-197]: `def __call__(self, seconds: float) -> None`
- **function `_wc`** [L200-201]: `def _wc(command: str)`
- **function `_rs`** [L204-205]: `def _rs(mode: str)`
- **function `_noop`** [L208-209]: `def _noop(box: Path) -> None`
- **function `_audit`** [L212-214]: `def _audit() -> dict`
- **function `_hold`** [L217-218]: `def _hold(mb: Path, audit_path: Path, script: Script, poll_s: float = 45.0) -> int`
- **test `test_no_hold_returns_zero_without_sleep_or_audit`** [L221-225]: `def test_no_hold_returns_zero_without_sleep_or_audit(mb: Path, tmp_path: Path) -> None`
- **test `test_stop_before_hold_raises`** [L228-232]: `def test_stop_before_hold_raises(mb: Path, tmp_path: Path) -> None`
- **test `test_resume_only_after_both_holds_released`** [L235-245]: `def test_resume_only_after_both_holds_released(mb: Path, tmp_path: Path) -> None`
- **test `test_release_in_other_order`** [L248-254]: `def test_release_in_other_order(mb: Path, tmp_path: Path) -> None`
- **test `test_removing_worker_control_releases_coordinator_hold`** [L257-261]: `def test_removing_worker_control_releases_coordinator_hold(mb: Path, tmp_path: Path) -> None`
- **test `test_time_never_resumes`** [L264-272]: `def test_time_never_resumes(mb: Path, tmp_path: Path, monkeypatch) -> None`
- **test `test_unreleased_hold_never_returns`** [L275-288]: `def test_unreleased_hold_never_returns(mb: Path, tmp_path: Path) -> None`
- **test `test_stop_while_held_raises`** [L298-305]: `def test_stop_while_held_raises(mb: Path, tmp_path: Path, stopper) -> None` decorators: @pytest.mark.parametrize('stopper', [lambda box: (box / 'STOP').write_text('', encoding='utf-8'), lambda box: _put(box, 'request.json', {'command': 'STOP'}), lambda box: _put(box, 'worker_control.json', {'command': 'STOP'}), lambda box: _put(box, 'runtime_state.json', '{corrupt'), lambda box: (box / 'request.json').unlink()])
- **test `test_audit_record_is_audit_only`** [L308-327]: `def test_audit_record_is_audit_only(mb: Path, tmp_path: Path) -> None`
- **test `test_poll_bounds_rejected_while_held`** [L331-337]: `def test_poll_bounds_rejected_while_held(mb: Path, tmp_path: Path, poll_s: float) -> None` decorators: @pytest.mark.parametrize('poll_s', [45.0001, 46.0, 3600.0, 0.0, -1.0])
- **test `test_poll_bounds_rejected_even_without_hold`** [L341-344]: `def test_poll_bounds_rejected_even_without_hold(mb: Path, tmp_path: Path, poll_s) -> None` decorators: @pytest.mark.parametrize('poll_s', [46.0, 0.0])
- **test `test_poll_bounds_inclusive_upper`** [L348-353]: `def test_poll_bounds_inclusive_upper(mb: Path, tmp_path: Path, poll_s: float) -> None` decorators: @pytest.mark.parametrize('poll_s', [45.0, 0.01])

