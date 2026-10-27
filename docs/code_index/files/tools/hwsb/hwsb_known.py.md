# `tools/hwsb/hwsb_known.py`

- Source: [tools/hwsb/hwsb_known.py](../../../../../tools/hwsb/hwsb_known.py)
- Kind: python
- Lines: 353

## Module docstring

> HWSB G0 and the known cases KB0-KB7 (API.md §7; protocol §3).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import hws_driver` -> [tools/hws/hws_driver.py](../hws/hws_driver.py.md) (line 16, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 17, via same directory)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](hwsb_law.py.md) (line 18, via same directory)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 19, via same directory)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../x4_circle_history/process_law.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MemoryBackend, ObservationSet, SeedTree, payload_checksum` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 32, via package root)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 108, via same directory) (inside a function)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 283, via same directory) (inside a function)
- `import hwsb_kb` -> [tools/hwsb/hwsb_kb.py](hwsb_kb.py.md) (line 350, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 13)
- `json` (lines 11)
- `pathlib` (lines 14)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_b_records.py](../../tests/hwsb/test_b_records.py.md) (line 29, import)
- [tests/hwsb/test_r_0168_kb_default_store.py](../../tests/hwsb/test_r_0168_kb_default_store.py.md) (line 21, import)
- [tests/hwsb/test_r_0170_kb2_status.py](../../tests/hwsb/test_r_0170_kb2_status.py.md) (line 19, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 19, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 24, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 19, import)
- [tools/hwsb/hwsb_kb.py](hwsb_kb.py.md) (line 17, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 18, import)

## Top-level constants

- `E4`
- `KC`
- `KNOWN`

## Classes and functions

- **function `jsonable`** [L39-58]: `def jsonable(x)` - JSON-safe copy: Fractions as str, numpy scalars as Python, (j, s) keys as 'j:s'.
- **function `_ok`** [L61-62]: `def _ok(flag) -> str`
- **function `_read_json`** [L65-66]: `def _read_json(path) -> dict`
- **function `classify_hits`** [L72-90]: `def classify_hits(hits, fragments=None, job_scratch=None, label='hwsb_declaration') -> dict` - Mirror of hws_driver.classify_seed_hits with the lists as arguments (RC-3).
- **function `g0`** [L93-101]: `def g0(out, root=hc.ROOT) -> dict`
- **function `kb0`** [L107-129]: `def kb0(out, auth, sched) -> dict`
- **function `kb1`** [L132-155]: `def kb1(store) -> tuple`
- **function `w0_process`** [L158-162]: `def w0_process(store=None) -> dict`
- **function `_e4_obs`** [L168-173]: `def _e4_obs(proc, split, n, rng, rep) -> ObservationSet`
- **function `_ck`** [L176-177]: `def _ck(obj) -> str`
- **function `kb2_kb3`** [L180-236]: `def kb2_kb3(proc_w0) -> dict`
- **function `kb4`** [L242-278]: `def kb4(proc_w0, proc_star) -> dict`
- **function `run_kb`** [L281-344]: `def run_kb(out, auth, sched, store=None) -> dict` - KB0 -> KB6 as gates; the first failure stops with later items NOT_RUN.
- **function `__getattr__`** [L347-353]: `def __getattr__(name)` - kb5, kb6 and kb7 live in hwsb_kb (split by size), re-exported lazily.

