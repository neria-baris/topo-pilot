# `tools/hwsb/hwsb_stages.py`

- Source: [tools/hwsb/hwsb_stages.py](../../../../../tools/hwsb/hwsb_stages.py)
- Kind: python
- Lines: 351

## Module docstring

> HWSB stage cores: one model's training and the EVAL gate sequence (API.md §8; protocol §4,
> §5, §6.1). Split out of hwsb_driver by size (the HWS E16 pattern); the driver adds preflight,
> authority, pauses and the CLI. A Plan argument lets the dry run use the same code.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import hws_exact` -> [tools/hws/hws_exact.py](../hws/hws_exact.py.md) (line 14, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 15, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 16, via same directory)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 17, via same directory)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 18, via same directory)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](hwsb_law.py.md) (line 19, via same directory)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 20, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 21, via unique basename)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 22, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 23, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import Checkpoint` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 77, via same directory) (inside a function)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 304, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 8)
- `pathlib` (lines 12)
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

- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 20, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 32, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 26, import)

## Top-level constants

- none

## Classes and functions

- **function `_gate`** [L30-31]: `def _gate(out, gate, status, **details) -> str`
- **function `train_core`** [L34-61]: `def train_core(out, store, proc, master, plan=hc.REAL_PLAN, hold=None) -> dict` - make_train_dev, then ht.train; TRAIN_RECORD.json (also written on a stop).
- **function `_ckpt`** [L64-68]: `def _ckpt(store, rec, step) -> Checkpoint`
- **function `_acts`** [L71-73]: `def _acts(store, rec, step, canon32, perm, plan) -> np.ndarray`
- **function `_cpu_by_model`** [L76-82]: `def _cpu_by_model(ledger_path, masters) -> dict`
- **function `eval_core`** [L85-351]: `def eval_core(out, plan, proc, store, train_records, hws_digests=None, p_d2a_ref=None, kb4_z=None, ledger_path=None, pause=None, freeze_sha256=None) -> dict` - Every EVAL gate in the §4 order; gates are computed whatever an earlier decision gave.

