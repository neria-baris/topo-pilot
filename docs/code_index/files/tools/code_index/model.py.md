# `tools/code_index/model.py`

- Source: [tools/code_index/model.py](../../../../../tools/code_index/model.py)
- Kind: python
- Lines: 143

## Module docstring

> Build the in-memory index model: records, per-file facts, resolved edges, cycles, stats.

## Imports

### Internal (repo files)

- `from . import pyinfo, shinfo` -> [tools/code_index/pyinfo.py](pyinfo.py.md), [tools/code_index/shinfo.py](shinfo.py.md) (line 5, via relative)
- `from .resolve import Resolver` -> [tools/code_index/resolve.py](resolve.py.md) (line 6, via relative)
- `from .scan import list_tracked, read_file, sources_digest` -> [tools/code_index/scan.py](scan.py.md) (line 7, via relative)

### External (third-party)

- none

### Standard library

- `collections` (lines 3)
- `posixpath` (lines 2)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/code_index/build.py](build.py.md) (line 7, import)
- [tools/code_index/render_pages.py](render_pages.py.md) (line 4, import)

## Top-level constants

- `PY_KINDS`
- `SH_KINDS`

## Classes and functions

- **function `import_text`** [L13-16]: `def import_text(rec)`
- **function `ancestors`** [L19-26]: `def ancestors(paths)`
- **function `tarjan`** [L29-69]: `def tarjan(nodes, out)` - Iterative Tarjan SCC; returns the list of components (each a sorted list).
- **function `resolve_dynamic`** [L72-84]: `def resolve_dynamic(dyn, path, resolver, sp_dirs, pyfiles)`
- **function `build_model`** [L87-143]: `def build_model(root)`

