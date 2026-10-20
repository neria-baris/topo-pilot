# `tools/code_index/resolve.py`

- Source: [tools/code_index/resolve.py](../../../../../tools/code_index/resolve.py)
- Kind: python
- Lines: 141

## Module docstring

> Import resolution against the tracked Python files (heuristics documented in README).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `collections` (lines 5)
- `posixpath` (lines 2)
- `re` (lines 3)
- `sys` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/code_index/model.py](model.py.md) (line 6, import)

## Top-level constants

- `SRC_ROOTS`
- `STDLIB`

## Classes and functions

- **function `join`** [L11-12]: `def join(*parts)`
- **class `Resolver`** [L15-141]
- **method `Resolver.__init__`** [L16-34]: `def __init__(self, pyfiles, dirs)`
- **method `Resolver.module_file`** [L37-50]: `def module_file(self, base, parts)` - Walk `parts` from directory `base`. Returns (file or None, complete).
- **method `Resolver.pair_dirs`** [L52-65]: `def pair_dirs(self, d)`
- **method `Resolver.bare_steps`** [L67-73]: `def bare_steps(self, fpath, syspath_dirs, parts)`
- **method `Resolver.find_module`** [L75-90]: `def find_module(self, fpath, syspath_dirs, parts)` - Resolve a level-0 dotted name. Returns (status, files, how).
- **method `Resolver.submodules`** [L92-103]: `def submodules(self, mfile, base_dir, names)` - Targets of `from M import names`: submodule files where they exist, else M.
- **method `Resolver.resolve`** [L106-111]: `def resolve(self, rec, fpath, syspath_dirs)` - Return dict(status, targets, candidates, how, top) for one import record.
- **method `Resolver._one`** [L113-141]: `def _one(self, fpath, syspath_dirs, parts, names, level)`

