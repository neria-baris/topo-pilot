# `tools/hwsb/hwsb_kb.py`

- Source: [tools/hwsb/hwsb_kb.py](../../../../../tools/hwsb/hwsb_kb.py)
- Kind: python
- Lines: 158

## Module docstring

> HWSB known cases KB5-KB7 (API.md §7; protocol §3). Split out of hwsb_known by size;
> hwsb_known re-exports kb5, kb6 and kb7. KB5 reads the AUTH-named S3 w* history table of
> hws-store (sha256-checked); KB6 regenerates the E4 test split in memory only.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 8, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 11, via unique basename)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../hws/hws_oracle.py.md) (line 12, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 13, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 14, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 16, via unique basename)
- `from hwsb_known import E4, KC, KNOWN, _ck, _e4_obs, _ok, _read_json` -> [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 17, via same directory)
- `from topo_pilot.activations import ActivationExtractor` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset import DatasetConfig, PanelBuilder` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 21, via package root)
- `from topo_pilot.oracle import BayesFilter, LastSymbolPosterior, context_gain` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 22, via package root)
- `from topo_pilot.prediction.metrics import PredictiveMetrics` -> [src/topo_pilot/prediction/metrics.py](../../src/topo_pilot/prediction/metrics.py.md) (line 23, via package root)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 128, via unique basename) (inside a function)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 129, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 350, import)
- [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 16, import)

## Top-level constants

- none

## Classes and functions

- **function `kb5`** [L26-67]: `def kb5(proc_star) -> dict`
- **function `_src_path`** [L70-81]: `def _src_path(proc_w0, obs, index, ckpt)`
- **function `kb6`** [L84-124]: `def kb6(proc_w0, ckpt100) -> dict`
- **function `kb7`** [L127-155]: `def kb7(proc_star, val) -> dict`

