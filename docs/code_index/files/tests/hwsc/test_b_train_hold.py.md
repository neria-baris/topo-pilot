# `tests/hwsc/test_b_train_hold.py`

- Source: [tests/hwsc/test_b_train_hold.py](../../../../../tests/hwsc/test_b_train_hold.py)
- Kind: python
- Lines: 361

## Module docstring

> Author B (job 0176): the TRAIN job (with spies: no real sampling or training), the per-model
> training hold and a tiny held-and-continued training (DRC12).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 24, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 25, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 26, via sys.path edit)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](../../tools/hwsc/hwsc_driver.py.md) (line 27, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 28, via sys.path edit)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 29, via sys.path edit)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 30, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 31, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 32, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 33, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../../tools/hwsb/hwsb_train.py.md) (line 34, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../../tools/k4b/k4b_fresh.py.md) (line 35, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 36, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 37, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, ErrorCode, MemoryBackend, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 38, via package root)

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `hashlib` (lines 11)
- `json` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `AUTH`
- `C`
- `DOWNSTREAM`
- `DRY`
- `FAILED_AUDIT`
- `KEY`
- `REPO`
- `SCHED`
- `STEPS`
- `_HIT`
- `_HWSC`

## Classes and functions

- **function `_sha`** [L50-51]: `def _sha(p)`
- **function `_outcome`** [L54-59]: `def _outcome(fn)` - (raised status or None, returned value or None).
- **function `_statuses`** [L62-70]: `def _statuses(out, raised, ret)`
- **function `_patch_all`** [L73-78]: `def _patch_all(monkeypatch, name, value, also=())` - Set `name` on every loaded stage-C module that defines it (a split by size may keep the
- **function `train_env`** [L83-130]: `def train_env(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **test `test_run_train_passes_stage_c_plan_and_hold`** [L133-151]: `def test_run_train_passes_stage_c_plan_and_hold(train_env)`
- **test `test_run_train_existing_record_is_rerun`** [L154-159]: `def test_run_train_existing_record_is_rerun(train_env)`
- **test `test_run_train_wrong_kc_accept_is_refused`** [L162-171]: `def test_run_train_wrong_kc_accept_is_refused(train_env, tmp_path)`
- **test `test_run_train_owner_stop_at_hold_writes_record`** [L174-181]: `def test_run_train_owner_stop_at_hold_writes_record(train_env)`
- **test `test_run_train_nonfinite_loss`** [L184-188]: `def test_run_train_nonfinite_loss(train_env)`
- **function `_rule`** [L192-206]: `def _rule(tmp_path, decision='CONTINUE')`
- **test `test_hold_constants`** [L209-213]: `def test_hold_constants()`
- **test `test_no_hold_before_step_1000`** [L216-219]: `def test_no_hold_before_step_1000(tmp_path)`
- **test `test_projection_above_cap_holds_and_continue_exempts`** [L222-232]: `def test_projection_above_cap_holds_and_continue_exempts(tmp_path)`
- **test `test_cap_equality_does_not_hold`** [L235-240]: `def test_cap_equality_does_not_hold(tmp_path)`
- **test `test_stop_at_hold_is_inconclusive`** [L243-248]: `def test_stop_at_hold_is_inconclusive(tmp_path)`
- **function `_tiny_run`** [L252-271]: `def _tiny_run(tmp_path, name, hold_dir=None)`
- **test `test_held_and_continued_tiny_run_is_bitwise_equal`** [L274-283]: `def test_held_and_continued_tiny_run_is_bitwise_equal(tmp_path)`
- **function `_plant_failing_audit`** [L300-323]: `def _plant_failing_audit(monkeypatch, stage)`
- **function `_assert_stopped_at_audit`** [L326-335]: `def _assert_stopped_at_audit(out, raised, ret, started)`
- **test `test_failed_binding_audit_stops_the_job`** [L339-353]: `def test_failed_binding_audit_stops_the_job(tmp_path, monkeypatch, stage)` decorators: @pytest.mark.parametrize('stage', ['E2', 'REG2', 'KC'])
- **test `test_failed_binding_audit_stops_train`** [L356-361]: `def test_failed_binding_audit_stops_train(train_env, monkeypatch)`

