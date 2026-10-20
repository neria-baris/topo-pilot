# `tests/circle_history/test_adapter.py`

- Source: [tests/circle_history/test_adapter.py](../../../../../tests/circle_history/test_adapter.py)
- Kind: python
- Lines: 347

## Module docstring

> Independent tests (author B) for adapter.py: TEST_PLAN items B7 and B10 (spec v2.3).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ActivationSet, ArtifactStore, Checkpoint, HistoryIndex, ObservationSet, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 26, via package root)
- `import adapter` -> [tools/x4_circle_history/adapter.py](../../tools/x4_circle_history/adapter.py.md) (line 33, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 31: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BAD_RELEASES`
- `CANONICAL`
- `DEFAULTS`
- `HOOKS`
- `JOIN_CANON`
- `JOIN_PANEL`
- `JOIN_ROWS`
- `JOIN_SEQ`
- `MODELS`
- `N_ROWS`
- `PERMS`
- `REPO_ROOT`
- `SEQ_IDS`

## Classes and functions

- **function `_canonical`** [L46-52]: `def _canonical() -> np.ndarray`
- **function `_save_model`** [L61-111]: `def _save_model(store: ArtifactStore, m: int, opt: dict) -> tuple[dict, dict]`
- **function `build`** [L114-127]: `def build(**bad) -> tuple[ArtifactStore, adapter.E4Manifest, dict]` - Store + manifest for three models; overrides in ``bad`` apply to model 1729 only.
- **class `CountingStore(ArtifactStore)`** [L130-139] - Shares the inner store's backend and policy and records every load call.
- **method `CountingStore.__init__`** [L133-135]: `def __init__(self, inner: ArtifactStore) -> None`
- **method `CountingStore.load`** [L137-139]: `def load(self, cls, artifact_id, *, consumer)`
- **function `valid`** [L143-144]: `def valid()` decorators: @pytest.fixture(scope='module')
- **test `test_lineage_passes_for_every_model`** [L148-152]: `def test_lineage_passes_for_every_model(valid) -> None`
- **test `test_lineage_mismatch_raises_join_error`** [L168-171]: `def test_lineage_mismatch_raises_join_error(bad: dict) -> None` decorators: @pytest.mark.parametrize('bad', [{'drop_hi_parent': True}, {'split': 'dev'}, {'end': 31}, {'hooks': ('resid_post_2', 'resid_post_4')}, {'swap': True}, {'bad_hash': True}, {'ckpt_field': '00000000deadbeef'}, {'source': 'baseline:R0'}, {'layout': (6, 2)}, {'foreign_obs': True}], ids=['parent', 'split', 'end', 'hook', 'order', 'tokens_hash', 'checkpoint', 'source', 'panel_layout', 'dataset'])
- **test `test_panels_rows_in_history_id_order_without_w33`** [L175-200]: `def test_panels_rows_in_history_id_order_without_w33(valid) -> None`
- **test `test_panel_outside_calibration_validation_denied_before_any_load`** [L204-212]: `def test_panel_outside_calibration_validation_denied_before_any_load(valid, request_panels) -> None` decorators: @pytest.mark.parametrize('request_panels', [(3,), (1, 3), (2, 3, 1), (0,), (9,)])
- **function `_auth`** [L216-219]: `def _auth(**changes) -> object`
- **test `test_invalid_scoring_release_denies_panel_3_before_any_load`** [L229-240]: `def test_invalid_scoring_release_denies_panel_3_before_any_load(valid, kind: str) -> None` decorators: @pytest.mark.parametrize('kind', sorted(BAD_RELEASES))
- **test `test_scoring_authority_unlocks_panel_3`** [L243-258]: `def test_scoring_authority_unlocks_panel_3(valid) -> None`
- **function `_leaves`** [L262-274]: `def _leaves(obj)`
- **test `test_identity_report_returns_no_arrays`** [L277-284]: `def test_identity_report_returns_no_arrays(valid) -> None`
- **test `test_identity_report_runs_every_lineage_check`** [L287-290]: `def test_identity_report_runs_every_lineage_check() -> None`
- **function `_join_input`** [L301-309]: `def _join_input(edits: dict | None = None) -> dict`
- **test `test_cross_model_join_orders_by_sequence_id`** [L312-324]: `def test_cross_model_join_orders_by_sequence_id() -> None`
- **function `_replace_seq`** [L327-328]: `def _replace_seq(rec: dict) -> None`
- **function `_change_tokens`** [L331-333]: `def _change_tokens(rec: dict) -> None`
- **function `_swap_panels`** [L336-339]: `def _swap_panels(rec: dict) -> None`
- **test `test_cross_model_join_mismatch_raises_join_error`** [L345-347]: `def test_cross_model_join_mismatch_raises_join_error(edits: dict) -> None` decorators: @pytest.mark.parametrize('edits', [{3141: _replace_seq}, {2718: _change_tokens}, {2718: _swap_panels}], ids=['sequence_set', 'digest', 'panel_sets'])

