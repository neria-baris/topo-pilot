# `tools/x4_circle_history/live_context.py`

- Source: [tools/x4_circle_history/live_context.py](../../../../../tools/x4_circle_history/live_context.py)
- Kind: python
- Lines: 140

## Module docstring

> Real-data Context for runner.py. Imported ONLY after a verified coordinator release.

## Imports

### Internal (repo files)

- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 35, via unique basename) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 36, via unique basename) (inside a function)
- `import topo_pilot` -> [src/topo_pilot/__init__.py](../../src/topo_pilot/__init__.py.md) (line 38, via package root) (inside a function)
- `import freeze_bind` -> [tools/x4_circle_history/freeze_bind.py](freeze_bind.py.md) (line 49, via same directory) (inside a function)
- `import env_identity` -> [tools/x4_circle_history/env_identity.py](env_identity.py.md) (line 55, via same directory) (inside a function)
- `import env_identity` -> [tools/x4_circle_history/env_identity.py](env_identity.py.md) (line 68, via same directory) (inside a function)
- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 69, via same directory) (inside a function)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 80, via unique basename) (inside a function)
- `from runner import Context` -> [tools/x4_circle_history/runner.py](runner.py.md) (line 97, via same directory) (inside a function)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](../x4_oracle_profile/inputs.py.md) (line 105, via unique basename) (inside a function)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](op_guard.py.md) (line 106, via same directory) (inside a function)
- `from adapter import E4Manifest` -> [tools/x4_circle_history/adapter.py](adapter.py.md) (line 107, via same directory) (inside a function)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 109, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 110, via package root) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 15)
- `hashlib` (lines 17)
- `json` (lines 18)
- `pathlib` (lines 20)
- `time` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/circle_history/test_builder_guards.py](../../tests/circle_history/test_builder_guards.py.md) (line 23, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 327, import)

## Top-level constants

- `HERE`
- `REPO`

## Classes and functions

- **class `StopRequested(RuntimeError)`** [L26-27] - STOP or invalid runtime control observed at a safe boundary (not a gate result).
- **function `_sha`** [L30-31]: `def _sha(path) -> str`
- **function `_pin_modules`** [L34-63]: `def _pin_modules(freeze: dict) -> dict`
- **function `check_loaded_modules`** [L66-76]: `def check_loaded_modules(ctx) -> None` - Stage-end re-check: no unfrozen project module and no new site-packages distribution.
- **function `_guard_factory`** [L79-93]: `def _guard_factory(rel: dict, out: Path)`
- **function `build`** [L96-140]: `def build(rel: dict)`

