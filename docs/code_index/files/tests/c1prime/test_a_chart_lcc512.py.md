# `tests/c1prime/test_a_chart_lcc512.py`

- Source: [tests/c1prime/test_a_chart_lcc512.py](../../../../../tests/c1prime/test_a_chart_lcc512.py)
- Kind: python
- Lines: 238

## Module docstring

> Independent tests, author A (job 0026): fit_chart_lcc on a 512-landmark fixture whose largest
> component has exactly 487 landmarks (TEST_PLAN A-1 items 2, 3, 5, 6 and 9; protocol section 14).

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 31, via sys.path edit)
- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 32, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 33, via sys.path edit)
- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 34, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 35, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)
- `ripser` (lines 19)
- `scipy` (lines 20, 21)

### Standard library

- `__future__` (lines 10)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)
- `types` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 29: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `REPO`
- `TWO_PI`

## Classes and functions

- **function `make_ids`** [L41-42]: `def make_ids(n, base=10 ** 9)`
- **function `loop_points`** [L45-60]: `def loop_points(m, width=8.0)` - m points on the perimeter (length m) of a (m/2 - width) x width rectangle, jittered.
- **class `Recorder`** [L63-68]
- **method `Recorder.__init__`** [L64-65]: `def __init__(self)`
- **method `Recorder.__call__`** [L67-68]: `def __call__(self, name, record)`
- **function `pick`** [L71-75]: `def pick(record, *names)`
- **function `built`** [L79-92]: `def built()` decorators: @pytest.fixture(scope='module')
- **function `ref`** [L96-123]: `def ref(built)` decorators: @pytest.fixture(scope='module') - Section 14 steps 1-8 with the frozen kernels, independently of c1_chart.
- **function `same`** [L126-128]: `def same(a, b)`
- **test `test_fixture_has_one_487_component_and_25_singletons`** [L131-136]: `def test_fixture_has_one_487_component_and_25_singletons(built, ref)`
- **test `test_giant_487_passes_and_restriction_keeps_cstar_only`** [L139-153]: `def test_giant_487_passes_and_restriction_keeps_cstar_only(built, ref)`
- **test `test_lift_primitive_smoothing_are_the_frozen_kernels_on_cstar`** [L156-165]: `def test_lift_primitive_smoothing_are_the_frozen_kernels_on_cstar(built, ref)`
- **test `test_scale_statistics_use_the_cstar_submatrix_only`** [L168-176]: `def test_scale_statistics_use_the_cstar_submatrix_only(built, ref)` - Item 6: d8, sigma and support_radius from _neighbor_scale(D[np.ix_(C*, C*)]).
- **test `test_persist_order_and_values`** [L179-195]: `def test_persist_order_and_values(built, ref)` - Items 3 and 9: giant before the lift, then lift kind, g and the smoothing residual.
- **test `test_excluded_landmarks_get_extension_phases_only`** [L198-212]: `def test_excluded_landmarks_get_extension_phases_only(built)` - Item 5: satellites are never charted neighbours; their phase comes from extend.
- **test `test_gauge_points_are_the_cstar_landmarks_only`** [L215-223]: `def test_gauge_points_are_the_cstar_landmarks_only(built)`
- **test `test_serialise_roles_and_identity_carrier`** [L226-238]: `def test_serialise_roles_and_identity_carrier(built)`

