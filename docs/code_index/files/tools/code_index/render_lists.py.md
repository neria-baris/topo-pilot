# `tools/code_index/render_lists.py`

- Source: [tools/code_index/render_lists.py](../../../../../tools/code_index/render_lists.py)
- Kind: python
- Lines: 143

## Module docstring

> FILES.md, FUNCTIONS*.md, index.json and README.md.

## Imports

### Internal (repo files)

- `from .render_pages import cell, code, page_path` -> [tools/code_index/render_pages.py](render_pages.py.md) (line 6, via relative)
- `from .scan import EXCLUDE` -> [tools/code_index/scan.py](scan.py.md) (line 7, via relative)

### External (third-party)

- none

### Standard library

- `collections` (lines 4)
- `json` (lines 2)
- `posixpath` (lines 3)

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

- `CHUNK_BYTES`
- `EXCLUSION_NOTE`

## Classes and functions

- **function `size_text`** [L15-16]: `def size_text(rec)`
- **function `files_md`** [L19-38]: `def files_md(model)`
- **function `function_rows`** [L41-49]: `def function_rows(model)`
- **function `functions_md`** [L52-78]: `def functions_md(model)`
- **function `index_json`** [L81-93]: `def index_json(model, counts)`
- **function `readme_md`** [L96-143]: `def readme_md(model, counts)`

