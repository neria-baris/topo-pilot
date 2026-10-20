# `tests/experiment/test_x5g1t_runtime_boundary.py`

- Source: [tests/experiment/test_x5g1t_runtime_boundary.py](../../../../../tests/experiment/test_x5g1t_runtime_boundary.py)
- Kind: python
- Lines: 373

## Module docstring

> Independent tests written from the API contract only (X5_G1_TRAINING_API.md §5 and §8
> "Runtime"; protocol x5g1-train-v3 §8-§9), before reading ``x5g1t_runtime``.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x4b_run` -> [src/topo_pilot/experiment/x4b_run.py](../../src/topo_pilot/experiment/x4b_run.py.md) (line 19, via package root)
- `from topo_pilot.experiment import x5g1t_runtime` -> [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md) (line 20, via package root)
- `from topo_pilot.experiment.x5g1_controls import BudgetExceeded, LedgerCorrupt, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 21, via package root)
- `from topo_pilot.experiment.x5g1_safety import OutputExists` -> [src/topo_pilot/experiment/x5g1_safety.py](../../src/topo_pilot/experiment/x5g1_safety.py.md) (line 27, via package root)

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 10)
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

- none

## Top-level constants

- `EST`
- `GIB`
- `PRIOR`

## Classes and functions

- **test `test_runlock_is_exclusive_and_removed`** [L40-54]: `def test_runlock_is_exclusive_and_removed(tmp_path: Path) -> None`
- **test `test_runlock_refuses_stale_lock_of_unknown_state`** [L57-63]: `def test_runlock_refuses_stale_lock_of_unknown_state(tmp_path: Path) -> None`
- **test `test_runlock_removed_on_error_and_never_suppresses`** [L66-76]: `def test_runlock_removed_on_error_and_never_suppresses(tmp_path: Path) -> None`
- **test `test_outcome_path_and_roundtrip`** [L79-87]: `def test_outcome_path_and_roundtrip(tmp_path: Path) -> None`
- **test `test_record_outcome_refuses_overwrite`** [L90-98]: `def test_record_outcome_refuses_overwrite(tmp_path: Path) -> None`
- **test `test_assert_can_start`** [L101-113]: `def test_assert_can_start(tmp_path: Path) -> None`
- **test `test_est_constants_and_defaults`** [L119-122]: `def test_est_constants_and_defaults() -> None`
- **test `test_check_boundary_equal_passes_above_raises`** [L125-134]: `def test_check_boundary_equal_passes_above_raises() -> None`
- **test `test_factor_is_applied_to_estimate_only`** [L137-146]: `def test_factor_is_applied_to_estimate_only() -> None`
- **test `test_interval_estimate`** [L149-155]: `def test_interval_estimate() -> None`
- **test `test_evaluation_reserve`** [L158-167]: `def test_evaluation_reserve() -> None`
- **test `test_realistic_boundary_with_prior_ledger`** [L170-178]: `def test_realistic_boundary_with_prior_ledger() -> None`
- **test `test_check_resources_caps`** [L184-198]: `def test_check_resources_caps() -> None`
- **test `test_dir_size`** [L201-211]: `def test_dir_size(tmp_path: Path) -> None`
- **function `env`** [L218-233]: `def env(tmp_path: Path, monkeypatch)` decorators: @pytest.fixture - Prior ledger (17.016 s), an allowing mailbox and deterministic, small resource use.
- **function `_ctl`** [L236-238]: `def _ctl(env) -> RunControls`
- **function `_study`** [L241-243]: `def _study(env, ctl, planner=None) -> rt.StudyControls`
- **function `_last`** [L246-250]: `def _last(env) -> dict`
- **test `test_boundary_continue_records_guard_step`** [L253-259]: `def test_boundary_continue_records_guard_step(env) -> None`
- **test `test_boundary_planner_sees_prior_plus_cpu`** [L262-274]: `def test_boundary_planner_sees_prior_plus_cpu(env) -> None`
- **test `test_boundary_stop_file`** [L277-282]: `def test_boundary_stop_file(env) -> None`
- **test `test_boundary_request_stop`** [L285-290]: `def test_boundary_request_stop(env) -> None`
- **function `_inject_sleep`** [L293-314]: `def _inject_sleep(monkeypatch, on_sleep) -> list` - Contract ambiguity: StudyControls takes no ``sleep``; patch the module-level
- **test `test_boundary_hold_then_release_proceeds`** [L317-331]: `def test_boundary_hold_then_release_proceeds(env, monkeypatch) -> None`
- **test `test_boundary_stop_while_held`** [L334-341]: `def test_boundary_stop_while_held(env, monkeypatch) -> None`
- **test `test_boundary_budget_exceeded`** [L344-349]: `def test_boundary_budget_exceeded(env) -> None`
- **test `test_boundary_budget_includes_prior`** [L352-356]: `def test_boundary_budget_includes_prior(env) -> None`
- **test `test_boundary_resources_fail_closed`** [L359-364]: `def test_boundary_resources_fail_closed(env) -> None`
- **test `test_corrupt_ledger_raises_and_keeps_bytes`** [L367-373]: `def test_corrupt_ledger_raises_and_keeps_bytes(env) -> None`

