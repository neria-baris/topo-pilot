# `tests/experiment/test_x5g1_scorebench_smoke.py`

- Source: [tests/experiment/test_x5g1_scorebench_smoke.py](../../../../../tests/experiment/test_x5g1_scorebench_smoke.py)
- Kind: python
- Lines: 52

## Module docstring

> Builder smoke tests for the scoring-only correction (x5g1-techbench-scoring-v2).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.experiment import x5g1_scorebench` -> [src/topo_pilot/experiment/x5g1_scorebench.py](../../src/topo_pilot/experiment/x5g1_scorebench.py.md) (line 8, via package root)
- `from topo_pilot.experiment.x5g1t_score import kl_from_log_probs, p32_log_probs, regret_rows` -> [src/topo_pilot/experiment/x5g1t_score.py](../../src/topo_pilot/experiment/x5g1t_score.py.md) (line 9, via package root)
- `from topo_pilot.learner import ModelConfig, TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)
- `torch` (lines 5)

### Standard library

- none

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

- `TINY`

## Classes and functions

- **test `test_projection_replaces_only_scoring_terms`** [L15-23]: `def test_projection_replaces_only_scoring_terms()`
- **test `test_fixture_is_seedtree_only_and_positive`** [L26-31]: `def test_fixture_is_seedtree_only_and_positive(monkeypatch)`
- **test `test_batched_scoring_equals_single_pass`** [L34-45]: `def test_batched_scoring_equals_single_pass()`
- **test `test_kl_zero_and_support_rules`** [L48-52]: `def test_kl_zero_and_support_rules()`

