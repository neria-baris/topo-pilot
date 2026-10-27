# `tests/hwsb/test_a_ladder.py`

- Source: [tests/hwsb/test_a_ladder.py](../../../../../tests/hwsb/test_a_ladder.py)
- Kind: python
- Lines: 293

## Module docstring

> HWSB author A: the B6 pilot ladder (protocol §4 B6, refinement 2; DRB9).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 30, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 31, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 32, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 33, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 34, via sys.path edit)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 37, via sys.path edit)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 38, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 15)
- `math` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 28: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `CASES`
- `LADDER`
- `M`
- `MISSING`
- `N_ROWS`
- `REPO`
- `SEEDS_B`
- `SEEDS_K4B`
- `STAGE_B`

## Classes and functions

- **function `need`** [L55-57]: `def need()`
- **function `F_plan`** [L60-61]: `def F_plan()`
- **function `planted`** [L64-74]: `def planted(models, sd, seed)` - Models share one base series (so the joint counts track the per-model ones).
- **function `ladder_ref`** [L77-116]: `def ladder_ref(Xm, Xp, r4n, F, models, seeds, ladder=LADDER)` - Independent §4 B6 rule (no k4b_stats code), width diagnostic omitted.
- **function `k4b_cases`** [L120-125]: `def k4b_cases()` decorators: @pytest.fixture(scope='module')
- **function `stage_b_cases`** [L129-134]: `def stage_b_cases()` decorators: @pytest.fixture(scope='module')
- **test `test_reference_cases_land_as_planted`** [L139-142]: `def test_reference_cases_land_as_planted(k4b_cases, stage_b_cases)`
- **test `test_reference_rule_equals_k4b_ladder`** [L145-157]: `def test_reference_rule_equals_k4b_ladder(k4b_cases)`
- **test `test_ladder_pilot_equals_k4b_ladder`** [L163-171]: `def test_ladder_pilot_equals_k4b_ladder(k4b_cases, name)` decorators: @pytest.mark.parametrize('name', list(CASES))
- **test `test_ladder_pilot_stage_b_rule`** [L177-194]: `def test_ladder_pilot_stage_b_rule(stage_b_cases, name)` decorators: @pytest.mark.parametrize('name', list(CASES))
- **test `test_ladder_pilot_defaults_are_stage_b`** [L197-205]: `def test_ladder_pilot_defaults_are_stage_b(stage_b_cases)`
- **test `test_ladder_pilot_width_diagnostic_with_d_bar`** [L208-225]: `def test_ladder_pilot_width_diagnostic_with_d_bar(stage_b_cases)`
- **function `boundary_sd`** [L230-245]: `def boundary_sd()` - A float sd with precision.mde(sd) == 0.02 exactly at N = 3,072, and Z_bound used.
- **test `test_reference_boundary_sd_exists`** [L248-251]: `def test_reference_boundary_sd_exists()`
- **test `test_mde_boundary_equality_passes`** [L255-276]: `def test_mde_boundary_equality_passes(monkeypatch, stage_b_cases, ulps_above, expected)` decorators: @pytest.mark.parametrize('ulps_above, expected', [(0, True), (1, False)])
- **test `test_b5_n_returns_ladder_n_or_fallback`** [L281-286]: `def test_b5_n_returns_ladder_n_or_fallback()`
- **test `test_b5_n_on_real_ladder_output`** [L289-293]: `def test_b5_n_on_real_ladder_output(stage_b_cases)`

