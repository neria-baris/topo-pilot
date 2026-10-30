# `tests/hwsc/test_a_law.py`

- Source: [tests/hwsc/test_a_law.py](../../../../../tests/hwsc/test_a_law.py)
- Kind: python
- Lines: 169

## Module docstring

> Author A (job 0176): the documented-law identity and the pilot exclusions.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 23, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 24, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 25, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 26, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 27, via unique basename)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../../tools/hwsb/hwsb_law.py.md) (line 28, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 29, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 30, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 9)
- `copy` (lines 11)
- `fractions` (lines 13)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `EXCL`
- `HV`
- `KC4`
- `REPO`
- `_HWSC`

## Classes and functions

- **function `law_state`** [L38-40]: `def law_state()`
- **function `assert_restored`** [L43-46]: `def assert_restored(before)`
- **function `proc_star`** [L50-51]: `def proc_star()` decorators: @pytest.fixture(scope='module')
- **function `handoff`** [L55-56]: `def handoff()` decorators: @pytest.fixture(scope='module')
- **function `identity`** [L60-64]: `def identity(proc_star, handoff)` decorators: @pytest.fixture(scope='module')
- **test `test_handoff_values`** [L67-70]: `def test_handoff_values(handoff)`
- **test `test_process_is_w_star`** [L73-76]: `def test_process_is_w_star(proc_star)`
- **test `test_law_identity_pass`** [L79-85]: `def test_law_identity_pass(identity, handoff)`
- **test `test_f_plan_identity`** [L88-90]: `def test_f_plan_identity(identity, handoff)`
- **test `test_law_identity_refuses_last_digit`** [L93-103]: `def test_law_identity_refuses_last_digit(proc_star, handoff)`
- **test `test_law_identity_maps_exception_and_status`** [L106-122]: `def test_law_identity_maps_exception_and_status(proc_star, handoff, monkeypatch)`
- **test `test_law_identity_called_with_registered_law`** [L125-140]: `def test_law_identity_called_with_registered_law(proc_star, handoff, monkeypatch)`
- **test `test_w0_law_equals_old_enclosure`** [L143-151]: `def test_w0_law_equals_old_enclosure()`
- **test `test_exclusion_check`** [L154-163]: `def test_exclusion_check()`
- **test `test_exclusion_check_fixture_list`** [L166-169]: `def test_exclusion_check_fixture_list()`

