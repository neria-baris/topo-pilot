# `tools/c2_readout/c2_oracle.py`

- Source: [tools/c2_readout/c2_oracle.py](../../../../../tools/c2_readout/c2_oracle.py)
- Kind: python
- Lines: 343

## Module docstring

> C2 oracle: process loading, the H1 static checks, the canonical oracle for the four
> histories (H^Y by the exact oracle forward on its defined rows only), the normalised predictive,
> d and G for the x and y pairs, the five nuisance covariates, eligibility, kappa_m, the x leakage
> of the y pair, zero-modulus flags, the H3 composition with the Decimal rows, and the rotation
> oracle (API.md §6, §19.3; C2-FROZEN-v2 §2.2, §2.3, §2.11, §2.12, §5.4, §7 rows 3, 6).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 16, via same directory)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../c1prime/c1_cert.py.md) (line 19, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 20, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 21, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 22, via unique basename)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](../x4_oracle_profile/inputs.py.md) (line 33, via unique basename) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 34, via unique basename) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 64, via same directory) (inside a function)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 267, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 12)
- `fractions` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 36, import)
- [tests/c2_readout/test_a_readout.py](../../tests/c2_readout/test_a_readout.py.md) (line 31, import)
- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 26, import)
- [tests/c2_readout/test_b_screens.py](../../tests/c2_readout/test_b_screens.py.md) (line 24, import)
- [tools/c2_nd/nd_dry.py](../c2_nd/nd_dry.py.md) (line 25, import)
- [tools/c2_nd/nd_split.py](../c2_nd/nd_split.py.md) (line 20, import)
- [tools/c2_nd/nd_stage_base.py](../c2_nd/nd_stage_base.py.md) (line 24, import)
- [tools/c2_nd/nd_stage_post.py](../c2_nd/nd_stage_post.py.md) (line 21, import)
- [tools/c2_nd/nd_stage_pre.py](../c2_nd/nd_stage_pre.py.md) (line 21, import)
- [tools/c2_readout/c2_code.py](c2_code.py.md) (line 19, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 26, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 19, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 23, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 19, import)

## Top-level constants

- `NUMERICAL`
- `_RANK`

## Classes and functions

- **function `load_process`** [L31-58]: `def load_process() -> dict` - The job-0014 inputs.load_config/load_process (unchanged), keyed by int model seed.
- **function `h1_static`** [L61-83]: `def h1_static(proc) -> dict` - C1 H1 unchanged (ids, validate_process, permutations, round trip, identical canonical
- **function `oracle_role`** [L87-101]: `def oracle_role(T, E, pi, tokens32, coords=None) -> dict` - c1_oracle.run_oracle plus q-bar; "m32" only when coords is given (API.md §19.1 E-5).
- **function `_scatter`** [L104-110]: `def _scatter(o, rows, n, N, V) -> dict` - n-row arrays of a role computed on `rows` only (NaN elsewhere: no H^Y is formed there).
- **function `oracle_split`** [L113-134]: `def oracle_split(T, E, pi, coords, canon32, k, o_H=None) -> dict` - The four roles (H from the H2 cache o_H when given; H^Y by the exact oracle forward on
- **function `nuisance5`** [L137-145]: `def nuisance5(b32, coords) -> np.ndarray` - (y-bar, Var y, |m32|) of c1_oracle.nuisance, the entropy (nats, 0 log 0 = 0) and the
- **function `d_named`** [L148-149]: `def d_named(d_canon, perm) -> np.ndarray`
- **function `s_max`** [L152-153]: `def s_max(s_fit_H) -> float`
- **function `eligibility`** [L156-163]: `def eligibility(o, smax) -> dict` - E_x (c1_oracle.eligible); E_y = Y_def, s(H^Y) <= s_max, finite log-evidence of H, H^Y.
- **function `kappa_m`** [L166-169]: `def kappa_m(m32_H, m32_HY, E_y_fit, m32_H_fit) -> float`
- **function `y_active`** [L172-173]: `def y_active(kappa) -> bool`
- **function `kappa_nu`** [L176-178]: `def kappa_nu(o_fit, E_x_fit, coords) -> float`
- **function `x_leakage`** [L181-191]: `def x_leakage(o, E_x, E_y, coords) -> dict` - lambda_x at b31 and b32: mean_{E_y} |m32(H^Y) - m32(H)| / mean_{E_x} |m32(H+) - m32(H-)|
- **function `phi_star`** [L194-198]: `def phi_star(m32) -> tuple` - Oracle x-phase arg m32 and m_valid = |m32| > 1e-12; the phase is 0.0 on invalid rows.
- **function `reason_flags`** [L201-214]: `def reason_flags(o, smax) -> dict` - The §5.5 oracle reasons of c2_data.REASONS; S_Y and LIK_Y only where H^Y is defined.
- **function `_rel_rows`** [L218-219]: `def _rel_rows(xh, xr, tol) -> bool`
- **function `_worst`** [L222-223]: `def _worst(a, b) -> str`
- **function `_closed_forms`** [L226-236]: `def _closed_forms(T, E, coords, canon, o, tol) -> bool` - The x pair only (T3): b32(H+-) = (rho_+-1 b31(H) T) * E[:, w32]; H^Y has no closed form.
- **function `_named_and_cross`** [L239-256]: `def _named_and_cross(T, pi, perms, E_named, canon, o) -> tuple`
- **function `_lowest`** [L259-261]: `def _lowest(E, seq, n=None) -> np.ndarray`
- **function `h3`** [L264-300]: `def h3(T, E, pi, coords, perms, E_named, splits, p0=None) -> dict` - H3 in the API.md §6.3/§19.3 order; `splits` = {split: (canon32, o, E_x, E_y, seq_ids)}.
- **function `decimal_rows`** [L303-330]: `def decimal_rows(T, E, pi, canon32, o, rows_x, rows_y, p0) -> str` - C1' H3 Decimal rows with the C1' fast-path rule (API.md C-7): b31, b32 and q by
- **function `rotation_oracle`** [L334-343]: `def rotation_oracle(b31_H, T, E, w32, coords, m) -> dict` - Roll the pre-last-symbol belief by +-m cells and re-apply w32 (corrected oracle, Q1).

