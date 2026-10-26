# `tools/theory_exact/theory_exact.py`

- Source: [tools/theory_exact/theory_exact.py](../../../../../tools/theory_exact/theory_exact.py)
- Kind: python
- Lines: 174

## Module docstring

> Exact process-only computations for THEORY_TRACK_HE.md (owner go-ahead 2026-10-26).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.process import AxisPermuted, EmissionConfig, OverlapGaussian, TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 16, via package root)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `itertools` (lines 8)
- `json` (lines 9)
- `sys` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/theory_exact/kappa_ceiling.py](kappa_ceiling.py.md) (line 14, import)
- [tools/theory_exact/null_kappa.py](null_kappa.py.md) (line 2, import)
- [tools/theory_exact/theory_exact2.py](theory_exact2.py.md) (line 13, import)
- [tools/theory_exact/theory_exact3.py](theory_exact3.py.md) (line 22, import)

## Top-level constants

- `N`
- `TWO_PI`

## Classes and functions

- **function `build`** [L23-31]: `def build(family, mode, sigma)`
- **function `grid_maps`** [L34-44]: `def grid_maps(periodic)`
- **function `symmetry_group`** [L47-62]: `def symmetry_group(T, E, periodic)`
- **function `sample`** [L65-72]: `def sample(T, E, n, L, rng)`
- **function `filt`** [L75-81]: `def filt(T, E, W)`
- **function `hellinger_matrix`** [L84-87]: `def hellinger_matrix(P)`
- **function `certificate`** [L90-126]: `def certificate(D, theta)` - Theorem 2.1: r* and the smallest delta < r* that closes a nonzero-winding chain.
- **function `amp`** [L129-131]: `def amp(P, coord, period)`
- **function `run`** [L134-159]: `def run(family, mode, sigma, n, rng, ks=(1, 2, 4, 8, 16, 32))`

