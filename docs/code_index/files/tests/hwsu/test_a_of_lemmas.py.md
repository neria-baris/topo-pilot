# `tests/hwsu/test_a_of_lemmas.py`

- Source: [tests/hwsu/test_a_of_lemmas.py](../../../../../tests/hwsu/test_a_of_lemmas.py)
- Kind: python
- Lines: 233

## Module docstring

> Author A (job 0198): Lemmas P1, P2, P3 and J (protocol §2.2; §5.1 KS-P), by exact enumeration
> of the natural suffix-matched pair law on the CONTRACT_OF KS-PAIR chain (L = 8, suffix 4,
> test-side Fractions), and the HWSU pair functions on planted arrays (API §3).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 16, via sys.path edit)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 17, via sys.path edit)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 18, via unique basename)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `itertools` (lines 7)
- `math` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 14: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `COND`
- `EF`
- `LQ4`
- `LQ8`
- `P`
- `PF`
- `PRE`
- `PS`
- `Q4`
- `Q8`
- `REPO`
- `SUF`
- `TF`

## Classes and functions

- **function `joint`** [L31-38]: `def joint(length)`
- **function `lg`** [L51-54]: `def lg(x)` - A fixed rational stand-in for log x: every identity below is algebraic in these values
- **function `dot`** [L61-62]: `def dot(a, b)`
- **function `sub`** [L65-66]: `def sub(a, b)`
- **function `pair_mean`** [L69-75]: `def pair_mean(f)` - E over the natural pair law: P(s) P(p1 | s) P(p2 | s) (Lemma P0).
- **function `row_mean`** [L78-79]: `def row_mean(f)`
- **test `test_predictives_and_tower_property`** [L82-87]: `def test_predictives_and_tower_property()`
- **test `test_lemma_p2_pair_covariance_identity`** [L90-98]: `def test_lemma_p2_pair_covariance_identity()` - ½E[(a¹−a²)ᵀ(b¹−b²)] = E[(a − E[a|S4])ᵀ(b − E[b|S4])], a = log q̄8, b = q̄8.
- **test `test_lemma_j_oracle_response_is_jeffreys`** [L101-106]: `def test_lemma_j_oracle_response_is_jeffreys()`
- **test `test_lemma_p1_suffix_only_predictor_reads_nothing`** [L109-116]: `def test_lemma_p1_suffix_only_predictor_reads_nothing()` - A predictor whose logits depend on the suffix only has A ≡ 0 on every pair.
- **test `test_lemma_p3_code_interchange_moves_only_the_beyond_four_part`** [L119-128]: `def test_lemma_p3_code_interchange_moves_only_the_beyond_four_part()`
- **function `_simplex`** [L132-134]: `def _simplex(rng, n, v=36)`
- **function `_helmert`** [L137-142]: `def _helmert(n=36)`
- **function `planted`** [L146-155]: `def planted()` decorators: @pytest.fixture(scope='module')
- **test `test_pair_core_equals_c1_oracle_G_hat`** [L158-165]: `def test_pair_core_equals_c1_oracle_G_hat(planted)`
- **test `test_readout_A_formula_and_suffix_only_zero`** [L168-179]: `def test_readout_A_formula_and_suffix_only_zero(planted)`
- **test `test_lemma_p_arrays_match_the_formulas`** [L182-204]: `def test_lemma_p_arrays_match_the_formulas(planted)`
- **test `test_label_share_formula`** [L207-218]: `def test_label_share_formula(planted)`
- **test `test_label_share_zero_when_circular_marginals_agree`** [L221-233]: `def test_label_share_zero_when_circular_marginals_agree()`

