# `tests/x6zc/test_x6zc_dryrun.py`

- Source: [tests/x6zc/test_x6zc_dryrun.py](../../../../../tests/x6zc/test_x6zc_dryrun.py)
- Kind: python
- Lines: 400

## Module docstring

> Author B, job 0120: the X6ZC synthetic dry run (PROTOCOL_X6ZC_v1 §12-§14; API.md §11, §15;
> TEST_PLAN.md §4), report schema, stage-1 no-write check, EXPOSURE/EVALUATIONS, ledger, pauses.
> Synthetic data only; planted predictors are described at class Planted.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](../../tools/x6zc/x6zc_core.py.md) (line 18, via sys.path edit)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](../../tools/x6zc/x6zc_census.py.md) (line 19, via sys.path edit)
- `import x6zc_run` -> [tools/x6zc/x6zc_run.py](../../tools/x6zc/x6zc_run.py.md) (line 20, via sys.path edit)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../../tools/x6_stage0/x6_exact.py.md) (line 21, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 22, via unique basename)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 23, via unique basename)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 24, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../../tools/x6_stage1/x6s1_pairs.py.md) (line 25, via unique basename)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 26, via unique basename)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 312, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)
- `torch` (lines 311)

### Standard library

- `__future__` (lines 4)
- `copy` (lines 5)
- `fractions` (lines 12)
- `hashlib` (lines 6)
- `json` (lines 7)
- `math` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 13)
- `re` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'x6zc')` -> `tools/x6zc`

## Imported by

- none

## Top-level constants

- `CC`
- `FIX`
- `KAPPA`
- `PATHS`
- `REPO`
- `UTC`

## Classes and functions

- **function `_pool`** [L41-48]: `def _pool(seed, rows=4096)`
- **function `_yield_rows`** [L49-55]: `def _yield_rows(pool)`
- **function `_jit`** [L56-61]: `def _jit(prefixes, seed)`
- **function `_info`** [L62-64]: `def _info(row, t)`
- **function `_ts`** [L65-67]: `def _ts(tokens, t)`
- **function `_rows`** [L68-73]: `def _rows(pred, tok, ts, memo)`
- **class `Fn`** [L74-78]
- **method `Fn.__init__`** [L75-76]: `def __init__(self, name, fn)`
- **method `Fn.__call__`** [L77-78]: `def __call__(self, tokens, t)`
- **class `Planted`** [L79-93] - p = Z + sum_k f_k(prefix)(P_k - Z), Z = q*_ZC, P_k a SyntheticPredictor; equal cue masses
- **method `Planted.__init__`** [L82-83]: `def __init__(self, name, comps)`
- **method `Planted.__call__`** [L84-93]: `def __call__(self, tokens, t)`
- **function `_partner`** [L94-101]: `def _partner(tok, ts)`
- **function `_nudge`** [L102-105]: `def _nudge(tok, ts)`
- **function `_pl`** [L106-108]: `def _pl(W, model, *comps)`
- **function `_stats`** [L133-142]: `def _stats(key, w, planted, seed=20261026)`
- **function `_st`** [L143-144]: `def _st(W, fid)`
- **function `_ev`** [L145-152]: `def _ev(**kw)`
- **function `_out`** [L153-154]: `def _out(rep, cell='P')`
- **function `_lic`** [L155-156]: `def _lic(rep, cell='P')`
- **function `_world`** [L157-160]: `def _world(fresh)`
- **function `W`** [L162-169]: `def W()` decorators: @pytest.fixture(scope='module')
- **test `test_planted_fixture_outcomes`** [L171-180]: `def test_planted_fixture_outcomes(W, fid)` decorators: @pytest.mark.parametrize('fid', sorted(FIX))
- **test `test_planted_fixture_details`** [L181-208]: `def test_planted_fixture_details(W)`
- **test `test_dr09_unstable_ratio`** [L209-225]: `def test_dr09_unstable_ratio()`
- **test `test_dr11_dr12_sizing`** [L226-246]: `def test_dr11_dr12_sizing(W)`
- **test `test_dr13_14_15_global`** [L247-271]: `def test_dr13_14_15_global(W)`
- **test `test_dr16_dr17_mixtures_and_swaps`** [L272-289]: `def test_dr16_dr17_mixtures_and_swaps(W)`
- **test `test_dr18_dr19_rejections`** [L290-309]: `def test_dr18_dr19_rejections(W)`
- **test `test_dr22_random_init_models`** [L310-335]: `def test_dr22_random_init_models(W, tmp_path)`
- **test `test_store_records`** [L336-379]: `def test_store_records(tmp_path)`
- **test `test_report_schema_from_pipeline`** [L380-400]: `def test_report_schema_from_pipeline(W)`

