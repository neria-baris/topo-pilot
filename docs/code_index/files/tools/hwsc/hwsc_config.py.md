# `tools/hwsc/hwsc_config.py`

- Source: [tools/hwsc/hwsc_config.py](../../../../../tools/hwsc/hwsc_config.py)
- Kind: python
- Lines: 204

## Module docstring

> HWSC configuration: CONTRACT.json, constants, plans, HANDOFF loader, blindness guard (API.md §1).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 27, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `fnmatch` (lines 11)
- `fractions` (lines 15)
- `hashlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> not statically determinable

## Imported by

- [tests/hwsc/test_a_decision.py](../../tests/hwsc/test_a_decision.py.md) (line 24, import)
- [tests/hwsc/test_a_k4b_known_bound.py](../../tests/hwsc/test_a_k4b_known_bound.py.md) (line 30, import)
- [tests/hwsc/test_a_ladder.py](../../tests/hwsc/test_a_ladder.py.md) (line 23, import)
- [tests/hwsc/test_a_law.py](../../tests/hwsc/test_a_law.py.md) (line 23, import)
- [tests/hwsc/test_a_learning.py](../../tests/hwsc/test_a_learning.py.md) (line 25, import)
- [tests/hwsc/test_a_outcomes.py](../../tests/hwsc/test_a_outcomes.py.md) (line 22, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 24, import)
- [tests/hwsc/test_b_guard_meter.py](../../tests/hwsc/test_b_guard_meter.py.md) (line 26, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 26, import)
- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 24, import)
- [tests/hwsc/test_b_registry2.py](../../tests/hwsc/test_b_registry2.py.md) (line 24, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 22, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 24, import)
- [tests/hwsc/test_r_0178_dry_store_rule.py](../../tests/hwsc/test_r_0178_dry_store_rule.py.md) (line 15, import)
- [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 7, import)
- [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 7, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 7, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 8, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 6, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 6, import)
- [tools/hwsc/hwsc_drystore.py](hwsc_drystore.py.md) (line 12, import)
- [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 6, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 6, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 6, import)
- [tools/hwsc/hwsc_meter_bind.py](hwsc_meter_bind.py.md) (line 12, import)
- [tools/hwsc/hwsc_outcome.py](hwsc_outcome.py.md) (line 6, import)
- [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 7, import)
- [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 7, import)
- [tools/hwsc/hwsc_registry_build.py](hwsc_registry_build.py.md) (line 7, import)
- [tools/hwsc/hwsc_scratch.py](hwsc_scratch.py.md) (line 8, import)

## Top-level constants

- `ALPHA`
- `API_PATH`
- `BLINDED_DIRS`
- `BLINDED_FILES`
- `BLINDED_GLOBS`
- `CAP`
- `CONTRACT`
- `CONTRACT_PATH`
- `DISCLOSURE`
- `DRAWS`
- `DRY_MASTERS`
- `DRY_SEEDS`
- `DRY_STORE`
- `FLOOR`
- `HANDOFF_PATH`
- `HERE`
- `HOLD_FROM`
- `HOLD_S`
- `HWSB_STORE`
- `HWSC_PLAN`
- `HWS_STORE`
- `KEY`
- `KS`
- `LADDER`
- `LEARN`
- `M`
- `MAILBOX`
- `MASTERS`
- `NEEDLES`
- `NEIGHBOUR`
- `P1C_SEEDS`
- `PROCESS`
- `PROTOCOL_PATH`
- `PROTOCOL_SHA256`
- `RANKS`
- `REPO`
- `ROOT`
- `SCOPE`
- `SCRATCH`
- `SEEDS`
- `SELECTION_PATH`
- `SIGMA`
- `SIZES`
- `STEPS`
- `STORE`
- `STUDY_LEDGER`
- `TEST_PLAN_PATH`
- `_CHECKS`
- `_DRY_SIZES`
- `_FRACTION_KEYS`
- `_INT_KEYS`
- `_ORDER`

## Classes and functions

- **function `load_contract`** [L47-48]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `_forbidden_anywhere`** [L102-112]: `def _forbidden_anywhere(obj, forbidden) -> list`
- **function `load_handoff`** [L115-137]: `def load_handoff(path=HANDOFF_PATH, expected_sha256=None) -> dict`
- **function `dry_plan`** [L147-151]: `def dry_plan(kind, case)`
- **function `run_key`** [L154-157]: `def run_key(plan, master) -> tuple`
- **function `_posix`** [L167-168]: `def _posix(path) -> str`
- **function `blinded`** [L171-183]: `def blinded(path, root=ROOT) -> bool`
- **function `public_summary`** [L186-190]: `def public_summary(path) -> bool`
- **function `guard`** [L193-196]: `def guard(path, root=ROOT) -> Path`
- **function `read_bytes`** [L199-200]: `def read_bytes(path, root=ROOT) -> bytes`
- **function `read_json`** [L203-204]: `def read_json(path, root=ROOT)`

