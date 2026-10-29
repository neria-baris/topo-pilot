# `tools/k4b/k4b_release.py`

- Source: [tools/k4b/k4b_release.py](../../../../../tools/k4b/k4b_release.py)
- Kind: python
- Lines: 229

## Module docstring

> K4b releases, pin check, freeze, reservation records and the rerun/lineage rule (API.md §12.1).

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 18, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 20, via unique basename)

### External (third-party)

- `numpy` (lines 92)

### Standard library

- `__future__` (lines 7)
- `hashlib` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 16)
- `platform` (lines 11)
- `shutil` (lines 12)
- `subprocess` (lines 13)
- `sys` (lines 14)
- `time` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 36, import)
- [tests/hwsc/test_b_registry2.py](../../tests/hwsc/test_b_registry2.py.md) (line 31, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 36, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 27, import)
- [tests/k4b/test_b_rerun.py](../../tests/k4b/test_b_rerun.py.md) (line 25, import)
- [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 19, import)
- [tools/hwsc/hwsc_driver.py](../hwsc/hwsc_driver.py.md) (line 21, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 29, import)
- [tools/hwsc/hwsc_dry3.py](../hwsc/hwsc_dry3.py.md) (line 19, import)
- [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 24, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 20, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 22, import)
- [tools/k4b/k4b_meter_bind.py](k4b_meter_bind.py.md) (line 123, import)

## Top-level constants

- `AUTHORITY`
- `FIELDS`
- `FIELDS_B`
- `FREE_DIRS`
- `LINEAGE`
- `RECORD_FILES`

## Classes and functions

- **function `_sha_bytes`** [L34-35]: `def _sha_bytes(data: bytes) -> str`
- **function `authorized_worker`** [L38-40]: `def authorized_worker(release, session) -> bool`
- **function `verify_release`** [L43-62]: `def verify_release(path, kind, task_sha256, session, freeze_path=None) -> dict`
- **function `_git`** [L65-66]: `def _git(repo, *args) -> bytes`
- **function `_chart_section`** [L69-70]: `def _chart_section(repo, ref) -> dict`
- **function `pin_check`** [L73-88]: `def pin_check(repo, r_ref, h_exec) -> dict` - S0 (§11.5): only allowlisted additions on the protected paths; reuse hashes at h_exec.
- **function `environment`** [L91-95]: `def environment() -> dict`
- **function `accept_tests`** [L98-104]: `def accept_tests(out, record) -> str` - tests/ACCEPTED.json (exclusive create): counts, junit and the sha256 of every test file.
- **function `freeze`** [L107-121]: `def freeze(out, repo, h_exec, accepted_sha256=None) -> dict` - FREEZE.json (exclusive create): protocol, h_exec, k4b and reuse file sha256, environment.
- **function `start_reservation`** [L124-128]: `def start_reservation(path, scope, utc) -> dict`
- **function `verify_reservation`** [L131-142]: `def verify_reservation(path, release, sampling_began=False) -> dict`
- **function `archive_attempt`** [L145-165]: `def archive_attempt(out, job, files, record_suffixes) -> Path` - §11.8: move the attempt's files and record suffixes to superseded/<job>/ + SHA256SUMS.
- **function `restore_records`** [L168-173]: `def restore_records(out, verified) -> None`
- **function `_superseded_ok`** [L176-191]: `def _superseded_ok(out) -> list`
- **function `lineage_ok`** [L194-217]: `def lineage_ok(out) -> dict` - PASS iff the store is absent or holds only this lineage's recorded files (§11.8 item 7).
- **function `regenerated_identical`** [L220-223]: `def regenerated_identical(old_sha, new_path) -> bool`
- **function `needs_owner`** [L226-229]: `def needs_owner(correction) -> bool` - True iff an outcome-bearing quantity would change, or was computed at/after failure.

