# `tools/hwsu/hwsu_resv.py`

- Source: [tools/hwsu/hwsu_resv.py](../../../../../tools/hwsu/hwsu_resv.py)
- Kind: python
- Lines: 294

## Module docstring

> HWSU name rule, reservations, W2 attestation, obligations, root inventory (API.md §5.1,
> §5.5, §5.6, §10; split from hwsu_records by size, re-exported there).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 6, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 14, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 15, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 16, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `fnmatch` (lines 7)
- `hashlib` (lines 8)
- `json` (lines 9)
- `os` (lines 10)
- `pathlib` (lines 12)
- `re` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_of_registry.py](../../tests/hwsu/test_b_of_registry.py.md) (line 35, import)

## Top-level constants

- `ARRAY_SUFFIXES`
- `ARTIFACT_TYPES`
- `_RES`

## Classes and functions

- **function `_prefixes`** [L23-28]: `def _prefixes(contract=None) -> list`
- **function `name_class`** [L31-46]: `def name_class(relpath, contract=None, dry=False)`
- **function `save_array`** [L49-55]: `def save_array(out, relpath, dry=False, **arrays) -> Path`
- **function `reservation_file`** [L63-67]: `def reservation_file(reservation_id) -> str`
- **function `write_reservation`** [L70-76]: `def write_reservation(store, reservation_id, scope, start_utc, written_by) -> Path`
- **function `_rel`** [L79-80]: `def _rel(path, root) -> str`
- **function `end_reservation`** [L83-102]: `def end_reservation(store, reservation_id, utc, obligation_path, written_by='hwsu_records.end_reservation') -> Path`
- **function `_ended`** [L105-124]: `def _ended(rec, f, root, w2_end, w2_sha) -> str | None`
- **function `w2_attestation`** [L127-155]: `def w2_attestation(root, own=None, w2_end=None, w2_end_sha256=None) -> dict`
- **function `obligation_name`** [L159-166]: `def obligation_name(job, attempt=None, final=False) -> str`
- **function `write_obligation`** [L169-197]: `def write_obligation(store, name, job, written_by, dry=False, contract=None, attempt=None, reservation_id=None, dry_stores=()) -> Path`
- **function `read_obligation`** [L200-252]: `def read_obligation(store, contract=None) -> dict` - J11 reader rule: the newest obligation by written_utc governs (API.md J11 erratum).
- **function `root_inventory`** [L256-294]: `def root_inventory(root=uc.ROOT) -> dict`

