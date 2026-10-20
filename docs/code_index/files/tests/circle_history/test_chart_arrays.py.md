# `tests/circle_history/test_chart_arrays.py`

- Source: [tests/circle_history/test_chart_arrays.py](../../../../../tests/circle_history/test_chart_arrays.py)
- Kind: python
- Lines: 117

## Module docstring

> Independent synthetic tests, author A (spec v2.3): chart_to_arrays / chart_from_arrays
> exact round trip (TEST_PLAN A13).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 23, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 7)
- `io` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `ARRAY_FIELDS`
- `CHART_KEYS`
- `INFO_KEYS`
- `INT_FIELDS`
- `PKG`
- `REPO_ROOT`
- `THETA`
- `TWO_PI`

## Classes and functions

- **function `make_cfg`** [L42-47]: `def make_cfg(**overrides)`
- **function `circle_points`** [L53-56]: `def circle_points(theta)`
- **function `fitted`** [L60-64]: `def fitted()` decorators: @pytest.fixture(scope='module')
- **function `assert_round_trip`** [L67-81]: `def assert_round_trip(back, gback, original, gauge)`
- **test `test_chart_arrays_round_trip_exact`** [L84-94]: `def test_chart_arrays_round_trip_exact(fitted)`
- **test `test_chart_arrays_survive_npz_without_pickle`** [L97-107]: `def test_chart_arrays_survive_npz_without_pickle(fitted)`
- **test `test_round_trip_preserves_extension`** [L110-117]: `def test_round_trip_preserves_extension(fitted)`

