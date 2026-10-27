# `tools/x6zc/x6zc_census.py`

- Source: [tools/x6zc/x6zc_census.py](../../../../../tools/x6zc/x6zc_census.py)
- Kind: python
- Lines: 328

## Module docstring

> X6ZC census: the A-audit of the stored pairs, A4 exposure matching, the K4 comparison, the K5
> independent checks, B3, B4, B6, B7, B10, D2, D3 and the Stage-B descriptive tier (X6ZC-DESIGN-v1
> §6-§7; API.md §10, §20). Descriptive except where a check status is returned. No I/O.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 12, via same directory)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 16, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 17, via unique basename)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 18, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 19, via unique basename)

### External (third-party)

- `numpy` (lines 15)
- `torch` (lines 201)

### Standard library

- `__future__` (lines 6)
- `collections` (lines 9)
- `fractions` (lines 10)
- `math` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 20, import)
- [tests/x6zc/test_x6zc_decide.py](../../tests/x6zc/test_x6zc_decide.py.md) (line 17, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 19, import)
- [tools/x6zc/x6zc_dry.py](x6zc_dry.py.md) (line 19, import)
- [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 24, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 17, import)

## Top-level constants

- `K4_KEYS`
- `_FLAGS`
- `_LEVELS`

## Classes and functions

- **function `_st`** [L24-24]: `def _st(ok) -> str`
- **function `_ints`** [L25-25]: `def _ints(row) -> tuple`
- **function `_ts`** [L26-26]: `def _ts(t, n) -> np.ndarray`
- **function `_audit_row`** [L29-54]: `def _audit_row(ra, rb, t, y, family) -> str | None`
- **function `audit_pairs`** [L55-70]: `def audit_pairs(D_arrays, family, n_prefixes=zc.N_D) -> dict`
- **function `exposure_matches`** [L73-79]: `def exposure_matches(hist, t, pool_tokens) -> np.ndarray`
- **function `_prefix_set`** [L80-82]: `def _prefix_set(P, L) -> set`
- **function `exposure_report`** [L83-105]: `def exposure_report(variant_arrays_by_family, pools) -> dict` - Pool-major, then t: one row-prefix set of one pool is alive at a time; it is built once,
- **function `_rel`** [L108-112]: `def _rel(g, s) -> float`
- **function `k4_compare`** [L113-123]: `def k4_compare(stored, got) -> dict`
- **function `_fcn`** [L126-128]: `def _fcn(row) -> list`
- **function `k5_independent`** [L129-154]: `def k5_independent(terms, beta_prod, tok_a=None, tok_b=None) -> dict` - (a) members rebuilt from content (§20 E-3); exact q*, exact cue normalisation and sums.
- **function `k5_swap`** [L155-159]: `def k5_swap(terms) -> dict`
- **function `_maxdiff`** [L160-160]: `def _maxdiff(a, b) -> float`
- **function `k5_padding`** [L161-167]: `def k5_padding(pred, tok, t) -> dict`
- **function `k5_batch`** [L168-172]: `def k5_batch(pred, tok, t) -> dict`
- **function `k5_readout_index`** [L173-181]: `def k5_readout_index(pred, arrays, family) -> dict`
- **function `k5_two_loads`** [L182-184]: `def k5_two_loads(pred1, pred2, tok, t) -> dict`
- **function `k5_scalar_vector`** [L185-189]: `def k5_scalar_vector(pred, tok, t) -> dict`
- **function `_rows`** [L190-193]: `def _rows(terms, idx) -> dict`
- **function `k5_permutation`** [L194-199]: `def k5_permutation(terms, gen=None) -> dict`
- **function `k5_bos`** [L200-209]: `def k5_bos(model, tok, t) -> dict`
- **function `structural_subset`** [L210-214]: `def structural_subset(t, y) -> np.ndarray`
- **function `_q`** [L218-218]: `def _q(x, lv=_LEVELS) -> list`
- **function `_diffs`** [L219-221]: `def _diffs(terms) -> tuple`
- **function `decompose`** [L222-240]: `def decompose(terms) -> dict`
- **function `zc_profile`** [L241-252]: `def zc_profile(terms, tables, arm) -> dict`
- **function `crosses`** [L253-255]: `def crosses(x, y, bar=0.1, band=1e-09) -> bool`
- **function `_sens`** [L256-256]: `def _sens(b, alt) -> bool`
- **function `d2_decompose`** [L257-270]: `def d2_decompose(terms) -> dict`
- **function `_wbeta`** [L271-271]: `def _wbeta(num, den, w) -> float`
- **function `weighting_summaries`** [L272-297]: `def weighting_summaries(terms, prefixes, named_mask) -> dict`
- **function `similarity`** [L300-306]: `def similarity(dp) -> dict`
- **function `control_families`** [L307-315]: `def control_families(stats_by_family) -> dict` - {"terms": {family: pair_arrays output}, "designed": designed_stats dict} -> B7 values.
- **function `float32_replay`** [L316-318]: `def float32_replay(beta32, beta64) -> dict`
- **function `descriptive_tier`** [L321-328]: `def descriptive_tier(model, family, k4_tier, k1_ok, k5_ok, max_pair_diff, flags, betas) -> dict`

