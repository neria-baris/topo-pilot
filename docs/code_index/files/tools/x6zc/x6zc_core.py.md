# `tools/x6zc/x6zc_core.py`

- Source: [tools/x6zc/x6zc_core.py](../../../../../tools/x6zc/x6zc_core.py)
- Kind: python
- Lines: 574

## Module docstring

> X6ZC core: constants and bindings, fresh prefixes and loop-sign variants, exact geometry (K0)
> and the q*_NA cache, synthetic predictors, pair terms and K1-K3/F1, the paired cluster bootstrap,
> ratio intervals, B9 sizing, the §9 decision, qualifiers, licences and the reuse verdict
> (X6ZC-DESIGN-v1; API.md §3-§9, §20). Import reads CONTRACT.json and the protocol bytes only.

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 24, via sys.path edit)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 28, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 29, via unique basename)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 30, via sys.path edit)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 31, via sys.path edit)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../x6_stage1/x6s1_stats.py.md) (line 32, via sys.path edit)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)

### External (third-party)

- `numpy` (lines 27)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 14)
- `fractions` (lines 15)
- `functools` (lines 16)
- `hashlib` (lines 9)
- `io` (lines 10)
- `json` (lines 11)
- `math` (lines 12)
- `pathlib` (lines 17)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(_p)` -> `tools/x6_stage1`, `tools/x6zc`

## Imported by

- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 19, import)
- [tests/x6zc/test_x6zc_decide.py](../../tests/x6zc/test_x6zc_decide.py.md) (line 16, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 18, import)
- [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 12, import)
- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 23, import)

## Top-level constants

- `ANSWERS`
- `CELLS`
- `CONTRACT`
- `HERE`
- `REPO`
- `T`
- `VARIANTS`
- `W1_CROSS_STEPS`
- `_K2`
- `_MISS`
- `_MK`

## Classes and functions

- **function `load_contract`** [L38-42]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `frac`** [L43-43]: `def frac(s) -> Fraction`
- **function `stream`** [L71-72]: `def stream(name) -> np.random.Generator`
- **function `dry_stream`** [L73-74]: `def dry_stream(*names) -> np.random.Generator`
- **function `_fl`** [L75-75]: `def _fl(x) -> float`
- **function `_ints`** [L76-76]: `def _ints(row) -> tuple`
- **function `prefix_yields`** [L79-85]: `def prefix_yields(prefix_tokens, rnd_len) -> list`
- **function `fresh_prefixes`** [L86-97]: `def fresh_prefixes(prefix_tokens, d_prefixes) -> dict`
- **function `variant_path`** [L98-101]: `def variant_path(family, variant, member) -> tuple`
- **function `variant_history`** [L102-104]: `def variant_history(family, variant, member, prefix, y) -> tuple`
- **function `variant_arrays`** [L105-112]: `def variant_arrays(prefixes, family) -> dict`
- **function `d_cluster`** [L113-113]: `def d_cluster(n_rows) -> np.ndarray`
- **function `_qx`** [L117-117]: `def _qx(arm, h) -> tuple` decorators: @lru_cache(maxsize=None)
- **function `qx`** [L118-121]: `def qx(arm, history) -> tuple`
- **function `crossings`** [L122-125]: `def crossings(path) -> list`
- **function `holonomy_missing`** [L126-133]: `def holonomy_missing(arm, segment, skip) -> tuple`
- **function `missed_law`** [L134-138]: `def missed_law(history, which) -> tuple`
- **function `answer_names`** [L139-143]: `def answer_names(history) -> dict`
- **function `_cn`** [L144-144]: `def _cn(q) -> tuple`
- **function `_dna`** [L145-145]: `def _dna(lam, y) -> list`
- **function `_w1_stats`** [L146-149]: `def _w1_stats(h, p) -> tuple`
- **function `_k0_pair`** [L150-179]: `def _k0_pair(ha, hb, family, v, lam)`
- **function `oracle_geometry`** [L180-200]: `def oracle_geometry(arrays, family, keys=VARIANT_ORDER) -> dict`
- **function `_cos`** [L201-204]: `def _cos(u, d) -> tuple`
- **function `coupling_table`** [L205-218]: `def coupling_table() -> dict`
- **class `QStarCache`** [L219-259] - q*_NA rows computed once per distinct (w_{1:t}, t); bitwise equal to se.qstar("NA").
- **method `QStarCache.__init__`** [L221-221]: `def __init__(self, table)`
- **method `QStarCache.key`** [L223-225]: `def key(row, t) -> str` decorators: @staticmethod
- **method `QStarCache.build`** [L227-237]: `def build(cls, array_dicts) -> QStarCache` decorators: @classmethod
- **method `QStarCache.__call__`** [L238-244]: `def __call__(self, tokens, t) -> tuple`
- **method `QStarCache.save`** [L245-252]: `def save(self, path) -> str`
- **method `QStarCache.load`** [L254-259]: `def load(cls, path, sha256) -> QStarCache` decorators: @classmethod
- **function `member_of`** [L262-267]: `def member_of(history) -> str`
- **function `_mix`** [L268-268]: `def _mix(*terms) -> tuple`
- **class `SyntheticPredictor`** [L270-308]
- **method `SyntheticPredictor.__init__`** [L271-273]: `def __init__(self, kind, **params)`
- **method `SyntheticPredictor.exact`** [L274-303]: `def exact(self, history) -> tuple`
- **method `SyntheticPredictor.__call__`** [L304-308]: `def __call__(self, tokens, t) -> np.ndarray`
- **function `oracle`** [L309-309]: `def oracle(arm, kind) -> se.OraclePredictor`
- **function `sym_arrays`** [L310-312]: `def sym_arrays(p_a, p_b) -> tuple`
- **function `pair_arrays`** [L315-325]: `def pair_arrays(pred, arrays, key, qstar_fn) -> dict`
- **function `pair_stats`** [L326-335]: `def pair_stats(terms) -> dict`
- **function `k1_check`** [L336-341]: `def k1_check(terms) -> dict`
- **function `k2_check`** [L344-353]: `def k2_check(terms_by_ref, family) -> dict`
- **function `beta_exact_pi0`** [L354-361]: `def beta_exact_pi0(law_fn, family, variant, ys=(0, 1, 2)) -> Fraction`
- **function `k2_exact_variants`** [L362-366]: `def k2_exact_variants(family) -> dict`
- **function `k3_grid`** [L367-373]: `def k3_grid() -> list`
- **function `k3_exact`** [L374-382]: `def k3_exact(family) -> dict`
- **function `k3_float_check`** [L383-392]: `def k3_float_check(family, arrays, qstar_fn) -> dict`
- **function `f1`** [L393-402]: `def f1(k3) -> dict`
- **function `cluster_sums`** [L405-409]: `def cluster_sums(values, cluster, P) -> np.ndarray`
- **function `paired_cluster_boot`** [L410-419]: `def paired_cluster_boot(num, den, B, gen) -> dict`
- **function `interval`** [L420-424]: `def interval(draws, q) -> tuple`
- **function `ratio_interval`** [L425-431]: `def ratio_interval(draws_v, draws_pp, sign, q) -> dict`
- **function `_ratio`** [L432-432]: `def _ratio(a, b)`
- **function `cell_statistics`** [L433-453]: `def cell_statistics(point, draws, cell) -> dict`
- **function `halfwidth`** [L454-456]: `def halfwidth(n, se_d, beta_d, z) -> float`
- **function `choose_n`** [L457-471]: `def choose_n(n_avail, se) -> dict`
- **function `_ascii`** [L474-474]: `def _ascii(rule) -> str`
- **function `_lt`** [L475-475]: `def _lt(x, bar) -> bool`
- **function `_gt`** [L476-476]: `def _gt(x, bar) -> bool`
- **function `_unstable`** [L477-480]: `def _unstable(s) -> bool`
- **function `_cell_rule`** [L481-499]: `def _cell_rule(ev, c) -> tuple`
- **function `decide_x6zc`** [L500-526]: `def decide_x6zc(ev) -> dict`
- **function `_lkey`** [L527-530]: `def _lkey(outcome, table, case=None) -> str`
- **function `licence`** [L531-537]: `def licence(outcome, values, case=None) -> str`
- **function `not_licensed`** [L538-539]: `def not_licensed(outcome, case=None) -> str`
- **function `qualifiers`** [L540-557]: `def qualifiers(ev, decision, census) -> dict`
- **function `reuse_verdict`** [L558-574]: `def reuse_verdict(ev, decision) -> dict`

