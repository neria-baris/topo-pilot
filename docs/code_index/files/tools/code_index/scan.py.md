# `tools/code_index/scan.py`

- Source: [tools/code_index/scan.py](../../../../../tools/code_index/scan.py)
- Kind: python
- Lines: 115

## Module docstring

> Tracked-file discovery, file kinds, line counts, hashes and one-line purposes.

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `hashlib` (lines 2)
- `pathlib` (lines 5)
- `re` (lines 3)
- `subprocess` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/code_index/build.py](build.py.md) (line 8, import)
- [tools/code_index/model.py](model.py.md) (line 7, import)
- [tools/code_index/pyinfo.py](pyinfo.py.md) (line 7, import)
- [tools/code_index/render_lists.py](render_lists.py.md) (line 7, import)
- [tools/code_index/render_pages.py](render_pages.py.md) (line 5, import)

## Top-level constants

- `BINARY_EXT`
- `CODE_EXT`
- `EXCLUDE`
- `KINDS`
- `OUT_DIR`
- `REPO`
- `_FORBIDDEN_WORDS`

## Classes and functions

- **function `clean`** [L23-27]: `def clean(text)` - Remove mentions of the forbidden paths from free text copied out of sources.
- **function `list_tracked`** [L30-35]: `def list_tracked(root=REPO)`
- **function `kind_of`** [L38-47]: `def kind_of(path)`
- **function `count_lines`** [L50-51]: `def count_lines(data)`
- **function `first_heading`** [L54-63]: `def first_heading(text)`
- **function `first_comment`** [L66-82]: `def first_comment(text)`
- **function `read_file`** [L85-108]: `def read_file(root, path)` - Return a record dict (with transient `data` bytes) for one tracked file.
- **function `sources_digest`** [L111-115]: `def sources_digest(records)`

