# `tests/hwsd/test_a_known_bound.py`

- Source: [tests/hwsd/test_a_known_bound.py](../../../../../tests/hwsd/test_a_known_bound.py)
- Kind: python
- Lines: 225

## Module docstring

> Author A (job 0197): KD6, the K4b known cases at the hwsd constants (§6 KD6; TEST_PLAN A).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 30, via sys.path edit)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](../../tools/hwsd/hwsd_bind.py.md) (line 31, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 32, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 33, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 34, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 35, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 36, via unique basename)
- `import test_a_hwsd_ref` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 37, via same directory)

### External (third-party)

- `numpy` (lines 21)
- `pytest` (lines 22)

### Standard library

- `__future__` (lines 10)
- `decimal` (lines 17)
- `fractions` (lines 18)
- `hashlib` (lines 12)
- `itertools` (lines 13)
- `math` (lines 14)
- `pathlib` (lines 19)
- `random` (lines 15)
- `sys` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `HERE`
- `M`
- `REPO`

## Classes and functions

- **function `bound`** [L43-46]: `def bound()` decorators: @pytest.fixture
- **function `_hmm`** [L50-58]: `def _hmm(S, A, seed)`
- **function `_enumerate`** [L61-72]: `def _enumerate(T, E, pi, c, L)`
- **test `test_proposition_1_exact`** [L76-98]: `def test_proposition_1_exact(bound, S, A, seed)` decorators: @pytest.mark.parametrize('S,A,seed', [(2, 2, 1), (3, 2, 2), (2, 3, 3), (3, 3, 4)])
- **test `test_theorem_a_completions`** [L102-121]: `def test_theorem_a_completions(bound)`
- **test `test_lemma_n_isqrt_bracket`** [L125-131]: `def test_lemma_n_isqrt_bracket(bound)`
- **test `test_lemma_n_norm_bound_planted`** [L134-144]: `def test_lemma_n_norm_bound_planted(bound)`
- **test `test_model_status_boundaries`** [L148-169]: `def test_model_status_boundaries(bound)`
- **test `test_model_status_random_grid`** [L172-181]: `def test_model_status_random_grid(bound)`
- **test `test_ranks`** [L185-200]: `def test_ranks(bound)`
- **test `test_bounds_ranks_84_4917`** [L203-206]: `def test_bounds_ranks_84_4917(bound)`
- **test `test_chart_equality_and_protocol_inside_binding`** [L210-216]: `def test_chart_equality_and_protocol_inside_binding(bound)`
- **test `test_constants_restored_after_the_block`** [L220-225]: `def test_constants_restored_after_the_block()`

