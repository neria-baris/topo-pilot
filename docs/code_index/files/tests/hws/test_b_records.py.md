# `tests/hws/test_b_records.py`

- Source: [tests/hws/test_b_records.py](../../../../../tests/hws/test_b_records.py)
- Kind: python
- Lines: 353

## Module docstring

> Author B (job 0119), TEST_PLAN §3 `test_b_records.py` and `test_b_meter.py` (merged: job
> 0119 task.md allows at most five author-B files; the G0 seed-search tests live in
> `test_b_kc1.py`). Records: STAGES.jsonl line format, `save_hist` paths and the canon32 key,
> exclusive-create refusals, `tree_sha`, `archive_partial` with SHA256SUMS, resume regenerating an
> interrupted synthetic world bit-identically, FREEZE.json fields and the implementation hash,
> `main` refusals (exit 2, nothing sampled), the pytest basetemp outside the project root.
> Meter (§9.2 RC-9, DR12): `hm.bind` (MEMORY_CAP 8 GiB, TEMP_ROOT = out), `effective_settings`,
> `main` (--max-cpu inf --max-wall inf, child env, RUN.lock refusal) with meter.main faked.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 29, via sys.path edit)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../../tools/hws/hws_oracle.py.md) (line 30, via sys.path edit)
- `import hws_driver` -> [tools/hws/hws_driver.py](../../tools/hws/hws_driver.py.md) (line 31, via sys.path edit)
- `import hws_meter_bind` -> [tools/hws/hws_meter_bind.py](../../tools/hws/hws_meter_bind.py.md) (line 32, via sys.path edit)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 34, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 35, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 36, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 37, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 38, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 39, via unique basename)
- `from topo_pilot.contracts import SequenceLayout, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 40, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 41, via package root)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 13)
- `hashlib` (lines 15)
- `json` (lines 16)
- `os` (lines 17)
- `pathlib` (lines 20)
- `subprocess` (lines 18)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO / 'tools' / 'hws')` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `GIB`
- `INF`
- `REPO`
- `TINY`

## Classes and functions

- **function `_sha_bytes`** [L49-50]: `def _sha_bytes(data: bytes) -> str`
- **function `_put`** [L53-56]: `def _put(path: Path, data: bytes) -> Path`
- **function `_under`** [L59-62]: `def _under(p: Path, root: Path) -> bool`
- **function `_code`** [L65-69]: `def _code(fn, *args) -> int`
- **function `_event`** [L72-75]: `def _event(kind: str, **fields) -> dict`
- **test `test_pytest_basetemp_is_outside_the_project_root`** [L80-82]: `def test_pytest_basetemp_is_outside_the_project_root(tmp_path)`
- **test `test_append_stage_event_line_format`** [L85-101]: `def test_append_stage_event_line_format(tmp_path)`
- **test `test_save_hist_paths_key_and_exclusive_create`** [L104-117]: `def test_save_hist_paths_key_and_exclusive_create(tmp_path)`
- **test `test_reused_writers_refuse_existing_paths`** [L120-127]: `def test_reused_writers_refuse_existing_paths(tmp_path)`
- **test `test_tree_sha_definition`** [L130-143]: `def test_tree_sha_definition(tmp_path)`
- **function `_partial_store`** [L146-158]: `def _partial_store(out: Path) -> dict`
- **test `test_archive_partial_moves_only_unlisted_files`** [L161-176]: `def test_archive_partial_moves_only_unlisted_files(tmp_path)`
- **test `test_resume_regenerates_the_interrupted_world_bit_identically`** [L179-194]: `def test_resume_regenerates_the_interrupted_world_bit_identically(tmp_path)`
- **function `_git`** [L197-199]: `def _git(*args) -> str`
- **test `test_freeze_fields_and_implementation_hash`** [L202-235]: `def test_freeze_fields_and_implementation_hash(tmp_path)`
- **test `test_main_refuses_without_freeze_auth_or_accept`** [L238-259]: `def test_main_refuses_without_freeze_auth_or_accept(tmp_path, monkeypatch)`
- **function `preserved`** [L265-281]: `def preserved(monkeypatch)` decorators: @pytest.fixture
- **test `test_bind_sets_the_hws_values`** [L284-301]: `def test_bind_sets_the_hws_values(tmp_path, preserved)`
- **test `test_bind_to_the_dry_store_puts_child_temp_on_x`** [L304-308]: `def test_bind_to_the_dry_store_puts_child_temp_on_x(preserved)`
- **function `_argv`** [L311-313]: `def _argv(out, *extra)`
- **test `test_main_binds_and_hands_over_to_the_meter`** [L316-337]: `def test_main_binds_and_hands_over_to_the_meter(tmp_path, preserved)`
- **test `test_main_refuses_a_foreign_run_lock_and_missing_out`** [L340-353]: `def test_main_refuses_a_foreign_run_lock_and_missing_out(tmp_path, preserved)`

