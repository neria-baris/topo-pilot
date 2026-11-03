# `tests/hwsu/test_b_u2_contract.py`

- Source: [tests/hwsu/test_b_u2_contract.py](../../../../../tests/hwsu/test_b_u2_contract.py)
- Kind: python
- Lines: 143

## Module docstring

> Author B (job 0223, phase 2): CONTRACT.json and its loader (TEST_PLAN_U2 section 3 row
> test_b_u2_contract; API_U2 section 0, U-D-2). Written from the protocol, API_U2, CONTRACT_OF.json
> and CONTRACT.json only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 18, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 19, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 113, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `hashlib` (lines 8)
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

- line 16: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `GIB`
- `HWSU`
- `OF`
- `P2`
- `REPO`

## Classes and functions

- **function `_sha`** [L27-28]: `def _sha(p: Path) -> str`
- **function `_new_keys_only`** [L31-41]: `def _new_keys_only(of, p2, path='')` - Every key of p2 is absent from of, or both are dicts and the rule recurses.
- **test `test_contract_of_sha256_binds_phase1_bytes`** [L44-45]: `def test_contract_of_sha256_binds_phase1_bytes()`
- **test `test_loader_succeeds_without_override`** [L48-52]: `def test_loader_succeeds_without_override()`
- **test `test_every_phase2_key_is_new_or_a_new_key_in_a_phase1_dict`** [L55-57]: `def test_every_phase2_key_is_new_or_a_new_key_in_a_phase1_dict()`
- **test `test_no_phase1_leaf_changed_in_merged_contract`** [L60-71]: `def test_no_phase1_leaf_changed_in_merged_contract()`
- **test `test_wrong_contract_of_sha256_refused`** [L74-81]: `def test_wrong_contract_of_sha256_refused(tmp_path)`
- **test `test_override_of_a_phase1_leaf_refused`** [L84-91]: `def test_override_of_a_phase1_leaf_refused(tmp_path)`
- **test `test_reuse_sha256_u2_disjoint_from_phase1_table`** [L94-98]: `def test_reuse_sha256_u2_disjoint_from_phase1_table()`
- **test `test_u2_memory_caps`** [L101-109]: `def test_u2_memory_caps()`
- **test `test_name_rule_unchanged_merged_rule_refuses_acts`** [L112-120]: `def test_name_rule_unchanged_merged_rule_refuses_acts()`
- **test `test_phase2_files_names_modules_and_documents`** [L123-131]: `def test_phase2_files_names_modules_and_documents()`
- **test `test_phase2_files_not_in_phase1_files`** [L134-135]: `def test_phase2_files_not_in_phase1_files()`
- **test `test_authority_and_dry_seeds_present`** [L138-143]: `def test_authority_and_dry_seeds_present()`

