# `tests/experiment/test_x5g1_safety.py`

- Source: [tests/experiment/test_x5g1_safety.py](../../../../../tests/experiment/test_x5g1_safety.py)
- Kind: python
- Lines: 399

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_REPAIR_API.md before
> reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MemoryBackend, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.experiment.x5g1_controls import BudgetExceeded, LedgerCorrupt, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 18, via package root)
- `from topo_pilot.experiment.x5g1_safety import OutputExists, SourceTampered, checked_computation, ensure_new_output_dir, guarded_export, verify_sources_full` -> [src/topo_pilot/experiment/x5g1_safety.py](../../src/topo_pilot/experiment/x5g1_safety.py.md) (line 24, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 7)
- `io` (lines 9)
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

- none

## Classes and functions

- **function `_burn`** [L39-43]: `def _burn(seconds: float = 0.05) -> None`
- **function `_spec`** [L46-47]: `def _spec() -> TransitionSpec`
- **class `_FlakyBackend(MemoryBackend)`** [L50-56]
- **method `_FlakyBackend.get`** [L53-56]: `def get(self, key: str) -> bytes`
- **function `saved`** [L60-68]: `def saved()` decorators: @pytest.fixture() - A store with two lawfully saved TransitionSpecs and their full expected hashes.
- **function `_key`** [L71-74]: `def _key(backend: MemoryBackend, aid: str, name: str) -> str`
- **function `_mutate_payload`** [L77-85]: `def _mutate_payload(backend: MemoryBackend, aid: str) -> None`
- **function `_mutate_meta_hash`** [L88-93]: `def _mutate_meta_hash(backend: MemoryBackend, aid: str) -> None`
- **function `_rc`** [L96-97]: `def _rc(tmp: Path, *, cap_s=3600.0, cum_cap=3600.0, job='unit') -> RunControls`
- **function `_ledger`** [L100-101]: `def _ledger(tmp: Path) -> dict`
- **test `test_verify_full_hash_of_lawful_artifacts_passes`** [L107-112]: `def test_verify_full_hash_of_lawful_artifacts_passes(saved)`
- **test `test_verify_wrong_full_hash_fails`** [L115-122]: `def test_verify_wrong_full_hash_fails(saved)`
- **test `test_verify_prefix_only_hash_rejected`** [L125-129]: `def test_verify_prefix_only_hash_rejected(saved)`
- **test `test_verify_payload_mutated_with_meta_intact_fails`** [L132-138]: `def test_verify_payload_mutated_with_meta_intact_fails(saved)`
- **test `test_verify_meta_hash_mutated_fails`** [L141-146]: `def test_verify_meta_hash_mutated_fails(saved)`
- **test `test_verify_disallowed_consumer_is_failure_not_raise`** [L149-152]: `def test_verify_disallowed_consumer_is_failure_not_raise(saved)`
- **test `test_verify_missing_artifact_is_failure_not_raise`** [L155-161]: `def test_verify_missing_artifact_is_failure_not_raise(saved)`
- **test `test_verify_broken_backend_is_failure_not_raise`** [L164-168]: `def test_verify_broken_backend_is_failure_not_raise(saved)`
- **test `test_checked_computation_returns_result_when_clean`** [L174-183]: `def test_checked_computation_returns_result_when_clean(saved)`
- **test `test_checked_computation_before_failure_skips_fn`** [L186-200]: `def test_checked_computation_before_failure_skips_fn(saved)`
- **test `test_checked_computation_tamper_inside_fn_raises_after`** [L205-220]: `def test_checked_computation_tamper_inside_fn_raises_after(saved, mutate)` decorators: @pytest.mark.parametrize('mutate', [_mutate_payload, _mutate_meta_hash], ids=['payload', 'meta_hash'])
- **test `test_output_dir_new_path_is_created`** [L226-233]: `def test_output_dir_new_path_is_created(tmp_path)`
- **test `test_output_dir_non_empty_raises_and_is_untouched`** [L237-253]: `def test_output_dir_non_empty_raises_and_is_untouched(tmp_path, kind)` decorators: @pytest.mark.parametrize('kind', ['file', 'subdir'])
- **function `_steps`** [L259-269]: `def _steps(log: list, names=('s1', 's2'), hooks=None)`
- **test `test_export_without_stop_runs_all_in_order`** [L272-283]: `def test_export_without_stop_runs_all_in_order(tmp_path)`
- **test `test_export_stop_file_created_in_step1`** [L286-302]: `def test_export_stop_file_created_in_step1(tmp_path)`
- **test `test_export_stop_in_middle_step_keeps_completed`** [L305-317]: `def test_export_stop_in_middle_step_keeps_completed(tmp_path)`
- **test `test_export_stop_present_before_start_runs_nothing`** [L320-330]: `def test_export_stop_present_before_start_runs_nothing(tmp_path)`
- **test `test_export_budget_exceeded`** [L333-346]: `def test_export_budget_exceeded(tmp_path)`
- **test `test_export_other_exception_propagates_without_status`** [L349-364]: `def test_export_other_exception_propagates_without_status(tmp_path)`
- **test `test_ledger_preserves_history_on_error_and_is_atomic`** [L370-389]: `def test_ledger_preserves_history_on_error_and_is_atomic(tmp_path)`
- **test `test_corrupt_ledger_raises_and_keeps_bytes`** [L392-399]: `def test_corrupt_ledger_raises_and_keeps_bytes(tmp_path)`

