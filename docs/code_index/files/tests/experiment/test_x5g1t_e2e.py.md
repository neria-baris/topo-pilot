# `tests/experiment/test_x5g1t_e2e.py`

- Source: [tests/experiment/test_x5g1t_e2e.py](../../../../../tests/experiment/test_x5g1t_e2e.py)
- Kind: python
- Lines: 83

## Module docstring

> Builder-authored SYNTHETIC end-to-end tests of the X5 G1 training-study CLI (job 0009): tiny
> N4/V3 processes, tiny models, temporary stores; persistence, endpoint and bootstrap composition
> only (not real-architecture training).

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.x5g1t_fixture import build_fixture` -> [src/topo_pilot/experiment/x5g1t_fixture.py](../../src/topo_pilot/experiment/x5g1t_fixture.py.md) (line 10, via package root)
- `from topo_pilot.experiment.x5g1t_main import main` -> [src/topo_pilot/experiment/x5g1t_main.py](../../src/topo_pilot/experiment/x5g1t_main.py.md) (line 11, via package root)

### External (third-party)

- `pytest` (lines 8)

### Standard library

- `hashlib` (lines 5)
- `json` (lines 6)

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

- **function `_cli`** [L17-18]: `def _cli(cfg, *args)`
- **function `_manifest_ok`** [L21-23]: `def _manifest_ok(d)`
- **test `test_full_staged_run`** [L26-55]: `def test_full_staged_run(tmp_path)`
- **test `test_budget_stop_records_incomplete_and_inconclusive`** [L58-69]: `def test_budget_stop_records_incomplete_and_inconclusive(tmp_path)`
- **test `test_stop_and_hold_controls`** [L72-83]: `def test_stop_and_hold_controls(tmp_path)`

