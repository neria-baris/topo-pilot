# `tools/code_index/render_deps.py`

- Source: [tools/code_index/render_deps.py](../../../../../tools/code_index/render_deps.py)
- Kind: python
- Lines: 101

## Module docstring

> DEPENDENCIES.md: package graph, per-file adjacency, entry-point trees, cycles, problems.

## Imports

### Internal (repo files)

- `from .render_pages import code` -> [tools/code_index/render_pages.py](render_pages.py.md) (line 5, via relative)

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

- [tools/code_index/build.py](build.py.md) (line 6, import)

## Top-level constants

- `PKG_ROOT`

## Classes and functions

- **function `package_of`** [L10-14]: `def package_of(path)`
- **function `package_graph`** [L17-27]: `def package_graph(model)`
- **function `groups`** [L30-41]: `def groups(model)` - Entry-point groups: name -> root files.
- **function `tree_lines`** [L44-62]: `def tree_lines(roots, out_edges)`
- **function `render`** [L65-101]: `def render(model)`

