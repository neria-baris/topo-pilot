# `tests/circle_history/test_builder_v24_stages.py`

- Source: [tests/circle_history/test_builder_v24_stages.py](../../../../../tests/circle_history/test_builder_v24_stages.py)
- Kind: python
- Lines: 182

## Module docstring

> BUILDER tests (not independent) for spec v2.4 items 1, 8, 9 and 10: gate taxonomy, stage
> prerequisites / no retry / evidence integrity, persisted reference reuse, saved-ID alignment,
> precision-stage controls and cross-model checks. Synthetic memory store only (the
> test_builder_e2e harness). See BUILDER_TESTS.md.

## Imports

### Internal (repo files)

- `import runner` -> [tools/x4_circle_history/runner.py](../../tools/x4_circle_history/runner.py.md) (line 19, via paired directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 20, via paired directory)
- `from errors import Invalid, JoinError, Unresolved` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 21, via paired directory)
- `from test_builder_e2e import MODELS, _context, _gates` -> [tests/circle_history/test_builder_e2e.py](test_builder_e2e.py.md) (line 22, via same directory)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 102, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 12)
- `pytest` (lines 13)

### Standard library

- `__future__` (lines 6)
- `json` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(HERE)` -> `tests/circle_history`

## Imported by

- none

## Top-level constants

- `HERE`

## Classes and functions

- **test `test_run_gate_taxonomy`** [L33-39]: `def test_run_gate_taxonomy(tmp_path, exc, status)` decorators: @pytest.mark.parametrize('exc,status', [(Invalid('x'), 'FAIL_TECHNICAL'), (JoinError('x'), 'FAIL_TECHNICAL'), (Unresolved('x'), 'INCONCLUSIVE')])
- **test `test_out_of_order_stage_refused_without_gate`** [L43-48]: `def test_out_of_order_stage_refused_without_gate(tmp_path, stage)` decorators: @pytest.mark.parametrize('stage', ['oracle', 'charts', 'precision'])
- **test `test_second_attempt_refused_even_without_completion`** [L51-60]: `def test_second_attempt_refused_even_without_completion(tmp_path)`
- **test `test_evidence_change_is_integrity_refusal_and_export_fails`** [L63-72]: `def test_evidence_change_is_integrity_refusal_and_export_fails(tmp_path)`
- **function `through_oracle`** [L76-81]: `def through_oracle(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `_copy_store`** [L84-86]: `def _copy_store(src: Path, dst: Path) -> None`
- **test `test_oracle_persists_bound_reference`** [L89-98]: `def test_oracle_persists_bound_reference(through_oracle)`
- **test `test_charts_reuse_reference_without_recomputation`** [L101-124]: `def test_charts_reuse_reference_without_recomputation(through_oracle, tmp_path, monkeypatch)`
- **test `test_charts_refuse_tampered_reference_identity`** [L127-133]: `def test_charts_refuse_tampered_reference_identity(through_oracle, tmp_path)`
- **test `test_saved_ids_must_match_reloaded_rows`** [L136-149]: `def test_saved_ids_must_match_reloaded_rows(through_oracle)`
- **function `_through_charts`** [L152-157]: `def _through_charts(tmp_path, through_oracle, **precision)`
- **test `test_precision_written_after_b4_stop_with_controls`** [L160-169]: `def test_precision_written_after_b4_stop_with_controls(through_oracle, tmp_path)`
- **test `test_precision_cross_model_sequence_mismatch_fails_technical`** [L172-182]: `def test_precision_cross_model_sequence_mismatch_fails_technical(through_oracle, tmp_path)`

