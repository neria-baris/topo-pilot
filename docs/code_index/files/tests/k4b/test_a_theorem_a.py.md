# `tests/k4b/test_a_theorem_a.py`

- Source: [tests/k4b/test_a_theorem_a.py](../../../../../tests/k4b/test_a_theorem_a.py)
- Kind: python
- Lines: 268

## Module docstring

> K4b author A, TEST_PLAN A2 (protocol §1.4, §11.4): Theorem A on the Proposition-1 HMM.

## Imports

### Internal (repo files)

- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 238, via sys.path edit) (inside a function)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 239, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 13)
- `functools` (lines 14)
- `itertools` (lines 15)
- `math` (lines 11)
- `pathlib` (lines 16)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `C`
- `D`
- `E`
- `E1`
- `GRID`
- `PI`
- `REPO`
- `T`
- `UNITS`

## Classes and functions

- **function `stationary`** [L42-53]: `def stationary(Tm)`
- **function `forward`** [L59-63]: `def forward(start, obs)`
- **function `mean_of`** [L66-69]: `def mean_of(a)`
- **function `dot`** [L72-73]: `def dot(u, v)`
- **function `in_support`** [L76-78]: `def in_support(w, r)` - Correlated with the prefix (w1) and with the residual sign.
- **function `rows`** [L82-93]: `def rows()` decorators: @lru_cache(maxsize=None)
- **function `endpoints`** [L96-103]: `def endpoints(sup=None, field=None)` - Brackets of E X- and E X+: (EXm_lo, EXm_hi, EXp_lo, EXp_hi, supported part).
- **function `delta`** [L106-113]: `def delta(completion)` - Delta4(u~) = E[u~ . r] over the joint law of (w, z_L); u~ = u on S.
- **function `pointwise_ok`** [L116-124]: `def pointwise_ok(completion)`
- **test `test_support_is_mixed_and_prefix_correlated`** [L127-136]: `def test_support_is_mixed_and_prefix_correlated()`
- **test `test_grid_completions_lie_in_bounds`** [L139-149]: `def test_grid_completions_lie_in_bounds()`
- **test `test_randomised_completion_lies_in_bounds`** [L152-159]: `def test_randomised_completion_lies_in_bounds()` - Auxiliary randomness w': u~ = v1 w.p. 1/3 and v2 w.p. 2/3 (Fubini).
- **function `scaled`** [L162-165]: `def scaled(sign, c=Fr(1))` - u~ = sign * c * r * D / (k+1) on S^c: |u~| < 1, and u~ . r = sign * c * s D / (k+1).
- **test `test_sharpness_extremal_completions`** [L168-177]: `def test_sharpness_extremal_completions()`
- **test `test_continuity_path_exact_affine_family`** [L180-193]: `def test_continuity_path_exact_affine_family()`
- **test `test_continuity_path_unit_rotation_float`** [L196-218]: `def test_continuity_path_unit_rotation_float()` - u~_theta = R_theta(-r/|r|): E[u~ . r] = E[X- 1_S] - cos(theta) E[|r| 1_{S^c}].
- **test `test_conditioning_on_support_is_spurious_but_bounds_hold`** [L221-234]: `def test_conditioning_on_support_is_spurious_but_bounds_hold()` - u = e1 on S' (a suffix-only field). Delta4(e1) = 0 exactly (Proposition 1), yet the
- **test `test_endpoint_arrays_row_construction`** [L237-268]: `def test_endpoint_arrays_row_construction()`

