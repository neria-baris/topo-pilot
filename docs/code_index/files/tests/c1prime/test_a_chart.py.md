# `tests/c1prime/test_a_chart.py`

- Source: [tests/c1prime/test_a_chart.py](../../../../../tests/c1prime/test_a_chart.py)
- Kind: python
- Lines: 303

## Module docstring

> Independent tests, author A (job 0026): the C1' chart wrapper (TEST_PLAN A-1 items 1-4 and 9).

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 32, via sys.path edit)
- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 33, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 34, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 35, via sys.path edit)
- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 36, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 37, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 38, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)
- `ripser` (lines 20)
- `scipy` (lines 21, 22)

### Standard library

- `__future__` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 28: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 30: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `ADDED_INFO`
- `ARRAYS`
- `FIELD`
- `REPO`

## Classes and functions

- **function `make_ids`** [L47-49]: `def make_ids(n, base=10 ** 9)` - 20-digit zero-padded sequence-id strings (protocol section 14, correction C-15).
- **function `loop_points`** [L52-67]: `def loop_points(m, width=8.0)` - m points on the perimeter (length m) of a (m/2 - width) x width rectangle, jittered.
- **function `with_satellites`** [L70-80]: `def with_satellites(m_loop, n_sat, n=512)` - Loop plus n_sat isolated satellites at interleaved landmark positions 7, 27, 47, ...
- **function `chain_and_ring`** [L83-90]: `def chain_and_ring()` - 492-point straight chain (spacing 0.9) and a 20-point unit ring 1000 beyond its end, in
- **function `my_components`** [L93-95]: `def my_components(E, n)`
- **function `reference_geometry`** [L98-111]: `def reference_geometry(X)` - Section 14 steps 1-4 with the frozen kernels, computed independently of c1_chart.
- **class `Recorder`** [L114-125] - persist(name, dict) callable that keeps every record in call order.
- **method `Recorder.__init__`** [L117-118]: `def __init__(self)`
- **method `Recorder.__call__`** [L120-121]: `def __call__(self, name, record)`
- **method `Recorder.names`** [L124-125]: `def names(self)` decorators: @property
- **function `pick`** [L128-133]: `def pick(record, *names)` - API.md names the giant-record fields but not their keys; accept protocol or info names.
- **function `check_giant_record`** [L136-148]: `def check_giant_record(rec, ref, ids, excluded_idx, m, passed)`
- **function `full_status`** [L151-157]: `def full_status(status, reason)` - Join a record's status prefix and reason suffix (API.md section 0).
- **function `innermost`** [L160-164]: `def innermost(exc)`
- **test `test_landmark_ids_are_20_digit_zero_padded_strings`** [L167-169]: `def test_landmark_ids_are_20_digit_zero_padded_strings()`
- **test `test_connected_graph_equals_fit_chart_bitwise`** [L172-193]: `def test_connected_graph_equals_fit_chart_bitwise()` - Item 1: m = n, so steps 1-9 are fit_chart's operations; only info gains keys.
- **test `test_components_partition_and_sizes`** [L196-207]: `def test_components_partition_and_sizes()`
- **test `test_giant_largest_component_ties_to_smallest_index`** [L219-221]: `def test_giant_largest_component_ties_to_smallest_index(labels, sizes, expected)` decorators: @pytest.mark.parametrize('labels, sizes, expected', [([0, 1, 1, 1, 2], [1, 3, 1], [1, 2, 3]), ([0, 0, 0, 1, 1, 1, 2], [3, 3, 1], [0, 1, 2]), ([1, 1, 1, 0, 0, 0, 2], [3, 3, 1], [0, 1, 2]), ([2, 0, 0, 1, 1, 2, 1, 0], [3, 3, 2], [1, 2, 7])])
- **test `test_restrict_reindexes_ascending_and_keeps_matching_cocycle_entries`** [L224-233]: `def test_restrict_reindexes_ascending_and_keeps_matching_cocycle_entries()`
- **test `test_giant_pass_integer_rule`** [L238-241]: `def test_giant_pass_integer_rule(m, n, ok)` decorators: @pytest.mark.parametrize('m, n, ok', [(487, 512, True), (486, 512, False), (512, 512, True), (95, 100, True), (94, 100, False), (19, 20, True)])
- **test `test_giant_486_of_512_stops_after_the_pre_raise_record`** [L244-267]: `def test_giant_486_of_512_stops_after_the_pre_raise_record(tmp_path)` - Item 3 (fail side): GIANT_BELOW_0.95, with the step-5 record persisted first.
- **test `test_trivial_restricted_class_stops_unresolved_after_lift_record`** [L270-291]: `def test_trivial_restricted_class_stops_unresolved_after_lift_record(tmp_path)` - Items 4 and 9: g = 0 on C* -> primitive_class raises Unresolved, which the chart gate
- **test `test_invalid_landmark_ids_are_a_technical_failure`** [L294-303]: `def test_invalid_landmark_ids_are_a_technical_failure(tmp_path)` - Input defects keep FAIL_TECHNICAL even at the chart boundary.

