# `src/topo_pilot/executors/run_bundle_script.py`

- Source: [src/topo_pilot/executors/run_bundle_script.py](../../../../../../src/topo_pilot/executors/run_bundle_script.py)
- Kind: python
- Lines: 103

## Module docstring

> Standalone ``run_bundle.py`` shipped inside every bundle (standard library only until the
> environment is installed).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 62, via package root) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 14)
- `argparse` (lines 16)
- `importlib` (lines 17)
- `json` (lines 18)
- `os` (lines 19)
- `pathlib` (lines 23)
- `re` (lines 20)
- `subprocess` (lines 21)
- `sys` (lines 22)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 61: `str(HERE / 'src')` -> `src`

## Imported by

- [tests/executors/test_static.py](../../../tests/executors/test_static.py.md) (line 43, import)

## Top-level constants

- `HERE`

## Classes and functions

- **function `filtered_requirements`** [L28-40]: `def filtered_requirements(text: str, torch_present: bool) -> list[str]` - Pins without local version suffixes; ``torch`` dropped when it is already importable.
- **function `install`** [L43-56]: `def install(work: Path) -> None` - ``pip install`` the filtered lock; fall back to one package at a time on failure.
- **function `run`** [L59-85]: `def run(work: Path) -> int` - Verify inputs, run the job, pack outputs; returns the job exit code.
- **function `main`** [L88-99]: `def main() -> int` - CLI entry.

