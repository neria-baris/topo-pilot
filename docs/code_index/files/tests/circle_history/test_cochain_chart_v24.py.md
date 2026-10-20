# `tests/circle_history/test_cochain_chart_v24.py`

- Source: [tests/circle_history/test_cochain_chart_v24.py](../../../../../tests/circle_history/test_cochain_chart_v24.py)
- Kind: python
- Lines: 245

## Module docstring

> Independent synthetic tests, author A (spec v2.4): integer_lift entry/exit timer and the
> fit_chart / extend timed hook (TEST_PLAN A16, A17; API.md "Spec v2.4 clarifications" 5 and 6).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 31, via sys.path edit)
- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 32, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 33, via sys.path edit)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)
- `scipy` (lines 24)

### Standard library

- `__future__` (lines 14)
- `itertools` (lines 16)
- `json` (lines 17)
- `math` (lines 18)
- `pathlib` (lines 20)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `ARRAY_FIELDS`
- `A_K4`
- `CHART_KEYS`
- `D1_K4`
- `EXACT_K4`
- `FIT_LABELS`
- `INFO_KEYS`
- `K4_EDGES`
- `K4_TRIS`
- `P`
- `PKG`
- `REPO_ROOT`
- `THETA`
- `TWO_PI`

## Classes and functions

- **function `make_cfg`** [L53-58]: `def make_cfg(**overrides)`
- **function `as_int`** [L61-62]: `def as_int(values)`
- **function `edge_index`** [L65-66]: `def edge_index(edges)`
- **function `triangle_sums`** [L69-73]: `def triangle_sums(c, edges, triangles)`
- **function `reference_d1`** [L76-86]: `def reference_d1(edges, triangles)`
- **class `SeqClock`** [L89-98] - Returns `values` in order, then `tail` forever; counts readings.
- **method `SeqClock.__init__`** [L92-94]: `def __init__(self, values=(), tail=0.0)`
- **method `SeqClock.__call__`** [L96-98]: `def __call__(self)`
- **class `Marker(Exception)`** [L101-102]
- **function `lift`** [L112-114]: `def lift(a, clock, guard=None, cfg=None)`
- **test `test_fixture_defects`** [L117-119]: `def test_fixture_defects()`
- **test `test_a16_closed_branch_past_cap_at_return_is_unresolved`** [L124-128]: `def test_a16_closed_branch_past_cap_at_return_is_unresolved(late)` decorators: @pytest.mark.parametrize('late', [31.0, 30.0])
- **test `test_a16_closed_branch_below_cap_returns_exact_lift`** [L131-137]: `def test_a16_closed_branch_below_cap_returns_exact_lift()`
- **test `test_a16_closed_branch_cap_only_at_final_check`** [L140-146]: `def test_a16_closed_branch_cap_only_at_final_check()`
- **test `test_a16_corrected_branch_cap_only_at_final_check`** [L150-165]: `def test_a16_corrected_branch_cap_only_at_final_check(overrides)` decorators: @pytest.mark.parametrize('overrides', [{}, {'local_passes': 0}])
- **test `test_a16_first_clock_call_precedes_defect`** [L168-178]: `def test_a16_first_clock_call_precedes_defect()`
- **function `circle_points`** [L185-188]: `def circle_points(theta)`
- **function `make_ids`** [L191-192]: `def make_ids(n)`
- **class `RecordingTimed`** [L195-204]
- **method `RecordingTimed.__init__`** [L196-197]: `def __init__(self, raise_at=None, error=None)`
- **method `RecordingTimed.__call__`** [L199-204]: `def __call__(self, label, fn)`
- **function `plain_chart`** [L208-209]: `def plain_chart()` decorators: @pytest.fixture(scope='module')
- **test `test_a17_fit_chart_labels_in_order_and_same_chart`** [L212-224]: `def test_a17_fit_chart_labels_in_order_and_same_chart(plain_chart)`
- **test `test_a17_timed_exception_propagates_and_stops`** [L227-233]: `def test_a17_timed_exception_propagates_and_stops()`
- **test `test_a17_extend_wraps_extension_distance`** [L236-245]: `def test_a17_extend_wraps_extension_distance(plain_chart)`

