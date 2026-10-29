# `tools/hwsc/hwsc_registry.py`

- Source: [tools/hwsc/hwsc_registry.py](../../../../../tools/hwsc/hwsc_registry.py)
- Kind: python
- Lines: 381

## Module docstring

> HWSC exposure registry hwsc-reg-v1: K-REG1, K-REG2, REHEARSAL (API.md §4; protocol §3.3-§3.4,
> RC-2..RC-4; rulings R-0176-G4, G9). Composes C2ND's frozen readers (R1, R3) unchanged with the new
> readers R2, R4-R7 and the stage-C inventory adapter (R8), in nd_registry.build's C2 format.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 12, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 13, via unique basename)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../hwsb/hwsb_registry.py.md) (line 14, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 15, via unique basename)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 16, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 18, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 20, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 22, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 23, via package root)
- `from hwsc_registry_build import build, obligation` -> [tools/hwsc/hwsc_registry_build.py](hwsc_registry_build.py.md) (line 381, via same directory)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 5)
- `fnmatch` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 27, import)
- [tests/hwsc/test_b_registry2.py](../../tests/hwsc/test_b_registry2.py.md) (line 26, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 30, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 18, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 26, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 18, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 17, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 21, import)
- [tools/hwsc/hwsc_registry_build.py](hwsc_registry_build.py.md) (line 14, import)

## Top-level constants

- `ARRAYS`
- `ART_TYPES`
- `C2_COLS`
- `REG`
- `STAGE_B`
- `VERSIONS`

## Classes and functions

- **function `_new`** [L34-36]: `def _new(present=True) -> dict`
- **function `_close`** [L39-41]: `def _close(out, lineage=False) -> dict`
- **function `_rel`** [L44-45]: `def _rel(base, f) -> str`
- **function `_walk_arrays`** [L48-54]: `def _walk_arrays(top, prune=None)`
- **function `_meta_type`** [L57-66]: `def _meta_type(f)` - artifact_type of <root>/<T>/<id>/payload.npz|state.pt from its meta.json, else None.
- **function `_c2_table`** [L70-82]: `def _c2_table(path, out) -> None`
- **function `source_c2nd`** [L85-122]: `def source_c2nd(store=None, bound=None) -> dict`
- **function `source_hwsb`** [L126-146]: `def source_hwsb(store=None, expected=None) -> dict`
- **function `_dry_paths`** [L150-153]: `def _dry_paths() -> list`
- **function `_os_canonical`** [L156-166]: `def _os_canonical(f, out) -> None`
- **function `_token_file`** [L169-188]: `def _token_file(f, out) -> None`
- **function `source_dry`** [L191-225]: `def source_dry(paths=None) -> dict`
- **function `source_scratch_c`** [L229-230]: `def source_scratch_c(scratch=None) -> dict`
- **function `_classify`** [L233-248]: `def _classify(f) -> tuple`
- **function `scratch_scan`** [L251-275]: `def scratch_scan(scratch=None) -> dict`
- **function `_row_for`** [L278-284]: `def _row_for(name, table)`
- **function `_fixture_ok`** [L287-293]: `def _fixture_ok(rel, rec, row) -> bool`
- **function `scratch_check`** [L296-329]: `def scratch_check(scratch=None, table=None, readers_ok=None) -> dict`
- **function `source_own`** [L333-354]: `def source_own(store, expected) -> dict`
- **function `inventory_c`** [L358-377]: `def inventory_c(root=None, readers=None) -> dict`

