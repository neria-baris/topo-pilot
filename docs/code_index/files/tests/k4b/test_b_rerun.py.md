# `tests/k4b/test_b_rerun.py`

- Source: [tests/k4b/test_b_rerun.py](../../../../../tests/k4b/test_b_rerun.py)
- Kind: python
- Lines: 211

## Module docstring

> Author B, K4b TEST_PLAN B13 and B18: the §11.8 rerun and lineage rule. Superseded moves with
> a SHA256SUMS manifest, byte restore of the record files, refusal of unrecorded prior files,
> an interrupted stage without a terminal gate record, bit-identical regeneration and the
> owner-escalation rule (an unchanged quantity computed before the failure point alone does not
> escalate).

## Imports

### Internal (repo files)

- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 24, via sys.path edit)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 25, via sys.path edit)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 26, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 27, via sys.path edit)

### External (third-party)

- `pytest` (lines 22)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `LINEAGE`
- `REPO`
- `TRAINED`

## Classes and functions

- **function `sha`** [L33-34]: `def sha(path) -> str`
- **function `outcome`** [L37-42]: `def outcome(fn, *args, **kwargs)`
- **function `jl`** [L45-46]: `def jl(*entries) -> bytes`
- **function `attempt_store`** [L49-68]: `def attempt_store(tmp_path)` - A store whose S4a attempt failed technically after earlier PASS gates.
- **test `test_archive_attempt_moves_files_with_sha256sums`** [L73-85]: `def test_archive_attempt_moves_files_with_sha256sums(tmp_path)`
- **test `test_restore_records_is_byte_exact`** [L88-93]: `def test_restore_records_is_byte_exact(tmp_path)`
- **test `test_archived_suffixes_are_kept`** [L96-102]: `def test_archived_suffixes_are_kept(tmp_path)`
- **test `test_lineage_ok_absent_store_passes`** [L107-109]: `def test_lineage_ok_absent_store_passes(tmp_path)`
- **test `test_lineage_ok_empty_store_passes`** [L112-116]: `def test_lineage_ok_empty_store_passes(tmp_path)`
- **test `test_lineage_ok_refuses_unrecorded_prior_file`** [L119-124]: `def test_lineage_ok_refuses_unrecorded_prior_file(tmp_path)`
- **test `test_lineage_ok_accepts_exactly_the_superseded_manifest`** [L127-137]: `def test_lineage_ok_accepts_exactly_the_superseded_manifest(tmp_path)`
- **test `test_begin_and_complete_stage_records`** [L142-154]: `def test_begin_and_complete_stage_records(tmp_path)`
- **test `test_interrupted_stage_without_gate_record_is_replayed_under_rule`** [L157-175]: `def test_interrupted_stage_without_gate_record_is_replayed_under_rule(tmp_path)`
- **test `test_regenerated_identical`** [L178-191]: `def test_regenerated_identical(tmp_path)`
- **function `q`** [L196-198]: `def q(name, outcome_bearing=True, changed=False, at_or_after_failure=False)`
- **test `test_needs_owner`** [L210-211]: `def test_needs_owner(quantities, expected)` decorators: @pytest.mark.parametrize('quantities,expected', [([q('B4 bounds')], False), ([q('SD bounds'), q('N')], False), ([q('B4 bounds', changed=True)], True), ([q('chart-validation criteria', at_or_after_failure=True)], True), ([q('SD bounds'), q('endpoint means', at_or_after_failure=True)], True), ([q('OPERATIONS.jsonl', outcome_bearing=False, changed=True)], False), ([], False)])

