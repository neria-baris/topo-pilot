# `tools/x6_stage1/x6s1_stage_pre.py`

- Source: [tools/x6_stage1/x6s1_stage_pre.py](../../../../../tools/x6_stage1/x6s1_stage_pre.py)
- Kind: python
- Lines: 431

## Module docstring

> X6S1 stage content of E0 and E0b (ruling R-0079-1): AUTH-ADMIT, S0, REG1 and the non-test
> pools, PF, G0-ORC (a)-(g), SCORE, G0-POS, REG2 with the test draw and SEP, G0-FEAS, HEADROOM-D,
> CLOUD-PREP and SMOKE-INGEST (X6S1-FROZEN-v1 §4.6, §5.3, §5.9, §6, §8 rows 0b-12, §12 item 11;
> API.md §13 items 27-29). Each gate is fn(ctx) -> {"status", "values"}, run in PLAN order by
> x6s1_run.run_stage. Import performs no I/O beyond the imported modules' own (§13 item 24).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 20, via same directory)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](../x6_stage0/x6_dp.py.md) (line 25, via unique basename)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 26, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 27, via unique basename)
- `import x6_run` -> [tools/x6_stage0/x6_run.py](../x6_stage0/x6_run.py.md) (line 28, via unique basename)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](x6s1_cloud.py.md) (line 29, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 30, via same directory)
- `import x6s1_ingest` -> [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 31, via same directory)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](x6s1_pairs.py.md) (line 32, via same directory)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](x6s1_registry.py.md) (line 33, via same directory)
- `import x6s1_run` -> [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 34, via same directory)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](x6s1_stats.py.md) (line 35, via same directory)
- `from topo_pilot.contracts import ArtifactStore, ObservationSet, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 37, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 38, via package root)

### External (third-party)

- `numpy` (lines 23)
- `torch` (lines 24)

### Standard library

- `__future__` (lines 8)
- `decimal` (lines 16)
- `fractions` (lines 17)
- `io` (lines 10)
- `json` (lines 11)
- `math` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 18)
- `subprocess` (lines 14)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 27, import)
- [tools/x6zc/x6zc_run.py](../x6zc/x6zc_run.py.md) (line 629, import)

## Top-level constants

- `BIG`
- `LADDER_G`
- `PLAN`
- `SUITES`

## Classes and functions

- **function `_r`** [L50-51]: `def _r(ok, values=None, bad='FAIL') -> dict`
- **function `_ok`** [L52-55]: `def _ok(v) -> bool`
- **function `_scratch`** [L56-56]: `def _scratch(ctx) -> Path`
- **function `_e0`** [L57-60]: `def _e0(store, *rel) -> Path`
- **function `_tok`** [L61-61]: `def _tok(ctx, name) -> np.ndarray`
- **function `ostore`** [L64-65]: `def ostore(store) -> ArtifactStore`
- **function `pools_index`** [L66-66]: `def pools_index(store) -> dict`
- **function `load_obs`** [L67-72]: `def load_obs(store, name) -> ObservationSet`
- **function `_draw`** [L73-89]: `def _draw(ctx, specs) -> None` - Each pool once from its registered stream (§6.1); train and smoke also as the .npy bundle
- **function `auth_admit`** [L92-93]: `def auth_admit(ctx) -> dict`
- **function `_s0_dispatch`** [L94-107]: `def _s0_dispatch(ctx) -> dict` - E0 only (D-0087-2, R-0087-3; API.md §13 item 39): a GATES.jsonl holding exactly this
- **function `s0`** [L108-111]: `def s0(ctx) -> dict`
- **function `_man`** [L112-112]: `def _man(m) -> dict`
- **function `reg1`** [L113-132]: `def reg1(ctx) -> dict` - REG1 from its four sources (the inventory over the dispatch's X6 scratch roots), then the
- **function `_run`** [L135-142]: `def _run(ctx, name, args, env) -> subprocess.CompletedProcess`
- **function `sizes_ok`** [L143-147]: `def sizes_ok(report) -> bool` - check_file_sizes lists no X6S1 file but the seven big modules (§13 items 28, 32, 37).
- **function `pf`** [L148-169]: `def pf(ctx) -> dict` - The unchanged suites and tests/x6_stage1, the size and import checks, NB-STATIC,
- **function `_pairs`** [L172-178]: `def _pairs(ctx, pool) -> dict` - The t = 32 partners of `pool` (§2.3) with q* of both members and den = ||Δq*_c||².
- **function `_t6`** [L179-181]: `def _t6(enc, name) -> bool`
- **function `_partner_ok`** [L182-188]: `def _partner_ok(h, h2) -> bool`
- **function `_model_arrays`** [L189-193]: `def _model_arrays(report) -> dict`
- **function `_designed`** [L194-212]: `def _designed(ctx, report) -> dict` - (f) on D: fraction_filter = closed_form at every designed readout, prefix invariance of
- **function `g0_orc`** [L213-241]: `def g0_orc(ctx) -> dict` - (a)-(g); persists tables/class_tables_NA.json and tables/designed.npz (D frozen in E0).
- **function `_quantiser`** [L244-255]: `def _quantiser(laws) -> dict`
- **function `score`** [L256-281]: `def score(ctx) -> dict` - Quantiser on synthetic and gate laws, the certified tables (tables/log_tables.npz), the
- **function `g0_pos`** [L282-299]: `def g0_pos(ctx) -> dict` - On gate(NA) 2^16: (a) the readout floor per row; (b) raw Δ_nat(q_S) vs G_S(32) within
- **function `reg2_sep`** [L302-316]: `def reg2_sep(ctx) -> dict` - REG2 and the test draw inside the reservation window, POOLS.json, SEP on every row; ρ̄.
- **function `g0_feas`** [L319-343]: `def g0_feas(ctx) -> dict` - (a)-(d) (FEASIBILITY_NO_GO, S3). The test partners (t = 32) are drawn and persisted: test(NA)
- **function `headroom`** [L344-349]: `def headroom(ctx) -> dict` - β_8 and mean ||d||² over all val(NA) rows (oracle only; se.gamma, R-0081-1: rows where q*
- **function `cloud_prep`** [L352-378]: `def cloud_prep(ctx) -> dict` - init(1..4) and the smoke init (stages/E0/init/) with digests; bundles C0, C1, C2 (tickets
- **function `frozen`** [L381-381]: `def frozen(store, wave) -> dict`
- **function `local_digests`** [L382-384]: `def local_digests(fz) -> dict`
- **function `_replay`** [L385-397]: `def _replay(d, chain, toks)` - Descriptive (§5.9): 100 local CPU updates from the GPU step-100 checkpoint against the GPU
- **function `smoke_ingest`** [L398-425]: `def smoke_ingest(ctx) -> dict` - The four integrity gates on the smoke, the float64 forward (t = 32) on 1,024 smoke rows,

