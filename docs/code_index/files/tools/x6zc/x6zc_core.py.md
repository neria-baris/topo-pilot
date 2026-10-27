# `tools/x6zc/x6zc_core.py`

- Source: [tools/x6zc/x6zc_core.py](../../../../../tools/x6zc/x6zc_core.py)
- Kind: python
- Lines: 375

## Module docstring

> X6ZC core: fresh prefixes and loop-sign variants, exact geometry (K0) and the q*_NA cache,
> synthetic predictors, pair terms and K1-K3/F1 (X6ZC-DESIGN-v1; API.md §4-§7, §20 C-52). It
> re-exports x6zc_const (constants, bindings) and x6zc_decide (bootstrap, B9, decision), so
> every API name stays reachable as zc.<name>. Import reads CONTRACT.json and the protocol only.

## Imports

### Internal (repo files)

- `from x6zc_const import HERE, REPO, CONTRACT_PATH, PROTOCOL_FILE, load_contract, frac, CONTRACT, KC, _PA, _X, PROTOCOL_ID, PROTOCOL_SHA256, PROJECT_ROOT, X6S1_STORE, STORE, WORKTREE, SCRATCH_ROOT, DRY_STORE, METER_IMPORT_DIR, NA_DIR, H3, MERGE_COMMIT, CLOSURE, X6ZC_MASTER, FAMILIES, VARIANT_ORDER, VARIANT_SIGN, W1_TAIL, VARIANTS, W1_CROSS_STEPS, READOUT_OFFSET, LAMBDA_INDEX, ANSWERS, CELLS, CELL_ORDER, _PR, MODELS, INITS, STAGE_B_ORDER, FOCAL, K5_MODELS, NA_MODELS, K6_CONTROLS, K6_MIN, T, B_DRAWS, N_FLOOR, N_D, N_LADDER, _S3N, _MISS, stream, dry_stream, _fl, _ints` -> [tools/x6zc/x6zc_const.py](x6zc_const.py.md) (line 21, via same directory)
- `from x6zc_decide import cluster_sums, paired_cluster_boot, interval, ratio_interval, _ratio, cell_statistics, halfwidth, choose_n, _ascii, _lt, _gt, _unstable, _cell_rule, decide_x6zc, _lkey, licence, not_licensed, qualifiers, reuse_verdict` -> [tools/x6zc/x6zc_decide.py](x6zc_decide.py.md) (line 32, via same directory)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 40, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 41, via unique basename)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 42, via unique basename)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 43, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 44, via unique basename)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 46, via package root)

### External (third-party)

- `numpy` (lines 39)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 13)
- `fractions` (lines 14)
- `functools` (lines 15)
- `hashlib` (lines 9)
- `io` (lines 10)
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

- line 19: `str(Path(__file__).resolve().parent)` -> `tools/x6zc`

## Imported by

- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 19, import)
- [tests/x6zc/test_x6zc_decide.py](../../tests/x6zc/test_x6zc_decide.py.md) (line 16, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 18, import)
- [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 12, import)
- [tools/x6zc/x6zc_dry.py](x6zc_dry.py.md) (line 13, import)
- [tools/x6zc/x6zc_guard.py](x6zc_guard.py.md) (line 18, import)
- [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 10, import)
- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 14, import)
- [tools/x6zc/x6zc_stage_a.py](x6zc_stage_a.py.md) (line 18, import)
- [tools/x6zc/x6zc_stage_bc.py](x6zc_stage_bc.py.md) (line 11, import)
- [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 18, import)

## Top-level constants

- `_K2`
- `_MK`

## Classes and functions

- **function `prefix_yields`** [L50-56]: `def prefix_yields(prefix_tokens, rnd_len) -> list`
- **function `fresh_prefixes`** [L57-68]: `def fresh_prefixes(prefix_tokens, d_prefixes) -> dict`
- **function `variant_path`** [L69-72]: `def variant_path(family, variant, member) -> tuple`
- **function `variant_history`** [L73-75]: `def variant_history(family, variant, member, prefix, y) -> tuple`
- **function `variant_arrays`** [L76-83]: `def variant_arrays(prefixes, family) -> dict`
- **function `d_cluster`** [L84-84]: `def d_cluster(n_rows) -> np.ndarray`
- **function `_qx`** [L88-88]: `def _qx(arm, h) -> tuple` decorators: @lru_cache(maxsize=None)
- **function `qx`** [L89-92]: `def qx(arm, history) -> tuple`
- **function `crossings`** [L93-96]: `def crossings(path) -> list`
- **function `holonomy_missing`** [L97-104]: `def holonomy_missing(arm, segment, skip) -> tuple`
- **function `missed_law`** [L105-109]: `def missed_law(history, which) -> tuple`
- **function `answer_names`** [L110-114]: `def answer_names(history) -> dict`
- **function `_cn`** [L115-115]: `def _cn(q) -> tuple`
- **function `_dna`** [L116-116]: `def _dna(lam, y) -> list`
- **function `_w1_stats`** [L117-120]: `def _w1_stats(h, p) -> tuple`
- **function `_k0_pair`** [L121-151]: `def _k0_pair(ha, hb, family, v, lam, out=None)`
- **function `oracle_geometry`** [L152-173]: `def oracle_geometry(arrays, family, keys=VARIANT_ORDER) -> dict`
- **function `_cos`** [L174-177]: `def _cos(u, d) -> tuple`
- **function `coupling_table`** [L178-191]: `def coupling_table() -> dict`
- **class `QStarCache`** [L192-232] - q*_NA rows computed once per distinct (w_{1:t}, t); bitwise equal to se.qstar("NA").
- **method `QStarCache.__init__`** [L194-194]: `def __init__(self, table)`
- **method `QStarCache.key`** [L196-198]: `def key(row, t) -> str` decorators: @staticmethod
- **method `QStarCache.build`** [L200-210]: `def build(cls, array_dicts) -> QStarCache` decorators: @classmethod
- **method `QStarCache.__call__`** [L211-217]: `def __call__(self, tokens, t) -> tuple`
- **method `QStarCache.save`** [L218-225]: `def save(self, path) -> str`
- **method `QStarCache.load`** [L227-232]: `def load(cls, path, sha256) -> QStarCache` decorators: @classmethod
- **function `member_of`** [L235-240]: `def member_of(history) -> str`
- **function `_mix`** [L241-241]: `def _mix(*terms) -> tuple`
- **class `SyntheticPredictor`** [L243-281]
- **method `SyntheticPredictor.__init__`** [L244-246]: `def __init__(self, kind, **params)`
- **method `SyntheticPredictor.exact`** [L247-276]: `def exact(self, history) -> tuple`
- **method `SyntheticPredictor.__call__`** [L277-281]: `def __call__(self, tokens, t) -> np.ndarray`
- **function `oracle`** [L282-282]: `def oracle(arm, kind) -> se.OraclePredictor`
- **function `sym_arrays`** [L283-285]: `def sym_arrays(p_a, p_b) -> tuple`
- **function `pair_arrays`** [L288-298]: `def pair_arrays(pred, arrays, key, qstar_fn) -> dict`
- **function `pair_stats`** [L299-308]: `def pair_stats(terms) -> dict`
- **function `k1_check`** [L309-314]: `def k1_check(terms) -> dict`
- **function `k2_check`** [L317-326]: `def k2_check(terms_by_ref, family) -> dict`
- **function `beta_exact_pi0`** [L327-334]: `def beta_exact_pi0(law_fn, family, variant, ys=(0, 1, 2)) -> Fraction`
- **function `k2_exact_variants`** [L335-339]: `def k2_exact_variants(family) -> dict`
- **function `k3_grid`** [L340-346]: `def k3_grid() -> list`
- **function `k3_exact`** [L347-355]: `def k3_exact(family) -> dict`
- **function `k3_float_check`** [L356-365]: `def k3_float_check(family, arrays, qstar_fn) -> dict`
- **function `f1`** [L366-375]: `def f1(k3) -> dict`

