# `tests/executors/conftest.py`

- Source: [tests/executors/conftest.py](../../../../../tests/executors/conftest.py)
- Kind: python
- Lines: 38

## Module docstring

> Fixtures for the executors tests: a throw-away repository copy, stores, subprocess env.

## Imports

### Internal (repo files)

- `from exec_helpers import make_store` -> [tests/executors/exec_helpers.py](exec_helpers.py.md) (line 12, via same directory)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 14, via package root)

### External (third-party)

- `pytest` (lines 7)

### Standard library

- `pathlib` (lines 5)
- `shutil` (lines 3)
- `sys` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(Path(__file__).resolve().parent)` -> `tests/executors`

## Imported by

- none

## Top-level constants

- `REAL_REPO`
- `STUB_DIR`

## Classes and functions

- **function `fake_repo`** [L21-33]: `def fake_repo(tmp_path_factory) -> Path` decorators: @pytest.fixture(scope='module') - A minimal repository (src, configs, pyproject, lock) plus planted secrets.
- **function `store`** [L37-38]: `def store(tmp_path) -> ArtifactStore` decorators: @pytest.fixture

