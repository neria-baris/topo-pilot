# `tools/hwsb/hwsb_data.py`

- Source: [tools/hwsb/hwsb_data.py](../../../../../tools/hwsb/hwsb_data.py)
- Kind: python
- Lines: 352

## Module docstring

> HWSB data: process build, streams, IDs, sampling, blocks, H2-B, registry reader (API.md §2).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 15, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 17, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 18, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from topo_pilot.contracts import EmissionSpec, ObservationSet, SeedTree, SequenceLayout, StageFailure, TransitionSpec, WorldSpec, payload_checksum` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 31, via package root)
- `from topo_pilot.dataset.checks import check_disjoint, check_first_token, check_ranges, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 32, via package root)
- `from topo_pilot.dataset.public import assert_public` -> [src/topo_pilot/dataset/public.py](../../src/topo_pilot/dataset/public.py.md) (line 39, via package root)
- `from topo_pilot.process.stage import ProcessStage` -> [src/topo_pilot/process/stage.py](../../src/topo_pilot/process/stage.py.md) (line 40, via package root)
- `from topo_pilot.world.stage import WorldStage` -> [src/topo_pilot/world/stage.py](../../src/topo_pilot/world/stage.py.md) (line 41, via package root)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](hwsb_registry.py.md) (line 349, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 16)
- `torch` (lines 230)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `hashlib` (lines 11)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 23, import)
- [tests/hwsb/test_b_hold.py](../../tests/hwsb/test_b_hold.py.md) (line 20, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 23, import)
- [tests/hwsb/test_b_process.py](../../tests/hwsb/test_b_process.py.md) (line 22, import)
- [tests/hwsb/test_b_registry.py](../../tests/hwsb/test_b_registry.py.md) (line 23, import)
- [tests/hwsb/test_b_streams.py](../../tests/hwsb/test_b_streams.py.md) (line 19, import)
- [tools/hwsb/hwsb_driver.py](hwsb_driver.py.md) (line 17, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 20, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 15, import)
- [tools/hwsb/hwsb_eval.py](hwsb_eval.py.md) (line 19, import)
- [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 13, import)
- [tools/hwsb/hwsb_kb.py](hwsb_kb.py.md) (line 13, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 17, import)
- [tools/hwsb/hwsb_registry.py](hwsb_registry.py.md) (line 15, import)
- [tools/hwsb/hwsb_registry.py](hwsb_registry.py.md) (line 19, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 15, import)

## Top-level constants

- `BLOCKS`
- `READER`
- `ROLES`
- `_REGISTRY_NAMES`

## Classes and functions

- **function `_check_perm`** [L50-58]: `def _check_perm(perm, V) -> np.ndarray`
- **function `assemble`** [L61-95]: `def assemble(world, trans, emissions, ids, features=None, n_axial=6) -> dict` - The process dict of API §2.1 from loaded specs (also used by the dry tiny world).
- **function `build_process`** [L98-117]: `def build_process(store, masters=hc.MASTERS, emission_cfg=hc.EMIS_CFG, world_cfg=hc.WORLD_CFG, transition_cfg=hc.TRANS_CFG) -> dict`
- **function `_sha_array`** [L120-121]: `def _sha_array(x) -> str`
- **function `arrays_sha256`** [L124-130]: `def arrays_sha256(proc) -> dict`
- **function `spec_checksums`** [L133-143]: `def spec_checksums(store, proc) -> dict`
- **function `_check_role`** [L146-158]: `def _check_role(role, plan, master, tree=None) -> None`
- **function `stream_record`** [L161-164]: `def stream_record(role, plan, master=None) -> list`
- **function `data_generator`** [L167-171]: `def data_generator(role, plan, master=None, tree=None)`
- **function `sequence_ids`** [L174-180]: `def sequence_ids(role, n, plan, master=None) -> np.ndarray`
- **function `_checks`** [L183-188]: `def _checks(tokens, states, V, N, p_w, split) -> None`
- **function `sample_observations`** [L191-201]: `def sample_observations(T, E_named, pi, perm, n, rng, split, layout=None) -> np.ndarray` - One split of DatasetStage._sample_all: canonical draw, named = perm[canonical].
- **function `sample_block`** [L204-213]: `def sample_block(T, E_canon, pi, n, rng, layout=None) -> np.ndarray`
- **function `canonical32`** [L216-217]: `def canonical32(named, perm) -> np.ndarray`
- **function `named32`** [L220-221]: `def named32(canon32, perm) -> np.ndarray`
- **function `model_inputs`** [L224-233]: `def model_inputs(canon32, perm)` - [BOS, named w1..w32]: c1_model.model_inputs (BOS 36) for V = 36; BOS = V otherwise
- **function `make_train_dev`** [L236-278]: `def make_train_dev(store, proc, master, plan) -> dict`
- **function `make_block`** [L281-294]: `def make_block(proc, role, plan) -> dict`
- **function `lowest_rows`** [L297-299]: `def lowest_rows(seq_ids, n=hc.PANEL) -> np.ndarray`
- **function `save_block`** [L302-312]: `def save_block(out, block) -> Path`
- **function `load_block`** [L315-339]: `def load_block(path) -> dict`
- **function `__getattr__`** [L346-352]: `def __getattr__(name)` - API names that live in hwsb_registry (split by size), re-exported lazily.

