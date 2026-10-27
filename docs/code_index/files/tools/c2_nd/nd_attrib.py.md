# `tools/c2_nd/nd_attrib.py`

- Source: [tools/c2_nd/nd_attrib.py](../../../../../tools/c2_nd/nd_attrib.py)
- Kind: python
- Lines: 265

## Module docstring

> C2ND attribution (closed forms; d = d_named; dy = y1 - y2; arm 1 = H+, arm 2 = H-): the N-R
> complement quantities and stream (Lemma N1), the N-M stream on the C2-M quantities, the D stream
> and the known-case arrays under a refit projector, the estimation leak, canonical angles and
> kappa_leak, the LN-scale split, the oracle response identity and the descriptive ratios (API.md
> §7, §20; C2ND-DESIGN-v1 §2.3, §2.4, §2.8, §2.9, §3 row 9, §4.2).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 15, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 18, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 19, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 20, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 24, import)
- [tests/c2_nd/test_a_identity.py](../../tests/c2_nd/test_a_identity.py.md) (line 25, import)
- [tests/c2_nd/test_a_known.py](../../tests/c2_nd/test_a_known.py.md) (line 26, import)
- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 26, import)
- [tests/c2_nd/test_b_dry_hs.py](../../tests/c2_nd/test_b_dry_hs.py.md) (line 26, import)
- [tests/c2_nd/test_b_layer2.py](../../tests/c2_nd/test_b_layer2.py.md) (line 26, import)
- [tests/c2_nd/test_b_policy.py](../../tests/c2_nd/test_b_policy.py.md) (line 18, import)
- [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 15, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 27, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 23, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 22, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 23, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 17, import)

## Top-level constants

- `C`
- `LEAKAGE`
- `NEC_CASES`
- `NEC_KEYS`
- `NM_KEYS`
- `NR_A`
- `NR_KEYS`

## Classes and functions

- **function `_f`** [L34-35]: `def _f(x) -> np.ndarray`
- **function `_comp`** [L38-40]: `def _comp(P) -> np.ndarray`
- **function `comp_arm`** [L44-47]: `def comp_arm(y1, y2, P_S) -> np.ndarray` - y_C^{2<-1} = y2 + (I - P_S)(y1 - y2): arm 2 receives arm 1's complement.
- **function `nr_quantities`** [L50-60]: `def nr_quantities(d, M, y1, y2, P_S) -> dict` - A_full, A_S, A_comp = A_full - A_S (by subtraction), e_full, e_S, e_comp and the cross
- **function `a_comp_direct`** [L63-65]: `def a_comp_direct(d, z_C, z_2) -> np.ndarray` - The patched complement arm against arm 2's natural logits (X1 compares it with A_comp).
- **function `nr_stream`** [L68-87]: `def nr_stream(q, qy, G_x, E_x, E_y, variants=None) -> dict` - The N-R family stream of one model (§4.2): 10 arrays plus 2 per variant (16 with three);
- **function `nm_stream`** [L98-108]: `def nm_stream(cm, A_full, G_x, E_x) -> dict` - The N-M family stream of one model (7 arrays): categories on A_C against A_F only.
- **function `check_refit`** [L112-118]: `def check_refit(refit, allowed=nc.REFITS) -> str` - The refit tag of a projector dict; the construction projector or the C2 FIT problem R in
- **function `d_stream`** [L121-130]: `def d_stream(qx, qy, G_x, E_x, E_y, qx_r=None, refit=None, refit_r=None) -> dict` - The D family stream of one model: the seven C2 R arrays of D-NULL under the RD refit, and
- **function `case_arrays`** [L133-145]: `def case_arrays(case, qx, qy, G_x, G_y, E_x, E_y, refit=None) -> dict` - KC / KC-R arrays of one case (keys "<case>:<stat>"): the R arrays, the case's own y
- **function `leak`** [L148-150]: `def leak(d, M_prime, dy, P_hat, P_S) -> np.ndarray` - 1/2 d' M' (P_hat - P_S) dy: the D-NULL refit code share is this leak (T-LEAK).
- **function `canonical_angles`** [L153-157]: `def canonical_angles(B_hat, B) -> np.ndarray` - The principal angles between col(B_hat) and col(B), ascending (radians).
- **function `kappa_leak`** [L160-164]: `def kappa_leak(M, P_S, B_hat) -> float` - ||C M (I - P_S) B_hat||_2 / ||C M B_hat||_2 (blind S2 diagnostic; reported, not gated).
- **function `nr_guards`** [L171-188]: `def nr_guards(arrays, geo) -> dict` - N-R guards: beta_A (coefficient 1, delta_P of the frozen C2 projector) on every
- **function `d_guards`** [L191-197]: `def d_guards(arrays, geo_D, geo_R=None) -> dict` - c2_decide.stream_guards on the DNULL arrays (M', RD refit delta_P) and on the "DNULLR:"
- **function `nm_guards`** [L200-201]: `def nm_guards(arrays) -> dict`
- **function `sigma`** [L205-207]: `def sigma(a3, eps) -> np.ndarray` - sqrt(Var(a3_i) + eps) per row of the resid_post_3 rows at position 32 ([n, d_model]).
- **function `ln_split`** [L210-214]: `def ln_split(y1, y2, s1, s2) -> tuple` - (dy_dir, dy_sig): dy_sig = (1 - s1/s2) y1, dy_dir = (s1/s2) y1 - y2 (exact split).
- **function `ln_sym`** [L217-219]: `def ln_sym(y1, y2, s1, s2) -> np.ndarray` - The symmetric sigma part over both arm orders.
- **function `ln_arrays`** [L222-231]: `def ln_arrays(d, M, P_S, y1, y2, s1, s2, M_prime=None) -> dict` - Per-row numerators of the LN-scale shares: 1/2 d' M (I - P_S) dy_sig (complement), with
- **function `oracle_identity`** [L235-244]: `def oracle_identity(qbar_p, qbar_m, d_named, perm, G) -> dict` - A_full with the oracle's own log-predictive equals G per row within 1e-12 max(1, |G|).
- **function `point_ratios_nd`** [L248-254]: `def point_ratios_nd(nums, dens, pairs, E) -> dict` - Eligible-row point ratios mean(num)/mean(den); nan on a zero denominator.
- **function `descriptives_nd`** [L257-265]: `def descriptives_nd(nums, dens, pairs, E, extra=None) -> dict` - The point ratios and one c2_attrib.ratio_intervals call (seed 630508, 5,000 draws; ranks

