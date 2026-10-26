# `tools/x6_stage1/x6s1_stats.py`

- Source: [tools/x6_stage1/x6s1_stats.py](../../../../../tools/x6_stage1/x6s1_stats.py)
- Kind: python
- Lines: 202

## Module docstring

> X6S1 stats (overflow module 2): the empirical-Bernstein bound evaluated outward, certified log
> tables, the quantile wrapper, the registered bootstraps and TAIL (X6S1-FROZEN-v1 §7.3-§7.5, §10.2
> T14-T16; API.md §8). Import performs no I/O.

## Imports

### Internal (repo files)

- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 22, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 23, via same directory)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 6)
- `decimal` (lines 12)
- `fractions` (lines 13)
- `hashlib` (lines 8)
- `itertools` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 14)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime_registry`, `tools/d2a`, `tools/k4b`, `tools/x4_oracle_profile`, `tools/x6_stage0`, `tools/x6_stage1`

## Imported by

- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 24, import)
- [tests/x6_stage1/test_a_eval.py](../../tests/x6_stage1/test_a_eval.py.md) (line 27, import)
- [tests/x6_stage1/test_a_numerics.py](../../tests/x6_stage1/test_a_numerics.py.md) (line 25, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 25, import)
- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 24, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 30, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 28, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 35, import)
- [tools/x6zc/x6zc_core.py](../x6zc/x6zc_core.py.md) (line 32, import)
- [tools/x6zc/x6zc_run.py](../x6zc/x6zc_run.py.md) (line 504, import)

## Top-level constants

- `OUT`
- `REPO`
- `SLACK`
- `_EXTRA`

## Classes and functions

- **function `_dec`** [L32-34]: `def _dec(fr, ctx: Context) -> Decimal`
- **function `_eb_parts`** [L38-45]: `def _eb_parts(delta, n, B, ctx: Context, slack: Decimal) -> dict`
- **function `eb_constants`** [L48-49]: `def eb_constants(delta, n, B=17) -> dict`
- **function `_eb`** [L52-57]: `def _eb(xbar, zbar, n, delta, B, ctx: Context, slack: Decimal) -> Decimal`
- **function `eb_bound`** [L60-61]: `def eb_bound(xbar_plus, zbar_plus, n, delta, B=17) -> Decimal`
- **function `eb_reference`** [L64-65]: `def eb_reference(xbar, zbar, n, delta, B=17, prec=80) -> Decimal`
- **function `outward_inputs`** [L68-74]: `def outward_inputs(xhat, e_row=sd.E_ROW) -> tuple`
- **function `eb_report`** [L77-82]: `def eb_report(xhat, delta) -> dict`
- **function `qvals`** [L86-91]: `def qvals() -> tuple`
- **function `_value`** [L94-98]: `def _value(x: Fraction, kind, prec) -> Decimal`
- **function `table_entry`** [L101-103]: `def table_entry(x: Fraction, kind) -> dict`
- **function `_arg`** [L106-107]: `def _arg(k, Q, eps) -> Fraction`
- **function `log_tables`** [L110-127]: `def log_tables(Q=2 ** 20, eps=sd.EPS) -> dict`
- **function `decimal_kl`** [L130-136]: `def decimal_kl(q, pq, prec=80) -> Decimal`
- **function `quantile`** [L140-141]: `def quantile(x, level) -> float`
- **function `boot_means`** [L144-148]: `def boot_means(x, B, gen) -> np.ndarray`
- **function `boot_beta`** [L151-157]: `def boot_beta(num, den, B, gen) -> np.ndarray`
- **function `cord_draws`** [L160-168]: `def cord_draws(num, den, N, B, gen) -> tuple`
- **function `_compositions`** [L171-174]: `def _compositions(M, k)`
- **function `two_stage_law`** [L177-187]: `def two_stage_law(N, informative) -> dict`
- **function `tail`** [L190-197]: `def tail(num_obs, den_obs, mean, lb_perc, draws_mean) -> dict`
- **function `boot_stream`** [L200-202]: `def boot_stream(statistic_id, model=None) -> np.random.Generator`

