# `tests/executors/test_static.py`

- Source: [tests/executors/test_static.py](../../../../../tests/executors/test_static.py)
- Kind: python
- Lines: 47

## Module docstring

(none)

## Imports

### Internal (repo files)

- `import topo_pilot.executors` -> [src/topo_pilot/executors/__init__.py](../../src/topo_pilot/executors/__init__.py.md) (line 36, via package root) (inside a function)
- `from topo_pilot.executors import run_bundle_script` -> [src/topo_pilot/executors/run_bundle_script.py](../../src/topo_pilot/executors/run_bundle_script.py.md) (line 43, via package root) (inside a function)

### External (third-party)

- `pytest` (lines 4)

### Standard library

- `ast` (lines 1)
- `pathlib` (lines 2)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `FORBIDDEN`
- `SRC`

## Classes and functions

- **function `imported_modules`** [L13-22]: `def imported_modules(path: Path) -> list[str]`
- **test `test_E07_no_science_or_experiment_imports`** [L25-32]: `def test_E07_no_science_or_experiment_imports()`
- **test `test_E07_public_api_is_exactly_the_spec`** [L35-39]: `def test_E07_public_api_is_exactly_the_spec()`
- **test `test_E07_requirements_filter_strips_local_suffix_and_skips_torch`** [L42-47]: `def test_E07_requirements_filter_strips_local_suffix_and_skips_torch()`

