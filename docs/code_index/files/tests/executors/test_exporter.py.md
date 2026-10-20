# `tests/executors/test_exporter.py`

- Source: [tests/executors/test_exporter.py](../../../../../tests/executors/test_exporter.py)
- Kind: python
- Lines: 87

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from exec_helpers import make_job, seed_input` -> [tests/executors/exec_helpers.py](exec_helpers.py.md) (line 9, via same directory)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 11, via package root)
- `from topo_pilot.executors import BundleExecutor, NotebookExporter, SSHExecutor` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md) (line 12, via package root)
- `from topo_pilot.executors.bundle import is_forbidden` -> [src/topo_pilot/executors/bundle.py](../../src/topo_pilot/executors/bundle.py.md) (line 13, via package root)
- `from topo_pilot.executors import JobHandle` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md) (line 82, via package root) (inside a function)

### External (third-party)

- `pytest` (lines 5)

### Standard library

- `json` (lines 43)
- `pathlib` (lines 3)
- `re` (lines 1)
- `tarfile` (lines 2)

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

- `LOCAL`

## Classes and functions

- **test `test_E04_secrets_in_tree_are_left_out`** [L16-23]: `def test_E04_secrets_in_tree_are_left_out(store, fake_repo, tmp_path)`
- **test `test_E04_explicitly_requested_secret_is_refused`** [L28-34]: `def test_E04_explicitly_requested_secret_is_refused(store, fake_repo, tmp_path, secret)` decorators: @pytest.mark.parametrize('secret', ['configs/local.yaml', 'configs/api_token.txt', '.env', 'configs/my_KEY.json'])
- **test `test_E04_forbidden_name_rule`** [L37-39]: `def test_E04_forbidden_name_rule()`
- **test `test_E06_notebook_is_valid_nbformat_with_three_code_cells`** [L42-57]: `def test_E06_notebook_is_valid_nbformat_with_three_code_cells(tmp_path)`
- **test `test_E01_ssh_builds_expected_command_lines`** [L63-72]: `def test_E01_ssh_builds_expected_command_lines(tmp_path)`
- **test `test_E01_ssh_requires_host_and_remote_dir`** [L75-78]: `def test_E01_ssh_requires_host_and_remote_dir(tmp_path)`
- **test `test_E01_ssh_status_parses_remote_output`** [L81-87]: `def test_E01_ssh_status_parses_remote_output(tmp_path, monkeypatch)`

