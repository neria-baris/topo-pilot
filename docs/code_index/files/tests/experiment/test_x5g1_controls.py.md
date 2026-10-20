# `tests/experiment/test_x5g1_controls.py`

- Source: [tests/experiment/test_x5g1_controls.py](../../../../../tests/experiment/test_x5g1_controls.py)
- Kind: python
- Lines: 193

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, MemoryBackend, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 18, via package root)
- `from topo_pilot.experiment.x5g1_controls import BudgetExceeded, RunControls, StopRequested, verify_parents` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 19, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 8)
- `json` (lines 10)
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

- none

## Top-level constants

- `ENTRY_KEYS`

## Classes and functions

- **function `_burn`** [L31-36]: `def _burn(seconds: float = 0.05) -> None` - Spend at least ``seconds`` of process CPU time.
- **function `_rc`** [L39-40]: `def _rc(tmp: Path, *, cap_s=3600.0, cum_cap=3600.0, job='unit') -> RunControls`
- **function `_ledger`** [L43-44]: `def _ledger(tmp: Path) -> dict`
- **test `test_ledger_written_on_normal_exit`** [L47-60]: `def test_ledger_written_on_normal_exit(tmp_path)`
- **test `test_ledger_written_on_exception_and_exception_propagates`** [L63-70]: `def test_ledger_written_on_exception_and_exception_propagates(tmp_path)`
- **test `test_ledger_written_on_stage_failure`** [L73-78]: `def test_ledger_written_on_stage_failure(tmp_path)`
- **test `test_stop_requested_mid_run`** [L81-90]: `def test_stop_requested_mid_run(tmp_path)`
- **test `test_budget_exceeded_per_run`** [L93-102]: `def test_budget_exceeded_per_run(tmp_path)`
- **test `test_cumulative_accumulates_and_is_never_reset`** [L105-115]: `def test_cumulative_accumulates_and_is_never_reset(tmp_path)`
- **test `test_prior_cumulative_is_kept`** [L118-127]: `def test_prior_cumulative_is_kept(tmp_path)`
- **test `test_cumulative_cap_exceeded`** [L130-139]: `def test_cumulative_cap_exceeded(tmp_path)`
- **test `test_missing_ledger_starts_at_zero`** [L142-148]: `def test_missing_ledger_starts_at_zero(tmp_path)`
- **function `store_and_id`** [L155-159]: `def store_and_id()` decorators: @pytest.fixture()
- **test `test_verify_parents_matching_prefix`** [L162-167]: `def test_verify_parents_matching_prefix(store_and_id)`
- **test `test_verify_parents_wrong_prefix`** [L170-175]: `def test_verify_parents_wrong_prefix(store_and_id)`
- **test `test_verify_parents_missing_id_never_raises`** [L178-184]: `def test_verify_parents_missing_id_never_raises(store_and_id)`
- **test `test_verify_parents_backend_error_never_raises`** [L187-193]: `def test_verify_parents_backend_error_never_raises()`

