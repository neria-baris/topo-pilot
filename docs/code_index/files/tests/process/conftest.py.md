# `tests/process/conftest.py`

- Source: [tests/process/conftest.py](../../../../../tests/process/conftest.py)
- Kind: python
- Lines: 32

## Module docstring

> Module-local fixtures for the process tests.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 8, via package root)

### External (third-party)

- `pytest` (lines 5)

### Standard library

- `__future__` (lines 3)

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

- none

## Classes and functions

- **function `square12`** [L12-14]: `def square12() -> WorldSpec` decorators: @pytest.fixture(scope='session') - 12 x 12 square (core-world size).
- **function `cylinder12`** [L18-20]: `def cylinder12() -> WorldSpec` decorators: @pytest.fixture(scope='session') - 12 x 12 cylinder, x periodic with period 12.
- **function `square3`** [L24-26]: `def square3() -> WorldSpec` decorators: @pytest.fixture(scope='session') - 3 x 3 square.
- **function `cylinder3`** [L30-32]: `def cylinder3() -> WorldSpec` decorators: @pytest.fixture(scope='session') - 3 x 3 cylinder.

