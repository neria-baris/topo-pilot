# `src/topo_pilot/experiment/x5g1t_runtime.py`

- Source: [src/topo_pilot/experiment/x5g1t_runtime.py](../../../../../../src/topo_pilot/experiment/x5g1t_runtime.py)
- Kind: python
- Lines: 246

## Module docstring

> X5 G1 training-study runtime controls (x5g1-train-v4 §8–§9; API v4 §2).

## Imports

### Internal (repo files)

- `from .x4b_run import peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 22, via relative)
- `from .x5g1_controls import BudgetExceeded, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 23, via relative)
- `from .x5g1_safety import OutputExists` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 24, via relative)
- `from .x5g1t_usage import UsageMalformed, apply_usage` -> [src/topo_pilot/experiment/x5g1t_usage.py](x5g1t_usage.py.md) (line 25, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 12)
- `collections` (lines 17)
- `datetime` (lines 18)
- `json` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 19)
- `time` (lines 16)
- `typing` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_exports.py](x5g1t_exports.py.md) (line 17, import)
- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 28, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 52, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 59, import)
- [src/topo_pilot/experiment/x5g1t_train.py](x5g1t_train.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_export_checks.py](../../../tests/experiment/test_x5g1t_export_checks.py.md) (line 19, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 19, import)
- [tests/experiment/test_x5g1t_runtime.py](../../../tests/experiment/test_x5g1t_runtime.py.md) (line 18, import)
- [tests/experiment/test_x5g1t_runtime_boundary.py](../../../tests/experiment/test_x5g1t_runtime_boundary.py.md) (line 20, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_usage_files.py](../../../tests/experiment/test_x5g1t_usage_files.py.md) (line 69, import)

## Top-level constants

- `AUDIT_KIND`
- `CONTINUE_MODES`
- `EST`
- `HOLD_MODES`
- `MAX_POLL_S`

## Classes and functions

- **class `ControlState(NamedTuple)`** [L35-37]
- **class `RunLocked(RuntimeError)`** [L40-41] - A run lock or an outcome already exists; a second start is refused (no retry).
- **class `ResourceExceeded(RuntimeError)`** [L44-45] - Peak RAM or new-output storage over its cap, or peak RAM unknown (fail closed).
- **function `_json`** [L48-49]: `def _json(path: Path)`
- **function `read_controls`** [L52-100]: `def read_controls(mailbox: Path, now: datetime | None = None) -> ControlState` - Precedence STOP > HOLD > CONTINUE (API v4 §2): STOP file, request, worker_control,
- **function `_atomic_json`** [L103-108]: `def _atomic_json(path: Path, obj) -> None`
- **function `_utc`** [L111-112]: `def _utc() -> str`
- **function `hold_while_needed`** [L115-136]: `def hold_while_needed(mailbox: Path, audit_path: Path, audit: Callable[[], dict], sleep: Callable[[float], None] | None = None, poll_s: float = MAX_POLL_S) -> int` - Hold the live process until controls say CONTINUE; STOP raises. Returns held polls.
- **class `RunLock`** [L139-157] - Exclusive lock file for one live model run; removed on exit, never suppresses errors.
- **method `RunLock.__init__`** [L142-143]: `def __init__(self, path: Path, identity: dict) -> None`
- **method `RunLock.__enter__`** [L145-153]: `def __enter__(self) -> RunLock`
- **method `RunLock.__exit__`** [L155-157]: `def __exit__(self, exc_type, exc, tb) -> bool`
- **function `outcome_path`** [L160-161]: `def outcome_path(root: Path, arm: str, master) -> Path`
- **function `read_outcome`** [L164-166]: `def read_outcome(root: Path, arm: str, master) -> dict | None`
- **function `record_outcome`** [L169-174]: `def record_outcome(root: Path, arm: str, master, outcome: dict) -> Path`
- **function `assert_can_start`** [L177-181]: `def assert_can_start(root: Path, arm: str, master, lock_path: Path) -> None`
- **class `BudgetPlanner`** [L184-195] - Proceed iff ``cumulative + factor * next_estimate + reserve <= cap``.
- **method `BudgetPlanner.__init__`** [L187-188]: `def __init__(self, cap_s: float = 21600.0, factor: float = 1.5) -> None`
- **method `BudgetPlanner.check`** [L190-195]: `def check(self, cumulative_now: float, next_estimate: float, reserve: float, what: str) -> None`
- **function `interval_estimate`** [L198-199]: `def interval_estimate(updates: int, est: dict = EST) -> float`
- **function `evaluation_reserve`** [L202-205]: `def evaluation_reserve(unscored_checkpoints: int, unscored_final: int, est: dict = EST, factor: float = 1.5) -> float`
- **function `dir_size`** [L208-210]: `def dir_size(path: Path) -> int`
- **function `check_resources`** [L213-220]: `def check_resources(peak_bytes: int | None, storage_bytes: int, ram_cap: int = 8 * 2 ** 30, storage_cap: int = 2 * 2 ** 30) -> None`
- **class `StudyControls`** [L223-246] - Guard, controls (with live hold), boundary budget and resources at one boundary.
- **method `StudyControls.__init__`** [L226-232]: `def __init__(self, ctl: RunControls, mailbox: Path, planner: BudgetPlanner, out_root: Path, audit_path: Path, sleep: Callable[[float], None] | None = None, poll_s: float = MAX_POLL_S) -> None`
- **method `StudyControls.boundary`** [L234-246]: `def boundary(self, what: str, next_estimate: float, reserve: float, audit: Callable[[], dict] = dict) -> None`

