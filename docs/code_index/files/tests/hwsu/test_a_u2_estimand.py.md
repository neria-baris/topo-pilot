# `tests/hwsu/test_a_u2_estimand.py`

- Source: [tests/hwsu/test_a_u2_estimand.py](../../../../../tests/hwsu/test_a_u2_estimand.py)
- Kind: python
- Lines: 153

## Module docstring

> Author A (job 0223): the response estimand theta and A_full (protocol 2.5; API_U2 1.2, 4.7).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 18, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 19, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 20, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 21, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 29, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 87)
- `importlib` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 31: `dynamic: name`

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `MASTERS`
- `REPO`

## Classes and functions

- **function `mod`** [L28-31]: `def mod(name)`
- **function `_basis`** [L34-36]: `def _basis(rng, V=36, k=127)`
- **function `_probs`** [L39-41]: `def _probs(rng, n, V=36)`
- **test `test_a_full_equals_half_dot_of_closed_logit_difference`** [L44-54]: `def test_a_full_equals_half_dot_of_closed_logit_difference()`
- **test `test_a_full_uses_named_d_and_canonical_d_is_wrong`** [L57-71]: `def test_a_full_uses_named_d_and_canonical_d_is_wrong()`
- **test `test_response_arrays_exact`** [L74-83]: `def test_response_arrays_exact()`
- **test `test_response_arrays_constants_are_contract_lines`** [L86-93]: `def test_response_arrays_constants_are_contract_lines()`
- **test `test_suffix_only_readout_gives_zero_bitwise`** [L96-115]: `def test_suffix_only_readout_gives_zero_bitwise()` - Lemma P1: a readout that is a function of w29..w32 gives y1 == y2 on suffix-matched pairs.
- **test `test_oracle_readout_gives_A_equal_G_via_helmert`** [L118-131]: `def test_oracle_readout_gives_A_equal_G_via_helmert()` - Lemma D2: with M = N (Helmert), y = log q N, A_full equals the phase-1 readout_A and G.
- **test `test_theta_hat_is_ratio_of_tree_means`** [L134-153]: `def test_theta_hat_is_ratio_of_tree_means(tmp_path)` - theta_j in SEALED_VALIDATION.json = tree_mean(A_j) / tree_mean(G) (API_U2 4.7).

