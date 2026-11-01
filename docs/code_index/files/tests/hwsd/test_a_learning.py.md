# `tests/hwsd/test_a_learning.py`

- Source: [tests/hwsd/test_a_learning.py](../../../../../tests/hwsd/test_a_learning.py)
- Kind: python
- Lines: 156

## Module docstring

> Author A (job 0197): the learning measures and onsets' inputs (§2.4 a, §5.2 k_L/k_P; KD5; DRD7).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 24, via sys.path edit)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](../../tools/hwsd/hwsd_known.py.md) (line 25, via sys.path edit)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](../../tools/hwsd/hwsd_score.py.md) (line 26, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 27, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../../tools/hwsb/hwsb_eval.py.md) (line 28, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../../tools/hwsc/hwsc_records.py.md) (line 29, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 30, via unique basename)
- `from topo_pilot.prediction.metrics import LearningGate` -> [src/topo_pilot/prediction/metrics.py](../../src/topo_pilot/prediction/metrics.py.md) (line 104, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 11)
- `pathlib` (lines 12)
- `statistics` (lines 13)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `HERE`
- `REPO`

## Classes and functions

- **function `planted_q`** [L33-35]: `def planted_q(n=96, seed=21)`
- **function `run`** [L38-49]: `def run(monkeypatch, q, p, **kw)`
- **test `test_z_constants`** [L52-56]: `def test_z_constants()`
- **test `test_p_equals_q32_captured_one`** [L59-64]: `def test_p_equals_q32_captured_one(monkeypatch)`
- **test `test_p_equals_q1_captured_zero`** [L67-70]: `def test_p_equals_q1_captured_zero(monkeypatch)`
- **test `test_p_equals_q4_no_beyond_four_gain`** [L73-77]: `def test_p_equals_q4_no_beyond_four_gain(monkeypatch)`
- **test `test_pass_through_of_b1_and_forcing`** [L80-92]: `def test_pass_through_of_b1_and_forcing(monkeypatch)`
- **test `test_explicit_z_arguments`** [L95-100]: `def test_explicit_z_arguments(monkeypatch)`
- **test `test_captured_exactly_four_fifths_passes`** [L103-118]: `def test_captured_exactly_four_fifths_passes(monkeypatch)`
- **test `test_learn_pass_reads_status_only`** [L121-131]: `def test_learn_pass_reads_status_only(monkeypatch)`
- **test `test_no_context_gain_is_numerical`** [L134-139]: `def test_no_context_gain_is_numerical(monkeypatch)`
- **test `test_nan_predictive_is_numerical`** [L142-150]: `def test_nan_predictive_is_numerical(monkeypatch)`
- **test `test_kd5_passes_on_w0`** [L154-156]: `def test_kd5_passes_on_w0()` decorators: @pytest.mark.slow

