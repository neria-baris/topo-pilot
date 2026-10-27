# `tools/c2_nd/nd_decoy.py`

- Source: [tools/c2_nd/nd_decoy.py](../../../../../tools/c2_nd/nd_decoy.py)
- Kind: python
- Lines: 373

## Module docstring

> C2ND decoys: the head edits D-NULL, D-NULL1, D-ONLY, D-DOSE (Lemmas DC1-DC3), the null basis
> V0, the move U and the map T (Lemma DC4), the coordinate wrapper and its basis adapter,
> decoy_sha64 and the construction record, M0-D (§3 row 11) and DX (§3 row 20) (API.md §6, §20;
> C2ND-DESIGN-v1 §2.6-§2.7).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 18, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 21, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 22, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 23, via unique basename)

### External (third-party)

- `numpy` (lines 24)
- `torch` (lines 25)

### Standard library

- `__future__` (lines 11)
- `copy` (lines 13)
- `fractions` (lines 16)
- `hashlib` (lines 14)
- `json` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 26, import)
- [tests/c2_nd/test_a_identity.py](../../tests/c2_nd/test_a_identity.py.md) (line 27, import)
- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 27, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 28, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 26, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 24, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 24, import)

## Top-level constants

- `BASIS_KEYS`
- `NUMERICAL`

## Classes and functions

- **function `_f`** [L32-33]: `def _f(x) -> np.ndarray`
- **function `_np`** [L36-37]: `def _np(t) -> np.ndarray`
- **function `_mx`** [L40-42]: `def _mx(x) -> float`
- **function `_le`** [L45-47]: `def _le(x, tol) -> bool` - x <= tol (CONTRACT string) in exact rationals; a non-finite x fails.
- **function `base_inputs`** [L51-56]: `def base_inputs(c2_fit, basis) -> dict` - The readout basis of model64 and the frozen C2 problem R (P_S, B, L_B = R_L[5:], Gamma).
- **function `pi_S`** [L59-60]: `def pi_S(Q0, P_S) -> np.ndarray`
- **function `head_edit`** [L63-75]: `def head_edit(kind, WU, Q0, P_S, g=nc.G_D, rho=nc.RHO) -> np.ndarray` - W'_U in exactly the CONTRACT association g * (WU @ (I - Pi_S)) (ND-C15, §20 B-8).
- **function `_with_head`** [L78-82]: `def _with_head(dec, W)`
- **function `make_head_decoy`** [L85-87]: `def make_head_decoy(model64, W)` - A deep copy of model64 with only unembed.weight replaced (float64).
- **function `null_basis`** [L91-95]: `def null_basis(M) -> np.ndarray` - An orthonormal basis of ker(M): right singular vectors with sv <= 1e-12 sigma_max.
- **function `move_map`** [L98-119]: `def move_map(B, L_B, M) -> dict` - U = V0 (L_B V0)^+, T = I + (U - B) L_B, Tinv = I + (B - U) L_B and the construction gates.
- **class `CoordMap(torch.nn.Module)`** [L122-131] - u -> beta + ((u - beta) @ Q0) @ T.T @ Q0.T over the last dimension (float64 buffers).
- **method `CoordMap.__init__`** [L125-128]: `def __init__(self, beta, Q0, T)`
- **method `CoordMap.forward`** [L130-131]: `def forward(self, u)`
- **function `coord_head`** [L134-139]: `def coord_head(kind, WU, Q0, Tinv, g=nc.G_D) -> np.ndarray`
- **function `make_coord_decoy`** [L142-147]: `def make_coord_decoy(model64, kind, Q0, beta, T, Tinv, WU, g=nc.G_D)` - A deep copy whose ln_final is Sequential(the base LayerNorm, CoordMap) and whose head is
- **function `coord_basis`** [L150-155]: `def coord_basis(decoy, base_basis) -> dict` - The readout_basis keys with the base LayerNorm basis and the decoy's head (§11.2).
- **function `decoy_basis`** [L158-159]: `def decoy_basis(decoy, base_basis) -> dict`
- **function `_is_coord`** [L162-163]: `def _is_coord(decoy) -> bool`
- **function `decoy_sha64`** [L167-176]: `def decoy_sha64(decoy, record) -> str` - sha256 over (key, NUL, shape, NUL, float64 bytes) per sorted state_dict key, then the
- **function `decoy_record`** [L179-189]: `def decoy_record(j, kind) -> dict`
- **function `construction_record`** [L192-195]: `def construction_record(j, kind, decoy, extra=None) -> dict` - The record plus decoy_sha64 and `extra` (coordinate decoys: cond_T, sv_LBV0, k0, U/B).
- **function `nullity`** [L199-205]: `def nullity(heads, B) -> dict` - {"null_<kind>": ||C M' B||_max / (||C M'||_max ||B||_max)} (C centres the outputs).
- **function `adapter_identities`** [L208-221]: `def adapter_identities(V0, U, T, Tinv, B, Gamma, L_B, M, heads, dz=None) -> dict` - The 1e-10 adapter identities of §3 row 11 (vii), norm-scaled (API.md §6.5, §20 A-2).
- **function `_tokens`** [L224-227]: `def _tokens(inputs) -> torch.Tensor`
- **function `_pairs`** [L230-232]: `def _pairs(z) -> np.ndarray`
- **function `_one`** [L235-272]: `def _one(kind, dec, model64, inp, base_basis, inputs, acts, policy, mm) -> tuple` - Items (i)-(v) and (viii) of one decoy; returns (items, values, logits).
- **function `m0d`** [L275-332]: `def m0d(j, model64, decoys, base_basis, c2_fit, inputs, acts, z_base, policy) -> dict` - M0-D on the given rows (API.md §6.5, §20 B-1): items (i)-(viii) per decoy. A head edit
- **function `_rows_over`** [L336-338]: `def _rows_over(num, den_scale, tol) -> np.ndarray`
- **function `dx`** [L341-373]: `def dx(arrays, policy) -> dict` - Per row with the construction projector: the exact non-use, dose, code-only and

