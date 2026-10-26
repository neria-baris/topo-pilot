# `tools/x6_stage1/x6s1_pairs.py`

- Source: [tools/x6_stage1/x6s1_pairs.py](../../../../../tools/x6_stage1/x6s1_pairs.py)
- Kind: python
- Lines: 322

## Module docstring

> X6S1 pairs: Parikh class tables, segment parse, the exact backward partner sampler and its
> exhaustive check, the designed set D, and the oracle laws of the references (X6S1-FROZEN-v1
> §2.3, §2.5, §6.3, §8 G0-ORC (c)-(d), (g); API.md §4). Import performs no I/O.

## Imports

### Internal (repo files)

- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](../x6_stage0/x6_dp.py.md) (line 22, via sys.path edit)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 23, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 24, via sys.path edit)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 25, via same directory)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from oracle_profile import suffix_posterior` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 300, via sys.path edit) (inside a function)
- `from topo_pilot.oracle import FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 302, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 6)
- `collections` (lines 11)
- `fractions` (lines 12)
- `functools` (lines 13)
- `hashlib` (lines 8)
- `json` (lines 68)
- `pathlib` (lines 14)
- `random` (lines 9)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime_registry`, `tools/d2a`, `tools/k4b`, `tools/x4_oracle_profile`, `tools/x6_stage0`, `tools/x6_stage1`

## Imported by

- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 22, import)
- [tests/x6_stage1/test_a_pairs.py](../../tests/x6_stage1/test_a_pairs.py.md) (line 24, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 22, import)
- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 23, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 29, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 32, import)
- [tools/x6zc/x6zc_census.py](../x6zc/x6zc_census.py.md) (line 19, import)
- [tools/x6zc/x6zc_core.py](../x6zc/x6zc_core.py.md) (line 44, import)
- [tools/x6zc/x6zc_dry.py](../x6zc/x6zc_dry.py.md) (line 18, import)
- [tools/x6zc/x6zc_stage_a.py](../x6zc/x6zc_stage_a.py.md) (line 21, import)
- [tools/x6zc/x6zc_stage_bc.py](../x6zc/x6zc_stage_bc.py.md) (line 15, import)

## Top-level constants

- `CONTROL_SETS`
- `FLAT_FACE`
- `PAIR_FAMILIES`
- `REPO`
- `STAGE0_NAMED`
- `STAGE0_PREFIXES`
- `W2_LETTERS`
- `_EXTRA`
- `_S7`

## Classes and functions

- **function `class_tables`** [L42-49]: `def class_tables(arm='NA', n_max=31) -> dict` decorators: @lru_cache(maxsize=None)
- **function `tables_bytes`** [L52-54]: `def tables_bytes(tables) -> bytes`
- **function `save_tables`** [L57-61]: `def save_tables(path, tables) -> str`
- **function `load_tables`** [L64-73]: `def load_tables(path, sha256) -> dict`
- **function `validate_tables`** [L76-82]: `def validate_tables(tables) -> dict` - Σ_{v ≠ a★, κ} c_m equals x6_dp.avoid_counts totals for every layer m ≥ 1 present.
- **function `segment`** [L86-94]: `def segment(tokens, t)`
- **function `in_r_ord`** [L97-99]: `def in_r_ord(tokens, t) -> bool`
- **function `_bump`** [L102-107]: `def _bump(k, u, v, d)`
- **function `predecessors`** [L110-117]: `def predecessors(tables, m, v, kappa) -> list`
- **function `sample_segment`** [L120-130]: `def sample_segment(tables, v_t, kappa, n, rnd: random.Random) -> tuple`
- **function `partner_seed`** [L133-134]: `def partner_seed(pool, t, row) -> int`
- **function `partner`** [L137-143]: `def partner(tables, tokens, t, pool, row)`
- **function `partners`** [L146-157]: `def partners(tables, pool_tokens, t, pool, rows=None) -> dict`
- **function `sampler_law`** [L160-171]: `def sampler_law(tables, v_t, kappa, n) -> dict`
- **function `exhaustive_check`** [L174-182]: `def exhaustive_check(n_max=6) -> dict`
- **function `natural_prefixes`** [L186-193]: `def natural_prefixes(prefix_tokens, rnd_len: np.random.Generator) -> list`
- **function `_loops`** [L196-197]: `def _loops(letters) -> tuple`
- **function `designed_history`** [L200-202]: `def designed_history(prefix, letters, y) -> tuple`
- **function `_w1_history`** [L205-207]: `def _w1_history(prefix, member, y) -> tuple`
- **function `designed_set`** [L210-225]: `def designed_set(prefix_pool) -> dict`
- **function `_pad`** [L228-232]: `def _pad(rows) -> np.ndarray`
- **function `designed_arrays`** [L235-246]: `def designed_arrays(D) -> dict`
- **function `designed_sha256`** [L249-255]: `def designed_sha256(arrays) -> str`
- **function `gap_enclosures`** [L258-269]: `def gap_enclosures() -> dict` - Δ_W2 (y = 0, the two W2 members) and Δ_W3 (y = 0, the 24 W3 orderings) as 80/120-digit
- **function `_hist`** [L273-274]: `def _hist(tokens, t) -> tuple`
- **function `q_exact`** [L277-278]: `def q_exact(arm, tokens, t) -> tuple`
- **function `_with_cue`** [L281-285]: `def _with_cue(q, m, w) -> tuple`
- **function `q_stat`** [L288-296]: `def q_stat(S, tokens, t) -> tuple` - Exact Bayes law given R_S (x6_run.gate_G6 semantics; class tables of x6_dp).
- **function `q_window`** [L299-307]: `def q_window(tokens, t, k=8) -> np.ndarray`
- **function `q_heuristic`** [L310-322]: `def q_heuristic(kind, tokens, t) -> tuple` - The competitor's law: the segment holonomy replaced by competitor_holonomy(kind, seam

