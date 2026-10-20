# `src/topo_pilot/experiment/x5g1_safety.py`

- Source: [src/topo_pilot/experiment/x5g1_safety.py](../../../../../../src/topo_pilot/experiment/x5g1_safety.py)
- Kind: python
- Lines: 84

## Module docstring

> X5 G1 audit repairs (job 0007): full-hash source verification before and after computation,
> STOP/budget-guarded exports and immutable output directories.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)
- `from .x5g1_controls import BudgetExceeded, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 13, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `collections` (lines 7)
- `json` (lines 6)
- `pathlib` (lines 8)
- `typing` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 34, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 45, import)
- [src/topo_pilot/experiment/x5g1_scorebench.py](x5g1_scorebench.py.md) (line 38, import)
- [src/topo_pilot/experiment/x5g1_techbench.py](x5g1_techbench.py.md) (line 30, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 48, import)
- [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 15, import)
- [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 27, import)
- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 23, import)
- [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 24, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 39, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 43, import)
- [tests/experiment/test_x5g1_safety.py](../../../tests/experiment/test_x5g1_safety.py.md) (line 24, import)
- [tests/experiment/test_x5g1_smoke.py](../../../tests/experiment/test_x5g1_smoke.py.md) (line 9, import)
- [tests/experiment/test_x5g1_techbench_smoke.py](../../../tests/experiment/test_x5g1_techbench_smoke.py.md) (line 8, import)
- [tests/experiment/test_x5g1t_runtime_boundary.py](../../../tests/experiment/test_x5g1t_runtime_boundary.py.md) (line 27, import)

## Top-level constants

- `T`

## Classes and functions

- **class `OutputExists(FileExistsError)`** [L18-19] - A completed output version already exists; it is never overwritten.
- **class `SourceTampered(RuntimeError)`** [L22-23] - A source artifact failed full-hash or payload verification.
- **function `verify_sources_full`** [L26-40]: `def verify_sources_full(store: ArtifactStore, expected: dict[str, tuple[type, str]], consumer: str = 'experiment') -> list[str]` - Failures for artifacts whose metadata hash differs from the full expected hash or whose
- **function `checked_computation`** [L43-54]: `def checked_computation(store: ArtifactStore, expected: dict[str, tuple[type, str]], fn: Callable[[], T]) -> T` - Verify sources, run ``fn``, verify again; any failure raises ``SourceTampered`` and an
- **function `ensure_new_output_dir`** [L57-63]: `def ensure_new_output_dir(path: Path) -> Path` - Create ``path``; refuse (``OutputExists``) if it already holds anything.
- **function `guarded_export`** [L66-84]: `def guarded_export(ctl: RunControls, steps: list[tuple[str, Callable[[], None]]], status_path: Path) -> None` - Run export steps with guards before and after each; on STOP/budget write only a small

