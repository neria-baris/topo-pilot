# `tests/c1prime/test_c_release_worker.py`

- Source: [tests/c1prime/test_c_release_worker.py](../../../../../tests/c1prime/test_c_release_worker.py)
- Kind: python
- Lines: 52

## Module docstring

> Coordinator regression test (job 0035, ruling R10): `c1_release.authorized_worker` takes the
> executing worker session from a verified release (protocol §18: "the authorized executing
> worker session"), requires the job's task.md to name it, and falls back to the CONTRACT default
> when the release has no `worker_session`. Pure function; no meter, no store, no git.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 18, via sys.path edit)
- `import c1_release` -> [tools/c1prime/c1_release.py](../../tools/c1prime/c1_release.py.md) (line 19, via sys.path edit)

### External (third-party)

- `pytest` (lines 11)

### Standard library

- `__future__` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / _sub)` -> `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `SESSION`

## Classes and functions

- **function `_job`** [L24-28]: `def _job(tmp_path, task_text)`
- **test `test_release_session_named_in_task`** [L31-33]: `def test_release_session_named_in_task(tmp_path)`
- **test `test_release_session_not_in_task_is_refused`** [L36-39]: `def test_release_session_not_in_task_is_refused(tmp_path)`
- **test `test_malformed_release_session_is_refused`** [L43-46]: `def test_malformed_release_session_is_refused(tmp_path, bad)` decorators: @pytest.mark.parametrize('bad', ['', 7, None.__class__])
- **test `test_no_release_session_falls_back_to_contract`** [L49-52]: `def test_no_release_session_falls_back_to_contract(tmp_path)`

