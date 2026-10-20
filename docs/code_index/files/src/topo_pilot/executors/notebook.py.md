# `src/topo_pilot/executors/notebook.py`

- Source: [src/topo_pilot/executors/notebook.py](../../../../../../src/topo_pilot/executors/notebook.py)
- Kind: python
- Lines: 66

## Module docstring

> NotebookExporter: a minimal three-cell ``.ipynb`` that runs a bundle (no Drive, no services).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `json` (lines 5)
- `pathlib` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/__init__.py](__init__.py.md) (line 8, import)

## Top-level constants

- `CELL_INSTALL`
- `CELL_RUN`
- `CELL_UNPACK`

## Classes and functions

- **class `NotebookExporter`** [L38-66] - Writes a minimal nbformat-4 notebook: unpack, install the lock, run and pack.
- **method `NotebookExporter.export`** [L41-66]: `def export(self, bundle_path: Path, dest: Path) -> Path` - Write the notebook for ``bundle_<job>.tar.gz``.

