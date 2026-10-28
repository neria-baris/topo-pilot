# `tools/c1prime/c1_records.py`

- Source: [tools/c1prime/c1_records.py](../../../../../tools/c1prime/c1_records.py)
- Kind: python
- Lines: 242

## Module docstring

> C1' stage records, gate boundary and exception mapping (API.md §2; protocol §16 conventions,
> §18 field 2). Reuses K4 stage_records unchanged with the C1 PREREQUISITE rebinding and the C1
> PASS-gate-set checks; classifies every exception before recording (run_gate is not relied on).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 12, via unique basename)
- `from oracle_profile import ProfileError` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 14, via unique basename)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 16, via package root)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 5)
- `decimal` (lines 7)
- `math` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `from errors import Invalid, JoinError, Unresolved` (line 13): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 34, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 30, import)
- [tests/c1prime/test_a_chart_val.py](../../tests/c1prime/test_a_chart_val.py.md) (line 31, import)
- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 31, import)
- [tests/c1prime/test_a_gates.py](../../tests/c1prime/test_a_gates.py.md) (line 24, import)
- [tests/c1prime/test_b_cert_oracle.py](../../tests/c1prime/test_b_cert_oracle.py.md) (line 35, import)
- [tests/c1prime/test_b_decoder.py](../../tests/c1prime/test_b_decoder.py.md) (line 33, import)
- [tests/c1prime/test_b_fwl.py](../../tests/c1prime/test_b_fwl.py.md) (line 28, import)
- [tests/c1prime/test_b_inference.py](../../tests/c1prime/test_b_inference.py.md) (line 31, import)
- [tests/c2_nd/test_b_policy.py](../../tests/c2_nd/test_b_policy.py.md) (line 23, import)
- [tests/c2_readout/test_b_policy.py](../../tests/c2_readout/test_b_policy.py.md) (line 29, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 30, import)
- [tests/k4b/test_a_transport_bound.py](../../tests/k4b/test_a_transport_bound.py.md) (line 29, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 27, import)
- [tests/k4b/test_b_data.py](../../tests/k4b/test_b_data.py.md) (line 25, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 31, import)
- [tests/k4b/test_b_h1_meta.py](../../tests/k4b/test_b_h1_meta.py.md) (line 31, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 31, import)
- [tests/k4b/test_b_registry.py](../../tests/k4b/test_b_registry.py.md) (line 32, import)
- [tests/k4b/test_b_registry_fixes.py](../../tests/k4b/test_b_registry_fixes.py.md) (line 31, import)
- [tests/k4b/test_b_registry_rules.py](../../tests/k4b/test_b_registry_rules.py.md) (line 35, import)
- [tests/k4b/test_b_rerun.py](../../tests/k4b/test_b_rerun.py.md) (line 27, import)
- [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 18, import)
- [tools/c1prime/c1_chart.py](c1_chart.py.md) (line 14, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 22, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 20, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 21, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 22, import)
- [tools/c1prime/c1_fit.py](c1_fit.py.md) (line 10, import)
- [tools/c1prime/c1_means.py](c1_means.py.md) (line 12, import)
- [tools/c1prime/c1_model.py](c1_model.py.md) (line 12, import)
- [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 15, import)
- [tools/c2_nd/nd_attrib.py](../c2_nd/nd_attrib.py.md) (line 23, import)
- [tools/c2_nd/nd_driver.py](../c2_nd/nd_driver.py.md) (line 27, import)
- [tools/c2_nd/nd_dry.py](../c2_nd/nd_dry.py.md) (line 34, import)
- [tools/c2_nd/nd_split.py](../c2_nd/nd_split.py.md) (line 31, import)
- [tools/c2_nd/nd_stage_base.py](../c2_nd/nd_stage_base.py.md) (line 29, import)
- [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 23, import)
- [tools/c2_readout/c2_driver.py](../c2_readout/c2_driver.py.md) (line 25, import)
- [tools/c2_readout/c2_stage_pre.py](../c2_readout/c2_stage_pre.py.md) (line 28, import)
- [tools/hws/hws_driver.py](../hws/hws_driver.py.md) (line 331, import)
- [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 64, import)
- [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 18, import)
- [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 18, import)
- [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 29, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 15, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 27, import)
- [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 28, import)
- [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 21, import)
- [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 20, import)
- [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 13, import)
- [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 19, import)

## Top-level constants

- `COCYCLE_MESSAGE`
- `GATE_ORDER`
- `PREREQUISITE`
- `REQUIRED_PASS`
- `STAGE_GATES`

## Classes and functions

- **class `C1GateFailure(Exception)`** [L36-41] - A declared unmet criterion or defect raised by a C1 kernel (.status is the full status).
- **method `C1GateFailure.__init__`** [L39-41]: `def __init__(self, status: str, reason: str = '')`
- **class `CertificateFlag(Exception)`** [L44-45] - A watched Decimal flag in a certificate computation (P3).
- **class `C1Stop(Exception)`** [L48-53] - The first non-PASS gate stops the cohort.
- **method `C1Stop.__init__`** [L51-53]: `def __init__(self, gate: str, status: str, reason: str = '')`
- **function `bind_stage_records`** [L56-58]: `def bind_stage_records()`
- **function `check_pass_set`** [L61-70]: `def check_pass_set(out, stage) -> None`
- **function `begin_stage`** [L73-77]: `def begin_stage(out, stage, models) -> None`
- **function `_code`** [L80-82]: `def _code(exc) -> str`
- **function `classify_exception`** [L85-108]: `def classify_exception(exc) -> tuple` - The §16 exception mapping (review fix 5) -> (status, reason).
- **function `_frames`** [L111-115]: `def _frames(exc)`
- **function `_raised_in`** [L118-119]: `def _raised_in(exc, module_name: str) -> bool`
- **function `_frame_of`** [L122-127]: `def _frame_of(exc, func: str)`
- **function `smoothing_diagnostics`** [L130-140]: `def smoothing_diagnostics(exc)` - f and residual from the failed smooth_phase frame (never rerun); None if unavailable.
- **function `adapt_chart_exception`** [L143-158]: `def adapt_chart_exception(exc)` - The two chart-specific Invalid cases of §14 / rulings 1, 2, 6; else None.
- **function `_operation`** [L161-165]: `def _operation(exc) -> str`
- **function `_record`** [L168-171]: `def _record(out, gate, full, reason, **extra) -> None`
- **function `run_c1_gate`** [L174-194]: `def run_c1_gate(out, gate, fn, chart=False)` - Run fn(); classify and record any failure, then raise C1Stop; record a returned status.
- **function `_jsonable`** [L197-206]: `def _jsonable(x)`
- **class `LogitPolicy`** [L209-242] - The computation-order rule (§2.2) as a gate-indexed permission (API.md §2).
- **method `LogitPolicy.__init__`** [L217-218]: `def __init__(self, done=())`
- **method `LogitPolicy.begin`** [L220-228]: `def begin(self, gate: str) -> None`
- **method `LogitPolicy.passed`** [L230-234]: `def passed(self, gate: str) -> None`
- **method `LogitPolicy.require`** [L236-242]: `def require(self, kind: str) -> None`

