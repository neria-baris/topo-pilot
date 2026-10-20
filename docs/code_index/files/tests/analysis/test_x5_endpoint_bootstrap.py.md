# `tests/analysis/test_x5_endpoint_bootstrap.py`

- Source: [tests/analysis/test_x5_endpoint_bootstrap.py](../../../../../tests/analysis/test_x5_endpoint_bootstrap.py)
- Kind: python
- Lines: 260

## Module docstring

> Independent contract tests for ``topo_pilot.analysis.x5_endpoint`` (part 2 of 2).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis.x5_endpoint import DELAY, DiffBounds, PairEvidence, cohort_verdict, difference_bounds, grid_event, pair_evidence, pair_flags, paired_bootstrap_endpoint` -> [src/topo_pilot/analysis/x5_endpoint.py](../../src/topo_pilot/analysis/x5_endpoint.py.md) (line 20, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 13)
- `math` (lines 15)

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

- `B`
- `G5`
- `N`
- `REG_C`
- `REG_F`
- `R_`
- `S`
- `_EVENTS`

## Classes and functions

- **function `_gen`** [L48-49]: `def _gen(name: str = 'boot') -> np.random.Generator`
- **function `_ref_event`** [L52-56]: `def _ref_event(passes, grid) -> tuple[float, float, bool]`
- **function `_ref_boot`** [L59-70]: `def _ref_boot(rc, rf, gcc, gcf, gen, n, grid, thr=0.05)`
- **function `_ref_q`** [L73-75]: `def _ref_q(values, q) -> float`
- **test `test_bootstrap_reproduces_shared_whole_row_draws`** [L81-93]: `def test_bootstrap_reproduces_shared_whole_row_draws() -> None`
- **test `test_bootstrap_keeps_censored_draws_and_fractions`** [L96-104]: `def test_bootstrap_keeps_censored_draws_and_fractions() -> None`
- **test `test_bootstrap_quantiles_are_inverted_cdf_order_statistics`** [L107-113]: `def test_bootstrap_quantiles_are_inverted_cdf_order_statistics() -> None`
- **test `test_bootstrap_consumes_exactly_one_integers_call_per_draw`** [L116-122]: `def test_bootstrap_consumes_exactly_one_integers_call_per_draw() -> None`
- **test `test_bootstrap_guard_strings_per_batch`** [L125-129]: `def test_bootstrap_guard_strings_per_batch() -> None`
- **test `test_bootstrap_guard_brackets_the_draws`** [L132-147]: `def test_bootstrap_guard_brackets_the_draws() -> None`
- **test `test_bootstrap_threshold_passthrough`** [L150-154]: `def test_bootstrap_threshold_passthrough() -> None`
- **test `test_bootstrap_default_grid_27_points`** [L157-163]: `def test_bootstrap_default_grid_27_points() -> None`
- **test `test_bootstrap_shape_errors`** [L168-171]: `def test_bootstrap_shape_errors(rc_shape, rf_shape) -> None` decorators: @pytest.mark.parametrize('rc_shape,rf_shape', [((7, 5), (6, 5)), ((7, 5), (7, 4)), ((7, 4), (7, 4))])
- **test `test_pair_evidence_point_from_full_sample_and_quantiles_from_bootstrap`** [L177-185]: `def test_pair_evidence_point_from_full_sample_and_quantiles_from_bootstrap() -> None`
- **test `test_pair_evidence_deterministic_observed`** [L188-195]: `def test_pair_evidence_deterministic_observed() -> None`
- **function `_pe`** [L203-205]: `def _pe(low: float, q025: float, q975: float, high: float = math.inf) -> PairEvidence`
- **test `test_pair_flags`** [L218-221]: `def test_pair_flags(low, q025, q975, want) -> None` decorators: @pytest.mark.parametrize('low,q025,q975,want', [(250.0, 1e-09, math.inf, (True, False)), (249.999, 10.0, math.inf, (False, False)), (500.0, 0.0, math.inf, (False, False)), (500.0, -math.inf, 1000.0, (False, False)), (math.inf, 10.0, math.inf, (True, False)), (-math.inf, -math.inf, 249.999, (False, True)), (-math.inf, -math.inf, 250.0, (False, False)), (300.0, 10.0, 200.0, (True, True))])
- **test `test_cohort_verdict_truth_table`** [L253-256]: `def test_cohort_verdict_truth_table(pairs, kw, want) -> None` decorators: @pytest.mark.parametrize('pairs,kw,want', [([S, S, S], {}, 'SUPPORTED'), ([S, S, R_], {}, 'REJECTED'), ([R_, N, N], {}, 'REJECTED'), ([R_, R_, R_], {}, 'REJECTED'), ([B, N, N], {}, 'REJECTED'), ([S, S, B], {}, 'INCONCLUSIVE'), ([B, B, B], {}, 'INCONCLUSIVE'), ([S, S, None], {}, 'INCONCLUSIVE'), ([R_, R_, None], {}, 'INCONCLUSIVE'), ([S, S, S], {'failures': ('a020 seed 2 INCOMPLETE',)}, 'INCONCLUSIVE'), ([R_, R_, R_], {'failures': ['integrity']}, 'INCONCLUSIVE'), ([S, S], {}, 'INCONCLUSIVE'), ([S, S, S, S], {}, 'INCONCLUSIVE'), ([], {}, 'INCONCLUSIVE'), ([S, S], {'n_required': 2}, 'SUPPORTED'), ([S, S, S], {'n_required': 2}, 'INCONCLUSIVE'), ([S, S, N], {}, 'INCONCLUSIVE'), ([N, N, N], {}, 'INCONCLUSIVE'), ([S, N, S], {}, 'INCONCLUSIVE')])
- **test `test_cohort_verdict_accepts_tuple`** [L259-260]: `def test_cohort_verdict_accepts_tuple() -> None`

