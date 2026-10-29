# `tests/hwsc/test_a_learning.py`

- Source: [tests/hwsc/test_a_learning.py](../../../../../tests/hwsc/test_a_learning.py)
- Kind: python
- Lines: 209

## Module docstring

> Author A (job 0176): the learning gate L1 on planted predictives.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 25, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 26, via sys.path edit)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 27, via unique basename)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 14)
- `json` (lines 11)
- `math` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `MODELS`
- `REPO`
- `_HWSC`

## Classes and functions

- **function `base`** [L34-39]: `def base(seed=5)`
- **function `mix`** [L42-43]: `def mix(q, lam)`
- **function `captured`** [L46-47]: `def captured(q, p)`
- **function `find_08`** [L50-74]: `def find_08()` - (q, p_at, p_below): captured(p_at) == 0.8 exactly, captured(p_below) < 0.8.
- **function `exact08`** [L78-83]: `def exact08()` decorators: @pytest.fixture(scope='module')
- **class `Spy`** [L86-96]
- **method `Spy.__init__`** [L87-88]: `def __init__(self, q, preds)`
- **method `Spy.oracle`** [L90-92]: `def oracle(self, proc, canon32, *a, **kw)`
- **method `Spy.model`** [L94-96]: `def model(self, checkpoint, canon32, perm, *a, **kw)`
- **function `ctx_for`** [L99-104]: `def ctx_for()`
- **function `install`** [L107-111]: `def install(monkeypatch, q, by_model)`
- **function `l1_json`** [L114-115]: `def l1_json(out)`
- **function `per_model`** [L118-120]: `def per_model(rec, j)`
- **test `test_reference_points`** [L123-127]: `def test_reference_points()`
- **test `test_all_pass_records_every_model`** [L130-148]: `def test_all_pass_records_every_model(tmp_path, monkeypatch, exact08)`
- **function `failing_case`** [L151-163]: `def failing_case(tmp_path, monkeypatch, q, preds, k, failing)`
- **test `test_first_model_failing_k1`** [L166-170]: `def test_first_model_failing_k1(tmp_path, monkeypatch)`
- **test `test_two_failing_k2`** [L173-176]: `def test_two_failing_k2(tmp_path, monkeypatch)`
- **test `test_just_below_08_fails`** [L179-183]: `def test_just_below_08_fails(tmp_path, monkeypatch, exact08)`
- **test `test_gc_floor_is_numerical`** [L186-193]: `def test_gc_floor_is_numerical(tmp_path, monkeypatch)`
- **test `test_nan_row_is_numerical`** [L196-205]: `def test_nan_row_is_numerical(tmp_path, monkeypatch)`
- **test `test_learning_constant`** [L208-209]: `def test_learning_constant()`

