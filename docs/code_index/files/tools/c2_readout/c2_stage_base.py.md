# `tools/c2_readout/c2_stage_base.py`

- Source: [tools/c2_readout/c2_stage_base.py](../../../../../tools/c2_readout/c2_stage_base.py)
- Kind: python
- Lines: 357

## Module docstring

> C2 stage helpers shared by every PLAN (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5, §6.6, §7,
> §8): the stage-entry bodies (rows 0b, 1), the store loaders and ctx caches, the gate history (the
> §7 scope rule), the per-model split state, and the split-level checks that later stages and T-PRE
> reuse (sampling with the Y-donor preparation, the ORACLE writer, H5, L1, R1, N2, support, X1, the
> closed-form streams, the bound wrapper). No PLAN here; nothing runs at import.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 13, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 16, via unique basename)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](../c1prime/c1_gates.py.md) (line 17, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 18, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 19, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 20, via same directory)
- `import c2_code` -> [tools/c2_readout/c2_code.py](c2_code.py.md) (line 21, via same directory)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 22, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](c2_decide.py.md) (line 23, via same directory)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](c2_driver.py.md) (line 24, via same directory)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 25, via same directory)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 26, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](c2_registry.py.md) (line 27, via same directory)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](c2_stats.py.md) (line 28, via same directory)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 29, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 31, via unique basename)

### External (third-party)

- `numpy` (lines 30)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 10)
- `json` (lines 9)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 21, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 25, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 25, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 29, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 23, import)

## Top-level constants

- `ENTRY`
- `FAM`
- `KP`

## Classes and functions

- **function `_abs`** [L41-44]: `def _abs(ctx, rel) -> Path`
- **function `put`** [L47-48]: `def put(ctx, rel, **arrays) -> None`
- **function `putj`** [L51-52]: `def putj(ctx, rel, obj) -> None`
- **function `cache`** [L55-58]: `def cache(ctx, key, fn)`
- **function `npz`** [L61-66]: `def npz(ctx, rel) -> dict`
- **function `js`** [L69-70]: `def js(ctx, rel) -> dict`
- **function `proc`** [L73-74]: `def proc(ctx) -> dict`
- **function `models`** [L77-78]: `def models(ctx) -> dict`
- **function `table`** [L81-89]: `def table(ctx, split) -> dict`
- **function `orc`** [L92-93]: `def orc(ctx, split) -> dict`
- **function `fitb`** [L96-97]: `def fitb(ctx, j) -> dict`
- **function `gates`** [L100-101]: `def gates(ctx) -> list`
- **function `prior`** [L104-110]: `def prior(ctx, j, fam)` - The first exclusion, CNHS or stop applying to (j, fam) (§7 scope; variants never).
- **function `alive`** [L113-114]: `def alive(ctx, j, fam) -> bool`
- **function `fstop`** [L117-119]: `def fstop(ctx, fam)`
- **function `family_stop`** [L122-129]: `def family_stop(ctx, fam)` - None while >= 2 models remain, else the §6.5 rule-2 outcome (CNHS names if >= 2 CNHS).
- **function `rec`** [L132-133]: `def rec(status, values=None, **who) -> dict`
- **function `lines`** [L136-138]: `def lines(recs) -> dict`
- **function `per`** [L141-145]: `def per(ctx, fams, fn) -> dict` - One line per alive (model, family); fn(j, fam) -> (status, values).
- **function `frac`** [L148-149]: `def frac(mask) -> Fraction`
- **function `auth_admit`** [L153-155]: `def auth_admit(ctx) -> dict`
- **function `g0_step`** [L158-160]: `def g0_step(ctx) -> dict`
- **function `inputs`** [L167-168]: `def inputs(ctx, j, H) -> np.ndarray`
- **function `charts`** [L171-176]: `def charts(ctx, j) -> tuple`
- **function `_state`** [L179-192]: `def _state(ctx, j, H, rows, n, kind) -> tuple` - (inputs, hooks, natural logits) of one role on `rows`; elsewhere inputs -1 (never
- **function `bundle`** [L195-213]: `def bundle(ctx, split, j, kind=None, roles=cc.ROLES) -> dict` - Per role: inputs, the three hooks, y, and for H, H+, H- the chart phase and support;
- **function `prob`** [L216-223]: `def prob(ctx, j, p, need_alive=True) -> dict` - The frozen FIT projector problem p of model j ({"ok": False} unless F1 PASS and alive).
- **function `w32`** [L226-227]: `def w32(ctx, split) -> np.ndarray`
- **function `zt`** [L230-232]: `def zt(ctx, split, j) -> np.ndarray`
- **function `Yf`** [L235-236]: `def Yf(fam, X, r) -> np.ndarray`
- **function `target`** [L239-240]: `def target(fam, phi, m32) -> np.ndarray`
- **function `afull`** [L243-248]: `def afull(ctx, split, j, pair) -> tuple` - (d named, dy, A_full) of the natural x or y pair (closed form; y pair NaN off Y_def).
- **function `decs`** [L252-254]: `def decs(ctx, j, fam) -> dict`
- **function `l1_check`** [L257-262]: `def l1_check(ctx, split, j, fam) -> tuple`
- **function `r1_check`** [L265-279]: `def r1_check(ctx, split, j, fam) -> tuple` - R1 with the zero overrides; the tally (ZERO_CODE, R1 counts) and, for R, the C1 chart-phase
- **function `n2_check`** [L282-296]: `def n2_check(ctx, split, j) -> tuple`
- **function `support`** [L299-303]: `def support(ctx, split, j) -> dict` - UNSUPPORTED_H/PLUS/MINUS counts (§5.5; rows kept and phased) and Sup(H).
- **function `h5_bounds`** [L306-314]: `def h5_bounds(ob, seed) -> dict`
- **function `sample`** [L317-343]: `def sample(ctx, blocks, version) -> dict` - H2 / H2': sample the splits; the Y-donor preparation (the natural-history oracle for b31(H)
- **function `save_oracle`** [L346-351]: `def save_oracle(ctx, split, o, el) -> None`
- **function `reg_files`** [L354-357]: `def reg_files(ctx, version) -> None`

