# `tests/c2_readout/test_a_scope.py`

- Source: [tests/c2_readout/test_a_scope.py](../../../../../tests/c2_readout/test_a_scope.py)
- Kind: python
- Lines: 321

## Module docstring

> Independent tests, author A (job 0101): T-SCOPE (RC-2, NEW-4; run with the R and the S*
> parameterisation), T-LEAK (RC-7) and T-PROJ (C2-FROZEN-v1 2.4-2.6, 3.1, 6.3-6.6, 13.3).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 35, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 36, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 37, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 38, via sys.path edit)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 39, via sys.path edit)

### External (third-party)

- `numpy` (lines 28)
- `pytest` (lines 29)

### Standard library

- `__future__` (lines 22)
- `functools` (lines 24)
- `pathlib` (lines 26)
- `sys` (lines 25)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 33: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `OUTCOME`
- `P1`
- `QCODE`
- `REPO`
- `VALUES`

## Classes and functions

- **function `_harm`** [L54-55]: `def _harm(phi, K)`
- **function `_world`** [L58-65]: `def _world(kind, seed=21)`
- **function `_zt`** [L68-72]: `def _zt(W, phi, xi)`
- **function `_rep`** [L75-81]: `def _rep(W, w, zt, phi, rng)`
- **function `_head`** [L84-86]: `def _head(W, fit)`
- **function `_regressors`** [L89-91]: `def _regressors(fam, phi, K)`
- **function `_pairs`** [L94-102]: `def _pairs(W, fam, g, fit, n, seed)`
- **function `_arrays`** [L105-115]: `def _arrays(d, M, dy, P_S, P_G, G, Sigma, prefix='')`
- **function `_b`** [L118-121]: `def _b(stats, model=1729, draws=2000)`
- **function `_pipeline`** [L125-171]: `def _pipeline(kind, fam)` decorators: @functools.lru_cache(maxsize=None)
- **test `test_out_of_code_and_excluded_direction_fixtures`** [L177-194]: `def test_out_of_code_and_excluded_direction_fixtures(kind, fam)` decorators: @pytest.mark.parametrize('fam', ['R', 'S*']) @pytest.mark.parametrize('kind', ['i-a', 'i-b', 'ii'])
- **test `test_interaction_fixture_is_orthogonal_to_the_additive_regressors`** [L197-205]: `def test_interaction_fixture_is_orthogonal_to_the_additive_regressors()`
- **function `_placebo`** [L209-222]: `def _placebo(out, coef_code, coef_other, n=1200, seed=31)` - The y pair (H, H^Y) of v2 2.2 on its E_y rows: dyY = y(H) - y(H^Y), d^Y, A^Y.
- **test `test_planted_y_direction_inside_col_B_fails_y1`** [L225-231]: `def test_planted_y_direction_inside_col_B_fails_y1()`
- **test `test_large_negative_placebo_passes_y1_and_licence_states_only_the_inequality`** [L234-249]: `def test_large_negative_placebo_passes_y1_and_licence_states_only_the_inequality()`
- **function `_proj_problem`** [L253-259]: `def _proj_problem(seed=41)`
- **function `_rows_through`** [L262-270]: `def _rows_through(M_dir, dirs, n=1200, seed=42)`
- **test `test_projector_dependent_when_euclidean_complement_changes_the_category`** [L273-298]: `def test_projector_dependent_when_euclidean_complement_changes_the_category()`
- **test `test_harmonic_dependent_when_the_k1_variant_changes_the_category`** [L301-321]: `def test_harmonic_dependent_when_the_k1_variant_changes_the_category()`

