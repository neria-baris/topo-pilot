# `tests/experiment/test_x4f_gates_smoke.py`

- Source: [tests/experiment/test_x4f_gates_smoke.py](../../../../../tests/experiment/test_x4f_gates_smoke.py)
- Kind: python
- Lines: 78

## Module docstring

> Builder-authored smoke test (not the independent X4-F tests): G1-G5 orchestration end to end
> on a tiny synthetic model and planted targets; checks plumbing, statuses and isolation only.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import fit_oblique_eraser, gate_verdict, whiten` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 7, via package root)
- `from topo_pilot.experiment import x4f_gates` -> [src/topo_pilot/experiment/x4f_gates.py](../../src/topo_pilot/experiment/x4f_gates.py.md) (line 8, via package root)
- `from topo_pilot.experiment.x4f_damage import g3, g4, g5` -> [src/topo_pilot/experiment/x4f_damage.py](../../src/topo_pilot/experiment/x4f_damage.py.md) (line 9, via package root)
- `from topo_pilot.experiment.x4f_data import ModelData` -> [src/topo_pilot/experiment/x4f_data.py](../../src/topo_pilot/experiment/x4f_data.py.md) (line 10, via package root)
- `from topo_pilot.experiment.x4f_gates import ValForward, control_targets, g1, g2` -> [src/topo_pilot/experiment/x4f_gates.py](../../src/topo_pilot/experiment/x4f_gates.py.md) (line 11, via package root)
- `from topo_pilot.learner import ModelConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 12, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)
- `torch` (lines 5)

### Standard library

- none

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

- **function `tiny`** [L18-42]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **test `test_gates_end_to_end`** [L45-67]: `def test_gates_end_to_end(tiny, monkeypatch)`
- **test `test_g1_ignores_validation_targets_for_selection`** [L70-78]: `def test_g1_ignores_validation_targets_for_selection(tiny, monkeypatch)`

