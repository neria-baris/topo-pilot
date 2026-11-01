# `tools/hwsd/hwsd_readers.py`

- Source: [tools/hwsd/hwsd_readers.py](../../../../../tools/hwsd/hwsd_readers.py)
- Kind: python
- Lines: 305

## Module docstring

> HWSD registry readers: R9 (hwsc-store layout), R10 (obligation, J11), the K4b table reader and
> the superset check (API.md section 4 and section 22). Sources return the hwsc_registry._new shape
> and are closed by hwsc_registry._close (looked up at call time).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 13, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../hwsc/hwsc_registry.py.md) (line 14, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 16, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 17, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 20, via package root)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 5)
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

- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 275, import)
- [tests/hwsd/test_b_registry_build.py](../../tests/hwsd/test_b_registry_build.py.md) (line 13, import)
- [tests/hwsd/test_b_registry_r10.py](../../tests/hwsd/test_b_registry_r10.py.md) (line 16, import)
- [tests/hwsd/test_b_registry_r9.py](../../tests/hwsd/test_b_registry_r9.py.md) (line 15, import)
- [tests/hwsd/test_b_reservation.py](../../tests/hwsd/test_b_reservation.py.md) (line 15, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 27, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 18, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 24, import)
- [tools/hwsd/hwsd_registry.py](hwsd_registry.py.md) (line 19, import)
- [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 13, import)

## Top-level constants

- `ARRAYS`
- `ART_TYPES`
- `_ART_RE`
- `_OS_PAYLOAD`
- `_SUPER_HIST`

## Classes and functions

- **function `_obl`** [L30-31]: `def _obl()`
- **function `_merge`** [L34-41]: `def _merge(dst, src) -> bool` - Union of two sources; True when src is a lineage failure.
- **function `read_k4b_table`** [L45-66]: `def read_k4b_table(path, expected_sha256=None) -> dict`
- **function `os_digests`** [L69-78]: `def os_digests(payload_path) -> list`
- **function `stage_complete_sha`** [L81-89]: `def stage_complete_sha(stages_jsonl, rel, stage=None)`
- **function `_art_type_ok`** [L92-96]: `def _art_type_ok(f, folder_type) -> bool`
- **function `source_hwsc`** [L100-155]: `def source_hwsc(store=None) -> dict`
- **function `superset_check`** [L158-174]: `def superset_check(reg, store=None) -> dict`
- **function `_check_header`** [L178-194]: `def _check_header(o, bad) -> bool`
- **function `_check_entry`** [L197-223]: `def _check_entry(store, e, rules, bad) -> bool`
- **function `obligation_check`** [L226-286]: `def obligation_check(store, kind='store') -> dict`
- **function `source_hwsu`** [L289-305]: `def source_hwsu(root=None, scratch=None) -> dict`

