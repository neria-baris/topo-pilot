# `tools/x6_stage1/x6s1_stage_post.py`

- Source: [tools/x6_stage1/x6s1_stage_post.py](../../../../../tools/x6_stage1/x6s1_stage_post.py)
- Kind: python
- Lines: 461

## Module docstring

> X6S1 stage content of E1, E2, E3a/E3w and E3z (ruling R-0079-1): INGEST, LEARN, LC, LOSS-ECHO,
> E3.0, DET, the wave schedule, `chunk_plan`, E3.2-E3.9, §2.8, the report and unsealing (protocol §8
> rows 14-30; API.md §13 items 27-31); gates fn(ctx) -> {"status", "values"}; no I/O at import.

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 15, via same directory)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 20, via unique basename)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](x6s1_cloud.py.md) (line 21, via same directory)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](x6s1_decide.py.md) (line 22, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 23, via same directory)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 24, via same directory)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](x6s1_pairs.py.md) (line 25, via same directory)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 26, via same directory)
- `import x6s1_stage_pre` -> [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 27, via same directory)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](x6s1_stats.py.md) (line 28, via same directory)

### External (third-party)

- `numpy` (lines 18)
- `torch` (lines 19)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 12)
- `io` (lines 8)
- `json` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 13)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `BINS`
- `PLAN`

## Classes and functions

- **function `_r`** [L37-38]: `def _r(ok, values=None, bad='FAIL') -> dict`
- **function `_gates`** [L39-43]: `def _gates(store) -> dict`
- **function `_last`** [L44-44]: `def _last(store, gate)`
- **function `_vals`** [L45-45]: `def _vals(store, gate) -> dict`
- **function `_e0`** [L46-46]: `def _e0(store) -> dict`
- **function `_bytes`** [L47-50]: `def _bytes(path, sha) -> bytes`
- **function `_npz`** [L51-53]: `def _npz(path, sha) -> dict`
- **function `_tables`** [L54-55]: `def _tables(store, e0) -> dict`
- **function `_partners`** [L56-59]: `def _partners(store, e0, arm='NA') -> dict`
- **function `_tok`** [L60-60]: `def _tok(store, name) -> np.ndarray`
- **function `_status`** [L61-63]: `def _status(store) -> dict`
- **function `_pred`** [L64-68]: `def _pred(store, m) -> se.ModelPredictor`
- **function `_dir`** [L69-71]: `def _dir(ctx) -> Path`
- **function `_wjson`** [L72-72]: `def _wjson(path, obj) -> str`
- **function `_mean`** [L73-73]: `def _mean(x) -> float`
- **function `_lt`** [L74-74]: `def _lt(x, bound) -> bool`
- **function `_waves`** [L75-75]: `def _waves(ctx) -> list`
- **function `_iv`** [L76-78]: `def _iv(r) -> dict`
- **function `s0`** [L81-87]: `def s0(ctx) -> dict`
- **function `_envs`** [L90-94]: `def _envs(snap, store, m) -> int`
- **function `_ingest`** [L95-102]: `def _ingest(ctx, wave) -> dict`
- **function `ingest_c2`** [L103-106]: `def ingest_c2(ctx) -> dict`
- **function `learn`** [L107-129]: `def learn(ctx) -> dict` - §4.7 on val: UB_0.975 of the B_GATE bootstrap of x̂ < G_8.lo; releases statuses only.
- **function `_lc`** [L130-141]: `def _lc(ctx, wave, part) -> dict`
- **function `schedule`** [L144-146]: `def schedule(store) -> list`
- **function `_regen`** [L147-157]: `def _regen(ctx) -> dict`
- **function `bind`** [L158-174]: `def bind(ctx) -> dict`
- **function `det`** [L175-182]: `def det(ctx) -> dict`
- **function `_spec`** [L183-193]: `def _spec(store, name, e0) -> dict`
- **function `chunk_plan`** [L194-217]: `def chunk_plan(store, name) -> dict`
- **function `e3a`** [L218-233]: `def e3a(ctx) -> dict`
- **function `_chunk`** [L236-242]: `def _chunk(store, name, rec)`
- **function `learn_test`** [L243-264]: `def learn_test(ctx) -> dict`
- **function `readout`** [L265-290]: `def readout(ctx) -> dict`
- **function `placebo`** [L291-296]: `def placebo(ctx) -> dict`
- **function `xcheck`** [L297-302]: `def xcheck(ctx) -> dict`
- **function `_draws`** [L303-307]: `def _draws(ctx, names, B, gen) -> tuple`
- **function `_descriptive`** [L308-345]: `def _descriptive(ctx) -> dict`
- **function `stats`** [L346-371]: `def stats(ctx) -> dict`
- **function `prec`** [L372-377]: `def prec(ctx) -> dict`
- **function `confirm`** [L378-398]: `def confirm(ctx) -> dict`
- **function `_released`** [L399-401]: `def _released(store) -> dict`
- **function `_echo`** [L402-405]: `def _echo(store) -> dict`
- **function `rules`** [L406-449]: `def rules(ctx) -> dict`

