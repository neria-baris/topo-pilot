# `tools/check_imports.py`

- Source: [tools/check_imports.py](../../../../tools/check_imports.py)
- Kind: python
- Lines: 109

## Module docstring

> Check import rules in src/topo_pilot (see tools/SPEC.md).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `argparse` (lines 6)
- `ast` (lines 7)
- `os` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tasks.ps1](../tasks.ps1.md) (line 13, invoke)

## Top-level constants

- `LEARNER_BANNED`
- `MODULES`
- `REPO`
- `SCIENCE`

## Classes and functions

- **function `import_paths`** [L20-43]: `def import_paths(node, root, path)` - Return the topo_pilot paths (parts after 'topo_pilot') that one import touches.
- **function `violations_for`** [L46-61]: `def violations_for(module, parts)` - Return the rule messages that importing topo_pilot.<parts> from <module> breaks.
- **function `display`** [L64-68]: `def display(path)`
- **function `scan`** [L71-87]: `def scan(root)`
- **function `main`** [L90-105]: `def main()`

