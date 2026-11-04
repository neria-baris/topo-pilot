# `tests/hwsg/test_b_guard.py`

- Source: [tests/hwsg/test_b_guard.py](../../../../../tests/hwsg/test_b_guard.py)
- Kind: python
- Lines: 107

## Module docstring

> Author B: blindness guard (protocol 8, DRG11).

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, expect_fail, mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 12, via same directory)

### External (third-party)

- `pytest` (lines 9)

### Standard library

- `__future__` (lines 2)
- `builtins` (lines 4)
- `os` (lines 5)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- `BL`

## Classes and functions

- **function `_root`** [L17-18]: `def _root()`
- **test `test_blinded_files`** [L22-26]: `def test_blinded_files(rel)` decorators: @pytest.mark.parametrize('rel', BL['files'])
- **test `test_blinded_dirs_and_below`** [L30-33]: `def test_blinded_dirs_and_below(rel)` decorators: @pytest.mark.parametrize('rel', BL['dirs'])
- **test `test_blinded_globs`** [L37-42]: `def test_blinded_globs(parent, pattern)` decorators: @pytest.mark.parametrize('parent,pattern', BL['globs'])
- **test `test_blinded_job_range`** [L46-50]: `def test_blinded_job_range(n)` decorators: @pytest.mark.parametrize('n', [197, 200, 210, 223])
- **test `test_not_blinded`** [L56-59]: `def test_not_blinded(rel)` decorators: @pytest.mark.parametrize('rel', ['agent-handoff/jobs/0196/task.md', 'agent-handoff/jobs/0224/task.md', 'hwsb-store/HANDOFF.json', 'tools/hwsg/CONTRACT.json'] + list(BL['allow'][:3]))
- **test `test_public_summary`** [L62-69]: `def test_public_summary()`
- **test `test_guard_raises_before_any_open`** [L72-83]: `def test_guard_raises_before_any_open(monkeypatch)`
- **test `test_prune_removes_blinded_dirs_before_descent`** [L86-96]: `def test_prune_removes_blinded_dirs_before_descent(tmp_path)`
- **test `test_prune_in_os_walk_never_enters`** [L99-107]: `def test_prune_in_os_walk_never_enters(tmp_path)`

