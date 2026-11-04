# `tests/hwsg/test_a_selection.py`

- Source: [tests/hwsg/test_a_selection.py](../../../../../tests/hwsg/test_a_selection.py)
- Kind: python
- Lines: 192

## Module docstring

> Author A (job 0224): world selection O0 and headroom O5 (protocol §3; API §4; TEST_PLAN §2).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 24, via sys.path edit)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](../../tools/hwsg/hwsg_oracle.py.md) (line 25, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 7)
- `copy` (lines 9)
- `hashlib` (lines 10)
- `json` (lines 11)
- `math` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hws`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`

## Imported by

- none

## Top-level constants

- `C`
- `KEYS`
- `REPO`
- `ROOT`
- `SEL`
- `W_STAR`
- `_ERR`

## Classes and functions

- **function `_imports`** [L36-38]: `def _imports()` decorators: @pytest.fixture(autouse=True)
- **function `_status`** [L41-46]: `def _status(fn, *a, **k)`
- **function `_sha`** [L49-50]: `def _sha(p)`
- **function `_rule`** [L53-61]: `def _rule(order, d4, bounded)` - Independent recomputation of the §3 rule.
- **function `_real_records`** [L64-75]: `def _real_records()`
- **test `test_independent_rule_reproduces_registered`** [L78-86]: `def test_independent_rule_reproduces_registered()`
- **test `test_go_selection_agrees_on_real_records`** [L89-94]: `def test_go_selection_agrees_on_real_records()`
- **function `_plant`** [L102-123]: `def _plant(tmp_path, monkeypatch, d4, unavailable=(), registered=None)`
- **test `test_tie_resolved_by_finalists_order`** [L126-132]: `def test_tie_resolved_by_finalists_order(tmp_path, monkeypatch)`
- **test `test_unavailable_world_excluded`** [L135-140]: `def test_unavailable_world_excluded(tmp_path, monkeypatch)`
- **test `test_changed_record_byte_fails_binding`** [L143-148]: `def test_changed_record_byte_fails_binding(tmp_path, monkeypatch)`
- **test `test_changed_report_byte_fails_binding`** [L151-155]: `def test_changed_report_byte_fails_binding(tmp_path, monkeypatch)`
- **test `test_unregistered_result_fails_binding`** [L158-162]: `def test_unregistered_result_fails_binding(tmp_path, monkeypatch)`
- **function `_rep`** [L168-169]: `def _rep(key, at3, d4)`
- **function `_ok`** [L172-173]: `def _ok(r)`
- **test `test_headroom_at_3x_false`** [L177-180]: `def test_headroom_at_3x_false(tag)` decorators: @pytest.mark.parametrize('tag', ['lo', 'mid', 'hi'])
- **test `test_headroom_threshold_equality_passes`** [L183-186]: `def test_headroom_threshold_equality_passes()`
- **test `test_headroom_below_threshold_fails`** [L189-192]: `def test_headroom_below_threshold_fails()`

