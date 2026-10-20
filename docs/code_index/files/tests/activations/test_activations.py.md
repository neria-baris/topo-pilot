# `tests/activations/test_activations.py`

- Source: [tests/activations/test_activations.py](../../../../../tests/activations/test_activations.py)
- Kind: python
- Lines: 167

## Module docstring

> Tests A01-A06 for the activations module (see TEST_PLAN.md).

## Imports

### Internal (repo files)

- `import topo_pilot.activations` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 15, via package root)
- `from topo_pilot.activations import ActivationExtractor, ActivationStage` -> [src/topo_pilot/activations/__init__.py](../../src/topo_pilot/activations/__init__.py.md) (line 16, via package root)
- `from topo_pilot.contracts import ActivationSet, Checkpoint, ErrorCode, EvalSidecar, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 25, via package root)
- `import topo_pilot.learner` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 157, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 11)
- `pytest` (lines 12)
- `torch` (lines 13)

### Standard library

- `__future__` (lines 3)
- `ast` (lines 5)
- `dataclasses` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 7)
- `types` (lines 8)

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

- `HOOKS`
- `PANEL_SIZE`
- `V`

## Classes and functions

- **test `test_A01_row_order_equals_index_order_for_any_batch_size`** [L35-50]: `def test_A01_row_order_equals_index_order_for_any_batch_size(tiny_model, tiny_obs, tiny_index)`
- **test `test_A02_logits_equal_plain_forward_at_position_32`** [L53-60]: `def test_A02_logits_equal_plain_forward_at_position_32(tiny_model, tiny_obs, tiny_index)`
- **function `_extract_one`** [L63-64]: `def _extract_one(model, obs, build_index)`
- **test `test_A03_w33_invisible_w32_visible`** [L67-76]: `def test_A03_w33_invisible_w32_visible(tiny_model, tiny_obs, index_builder)`
- **test `test_A04_unknown_hook_and_corrupted_hash`** [L79-93]: `def test_A04_unknown_hook_and_corrupted_hash(tiny_model, tiny_obs, tiny_index)`
- **test `test_A04_numerical_failure_when_hooked_path_disagrees`** [L96-106]: `def test_A04_numerical_failure_when_hooked_path_disagrees(tiny_obs, tiny_index, standin_cls)`
- **test `test_A05_panel_filter_returns_exactly_the_panel_ids`** [L109-117]: `def test_A05_panel_filter_returns_exactly_the_panel_ids(tiny_model, tiny_obs, tiny_index)`
- **function `_is_forbidden`** [L120-123]: `def _is_forbidden(name: str) -> bool`
- **test `test_A06_static_imports_are_allowed_only`** [L126-139]: `def test_A06_static_imports_are_allowed_only()`
- **test `test_A06_sidecar_access_raises_leakage_and_stage_roundtrip`** [L142-167]: `def test_A06_sidecar_access_raises_leakage_and_stage_roundtrip(tiny_model, tiny_obs, tiny_index, monkeypatch)`

