# `src/topo_pilot/experiment/s7_probes.py`

- Source: [src/topo_pilot/experiment/s7_probes.py](../../../../../../src/topo_pilot/experiment/s7_probes.py)
- Kind: python
- Lines: 133

## Module docstring

> S7 probes (D-047; RESEARCH_SUMMARY §7.7): ridge decoding of the 32-symbol belief.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 24, via package root)
- `from topo_pilot.prediction import RidgeProbe` -> [src/topo_pilot/prediction/__init__.py](../prediction/__init__.py.md) (line 25, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 27, via relative)
- `from .s4_analysis import _row` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 28, via relative)
- `from .s7_dev import DevData, ProbeData` -> [src/topo_pilot/experiment/s7_dev.py](s7_dev.py.md) (line 29, via relative)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 18)
- `logging` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 23, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 17, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 22, import)

## Top-level constants

- `CONS`

## Classes and functions

- **function `_onehot`** [L35-36]: `def _onehot(w: np.ndarray, V: int) -> np.ndarray`
- **class `ProbesJob`** [L39-133] - Writes one MetricRecords (``kind = probes``).
- **method `ProbesJob.__init__`** [L42-50]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `ProbesJob._features`** [L52-62]: `def _features(self, world, cond, seed, dev: ProbeData, test: ProbeData, V: int) -> dict`
- **method `ProbesJob.probe`** [L64-75]: `def probe(self, Xd, Yd, Xt, Yt, dev: ProbeData, test: ProbeData, shuffle_rng=None) -> tuple[RidgeProbe, dict, list[float]]`
- **method `ProbesJob.run_rows`** [L77-107]: `def run_rows(self, world: str, cond: str, seed: int) -> tuple[list[MetricRow], int]`
- **method `ProbesJob.run`** [L109-133]: `def run(self) -> list[str]`

