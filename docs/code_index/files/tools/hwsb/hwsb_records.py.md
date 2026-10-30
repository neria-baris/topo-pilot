# `tools/hwsb/hwsb_records.py`

- Source: [tools/hwsb/hwsb_records.py](../../../../../tools/hwsb/hwsb_records.py)
- Kind: python
- Lines: 160

## Module docstring

> HWSB records: the study ledger, project-root inventories, and FREEZE.json (API.md §8,
> §13; protocol §6.4 rule 1, §8.2 RC-7). Split out of hwsb_driver by size; hwsb_driver
> re-exports every name.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 8, via same directory)
- `import hws_records` -> [tools/hws/hws_records.py](../hws/hws_records.py.md) (line 16, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 17, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)

### External (third-party)

- `numpy` (lines 18)
- `scipy` (lines 122)
- `torch` (lines 123)

### Standard library

- `__future__` (lines 6)
- `json` (lines 9)
- `os` (lines 10)
- `pathlib` (lines 14)
- `platform` (lines 11)
- `subprocess` (lines 12)
- `time` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 23, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 25, import)
- [tools/hwsc/hwsc_jobs.py](../hwsc/hwsc_jobs.py.md) (line 14, import)

## Top-level constants

- `C`
- `FREEZE`

## Classes and functions

- **function `utc`** [L27-28]: `def utc() -> str`
- **function `ledger_read`** [L31-35]: `def ledger_read(path) -> dict`
- **function `ledger_append`** [L38-57]: `def ledger_append(path, job, stage, cpu_s, source, master=None) -> dict`
- **function `inventory_snapshot`** [L60-69]: `def inventory_snapshot(root=hc.ROOT, exclude=()) -> dict`
- **function `inventory_diff`** [L72-80]: `def inventory_diff(before, after) -> dict`
- **function `_git`** [L83-84]: `def _git(repo, *args) -> bytes`
- **function `implementation_files`** [L87-94]: `def implementation_files(repo, h_exec) -> dict`
- **function `_hashes`** [L97-113]: `def _hashes(repo) -> dict`
- **function `freeze`** [L116-143]: `def freeze(out, repo, h_exec, dry_report) -> dict`
- **function `verify_freeze`** [L146-157]: `def verify_freeze(out, repo) -> dict`

