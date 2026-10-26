# `tools/theory_exact/check_ceiling.py`

- Source: [tools/theory_exact/check_ceiling.py](../../../../../tools/theory_exact/check_ceiling.py)
- Kind: python
- Lines: 106

## Module docstring

> Reviewer check: kappa <= Pi on the SAME cloud for every searched map (with winding), F2 vs F3
> ceilings, and attainability of Pi by a cocycle-derived (de Silva style) circular coordinate.

## Imports

### Internal (repo files)

- `from theory_exact import N, amp, build, certificate, filt, hellinger_matrix, sample` -> [tools/theory_exact/theory_exact.py](theory_exact.py.md) (line 11, via same directory)

### External (third-party)

- `numpy` (lines 6)
- `ripser` (lines 7)
- `scipy` (lines 8, 9)

### Standard library

- `json` (lines 3)
- `sys` (lines 4)

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

- none

## Classes and functions

- **function `bars`** [L14-20]: `def bars(D, p)`
- **function `cocycle_map`** [L23-54]: `def cocycle_map(D, p=47, fracs=(0.3, 0.6, 0.9, 0.99))`
- **function `run`** [L57-95]: `def run(family, n, seed)`

