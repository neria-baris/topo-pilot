# `tools/x2a_stage0/x2a_model.py`

- Source: [tools/x2a_stage0/x2a_model.py](../../../../../tools/x2a_stage0/x2a_model.py)
- Kind: python
- Lines: 360

## Module docstring

> X2a stage 0, part 1 (X2A-FROZEN-v1; API.md): construction, exact k <= 4 enumeration, closed
> forms, stencil filter, gates G0-G2. Local unregistered torus builder; point_distances is never
> called.

## Imports

### Internal (repo files)

- `from oracle_profile import validate_process` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 21, via sys.path edit)
- `import topo_pilot.world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 24, via package root)
- `from topo_pilot.process import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 25, via package root)
- `from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 26, via package root)
- `from topo_pilot.world.complex import check_boundary_closed` -> [src/topo_pilot/world/complex.py](../../src/topo_pilot/world/complex.py.md) (line 27, via package root)
- `from topo_pilot.world.metrics import check_flat_bounds` -> [src/topo_pilot/world/metrics.py](../../src/topo_pilot/world/metrics.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 14)
- `scipy` (lines 22)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `math` (lines 7)
- `pathlib` (lines 11)
- `subprocess` (lines 8)
- `sys` (lines 9)
- `typing` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/x2a_stage0`, `tools/x4_oracle_profile`

## Imported by

- [tests/x2a_stage0/test_x2a_stage0.py](../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 37, import)
- [tools/x2a_stage0/x2a_mc.py](x2a_mc.py.md) (line 15, import)
- [tools/x2a_stage0/x2a_ph.py](x2a_ph.py.md) (line 17, import)

## Top-level constants

- `BASE_COMMIT`
- `EXACT_VARIANTS`
- `HAND`
- `LN2`
- `PROTOCOL_SHA256`
- `REPO`
- `REQUEST_SHA256`
- `VARIANTS`
- `_EXTRA`

## Classes and functions

- **function `state`** [L48-49]: `def state(x, y)`
- **function `token`** [L51-52]: `def token(a, b)`
- **function `delta12`** [L54-56]: `def delta12(u, v)`
- **class `_X2aTorusBuilder(tw.QuotientLatticeBuilder)`** [L58-62]
- **function `build_world`** [L64-69]: `def build_world()`
- **function `kernel`** [L71-72]: `def kernel(spec)`
- **function `field_e`** [L74-77]: `def field_e()`
- **function `emission_A`** [L79-81]: `def emission_A(e=None)`
- **function `_perm`** [L83-84]: `def _perm(dx_of)`
- **function `dehn_perm`** [L86-87]: `def dehn_perm()`
- **function `iso_perm`** [L89-90]: `def iso_perm()`
- **function `emission_local`** [L92-93]: `def emission_local(E_A)`
- **function `emission_pref`** [L95-98]: `def emission_pref(spec, E_A)`
- **function `mixture`** [L100-103]: `def mixture(T, E1, E2)`
- **function `variant_model`** [L105-121]: `def variant_model(variant, spec=None)`
- **function `window_law`** [L124-132]: `def window_law(T, E, k)`
- **function `js_phi`** [L134-144]: `def js_phi(r)`
- **function `js_information`** [L146-152]: `def js_information(PA, PB)`
- **function `bayes_accuracy`** [L154-155]: `def bayes_accuracy(PA, PB)`
- **function `exact_curve`** [L157-163]: `def exact_curve(T, E1, E2, kmax=4)`
- **function `G_overlap`** [L165-166]: `def G_overlap(e, d)`
- **function `delta_rep_closed`** [L168-169]: `def delta_rep_closed(e)`
- **function `pair_law`** [L171-172]: `def pair_law(T, E)`
- **function `_stencil`** [L175-187]: `def _stencil(E, tok)`
- **function `stencil_filter`** [L189-195]: `def stencil_filter(E1, E2, tokens)`
- **function `_status`** [L198-199]: `def _status(checks)`
- **function `_fraction_T`** [L201-204]: `def _fraction_T()`
- **function `gate_G0`** [L206-233]: `def gate_G0(spec, T)`
- **function `_brute_E_A`** [L235-243]: `def _brute_E_A()`
- **function `gate_G1`** [L245-283]: `def gate_G1(models)`
- **function `_translate`** [L285-291]: `def _translate(law, k, da, db)`
- **function `_hand`** [L293-310]: `def _hand(models)`
- **function `gate_G2`** [L312-346]: `def gate_G2(models)`
- **function `_git`** [L349-351]: `def _git(*args)`
- **function `_jsonable`** [L353-360]: `def _jsonable(x)`

