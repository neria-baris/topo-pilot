# `tests/experiment/test_s8_e4.py`

- Source: [tests/experiment/test_s8_e4.py](../../../../../tests/experiment/test_s8_e4.py)
- Kind: python
- Lines: 289

## Module docstring

> Stage S8 and the E4 report (TEST_PLAN X22-X25): stub memory stores, hand-computed values.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, GateCheck, GateReport, MetricRecords, MetricRow, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 12, via package root)
- `from topo_pilot.experiment import STAGE_REGISTRY` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 13, via package root)
- `from topo_pilot.experiment.report_e4 import build_e4` -> [src/topo_pilot/experiment/report_e4.py](../../src/topo_pilot/experiment/report_e4.py.md) (line 14, via package root)
- `from topo_pilot.experiment.report_e4_s7 import CIRC, circular_table, control_runs, control_table, probe_table, sensitivity_table` -> [src/topo_pilot/experiment/report_e4_s7.py](../../src/topo_pilot/experiment/report_e4_s7.py.md) (line 15, via package root)
- `from topo_pilot.experiment.s8 import TIMING_METRICS, RerunJob, compare_stores, integrity` -> [src/topo_pilot/experiment/s8.py](../../src/topo_pilot/experiment/s8.py.md) (line 23, via package root)

### External (third-party)

- `pytest` (lines 2)

### Standard library

- none

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

- `CONS`

## Classes and functions

- **function `_r`** [L30-31]: `def _r(metric, value, space='x', **kw)`
- **function `_rec`** [L34-36]: `def _rec(store, rows, parents=(), **config)`
- **function `_gate`** [L39-43]: `def _gate(store, stage, gate_id, verdict='pass', value=1.0)`
- **function `_row_value`** [L46-47]: `def _row_value(rows, space, metric)`
- **function `_mismatch_text`** [L50-51]: `def _mismatch_text(rows)`
- **function `_pair`** [L54-55]: `def _pair()`
- **test `test_X22_identical_stores_ok_and_every_type_counted`** [L60-73]: `def test_X22_identical_stores_ok_and_every_type_counted()`
- **test `test_X22_same_id_different_payload_is_checksum_mismatch`** [L76-84]: `def test_X22_same_id_different_payload_is_checksum_mismatch()`
- **test `test_X22_artifact_absent_from_main_is_missing`** [L87-97]: `def test_X22_artifact_absent_from_main_is_missing()`
- **test `test_X22_run_timing_differs_only_in_timing_rows_is_equal`** [L100-112]: `def test_X22_run_timing_differs_only_in_timing_rows_is_equal()`
- **test `test_X22_run_timing_with_other_row_differing_is_mismatch`** [L115-122]: `def test_X22_run_timing_with_other_row_differing_is_mismatch()`
- **test `test_X22_untimed_kind_differing_in_wall_time_is_mismatch`** [L125-129]: `def test_X22_untimed_kind_differing_in_wall_time_is_mismatch()`
- **test `test_X22_gate_reports_compared_by_gate_and_verdict_only`** [L132-144]: `def test_X22_gate_reports_compared_by_gate_and_verdict_only()`
- **test `test_X23_intact_store_ok_with_n_equal_n_verified`** [L149-158]: `def test_X23_intact_store_ok_with_n_equal_n_verified()`
- **test `test_X23_missing_parent_is_reported`** [L161-176]: `def test_X23_missing_parent_is_reported()`
- **test `test_X24_s8_registered_with_requires_and_gate`** [L181-184]: `def test_X24_s8_registered_with_requires_and_gate()`
- **class `_Cfg`** [L187-196]
- **method `_Cfg.__init__`** [L190-193]: `def __init__(self, s3_runs, identity)`
- **method `_Cfg.stage`** [L195-196]: `def stage(self, sid)`
- **test `test_X24_rerun_job_rejects_s3_runs_differing_from_identity_check`** [L199-206]: `def test_X24_rerun_job_rejects_s3_runs_differing_from_identity_check()`
- **test `test_X25_empty_store_prints_not_run_and_invents_nothing`** [L211-228]: `def test_X25_empty_store_prints_not_run_and_invents_nothing(tmp_path)`
- **test `test_X25_probe_table_hand_computed`** [L231-241]: `def test_X25_probe_table_hand_computed()`
- **test `test_X25_circular_table_hand_computed`** [L244-260]: `def test_X25_circular_table_hand_computed()`
- **test `test_X25_sensitivity_table_hand_computed`** [L263-276]: `def test_X25_sensitivity_table_hand_computed()`
- **test `test_X25_failed_control_run_prints_failed_reason`** [L279-289]: `def test_X25_failed_control_run_prints_failed_reason()`

