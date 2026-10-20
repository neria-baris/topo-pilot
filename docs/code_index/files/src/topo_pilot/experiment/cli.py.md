# `src/topo_pilot/experiment/cli.py`

- Source: [src/topo_pilot/experiment/cli.py](../../../../../../src/topo_pilot/experiment/cli.py)
- Kind: python
- Lines: 139

## Module docstring

> The ``topo-pilot`` command line (W0 skeleton: ``status`` and ``stage``).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ARTIFACT_CLASSES, ArtifactMeta, ArtifactStore, GateReport, LocalFSBackend, MetricRecords, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from .config import ResolvedConfig, load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 22, via relative)
- `from .prereg import write_prereg` -> [src/topo_pilot/experiment/prereg.py](prereg.py.md) (line 23, via relative)
- `from .report import build_e0` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 24, via relative)
- `from .report_e2 import build_e2` -> [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 25, via relative)
- `from .report_e3 import build_e3` -> [src/topo_pilot/experiment/report_e3.py](report_e3.py.md) (line 26, via relative)
- `from .report_e4 import build_e4` -> [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 27, via relative)
- `from .report_x4 import x4_section` -> [src/topo_pilot/experiment/report_x4.py](report_x4.py.md) (line 28, via relative)
- `from .stages import STAGE_REGISTRY, run_stage` -> [src/topo_pilot/experiment/stages.py](stages.py.md) (line 29, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `argparse` (lines 5)
- `collections` (lines 9)
- `json` (lines 6)
- `logging` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/__init__.py](__init__.py.md) (line 11, import)
- [src/topo_pilot/experiment/s8.py](s8.py.md) (line 206, import)

## Top-level constants

- `MAX_STATUS_LINES`

## Classes and functions

- **function `open_store`** [L34-37]: `def open_store(cfg: ResolvedConfig) -> ArtifactStore` - The local artifact store at ``cfg.artifact_root`` (created on first write).
- **function `status_lines`** [L40-63]: `def status_lines(cfg: ResolvedConfig, store: ArtifactStore) -> list[str]` - At most 40 lines: artifact counts per type, the latest verdict per gate, config hash.
- **function `build_reports`** [L66-85]: `def build_reports(level: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[Path]` - Write the report(s) for ``level``; ``all`` skips E2 / E3 / E4 until an S4 / S5
- **function `_parser`** [L88-106]: `def _parser() -> argparse.ArgumentParser`
- **function `main`** [L109-135]: `def main(argv: list[str] | None = None) -> int` - Entry point. Exit codes: 0 ok, 1 ``StageFailure``, 2 usage error.

