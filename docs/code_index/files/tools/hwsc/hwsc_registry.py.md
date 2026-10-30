# `tools/hwsc/hwsc_registry.py`

- Source: [tools/hwsc/hwsc_registry.py](../../../../../tools/hwsc/hwsc_registry.py)
- Kind: python
- Lines: 331

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
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 22, via package root)
- `import hwsc_drystore` -> [tools/hwsc/hwsc_drystore.py](hwsc_drystore.py.md) (line 238, via same directory) (inside a function)
- `import hwsc_scratch` -> [tools/hwsc/hwsc_scratch.py](hwsc_scratch.py.md) (line 239, via same directory) (inside a function)
- `from hwsc_registry_build import build, obligation` -> [tools/hwsc/hwsc_registry_build.py](hwsc_registry_build.py.md) (line 330, via same directory)
- `from hwsc_scratch import _classify, scratch_check, scratch_scan` -> [tools/hwsc/hwsc_scratch.py](hwsc_scratch.py.md) (line 331, via same directory)

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
- [tests/hwsc/test_r_0178_dry_store_rule.py](../../tests/hwsc/test_r_0178_dry_store_rule.py.md) (line 17, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 18, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 26, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 18, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 17, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 21, import)
- [tools/hwsc/hwsc_registry_build.py](hwsc_registry_build.py.md) (line 14, import)
- [tools/hwsc/hwsc_scratch.py](hwsc_scratch.py.md) (line 18, import)

## Top-level constants

- `ARRAYS`
- `ART_TYPES`
- `C2_COLS`
- `REG`
- `STAGE_B`
- `VERSIONS`

## Classes and functions

- **function `_new`** [L33-35]: `def _new(present=True) -> dict`
- **function `_close`** [L38-40]: `def _close(out, lineage=False) -> dict`
- **function `_rel`** [L43-44]: `def _rel(base, f) -> str`
- **function `_walk_arrays`** [L47-53]: `def _walk_arrays(top, prune=None)`
- **function `_meta_type`** [L56-65]: `def _meta_type(f)` - artifact_type of <root>/<T>/<id>/payload.npz|state.pt from its meta.json, else None.
- **function `_c2_table`** [L69-81]: `def _c2_table(path, out) -> None`
- **function `source_c2nd`** [L84-121]: `def source_c2nd(store=None, bound=None) -> dict`
- **function `source_hwsb`** [L125-145]: `def source_hwsb(store=None, expected=None) -> dict`
- **function `_dry_paths`** [L149-152]: `def _dry_paths() -> list`
- **function `_os_canonical`** [L155-165]: `def _os_canonical(f, out) -> None`
- **function `_token_file`** [L168-191]: `def _token_file(f, out) -> None`
- **function `source_dry`** [L194-234]: `def source_dry(paths=None) -> dict`
- **function `_dry_file`** [L237-257]: `def _dry_file(top, rel, f, out) -> None`
- **function `_os_roots`** [L260-273]: `def _os_roots(out, roots=None) -> None` - R-0176-R6 rule 1: ObservationSet stores in scratch whose EmissionSpec parents lie in the
- **function `source_scratch_c`** [L277-278]: `def source_scratch_c(scratch=None) -> dict`
- **function `source_own`** [L282-303]: `def source_own(store, expected) -> dict`
- **function `inventory_c`** [L307-326]: `def inventory_c(root=None, readers=None) -> dict`

