# `tools/d2a/d2a_world.py`

- Source: [tools/d2a/d2a_world.py](../../../../../tools/d2a/d2a_world.py)
- Kind: python
- Lines: 397

## Module docstring

> D-2a world, pools, seed map, bins, templates and S0 bindings (D2A-FROZEN-v1 §2, §9.2, §11.3;
> tools/d2a/API.md §2.1, §3). D-1's 4x3 construction is imported unchanged from tools/d1_seam.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import percentile_interval` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 19, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../d1_seam/d1_seam.py.md) (line 28, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 181, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 182, via package root) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](d2a_train.py.md) (line 292, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 4)
- `ast` (lines 6)
- `hashlib` (lines 7)
- `itertools` (lines 12)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 13)
- `subprocess` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(_p)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- [tests/d2a/test_a_pad.py](../../tests/d2a/test_a_pad.py.md) (line 26, import)
- [tests/d2a/test_a_targets.py](../../tests/d2a/test_a_targets.py.md) (line 30, import)
- [tests/d2a/test_a_templates.py](../../tests/d2a/test_a_templates.py.md) (line 27, import)
- [tests/d2a/test_a_world.py](../../tests/d2a/test_a_world.py.md) (line 25, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 20, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 21, import)
- [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 22, import)
- [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 23, import)
- [tools/d2a/d2a_targets.py](d2a_targets.py.md) (line 14, import)
- [tools/d2a/d2a_targets.py](d2a_targets.py.md) (line 15, import)
- [tools/d2a/d2a_train.py](d2a_train.py.md) (line 69, import)
- [tools/d2a/d2a_train.py](d2a_train.py.md) (line 266, import)

## Top-level constants

- `ALLOWED_A`
- `BINS`
- `CHUNK`
- `DISPATCH`
- `GUARDED`
- `HERE`
- `POOLS`
- `POSITIONS`
- `PROTECTED`
- `PROTOCOL`
- `PROTOCOL_SHA`
- `REPO`
- `ROOT`
- `S2`
- `S3`
- `SEQ_CODE`
- `STORE`
- `_FM`

## Classes and functions

- **function `_float_model`** [L68-71]: `def _float_model() -> dict`
- **function `process`** [L74-83]: `def process(proc: str) -> dict` - ``{"T", "E", "mu"}`` of the CM mixture or the C⊕C null (blockdiag(T_C, T_C)).
- **function `world_kernels`** [L86-91]: `def world_kernels(proc: str) -> dict` - Per-block filters: ``T_C``, ``T_M`` (``T_C`` twice for CC), ``E``, ``mu_C``, ``mu_M``.
- **function `stream`** [L94-98]: `def stream(pool: str) -> tuple`
- **function `pool_generator`** [L101-102]: `def pool_generator(pool: str) -> np.random.Generator`
- **function `sequence_ids`** [L105-106]: `def sequence_ids(pool: str) -> np.ndarray`
- **function `sample_pool`** [L109-112]: `def sample_pool(pool: str) -> tuple[np.ndarray, np.ndarray]`
- **function `decision_rows`** [L115-116]: `def decision_rows(tokens: np.ndarray, t: int) -> np.ndarray`
- **function `bin_positions`** [L119-131]: `def bin_positions(tokens: np.ndarray, pool: str) -> np.ndarray` - ``[3, R]``: per bin one decision t chosen uniformly (registered stream), or 0.
- **function `pad`** [L134-137]: `def pad(history) -> np.ndarray`
- **function `template_enumeration`** [L140-159]: `def template_enumeration(t: int) -> list[tuple[tuple, tuple]]` - All equal-gap template pairs at t (§9.2), in the API.md order.
- **function `registered_templates`** [L162-167]: `def registered_templates(t: int) -> list[tuple[tuple, tuple]]`
- **function `template_hashes`** [L170-171]: `def template_hashes(t: int) -> list[str]`
- **function `coverage`** [L174-177]: `def coverage(tokens: np.ndarray, pool: str) -> dict`
- **function `open_store`** [L180-184]: `def open_store(store_root=STORE)`
- **function `_sha`** [L187-188]: `def _sha(path) -> str`
- **function `save_pools`** [L191-216]: `def save_pools(store_root=STORE) -> dict` - Sample and save all 21 pools (POOLS order) once; write pools.json (refuses if present).
- **function `_guard`** [L219-222]: `def _guard(pool: str) -> None`
- **function `pool_index`** [L225-226]: `def pool_index(store_root=STORE) -> dict`
- **function `load_tokens`** [L229-233]: `def load_tokens(pool: str, store_root=STORE) -> np.ndarray`
- **function `load_private`** [L236-242]: `def load_private(pool: str, store_root=STORE) -> tuple[np.ndarray, np.ndarray]`
- **function `master_collisions`** [L245-259]: `def master_collisions(roots) -> list[str]` - meta.json files whose seed_map values or config text contain DATA or MODEL (§2.6).
- **function `_git`** [L262-264]: `def _git(*args) -> str`
- **function `protected_diff`** [L267-279]: `def protected_diff(R: str = '2babe9d', H: str = 'HEAD') -> tuple[list[str], list[str]]` - (entries, violations) of ``git diff --no-renames --name-status R H -- PROTECTED``.
- **function `dispatch`** [L282-286]: `def dispatch(store_root=STORE) -> dict` - Current dispatch identities and pinned H, from the store-local binding (ruling Q4).
- **function `s0_bindings`** [L289-320]: `def s0_bindings(store_root=STORE, mailbox=ROOT / 'agent-handoff', R: str = '2babe9d') -> dict` - Gate 1 (§10.6, API §3): protocol hash, dispatch identities from the store-local binding,
- **function `boot_counts`** [L325-330]: `def boot_counts(n: int, B: int, scope, chunk: int = 250)` - Episode-cluster resamples as count matrices ``[b, n]`` (registered ``boot`` stream).
- **function `boot_totals`** [L333-336]: `def boot_totals(columns, B: int, scope) -> np.ndarray` - ``[B, k]`` resampled totals of per-episode columns ``[n, k]``.
- **function `r2_columns`** [L339-346]: `def r2_columns(n: int, ep, Y, pred, mean_cal) -> np.ndarray` - Per-episode ``(sse, sst, count)`` for the pooled R² with the calibration mean.
- **function `r2_from_sums`** [L349-353]: `def r2_from_sums(sse, sst, count) -> np.ndarray` - ``1 - sse/sst``; NaN where ``sst ≤ 1e-12·count``, and NaN inputs propagate (6c).
- **function `ratio_from_sums`** [L356-359]: `def ratio_from_sums(num, den) -> np.ndarray`
- **function `quantiles`** [L362-367]: `def quantiles(draws, qs) -> list | None` - None when any draw is undefined: the interval is invalidated, never redrawn (§6).
- **function `interval`** [L370-372]: `def interval(draws) -> tuple | None`
- **function `beta_draws`** [L375-386]: `def beta_draws(ep, r, d, n, B, scope, extra=None) -> dict` - Point and resampled β = Σrd/Σd² (and Σ r8·d for the window baseline), per episode.
- **function `pooled_r2`** [L389-397]: `def pooled_r2(cols: list, B: int, scope) -> tuple` - ``(point(i), draws(i))``: pooled R² of the i-th stacked ``(sse, sst, count)`` triple.

