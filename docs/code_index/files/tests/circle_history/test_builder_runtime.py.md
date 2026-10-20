# `tests/circle_history/test_builder_runtime.py`

- Source: [tests/circle_history/test_builder_runtime.py](../../../../../tests/circle_history/test_builder_runtime.py)
- Kind: python
- Lines: 235

## Module docstring

> BUILDER tests (not independent): job binding, stage ceilings, release refusals, static
> scored-access audit and import hygiene. See BUILDER_TESTS.md.

## Imports

### Internal (repo files)

- `import meter_bind` -> [tools/x4_circle_history/meter_bind.py](../../tools/x4_circle_history/meter_bind.py.md) (line 21, via sys.path edit)
- `import release` -> [tools/x4_circle_history/release.py](../../tools/x4_circle_history/release.py.md) (line 22, via sys.path edit)
- `import runner` -> [tools/x4_circle_history/runner.py](../../tools/x4_circle_history/runner.py.md) (line 166, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 4)
- `ast` (lines 6)
- `copy` (lines 7)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `SIDE_EFFECT_FREE`
- `TOOL`

## Classes and functions

- **function `_ledger`** [L25-28]: `def _ledger(tmp_path, entries)`
- **function `bound`** [L32-51]: `def bound(tmp_path, monkeypatch)` decorators: @pytest.fixture()
- **test `test_binding_points_unchanged_modules_at_this_job`** [L54-60]: `def test_binding_points_unchanged_modules_at_this_job(bound)`
- **test `test_stage_label_and_ceiling`** [L63-76]: `def test_stage_label_and_ceiling(bound)`
- **test `test_exhausted_or_unreleased_stage_runs_noop`** [L82-86]: `def test_exhausted_or_unreleased_stage_runs_noop(bound, stage, spent)` decorators: @pytest.mark.parametrize('stage,spent', [('implementation', 399.5), ('export', 79.2), ('charts', 0.0), ('oracle', 0.0)])
- **test `test_export_cap_is_80_without_release`** [L89-92]: `def test_export_cap_is_80_without_release(bound)`
- **function `_mailbox`** [L95-120]: `def _mailbox(tmp_path, job='0099')`
- **function `_write`** [L123-126]: `def _write(box, rel, job='0099')`
- **test `test_release_accepts_exact_binding`** [L129-131]: `def test_release_accepts_exact_binding(tmp_path)`
- **test `test_release_refuses_any_mismatch`** [L148-152]: `def test_release_refuses_any_mismatch(tmp_path, field, value)` decorators: @pytest.mark.parametrize('field,value', [('task_sha256', '0' * 64), ('job_id', '0098'), ('source_commit', '0' * 40), ('freeze_sha256', '0' * 64), ('contract_sha256', '0' * 64), ('issued_by', 'someone'), ('schema', 'other'), ('released_stages', ['identity', 'scoring_everything']), ('scoring_released', True)])
- **test `test_release_refuses_wrong_location_and_unreadable`** [L155-162]: `def test_release_refuses_wrong_location_and_unreadable(tmp_path)`
- **test `test_runner_refuses_without_release`** [L165-168]: `def test_runner_refuses_without_release(tmp_path)`
- **test `test_module_top_level_has_no_calls_with_io`** [L195-219]: `def test_module_top_level_has_no_calls_with_io(name)` decorators: @pytest.mark.parametrize('name', SIDE_EFFECT_FREE)
- **test `test_static_scored_access_audit`** [L222-235]: `def test_static_scored_access_audit()`

