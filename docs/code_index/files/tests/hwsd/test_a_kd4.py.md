# `tests/hwsd/test_a_kd4.py`

- Source: [tests/hwsd/test_a_kd4.py](../../../../../tests/hwsd/test_a_kd4.py)
- Kind: python
- Lines: 195

## Module docstring

> Author A (job 0197): KD4 known-case fixtures (§6 KD4; API.md §12 plant_acts/seq_cases, §17.3).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 29, via sys.path edit)
- `import hwsd_dry` -> [tools/hwsd/hwsd_dry.py](../../tools/hwsd/hwsd_dry.py.md) (line 30, via sys.path edit)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](../../tools/hwsd/hwsd_statements.py.md) (line 31, via sys.path edit)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 32, via unique basename)
- `import test_a_hwsd_ref` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 33, via same directory)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 11)
- `hashlib` (lines 13)
- `json` (lines 14)
- `math` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 18)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `DRY`
- `HERE`
- `REPO`
- `TWO_PI`

## Classes and functions

- **function `u_of`** [L39-40]: `def u_of(i)`
- **function `g_ref`** [L43-48]: `def g_ref(theta, a)` - API.md §12: [0, 2*pi*a) -> [0, pi/6) and [2*pi*a, 2*pi) -> [pi/6, 2*pi), linear.
- **function `fixture`** [L51-60]: `def fixture(n=256, seed=11)`
- **function `params`** [L63-66]: `def params(noise=0.0, g_mass=0.01)`
- **test `test_case_ids_and_sequences_are_the_protocol_ones`** [L70-76]: `def test_case_ids_and_sequences_are_the_protocol_ones()`
- **test `test_plant_acts_noise_free_matches_construction`** [L80-95]: `def test_plant_acts_noise_free_matches_construction(case)` decorators: @pytest.mark.parametrize('case', ['i', 'ii', 'iii', 'iv', 'v'])
- **test `test_plant_acts_case_iv_mass_in_first_arc`** [L98-108]: `def test_plant_acts_case_iv_mass_in_first_arc()`
- **test `test_plant_acts_noise_scale_and_seeds`** [L111-125]: `def test_plant_acts_noise_scale_and_seeds()`
- **test `test_kd4_sequence_readings_on_planted_rows`** [L130-141]: `def test_kd4_sequence_readings_on_planted_rows(name)` decorators: @pytest.mark.parametrize('name', list(ref.KD4_EXPECTED))
- **test `test_step0_control_reports_sigma_step0_and_k_C_plus`** [L144-150]: `def test_step0_control_reports_sigma_step0_and_k_C_plus()`
- **test `test_before_sequence_unvalidated_case_is_not_an_onset`** [L153-158]: `def test_before_sequence_unvalidated_case_is_not_an_onset()`
- **function `_kd4_params`** [L162-171]: `def _kd4_params()`
- **test `test_seq_cases_end_to_end`** [L175-195]: `def test_seq_cases_end_to_end(tmp_path)` decorators: @pytest.mark.slow

