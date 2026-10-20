# `tools/chart_diag/chart_diag.py`

- Source: [tools/chart_diag/chart_diag.py](../../../../../tools/chart_diag/chart_diag.py)
- Kind: python
- Lines: 249

## Module docstring

> Geometry-only chart diagnostic (CHART-DIAG-FROZEN-v1; job 0023; owner decision A1).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 32, via sys.path edit)
- `from cochain import edge_list` -> [tools/x4_circle_history/cochain.py](../x4_circle_history/cochain.py.md) (line 33, via sys.path edit)
- `from adapter import E4Manifest, RestrictedE4Adapter` -> [tools/x4_circle_history/adapter.py](../x4_circle_history/adapter.py.md) (line 127, via sys.path edit) (inside a function)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 129, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 130, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 22)
- `scipy` (lines 23, 24)

### Standard library

- `__future__` (lines 14)
- `hashlib` (lines 16)
- `json` (lines 17)
- `pathlib` (lines 20)
- `sys` (lines 18)
- `time` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 30: `str(_p)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/chart_diag/test_chart_diag.py](../../tests/chart_diag/test_chart_diag.py.md) (line 15, import)

## Top-level constants

- `K4`
- `K4_STORE`
- `OWNER_SHA`
- `REPO`
- `REUSED`
- `SPEC_SHA`

## Classes and functions

- **function `sha`** [L46-47]: `def sha(path) -> str`
- **function `components`** [L50-60]: `def components(D, r)` - Connected components of the 1-skeleton {i < j : D[i, j] <= r} (cochain.edge_list rule).
- **function `x_interval`** [L63-66]: `def x_interval(l_max, d)` - X's interval [l_max, d): descriptive only.
- **function `verdict`** [L69-73]: `def verdict(fractions, invalid=False)` - Mechanical rule (fixed in the spec): GO iff every giant fraction >= 0.95.
- **function `geometry`** [L76-123]: `def geometry(X, ids)` - The frozen K4 path to bar selection, then the diagnostic readouts.
- **function `_adapter`** [L126-135]: `def _adapter()`
- **function `integrity`** [L138-159]: `def integrity()` - Reused K4 files must equal the frozen K4 build (FREEZE.json); record the 0018 evidence.
- **function `run`** [L162-208]: `def run(out_dir)`
- **function `_row`** [L211-228]: `def _row(name, c) -> str`
- **function `markdown`** [L231-245]: `def markdown(rep) -> str`

