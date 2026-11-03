# `tests/hwsu/test_a_u2_family.py`

- Source: [tests/hwsu/test_a_u2_family.py](../../../../../tests/hwsu/test_a_u2_family.py)
- Kind: python
- Lines: 194

## Module docstring

> Author A (job 0223): family stream U and Lemma FW-U, response part (protocol 2.9; API_U2 4.4).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 18, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 19, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 28, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 11)
- `importlib` (lines 8)
- `math` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 30: `dynamic: name`

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `MASTERS`
- `N`
- `REGIONS`
- `REPO`

## Classes and functions

- **function `mod`** [L27-30]: `def mod(name)`
- **function `data`** [L34-38]: `def data()` decorators: @pytest.fixture(scope='module')
- **function `fb`** [L42-44]: `def fb(data)` decorators: @pytest.fixture(scope='module')
- **function `_arrays`** [L47-53]: `def _arrays(A, G, models)`
- **test `test_ranks_at_alpha_1_300`** [L56-59]: `def test_ranks_at_alpha_1_300()`
- **test `test_keys_and_ranks`** [L62-66]: `def test_keys_and_ranks(fb)`
- **test `test_equals_one_shared_stream`** [L69-76]: `def test_equals_one_shared_stream(data, fb)`
- **test `test_key_order_is_part_of_contract`** [L79-88]: `def test_key_order_is_part_of_contract(data, fb)` - Erratum E4 (R-0223-8): the key sequence follows the given master order; per-key bounds
- **test `test_seed_default_640111`** [L91-95]: `def test_seed_default_640111(data, fb)`
- **test `test_rank_mismatch_fails_numerical`** [L98-111]: `def test_rank_mismatch_fails_numerical(data, monkeypatch)`
- **test `test_bound_ordering`** [L114-116]: `def test_bound_ordering(fb)`
- **function `_events_by_hand`** [L130-156]: `def _events_by_hand(theta)` - Coverage-failure events whose union contains 'a declared response statement is false'.
- **function `_choices`** [L159-165]: `def _choices(lists)`
- **test `test_fw_events_by_hand_at_most_two`** [L169-171]: `def test_fw_events_by_hand_at_most_two(region)` decorators: @pytest.mark.parametrize('region', list(REGIONS))
- **test `test_fw_events_implementation_at_most_two`** [L175-179]: `def test_fw_events_implementation_at_most_two(region)` decorators: @pytest.mark.parametrize('region', list(REGIONS))
- **test `test_fw_events_protocol_counts`** [L182-187]: `def test_fw_events_protocol_counts()`
- **test `test_family_error`** [L190-194]: `def test_family_error()`

