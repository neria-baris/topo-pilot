# `tests/x6_stage1/test_b_chain_ops.py`

- Source: [tests/x6_stage1/test_b_chain_ops.py](../../../../../tests/x6_stage1/test_b_chain_ops.py)
- Kind: python
- Lines: 396

## Module docstring

> Author B (operations): T-CHAIN (discovery, quarantine, marker), T-LINEAGE, T-ENV-LOCAL, T-METER,
> T-BUNDLE (classes, code.tar), T-INGEST (execution records) (X6S1-FROZEN-v1 §5, §12-§14; API.md).

## Imports

### Internal (repo files)

- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../../tools/x6_stage1/x6s1_cloud.py.md) (line 25, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 26, via sys.path edit)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](../../tools/x6_stage1/x6s1_ingest.py.md) (line 27, via sys.path edit)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](../../tools/x6_stage1/x6s1_run.py.md) (line 28, via sys.path edit)
- `import x6_store` -> [tools/x6_stage0/x6_store.py](../../tools/x6_stage0/x6_store.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)
- `torch` (lines 20)

### Standard library

- `__future__` (lines 6)
- `builtins` (lines 127)
- `hashlib` (lines 8)
- `io` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 16)
- `re` (lines 12)
- `subprocess` (lines 13)
- `sys` (lines 14)
- `tarfile` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`

## Imported by

- none

## Top-level constants

- `ENTRY`
- `ENV_KEYS`
- `MODEL`
- `PASTED`
- `REPO`
- `T`

## Classes and functions

- **function `_sha`** [L37-38]: `def _sha(b: bytes) -> str`
- **function `_fake_ckpt`** [L41-46]: `def _fake_ckpt(step)`
- **function `build_chain`** [L49-63]: `def build_chain(mdir, steps_list, entry=ENTRY)`
- **function `_names`** [L66-67]: `def _names(paths)`
- **function `_marker`** [L70-74]: `def _marker(mdir, recs)`
- **test `test_discover_full_chain_and_prefix`** [L78-90]: `def test_discover_full_chain_and_prefix(tmp_path)`
- **test `test_discover_lists_nonterminal_orphans`** [L97-115]: `def test_discover_lists_nonterminal_orphans(tmp_path, kind, name)` decorators: @pytest.mark.parametrize('kind,name', [('part_ckpt', '000004.pt.part'), ('part_rec', '000004.json.part'), ('ckpt_no_rec', '000004.pt'), ('rec_no_ckpt', '000004.json'), ('truncated', '000004.json')])
- **test `test_discover_broken_interior_link`** [L118-123]: `def test_discover_broken_interior_link(tmp_path)`
- **test `test_discover_read_failure_is_hold_then_stable_reread`** [L126-143]: `def test_discover_read_failure_is_hold_then_stable_reread(tmp_path, monkeypatch)`
- **test `test_terminal_marker_survives_quarantine`** [L146-169]: `def test_terminal_marker_survives_quarantine(tmp_path)`
- **test `test_quarantine_never_touches_chain_elements`** [L172-178]: `def test_quarantine_never_touches_chain_elements(tmp_path)`
- **test `test_unreadable_marker_stops_recovery`** [L182-194]: `def test_unreadable_marker_stops_recovery(tmp_path, bad)` decorators: @pytest.mark.parametrize('bad', ['garbage', 'tampered'])
- **function `_run_dir`** [L198-202]: `def _run_dir(store, payload=b'{"a":1}')`
- **test `test_supersede_manifest_and_bit_identical_regeneration`** [L205-223]: `def test_supersede_manifest_and_bit_identical_regeneration(tmp_path)`
- **test `test_volatile_fields_ignored_in_report_comparison`** [L226-235]: `def test_volatile_fields_ignored_in_report_comparison()`
- **test `test_regenerated_init_states_are_bit_identical`** [L238-241]: `def test_regenerated_init_states_are_bit_identical()`
- **test `test_retrain_route_refused_after_admission_or_any_local_evaluation`** [L244-264]: `def test_retrain_route_refused_after_admission_or_any_local_evaluation(tmp_path)`
- **function `_head`** [L268-270]: `def _head()`
- **test `test_env_local_record_complete`** [L273-282]: `def test_env_local_record_complete()`
- **test `test_env_changed_reports_only_real_changes`** [L285-289]: `def test_env_changed_reports_only_real_changes()`
- **test `test_evaluating_stage_record_holds_env_local`** [L292-300]: `def test_evaluating_stage_record_holds_env_local(tmp_path)`
- **test `test_meter_values`** [L304-308]: `def test_meter_values()`
- **test `test_meter_bind_check_refusals`** [L311-326]: `def test_meter_bind_check_refusals(tmp_path)`
- **test `test_forbidden`** [L337-338]: `def test_forbidden(rel, bad)` decorators: @pytest.mark.parametrize('rel,bad', [('data/val_NA.npy', True), ('data/test_NA.npy', True), ('data/gate_NA.npy', True), ('data/prefix.npy', True), ('data/dev_NA_s1.npy', True), ('sealed/learn.json', True), ('registry/X6-REG2.json', True), ('data/states.npy', True), ('data/latent_z.npy', True), ('Data/TEST_na.npy', True), ('notes.txt', True), ('code.tar', False), ('SHA256SUMS', False), ('ticket_C1.json', False), ('data/train_NA_s1.npy', False), ('init/init_s1.pt', False), ('data/smoke.npy', False), ('init/init_smoke.pt', False), ('X6S1_colab.ipynb', False)])
- **test `test_allowed_class`** [L348-349]: `def test_allowed_class(wave, rel, ok)` decorators: @pytest.mark.parametrize('wave,rel,ok', [('C1', 'data/train_NA_s1.npy', True), ('C1', 'data/train_ZC_s1.npy', True), ('C1', 'init/init_s2.pt', True), ('C1', 'data/train_NA_s3.npy', False), ('C1', 'data/train_AB_s1.npy', False), ('C1', 'init/init_s3.pt', False), ('C1', 'data/smoke.npy', False), ('C0', 'data/smoke.npy', True), ('C0', 'init/init_smoke.pt', True), ('C0', 'data/train_NA_s1.npy', False), ('C2', 'data/train_AB_s4.npy', True), ('C2', 'data/train_NA_s1.npy', False)])
- **test `test_code_tar_is_git_archive_of_head`** [L352-359]: `def test_code_tar_is_git_archive_of_head(tmp_path)`
- **function `_start`** [L367-369]: `def _start(seq, sid='s1')`
- **function `_final`** [L372-376]: `def _final(start, seq)`
- **test `test_check_execution_accepts_registered_sequences`** [L381-384]: `def test_check_execution_accepts_registered_sequences(seq)` decorators: @pytest.mark.parametrize('seq', [[1, 2, 3, 4, 5], [1, 2, 2, 3, 4, 5], [1, 2, 3, 4, 3, 4, 5], [1, PASTED, 3, 4, 5], [1, 1, 2, 3, 4, 5]])
- **test `test_check_execution_refuses_edits_extra_code_and_order`** [L389-390]: `def test_check_execution_refuses_edits_extra_code_and_order(seq)` decorators: @pytest.mark.parametrize('seq', [[1, 2, 3, T[3] + '\nprint(1)', 5], [1, 2, 3, 4, 'import os', 5], [1, 3, 2, 4, 5], [2, 3, 4, 5], [1, 2, 3, 5], [1, 2, 3, 4, 5, 6]])
- **test `test_check_execution_final_record_rules`** [L393-396]: `def test_check_execution_final_record_rules()`

