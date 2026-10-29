# `tests/hwsc/test_a_ladder.py`

- Source: [tests/hwsc/test_a_ladder.py](../../../../../tests/hwsc/test_a_ladder.py)
- Kind: python
- Lines: 277

## Module docstring

> Author A (job 0176): the P1 ladder, the N rule and the registry-risk check.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 23, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 24, via sys.path edit)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md) (line 25, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 26, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 27, via unique basename)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 28, via unique basename)
- `import hws_exact` -> [tools/hws/hws_exact.py](../../tools/hws/hws_exact.py.md) (line 29, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 30, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 31, via unique basename)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `math` (lines 10)
- `pathlib` (lines 13)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `ALPHA`
- `CASES`
- `F_PLAN`
- `HV`
- `LADDER`
- `M`
- `MODELS`
- `N_ROWS`
- `REPO`
- `_CACHE`
- `_HWSC`

## Classes and functions

- **function `planted`** [L42-53]: `def planted(sd, seed, n=N_ROWS)` - Three strongly correlated models (shared base), small width on 10% of rows.
- **function `deq`** [L56-67]: `def deq(a, b)`
- **function `get`** [L70-71]: `def get(d, j)`
- **function `reference`** [L74-108]: `def reference(Xm, Xp, r4n, F, seeds=(620311, 620315))` - Independent re-implementation of K4B §7.1-§7.2 for the stage-C keys.
- **function `run_case`** [L115-123]: `def run_case(name)`
- **test `test_p1c_equals_ladder_pilot_and_reference`** [L127-149]: `def test_p1c_equals_ladder_pilot_and_reference(name)` decorators: @pytest.mark.parametrize('name', list(CASES))
- **test `test_seed_sensitive_fixture`** [L152-157]: `def test_seed_sensitive_fixture()`
- **test `test_p1c_inside_binding_equal`** [L160-164]: `def test_p1c_inside_binding_equal()`
- **test `test_projection_invariant_to_mean_shift`** [L167-177]: `def test_projection_invariant_to_mean_shift()`
- **test `test_choose_N_max`** [L185-190]: `def test_choose_N_max(N_C, N_P1)` decorators: @pytest.mark.parametrize('N_C', [3072, 6144]) @pytest.mark.parametrize('N_P1', [3072, 6144, 12288])
- **test `test_choose_N_underpowered`** [L194-197]: `def test_choose_N_underpowered(N_C)` decorators: @pytest.mark.parametrize('N_C', [3072, 6144, 12288])
- **test `test_choose_N_off_ladder`** [L201-204]: `def test_choose_N_off_ladder(N_C, N_P1)` decorators: @pytest.mark.parametrize('N_C, N_P1', [(5000, 3072), (24576, 3072), (9216, 6144)])
- **function `rows`** [L210-211]: `def rows(N)`
- **test `test_registry_risk_value_exact`** [L215-222]: `def test_registry_risk_value_exact(N)` decorators: @pytest.mark.parametrize('N', LADDER)
- **test `test_registry_risk_desk_value`** [L225-228]: `def test_registry_risk_desk_value()`
- **test `test_registry_risk_boundary`** [L232-245]: `def test_registry_risk_boundary(N)` decorators: @pytest.mark.parametrize('N', LADDER)
- **function `proc_stub`** [L251-252]: `def proc_stub()`
- **test `test_p_d2a_check_tolerance`** [L255-268]: `def test_p_d2a_check_tolerance(monkeypatch)`
- **test `test_p_d2a_check_handoff_value`** [L271-277]: `def test_p_d2a_check_handoff_value(monkeypatch)`

