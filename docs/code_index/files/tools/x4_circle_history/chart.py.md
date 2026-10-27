# `tools/x4_circle_history/chart.py`

- Source: [tools/x4_circle_history/chart.py](../../../../../tools/x4_circle_history/chart.py)
- Kind: python
- Lines: 350

## Module docstring

> Fitted, certified circular chart with separate calibration gauge and transform (API.md).

## Imports

### Internal (repo files)

- `from cochain import edge_list, integer_lift, primitive_class, smooth_phase, triangle_system` -> [tools/x4_circle_history/cochain.py](cochain.py.md) (line 17, via same directory)
- `from errors import Invalid, Unresolved` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 18, via same directory)

### External (third-party)

- `numpy` (lines 15)
- `ripser` (lines 16)
- `scipy` (lines 19)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 13)
- `json` (lines 11)
- `math` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 35, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 31, import)
- [tests/c1prime/test_a_chart_lcc512.py](../../tests/c1prime/test_a_chart_lcc512.py.md) (line 33, import)
- [tests/c1prime/test_a_chart_val.py](../../tests/c1prime/test_a_chart_val.py.md) (line 32, import)
- [tests/circle_history/test_builder_v25.py](../../tests/circle_history/test_builder_v25.py.md) (line 22, import)
- [tests/circle_history/test_chart.py](../../tests/circle_history/test_chart.py.md) (line 26, import)
- [tests/circle_history/test_chart_arrays.py](../../tests/circle_history/test_chart_arrays.py.md) (line 23, import)
- [tests/circle_history/test_chart_extension.py](../../tests/circle_history/test_chart_extension.py.md) (line 26, import)
- [tests/circle_history/test_cochain_chart_v24.py](../../tests/circle_history/test_cochain_chart_v24.py.md) (line 31, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 23, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 28, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 22, import)
- [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 11, import)
- [tools/c1prime/c1_driver_cal.py](../c1prime/c1_driver_cal.py.md) (line 17, import)
- [tools/c2_nd/nd_stage_base.py](../c2_nd/nd_stage_base.py.md) (line 25, import)
- [tools/c2_readout/c2_stage_base.py](../c2_readout/c2_stage_base.py.md) (line 29, import)
- [tools/chart_diag/chart_diag.py](../chart_diag/chart_diag.py.md) (line 32, import)
- [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 14, import)
- [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 321, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 185, import)

## Top-level constants

- `TWO_PI`
- `_ARRAY_FIELDS`

## Classes and functions

- **function `_cmean`** [L24-30]: `def _cmean(values) -> complex` - Complex mean with each component summed then divided ONCE in IEEE double (correctly
- **function `_wrap`** [L33-37]: `def _wrap(phi) -> np.ndarray` - Phases in [0, 2pi): a modulo result that rounds to exactly 2pi becomes 0.0 (F4).
- **function `_cabs`** [L40-41]: `def _cabs(z: complex) -> float`
- **class `Chart`** [L45-59] decorators: @dataclass(frozen=True)
- **class `Gauge`** [L63-66] decorators: @dataclass(frozen=True)
- **class `Extension`** [L70-75] decorators: @dataclass(frozen=True)
- **function `select_h1_bar`** [L78-84]: `def select_h1_bar(dgm) -> int` - Index of the largest strictly positive finite lifetime; ties birth, death, index.
- **function `cocycle_to_edges`** [L87-98]: `def cocycle_to_edges(cocycle_rows, edges, p) -> np.ndarray` - Centred, oriented integer representative of a ripser F_p cocycle on ``edges``.
- **function `_neighbor_scale`** [L101-109]: `def _neighbor_scale(D)`
- **function `_check_landmarks`** [L112-119]: `def _check_landmarks(X, landmark_ids)`
- **function `fit_chart`** [L122-172]: `def fit_chart(X, landmark_ids, cfg, guard=None, timed=None) -> Chart` - Fixed-rule certified chart on all landmarks (API.md fit_chart).
- **function `fit_gauge`** [L175-189]: `def fit_gauge(chart: Chart, m32) -> Gauge` - Calibration-only reflection/rotation gauge (API.md fit_gauge).
- **function `apply_gauge`** [L192-193]: `def apply_gauge(phi, gauge: Gauge) -> np.ndarray`
- **function `extend`** [L196-220]: `def extend(chart: Chart, gauge: Gauge, Q, cfg, timed=None) -> Extension` - Out-of-sample phase by the fixed 8-nearest Gaussian rule (API.md extend; v2.4 timed).
- **function `agreement`** [L223-232]: `def agreement(phi_a, phi_b) -> float`
- **function `phase_bin_counts`** [L235-240]: `def phase_bin_counts(phi, bins: int = 12) -> np.ndarray`
- **function `overall_resultant`** [L243-247]: `def overall_resultant(phi) -> float`
- **function `_record`** [L250-256]: `def _record(met: bool, value, threshold) -> dict`
- **function `chart_gates`** [L259-286]: `def chart_gates(ext: Extension, direct_phi, cfg) -> dict` - Support, fidelity, bins and overall-resultant criteria (API.md chart_gates).
- **function `chart_to_arrays`** [L303-318]: `def chart_to_arrays(chart: Chart, gauge: Gauge) -> dict` - Arrays for an immutable NPZ; info travels as a JSON string in a unicode array (no pickle).
- **function `_jsonable`** [L321-326]: `def _jsonable(value)`
- **function `chart_from_arrays`** [L329-350]: `def chart_from_arrays(d) -> tuple[Chart, Gauge]`

