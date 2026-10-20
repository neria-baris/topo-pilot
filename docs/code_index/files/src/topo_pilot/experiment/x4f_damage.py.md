# `src/topo_pilot/experiment/x4f_damage.py`

- Source: [src/topo_pilot/experiment/x4f_damage.py](../../../../../../src/topo_pilot/experiment/x4f_damage.py)
- Kind: python
- Lines: 131

## Module docstring

> X4-F gates G3-G5 for one model: primary erasure, F-primary family, damage profiles, support
> (x4f-exec-v2 §5, §6, §8, §9). Validation regret is never computed here.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import apply_map, displacements, fit_oblique_eraser, mismatch_report, random_family, support_gate, support_report` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 8, via package root)
- `from .x4f_data import ModelData` -> [src/topo_pilot/experiment/x4f_data.py](x4f_data.py.md) (line 18, via relative)
- `from .x4f_gates import CONTROLS, G3_LINEAR, G3_RBF_LABEL, ValForward, gen, probe, rbf_probe` -> [src/topo_pilot/experiment/x4f_gates.py](x4f_gates.py.md) (line 19, via relative)

### External (third-party)

- `numpy` (lines 6)

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

- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 36, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 9, import)
- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 10, import)

## Top-level constants

- none

## Classes and functions

- **function `g3`** [L30-49]: `def g3(d: ModelData, wh, primary, checkpoint=lambda _: None) -> dict` - Primary eraser validity and post-erasure linear / RBF recoverability of m32.
- **function `_profile`** [L52-70]: `def _profile(d: ModelData, vf: ValForward, mu, M, base_q1: dict, d_primary_val, scale, checkpoint=lambda _: None) -> dict` - Damage profile of one map on validation (units kept separate).
- **function `g4`** [L73-119]: `def g4(d: ModelData, vf: ValForward, wh, primary, controls: dict, checkpoint=lambda _: None) -> tuple[dict, dict]` - F-primary construction plus damage profiles; returns (gate record, patched clouds).
- **function `g5`** [L122-131]: `def g5(d: ModelData, clouds: dict) -> dict` - Mahalanobis support of patched validation vectors (primary vs its F-primary family).

