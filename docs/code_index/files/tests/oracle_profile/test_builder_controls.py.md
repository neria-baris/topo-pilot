# `tests/oracle_profile/test_builder_controls.py`

- Source: [tests/oracle_profile/test_builder_controls.py](../../../../../tests/oracle_profile/test_builder_controls.py)
- Kind: python
- Lines: 238

## Module docstring

> BUILDER tests (not independent): runtime-control classifier on synthetic mailboxes only.

## Imports

### Internal (repo files)

- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 17, via sys.path edit)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(Path(__file__).resolve().parents[2] / 'tools' / 'x4_oracle_profile')` -> `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `DIGEST`
- `TASK`

## Classes and functions

- **function `box`** [L24-33]: `def box(tmp_path, monkeypatch)` decorators: @pytest.fixture()
- **function `write`** [L36-37]: `def write(root: Path, name: str, obj) -> None`
- **function `usage`** [L40-45]: `def usage(percent, warning, relevant=True) -> dict`
- **function `state`** [L48-49]: `def state(root, out=None, mode='run')`
- **test `test_continue`** [L52-53]: `def test_continue(box)`
- **test `test_stop_files`** [L57-60]: `def test_stop_files(box, tmp_path_factory, where)` decorators: @pytest.mark.parametrize('where', ['owner', 'own'])
- **test `test_request_and_control_stop`** [L63-68]: `def test_request_and_control_stop(box)`
- **test `test_stop_beats_invalid_and_hold`** [L71-77]: `def test_stop_beats_invalid_and_hold(box)`
- **test `test_invalid_request`** [L89-91]: `def test_invalid_request(box, request_obj)` decorators: @pytest.mark.parametrize('request_obj', [{'command': 'RUN_NEXT', 'job_id': '0015', 'task_sha256': DIGEST}, {'command': 'RUN_NEXT', 'job_id': '0014', 'task_sha256': '0' * 64}, {'command': 'PAUSE', 'job_id': '0014', 'task_sha256': DIGEST}, [1, 2]])
- **test `test_invalid_unreadable_and_task_bytes`** [L94-101]: `def test_invalid_unreadable_and_task_bytes(box)`
- **test `test_invalid_unknown_control_and_usage`** [L104-112]: `def test_invalid_unknown_control_and_usage(box)`
- **test `test_holds`** [L115-131]: `def test_holds(box)`
- **test `test_audit_mode`** [L134-149]: `def test_audit_mode(box)`
- **test `test_classify_all_most_restrictive`** [L152-161]: `def test_classify_all_most_restrictive(box, tmp_path_factory)`
- **test `test_malformed_percent_fails_closed`** [L165-167]: `def test_malformed_percent_fails_closed(box, value)` decorators: @pytest.mark.parametrize('value', [float('nan'), float('inf'), -1.0, 100.5, True, '50'])
- **test `test_utc_parsing_accepts_coordinator_timestamps`** [L170-174]: `def test_utc_parsing_accepts_coordinator_timestamps()`
- **function `latched`** [L177-178]: `def latched(box, latch_dir)`
- **test `test_persistent_latch_requires_fresh_clearance_and_release`** [L181-218]: `def test_persistent_latch_requires_fresh_clearance_and_release(box, tmp_path_factory)`
- **test `test_latch_from_coordinator_hold_and_stop_precedence`** [L221-231]: `def test_latch_from_coordinator_hold_and_stop_precedence(box, tmp_path_factory)`
- **test `test_classify_all_latches_synthetic_in_its_own_dir`** [L234-238]: `def test_classify_all_latches_synthetic_in_its_own_dir(box, tmp_path_factory)`

