# `tools/theory_exact/theory_exact2.py`

- Source: [tools/theory_exact/theory_exact2.py](../../../../../tools/theory_exact/theory_exact2.py)
- Kind: python
- Lines: 136

## Module docstring

> Exact process-only computations, part 2.

## Imports

### Internal (repo files)

- `from theory_exact import N, TWO_PI, build, filt, hellinger_matrix, sample` -> [tools/theory_exact/theory_exact.py](theory_exact.py.md) (line 13, via same directory)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root) (inside a function)
- `from topo_pilot.process import EmissionConfig, OverlapGaussian` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 24, via package root) (inside a function)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 25, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `json` (lines 9)

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

- **function `isotypic`** [L16-43]: `def isotypic(n, rng)`
- **function `lattice`** [L46-70]: `def lattice(periodic_x, periodic_y, sigma=1.25)`
- **function `rank_certificate`** [L73-116]: `def rank_certificate(D, thetas)` - Largest rank of winding vectors over cycles of the graph {d < delta}, as delta grows to
- **function `topo`** [L119-129]: `def topo(n, rng)`

