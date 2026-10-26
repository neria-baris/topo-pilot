# `tests/c2_readout/test_a_oracle.py`

- Source: [tests/c2_readout/test_a_oracle.py](../../../../../tests/c2_readout/test_a_oracle.py)
- Kind: python
- Lines: 400

## Module docstring

> Independent tests, author A (job 0101; v2 update, job 0105): T-ORACLE with the y-translation
> donor H^Y (D-0104-1) and T-ROT (RC-14) (C2-FROZEN-v2 2.2, 2.3, 2.11, 5.4, 5.5, 13.3), and
> T-LADDER (RC-15; 6.7; targets cs.p1, cs.n_test), moved here from test_a_gls.py (400 lines).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 31, via sys.path edit)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../tools/c1prime/c1_oracle.py.md) (line 32, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 33, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 34, via sys.path edit)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 35, via sys.path edit)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../../tools/c2_readout/c2_oracle.py.md) (line 36, via sys.path edit)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 37, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 38, via unique basename)

### External (third-party)

- `numpy` (lines 24)
- `pytest` (lines 25)

### Standard library

- `__future__` (lines 18)
- `fractions` (lines 21)
- `pathlib` (lines 22)
- `sys` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `EX`
- `EY5`
- `MODELS`
- `REPO`
- `SEEDS`

## Classes and functions

- **function `_hmm`** [L46-61]: `def _hmm()`
- **function `_filter`** [L64-73]: `def _filter(T, E, pi, tokens)` - Exact forward filter: b_t = a_t * E[:, w_t] / norm, a_{t+1} = b_t T; returns b31, b32.
- **function `_canon`** [L76-81]: `def _canon(n=6, seed=0, rows=(1, 4))` - Canonical histories whose prefix symbols lie in symbol rows rows[0]..rows[1].
- **function `_hy_ref`** [L84-92]: `def _hy_ref(H, k)` - Independent H^Y (v2 2.2): b -> b + k on w1..w31, a and w32 kept; Y_def per row.
- **function `_split`** [L95-98]: `def _split(T, E, pi, coords, H)`
- **test `test_k_y_sign_rule_with_the_tie_going_to_minus_one`** [L102-114]: `def test_k_y_sign_rule_with_the_tie_going_to_minus_one()`
- **test `test_y_donor_shifts_the_symbol_row_and_keeps_column_and_w32`** [L117-130]: `def test_y_donor_shifts_the_symbol_row_and_keeps_column_and_w32()`
- **test `test_off_grid_rule_never_clamps_or_wraps_and_forms_no_HY`** [L133-156]: `def test_off_grid_rule_never_clamps_or_wraps_and_forms_no_HY()`
- **test `test_oracle_split_HY_by_exact_forward_eligibility_f_y_and_x_leakage`** [L159-205]: `def test_oracle_split_HY_by_exact_forward_eligibility_f_y_and_x_leakage()`
- **test `test_rho_m_index_maps_on_the_full_grid`** [L208-217]: `def test_rho_m_index_maps_on_the_full_grid()`
- **test `test_rotation_oracle_rolls_b31_and_reapplies_w32`** [L221-240]: `def test_rotation_oracle_rolls_b31_and_reapplies_w32(m)` decorators: @pytest.mark.parametrize('m', [1, 2])
- **function `_f`** [L244-245]: `def _f(phi, K)`
- **test `test_frozen_orientation_rotates_every_harmonic_by_k_theta`** [L249-259]: `def test_frozen_orientation_rotates_every_harmonic_by_k_theta(theta)` decorators: @pytest.mark.parametrize('theta', [np.pi / 6, np.pi / 3])
- **function `_rot_world`** [L262-270]: `def _rot_world(n=300, seed=5)`
- **test `test_y_rot_rotates_the_code_and_holds_every_other_coordinate`** [L273-281]: `def test_y_rot_rotates_the_code_and_holds_every_other_coordinate()`
- **test `test_exact_sign_fixture_plus_theta_moves_toward_the_plus_rolled_belief`** [L285-316]: `def test_exact_sign_fixture_plus_theta_moves_toward_the_plus_rolled_belief(m, theta)` decorators: @pytest.mark.parametrize('m, theta', [(1, np.pi / 6), (2, np.pi / 3)])
- **function `_ladder`** [L324-355]: `def _ladder(monkeypatch, family, pass_at)` - Stub the kernels: record their arguments; per-model pass/fail by (array, N).
- **test `test_p1_calls_kernels_with_the_registered_cfg_and_seeds`** [L359-372]: `def test_p1_calls_kernels_with_the_registered_cfg_and_seeds(monkeypatch, family)` decorators: @pytest.mark.parametrize('family', ['R', 'M', 'S*'])
- **function `_pa`** [L375-380]: `def _pa(**kw)`
- **test `test_p1_n_f_rules_and_precision_limited`** [L390-394]: `def test_p1_n_f_rules_and_precision_limited(monkeypatch, pass_at, n_f, limited, status)` decorators: @pytest.mark.parametrize('pass_at, n_f, limited, status', [(_pa(Z010={1729: 8192}), 8192, [], 'PASS'), (_pa(Z050={3141: None}), 4096, [3141], 'PASS'), (_pa(Z010={2718: 16384}, Z050={3141: 8192}), 16384, [], 'PASS'), (_pa(Z010={2718: 16384}, Z050={3141: None}), 16384, [3141], 'PASS'), (_pa(Z010={1729: None, 2718: None}), None, None, 'INCONCLUSIVE/UNDERPOWERED')])
- **test `test_n_test_is_the_max_over_alive_families`** [L397-400]: `def test_n_test_is_the_max_over_alive_families()`

