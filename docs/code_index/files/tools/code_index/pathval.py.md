# `tools/code_index/pathval.py`

- Source: [tools/code_index/pathval.py](../../../../../tools/code_index/pathval.py)
- Kind: python
- Lines: 157

## Module docstring

> Best-effort static evaluation of path expressions (used for sys.path and dynamic imports).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `ast` (lines 6)
- `copy` (lines 7)
- `itertools` (lines 8)
- `posixpath` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/code_index/pyinfo.py](pyinfo.py.md) (line 6, import)

## Top-level constants

- `MAX_ALT`
- `PASS_FUNCS`
- `PASS_METHODS`
- `PATH_CTORS`

## Classes and functions

- **function `norm`** [L17-22]: `def norm(text)`
- **function `_join`** [L25-32]: `def _join(parts)`
- **function `_cap`** [L35-40]: `def _cap(values)`
- **function `_parent`** [L43-46]: `def _parent(path)`
- **class `_Subst(ast.NodeTransformer)`** [L49-54]
- **method `_Subst.__init__`** [L50-51]: `def __init__(self, name, value)`
- **method `_Subst.visit_Name`** [L53-54]: `def visit_Name(self, node)`
- **function `iter_nodes`** [L57-72]: `def iter_nodes(node, env, depth=0)` - Element nodes of a literal iterable (directly, through a Name, `+`, or a comprehension).
- **function `_args`** [L75-86]: `def _args(call, env, fpath, depth)` - Argument sequences (each a list of alternative-lists); starred literals are expanded.
- **function `evaluate`** [L89-136]: `def evaluate(node, env, fpath, depth=0)`
- **function `_call`** [L139-157]: `def _call(node, env, fpath, depth, ev)`

