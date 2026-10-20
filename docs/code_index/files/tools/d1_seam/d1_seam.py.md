# `tools/d1_seam/d1_seam.py`

- Source: [tools/d1_seam/d1_seam.py](../../../../../tools/d1_seam/d1_seam.py)
- Kind: python
- Lines: 400

## Module docstring

> D-1 seam check part 1 (D1-FROZEN-v1; API.md): model, kernels, enumerator, G0-G3. G4-G6 and run
> are in d1_seam_checks.py (addendum 2). Local unregistered Möbius builder; no point_distances.

## Imports

### Internal (repo files)

- `import topo_pilot.world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 18, via package root)
- `from topo_pilot.process import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 19, via package root)
- `from topo_pilot.world.complex import check_boundary_closed, rank_mod_p` -> [src/topo_pilot/world/complex.py](../../src/topo_pilot/world/complex.py.md) (line 20, via package root)
- `from topo_pilot.world.metrics import check_flat_bounds` -> [src/topo_pilot/world/metrics.py](../../src/topo_pilot/world/metrics.py.md) (line 21, via package root)
- `from d1_seam_checks import gate_G4, gate_G5, gate_G6, run` -> [tools/d1_seam/d1_seam_checks.py](d1_seam_checks.py.md) (line 400, via same directory)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 4)
- `decimal` (lines 7)
- `fractions` (lines 8)
- `pathlib` (lines 9)
- `sys` (lines 6)
- `typing` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/d1_seam`

## Imported by

- [tests/d1_seam/test_d1_seam.py](../../tests/d1_seam/test_d1_seam.py.md) (line 29, import)
- [tests/d2a/test_a_pad.py](../../tests/d2a/test_a_pad.py.md) (line 25, import)
- [tests/d2a/test_a_targets.py](../../tests/d2a/test_a_targets.py.md) (line 28, import)
- [tests/d2a/test_a_templates.py](../../tests/d2a/test_a_templates.py.md) (line 25, import)
- [tests/d2a/test_a_world.py](../../tests/d2a/test_a_world.py.md) (line 24, import)
- [tests/d2a/test_b_targets.py](../../tests/d2a/test_b_targets.py.md) (line 26, import)
- [tests/learner/test_trainer_golden.py](../../tests/learner/test_trainer_golden.py.md) (line 42, import)
- [tools/d1_seam/d1_seam_checks.py](d1_seam_checks.py.md) (line 16, import)
- [tools/d2a/d2a_world.py](../d2a/d2a_world.py.md) (line 28, import)

## Top-level constants

- `EXP`
- `JC_STAR`
- `JM_STAR`
- `LITERAL_E`
- `Q1_HI`
- `REPO`
- `VARIANTS`
- `_EXTRA`
- `_JROWS`

## Classes and functions

- **function `st`** [L37-37]: `def st(x, y)`
- **function `_R`** [L38-38]: `def _R(s)`
- **function `_seam`** [L39-39]: `def _seam(i, j)`
- **function `_nb`** [L40-40]: `def _nb(T)`
- **function `_vec`** [L41-41]: `def _vec(d, n=NS)`
- **function `_q2d`** [L42-42]: `def _q2d(J)`
- **function `_delta`** [L43-43]: `def _delta(b)`
- **function `_dln`** [L44-44]: `def _dln(x)`
- **function `edge_set`** [L46-49]: `def edge_set(world)`
- **function `exact_world_T`** [L51-54]: `def exact_world_T(world)`
- **function `exact_E`** [L56-62]: `def exact_E(variant='frozen')`
- **function `exact_model`** [L64-71]: `def exact_model(variant='frozen')`
- **class `_D1MobiusBuilder(tw.QuotientLatticeBuilder)`** [L73-76]
- **function `build_worlds`** [L78-84]: `def build_worlds()`
- **function `float_model`** [L86-93]: `def float_model(worlds=None)`
- **function `_step`** [L95-102]: `def _step(al, nb, E, w, emit=None)`
- **function `_q1`** [L104-104]: `def _q1(al, nb, E)`
- **function `_J`** [L105-105]: `def _J(b, nb, E)`
- **function `_norm`** [L107-109]: `def _norm(al)`
- **function `_mix`** [L111-114]: `def _mix(p, q, pi)`
- **function `tv`** [L116-119]: `def tv(p, q)`
- **function `parity_profile`** [L121-126]: `def parity_profile(h)`
- **function `exact_history`** [L128-146]: `def exact_history(history, variant='frozen', model=None)`
- **function `_nodes`** [L148-168]: `def _nodes(m, K)` - Depth-first reachable histories: C, M, reflected-C (Theorem C(b)) and 24-state passes.
- **function `gate_G2`** [L170-225]: `def gate_G2(variant='frozen', K=K_DEPTH)`
- **function `_gate`** [L227-228]: `def _gate(ck, values)`
- **function `gate_G0`** [L230-261]: `def gate_G0(worlds, E_mix=None)`
- **function `_components`** [L263-268]: `def _components(n, pairs)` - Number of connected components of a graph on range(n) (reachability by matrix power).
- **function `_complex`** [L270-273]: `def _complex(w)`
- **function `gate_G0S`** [L275-294]: `def gate_G0S(worlds)`
- **function `gate_G0O`** [L296-322]: `def gate_G0O(worlds)`
- **function `gate_G1`** [L324-349]: `def gate_G1(variant='frozen')`
- **function `_kl`** [L355-357]: `def _kl(P, Q)`
- **function `gate_G3`** [L359-398]: `def gate_G3()`

