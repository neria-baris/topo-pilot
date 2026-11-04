# `tests/hwsg/test_a_law.py`

- Source: [tests/hwsg/test_a_law.py](../../../../../tests/hwsg/test_a_law.py)
- Kind: python
- Lines: 181

## Module docstring

> Author A (job 0224): process override and law bound per sigma (O1/O2/O3; KG5; DRG8).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 24, via sys.path edit)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](../../tools/hwsg/hwsg_oracle.py.md) (line 25, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 26, via sys.path edit)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../../tools/hwsb/hwsb_law.py.md) (line 27, via sys.path edit)
- `import hws_exact` -> [tools/hws/hws_exact.py](../../tools/hws/hws_exact.py.md) (line 28, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 29, via sys.path edit)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 30, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 13)
- `hashlib` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hws`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`, `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `C`
- `DUMMY`
- `NEIGHBOUR`
- `REPO`
- `ROOT`
- `TAGS`
- `_ERR`
- `_PROCS`

## Classes and functions

- **function `_imports`** [L42-44]: `def _imports()` decorators: @pytest.fixture(autouse=True)
- **function `_status`** [L47-52]: `def _status(fn, *a, **k)`
- **function `_proc`** [L58-61]: `def _proc(tag)`
- **test `test_neighbour_rule_exact`** [L64-69]: `def test_neighbour_rule_exact()`
- **test `test_build_process_g_overrides_exact`** [L73-77]: `def test_build_process_g_overrides_exact(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_identity_refuses_float_repr_neighbour`** [L80-85]: `def test_identity_refuses_float_repr_neighbour()`
- **test `test_law_per_sigma`** [L89-96]: `def test_law_per_sigma(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_law_F_plan_above_max_fails`** [L99-101]: `def test_law_F_plan_above_max_fails(monkeypatch)`
- **test `test_law_Z_off_by_one_numerator_fails`** [L104-114]: `def test_law_Z_off_by_one_numerator_fails(monkeypatch)`
- **test `test_law_nonbounded_fails`** [L117-121]: `def test_law_nonbounded_fails(monkeypatch)`
- **test `test_w_star_law_equals_handoff`** [L124-134]: `def test_w_star_law_equals_handoff()`
- **test `test_sigma_5_4_enclosure_delta_zero`** [L137-149]: `def test_sigma_5_4_enclosure_delta_zero()` - DRG8: at sigma 5/4 the rounded enclosure equals process_law.softmax_enclosure (delta 0).
- **function `_boundary_p`** [L155-162]: `def _boundary_p()` - Largest float p with 22528 * Fraction(p) <= 1/100 (independent search).
- **test `test_d2a_boundary_passes`** [L168-173]: `def test_d2a_boundary_passes(monkeypatch)`
- **test `test_d2a_above_fails`** [L176-181]: `def test_d2a_above_fails(monkeypatch)`

