# `tests/topology/test_persistence.py`

- Source: [tests/topology/test_persistence.py](../../../../../tests/topology/test_persistence.py)
- Kind: python
- Lines: 238

## Module docstring

> T03, T04, T05, T08, T09, T10 and contract checks for PH, summaries, landmarks.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.topology import DistancePipeline, Euclidean, PersistenceComputer, PHConfig, Summaries` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 4)
- `pytest` (lines 5)
- `scipy` (lines 6)

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

- none

## Classes and functions

- **function `ids`** [L20-21]: `def ids(n)`
- **function `circle_pts`** [L24-28]: `def circle_pts(m, radius=1.0, ambient=2)`
- **function `noisy_circle`** [L31-36]: `def noisy_circle(m, seed, ambient=8, noise=0.02)`
- **function `rows_of`** [L39-40]: `def rows_of(diag)`
- **function `bars`** [L43-45]: `def bars(diag, dim)`
- **function `sorted_rows`** [L48-50]: `def sorted_rows(r)`
- **test `test_T03_unit_square_known_answer`** [L53-69]: `def test_T03_unit_square_known_answer()`
- **test `test_T04_scale_covariance`** [L72-90]: `def test_T04_scale_covariance()`
- **test `test_scale_s_is_q95_of_positive_distances`** [L93-102]: `def test_scale_s_is_q95_of_positive_distances()`
- **test `test_T05_permutation_invariance`** [L105-120]: `def test_T05_permutation_invariance()`
- **test `test_T08_dedup_same_diagrams`** [L123-134]: `def test_T08_dedup_same_diagrams()`
- **test `test_T08_all_identical_cloud_collapsed`** [L137-141]: `def test_T08_all_identical_cloud_collapsed()`
- **test `test_T08_all_zero_D_collapsed_and_S_zero`** [L144-148]: `def test_T08_all_zero_D_collapsed_and_S_zero()`
- **test `test_T09_small_threshold_marks_censored_not_dropped`** [L151-169]: `def test_T09_small_threshold_marks_censored_not_dropped()`
- **test `test_non_metric_input_raises`** [L177-182]: `def test_non_metric_input_raises(make_bad)` decorators: @pytest.mark.parametrize('make_bad', [lambda D: np.triu(D) + 0.3 * np.tril(np.ones_like(D), -1), lambda D: D - 5.0 * (1 - np.eye(len(D))), lambda D: D + 0.5 * np.eye(len(D))])
- **test `test_summaries_hand_values`** [L185-199]: `def test_summaries_hand_values()`
- **test `test_maxmin_landmarks`** [L202-215]: `def test_maxmin_landmarks()`
- **function `rp2_sample`** [L218-223]: `def rp2_sample(m, seed)` - Veronese embedding x -> x x^T of random points on S^2: an embedded RP^2 in R^9.
- **test `test_T10_coeff_p_passed_through`** [L227-238]: `def test_T10_coeff_p_passed_through()` decorators: @pytest.mark.slow

