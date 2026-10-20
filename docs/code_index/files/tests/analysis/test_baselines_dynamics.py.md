# `tests/analysis/test_baselines_dynamics.py`

- Source: [tests/analysis/test_baselines_dynamics.py](../../../../../tests/analysis/test_baselines_dynamics.py)
- Kind: python
- Lines: 121

## Module docstring

> Independent tests N11 (R2 baseline on a ring process) and N12 (checkpoint-order null).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import Dynamics, r2_points, r3_points, spectral_embedding` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 7, via package root)
- `from topo_pilot.topology import DistancePipeline, Euclidean, NullClouds, PersistenceComputer, PHConfig, Summaries` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 4)
- `pytest` (lines 5)

### Standard library

- `math` (lines 2)

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

- `EARLY`
- `V`

## Classes and functions

- **function `ring_process`** [L22-31]: `def ring_process(eps=0.05)`
- **function `sample_histories`** [L34-43]: `def sample_histories(E, T, M, L, rng)`
- **function `S_h1`** [L46-49]: `def S_h1(X)`
- **test `test_spectral_embedding_shape_and_r2_r3_definitions`** [L52-58]: `def test_spectral_embedding_shape_and_r2_r3_definitions()`
- **test `test_r2_points_on_ring_process_have_h1_above_gaussian_null`** [L61-72]: `def test_r2_points_on_ring_process_have_h1_above_gaussian_null()`
- **function `stat_ref`** [L76-79]: `def stat_ref(values)`
- **test `test_checkpoint_order_statistic_hand_values`** [L85-93]: `def test_checkpoint_order_statistic_hand_values()`
- **test `test_p_value_has_plus_one_form`** [L96-100]: `def test_p_value_has_plus_one_form()`
- **test `test_early_jump_gives_small_p`** [L103-106]: `def test_early_jump_gives_small_p()`
- **test `test_p_value_matches_independent_monte_carlo`** [L109-114]: `def test_p_value_matches_independent_monte_carlo()`
- **test `test_random_sequences_are_not_systematically_small_p`** [L117-121]: `def test_random_sequences_are_not_systematically_small_p()`

