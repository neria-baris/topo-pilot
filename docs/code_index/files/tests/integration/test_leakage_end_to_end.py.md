# `tests/integration/test_leakage_end_to_end.py`

- Source: [tests/integration/test_leakage_end_to_end.py](../../../../../tests/integration/test_leakage_end_to_end.py)
- Kind: python
- Lines: 26

## Module docstring

> I04: scrambling EvalSidecar.z leaves every Checkpoint / ActivationSet id and payload
> checksum unchanged, so the learner and activations never read the latents.

## Imports

### Internal (repo files)

- `import _mini_pipeline` -> [tests/integration/_mini_pipeline.py](_mini_pipeline.py.md) (line 10, via same directory)
- `from topo_pilot.contracts import ActivationSet, Checkpoint, EvalSidecar` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 12, via package root)

### External (third-party)

- `pytest` (lines 7)

### Standard library

- `pathlib` (lines 5)
- `sys` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 9: `str(Path(__file__).parent)` -> `tests/integration`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_I04_scrambled_latents_do_not_reach_learner`** [L17-26]: `def test_I04_scrambled_latents_do_not_reach_learner(tmp_path_factory)`

