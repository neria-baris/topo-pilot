# `tools/c2_nd/nd_stage_base.py`

- Source: [tools/c2_nd/nd_stage_base.py](../../../../../tools/c2_nd/nd_stage_base.py)
- Kind: python
- Lines: 389

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

- `import_module` line 286: `nd_dry` -> [tools/c2_nd/nd_dry.py](nd_dry.py.md)

### sys.path additions

- none

## Imported by

- [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 25, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 31, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 28, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 32, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 28, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 33, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 27, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 42, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 21, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 25, import)

## Top-level constants

- `COORD`
- `FP`
- `PROB_KEYS`
- `SCHEMA`
- `SRC`

## Classes and functions

- **function `_jr`** [L42-46]: `def _jr(path)`
- **function `_eq`** [L49-50]: `def _eq(a, b) -> bool`
- **function `_sha_ok`** [L53-54]: `def _sha_ok(path, want) -> bool`
- **function `_js`** [L57-69]: `def _js(v)`
- **function `_npz`** [L72-74]: `def _npz(path) -> dict`
- **function `cache`** [L77-80]: `def cache(ctx, key, fn)`
- **function `c2_store`** [L83-89]: `def c2_store(ctx) -> tuple` - (root, {rel: sha256}): the C2 store and its CONTRACT table, or in a dry-run store its c2/
- **function `c2_rehash`** [L92-94]: `def c2_rehash(ctx) -> list`
- **function `_load`** [L97-104]: `def _load(ctx, rel, kind, c2)`
- **function `npz`** [L107-108]: `def npz(ctx, rel, c2=False) -> dict`
- **function `js`** [L111-112]: `def js(ctx, rel, c2=False) -> dict`
- **function `c2npz`** [L115-116]: `def c2npz(ctx, rel) -> dict`
- **function `c2js`** [L119-120]: `def c2js(ctx, rel) -> dict`
- **function `_abs`** [L123-126]: `def _abs(ctx, rel) -> Path`
- **function `put`** [L129-130]: `def put(ctx, rel, **arrays) -> None`
- **function `putj`** [L133-134]: `def putj(ctx, rel, obj) -> None`
- **function `_skip`** [L138-140]: `def _skip(rel) -> bool`
- **function `manifest_stem`** [L143-145]: `def manifest_stem(ctx, stage) -> str` - manifests/<job>.json; a dry-run store runs every stage in one job: <job>-<stage>.
- **function `write_manifest`** [L148-159]: `def write_manifest(ctx, stage) -> Path`
- **function `_coord_ok`** [L162-169]: `def _coord_ok(p) -> bool`
- **function `recognised`** [L172-197]: `def recognised(store) -> dict` - {rel: sha256}: coordinator records, the bound meter file, every accepted manifest's files
- **function `supersede`** [L200-213]: `def supersede(ctx, job, attempt, paths, ruling) -> Path`
- **function `regen_compare`** [L216-217]: `def regen_compare(ctx, path, archived_sha256) -> bool`
- **function `gates`** [L221-222]: `def gates(ctx) -> list`
- **function `_applies`** [L225-227]: `def _applies(g, j, fam) -> bool`
- **function `prior`** [L230-238]: `def prior(ctx, j, fam)` - The first exclusion, CNHS or stop for (j, fam); report-only records never apply
- **function `alive`** [L241-242]: `def alive(ctx, j, fam) -> bool`
- **function `fstop`** [L245-247]: `def fstop(ctx, fam)`
- **function `family_stop`** [L250-256]: `def family_stop(ctx, fam)` - None while >= 2 models remain, else the 2-of-3 rule's outcome (C2 §6.5 rule 2).
- **function `rec`** [L259-260]: `def rec(status, values=None, **who) -> dict`
- **function `lines`** [L263-265]: `def lines(recs) -> dict`
- **function `per`** [L268-271]: `def per(ctx, fams, fn) -> dict` - One line per alive (model, family); fn(j, fam) -> (status, values).
- **function `sg`** [L274-276]: `def sg(b, side) -> int` - The guarded sign of bound `side` ("L" or "U") of one nd_split.bounds entry (C2 sg).
- **function `frac`** [L279-280]: `def frac(mask) -> Fraction`
- **function `dry`** [L284-286]: `def dry(ctx)` - nd_dry, only in a dry-run store (its functions refuse otherwise; G0 (x)).
- **function `proc`** [L289-290]: `def proc(ctx) -> dict`
- **function `models`** [L293-295]: `def models(ctx) -> dict` - {j: (model64, state_sha)}: the C2 checkpoints, or the planted dry-run models.
- **function `_models`** [L298-299]: `def _models(ctx) -> dict`
- **function `table`** [L302-308]: `def table(ctx, split) -> dict`
- **function `orc`** [L311-312]: `def orc(ctx, split) -> dict`
- **function `c2fit`** [L315-316]: `def c2fit(ctx, j) -> dict`
- **function `frozen_oracle`** [L319-320]: `def frozen_oracle(ctx) -> dict`
- **function `inputs`** [L323-324]: `def inputs(ctx, j, H) -> np.ndarray`
- **function `phase`** [L327-338]: `def phase(ctx, j, a3) -> tuple` - (phi, supported) of resid_post_3 rows: the frozen production chart (C2), or the dry-run
- **function `_state`** [L341-352]: `def _state(ctx, j, H, rows, n, kind) -> tuple`
- **function `bundle`** [L355-375]: `def bundle(ctx, split, j, kind=None, roles=cc.ROLES) -> dict` - Per role: inputs, the three hooks, y (frozen C2 basis), for H, H+, H- the phase and
- **function `problem`** [L379-389]: `def problem(ctx, j, p) -> dict` - The projector problem p of model j: C2's frozen R, R_E, R_K1, R_K2, M, or the refit RD,

