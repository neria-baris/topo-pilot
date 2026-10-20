# `tests/learner/test_model.py`

- Source: [tests/learner/test_model.py](../../../../../tests/learner/test_model.py)
- Kind: python
- Lines: 92

## Module docstring

> L01-L03, L09: architecture contracts.

## Imports

### Internal (repo files)

- `import topo_pilot.learner` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.learner import HOOK_NAMES, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 11, via package root)

### External (third-party)

- `pytest` (lines 6)
- `torch` (lines 7, 42)

### Standard library

- `ast` (lines 3)
- `pathlib` (lines 4)

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

- **function `model`** [L17-22]: `def model(model_cfg)` decorators: @pytest.fixture()
- **function `_inputs`** [L25-27]: `def _inputs(cfg, batch=3, seed=1)`
- **test `test_L01_causality_every_position`** [L30-38]: `def test_L01_causality_every_position(model, model_cfg)`
- **test `test_L01b_causal_mask_failed_raised_at_construction`** [L41-48]: `def test_L01b_causal_mask_failed_raised_at_construction(monkeypatch, model_cfg)`
- **test `test_L02_shapes_and_hook_names`** [L51-63]: `def test_L02_shapes_and_hook_names(model, model_cfg)`
- **test `test_L03_resid_to_logits_exact`** [L66-74]: `def test_L03_resid_to_logits_exact(model, model_cfg)`
- **test `test_L09_no_forbidden_imports`** [L77-92]: `def test_L09_no_forbidden_imports()`

