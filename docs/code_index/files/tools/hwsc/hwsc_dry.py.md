# `tools/hwsc/hwsc_dry.py`

- Source: [tools/hwsc/hwsc_dry.py](../../../../../tools/hwsc/hwsc_dry.py)
- Kind: python
- Lines: 326

## Module docstring

> HWSC synthetic dry run: run_dry and DRC1-DRC4 (API.md §8; protocol §7; ruling R-0176-G3).
> DRC5-DRC14 live in hwsc_dry2 (split by size). Streams only under the dry scopes, masters
> 629911-629913, seeds DRY_SEEDS (620311/620315 only on DRC6's synthetic arrays, R-0176-G5);
> persisted histories only from the tiny world (DRYHIST_ names); w* rows stay in memory.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 8, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 15, via unique basename)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 16, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 17, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../hwsb/hwsb_dry.py.md) (line 18, via unique basename)
- `import hwsb_dry2` -> [tools/hwsb/hwsb_dry2.py](../hwsb/hwsb_dry2.py.md) (line 19, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 20, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 21, via same directory)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 22, via same directory)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 23, via same directory)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 24, via same directory)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 25, via same directory)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 26, via same directory)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 27, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 28, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 29, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 31, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 33, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 34, via package root)
- `from topo_pilot.learner.stage import LearnerStage` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 35, via package root)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 135, via unique basename) (inside a function)
- `from hwsc_jobs import run_close` -> [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 161, via same directory) (inside a function)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 181, via unique basename) (inside a function)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 182, via unique basename) (inside a function)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 183, via unique basename) (inside a function)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 184, via unique basename) (inside a function)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 243, via same directory) (inside a function)
- `import hwsc_dry2` -> [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 298, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 30)

### Standard library

- `__future__` (lines 6)
- `dataclasses` (lines 215)
- `fractions` (lines 12)
- `json` (lines 9)
- `pathlib` (lines 13)
- `time` (lines 10)
- `traceback` (lines 11)
- `types` (lines 241)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 23, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 183, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 26, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 180, import)

## Top-level constants

- `REGISTERED`

## Classes and functions

- **function `_registered`** [L40-41]: `def _registered(s) -> bool`
- **function `case_dir`** [L44-47]: `def case_dir(out, case) -> Path`
- **function `_mem`** [L50-51]: `def _mem()`
- **function `build_tiny_process_c`** [L54-55]: `def build_tiny_process_c(store, masters=cc.DRY_MASTERS) -> dict`
- **function `_stub`** [L58-61]: `def _stub(digests=(), status='PASS')`
- **function `synthetic_root`** [L64-70]: `def synthetic_root(base) -> dict` - A synthetic project root and scratch root (never the real ones; S2).
- **function `stub_sources`** [L73-86]: `def stub_sources(extra_digests=()) -> dict` - Synthetic replacements for the sources that need the real stores (DRC1, DRC9).
- **function `_train_tiny`** [L90-104]: `def _train_tiny(d, store, proc, plan) -> dict`
- **function `drc1`** [L107-176]: `def drc1(out, ctx) -> dict`
- **function `e4_eval_check_c`** [L180-208]: `def e4_eval_check_c(store, ckpt_id, proc, m, plan_b, case_dir_) -> dict`
- **function `drc2`** [L211-236]: `def drc2(out, ctx) -> dict`
- **function `drc3`** [L240-268]: `def drc3(out, ctx) -> dict`
- **function `drc4`** [L271-293]: `def drc4(out, ctx) -> dict`
- **function `run_dry`** [L297-326]: `def run_dry(out=None, sched=None, only=None) -> dict`

