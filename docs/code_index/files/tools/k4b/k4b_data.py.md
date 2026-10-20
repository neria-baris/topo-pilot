# `tools/k4b/k4b_data.py`

- Source: [tools/k4b/k4b_data.py](../../../../../tools/k4b/k4b_data.py)
- Kind: python
- Lines: 190

## Module docstring

> K4b process assembly, sampling, sequence IDs, history tables, separation (API.md §2).

## Imports

### Internal (repo files)

- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 11, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 12, via same directory)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 14, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 15, via unique basename)
- `from k4b_config import BLOCK, MODELS, PANEL, PROCESS, SCOPE` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 16, via same directory)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 19, via package root)
- `from topo_pilot.dataset.checks import check_disjoint, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 20, via package root)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](../x4_oracle_profile/inputs.py.md) (line 38, via unique basename) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 39, via unique basename) (inside a function)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 100, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_b_data.py](../../tests/k4b/test_b_data.py.md) (line 23, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 18, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 18, import)

## Top-level constants

- `IDENTITY`
- `INCOMPLETE`
- `LINEAGE`
- `PREDICATES`
- `PREDICATE_REASON`

## Classes and functions

- **function `_int_map`** [L28-33]: `def _int_map(d, what) -> dict`
- **function `load_process`** [L36-71]: `def load_process(cfg=None) -> dict` - inputs.load_process, re-keyed by int seed; perms and canonical emissions checked.
- **function `history_generator`** [L74-75]: `def history_generator(split, block) -> np.random.Generator`
- **function `sequence_ids`** [L78-80]: `def sequence_ids(split, block) -> np.ndarray`
- **function `sample_block`** [L83-92]: `def sample_block(T, E_canon, pi, split, block) -> tuple` - One HMMSampler.sample(3072, rng) call; w33 and the states dropped; rows sorted by id.
- **function `named_from_canonical`** [L95-96]: `def named_from_canonical(canon32, perm) -> np.ndarray`
- **function `model_inputs`** [L99-102]: `def model_inputs(canon32, perm)`
- **function `digests`** [L105-106]: `def digests(canon32) -> list`
- **function `lowest_rows`** [L109-110]: `def lowest_rows(seq_ids, n=PANEL) -> np.ndarray`
- **function `duplicates`** [L113-122]: `def duplicates(canon32) -> dict` - Counted by digest, never removed. n_duplicate_rows = n_rows - n_unique (API §13 item 24).
- **function `history_table`** [L125-147]: `def history_table(canon32, seq_ids, split, block) -> dict` - Rows in ascending sequence_id; landmarks (cal, val), ref rows and decoder panels (cal).
- **function `separation_cal_val`** [L150-151]: `def separation_cal_val(U_cal, U_val, reg1) -> dict`
- **function `separation_fresh`** [L154-157]: `def separation_fresh(U_test, reg2) -> dict`
- **function `seq_disjoint`** [L160-175]: `def seq_disjoint(blocks, frozen_union, frozen_ranges=()) -> dict`
- **function `sealed_d2a_predicate`** [L178-180]: `def sealed_d2a_predicate(canon32) -> np.ndarray` - True where all 32 symbols lie in {0,...,4} (the sealed D-2a alphabet, §3.4 e).
- **function `predicate_check`** [L186-190]: `def predicate_check(canon32, predicates) -> dict`

