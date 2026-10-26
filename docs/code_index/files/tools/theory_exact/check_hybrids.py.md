# `tools/theory_exact/check_hybrids.py`

- Source: [tools/theory_exact/check_hybrids.py](../../../../../tools/theory_exact/check_hybrids.py)
- Kind: python
- Lines: 69

## Module docstring

> Reviewer check of section 5.7: for all 8 hybrid cells, map-free ceilings Pi of belief and
> prediction clouds, belief kappa (world x-phase), prediction kappa with the symbol-column map, and a
> prediction map defined through the WORLD state (linear readout of the next-state x-phase from
> sqrt(q), fitted on an independent training cloud).

## Imports

### Internal (repo files)

- `from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 11, via package root)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 12, via package root)
- `from theory_exact import N, amp, build, certificate, filt, hellinger_matrix, sample` -> [tools/theory_exact/theory_exact.py](theory_exact.py.md) (line 13, via same directory)

### External (third-party)

- `numpy` (lines 8)
- `ripser` (lines 9)

### Standard library

- `json` (lines 5)
- `sys` (lines 6)

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

- **function `kap`** [L16-18]: `def kap(D, th)`
- **function `Pi`** [L21-24]: `def Pi(D)`
- **function `cell`** [L27-53]: `def cell(world, chart, permuted, n, rng)`

