# `tests/dataset/test_sampler.py`

- Source: [tests/dataset/test_sampler.py](../../../../../tests/dataset/test_sampler.py)
- Kind: python
- Lines: 59

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 5, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 6, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 7, via package root)

### External (third-party)

- `numpy` (lines 1)
- `pytest` (lines 2)
- `scipy` (lines 3)

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

- **test `test_D01_deterministic_cycle_known_answer`** [L12-22]: `def test_D01_deterministic_cycle_known_answer()`
- **test `test_D02_empirical_frequencies_match_T_E_pi`** [L25-42]: `def test_D02_empirical_frequencies_match_T_E_pi()`
- **test `test_D03_emission_before_transition`** [L45-51]: `def test_D03_emission_before_transition()`
- **test `test_sampler_never_draws_zero_probability_symbols`** [L54-59]: `def test_sampler_never_draws_zero_probability_symbols()`

