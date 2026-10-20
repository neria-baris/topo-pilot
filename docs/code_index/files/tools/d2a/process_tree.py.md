# `tools/d2a/process_tree.py`

- Source: [tools/d2a/process_tree.py](../../../../../tools/d2a/process_tree.py)
- Kind: python
- Lines: 88

## Module docstring

> Windows training process tree: nested Job Object, attached before any child runs.

## Imports

### Internal (repo files)

- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 13, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `contextlib` (lines 11)
- `ctypes` (lines 8)
- `os` (lines 9)
- `subprocess` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 21, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 125, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 137, import)
- [tools/d2a/d2a_train.py](d2a_train.py.md) (line 307, import)
- [tools/d2a/d2a_train.py](d2a_train.py.md) (line 318, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 304, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 347, import)

## Top-level constants

- none

## Classes and functions

- **function `wave_lease`** [L17-31]: `def wave_lease(root, wave)` decorators: @contextmanager - Exclusive wave lease; an abandoned lease is never silently cleared.
- **class `TrainingProcess`** [L34-88] - Popen-compatible training handle with accounting for launcher and descendants.
- **method `TrainingProcess.__init__`** [L37-58]: `def __init__(self, args, **kwargs)`
- **method `TrainingProcess.returncode`** [L61-62]: `def returncode(self)` decorators: @property
- **method `TrainingProcess.cpu_s`** [L64-66]: `def cpu_s(self) -> float`
- **method `TrainingProcess.memory_bytes`** [L68-72]: `def memory_bytes(self) -> int` - Peak per-process committed memory, including processes that already exited.
- **method `TrainingProcess.poll`** [L74-76]: `def poll(self)`
- **method `TrainingProcess.terminate`** [L78-80]: `def terminate(self) -> None`
- **method `TrainingProcess.wait`** [L82-83]: `def wait(self)`
- **method `TrainingProcess.close`** [L85-88]: `def close(self) -> None`

