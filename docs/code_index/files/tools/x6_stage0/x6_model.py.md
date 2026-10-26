# `tools/x6_stage0/x6_model.py`

- Source: [tools/x6_stage0/x6_model.py](../../../../../tools/x6_stage0/x6_model.py)
- Kind: python
- Lines: 398

## Module docstring

> X6 stage 0: model, closed-form oracle, gates G0/G1 (X6-FROZEN-v1 sections 0-3; API.md 3).
> Exact objects are Fractions and Python ints; floats are float(Fraction). Import does no I/O.

## Imports

### Internal (repo files)

- `from oracle_profile import validate_process` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 21, via sys.path edit)
- `import topo_pilot.world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 23, via package root)
- `from topo_pilot.process import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 24, via package root)
- `from topo_pilot.world.complex import check_boundary_closed` -> [src/topo_pilot/world/complex.py](../../src/topo_pilot/world/complex.py.md) (line 25, via package root)
- `from topo_pilot.world.metrics import check_flat_bounds` -> [src/topo_pilot/world/metrics.py](../../src/topo_pilot/world/metrics.py.md) (line 26, via package root)

### External (third-party)

- `numpy` (lines 14)

### Standard library

- `__future__` (lines 4)
- `decimal` (lines 8)
- `fractions` (lines 9)
- `functools` (lines 10)
- `itertools` (lines 6)
- `pathlib` (lines 11)
- `sys` (lines 7)
- `typing` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/x4_oracle_profile`, `tools/x6_stage0`

## Imported by

- [tests/x6_stage0/test_x6_stage0.py](../../tests/x6_stage0/test_x6_stage0.py.md) (line 24, import)
- [tests/x6_stage0/test_x6_stage0_dp.py](../../tests/x6_stage0/test_x6_stage0_dp.py.md) (line 27, import)
- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 29, import)
- [tests/x6_stage1/test_a_eval.py](../../tests/x6_stage1/test_a_eval.py.md) (line 31, import)
- [tests/x6_stage1/test_a_numerics.py](../../tests/x6_stage1/test_a_numerics.py.md) (line 30, import)
- [tests/x6_stage1/test_a_pairs.py](../../tests/x6_stage1/test_a_pairs.py.md) (line 30, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 26, import)
- [tests/x6zc/test_x6zc_core.py](../../tests/x6zc/test_x6zc_core.py.md) (line 21, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 22, import)
- [tools/x6_stage0/x6_dp.py](x6_dp.py.md) (line 11, import)
- [tools/x6_stage0/x6_exact.py](x6_exact.py.md) (line 13, import)
- [tools/x6_stage0/x6_run.py](x6_run.py.md) (line 18, import)
- [tools/x6_stage0/x6_run.py](x6_run.py.md) (line 26, import)
- [tools/x6_stage0/x6_store.py](x6_store.py.md) (line 20, import)
- [tools/x6_stage0/x6_store.py](x6_store.py.md) (line 23, import)
- [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 21, import)
- [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 26, import)
- [tools/x6_stage1/x6s1_stage_post.py](../x6_stage1/x6s1_stage_post.py.md) (line 20, import)
- [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_stats.py](../x6_stage1/x6s1_stats.py.md) (line 22, import)
- [tools/x6zc/x6zc_census.py](../x6zc/x6zc_census.py.md) (line 17, import)
- [tools/x6zc/x6zc_core.py](../x6zc/x6zc_core.py.md) (line 29, import)
- [tools/x6zc/x6zc_run.py](../x6zc/x6zc_run.py.md) (line 304, import)
- [tools/x6zc/x6zc_run.py](../x6zc/x6zc_run.py.md) (line 313, import)
- [tools/x6zc/x6zc_run.py](../x6zc/x6zc_run.py.md) (line 759, import)

## Top-level constants

- `ARMS`
- `ARMS_SEAM`
- `EMISSIONS`
- `H_COV`
- `H_FIX`
- `KERNEL_BASE`
- `LADDER`
- `MC_ARMS`
- `MC_ROWS`
- `NEIGHBOURS`
- `PROTOCOL_SHA256`
- `REPO`
- `REQUEST_SHA256`
- `R_COMMIT`
- `S3_LIST`
- `SCRATCH_ROOT`
- `STORE`
- `WORKTREE`
- `ZC_WITNESS`
- `_COVER_EXPECT`
- `_EXTRA`
- `_FLUX_EXPECT`
- `_GAUGE`
- `_LETTERS`
- `_NAMES`
- `_SEAM`

## Classes and functions

- **function `compose`** [L62-63]: `def compose(g, h) -> tuple`
- **function `inverse`** [L64-65]: `def inverse(g) -> tuple`
- **function `perm_name`** [L66-67]: `def perm_name(g) -> str`
- **function `state`** [L68-69]: `def state(i: int, x: int) -> int`
- **function `split_state`** [L70-71]: `def split_state(s: int) -> tuple`
- **function `tok`** [L72-75]: `def tok(i: int) -> int`
- **function `vertex`** [L76-79]: `def vertex(w: int) -> int`
- **function `cue`** [L80-81]: `def cue(x: int) -> int`
- **function `seam_letter`** [L88-94]: `def seam_letter(i: int, j: int)`
- **function `seam_labels`** [L103-107]: `def seam_labels(arm: str) -> dict`
- **function `_edge_labels`** [L109-116]: `def _edge_labels(arm: str) -> tuple` decorators: @lru_cache(maxsize=None)
- **function `edge_labels`** [L118-119]: `def edge_labels(arm: str) -> dict`
- **function `eta`** [L120-121]: `def eta(arm: str) -> Fraction`
- **class `_X6TorusBuilder(tw.QuotientLatticeBuilder)`** [L124-128]
- **function `build_world`** [L130-135]: `def build_world()`
- **function `kernel`** [L136-137]: `def kernel(spec) -> np.ndarray`
- **function `f_star_index`** [L138-140]: `def f_star_index(spec) -> int`
- **function `punctured_complex`** [L141-143]: `def punctured_complex(spec)`
- **function `t_base_exact`** [L144-146]: `def t_base_exact() -> list`
- **function `lift`** [L147-154]: `def lift(T_base, labels, eta) -> list`
- **function `sigma_tok`** [L156-157]: `def sigma_tok(w: int) -> int`
- **function `emission`** [L158-166]: `def emission(kind: str) -> list`
- **function `to_float`** [L168-170]: `def to_float(M) -> np.ndarray`
- **function `_model`** [L172-176]: `def _model(arm: str, kind: str) -> dict` decorators: @lru_cache(maxsize=None)
- **function `model`** [L177-181]: `def model(arm: str, kind=None) -> dict` - Cached record (callers never mutate it); kind None: E_cov for GAUGE-COV, else E.
- **function `face_cycle`** [L184-185]: `def face_cycle(row) -> tuple`
- **function `holonomy`** [L186-190]: `def holonomy(path, labels) -> tuple`
- **function `face_holonomies`** [L191-192]: `def face_holonomies(spec, labels) -> list`
- **function `flux`** [L193-194]: `def flux(spec, labels) -> tuple`
- **function `cover_complex`** [L195-204]: `def cover_complex(spec, labels)`
- **function `boundary_circles`** [L206-219]: `def boundary_circles(cx) -> int`
- **function `cover_betti`** [L221-222]: `def cover_betti(cx) -> dict`
- **function `path_letters`** [L225-226]: `def path_letters(path) -> list`
- **function `parikh`** [L227-231]: `def parikh(path) -> tuple`
- **function `statistic`** [L232-236]: `def statistic(S: str, kappa)`
- **function `lam`** [L242-243]: `def lam(m: int, eta=ETA) -> Fraction` decorators: @lru_cache(maxsize=None)
- **function `point_law`** [L245-247]: `def point_law(m: int, z: int, eta=ETA) -> tuple` decorators: @lru_cache(maxsize=None)
- **function `parse`** [L248-259]: `def parse(tokens) -> dict`
- **function `closed_form`** [L261-284]: `def closed_form(arm: str, tokens) -> dict`
- **function `cue_normalised`** [L286-287]: `def cue_normalised(q) -> tuple`
- **function `kgram_law`** [L290-309]: `def kgram_law(m: dict, k: int) -> dict` - Exact stationary law of (w_1..w_k) over reachable strings (prefix-shared DFS).
- **function `five_gram`** [L311-312]: `def five_gram(y: int, y2: int) -> tuple`
- **function `_passes`** [L320-325]: `def _passes(fn, *args) -> bool`
- **function `_lift_ok`** [L326-333]: `def _lift_ok(arm: str, T) -> bool` - Entrywise against the section 2.5 values; exact row and column sums.
- **function `gate_G0`** [L335-373]: `def gate_G0(spec=None) -> dict`
- **function `_one_hot`** [L375-384]: `def _one_hot(kind: str) -> bool`
- **function `gate_G1`** [L386-398]: `def gate_G1() -> dict`

