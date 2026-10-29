# `tools/hwsb/hwsb_dry.py`

- Source: [tools/hwsb/hwsb_dry.py](../../../../../tools/hwsb/hwsb_dry.py)
- Kind: python
- Lines: 385

## Module docstring

> HWSB synthetic dry run DRB1-DRB16 and DRB13b (API.md §9; TEST_PLAN §4; protocol §7).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../hws/hws_worlds.py.md) (line 19, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 20, via same directory)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 21, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 22, via same directory)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 23, via same directory)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 24, via same directory)
- `import hwsb_records` -> [tools/hwsb/hwsb_records.py](hwsb_records.py.md) (line 25, via same directory)
- `import hwsb_stages` -> [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 26, via same directory)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 27, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 29, via unique basename)
- `from topo_pilot.activations import ActivationExtractor` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 31, via package root)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, MemoryBackend, ObservationSet, SeedTree, SequenceLayout, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 32, via package root)
- `from topo_pilot.dataset import DatasetConfig, DatasetStage, PanelBuilder` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 43, via package root)
- `from topo_pilot.learner import LearnerStage, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 44, via package root)
- `from topo_pilot.process import TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 45, via package root)
- `from topo_pilot.process._diagnostics import emission_diagnostics` -> [src/topo_pilot/process/_diagnostics.py](../../src/topo_pilot/process/_diagnostics.py.md) (line 46, via package root)
- `from topo_pilot.process.stage import ProcessStage` -> [src/topo_pilot/process/stage.py](../../src/topo_pilot/process/stage.py.md) (line 47, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 48, via package root)
- `from topo_pilot.world.stage import WorldStage` -> [src/topo_pilot/world/stage.py](../../src/topo_pilot/world/stage.py.md) (line 49, via package root)
- `import hwsb_dry2` -> [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 155, via same directory) (inside a function)
- `import hwsb_dry2` -> [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 344, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 28)
- `torch` (lines 242)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 11)
- `fractions` (lines 16)
- `json` (lines 12)
- `pathlib` (lines 17)
- `shutil` (lines 13)
- `subprocess` (lines 14)
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

- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 24, import)
- [tests/hwsb/test_b_hold.py](../../tests/hwsb/test_b_hold.py.md) (line 21, import)
- [tests/hwsb/test_b_process.py](../../tests/hwsb/test_b_process.py.md) (line 23, import)
- [tests/hwsb/test_b_records.py](../../tests/hwsb/test_b_records.py.md) (line 28, import)
- [tests/hwsb/test_b_registry.py](../../tests/hwsb/test_b_registry.py.md) (line 24, import)
- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 30, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 27, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 32, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 310, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 29, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 18, import)

## Top-level constants

- `CASES`
- `CASE_NAMES`
- `FIX`

## Classes and functions

- **function `build_tiny_process`** [L54-87]: `def build_tiny_process(store, masters=hc.DRY_MASTERS) -> dict`
- **function `_res`** [L90-91]: `def _res(ok, **details) -> dict`
- **function `_dir`** [L94-97]: `def _dir(out, case) -> Path`
- **function `_fs`** [L100-101]: `def _fs(d) -> ArtifactStore`
- **function `_mem`** [L104-105]: `def _mem() -> ArtifactStore`
- **function `_tiny_plan`** [L108-117]: `def _tiny_plan(case, steps=None, ckpts=None, sizes=None)`
- **function `drb1`** [L120-135]: `def drb1(out, ctx) -> dict`
- **function `drb2`** [L138-158]: `def drb2(out, ctx) -> dict`
- **function `drb3`** [L161-196]: `def drb3(out, ctx) -> dict`
- **function `drb4`** [L199-214]: `def drb4(out, ctx) -> dict`
- **function `_dirichlet`** [L217-218]: `def _dirichlet(rng, n, V=36) -> np.ndarray`
- **function `drb5`** [L221-238]: `def drb5(out, ctx) -> dict`
- **function `drb6`** [L241-265]: `def drb6(out, ctx) -> dict`
- **function `_embed`** [L268-270]: `def _embed(rng, th, B, noise=0.01) -> np.ndarray`
- **function `drb7`** [L273-306]: `def drb7(out, ctx) -> dict`
- **function `_tiny_store`** [L309-318]: `def _tiny_store(d, case, sizes=None, steps=None)`
- **function `run_dry`** [L343-385]: `def run_dry(out=hc.DRY_STORE, sched=None, only=None) -> dict`

