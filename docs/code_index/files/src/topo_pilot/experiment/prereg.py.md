# `src/topo_pilot/experiment/prereg.py`

- Source: [src/topo_pilot/experiment/prereg.py](../../../../../../src/topo_pilot/experiment/prereg.py)
- Kind: python
- Lines: 164

## Module docstring

> ``topo-pilot prereg``: write PREREGISTRATION.md from S2 outputs and base.yaml (H1 draft).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, GateReport, MetricRecords, MetricRow, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 18, via package root)
- `from .config import ResolvedConfig, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 27, via relative)

### External (third-party)

- `yaml` (lines 16)

### Standard library

- `__future__` (lines 8)
- `collections` (lines 12)
- `datetime` (lines 13)
- `pathlib` (lines 14)
- `re` (lines 10)
- `statistics` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 23, import)
- [tests/experiment/test_runner.py](../../../tests/experiment/test_runner.py.md) (line 21, import)

## Top-level constants

- `S2_GATES`
- `SPACES`

## Classes and functions

- **function `_section`** [L33-38]: `def _section(text: str, heading: str) -> str` - The markdown block starting at ``heading`` up to the next heading of the same level.
- **function `_demote`** [L41-43]: `def _demote(text: str) -> str` - Embed a copied section one heading level deeper, so its headings nest under ours.
- **function `_s2_rows`** [L46-50]: `def _s2_rows(store: ArtifactStore) -> list[MetricRow]`
- **function `_gates`** [L53-58]: `def _gates(store: ArtifactStore) -> dict[str, GateReport]`
- **function `sigma_table`** [L61-69]: `def sigma_table(rows: list[MetricRow]) -> list[str]`
- **function `disc_table`** [L72-112]: `def disc_table(rows: list[MetricRow], n_panels: int) -> list[str]` - Median S over panels per space × world × condition, and panels with S_cyl > S_sq.
- **function `write_prereg`** [L115-164]: `def write_prereg(cfg: ResolvedConfig, store: ArtifactStore, conductor_note: str = '', force: bool = False) -> Path` - Write ``PREREGISTRATION.md`` at the repository root; returns its path.

