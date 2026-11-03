# `tests/hwsu/test_a_u2_known.py`

- Source: [tests/hwsu/test_a_u2_known.py](../../../../../tests/hwsu/test_a_u2_known.py)
- Kind: python
- Lines: 101

## Module docstring

> Author A (job 0223): KO1-KO3 at VAL and TEST (protocol 5.2; API_U2 4.1 KC-U, 4.6) and KS-RULES.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 16, via sys.path edit)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 17, via sys.path edit)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 23, via sys.path edit) (inside a function)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 80, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 7)
- `importlib` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 25: `dynamic: name`

### sys.path additions

- line 14: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `mod`** [L22-25]: `def mod(name)`
- **function `_probs`** [L28-30]: `def _probs(rng, n, V=36)`
- **function `world`** [L34-46]: `def world()` decorators: @pytest.fixture(scope='module') - Tiny synthetic oracle: q32 per arm, a shared suffix predictive q4.
- **test `test_ko_identities`** [L49-52]: `def test_ko_identities(world)`
- **test `test_ko_categories_at_val_and_test_seeds`** [L56-62]: `def test_ko_categories_at_val_and_test_seeds(world, seed)` decorators: @pytest.mark.parametrize('seed', [640112, 640118])
- **test `test_contract_seed_uses`** [L65-67]: `def test_contract_seed_uses()`
- **test `test_planted_lambda_breaks_ko3`** [L70-75]: `def test_planted_lambda_breaks_ko3(world)`
- **test `test_kc_u_planted_lambda_fails_known_case`** [L78-96]: `def test_kc_u_planted_lambda_fails_known_case(world, monkeypatch)` - kc_u must fail closed FAIL_TECHNICAL/KNOWN_CASE when KO3 uses lambda != 1/5.
- **test `test_ks_rules_passes`** [L99-101]: `def test_ks_rules_passes(tmp_path)`

