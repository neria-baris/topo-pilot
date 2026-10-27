# `tools/c2_nd/nd_split.py`

- Source: [tools/c2_nd/nd_split.py](../../../../../tools/c2_nd/nd_split.py)
- Kind: python
- Lines: 400

## Module docstring

> C2ND split-level helpers (the second extra module of job 0125, ND-C44; split out of
> nd_stage_pre by function group): sampling with the Y-donor preparation, the oracle writer and
> H3, H5 bounds, the decoy builder and its S4/S5 rebuild check, the M0 rows, and the L1, R1, N2
> and support checks of DFEAS that T-PRE reuses on DTEST (API.md §10).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 10, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 13, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 14, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../c2_readout/c2_code.py.md) (line 15, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 16, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 17, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 18, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 19, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 20, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 21, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 22, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 23, via same directory)
- `import nd_data` -> [tools/c2_nd/nd_data.py](nd_data.py.md) (line 24, via same directory)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 25, via same directory)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](nd_decoy.py.md) (line 26, via same directory)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 27, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 28, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 31, via unique basename)
- `from nd_stage_base import EXC, J1, OK, X3, bundle, c2fit, js, npz, orc, problem, proc, put, rec` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 32, via same directory)

### External (third-party)

- `numpy` (lines 29)
- `torch` (lines 30)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_dry_hs.py](../../tests/c2_nd/test_b_dry_hs.py.md) (line 31, import)
- [tests/c2_nd/test_impl_dry_hs.py](../../tests/c2_nd/test_impl_dry_hs.py.md) (line 34, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 27, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 29, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 20, import)

## Top-level constants

- `DREF`

## Classes and functions

- **function `w32`** [L39-40]: `def w32(ctx, split) -> np.ndarray`
- **function `afull`** [L43-48]: `def afull(ctx, split, j, pair, M=None) -> tuple` - (d named, dy, A_full) of the natural x or y pair under the readout M (base default).
- **function `move_T`** [L51-53]: `def move_T(ctx, j)`
- **function `Yof`** [L56-59]: `def Yof(src, X, r, T=None) -> np.ndarray`
- **function `zt`** [L62-64]: `def zt(ctx, split, j, src) -> np.ndarray`
- **function `decs`** [L67-72]: `def decs(ctx, j, src) -> dict`
- **function `build_decoys`** [L75-85]: `def build_decoys(ctx, j) -> tuple` - ({kind: decoy}, move map, base basis) from the frozen C2 problem R (§2.6, Lemma DC4).
- **function `decoys`** [L88-99]: `def decoys(ctx, j) -> dict` - {kind: (decoy, basis)} rebuilt at S4/S5; decoy_sha64 must equal the S2 record.
- **function `l1_check`** [L103-108]: `def l1_check(ctx, split, j, src) -> tuple`
- **function `r1_check`** [L111-118]: `def r1_check(ctx, split, j, src) -> tuple`
- **function `n2_check`** [L121-131]: `def n2_check(ctx, split, j) -> tuple`
- **function `support`** [L134-137]: `def support(ctx, split, j) -> dict`
- **function `h5_bounds`** [L140-147]: `def h5_bounds(ob, level=nc.H5) -> dict` - Rank-250 lower bounds (5,000 draws, seed 630518, one call per pair) of mean G | E.
- **function `sample`** [L150-173]: `def sample(ctx, blocks, version) -> dict` - H2 / REG2: the splits (scope c2nd-v1, or c2nd-dry-v1 in a dry-run store), the Y-donor
- **function `h3_run`** [L176-193]: `def h3_run(ctx, splits) -> tuple` - The four-role oracle per split from the sampling cache, eligibility with the frozen C2
- **function `m0_rows`** [L196-206]: `def m0_rows(ctx, split, j) -> tuple` - (rows, inputs, hooks, natural logits, basis) on the 1,024 lowest-id rows (M0, M0-D).
- **function `bounds`** [L210-212]: `def bounds(arrays, guards, seed, alpha=nc.VAL_ALPHA, draws=nc.VAL_DRAWS) -> dict`
- **function `split_b`** [L215-216]: `def split_b(b, j) -> dict`
- **function `E`** [L219-220]: `def E(ctx, split, p) -> np.ndarray`
- **function `lowid`** [L223-225]: `def lowid(Ex, seq, n=nc.LOWID_ROWS) -> np.ndarray`
- **function `ys`** [L228-231]: `def ys(ctx, split, j, kind=None) -> dict` - Readout coordinates per role: y, or y @ T.T for a coordinate decoy.
- **function `readout`** [L234-235]: `def readout(ctx, j, kind) -> np.ndarray`
- **function `quant`** [L238-249]: `def quant(ctx, split, j, kind=None, P=None) -> dict` - x and y pair quantities under the readout of `kind` (None: base) and the problem P
- **function `head_logits`** [L252-257]: `def head_logits(dec, u) -> np.ndarray` - The decoy's natural logits from the base ln_final_out (head-only path, §9).
- **function `_arms`** [L261-265]: `def _arms(X, y, rows, P, prefix, seq) -> dict` - The x interchange arms 21, 12 (arm 2's tokens, C2 C-23) on `rows`.
- **function `x1_model`** [L268-309]: `def x1_model(ctx, split, j) -> list` - §3 row 19: base natural, R interchange and direct complement arms (compared with
- **function `dx_model`** [L312-325]: `def dx_model(ctx, split, j) -> dict` - §3 row 20 with the construction projector (the frozen C2 R P_S) on the eligible rows.
- **function `cm_pair`** [L329-344]: `def cm_pair(ctx, split, j, kind) -> dict`
- **function `_m`** [L348-349]: `def _m(x, E) -> float`
- **function `point`** [L352-366]: `def point(fam, q, E) -> dict` - Eligible-row point ratios of one model (DTEST; descriptive).
- **function `lic_values`** [L369-383]: `def lic_values(fam, outcome, pm) -> dict` - The bracket values of the §7 sentences: claim models, point values, declared bounds.
- **function `_unsealed`** [L386-393]: `def _unsealed(ctx, sealed, unseal) -> dict` - Point means of every opened VAL bundle (secondary, after every outcome).
- **function `_c2_outcome`** [L396-400]: `def _c2_outcome(ctx)`

