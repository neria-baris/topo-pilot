# `tools/hwsg/hwsg_config.py`

- Source: [tools/hwsg/hwsg_config.py](../../../../../tools/hwsg/hwsg_config.py)
- Kind: python
- Lines: 265

## Module docstring

> HWSG configuration: CONTRACT.json, constants, worlds, plans, paths, blindness guard (API.md §1).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 27, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 28, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 29, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 30, via unique basename)
- `from topo_pilot.process import EmissionConfig, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 32, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `copy` (lines 9)
- `dataclasses` (lines 10)
- `fnmatch` (lines 11)
- `fractions` (lines 15)
- `hashlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> not statically determinable

## Imported by

- [tests/hwsg/test_a_cross.py](../../tests/hwsg/test_a_cross.py.md) (line 22, import)
- [tests/hwsg/test_a_kg6_port.py](../../tests/hwsg/test_a_kg6_port.py.md) (line 24, import)
- [tests/hwsg/test_a_law.py](../../tests/hwsg/test_a_law.py.md) (line 24, import)
- [tests/hwsg/test_a_outcomes_licences.py](../../tests/hwsg/test_a_outcomes_licences.py.md) (line 22, import)
- [tests/hwsg/test_a_ratio.py](../../tests/hwsg/test_a_ratio.py.md) (line 23, import)
- [tests/hwsg/test_a_selection.py](../../tests/hwsg/test_a_selection.py.md) (line 24, import)
- [tests/hwsg/test_b_common.py](../../tests/hwsg/test_b_common.py.md) (line 29, dynamic)
- [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 6, import)
- [tools/hwsg/hwsg_cross.py](hwsg_cross.py.md) (line 6, import)
- [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 6, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 5, import)
- [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 5, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 6, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 5, import)
- [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 5, import)
- [tools/hwsg/hwsg_ratio.py](hwsg_ratio.py.md) (line 5, import)
- [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 6, import)
- [tools/hwsg/hwsg_registry.py](hwsg_registry.py.md) (line 6, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 5, import)

## Top-level constants

- `ALPHA`
- `API_PATH`
- `BAD`
- `CAP`
- `CAPTURE_FLOOR`
- `CONTRACT`
- `CONTRACT_PATH`
- `CROSS_SEED`
- `DISCLOSURE`
- `DRAWS`
- `DRY_MASTERS`
- `DRY_SEEDS`
- `DRY_STORE`
- `FLOOR`
- `F_PLAN_MAX`
- `HERE`
- `HOLD_FROM`
- `HOLD_S`
- `HWSB_STORE`
- `HWSC_STORE`
- `HWSD_STORE`
- `HWSU_STORE`
- `HWS_STORE`
- `KS`
- `LADDER`
- `LEARN`
- `M`
- `MAILBOX`
- `NEEDLES`
- `O3_ROWS`
- `PROTOCOL_PATH`
- `PROTOCOL_SHA`
- `PROTOCOL_SHA256`
- `RANKS`
- `REPO`
- `REPORT_PATH`
- `RISK_MAX`
- `ROOT`
- `S3_DIR`
- `SCOPE`
- `SCRATCH`
- `SIZES`
- `STEPS`
- `STORE`
- `STUDY_LEDGER`
- `TAGS`
- `TEST_PLAN_PATH`
- `WORLDS`
- `W_STAR`
- `_ORDER`

## Classes and functions

- **function `load_contract`** [L54-55]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `protocol_ok`** [L64-65]: `def protocol_ok() -> bool`
- **function `exclusions`** [L104-110]: `def exclusions(handoff_path=None) -> tuple`
- **class `WorldDef`** [L115-133] decorators: @dataclasses.dataclass(frozen=True)
- **function `_make`** [L136-151]: `def _make(tag, d) -> WorldDef`
- **function `world`** [L157-165]: `def world(w) -> WorldDef`
- **function `world_dir`** [L168-169]: `def world_dir(store, w) -> Path`
- **function `plan`** [L172-176]: `def plan(w) -> hwsb_config.Plan`
- **function `dry_plan`** [L179-185]: `def dry_plan(w, case, kind='dry_tiny') -> hwsb_config.Plan`
- **function `run_key`** [L188-192]: `def run_key(w, master, case=None) -> tuple`
- **function `k4b_view`** [L195-199]: `def k4b_view() -> dict`
- **function `_posix`** [L203-204]: `def _posix(path) -> str`
- **function `_rel`** [L207-211]: `def _rel(path, root)`
- **function `blinded`** [L214-238]: `def blinded(path, root=ROOT) -> bool`
- **function `public_summary`** [L241-245]: `def public_summary(path) -> bool`
- **function `guard`** [L248-251]: `def guard(path, root=ROOT) -> Path`
- **function `read_json`** [L254-255]: `def read_json(path, root=ROOT)`
- **function `read_bytes`** [L258-259]: `def read_bytes(path, root=ROOT) -> bytes`
- **function `prune`** [L262-265]: `def prune(dirpath, dirnames, root=ROOT) -> None`

