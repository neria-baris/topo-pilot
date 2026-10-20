# `tools/code_index/pyinfo.py`

- Source: [tools/code_index/pyinfo.py](../../../../../tools/code_index/pyinfo.py)
- Kind: python
- Lines: 210

## Module docstring

> AST extraction for one Python source: docstring, imports, sys.path edits, symbols.

## Imports

### Internal (repo files)

- `from .pathval import evaluate, iter_nodes, norm` -> [tools/code_index/pathval.py](pathval.py.md) (line 6, via relative)
- `from .scan import clean` -> [tools/code_index/scan.py](scan.py.md) (line 7, via relative)

### External (third-party)

- none

### Standard library

- `ast` (lines 2)
- `json` (lines 3)
- `re` (lines 4)

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

- `CONST_RE`
- `DYN_FUNCS`

## Classes and functions

- **function `notebook_source`** [L13-24]: `def notebook_source(data)` - Concatenate code cells (magics blanked) of a notebook; best effort.
- **function `args_str`** [L27-50]: `def args_str(a)`
- **function `signature`** [L53-58]: `def signature(node)`
- **function `doc_first_line`** [L61-68]: `def doc_first_line(node)`
- **function `first_paragraph`** [L71-73]: `def first_paragraph(doc, limit=1500)`
- **class `Collector`** [L76-154] - Single pass over a module collecting imports, dynamic imports and sys.path edits.
- **method `Collector.__init__`** [L79-93]: `def __init__(self, tree, path, dirset)`
- **method `Collector.visit`** [L95-115]: `def visit(self, node, lazy)`
- **method `Collector.add_syspath`** [L117-123]: `def add_syspath(self, node, expr)`
- **method `Collector.fallback`** [L125-134]: `def fallback(self, expr)`
- **method `Collector.call`** [L136-154]: `def call(self, node)`
- **function `symbols`** [L157-191]: `def symbols(tree, path)`
- **function `extract`** [L194-210]: `def extract(path, data, dirset, is_notebook=False)`

