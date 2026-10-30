# `tools/hwsb/hwsb_config.py`

- Source: [tools/hwsb/hwsb_config.py](../../../../../tools/hwsb/hwsb_config.py)
- Kind: python
- Lines: 190

## Module docstring

> HWSB configuration: CONTRACT.json, constants, plans (API.md §1; protocol §2, §4, §8).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 26, via unique basename)
- `from topo_pilot.learner.config import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/config.py](../../src/topo_pilot/learner/config.py.md) (line 28, via package root)
- `from topo_pilot.process import EmissionConfig, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 29, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 30, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 11)
- `fractions` (lines 12)
- `json` (lines 9)
- `pathlib` (lines 13)
- `statistics` (lines 14)
- `sys` (lines 10)
- `typing` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> not statically determinable

## Imported by

- [tests/hwsb/test_a_capture.py](../../tests/hwsb/test_a_capture.py.md) (line 35, import)
- [tests/hwsb/test_a_enclosure_proof.py](../../tests/hwsb/test_a_enclosure_proof.py.md) (line 39, import)
- [tests/hwsb/test_a_endpoints.py](../../tests/hwsb/test_a_endpoints.py.md) (line 33, import)
- [tests/hwsb/test_a_ladder.py](../../tests/hwsb/test_a_ladder.py.md) (line 37, import)
- [tests/hwsb/test_a_learning.py](../../tests/hwsb/test_a_learning.py.md) (line 35, import)
- [tests/hwsb/test_a_outcomes.py](../../tests/hwsb/test_a_outcomes.py.md) (line 28, import)
- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 22, import)
- [tests/hwsb/test_b_hold.py](../../tests/hwsb/test_b_hold.py.md) (line 19, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 22, import)
- [tests/hwsb/test_b_process.py](../../tests/hwsb/test_b_process.py.md) (line 21, import)
- [tests/hwsb/test_b_records.py](../../tests/hwsb/test_b_records.py.md) (line 26, import)
- [tests/hwsb/test_b_registry.py](../../tests/hwsb/test_b_registry.py.md) (line 22, import)
- [tests/hwsb/test_b_streams.py](../../tests/hwsb/test_b_streams.py.md) (line 18, import)
- [tests/hwsb/test_r_0168_kb_default_store.py](../../tests/hwsb/test_r_0168_kb_default_store.py.md) (line 19, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 168, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 32, import)
- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 28, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 25, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 31, import)
- [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 10, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 9, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 10, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 7, import)
- [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 10, import)
- [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 7, import)
- [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 18, import)
- [tools/hwsb/hwsb_kb.py](hwsb_kb.py.md) (line 8, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 10, import)
- [tools/hwsb/hwsb_law.py](hwsb_law.py.md) (line 14, import)
- [tools/hwsb/hwsb_meter_bind.py](hwsb_meter_bind.py.md) (line 11, import)
- [tools/hwsb/hwsb_records.py](hwsb_records.py.md) (line 8, import)
- [tools/hwsb/hwsb_registry.py](hwsb_registry.py.md) (line 11, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 10, import)
- [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 10, import)
- [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 27, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 16, import)
- [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 19, import)

## Top-level constants

- `ADDENDUM_32_SHA`
- `ALPHA_B23`
- `ALPHA_C`
- `CONTRACT`
- `CONTRACT_PATH`
- `CPU`
- `C_MIN_FALLBACK_N`
- `DRAWS`
- `DRY_MASTERS`
- `DRY_STORE`
- `EMIS_CFG`
- `HERE`
- `HIST_NAMES`
- `HWS_STORE`
- `KEY`
- `KS`
- `LADDER`
- `LEARN`
- `M`
- `MASTERS`
- `MDE_MAX`
- `MIN_SUCCESSES`
- `MODEL_CFG`
- `NEEDLES`
- `NEIGHBOUR`
- `PANEL`
- `POWER`
- `PROCESS`
- `PROOF_PATH`
- `PROTOCOL_PATH`
- `RANKS`
- `REAL_PLAN`
- `REGISTRY_CAP`
- `REPO`
- `ROOT`
- `SCOPE`
- `SCRATCH`
- `SEEDS`
- `SIGMA`
- `SIZES`
- `STORE`
- `STUDY_LEDGER`
- `TRAIN_CFG`
- `TRANS_CFG`
- `W0_EMIS_CFG`
- `WORLD_CFG`
- `Z_B23`
- `Z_C`
- `Z_P`
- `Z_STANDIN`
- `Z_SUM`
- `_S`
- `_T`

## Classes and functions

- **function `load_contract`** [L43-44]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **class `HwsbStop(RuntimeError)`** [L50-56] - A technical or resource stop carrying a full status string (API.md §0).
- **method `HwsbStop.__init__`** [L53-56]: `def __init__(self, status: str, reason: str = '')`
- **function `_train_cfg`** [L75-78]: `def _train_cfg(d) -> TrainConfig`
- **class `Plan`** [L122-138] decorators: @dataclass(frozen=True) - One code path for the real run and the dry run (API.md §1.2, choice 2).
- **method `Plan.dry`** [L137-138]: `def dry(self) -> bool` decorators: @property
- **function `dry_plan`** [L144-184]: `def dry_plan(kind, case) -> Plan`
- **function `run_key`** [L187-190]: `def run_key(plan, master) -> tuple`

