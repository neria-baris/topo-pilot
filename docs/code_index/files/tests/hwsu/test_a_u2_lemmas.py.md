# `tests/hwsu/test_a_u2_lemmas.py`

- Source: [tests/hwsu/test_a_u2_lemmas.py](../../../../../tests/hwsu/test_a_u2_lemmas.py)
- Kind: python
- Lines: 175

## Module docstring

> Author A (job 0223): Lemmas P1, P2 and J by exact enumeration in Fractions on the phase-1
> non-reversible chain (protocol 2.2, 2.6; 5.1 KS-P), and the DRU case udry2.ks_p.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 19, via sys.path edit)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../../tools/hwsu/hwsu_dry.py.md) (line 20, via sys.path edit)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 27, via sys.path edit) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 13)
- `importlib` (lines 9)
- `itertools` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 29: `dynamic: name`

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `L4`
- `L8`
- `P`
- `PRE`
- `PS`
- `Q4`
- `Q8`
- `REPO`
- `SUF`

## Classes and functions

- **function `mod`** [L26-29]: `def mod(name)`
- **function `_chain`** [L32-37]: `def _chain()`
- **function `joint`** [L44-51]: `def joint(length)`
- **function `lg`** [L62-63]: `def lg(x)`
- **function `dot`** [L70-71]: `def dot(a, b)`
- **function `sub`** [L74-75]: `def sub(a, b)`
- **function `pair_moment`** [L78-93]: `def pair_moment(fa, fb, matched=True)` - 1/2 E[(a1 - a2)^T (b1 - b2)] under the pair law (matched) or independent histories.
- **function `cond_cov`** [L96-103]: `def cond_cov(fa, fb)`
- **function `fa`** [L106-107]: `def fa(h)`
- **function `fb`** [L110-111]: `def fb(h)`
- **test `test_chain_is_valid_and_nonreversible`** [L114-118]: `def test_chain_is_valid_and_nonreversible()`
- **test `test_lemma_p2_pair_moment_equals_conditional_covariance`** [L121-123]: `def test_lemma_p2_pair_moment_equals_conditional_covariance()`
- **test `test_lemma_p2_A_full_mean_equals_z_rho4`** [L126-134]: `def test_lemma_p2_A_full_mean_equals_z_rho4()` - E[A_full] with d = q1 - q2 equals E[z^T rho4], rho4 = q32 - q4 (z any history function).
- **test `test_lemma_j_G_equals_two_kls`** [L137-147]: `def test_lemma_j_G_equals_two_kls()`
- **test `test_lemma_p1_suffix_only_predictor_has_zero_effect`** [L150-155]: `def test_lemma_p1_suffix_only_predictor_has_zero_effect()`
- **test `test_planted_defect_independent_suffixes_breaks_identity`** [L158-165]: `def test_planted_defect_independent_suffixes_breaks_identity()` - Pairs built from independent histories (suffix not shared) do not satisfy Lemma P2/P1.
- **test `test_ks_p_dru_case_passes`** [L168-171]: `def test_ks_p_dru_case_passes(tmp_path)`
- **test `test_uc_contract_loaded`** [L174-175]: `def test_uc_contract_loaded()`

