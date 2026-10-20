# `tools/x6_stage0/x6_dp.py`

- Source: [tools/x6_stage0/x6_dp.py](../../../../../tools/x6_stage0/x6_dp.py)
- Kind: python
- Lines: 397

## Module docstring

> X6 stage 0: integer segment DP, Decimal enclosures, natural quantities, K-blk, gate G4
> (X6-FROZEN-v1 sections 5-6.2; API.md 4). Counts are Python ints; logs are certified enclosures.

## Imports

### Internal (repo files)

- `from x6_model import ANCHOR, ANCHOR_NB, ARMS_SEAM, G_MIN, LADDER, NEIGHBOURS, S3_A, S3_B, S3_E, THETA_ROW, WINDOWS, compose, edge_labels, lam, model, perm_name, point_law, seam_letter, statistic` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 11, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `collections` (lines 7)
- `decimal` (lines 8)
- `fractions` (lines 9)
- `itertools` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage0/test_x6_stage0_dp.py](../../tests/x6_stage0/test_x6_stage0_dp.py.md) (line 25, import)
- [tools/x6_stage0/x6_exact.py](x6_exact.py.md) (line 11, import)
- [tools/x6_stage0/x6_run.py](x6_run.py.md) (line 19, import)
- [tools/x6_stage0/x6_store.py](x6_store.py.md) (line 21, import)
- [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 274, import)
- [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 287, import)
- [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 22, import)
- [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 25, import)

## Top-level constants

- `C200`
- `CTX`
- `G4_CHECKS`
- `MEMO`
- `_LADDER_PAIRS`
- `_LETTERS`
- `_LN`
- `_PYTH`

## Classes and functions

- **function `segment_dp`** [L18-34]: `def segment_dp(arm: str, n_max: int = 31)` - Yield (n, {(v, kappa, g): count}) for n = 0..n_max (anchor-avoiding paths from ANCHOR).
- **function `classes`** [L36-41]: `def classes(layer: dict, S: str) -> dict`
- **function `_image_counts`** [L42-46]: `def _image_counts(cls: dict, y: int) -> list`
- **function `weights`** [L47-49]: `def weights(cls: dict, y: int) -> tuple`
- **function `ambiguous`** [L50-51]: `def ambiguous(cls: dict, y: int) -> bool`
- **function `avoid_counts`** [L52-66]: `def avoid_counts(n_max: int = 31) -> dict`
- **function `total_mass`** [L68-70]: `def total_mass(t: int, counts: dict) -> Fraction`
- **function `to_decimal`** [L80-82]: `def to_decimal(fr, prec: int) -> Decimal`
- **function `kl_decimal`** [L83-92]: `def kl_decimal(p, q, prec: int) -> Decimal`
- **function `entropy_decimal`** [L94-99]: `def entropy_decimal(p, prec: int) -> Decimal`
- **function `memo_key`** [L100-101]: `def memo_key(prec, kind, n, w, z) -> tuple`
- **function `_mix`** [L102-104]: `def _mix(m: int, w) -> list`
- **function `kl_term_uncached`** [L105-109]: `def kl_term_uncached(prec, kind, n, w, z) -> Decimal`
- **function `kl_term`** [L110-114]: `def kl_term(prec, kind, n, w, z) -> Decimal`
- **function `memo_clear`** [L115-118]: `def memo_clear() -> None`
- **function `_pyth_kl`** [L119-123]: `def _pyth_kl(prec, n, w_fine, w_coarse) -> Decimal`
- **function `decimal_model`** [L124-127]: `def decimal_model(arm: str, prec: int) -> tuple`
- **function `enclosure`** [L130-134]: `def enclosure(v80, v120, abs_sum, n_terms) -> dict`
- **function `enclose_sum`** [L135-140]: `def enclose_sum(pairs) -> dict`
- **function `certify`** [L141-144]: `def certify(enc: dict, theta) -> str`
- **function `mass_bounds`** [L145-150]: `def mass_bounds(rows, theta) -> tuple`
- **function `certify_mass`** [L151-153]: `def certify_mass(m_lower, m_upper, threshold) -> str`
- **function `_rec`** [L156-157]: `def _rec() -> dict`
- **function `_add`** [L158-161]: `def _add(rec: dict, mult: int, vals: dict) -> None`
- **function `_scale`** [L162-164]: `def _scale(rec: dict, coef) -> dict`
- **function `_enc`** [L165-173]: `def _enc(recs, signs=None) -> dict`
- **function `_both`** [L175-176]: `def _both(fn, *args) -> dict`
- **function `_mass`** [L177-178]: `def _mass(cnt: list, t: int) -> Fraction`
- **function `_row_enc`** [L179-181]: `def _row_enc(vals: dict) -> dict`
- **function `natural`** [L184-286]: `def natural(arm: str, t_max: int = 32) -> dict`
- **function `kblk`** [L289-329]: `def kblk(arm: str) -> dict`
- **function `_encs`** [L337-343]: `def _encs(obj)`
- **function `_ge`** [L344-345]: `def _ge(a: dict, b: dict) -> bool`
- **function `_g4_checks`** [L346-374]: `def _g4_checks(nat: dict, kb: dict, arms) -> dict`
- **function `gate_G4`** [L376-397]: `def gate_G4(arms=ARMS_SEAM) -> dict`

