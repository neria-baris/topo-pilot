# `tools/code_index/render_pages.py`

- Source: [tools/code_index/render_pages.py](../../../../../tools/code_index/render_pages.py)
- Kind: python
- Lines: 136

## Module docstring

> Per-code-file pages: docs/code_index/files/<path>.md.

## Imports

### Internal (repo files)

- `from .model import import_text` -> [tools/code_index/model.py](model.py.md) (line 4, via relative)
- `from .scan import OUT_DIR` -> [tools/code_index/scan.py](scan.py.md) (line 5, via relative)

### External (third-party)

- none

### Standard library

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
- [tools/code_index/render_deps.py](render_deps.py.md) (line 5, import)
- [tools/code_index/render_lists.py](render_lists.py.md) (line 6, import)

## Top-level constants

- none

## Classes and functions

- **function `code`** [L8-10]: `def code(text)`
- **function `cell`** [L13-14]: `def cell(text)`
- **function `page_path`** [L17-18]: `def page_path(path)`
- **function `link_page`** [L21-22]: `def link_page(src_page_dir, target)`
- **function `link_source`** [L25-28]: `def link_source(path, page_rel)` - Relative link from an index page to the repo file (index lives in docs/code_index).
- **function `lines_text`** [L31-32]: `def lines_text(nums)`
- **function `imports_section`** [L35-76]: `def imports_section(path, info, page_dir)`
- **function `symbols_section`** [L79-95]: `def symbols_section(info, notebook)`
- **function `_deco`** [L98-99]: `def _deco(deco)`
- **function `py_page`** [L102-120]: `def py_page(path, rec, info, inn_edges)`
- **function `sh_page`** [L123-136]: `def sh_page(path, rec, info, inn_edges)`

