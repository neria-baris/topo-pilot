# `tools/hwsd/hwsd_config.py`

- Source: [tools/hwsd/hwsd_config.py](../../../../../tools/hwsd/hwsd_config.py)
- Kind: python
- Lines: 256

## Module docstring

> HWSD configuration: CONTRACT.json, constants, registry tables, plans, blindness guard (API.md §1).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 29, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 30, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 31, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 32, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 33, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `copy` (lines 10)
- `dataclasses` (lines 11)
- `fnmatch` (lines 12)
- `fractions` (lines 16)
- `hashlib` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 17)
- `statistics` (lines 18)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> `tools/hwsc`, `tools/hwsd`
- line 27: `str(HERE)` -> `tools/hwsd`

## Imported by

- [tests/hwsd/test_a_bounds.py](../../tests/hwsd/test_a_bounds.py.md) (line 25, import)
- [tests/hwsd/test_a_evaluate.py](../../tests/hwsd/test_a_evaluate.py.md) (line 20, import)
- [tests/hwsd/test_a_kd4.py](../../tests/hwsd/test_a_kd4.py.md) (line 29, import)
- [tests/hwsd/test_a_known_bound.py](../../tests/hwsd/test_a_known_bound.py.md) (line 30, import)
- [tests/hwsd/test_a_learning.py](../../tests/hwsd/test_a_learning.py.md) (line 24, import)
- [tests/hwsd/test_a_onsets_order.py](../../tests/hwsd/test_a_onsets_order.py.md) (line 21, import)
- [tests/hwsd/test_a_scorer.py](../../tests/hwsd/test_a_scorer.py.md) (line 27, import)
- [tests/hwsd/test_a_statements.py](../../tests/hwsd/test_a_statements.py.md) (line 21, import)
- [tests/hwsd/test_b_binding.py](../../tests/hwsd/test_b_binding.py.md) (line 16, import)
- [tests/hwsd/test_b_data.py](../../tests/hwsd/test_b_data.py.md) (line 15, import)
- [tests/hwsd/test_b_guard_search.py](../../tests/hwsd/test_b_guard_search.py.md) (line 13, import)
- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 16, import)
- [tests/hwsd/test_b_registry_build.py](../../tests/hwsd/test_b_registry_build.py.md) (line 12, import)
- [tests/hwsd/test_b_registry_r10.py](../../tests/hwsd/test_b_registry_r10.py.md) (line 14, import)
- [tests/hwsd/test_b_registry_r9.py](../../tests/hwsd/test_b_registry_r9.py.md) (line 14, import)
- [tests/hwsd/test_b_reservation.py](../../tests/hwsd/test_b_reservation.py.md) (line 13, import)
- [tests/hwsd/test_b_util.py](../../tests/hwsd/test_b_util.py.md) (line 27, import)
- [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 6, import)
- [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 8, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 7, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 10, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 7, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 7, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 7, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 6, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 6, import)
- [tools/hwsd/hwsd_meter_bind.py](hwsd_meter_bind.py.md) (line 11, import)
- [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 7, import)
- [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 7, import)
- [tools/hwsd/hwsd_registry.py](hwsd_registry.py.md) (line 7, import)
- [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 7, import)
- [tools/hwsd/hwsd_statements.py](hwsd_statements.py.md) (line 9, import)
- [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 6, import)

## Top-level constants

- `API_PATH`
- `CHECKPOINTS`
- `CONTRACT`
- `CONTRACT_PATH`
- `DISCLOSURE`
- `DRY_MASTERS`
- `DRY_SEEDS`
- `DRY_STORE`
- `DRY_STRONG_SEED`
- `F_PLANTED`
- `HANDOFF_PATH`
- `HERE`
- `HWSC_STORE`
- `HWSU_STORE`
- `KEY`
- `K_OF`
- `MAILBOX`
- `MASTERS`
- `NEEDLES`
- `PROCESS`
- `PROTOCOL_PATH`
- `PROTOCOL_SHA256`
- `RANKS`
- `REPO`
- `RESERVATION_PREFIX`
- `ROOT`
- `SCRATCH`
- `SEEDS`
- `SIZES`
- `SPLITS`
- `STEPS`
- `STORE`
- `STRONG_RANKS`
- `STRONG_SEED`
- `STUDY_LEDGER`
- `TEST_PLAN_PATH`
- `TINY_PROCESS`
- `TRAIN_WHITELIST`
- `Z`
- `Z_S`
- `_T`

## Classes and functions

- **function `load_contract`** [L50-51]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `_import_checks`** [L89-109]: `def _import_checks() -> None`
- **function `_sha_file`** [L116-117]: `def _sha_file(path) -> str`
- **function `inherited_sha_ok`** [L120-122]: `def inherited_sha_ok() -> bool`
- **function `_need_inherit`** [L125-127]: `def _need_inherit() -> None`
- **function `scratch_table`** [L130-136]: `def scratch_table() -> dict`
- **function `root_table`** [L139-143]: `def root_table() -> dict`
- **function `dry_plan`** [L147-157]: `def dry_plan(kind, case)`
- **function `_posix`** [L161-162]: `def _posix(path) -> str`
- **function `_under`** [L165-166]: `def _under(p: str, d: str) -> bool`
- **function `blinded`** [L169-188]: `def blinded(path, root=ROOT, scratch=SCRATCH) -> bool`
- **function `search_pruned`** [L191-206]: `def search_pruned(path, root=ROOT, scratch=SCRATCH) -> bool`
- **function `public_summary`** [L209-210]: `def public_summary(path) -> bool`
- **function `guard`** [L213-216]: `def guard(path, root=ROOT) -> Path`
- **function `read_bytes`** [L219-220]: `def read_bytes(path, root=ROOT) -> bytes`
- **function `read_json`** [L223-224]: `def read_json(path, root=ROOT)`
- **function `read_train_record`** [L228-241]: `def read_train_record(master, store=HWSC_STORE) -> tuple`
- **function `read_obs_inventory`** [L244-256]: `def read_obs_inventory(store=HWSC_STORE, expected_sha256=None) -> dict`

