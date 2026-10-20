# `tools/x6_stage1/x6s1_eval.py`

- Source: [tools/x6_stage1/x6s1_eval.py](../../../../../tools/x6_stage1/x6s1_eval.py)
- Kind: python
- Lines: 447

## Module docstring

> X6S1 eval: the predictor interface (float64 model wrapper, exact oracle and reference wrappers),
> the quantised readout, scoring, cue mass, pair terms, designed statistics and the E3.A chunk outputs
> (X6S1-FROZEN-v1 §2.2-§2.8, §7.4; API.md §7). Import performs no I/O.

## Imports

### Internal (repo files)

- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 25, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 26, via sys.path edit)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](x6s1_cloud.py.md) (line 27, via same directory)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 28, via same directory)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](x6s1_pairs.py.md) (line 29, via same directory)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](x6s1_stats.py.md) (line 30, via same directory)
- `from topo_pilot.contracts import Checkpoint, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 32, via package root)
- `from topo_pilot.learner.stage import load_model` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 33, via package root)
- `import d2a_train` -> [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 42, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 23)
- `torch` (lines 24)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 8)
- `dataclasses` (lines 13)
- `fractions` (lines 14)
- `functools` (lines 15)
- `io` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 16)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime_registry`, `tools/d2a`, `tools/k4b`, `tools/x4_oracle_profile`, `tools/x6_stage0`, `tools/x6_stage1`

## Imported by

- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 23, import)
- [tests/x6_stage1/test_a_eval.py](../../tests/x6_stage1/test_a_eval.py.md) (line 26, import)
- [tests/x6_stage1/test_a_numerics.py](../../tests/x6_stage1/test_a_numerics.py.md) (line 24, import)
- [tests/x6_stage1/test_a_pairs.py](../../tests/x6_stage1/test_a_pairs.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 548, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 23, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 30, import)

## Top-level constants

- `BOS`
- `ORACLE_KINDS`
- `PROFILE_T`
- `REPO`
- `_EXTRA`

## Classes and functions

- **function `set_threads`** [L41-46]: `def set_threads() -> None`
- **function `pad`** [L49-53]: `def pad(histories, n_obs=33) -> np.ndarray`
- **function `model_inputs`** [L56-59]: `def model_inputs(tokens) -> torch.Tensor`
- **function `_ts`** [L62-63]: `def _ts(t, n) -> np.ndarray`
- **class `ModelPredictor`** [L66-113] - The float64 CPU evaluation of a model's verified float32 weights (§2.2).
- **method `ModelPredictor.__init__`** [L69-77]: `def __init__(self, ckpt_path, file_sha256, weights_sha256)`
- **method `ModelPredictor.from_state`** [L80-83]: `def from_state(cls, sd_, name) -> ModelPredictor` decorators: @classmethod
- **method `ModelPredictor._build`** [L85-91]: `def _build(self, sd_, name, step) -> None`
- **method `ModelPredictor.__call__`** [L93-94]: `def __call__(self, tokens, t) -> np.ndarray`
- **method `ModelPredictor.float32`** [L96-101]: `def float32(self, tokens, t) -> np.ndarray` - The same readout from a float32 copy (the weights are float32, so the copy is exact):
- **method `ModelPredictor._run`** [L104-113]: `def _run(model, tokens, t) -> np.ndarray` decorators: @staticmethod
- **function `_law`** [L116-125]: `def _law(arm, kind, h, t)`
- **class `OraclePredictor`** [L128-138]
- **method `OraclePredictor.__init__`** [L129-132]: `def __init__(self, arm, kind)`
- **method `OraclePredictor.__call__`** [L134-138]: `def __call__(self, tokens, t) -> np.ndarray`
- **function `_qcode`** [L142-143]: `def _qcode() -> dict` decorators: @lru_cache(maxsize=None)
- **function `qstar`** [L146-153]: `def qstar(arm, tokens, t) -> tuple`
- **class `QuantInvalid(ValueError)`** [L156-157]
- **function `quantise`** [L160-175]: `def quantise(s) -> np.ndarray` - §2.2 steps 1-3 (T13, T25): Q = 2**20, the R largest fractional parts get +1, ties by the
- **function `readout_exact`** [L178-179]: `def readout_exact(k_row) -> tuple`
- **function `readout`** [L182-183]: `def readout(k) -> np.ndarray`
- **function `score`** [L186-190]: `def score(codes, k, tables) -> np.ndarray` - x_hat_i = sum_j (q ln q)[code] - fl(q)[code] * ln p^Q[k] (§7.4 item 3).
- **function `kl_rows`** [L193-197]: `def kl_rows(q, p) -> np.ndarray`
- **function `cue_mass`** [L200-201]: `def cue_mass(p) -> np.ndarray`
- **function `cue_normalise`** [L204-210]: `def cue_normalise(p) -> np.ndarray`
- **function `pair_terms`** [L213-216]: `def pair_terms(ph, ph2, qh, qh2) -> tuple`
- **function `beta_fsum`** [L219-221]: `def beta_fsum(num, den) -> float`
- **function `beta_exact`** [L224-233]: `def beta_exact(num, den, informative=None) -> Fraction` - x6_exact.beta with pair i as a two-member set of weight den_i, oracle cue difference e_0
- **function `_fam`** [L237-245]: `def _fam(A, fam, pred, qstar_fn, tables) -> dict`
- **function `_xhat`** [L248-249]: `def _xhat(r, tables) -> np.ndarray`
- **function `_mean`** [L252-253]: `def _mean(x) -> float`
- **function `_set_beta`** [L256-270]: `def _set_beta(tok, t, p, q, balanced=False) -> float` - beta over sets (x6_exact.beta semantics in float64): a set is the histories sharing w_{1:s}
- **function `designed_stats`** [L273-303]: `def designed_stats(pred, D_arrays, qstar_fn, tables) -> dict`
- **function `natural_pairs`** [L306-313]: `def natural_pairs(pred, test_tokens, partner_tokens, rows, t=32) -> dict`
- **function `own_arm`** [L316-320]: `def own_arm(pred, arm, tokens, tables, t=32, p=None) -> dict`
- **function `own_pairs`** [L323-331]: `def own_pairs(pred, tokens, partner_tokens, rows, t=32, p_h=None) -> dict` - §2.8 abelian own-process spread (R-0082-2): per own-process R_ord(t) pair, the within-
- **function `float32_diff`** [L334-341]: `def float32_diff(pred, tokens, t=32) -> dict` - §2.8 raw values (R-0082-2): a float32 forward next to the float64 one on the same rows;
- **function `_cue_rows`** [L344-349]: `def _cue_rows(x, cue, name) -> np.ndarray` - Cue-normalised rows of a reference law where q* has cue mass; undefined there raises.
- **function `gamma`** [L352-372]: `def gamma(pred, val_tokens, t=32) -> dict` - gamma_m (§2.8; descriptive; R-0081-1): beta = sum<p_c - q_Parikh,c, d> / sum ||d||^2 with
- **function `_predictor`** [L376-379]: `def _predictor(name, spec)`
- **function `_excl`** [L382-385]: `def _excl(path: Path, data: bytes) -> str`
- **function `_npz`** [L388-391]: `def _npz(path: Path, arrays: dict) -> str`
- **function `_clean`** [L394-399]: `def _clean(v)`
- **function `_json`** [L402-403]: `def _json(path: Path, obj) -> str`
- **function `eval_chunk`** [L406-447]: `def eval_chunk(name, plan, out_dir) -> dict`

