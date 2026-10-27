# `tests/hwsb/test_b_hold.py`

- Source: [tests/hwsb/test_b_hold.py](../../../../../tests/hwsb/test_b_hold.py)
- Kind: python
- Lines: 192

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_hold.py`: the hold rule (section 8.2, RC-14,
> X-2; DRB14): `hold_check` boundaries and triggers, `HoldRule` files and decisions with a planted
> CPU function and a fake sleep, and tiny trainings held at step 10. tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 19, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 20, via sys.path edit)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 21, via sys.path edit)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../../tools/hwsb/hwsb_train.py.md) (line 22, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 24, via package root)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 5)
- `dataclasses` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 9)
- `time` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `MASTER`
- `REFUSE`
- `REPO`

## Classes and functions

- **test `test_contract_hold_numbers`** [L32-34]: `def test_contract_hold_numbers()`
- **test `test_no_projection_before_step_1000`** [L37-40]: `def test_no_projection_before_step_1000()`
- **test `test_projection_at_step_1000_is_cpu_times_five`** [L43-47]: `def test_projection_at_step_1000_is_cpu_times_five()`
- **test `test_exactly_7275_does_not_hold_and_just_above_holds`** [L50-57]: `def test_exactly_7275_does_not_hold_and_just_above_holds()`
- **test `test_both_trigger`** [L60-62]: `def test_both_trigger()`
- **test `test_custom_cap_steps_and_from_step`** [L65-68]: `def test_custom_cap_steps_and_from_step()`
- **class `FakeSleep`** [L72-87] - Counts calls; writes the decision file on the n-th call.
- **method `FakeSleep.__init__`** [L75-77]: `def __init__(self, out, step, decision, n=3, cpu_calls=None, cpu_log=None)`
- **method `FakeSleep.__call__`** [L79-87]: `def __call__(self, seconds)`
- **function `make_rule`** [L90-100]: `def make_rule(tmp_path, decision, step=10, **kw)`
- **test `test_no_hold_returns_none_and_writes_nothing`** [L103-105]: `def test_no_hold_returns_none_and_writes_nothing(tmp_path)`
- **test `test_hold_writes_report_without_dev_ce_and_continue_exempts`** [L108-121]: `def test_hold_writes_report_without_dev_ce_and_continue_exempts(tmp_path)`
- **test `test_stop_ends_inconclusive`** [L124-129]: `def test_stop_ends_inconclusive(tmp_path)`
- **test `test_unknown_or_unreadable_decision_is_hold_failure`** [L133-137]: `def test_unknown_or_unreadable_decision_is_hold_failure(tmp_path, decision)` decorators: @pytest.mark.parametrize('decision', ['MAYBE', '{not json'])
- **test `test_hold_report_refuses_overwrite`** [L140-145]: `def test_hold_report_refuses_overwrite(tmp_path)`
- **function `plan20`** [L149-156]: `def plan20()`
- **function `world`** [L159-163]: `def world(plan)`
- **function `steps_in`** [L166-167]: `def steps_in(store)`
- **test `test_held_and_continued_run_equals_unheld_run_bitwise`** [L170-181]: `def test_held_and_continued_run_equals_unheld_run_bitwise(tmp_path)`
- **test `test_stop_at_a_hold_leaves_only_earlier_checkpoints`** [L184-192]: `def test_stop_at_a_hold_leaves_only_earlier_checkpoints(tmp_path)`

