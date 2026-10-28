# `tests/hwsb/test_r_0170_kb2_status.py`

- Source: [tests/hwsb/test_r_0170_kb2_status.py](../../../../../tests/hwsb/test_r_0170_kb2_status.py)
- Kind: python
- Lines: 72

## Module docstring

> Regression D-0170-1 (coordinator 08ad4eaf, job 0170).

## Imports

### Internal (repo files)

- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 19, via sys.path edit)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../../tools/hwsb/hwsb_train.py.md) (line 20, via sys.path edit)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `K2`
- `REF_CE`
- `REF_CK`
- `REPO`

## Classes and functions

- **class `_Obs`** [L27-29]
- **method `_Obs.__init__`** [L28-29]: `def __init__(self, split)`
- **function `_stub`** [L32-45]: `def _stub(monkeypatch, checksums, dev_ce)`
- **test `test_bitwise_reading_is_gate_pass`** [L48-54]: `def test_bitwise_reading_is_gate_pass(monkeypatch)`
- **test `test_secondary_reading_keeps_its_status`** [L57-64]: `def test_secondary_reading_keeps_its_status(monkeypatch)`
- **test `test_no_reading_fails_known_case`** [L68-72]: `def test_no_reading_fails_known_case(monkeypatch, delta)` decorators: @pytest.mark.parametrize('delta', [0.01])

