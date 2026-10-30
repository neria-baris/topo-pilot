# `tests/hwsc/test_b_records.py`

- Source: [tests/hwsc/test_b_records.py](../../../../../tests/hwsc/test_b_records.py)
- Kind: python
- Lines: 400

## Module docstring

> Author B (job 0176): records, the gate runner, lineage, authority records, the study
> ledger, pauses, the D6 export (RESULT.json and SEALED_OPENED.json) and the HANDOFF reader.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 26, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 27, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 28, via sys.path edit)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](../../tools/hwsc/hwsc_driver.py.md) (line 29, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 30, via unique basename)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 32, via unique basename)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../../tools/hwsb/hwsb_driver.py.md) (line 33, via unique basename)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 34, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 35, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 36, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 37, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 38, via unique basename)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 39, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 15)
- `hashlib` (lines 10)
- `json` (lines 11)
- `math` (lines 12)
- `pathlib` (lines 16)
- `sys` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `import errors` (line 31): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- line 24: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `ADD34`
- `C`
- `CENTRAL`
- `CUMUL`
- `GF`
- `REPO`
- `SCHED`
- `_HWSC`

## Classes and functions

- **function `_sha`** [L45-46]: `def _sha(p)`
- **function `_events`** [L49-51]: `def _events(out)`
- **function `_gates`** [L54-55]: `def _gates(out)`
- **function `_sf`** [L59-60]: `def _sf(code)`
- **test `test_status_of`** [L75-76]: `def test_status_of(exc, status)` decorators: @pytest.mark.parametrize('exc,status', [(GF('INCONCLUSIVE/HEADROOM', 'r'), 'INCONCLUSIVE/HEADROOM'), (GF('FAIL_TECHNICAL/ORACLE', 'r'), 'FAIL_TECHNICAL/ORACLE'), (hwsb_config.HwsbStop('FAIL_TECHNICAL/HOLD', 'r'), 'FAIL_TECHNICAL/HOLD'), (hwsb_config.HwsbStop('INCONCLUSIVE/RESOURCE_OR_AUTHORITY', 'r'), 'INCONCLUSIVE/RESOURCE_OR_AUTHORITY'), (hws_worlds.HwsStop('FAIL_TECHNICAL/IDENTITY', 'r'), 'FAIL_TECHNICAL/IDENTITY'), (_sf(ErrorCode.NONFINITE_LOSS), 'FAIL_TECHNICAL/NONFINITE'), (_sf(ErrorCode.SPLIT_OVERLAP), 'FAIL_TECHNICAL/LINEAGE'), (hwsb_driver.Paused('KC: STAGE'), 'PAUSE'), (RuntimeError('bare'), 'FAIL_TECHNICAL/UNEXPECTED')])
- **test `test_status_of_other_exceptions_follow_classify_exception`** [L79-83]: `def test_status_of_other_exceptions_follow_classify_exception()`
- **function `_steps`** [L87-102]: `def _steps(calls, mid)`
- **test `test_run_gates_stops_at_first_non_pass`** [L107-113]: `def test_run_gates_stops_at_first_non_pass(tmp_path, mid, status)` decorators: @pytest.mark.parametrize('mid,status', [(GF('INCONCLUSIVE/HEADROOM', 'r'), 'INCONCLUSIVE/HEADROOM'), ('FAIL_TECHNICAL/ORACLE', 'FAIL_TECHNICAL/ORACLE')])
- **test `test_run_gates_dry_continue_calls_later_gates`** [L116-120]: `def test_run_gates_dry_continue_calls_later_gates(tmp_path)`
- **test `test_run_gates_pause_is_recorded_and_stops`** [L123-130]: `def test_run_gates_pause_is_recorded_and_stops(tmp_path)`
- **function `_recorded_store`** [L134-146]: `def _recorded_store(out)`
- **test `test_lineage_absent_and_recorded`** [L149-153]: `def test_lineage_absent_and_recorded(tmp_path)`
- **test `test_lineage_unrecorded_file_fails`** [L156-163]: `def test_lineage_unrecorded_file_fails(tmp_path)`
- **test `test_lineage_superseded_manifest`** [L166-180]: `def test_lineage_superseded_manifest(tmp_path)`
- **test `test_auth_ok_refusals`** [L188-193]: `def test_auth_ok_refusals(stage)` decorators: @pytest.mark.parametrize('stage', ['KC', 'TRAIN', 'E1', 'REG2', 'E2'])
- **test `test_sched_ok_rules`** [L202-208]: `def test_sched_ok_rules(stage)` decorators: @pytest.mark.parametrize('stage', ['DRY', 'KC', 'TRAIN', 'E1', 'REG2', 'E2'])
- **test `test_ledger_read_default`** [L212-214]: `def test_ledger_read_default(tmp_path)`
- **test `test_ledger_append_atomic_cumulative_and_unique`** [L217-230]: `def test_ledger_append_atomic_cumulative_and_unique(tmp_path)`
- **test `test_pause_check_thresholds_and_strictness`** [L239-251]: `def test_pause_check_thresholds_and_strictness(stage)` decorators: @pytest.mark.parametrize('stage', list(CENTRAL))
- **test `test_pause_check_e2_from_k`** [L255-260]: `def test_pause_check_e2_from_k(k)` decorators: @pytest.mark.parametrize('k', [1, 2, 4])
- **test `test_pause_or_raise_writes_cpu_only_gate`** [L263-275]: `def test_pause_or_raise_writes_cpu_only_gate(tmp_path)`
- **test `test_pause_or_raise_exempt_and_disabled`** [L278-287]: `def test_pause_or_raise_exempt_and_disabled(tmp_path)`
- **function `_endpoint`** [L291-294]: `def _endpoint()`
- **function `_state`** [L297-299]: `def _state(result)`
- **test `test_export_writes_result_and_sealed_opened_in_one_s8_event`** [L302-334]: `def test_export_writes_result_and_sealed_opened_in_one_s8_event(tmp_path)`
- **test `test_export_without_sealed_validation_fails`** [L337-344]: `def test_export_without_sealed_validation_fails(tmp_path)`
- **test `test_sealed_keys_refused_anywhere`** [L348-354]: `def test_sealed_keys_refused_anywhere(key)` decorators: @pytest.mark.parametrize('key', list(k4b_stats.SEALED_KEYS))
- **test `test_load_handoff_real`** [L358-368]: `def test_load_handoff_real()`
- **function `_variant`** [L371-376]: `def _variant(tmp_path, name, mutate)`
- **test `test_load_handoff_refuses_structure`** [L384-388]: `def test_load_handoff_refuses_structure(tmp_path, name, mutate)` decorators: @pytest.mark.parametrize('name,mutate', [('forbidden.json', lambda d: d['store_inventory'].update({'x/y.npz': {'dev_ce': 1.0}})), ('forbidden2.json', lambda d: d.update(registry_obligation={'note': {'captured': 0.5}})), ('extra.json', lambda d: d.update(extra_key=1)), ('missing.json', lambda d: d.pop('k_C'))])
- **test `test_load_handoff_sha_checked`** [L391-400]: `def test_load_handoff_sha_checked(tmp_path)`

