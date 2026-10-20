# `tests/d2a/test_process_tree_repair.py`

- Source: [tests/d2a/test_process_tree_repair.py](../../../../../tests/d2a/test_process_tree_repair.py)
- Kind: python
- Lines: 142

## Module docstring

> Maintenance regression: real Windows launcher grandchildren, no research data or training.

## Imports

### Internal (repo files)

- `from d2a_train import Limits, Supervisor` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 20, via sys.path edit)
- `from process_tree import TrainingProcess` -> [tools/d2a/process_tree.py](../../tools/d2a/process_tree.py.md) (line 21, via sys.path edit)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 84, via sys.path edit) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 112, via sys.path edit) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../../tools/d2a/d2a_train.py.md) (line 124, via sys.path edit) (inside a function)
- `from process_tree import wave_lease` -> [tools/d2a/process_tree.py](../../tools/d2a/process_tree.py.md) (line 125, via sys.path edit) (inside a function)
- `from process_tree import wave_lease` -> [tools/d2a/process_tree.py](../../tools/d2a/process_tree.py.md) (line 137, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `dataclasses` (lines 5)
- `json` (lines 6)
- `os` (lines 7)
- `pathlib` (lines 11)
- `subprocess` (lines 8)
- `sys` (lines 9)
- `time` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / directory)` -> `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `launch_grandchild`** [L24-46]: `def launch_grandchild(tmp_path)`
- **test `test_exited_launcher_does_not_hide_live_grandchild_or_its_usage`** [L49-62]: `def test_exited_launcher_does_not_hide_live_grandchild_or_its_usage(tmp_path)`
- **test `test_supervisor_enforces_limits_on_grandchild`** [L69-80]: `def test_supervisor_enforces_limits_on_grandchild(tmp_path, limit, reason)` decorators: @pytest.mark.parametrize('limit,reason', [({'model_cpu_s': 0.05}, 'INCOMPLETE:MODEL_CPU'), ({'process_mem': 1024 ** 2}, 'INCOMPLETE:PROCESS_MEMORY')])
- **test `test_wave_exception_closes_all_started_trees`** [L83-106]: `def test_wave_exception_closes_all_started_trees(tmp_path, monkeypatch)`
- **test `test_wave_refuses_duplicate_training_before_launch`** [L111-120]: `def test_wave_refuses_duplicate_training_before_launch(tmp_path, monkeypatch, record)` decorators: @pytest.mark.parametrize('record', ['waves/W1.json', 'runs/d2a-s1-H3.json', 'runs/d2a-s2-H3.attempt.json'])
- **test `test_concurrent_wave_is_refused_before_launch`** [L123-132]: `def test_concurrent_wave_is_refused_before_launch(tmp_path, monkeypatch)`
- **test `test_wave_lease_rejects_path_components_before_creating_files`** [L136-142]: `def test_wave_lease_rejects_path_components_before_creating_files(tmp_path, wave)` decorators: @pytest.mark.parametrize('wave', ['../escape', '..\\escape', 'X:escape'])

