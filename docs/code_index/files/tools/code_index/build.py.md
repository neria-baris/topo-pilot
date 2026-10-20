# `tools/code_index/build.py`

- Source: [tools/code_index/build.py](../../../../../tools/code_index/build.py)
- Kind: python
- Lines: 111

## Module docstring

> Assemble all index outputs in memory; write them or compare them with the disk copy.

## Imports

### Internal (repo files)

- `from . import render_deps, render_lists, render_pages` -> [tools/code_index/render_deps.py](render_deps.py.md), [tools/code_index/render_lists.py](render_lists.py.md), [tools/code_index/render_pages.py](render_pages.py.md) (line 6, via relative)
- `from .model import build_model` -> [tools/code_index/model.py](model.py.md) (line 7, via relative)
- `from .scan import OUT_DIR, REPO` -> [tools/code_index/scan.py](scan.py.md) (line 8, via relative)

### External (third-party)

- none

### Standard library

- `argparse` (lines 2)
- `collections` (lines 4)
- `sys` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/build_code_index.py](../build_code_index.py.md) (line 5, import)

## Top-level constants

- `PY_KINDS`

## Classes and functions

- **function `counts_of`** [L13-34]: `def counts_of(model)`
- **function `generate`** [L37-58]: `def generate(root=REPO)` - Return ({relative output path: bytes}, counts).
- **function `existing`** [L61-62]: `def existing(base)`
- **function `write`** [L65-78]: `def write(root, outputs)`
- **function `check`** [L81-88]: `def check(root, outputs)`
- **function `main`** [L91-107]: `def main(argv=None)`

