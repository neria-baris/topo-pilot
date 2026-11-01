# `tools/hwsu/hwsu_pairs.py`

- Source: [tools/hwsu/hwsu_pairs.py](../../../../../tools/hwsu/hwsu_pairs.py)
- Kind: python
- Lines: 143

## Module docstring

> HWSU exact conditional prefix sampler, blocks, ids and history tables (API.md §2; protocol §2.1,
> §2.8). Kernel functions keep the input dtype: object arrays of Fraction give exact results.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 6, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 9, via unique basename)
- `import topo_pilot.dataset.checks` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 10, via package root)
- `import topo_pilot.dataset.sampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 11, via package root)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 12, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 13, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 14, via package root)

### External (third-party)

- `numpy` (lines 7)

### Standard library

- `__future__` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 15, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 14, import)
- [tests/hwsu/test_a_of_sampler.py](../../tests/hwsu/test_a_of_sampler.py.md) (line 16, import)
- [tests/hwsu/test_b_of_streams.py](../../tests/hwsu/test_b_of_streams.py.md) (line 18, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 12, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 10, import)
- [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 12, import)

## Top-level constants

- `SAMPLER`

## Classes and functions

- **function `_flat`** [L19-20]: `def _flat(x)`
- **function `stationarity_error`** [L23-25]: `def stationarity_error(T, pi) -> float`
- **function `check_process`** [L28-37]: `def check_process(T, E, pi) -> None`
- **function `time_reversal`** [L40-42]: `def time_reversal(T, pi)`
- **function `backward_messages`** [L45-53]: `def backward_messages(T, E, tokens, suffix_len=4)`
- **function `bridge`** [L56-62]: `def bridge(pi, beta)`
- **function `prefix_kernels`** [L65-69]: `def prefix_kernels(T, E, pi, suffix_row, prefix_len) -> dict`
- **function `sample_prefix`** [L72-87]: `def sample_prefix(T, E, pi, arm1, rng, suffix_len=4)`
- **function `suffix_equal`** [L90-92]: `def suffix_equal(arm1, arm2, suffix_len=4)`
- **function `generator`** [L96-97]: `def generator(scope, split, block, process=None)`
- **function `seq_ids`** [L100-104]: `def seq_ids(scope, split, block, arm, n, process=None)`
- **function `_singles`** [L107-114]: `def _singles(T, E, pi, scope, split, block, n, arm, process)`
- **function `sample_singles`** [L117-119]: `def sample_singles(T, E, pi, scope, split, block, n, process=None) -> dict`
- **function `sample_pairs`** [L122-126]: `def sample_pairs(T, E, pi, scope, split, block, n, process=None) -> dict`
- **function `history_table`** [L129-132]: `def history_table(canon32, ids, label, block) -> dict`
- **function `table_arrays`** [L135-137]: `def table_arrays(table) -> dict`
- **function `hist_name`** [L140-143]: `def hist_name(kind, block, dry=False) -> str`

