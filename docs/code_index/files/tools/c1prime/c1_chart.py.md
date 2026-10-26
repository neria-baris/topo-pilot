# `tools/c1prime/c1_chart.py`

- Source: [tools/c1prime/c1_chart.py](../../../../../tools/c1prime/c1_chart.py)
- Kind: python
- Lines: 176

## Module docstring

> C1' chart: the frozen K4 construction restricted to the largest connected component at the
> selected bar's midpoint (API.md §3; protocol §14). Every step calls the frozen chart/cochain
> function named, unchanged, in fit_chart's order; persistence goes through an injected callable.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 11, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 14, via same directory)
- `from cochain import edge_list, integer_lift, primitive_class, smooth_phase, triangle_system` -> [tools/x4_circle_history/cochain.py](../x4_circle_history/cochain.py.md) (line 15, via unique basename)

### External (third-party)

- `numpy` (lines 12)
- `ripser` (lines 13)
- `scipy` (lines 16, 17)

### Standard library

- `__future__` (lines 5)
- `json` (lines 7)
- `pathlib` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 32, import)
- [tests/c1prime/test_a_chart_lcc512.py](../../tests/c1prime/test_a_chart_lcc512.py.md) (line 31, import)
- [tests/c1prime/test_a_chart_val.py](../../tests/c1prime/test_a_chart_val.py.md) (line 29, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 21, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 9, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 11, import)
- [tools/c2_readout/c2_stage_base.py](../c2_readout/c2_stage_base.py.md) (line 16, import)
- [tools/c2_readout/c2_stage_pre.py](../c2_readout/c2_stage_pre.py.md) (line 16, import)
- [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 13, import)

## Top-level constants

- `IDENTITY_CARRIER`
- `MAX_CONSTRUCTIONS`
- `ROLES`

## Classes and functions

- **function `landmark_ids`** [L24-25]: `def landmark_ids(seq_ids) -> np.ndarray`
- **class `ConstructionLedger`** [L28-50] - At most six constructions in total, one per (model, role); never retried (§14).
- **method `ConstructionLedger.__init__`** [L31-32]: `def __init__(self, path)`
- **method `ConstructionLedger.claims`** [L34-37]: `def claims(self) -> list`
- **method `ConstructionLedger.claim`** [L39-50]: `def claim(self, model, role) -> None`
- **function `components`** [L53-58]: `def components(edges, n) -> tuple`
- **function `giant`** [L61-67]: `def giant(labels, sizes) -> tuple` - Largest component; ties to the component containing the smallest index.
- **function `giant_pass`** [L70-71]: `def giant_pass(m, n=512) -> bool`
- **function `restrict`** [L74-81]: `def restrict(edges, cocycle, cstar, n) -> tuple`
- **function `_largest_finite_h0`** [L84-87]: `def _largest_finite_h0(dgm0) -> float`
- **function `fit_chart_lcc`** [L90-140]: `def fit_chart_lcc(X, ids, cfg, guard=None, timed=None, persist=None) -> chart.Chart` - §14 steps 1-10; equals chart.fit_chart bitwise (arrays, scalars) on a connected graph.
- **function `fit_production_gauge`** [L143-144]: `def fit_production_gauge(ch, m32_cstar) -> chart.Gauge`
- **function `serialise`** [L147-154]: `def serialise(ch, gauge, role) -> dict`
- **function `extend_phase`** [L157-158]: `def extend_phase(prod, gauge, Q, cfg, timed=None)`
- **function `c0_val`** [L161-176]: `def c0_val(prod, gauge, val_X, direct, cfg) -> dict` - The four C0-val criteria (§14) with the frozen kernels; chart_gates is never called.

