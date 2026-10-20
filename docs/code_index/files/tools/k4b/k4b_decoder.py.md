# `tools/k4b/k4b_decoder.py`

- Source: [tools/k4b/k4b_decoder.py](../../../../../tools/k4b/k4b_decoder.py)
- Kind: python
- Lines: 117

## Module docstring

> K4b descriptive suffix decoder (API.md §5; protocol §9.4, §5.6 R13 tolerance).

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 9, via same directory)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 10, via same directory)
- `from k4b_config import SCOPE` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 12, via same directory)
- `from topo_pilot.analysis.x4f_scores import rbf_bandwidth, rbf_features, rbf_map, standardizer` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 14, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 16, via package root)
- `from topo_pilot.prediction.ridge import RidgeProbe` -> [src/topo_pilot/prediction/ridge.py](../../src/topo_pilot/prediction/ridge.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/k4b/k4b_charts.py](k4b_charts.py.md) (line 130, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 283, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 19, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 31, import)
- [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 127, import)

## Top-level constants

- `GRID`
- `SAVED`

## Classes and functions

- **function `one_hot_suffix`** [L25-30]: `def one_hot_suffix(canon32) -> np.ndarray`
- **function `equivalence_tolerance`** [L33-41]: `def equivalence_tolerance(Ft, lam, pred) -> tuple` - R13 formula: tol = max(1e-10, 64 eps kappa max|pred|), kappa of Xc'Xc + lam I.
- **function `_unavailable`** [L44-45]: `def _unavailable(reason, **extra) -> dict`
- **function `fit`** [L48-79]: `def fit(canon32, seq_ids, phi, model) -> dict` - Fit on the 2,560 non-landmark cal rows the caller passes (panels by id rank // 512).
- **function `predict_phase`** [L82-87]: `def predict_phase(dec, canon32) -> np.ndarray`
- **function `agreement`** [L90-93]: `def agreement(phi, psi, supported) -> float`
- **function `to_arrays`** [L96-101]: `def to_arrays(dec) -> dict`
- **function `from_arrays`** [L104-110]: `def from_arrays(a) -> dict`
- **function `decoder_agreement`** [L113-117]: `def decoder_agreement(ext, decoders, canon32) -> dict`

