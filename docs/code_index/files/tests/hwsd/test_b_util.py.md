# `tests/hwsd/test_b_util.py`

- Source: [tests/hwsd/test_b_util.py](../../../../../tests/hwsd/test_b_util.py)
- Kind: python
- Lines: 251

## Module docstring

> Author B shared helpers for tests/hwsd (job 0197). Holds no tests.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 27, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via unique basename)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 32, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 33, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 34, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 35, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 36, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 37, via package root)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 143, via unique basename) (inside a function)
- `from topo_pilot.contracts import EmissionSpec, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 144, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 29)

### Standard library

- `__future__` (lines 8)
- `builtins` (lines 10)
- `copy` (lines 11)
- `dataclasses` (lines 12)
- `hashlib` (lines 13)
- `importlib` (lines 14)
- `io` (lines 15)
- `json` (lines 16)
- `os` (lines 17)
- `pathlib` (lines 18, 20)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 107: `dynamic: mod`

### sys.path additions

- line 25: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- [tests/hwsd/test_b_binding.py](test_b_binding.py.md) (line 18, import)
- [tests/hwsd/test_b_data.py](test_b_data.py.md) (line 18, import)
- [tests/hwsd/test_b_guard_search.py](test_b_guard_search.py.md) (line 15, import)
- [tests/hwsd/test_b_records_meter.py](test_b_records_meter.py.md) (line 20, import)
- [tests/hwsd/test_b_registry_build.py](test_b_registry_build.py.md) (line 15, import)
- [tests/hwsd/test_b_registry_r10.py](test_b_registry_r10.py.md) (line 17, import)
- [tests/hwsd/test_b_registry_r9.py](test_b_registry_r9.py.md) (line 16, import)
- [tests/hwsd/test_b_reservation.py](test_b_reservation.py.md) (line 16, import)

## Top-level constants

- `GIB`
- `READER`
- `REPO`
- `UTC`
- `U_RULES`

## Classes and functions

- **function `sha`** [L44-45]: `def sha(path) -> str`
- **function `norm`** [L48-49]: `def norm(p) -> str`
- **function `under`** [L52-54]: `def under(p, d) -> bool`
- **function `write_json`** [L57-61]: `def write_json(path, obj) -> Path`
- **function `junk`** [L64-68]: `def junk(path, data: bytes = b'\x00junk-bytes-never-opened') -> Path`
- **class `OpenSpy`** [L71-95] - Records every path opened through open/io.open/os.open/pathlib (Python 3.10).
- **method `OpenSpy.__init__`** [L74-75]: `def __init__(self)`
- **method `OpenSpy._wrap`** [L77-83]: `def _wrap(self, f)`
- **method `OpenSpy.install`** [L85-92]: `def install(self, monkeypatch)`
- **method `OpenSpy.opened_under`** [L94-95]: `def opened_under(self, d) -> list`
- **function `never_called_names`** [L98-99]: `def never_called_names() -> list`
- **function `tripwire`** [L102-116]: `def tripwire(monkeypatch, names=None) -> list` - Replace never-called functions by tripwires; returns the list of names hit.
- **function `status_of`** [L119-120]: `def status_of(exc) -> str`
- **function `tiny_artifacts`** [L126-134]: `def tiny_artifacts(artifacts: Path, n_train: int = 48, n_dev: int = 24) -> dict` - WorldSpec, TransitionSpec, two EmissionSpecs, two ObservationSets (tiny world).
- **function `os_payloads`** [L137-138]: `def os_payloads(artifacts: Path) -> list`
- **function `expected_os_digests`** [L141-154]: `def expected_os_digests(artifacts: Path) -> set` - Independent canonical digests of every ObservationSet of an artifacts root.
- **function `hist_table`** [L157-161]: `def hist_table(split: str, n: int, seed: int, start: int, low: int = 5) -> dict`
- **function `save_table`** [L164-168]: `def save_table(path, table) -> Path`
- **function `stage_complete`** [L171-176]: `def stage_complete(store: Path, stage: str, rels) -> None` - Append one STAGE_COMPLETE event (the k4b_driver.complete_stage line format).
- **function `fake_artifact`** [L179-184]: `def fake_artifact(artifacts: Path, kind: str, hexid: str, names=('payload.npz',), meta=None)`
- **function `array_npz`** [L187-191]: `def array_npz(path, **arrays) -> Path`
- **function `u_entry`** [L204-208]: `def u_entry(store: Path, rel: str, cls: str, basis) -> dict`
- **function `u_obligation`** [L211-217]: `def u_obligation(store: Path, entries, utc=UTC, rules=None, track='U') -> dict`
- **function `build_u_store`** [L220-247]: `def build_u_store(store: Path) -> dict` - A store as track U would leave it after its oracle-only stage (J6, J10, J11).
- **function `put_obligation`** [L250-251]: `def put_obligation(store: Path, obl: dict, name='REGISTRY_OBLIGATION_OF.json') -> Path`

