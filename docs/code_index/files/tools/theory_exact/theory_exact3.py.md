# `tools/theory_exact/theory_exact3.py`

- Source: [tools/theory_exact/theory_exact3.py](../../../../../tools/theory_exact/theory_exact3.py)
- Kind: python
- Lines: 140

## Module docstring

> Exact process-only computations, part 3.

## Imports

### Internal (repo files)

- `from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 20, via package root)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 21, via package root)
- `from theory_exact import N, TWO_PI, amp, build, certificate, filt, hellinger_matrix, sample` -> [tools/theory_exact/theory_exact.py](theory_exact.py.md) (line 22, via same directory)

### External (third-party)

- `numpy` (lines 17)
- `ripser` (lines 18)

### Standard library

- `json` (lines 13)
- `sys` (lines 14)
- `time` (lines 15)

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

- **function `kappa`** [L25-27]: `def kappa(D, th)`
- **function `searched_null`** [L30-65]: `def searched_null(family, n, rng, n_points=25, n_pairs=10, n_random=30, n_climb=60)`
- **function `overlap_E`** [L68-70]: `def overlap_E(family, sigma=1.25)`
- **function `prediction_certificates`** [L73-108]: `def prediction_certificates(n, rng)`
- **function `barcodes`** [L111-125]: `def barcodes(n, rng)`

