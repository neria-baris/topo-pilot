# `tests/dataset/test_public.py`

- Source: [tests/dataset/test_public.py](../../../../../tests/dataset/test_public.py)
- Kind: python
- Lines: 55

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, EvalSidecar, ObservationSet, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 14, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 15, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)
- `torch` (lines 5)

### Standard library

- `dataclasses` (lines 1)

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

- **test `test_D06_observation_set_has_no_latent_field_and_sidecar_is_rejected`** [L20-27]: `def test_D06_observation_set_has_no_latent_field_and_sidecar_is_rejected()`
- **test `test_latent_field_added_to_observation_subclass_is_leakage`** [L30-40]: `def test_latent_field_added_to_observation_subclass_is_leakage()`
- **test `test_D07_inputs_and_targets_via_layout`** [L43-55]: `def test_D07_inputs_and_targets_via_layout()`

