# `tools/hwsu/hwsu_config.py`

- Source: [tools/hwsu/hwsu_config.py](../../../../../tools/hwsu/hwsu_config.py)
- Kind: python
- Lines: 186

## Module docstring

> HWSU configuration: CONTRACT loader, constants, blindness guard, HANDOFF mirror (API.md §1).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 26, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 27, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `copy` (lines 9)
- `fnmatch` (lines 10)
- `fractions` (lines 14)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> not statically determinable

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 14, import)
- [tests/hwsu/test_a_of_ladder.py](../../tests/hwsu/test_a_of_ladder.py.md) (line 12, import)
- [tests/hwsu/test_a_of_lemmas.py](../../tests/hwsu/test_a_of_lemmas.py.md) (line 16, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 13, import)
- [tests/hwsu/test_a_of_sampler.py](../../tests/hwsu/test_a_of_sampler.py.md) (line 15, import)
- [tests/hwsu/test_a_u2_estimand.py](../../tests/hwsu/test_a_u2_estimand.py.md) (line 17, import)
- [tests/hwsu/test_a_u2_family.py](../../tests/hwsu/test_a_u2_family.py.md) (line 17, import)
- [tests/hwsu/test_a_u2_known.py](../../tests/hwsu/test_a_u2_known.py.md) (line 16, import)
- [tests/hwsu/test_a_u2_lemmas.py](../../tests/hwsu/test_a_u2_lemmas.py.md) (line 19, import)
- [tests/hwsu/test_a_u2_outcome.py](../../tests/hwsu/test_a_u2_outcome.py.md) (line 15, import)
- [tests/hwsu/test_a_u2_p1.py](../../tests/hwsu/test_a_u2_p1.py.md) (line 15, import)
- [tests/hwsu/test_a_u2_rules.py](../../tests/hwsu/test_a_u2_rules.py.md) (line 17, import)
- [tests/hwsu/test_b_of_bind.py](../../tests/hwsu/test_b_of_bind.py.md) (line 19, import)
- [tests/hwsu/test_b_of_config.py](../../tests/hwsu/test_b_of_config.py.md) (line 22, import)
- [tests/hwsu/test_b_of_driver.py](../../tests/hwsu/test_b_of_driver.py.md) (line 19, import)
- [tests/hwsu/test_b_of_freeze.py](../../tests/hwsu/test_b_of_freeze.py.md) (line 20, import)
- [tests/hwsu/test_b_of_meter.py](../../tests/hwsu/test_b_of_meter.py.md) (line 18, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 23, import)
- [tests/hwsu/test_b_of_records.py](../../tests/hwsu/test_b_of_records.py.md) (line 21, import)
- [tests/hwsu/test_b_of_registry.py](../../tests/hwsu/test_b_of_registry.py.md) (line 23, import)
- [tests/hwsu/test_b_of_reservations.py](../../tests/hwsu/test_b_of_reservations.py.md) (line 17, import)
- [tests/hwsu/test_b_of_seed.py](../../tests/hwsu/test_b_of_seed.py.md) (line 26, import)
- [tests/hwsu/test_b_of_streams.py](../../tests/hwsu/test_b_of_streams.py.md) (line 17, import)
- [tests/hwsu/test_b_u2_audit.py](../../tests/hwsu/test_b_u2_audit.py.md) (line 20, import)
- [tests/hwsu/test_b_u2_binding.py](../../tests/hwsu/test_b_u2_binding.py.md) (line 20, import)
- [tests/hwsu/test_b_u2_contract.py](../../tests/hwsu/test_b_u2_contract.py.md) (line 18, import)
- [tests/hwsu/test_b_u2_dx_policy.py](../../tests/hwsu/test_b_u2_dx_policy.py.md) (line 17, import)
- [tests/hwsu/test_b_u2_freeze.py](../../tests/hwsu/test_b_u2_freeze.py.md) (line 21, import)
- [tests/hwsu/test_b_u2_hwsd.py](../../tests/hwsu/test_b_u2_hwsd.py.md) (line 21, import)
- [tests/hwsu/test_b_u2_of_binding.py](../../tests/hwsu/test_b_u2_of_binding.py.md) (line 19, import)
- [tests/hwsu/test_b_u2_records.py](../../tests/hwsu/test_b_u2_records.py.md) (line 18, import)
- [tests/hwsu/test_b_u2_registry.py](../../tests/hwsu/test_b_u2_registry.py.md) (line 21, import)
- [tests/hwsu/test_impl_u2_mirror.py](../../tests/hwsu/test_impl_u2_mirror.py.md) (line 3, import)
- [tools/hwsu/hwsu_bind.py](hwsu_bind.py.md) (line 5, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 5, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 7, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 6, import)
- [tools/hwsu/hwsu_freeze.py](hwsu_freeze.py.md) (line 5, import)
- [tools/hwsu/hwsu_meter_bind.py](hwsu_meter_bind.py.md) (line 5, import)
- [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 10, import)
- [tools/hwsu/hwsu_oracle.py](hwsu_oracle.py.md) (line 6, import)
- [tools/hwsu/hwsu_pairs.py](hwsu_pairs.py.md) (line 6, import)
- [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 9, import)
- [tools/hwsu/hwsu_resv.py](hwsu_resv.py.md) (line 6, import)
- [tools/hwsu/hwsu_seed.py](hwsu_seed.py.md) (line 6, import)
- [tools/hwsu/u2/hwsu_bind_u2.py](u2/hwsu_bind_u2.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_decide.py](u2/hwsu_decide.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_driver.py](u2/hwsu_driver.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_dry2.py](u2/hwsu_dry2.py.md) (line 12, import)
- [tools/hwsu/u2/hwsu_dry2b.py](u2/hwsu_dry2b.py.md) (line 9, import)
- [tools/hwsu/u2/hwsu_e2.py](u2/hwsu_e2.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_gates.py](u2/hwsu_gates.py.md) (line 10, import)
- [tools/hwsu/u2/hwsu_known.py](u2/hwsu_known.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_model.py](u2/hwsu_model.py.md) (line 10, import)
- [tools/hwsu/u2/hwsu_registry.py](u2/hwsu_registry.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_regsrc.py](u2/hwsu_regsrc.py.md) (line 7, import)

## Top-level constants

- `API_PATH`
- `BINDING`
- `CONTRACT`
- `CONTRACT_OF_PATH`
- `CONTRACT_PATH`
- `CONTRACT_SHA256`
- `DECIMAL_ROWS`
- `DRY_SEEDS_OF`
- `DRY_STORE`
- `HANDOFF_PATH`
- `HERE`
- `HWSC_STORE`
- `KEY`
- `LAMBDA_KO3`
- `MAILBOX`
- `MASTERS`
- `PROC`
- `PROTOCOL_PATH`
- `REPO`
- `ROOT`
- `SCRATCH`
- `SEEDS_OF`
- `SELECTION_PATH`
- `STORE`
- `STUDY_LEDGER`
- `TEST_PLAN_PATH`
- `_ORDER`

## Classes and functions

- **function `_sha_bytes`** [L47-48]: `def _sha_bytes(data: bytes) -> str`
- **function `merge`** [L51-63]: `def merge(a, b, path='') -> dict` - Recursive union of two dicts; any shared non-dict key is an override (D-2).
- **function `load_contract`** [L66-80]: `def load_contract(of_path=CONTRACT_OF_PATH, phase2_path=CONTRACT_PATH) -> dict`
- **function `_posix`** [L111-112]: `def _posix(path) -> str`
- **function `_hwsd_allowed`** [L115-120]: `def _hwsd_allowed(q: str) -> bool`
- **function `blinded`** [L123-140]: `def blinded(path, root=ROOT) -> bool`
- **function `public_summary`** [L143-144]: `def public_summary(path) -> bool`
- **function `guard`** [L147-150]: `def guard(path, root=ROOT) -> Path`
- **function `read_bytes`** [L153-154]: `def read_bytes(path, root=ROOT) -> bytes`
- **function `read_json`** [L157-158]: `def read_json(path, root=ROOT)`
- **function `sha256_file`** [L161-162]: `def sha256_file(path, root=ROOT) -> str`
- **function `load_handoff_u`** [L166-176]: `def load_handoff_u(path=HANDOFF_PATH, expected_sha256=None) -> dict`
- **function `dry_store_ok`** [L179-186]: `def dry_store_ok(path) -> bool` - True iff path lies under SCRATCH/hwsu-dry* or SCRATCH/test_hwsu-* (dry guard, E-4).

