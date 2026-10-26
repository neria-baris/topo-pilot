# `tools/theory_exact/sym_check.py`

- Source: [tools/theory_exact/sym_check.py](../../../../../tools/theory_exact/sym_check.py)
- Kind: python
- Lines: 92

## Module docstring

> Brute-force: which grid automorphisms g admit a symbol permutation s with E[g z, s w] = E[z, w]
> and T[g i, g j] = T[i, j], for the O emission on square/cylinder (built from the formula in
> RESEARCH_PLAN §3.3, not from project code). Also P-type per-axis shuffles.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 5)

### Standard library

- `itertools` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `E`
- `N`
- `T`

## Classes and functions

- **function `dist`** [L10-14]: `def dist(x1, y1, x2, y2, periodic)`
- **function `emission`** [L17-25]: `def emission(periodic, sigma)`
- **function `transition`** [L28-42]: `def transition(periodic)`
- **function `grid_maps`** [L45-60]: `def grid_maps(periodic)`
- **function `symbol_perm`** [L63-73]: `def symbol_perm(E, g)` - s with E[g z, s(w)] == E[z, w] for all z, w, or None.

