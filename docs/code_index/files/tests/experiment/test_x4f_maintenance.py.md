# `tests/experiment/test_x4f_maintenance.py`

- Source: [tests/experiment/test_x4f_maintenance.py](../../../../../tests/experiment/test_x4f_maintenance.py)
- Kind: python
- Lines: 140

## Module docstring

> Author-written maintenance regressions on synthetic arrays and temporary stores only.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x4f_damage, x4f_gates, x4f_probe, x4f_run` -> [src/topo_pilot/experiment/x4f_damage.py](../../src/topo_pilot/experiment/x4f_damage.py.md), [src/topo_pilot/experiment/x4f_gates.py](../../src/topo_pilot/experiment/x4f_gates.py.md), [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md), [src/topo_pilot/experiment/x4f_run.py](../../src/topo_pilot/experiment/x4f_run.py.md) (line 10, via package root)
- `from topo_pilot.experiment.x5g1_controls import BudgetExceeded, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](../../src/topo_pilot/experiment/x5g1_controls.py.md) (line 11, via package root)
- `from topo_pilot.analysis import fit_oblique_eraser, whiten` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 95, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)

### Standard library

- `hashlib` (lines 2)
- `json` (lines 3)
- `time` (lines 4)
- `types` (lines 5)

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

- **test `test_runner_persists_prior_cpu_and_failure`** [L22-39]: `def test_runner_persists_prior_cpu_and_failure(tmp_path, monkeypatch, exc, status)` decorators: @pytest.mark.parametrize('exc,status', [(StopRequested('synthetic STOP'), 'stopped'), (BudgetExceeded('synthetic budget'), 'budget'), (ValueError('synthetic export failure'), 'error:ValueError'), (KeyboardInterrupt(), 'error:KeyboardInterrupt')])
- **test `test_stop_precedes_any_source_load`** [L42-47]: `def test_stop_precedes_any_source_load(tmp_path, monkeypatch)`
- **test `test_completed_exports_are_not_overwritten`** [L50-58]: `def test_completed_exports_are_not_overwritten(tmp_path)`
- **test `test_ridge_stop_inside_solver_grid`** [L61-74]: `def test_ridge_stop_inside_solver_grid()`
- **test `test_shuffle_stop_inside_refits`** [L77-91]: `def test_shuffle_stop_inside_refits(monkeypatch)`
- **test `test_unmatched_family_keeps_partial_and_control_maps`** [L94-110]: `def test_unmatched_family_keeps_partial_and_control_maps(monkeypatch)`
- **test `test_export_round_trips_all_maps_without_pickle_and_records_hash`** [L113-140]: `def test_export_round_trips_all_maps_without_pickle_and_records_hash(tmp_path, monkeypatch)`

