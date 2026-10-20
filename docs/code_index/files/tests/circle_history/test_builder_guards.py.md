# `tests/circle_history/test_builder_guards.py`

- Source: [tests/circle_history/test_builder_guards.py](../../../../../tests/circle_history/test_builder_guards.py)
- Kind: python
- Lines: 202

## Module docstring

> BUILDER tests (not independent): spec v2.3 guards: supervisor-inclusive stage limiter,
> finalization reserve, strict release/scoring authority, and source integrity before payload I/O.
> Synthetic counters and files only. See BUILDER_TESTS.md.

## Imports

### Internal (repo files)

- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 22, via sys.path edit)
- `import live_context` -> [tools/x4_circle_history/live_context.py](../../tools/x4_circle_history/live_context.py.md) (line 23, via sys.path edit)
- `import meter_bind` -> [tools/x4_circle_history/meter_bind.py](../../tools/x4_circle_history/meter_bind.py.md) (line 24, via sys.path edit)
- `import release` -> [tools/x4_circle_history/release.py](../../tools/x4_circle_history/release.py.md) (line 25, via sys.path edit)
- `import freeze_bind` -> [tools/x4_circle_history/freeze_bind.py](../../tools/x4_circle_history/freeze_bind.py.md) (line 166, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 14)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `subprocess` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `NOT_PASS`
- `REPO`
- `TOOL`

## Classes and functions

- **test `test_stage_limiter_includes_supervisor_and_tail`** [L30-38]: `def test_stage_limiter_includes_supervisor_and_tail()`
- **test `test_stage_limiter_grows_with_supervisor_cpu`** [L41-48]: `def test_stage_limiter_grows_with_supervisor_cpu()`
- **test `test_stage_limiter_delegates_to_unchanged_global_limiter`** [L51-59]: `def test_stage_limiter_delegates_to_unchanged_global_limiter()`
- **function `restore_meter`** [L63-78]: `def restore_meter(monkeypatch)` decorators: @pytest.fixture()
- **test `test_finalization_reserve_binding`** [L81-88]: `def test_finalization_reserve_binding(tmp_path, restore_meter, monkeypatch)`
- **test `test_finalization_only_for_export`** [L91-93]: `def test_finalization_only_for_export(tmp_path, restore_meter)`
- **test `test_require_scoring_denies_non_authority`** [L97-99]: `def test_require_scoring_denies_non_authority(value)` decorators: @pytest.mark.parametrize('value', [None, False, True, {}, 'token', object(), 1])
- **test `test_require_scoring_denies_wrong_scope_or_sha`** [L103-106]: `def test_require_scoring_denies_wrong_scope_or_sha(scope, sha)` decorators: @pytest.mark.parametrize('scope,sha', [(('feasibility',), '0' * 64), (('scoring',), '0' * 10)])
- **test `test_require_scoring_accepts_verified_shape`** [L109-110]: `def test_require_scoring_accepts_verified_shape()`
- **test `test_head_without_subprocess_matches_git`** [L113-117]: `def test_head_without_subprocess_matches_git()`
- **function `_release`** [L120-124]: `def _release(tmp_path, scoring=False, ref=None)`
- **test `test_scoring_authority_requires_strict_true_and_owner_record`** [L127-146]: `def test_scoring_authority_requires_strict_true_and_owner_record(tmp_path)`
- **test `test_scoring_authority_constructed_only_in_release_and_errors`** [L149-153]: `def test_scoring_authority_constructed_only_in_release_and_errors()`
- **test `test_dirty_source_refused_before_io`** [L156-162]: `def test_dirty_source_refused_before_io(tmp_path)`
- **test `test_frozen_file_set_change_refused`** [L165-171]: `def test_frozen_file_set_change_refused()`
- **test `test_release_strict_boolean_in_verify`** [L174-202]: `def test_release_strict_boolean_in_verify(tmp_path)`

