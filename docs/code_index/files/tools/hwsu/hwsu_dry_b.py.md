# `tools/hwsu/hwsu_dry_b.py`

- Source: [tools/hwsu/hwsu_dry_b.py](../../../../../tools/hwsu/hwsu_dry_b.py)
- Kind: python
- Lines: 241

## Module docstring

> HWSU dry run DRO5-DRO9 and the J11 obligation reader fixture (API.md §10; split from hwsu_dry by
> size, API erratum; every name is reachable as hwsu_dry.<name>).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 6, via same directory)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 7, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 8, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](hwsu_oracle.py.md) (line 9, via same directory)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](hwsu_pairs.py.md) (line 10, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 11, via same directory)
- `import hwsu_seed` -> [tools/hwsu/hwsu_seed.py](hwsu_seed.py.md) (line 12, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 17, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 20, via unique basename)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 4)
- `copy` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 245, dynamic)

## Top-level constants

- `SEEDS`

## Classes and functions

- **function `obligation_reader_fixture`** [L25-26]: `def obligation_reader_fixture(store) -> dict`
- **function `_lemma_ctx`** [L29-33]: `def _lemma_ctx(w, a1, a2) -> dict`
- **function `dro5`** [L36-49]: `def dro5(base) -> dict`
- **function `dro6`** [L52-75]: `def dro6(base) -> dict`
- **function `_freeze_record`** [L78-88]: `def _freeze_record(repo: Path) -> dict`
- **function `dro7`** [L91-155]: `def dro7(base) -> dict`
- **function `dro8`** [L158-172]: `def dro8(base) -> dict`
- **function `_arr`** [L175-177]: `def _arr(path, **kw)`
- **function `dro9`** [L180-241]: `def dro9(base) -> dict`

