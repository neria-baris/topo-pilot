# `src/topo_pilot/experiment/config.py`

- Source: [src/topo_pilot/experiment/config.py](../../../../../../src/topo_pilot/experiment/config.py)
- Kind: python
- Lines: 82

## Module docstring

> Layered config loading: base.yaml -> stages.yaml -> local.yaml (untracked).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)

### External (third-party)

- `yaml` (lines 12)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 7)
- `dataclasses` (lines 8)
- `hashlib` (lines 5)
- `pathlib` (lines 9)
- `subprocess` (lines 6)
- `typing` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/__init__.py](__init__.py.md) (line 12, import)
- [src/topo_pilot/experiment/circ_audit.py](circ_audit.py.md) (line 43, import)
- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 22, import)
- [src/topo_pilot/experiment/prereg.py](prereg.py.md) (line 27, import)
- [src/topo_pilot/experiment/s1.py](s1.py.md) (line 31, import)
- [src/topo_pilot/experiment/s2.py](s2.py.md) (line 46, import)
- [src/topo_pilot/experiment/s3.py](s3.py.md) (line 41, import)
- [src/topo_pilot/experiment/s4.py](s4.py.md) (line 20, import)
- [src/topo_pilot/experiment/s6.py](s6.py.md) (line 48, import)
- [src/topo_pilot/experiment/s7.py](s7.py.md) (line 35, import)
- [src/topo_pilot/experiment/s7_circular.py](s7_circular.py.md) (line 29, import)
- [src/topo_pilot/experiment/s7_controls.py](s7_controls.py.md) (line 27, import)
- [src/topo_pilot/experiment/s7_dev.py](s7_dev.py.md) (line 36, import)
- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 7, import)
- [src/topo_pilot/experiment/s7_probes.py](s7_probes.py.md) (line 27, import)
- [src/topo_pilot/experiment/s7_sensitivity.py](s7_sensitivity.py.md) (line 28, import)
- [src/topo_pilot/experiment/s8.py](s8.py.md) (line 54, import)
- [src/topo_pilot/experiment/stages.py](stages.py.md) (line 26, import)
- [src/topo_pilot/experiment/x4.py](x4.py.md) (line 39, import)
- [src/topo_pilot/experiment/x4_inputs.py](x4_inputs.py.md) (line 32, import)
- [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 28, import)
- [src/topo_pilot/experiment/x4b2_run.py](x4b2_run.py.md) (line 35, import)
- [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 35, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 32, import)
- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 28, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 35, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 42, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 35, import)
- [tests/experiment/test_runner.py](../../../tests/experiment/test_runner.py.md) (line 20, import)

## Top-level constants

- none

## Classes and functions

- **class `ResolvedConfig`** [L18-45] decorators: @dataclass(frozen=True) - The resolved configuration of one invocation.
- **method `ResolvedConfig.config_hash`** [L33-35]: `def config_hash(self) -> str` decorators: @property
- **method `ResolvedConfig.stage`** [L37-39]: `def stage(self, stage_id: str) -> Mapping[str, Any]` - The settings block of ``stage_id`` (empty if absent).
- **method `ResolvedConfig.artifact_root`** [L42-45]: `def artifact_root(self) -> Path` decorators: @property - Store root: ``local.yaml: artifact_root`` if set, else ``<repo>/artifacts``.
- **function `_read_yaml`** [L48-58]: `def _read_yaml(path: Path, required: bool) -> dict[str, Any]`
- **function `load_config`** [L61-68]: `def load_config(stages_path: Path, repo_root: Path | None = None) -> ResolvedConfig` - Read ``base.yaml`` and ``local.yaml`` from the folder of ``stages_path``.
- **function `producer_version`** [L71-82]: `def producer_version(repo_root: Path) -> str` - ``<git sha>`` plus ``+dirty`` when the work tree has uncommitted changes; ``unknown``

