# `src/topo_pilot/experiment/x5g1t_main.py`

- Source: [src/topo_pilot/experiment/x5g1t_main.py](../../../../../../src/topo_pilot/experiment/x5g1t_main.py)
- Kind: python
- Lines: 90

## Module docstring

> X5 G1 training-study CLI (x5g1-train-v4 §10; API v4 §6). Stages run separately so that the root
> can authorise pools/training/dev analysis first and the fresh test last.

## Imports

### Internal (repo files)

- `from .x5g1_controls import BudgetExceeded, LedgerCorrupt, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 22, via relative)
- `from .x5g1_safety import OutputExists` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 23, via relative)
- `from .x5g1t_checks import IntegrityFailed` -> [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 24, via relative)
- `from .x5g1t_config import ConfigInvalid, load_config, validate_config` -> [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 25, via relative)
- `from .x5g1t_exports import ExportIncomplete` -> [src/topo_pilot/experiment/x5g1t_exports.py](x5g1t_exports.py.md) (line 26, via relative)
- `from .x5g1t_fixture import build_fixture` -> [src/topo_pilot/experiment/x5g1t_fixture.py](x5g1t_fixture.py.md) (line 27, via relative)
- `from .x5g1t_runtime import ResourceExceeded, RunLocked` -> [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 28, via relative)
- `from .x5g1t_stages import StudyFailed, run_pools, run_train` -> [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 29, via relative)
- `from .x5g1t_stages_eval import run_dev_analysis, run_final_test` -> [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 30, via relative)
- `from .x5g1t_usage import UsageMalformed` -> [src/topo_pilot/experiment/x5g1t_usage.py](x5g1t_usage.py.md) (line 31, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 15)
- `argparse` (lines 17)
- `json` (lines 18)
- `logging` (lines 19)
- `pathlib` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x5g1t_e2e.py](../../../tests/experiment/test_x5g1t_e2e.py.md) (line 11, import)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 34, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 22, import)

## Top-level constants

- `REFUSALS`

## Classes and functions

- **function `_master`** [L39-40]: `def _master(text: str)`
- **function `main`** [L43-86]: `def main(argv: list[str] | None = None) -> int`

