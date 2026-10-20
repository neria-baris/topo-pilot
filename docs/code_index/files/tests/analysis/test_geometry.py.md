# `tests/analysis/test_geometry.py`

- Source: [tests/analysis/test_geometry.py](../../../../../tests/analysis/test_geometry.py)
- Kind: python
- Lines: 116

## Module docstring

> Independent tests N07, N08 for Delta_geom (RESEARCH_SUMMARY 7.5).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import GeometryAlignment` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 6, via package root)

### External (third-party)

- `numpy` (lines 2)
- `pytest` (lines 3)
- `scipy` (lines 4)

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

- **function `mat_from_upper`** [L11-14]: `def mat_from_upper(vec, M)`
- **function `pdist_mat`** [L17-18]: `def pdist_mat(X)`
- **function `planted`** [L21-26]: `def planted(M=40, seed=0)`
- **test `test_delta_geom_known_answer_six_pairs`** [L29-34]: `def test_delta_geom_known_answer_six_pairs()`
- **test `test_delta_geom_positive_for_planted_and_negative_when_swapped`** [L37-47]: `def test_delta_geom_positive_for_planted_and_negative_when_swapped()`
- **function `run_pairs`** [L50-52]: `def run_pairs(last)`
- **test `test_same_pair_count_hand_array_and_inconclusive`** [L55-59]: `def test_same_pair_count_hand_array_and_inconclusive()`
- **test `test_same_pairs_below_200_inconclusive`** [L62-66]: `def test_same_pairs_below_200_inconclusive()`
- **test `test_same_pairs_199_inconclusive_and_200_ok`** [L69-76]: `def test_same_pairs_199_inconclusive_and_200_ok()`
- **test `test_same_last_symbol_value_matches_restricted_spearman`** [L79-90]: `def test_same_last_symbol_value_matches_restricted_spearman()`
- **test `test_same_last_symbol_finite_when_b1_is_a_function_of_w32`** [L93-107]: `def test_same_last_symbol_finite_when_b1_is_a_function_of_w32()`
- **test `test_same_last_symbol_none_when_activation_distances_constant`** [L110-116]: `def test_same_last_symbol_none_when_activation_distances_constant()`

