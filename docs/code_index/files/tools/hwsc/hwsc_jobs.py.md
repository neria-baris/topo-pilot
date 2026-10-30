# `tools/hwsc/hwsc_jobs.py`

- Source: [tools/hwsc/hwsc_jobs.py](../../../../../tools/hwsc/hwsc_jobs.py)
- Kind: python
- Lines: 206

## Module docstring

> HWSC E2 job (release B), the close record and the CLI (API.md §7.3, §11.4; split from
> hwsc_driver by size, API erratum; re-exported by hwsc_driver).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 12, via unique basename)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 13, via unique basename)
- `import hwsb_records` -> [tools/hwsb/hwsb_records.py](../hwsb/hwsb_records.py.md) (line 14, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 15, via same directory)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 16, via same directory)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 17, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 18, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 19, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 22, via unique basename)
- `from hwsc_records import export_c, freeze_c, pause_or_raise_c, preflight, record_gate_files, run_gates_c, s0, status_of` -> [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 23, via same directory)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 28, via package root)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 100, via same directory) (inside a function)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 150, via same directory) (inside a function)
- `import hwsc_dry` -> [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 180, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `argparse` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 10)
- `time` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_r_0187_e1_release_and_gate_files.py](../../tests/hwsc/test_r_0187_e1_release_and_gate_files.py.md) (line 20, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 255, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 161, import)

## Top-level constants

- `E2_GATES`
- `STEPS`

## Classes and functions

- **function `e2_context`** [L34-53]: `def e2_context(out, rel, handoff, dry=False) -> dict` - Release-B context exactly as k4b_fresh.main assembles it (identity re-checked first).
- **function `_fill`** [L56-64]: `def _fill(result) -> dict`
- **function `run_e2`** [L67-114]: `def run_e2(out, auth, sched, release_path, session, dry=False, dry_continue=False) -> dict`
- **function `run_close`** [L117-133]: `def run_close(out, recs=None, reason=None) -> dict`
- **function `_load`** [L136-137]: `def _load(p)`
- **function `_exit`** [L140-146]: `def _exit(res) -> int`
- **function `main`** [L149-206]: `def main(argv=None) -> int`

