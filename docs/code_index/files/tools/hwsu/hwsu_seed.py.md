# `tools/hwsu/hwsu_seed.py`

- Source: [tools/hwsu/hwsu_seed.py](../../../../../tools/hwsu/hwsu_seed.py)
- Kind: python
- Lines: 158

## Module docstring

> HWSU needle search, hit classification, namespace overlap and G0-OF (API.md §6; protocol §4.2
> OF-0; RC-3, J3, J5, J9, J10).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 6, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 7, via same directory)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 13, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 14, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 15, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 16, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 11)
- `re` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_of_driver.py](../../tests/hwsu/test_b_of_driver.py.md) (line 23, import)
- [tests/hwsu/test_b_of_seed.py](../../tests/hwsu/test_b_of_seed.py.md) (line 28, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 8, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 12, import)

## Top-level constants

- `SKIP_DIRS`
- `TEXT_SUFFIXES`

## Classes and functions

- **function `_skip_dir`** [L23-27]: `def _skip_dir(parent, name, groot) -> bool`
- **function `_prefilter`** [L30-33]: `def _prefilter(needles)`
- **function `seed_search_u`** [L36-54]: `def seed_search_u(root, needles, root_for_guard=None) -> list`
- **function `classify_hits_u`** [L57-61]: `def classify_hits_u(hits, fragments=None, job_scratch=None) -> dict`
- **function `needles`** [L64-66]: `def needles(contract=None) -> tuple`
- **function `_tokens`** [L69-74]: `def _tokens(track) -> tuple`
- **function `namespace_overlap`** [L77-82]: `def namespace_overlap(u, d) -> list`
- **function `_sha_ok`** [L85-89]: `def _sha_ok(path, want, root) -> bool`
- **function `_authority`** [L92-114]: `def _authority(out, ctx, checks) -> None`
- **function `_records`** [L117-130]: `def _records(ctx, checks) -> None`
- **function `g0_of`** [L133-158]: `def g0_of(out, ctx) -> dict`

