# `tools/code_index/shinfo.py`

- Source: [tools/code_index/shinfo.py](../../../../../tools/code_index/shinfo.py)
- Kind: python
- Lines: 40

## Module docstring

> PowerShell / shell scripts: function definitions and invoked repo scripts (regex based).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `posixpath` (lines 2)
- `re` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/code_index/model.py](model.py.md) (line 5, import)

## Top-level constants

- `FUNC_PS`
- `FUNC_SH`
- `SCRIPT`

## Classes and functions

- **function `extract`** [L10-40]: `def extract(path, text, kind, code_files)` - Return {functions: [{name, line}], invokes: [{line, token, target}]}.

