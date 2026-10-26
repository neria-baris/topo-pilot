# `tools/c2_nd/nd_stage_base.py`

- Source: [tools/c2_nd/nd_stage_base.py](../../../../../tools/c2_nd/nd_stage_base.py)
- Kind: python
- Lines: 383

## Module docstring

> C2ND shared stage plumbing (the extra module of job 0125, ND-C43; C2 c2_stage_base pattern,
> ND-C6): store loaders and caches with the read-only C2 store, lineage records, the gate history
> (the §3 scope rule), per-model split state (inputs, hooks, readout coordinates, phases) and the
> split-level checks reused by S3 and T-PRE (L1, R1, N2, support, H5). It never imports nd_driver
> or a stage module; nd_dry is imported lazily in a dry-run store only. Nothing runs at import.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 16, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 19, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 20, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 21, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 22, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 23, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 24, via unique basename)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 25, via unique basename)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 26, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via unique basename)

### External (third-party)

- `numpy` (lines 27)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 12)
- `functools` (lines 13)
- `importlib` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 280: `nd_dry` -> [tools/c2_nd/nd_dry.py](nd_dry.py.md)

### sys.path additions

- none

## Imported by

- [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 25, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 31, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 28, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 32, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 28, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 32, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 27, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 42, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 21, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 25, import)

## Top-level constants

- `COORD`
- `PROB_KEYS`
- `SCHEMA`
- `SRC`

## Classes and functions

- **function `_jr`** [L41-45]: `def _jr(path)`
- **function `_eq`** [L48-49]: `def _eq(a, b) -> bool`
- **function `_sha_ok`** [L52-53]: `def _sha_ok(path, want) -> bool`
- **function `_js`** [L56-68]: `def _js(v)`
- **function `_npz`** [L71-73]: `def _npz(path) -> dict`
- **function `cache`** [L76-79]: `def cache(ctx, key, fn)`
- **function `c2_store`** [L82-88]: `def c2_store(ctx) -> tuple` - (root, {rel: sha256}): the C2 store and its CONTRACT table, or in a dry-run store its c2/
- **function `c2_rehash`** [L91-93]: `def c2_rehash(ctx) -> list`
- **function `_load`** [L96-103]: `def _load(ctx, rel, kind, c2)`
- **function `npz`** [L106-107]: `def npz(ctx, rel, c2=False) -> dict`
- **function `js`** [L110-111]: `def js(ctx, rel, c2=False) -> dict`
- **function `c2npz`** [L114-115]: `def c2npz(ctx, rel) -> dict`
- **function `c2js`** [L118-119]: `def c2js(ctx, rel) -> dict`
- **function `_abs`** [L122-125]: `def _abs(ctx, rel) -> Path`
- **function `put`** [L128-129]: `def put(ctx, rel, **arrays) -> None`
- **function `putj`** [L132-133]: `def putj(ctx, rel, obj) -> None`
- **function `_skip`** [L137-139]: `def _skip(rel) -> bool`
- **function `manifest_stem`** [L142-144]: `def manifest_stem(ctx, stage) -> str` - manifests/<job>.json; a dry-run store runs every stage in one job: <job>-<stage>.
- **function `write_manifest`** [L147-158]: `def write_manifest(ctx, stage) -> Path`
- **function `_coord_ok`** [L161-168]: `def _coord_ok(p) -> bool`
- **function `recognised`** [L171-196]: `def recognised(store) -> dict` - {rel: sha256}: coordinator records, the bound meter file, every accepted manifest's files
- **function `supersede`** [L199-212]: `def supersede(ctx, job, attempt, paths, ruling) -> Path`
- **function `regen_compare`** [L215-216]: `def regen_compare(ctx, path, archived_sha256) -> bool`
- **function `gates`** [L220-221]: `def gates(ctx) -> list`
- **function `_applies`** [L224-226]: `def _applies(g, j, fam) -> bool`
- **function `prior`** [L229-237]: `def prior(ctx, j, fam)` - The first exclusion, CNHS or stop for (j, fam); report-only records never apply
- **function `alive`** [L240-241]: `def alive(ctx, j, fam) -> bool`
- **function `fstop`** [L244-246]: `def fstop(ctx, fam)`
- **function `family_stop`** [L249-255]: `def family_stop(ctx, fam)` - None while >= 2 models remain, else the 2-of-3 rule's outcome (C2 §6.5 rule 2).
- **function `rec`** [L258-259]: `def rec(status, values=None, **who) -> dict`
- **function `lines`** [L262-264]: `def lines(recs) -> dict`
- **function `per`** [L267-270]: `def per(ctx, fams, fn) -> dict` - One line per alive (model, family); fn(j, fam) -> (status, values).
- **function `frac`** [L273-274]: `def frac(mask) -> Fraction`
- **function `dry`** [L278-280]: `def dry(ctx)` - nd_dry, only in a dry-run store (its functions refuse otherwise; G0 (x)).
- **function `proc`** [L283-284]: `def proc(ctx) -> dict`
- **function `models`** [L287-289]: `def models(ctx) -> dict` - {j: (model64, state_sha)}: the C2 checkpoints, or the planted dry-run models.
- **function `_models`** [L292-293]: `def _models(ctx) -> dict`
- **function `table`** [L296-302]: `def table(ctx, split) -> dict`
- **function `orc`** [L305-306]: `def orc(ctx, split) -> dict`
- **function `c2fit`** [L309-310]: `def c2fit(ctx, j) -> dict`
- **function `frozen_oracle`** [L313-314]: `def frozen_oracle(ctx) -> dict`
- **function `inputs`** [L317-318]: `def inputs(ctx, j, H) -> np.ndarray`
- **function `phase`** [L321-332]: `def phase(ctx, j, a3) -> tuple` - (phi, supported) of resid_post_3 rows: the frozen production chart (C2), or the dry-run
- **function `_state`** [L335-346]: `def _state(ctx, j, H, rows, n, kind) -> tuple`
- **function `bundle`** [L349-369]: `def bundle(ctx, split, j, kind=None, roles=cc.ROLES) -> dict` - Per role: inputs, the three hooks, y (frozen C2 basis), for H, H+, H- the phase and
- **function `problem`** [L373-383]: `def problem(ctx, j, p) -> dict` - The projector problem p of model j: C2's frozen R, R_E, R_K1, R_K2, M, or the refit RD,

