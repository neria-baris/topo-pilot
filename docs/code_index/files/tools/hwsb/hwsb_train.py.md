# `tools/hwsb/hwsb_train.py`

- Source: [tools/hwsb/hwsb_train.py](../../../../../tools/hwsb/hwsb_train.py)
- Kind: python
- Lines: 325

## Module docstring

> HWSB training: Trainer.fit with a LearnerStage-mirroring callback, threads, the hold rule
> and the KB2/KB3 known-case harness (API.md §3; protocol §2.1 item 3, §3 KB2/KB3, §8.2 RC-14).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 17, via unique basename)
- `from topo_pilot.contracts import Checkpoint, ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure, payload_checksum` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 29, via package root)
- `from topo_pilot.learner import Trainer` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 30, via package root)
- `from topo_pilot.learner.stage import serialise_state` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 31, via package root)

### External (third-party)

- `torch` (lines 18)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 15)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 26, import)
- [tests/hwsb/test_b_hold.py](../../tests/hwsb/test_b_hold.py.md) (line 22, import)
- [tests/hwsb/test_r_0170_kb2_status.py](../../tests/hwsb/test_r_0170_kb2_status.py.md) (line 20, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 21, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 27, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 22, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 19, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 20, import)

## Top-level constants

- `KNOWN`

## Classes and functions

- **function `_plain`** [L36-41]: `def _plain(x)`
- **function `check_recipe`** [L44-53]: `def check_recipe(model_cfg, train_cfg, reference=None) -> dict`
- **function `set_threads`** [L56-67]: `def set_threads(n) -> dict`
- **function `torch_versions`** [L70-78]: `def torch_versions(repo=hc.REPO) -> dict`
- **class `SentinelStop(Exception)`** [L81-86] - Raised by the checkpoint callback to stop training after a step (KB2, KB3).
- **method `SentinelStop.__init__`** [L84-86]: `def __init__(self, step)`
- **function `build_checkpoint`** [L89-98]: `def build_checkpoint(step, model, info, run_id, observation_id, model_cfg, train_cfg)`
- **class `CheckpointSaver`** [L101-164] - The on_checkpoint callback: LearnerStage's save, then the hold, then a sentinel.
- **method `CheckpointSaver.__init__`** [L104-132]: `def __init__(self, store, obs_train_id, obs_dev_id, model_cfg, train_cfg, seeds, run_key, *, observation_id=None, run_id=None, hold=None, stop_after=None)`
- **method `CheckpointSaver.__call__`** [L134-164]: `def __call__(self, step, model, info) -> None`
- **function `hold_check`** [L167-187]: `def hold_check(step, cpu_s, steps=5000, cap_s=7275.0, from_step=1000) -> dict`
- **class `HoldRule`** [L190-234] - The RC-14 hold: write HOLD_<step>.json, poll DECISION_<step>.json with sleep.
- **method `HoldRule.__init__`** [L193-206]: `def __init__(self, out_dir, cap_s=7275.0, steps=5000, from_step=1000, cpu_fn=time.process_time, poll_s=30.0, sleep=time.sleep)`
- **method `HoldRule.__call__`** [L208-234]: `def __call__(self, step)`
- **function `_datasets`** [L237-239]: `def _datasets(train_obs, dev_obs) -> tuple`
- **function `_fit`** [L242-248]: `def _fit(trainer, train, dev, saver)`
- **function `_summary`** [L251-262]: `def _summary(s) -> dict`
- **function `train`** [L265-283]: `def train(store, obs_ids, master, plan=hc.REAL_PLAN, hold=None, seeds=None) -> dict` - LearnerStage.run, composed: same loads, datasets, Trainer and checkpoint identities.
- **function `train_known`** [L286-325]: `def train_known(obs_train, obs_dev, master, run_key, run_id, observation_id, stop_after, threads, model_cfg=hc.MODEL_CFG, train_cfg=hc.TRAIN_CFG) -> dict` - KB2/KB3: in-memory ObservationSets, stopped by a sentinel; nothing persisted.

