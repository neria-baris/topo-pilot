# `src/topo_pilot/process/__init__.py`

- Source: [src/topo_pilot/process/__init__.py](../../../../../../src/topo_pilot/process/__init__.py)
- Kind: python
- Lines: 24

## Module docstring

> Public API of `topo_pilot.process` (see SPEC.md and README.md).

## Imports

### Internal (repo files)

- `from .centers import CENTER_REGISTRY, CenterStrategy, FPSCenters, GridCenters` -> [src/topo_pilot/process/centers.py](centers.py.md) (line 3, via relative)
- `from .conductance import ConductanceConfig, conductance_kernel, warp_profile` -> [src/topo_pilot/process/conductance.py](conductance.py.md) (line 4, via relative)
- `from .emission import EMISSION_REGISTRY, AxisPermuted, EmissionConfig, EmissionModel, FullPermuted, Identical, OverlapGaussian, Unique` -> [src/topo_pilot/process/emission.py](emission.py.md) (line 5, via relative)
- `from .stage import ProcessStage` -> [src/topo_pilot/process/stage.py](stage.py.md) (line 15, via relative)
- `from .transition import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/transition.py](transition.py.md) (line 16, via relative)

### External (third-party)

- none

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

- [src/topo_pilot/experiment/s1.py](../experiment/s1.py.md) (line 27, import)
- [src/topo_pilot/experiment/s2.py](../experiment/s2.py.md) (line 44, import)
- [src/topo_pilot/experiment/x5g1_run.py](../experiment/x5g1_run.py.md) (line 33, import)
- [src/topo_pilot/experiment/x5g1_verify.py](../experiment/x5g1_verify.py.md) (line 40, import)
- [tests/hws/test_b_exact.py](../../../tests/hws/test_b_exact.py.md) (line 32, import)
- [tests/hws/test_b_kc1.py](../../../tests/hws/test_b_kc1.py.md) (line 44, import)
- [tests/hws/test_b_worlds.py](../../../tests/hws/test_b_worlds.py.md) (line 31, import)
- [tests/process/test_conductance.py](../../../tests/process/test_conductance.py.md) (line 27, import)
- [tests/process/test_controls.py](../../../tests/process/test_controls.py.md) (line 19, import)
- [tests/process/test_overlap.py](../../../tests/process/test_overlap.py.md) (line 11, import)
- [tests/process/test_transition.py](../../../tests/process/test_transition.py.md) (line 12, import)
- [tools/check_process_rebuild.py](../../../tools/check_process_rebuild.py.md) (line 26, import)
- [tools/d1_seam/d1_seam.py](../../../tools/d1_seam/d1_seam.py.md) (line 19, import)
- [tools/hws/hws_exact.py](../../../tools/hws/hws_exact.py.md) (line 27, import)
- [tools/hws/hws_known.py](../../../tools/hws/hws_known.py.md) (line 27, import)
- [tools/hws/hws_records.py](../../../tools/hws/hws_records.py.md) (line 27, import)
- [tools/hws/hws_worlds.py](../../../tools/hws/hws_worlds.py.md) (line 28, import)
- [tools/hws/hws_worlds.py](../../../tools/hws/hws_worlds.py.md) (line 29, import)
- [tools/hwsb/hwsb_config.py](../../../tools/hwsb/hwsb_config.py.md) (line 29, import)
- [tools/hwsb/hwsb_dry.py](../../../tools/hwsb/hwsb_dry.py.md) (line 45, import)
- [tools/hwsb/hwsb_dry2.py](../../../tools/hwsb/hwsb_dry2.py.md) (line 34, import)
- [tools/theory_exact/theory_exact.py](../../../tools/theory_exact/theory_exact.py.md) (line 16, import)
- [tools/theory_exact/theory_exact2.py](../../../tools/theory_exact/theory_exact2.py.md) (line 24, import)
- [tools/x2a_stage0/x2a_model.py](../../../tools/x2a_stage0/x2a_model.py.md) (line 25, import)
- [tools/x6_stage0/x6_model.py](../../../tools/x6_stage0/x6_model.py.md) (line 24, import)

## Top-level constants

- none

## Classes and functions

- none

