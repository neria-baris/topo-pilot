# `tools/d2a/d2a_train.py`

- Source: [tools/d2a/d2a_train.py](../../../../../tools/d2a/d2a_train.py)
- Kind: python
- Lines: 399

## Module docstring

> D-2a training: runs, waves, children, resource supervisor, controls and meter binding
> (D2A-FROZEN-v1 §4, §10.7 S5/S6/S8, §11.3; tools/d2a/API.md §2.3).

## Imports

### Internal (repo files)

- `from topo_pilot.learner import TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 50, via package root) (inside a function)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 57, via package root) (inside a function)
- `from d2a_world import MODEL` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 69, via same directory) (inside a function)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 71, via package root) (inside a function)
- `from topo_pilot.learner import Trainer` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 72, via package root) (inside a function)
- `from topo_pilot.learner.multihorizon import MultiHorizonLM, multi_horizon_loss` -> [src/topo_pilot/learner/multihorizon.py](../../src/topo_pilot/learner/multihorizon.py.md) (line 73, via package root) (inside a function)
- `from topo_pilot.contracts import Checkpoint` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 87, via package root) (inside a function)
- `from topo_pilot.learner import serialise_state` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 88, via package root) (inside a function)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 114, via sys.path edit) (inside a function)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 216, via package root) (inside a function)
- `import d2a_world` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 266, via same directory) (inside a function)
- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 268, via package root) (inside a function)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 269, via package root) (inside a function)
- `from process_tree import TrainingProcess` -> [tools/d2a/process_tree.py](process_tree.py.md) (line 307, via same directory) (inside a function)
- `from process_tree import wave_lease` -> [tools/d2a/process_tree.py](process_tree.py.md) (line 318, via same directory) (inside a function)

### External (third-party)

- `torch` (lines 93, 253)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `functools` (lines 18)
- `hashlib` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 19)
- `shutil` (lines 14)
- `subprocess` (lines 15)
- `sys` (lines 16)
- `time` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(_p)` -> `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- [tests/d2a/test_b_resource.py](../../tests/d2a/test_b_resource.py.md) (line 33, import)
- [tests/d2a/test_b_resource.py](../../tests/d2a/test_b_resource.py.md) (line 34, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 20, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 84, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 112, import)
- [tests/d2a/test_process_tree_repair.py](../../tests/d2a/test_process_tree_repair.py.md) (line 124, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 29, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 28, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 19, import)
- [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 34, import)
- [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 252, import)
- [tools/d2a/d2a_world.py](d2a_world.py.md) (line 292, import)
- [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 42, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 32, import)

## Top-level constants

- `HERE`
- `MAILBOX`
- `MAX_WALL_S`
- `REPO`
- `ROOT`
- `RUNS`
- `STORE`
- `THREADS`
- `THREAD_VARS`
- `VENV_PY`
- `WAVES`
- `WAVE_MAX_CPU_S`
- `WAVE_STAGE`

## Classes and functions

- **class `D2AStop(RuntimeError)`** [L45-46] - STOP or INVALID control state (owner STOP, malformed control): stop at the boundary.
- **function `train_config`** [L49-53]: `def train_config()`
- **function `model_config`** [L56-59]: `def model_config()`
- **function `make_trainer`** [L67-81]: `def make_trainer(run_id: str, model_cfg=None, train_cfg=None)` - Trainer for a registered run (§4.5); H = 1 is exactly the default path.
- **function `checkpoint_callback`** [L84-109]: `def checkpoint_callback(store, obs_train_id, obs_dev_id, run_id, horizon, proc, model_cfg, train_cfg, seeds, run_key, before, after, record)` - x5g1t_train.checkpoint_callback with run_id and horizon added to the identity (§2.5).
- **function `bound_controls`** [L112-117]: `def bound_controls(out, job_id, task_sha256)` - The job-0014 controls module bound to the current dispatch identities (in this process).
- **function `boundary`** [L120-128]: `def boundary(classify, sleep=time.sleep, poll_s: float = 30.0) -> None` - Safe boundary: CONTINUE returns, HOLD waits, STOP / INVALID raise ``D2AStop``.
- **function `disk_reason`** [L131-139]: `def disk_reason(usage=shutil.disk_usage)`
- **class `Limits`** [L143-151] decorators: @dataclasses.dataclass(frozen=True)
- **function `stage_spent`** [L154-156]: `def stage_spent(ledger: dict, stage: str) -> float`
- **function `total_spent`** [L159-160]: `def total_spent(ledger: dict) -> float`
- **function `admit`** [L163-165]: `def admit(stage, spent_stage, spent_total, limits=Limits(), need_s: float = 0.0) -> bool`
- **class `Supervisor`** [L168-192] - Polling per-model CPU, per-process memory and stage/total budget enforcement (S6).
- **method `Supervisor.__init__`** [L171-173]: `def __init__(self, limits, cpu_of, mem_of, kill, clock=time.monotonic)`
- **method `Supervisor.check`** [L175-192]: `def check(self, children: dict, spent_stage: float, spent_total: float, stage: str) -> dict`
- **function `_read`** [L195-196]: `def _read(path)`
- **function `jsonable`** [L199-205]: `def jsonable(x)`
- **function `write_json`** [L208-211]: `def write_json(path, rec) -> None` - Exclusive-create JSON write of ``jsonable(rec)`` (stage records are never overwritten).
- **function `verify_identity`** [L214-236]: `def verify_identity(mailbox, job_id, task_sha256, session, lock_path) -> None` - Dispatch identities (ruling D6): request, task.json, task.md digest, RUN.lock session.
- **function `bind_meter`** [L239-249]: `def bind_meter(meter, controls, winjob, out, job_id, task_sha256, session) -> None` - Store-local rebinding of the unchanged job-0014 meter (§11.3; module names only).
- **function `_set_threads`** [L252-260]: `def _set_threads()`
- **function `child_main`** [L263-303]: `def child_main(run_id: str, store_root=STORE) -> int` - One training (CLI ``child RUN``): threads first, then train, saving every checkpoint.
- **function `_launch`** [L306-314]: `def _launch(run_id, root)`
- **function `wave_main`** [L317-321]: `def wave_main(wave: str, store_root=STORE, limits=Limits()) -> int`
- **function `_wave_main`** [L324-390]: `def _wave_main(wave: str, store_root, limits) -> int` - CLI ``wave W``: ≤ 3 children, supervised; the S5 rerun rule; waves/{W}.json.

