# `tools/x6_stage1/x6s1_data.py`

- Source: [tools/x6_stage1/x6s1_data.py](../../../../../tools/x6_stage1/x6s1_data.py)
- Kind: python
- Lines: 353

## Module docstring

> X6S1 data: bindings, constants, stage-0 constant map, seeds, pools, sampling, digests,
> stage-0 regeneration and init states (X6S1-FROZEN-v1 §2.1, §4, §6.1-§6.2; API.md §3).
> Import performs no I/O and no computation beyond small constants.

## Imports

### Internal (repo files)

- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 21, via sys.path edit)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 24, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 25, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 26, via package root)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 255, via package root) (inside a function)
- `import x6_run` -> [tools/x6_stage0/x6_run.py](../x6_stage0/x6_run.py.md) (line 265, via sys.path edit) (inside a function)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](../x6_stage0/x6_dp.py.md) (line 274, via sys.path edit) (inside a function)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](../x6_stage0/x6_dp.py.md) (line 287, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 20)
- `torch` (lines 253)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 10)
- `functools` (lines 11)
- `hashlib` (lines 8)
- `pathlib` (lines 12)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime_registry`, `tools/d2a`, `tools/k4b`, `tools/x4_oracle_profile`, `tools/x6_stage0`, `tools/x6_stage1`

## Imported by

- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 21, import)
- [tests/x6_stage1/test_a_eval.py](../../tests/x6_stage1/test_a_eval.py.md) (line 24, import)
- [tests/x6_stage1/test_a_numerics.py](../../tests/x6_stage1/test_a_numerics.py.md) (line 23, import)
- [tests/x6_stage1/test_a_pairs.py](../../tests/x6_stage1/test_a_pairs.py.md) (line 23, import)
- [tests/x6_stage1/test_a_rules.py](../../tests/x6_stage1/test_a_rules.py.md) (line 19, import)
- [tests/x6_stage1/test_b_chain_ops.py](../../tests/x6_stage1/test_b_chain_ops.py.md) (line 26, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 27, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 26, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 21, import)
- [tests/x6_stage1/test_b_train_chain.py](../../tests/x6_stage1/test_b_train_chain.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_decide.py](x6s1_decide.py.md) (line 20, import)
- [tools/x6_stage1/x6s1_eval.py](x6s1_eval.py.md) (line 28, import)
- [tools/x6_stage1/x6s1_ingest.py](x6s1_ingest.py.md) (line 24, import)
- [tools/x6_stage1/x6s1_pairs.py](x6s1_pairs.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_registry.py](x6s1_registry.py.md) (line 18, import)
- [tools/x6_stage1/x6s1_run.py](x6s1_run.py.md) (line 23, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 15, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 20, import)
- [tools/x6_stage1/x6s1_stats.py](x6s1_stats.py.md) (line 23, import)

## Top-level constants

- `ACCT_CFG`
- `ADDENDUM1_SHA256`
- `CONST_MAP`
- `EQUIV_CFG`
- `INITS`
- `K4B_STORE`
- `KREG2_FILES`
- `KREG2_N_DIGESTS`
- `KREG_DIR`
- `K_EQUIV`
- `LC_STEPS`
- `MAILBOX`
- `MODELS`
- `MODEL_CFG`
- `NONTEST_POOLS`
- `PREDICTORS`
- `PROJECT_ROOT`
- `PROTOCOL_ID`
- `PROTOCOL_SHA256`
- `P_COMMIT`
- `REPAIR_BLOBS`
- `REPO`
- `REQUEST_SHA256`
- `R_COMMIT`
- `SCRATCH_ROOT`
- `STAGE0_FILES`
- `STAGE0_OUTCOME`
- `STAGE0_STORE`
- `STORE`
- `TEST_POOLS`
- `WAVES`
- `WORKTREE`
- `_EXTRA`
- `_LADDER_NAMES`
- `_POOL_ROWS`

## Classes and functions

- **function `_enc`** [L112-113]: `def _enc(path: str, lo: str, hi: str) -> dict`
- **function `parse_model`** [L159-165]: `def parse_model(name) -> tuple`
- **function `run_key`** [L168-169]: `def run_key(name) -> tuple`
- **function `init_seed`** [L172-173]: `def init_seed(name) -> int`
- **function `batch_generator`** [L176-177]: `def batch_generator(name) -> np.random.Generator`
- **function `pool_spec`** [L184-199]: `def pool_spec(pool, arm='NA', s=None) -> dict`
- **function `sequence_ids`** [L209-210]: `def sequence_ids(spec) -> np.ndarray`
- **function `arm_model`** [L214-215]: `def arm_model(arm) -> dict` decorators: @lru_cache(maxsize=None)
- **function `sample_pool`** [L218-224]: `def sample_pool(spec) -> np.ndarray`
- **function `observation_set`** [L227-229]: `def observation_set(spec, tokens) -> ObservationSet`
- **function `token_digest`** [L232-233]: `def token_digest(tokens) -> str`
- **function `_file_sha`** [L236-237]: `def _file_sha(path) -> str`
- **function `save_pool`** [L240-243]: `def save_pool(path, tokens) -> str`
- **function `load_pool`** [L246-249]: `def load_pool(path, file_sha256) -> np.ndarray`
- **function `init_state`** [L252-260]: `def init_state(name) -> dict`
- **function `regenerate_stage0`** [L264-268]: `def regenerate_stage0() -> dict`
- **function `holonomy_classes`** [L272-281]: `def holonomy_classes(arm='NA', n_max=31) -> dict` decorators: @lru_cache(maxsize=None) - {S: {n: {(v, statistic): {g: count}}}} for n = 1..n_max (x6_dp, unchanged).
- **function `stage0_counts`** [L284-298]: `def stage0_counts(na_tokens) -> dict` - Stage-0 G6 `hits` semantics (x6_run.gate_G6): E_cue = a cue in w_1..w_32; amb_nb =
- **function `stage0_count_check`** [L301-304]: `def stage0_count_check(counts) -> str`
- **function `stage0_value`** [L307-311]: `def stage0_value(report, name)`
- **function `_same`** [L314-315]: `def _same(got, want) -> bool`
- **function `check_stage0_constants`** [L318-329]: `def check_stage0_constants(report) -> dict`
- **function `g0_lo`** [L332-333]: `def g0_lo() -> Fraction`
- **function `g8_lo`** [L336-337]: `def g8_lo() -> Fraction`
- **function `target_threshold`** [L340-341]: `def target_threshold() -> Fraction`
- **function `regret_bar`** [L344-345]: `def regret_bar(dw2_lo: Fraction) -> Fraction`
- **function `prec_delta`** [L348-349]: `def prec_delta() -> Fraction`
- **function `ladder_lo`** [L352-353]: `def ladder_lo(S) -> Fraction`

