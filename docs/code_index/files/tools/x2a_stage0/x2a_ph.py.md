# `tools/x2a_stage0/x2a_ph.py`

- Source: [tools/x2a_stage0/x2a_ph.py](../../../../../tools/x2a_stage0/x2a_ph.py)
- Kind: python
- Lines: 395

## Module docstring

> X2a stage 0, part 3 (X2A-FROZEN-v1; API.md): PH route (K1 band, K2 C-world, K3 H0 height),
> clouds and readings, PH controls, noise floor, outcome logic, S0 and run (report and NPZ).

## Imports

### Internal (repo files)

- `import x2a_mc` -> [tools/x2a_stage0/x2a_mc.py](x2a_mc.py.md) (line 16, via same directory)
- `import x2a_model` -> [tools/x2a_stage0/x2a_model.py](x2a_model.py.md) (line 17, via same directory)
- `from topo_pilot.contracts import SeedTree, Status` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.topology import DistancePipeline, Euclidean, Hellinger, NullClouds, PersistenceComputer, PHConfig, Summaries` -> [src/topo_pilot/topology/__init__.py](../../src/topo_pilot/topology/__init__.py.md) (line 22, via package root)

### External (third-party)

- `numpy` (lines 12)
- `scipy` (lines 18, 19)

### Standard library

- `__future__` (lines 4)
- `hashlib` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 8)
- `time` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 14: `[p for p in (str(Path(__file__).resolve().parent),) if p not in sys.path]` -> `tools/x2a_stage0`

## Imported by

- [tests/x2a_stage0/test_x2a_stage0.py](../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 38, import)
- [tests/x2a_stage0/test_x2a_stage0_ph.py](../../tests/x2a_stage0/test_x2a_stage0_ph.py.md) (line 30, import)

## Top-level constants

- `BOUND`
- `GATES`
- `PLANNING`
- `_PH`

## Classes and functions

- **function `_bars`** [L39-41]: `def _bars(rows, dim)`
- **function `betti_at`** [L43-45]: `def betti_at(rows, dim, r)`
- **function `_segments`** [L47-51]: `def _segments(rows, lo, hi)`
- **function `_merge`** [L53-60]: `def _merge(S)`
- **function `band_select`** [L62-73]: `def band_select(diagrams, lo=0.0, hi=0.99, min_width=0.08)`
- **function `beta1_band`** [L75-77]: `def beta1_band(rows, band)`
- **function `k2_check`** [L79-82]: `def k2_check(rows)`
- **function `clusters_at`** [L84-100]: `def clusters_at(D, h, dedup_map, min_size=MIN_SIZE)`
- **function `split_check`** [L102-113]: `def split_check(labels, truth, purity=0.95)`
- **function `_h0_deaths`** [L115-117]: `def _h0_deaths(rows)`
- **function `h0_star`** [L119-125]: `def h0_star(xhalf_rows, x1_rows)`
- **function `q1_outcome`** [L128-133]: `def q1_outcome(n_a, n_b, n_pref, invalid=False)`
- **function `q2_outcome`** [L135-142]: `def q2_outcome(n_full_split, n_win_connected, n_win_split, invalid=False)`
- **function `validity`** [L144-149]: `def validity(statuses)`
- **function `released`** [L151-154]: `def released(verdict, first_failed, labels)`
- **function `_ph`** [L159-165]: `def _ph(X, maxdim, metric=None)`
- **function `_cond`** [L167-169]: `def _cond(b, c)`
- **function `_g0`** [L171-173]: `def _g0(rows)`
- **function `_item`** [L175-180]: `def _item(fn, store, key)`
- **function `ph_route`** [L182-225]: `def ph_route(spec, models, keepA, keepB, pref_B, ctl_b32, tree, H_t, diags)`
- **function `_q2`** [L227-282]: `def _q2(kA, kB, ctl, P, diags, H_t)`
- **function `_ctl`** [L284-285]: `def _ctl(pair, p)`
- **function `s0_check`** [L288-296]: `def s0_check()`
- **function `_stages`** [L298-313]: `def _stages(st, rep, data, tree)`
- **function `run`** [L315-390]: `def run(out_dir, preflight)`

