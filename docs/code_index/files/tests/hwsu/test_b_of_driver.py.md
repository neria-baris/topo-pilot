# `tests/hwsu/test_b_of_driver.py`

- Source: [tests/hwsu/test_b_of_driver.py](../../../../../tests/hwsu/test_b_of_driver.py)
- Kind: python
- Lines: 307

## Module docstring

> Author B (job 0198): the OF job order, stopped-attempt obligations and reservation ends (D-17,
> J10 item 3), exit codes, and OF-P's stage-C identity binding (protocol §4.1 J6/J10, §3.1, §4.2
> OF-P; API §4, §9; D-11). TEST_PLAN §3 row test_b_of_driver; DRO1 order, DRO7, DRO9 (5).
> The gate computations are stubbed here (author A tests them); the records, obligations and
> reservations are real and written under tmp_path. The full tiny-world OF run is the DRO1 case.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 19, via sys.path edit)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](../../tools/hwsu/hwsu_driver_of.py.md) (line 20, via sys.path edit)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 21, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 22, via sys.path edit)
- `import hwsu_seed` -> [tools/hwsu/hwsu_seed.py](../../tools/hwsu/hwsu_seed.py.md) (line 23, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 24, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 25, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 26, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 7)
- `hashlib` (lines 101)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `GATES`
- `REPO`
- `STUB`
- `UTC`

## Classes and functions

- **function `_table`** [L35-39]: `def _table(b, sym)`
- **function `_world`** [L42-77]: `def _world(tmp_path, monkeypatch, fail=None, ofb=None)` - fail: {gate: exception or details dict}. Returns (root, out, calls).
- **function `_ctx`** [L80-82]: `def _ctx(root, out, attempt=1, rid='RES-HWSU-OF')`
- **function `_run`** [L85-89]: `def _run(root, out, attempt=1, rid='RES-HWSU-OF', reserve=True, **kw)`
- **function `_obl`** [L92-93]: `def _obl(out, name)`
- **function `_end`** [L96-97]: `def _end(out, rid)`
- **function `_sha`** [L100-102]: `def _sha(p)`
- **test `test_build_ctx`** [L106-114]: `def test_build_ctx(tmp_path)`
- **test `test_success_order_obligation_then_end`** [L118-139]: `def test_success_order_obligation_then_end(tmp_path, monkeypatch)`
- **test `test_share_dropped_gives_response_only`** [L142-147]: `def test_share_dropped_gives_response_only(tmp_path, monkeypatch)`
- **test `test_of_b_failure_writes_only_the_gate_line`** [L151-162]: `def test_of_b_failure_writes_only_the_gate_line(tmp_path, monkeypatch)`
- **test `test_stop_before_first_row_then_rerun`** [L165-186]: `def test_stop_before_first_row_then_rerun(tmp_path, monkeypatch)` - D-17 / J10 item 3: a no-history obligation ends RES-HWSU-OF; the rerun uses RES-HWSU-OF-a2.
- **test `test_of_0_failure_refused`** [L189-195]: `def test_of_0_failure_refused(tmp_path, monkeypatch)`
- **test `test_stop_after_rows_exit_codes_and_obligation`** [L204-212]: `def test_stop_after_rows_exit_codes_and_obligation(tmp_path, monkeypatch, gate, exc, code)` decorators: @pytest.mark.parametrize('gate,exc,code', [('OF-1', C1GateFailure('FAIL_TECHNICAL/ORACLE', 'KO3'), 3), ('OF-H', C1GateFailure('INCONCLUSIVE/REGISTRY_INCOMPLETE', 'sealed row'), 5), ('OF-2', C1GateFailure('INCONCLUSIVE/ORACLE_FEASIBILITY', 'headroom'), 5), ('OF-5', C1GateFailure('FAIL_TECHNICAL/SAMPLER', 'lemma P'), 3)])
- **test `test_pause_exit_4_with_obligation`** [L215-224]: `def test_pause_exit_4_with_obligation(tmp_path, monkeypatch)`
- **test `test_dry_continue_runs_every_gate`** [L227-233]: `def test_dry_continue_runs_every_gate(tmp_path, monkeypatch)`
- **test `test_main_unknown_subcommand`** [L236-241]: `def test_main_unknown_subcommand()`
- **function `real_ids`** [L246-248]: `def real_ids()` decorators: @pytest.fixture(scope='module')
- **function `_hwsc_meta`** [L251-261]: `def _hwsc_meta(hs, ids, skip=None, **bad)`
- **function `_of_p_status`** [L264-269]: `def _of_p_status(ctx)`
- **test `test_of_p_pass_and_explicit_masters`** [L272-291]: `def test_of_p_pass_and_explicit_masters(tmp_path, monkeypatch, real_ids)`
- **test `test_of_p_identity_failures`** [L295-307]: `def test_of_p_identity_failures(tmp_path, real_ids, case)` decorators: @pytest.mark.parametrize('case', ['missing_620302', 'replicate', 'atype', 'no_world'])

