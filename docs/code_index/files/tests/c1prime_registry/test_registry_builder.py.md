# `tests/c1prime_registry/test_registry_builder.py`

- Source: [tests/c1prime_registry/test_registry_builder.py](../../../../../tests/c1prime_registry/test_registry_builder.py)
- Kind: python
- Lines: 105

## Module docstring

> Builder tests for tools/c1prime/c1_registry_sources.py (job 0027; synthetic fixtures only).

## Imports

### Internal (repo files)

- `import c1_data` -> [tools/c1prime/c1_data.py](../../tools/c1prime/c1_data.py.md) (line 19, via sys.path edit)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../../tools/c1prime_registry/c1_registry_sources.py.md) (line 20, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 22, via sys.path edit)
- `import reference_cache` -> [tools/x4_circle_history/reference_cache.py](../../tools/x4_circle_history/reference_cache.py.md) (line 39, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 10)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 3)
- `hashlib` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 8)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(_p)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/c1prime_registry`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **test `test_canonical32_inverts_the_named_permutation`** [L25-30]: `def test_canonical32_inverts_the_named_permutation()`
- **test `test_canonical32_rejects_a_non_permutation`** [L33-35]: `def test_canonical32_rejects_a_non_permutation()`
- **test `test_reference_cache_reader_keeps_only_32_symbol_entries`** [L38-48]: `def test_reference_cache_reader_keeps_only_32_symbol_entries(tmp_path)`
- **test `test_token_readers_reject_out_of_range_values_instead_of_wrapping`** [L51-58]: `def test_token_readers_reject_out_of_range_values_instead_of_wrapping()`
- **test `test_handoff_scan_finds_token_lists_and_ignores_others`** [L61-71]: `def test_handoff_scan_finds_token_lists_and_ignores_others(tmp_path)`
- **test `test_frozen_builder_unions_and_hashes_sources`** [L74-82]: `def test_frozen_builder_unions_and_hashes_sources(tmp_path)`
- **test `test_store_sources_record_every_listed_store_explicitly`** [L85-93]: `def test_store_sources_record_every_listed_store_explicitly()`
- **test `test_store_file_hashes_bind_every_file_by_content`** [L96-105]: `def test_store_file_hashes_bind_every_file_by_content(tmp_path)`

