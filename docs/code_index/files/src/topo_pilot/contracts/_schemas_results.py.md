# `src/topo_pilot/contracts/_schemas_results.py`

- Source: [src/topo_pilot/contracts/_schemas_results.py](../../../../../../src/topo_pilot/contracts/_schemas_results.py)
- Kind: python
- Lines: 261

## Module docstring

> Model, topology and result artifacts (DATA_SCHEMAS §5–§6).

## Imports

### Internal (repo files)

- `from . import _checks` -> [src/topo_pilot/contracts/_checks.py](_checks.py.md) (line 12, via relative)
- `from .base import Artifact, array_field, optional_array_field` -> [src/topo_pilot/contracts/base.py](base.py.md) (line 13, via relative)
- `from .errors import ErrorCode, Status` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 14, via relative)

### External (third-party)

- `numpy` (lines 10)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 6)
- `dataclasses` (lines 7)
- `math` (lines 5)
- `typing` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 13, import)

## Top-level constants

- `ACTIVATION_SOURCES`
- `GATE_VERDICTS`
- `STATUS_VALUES`

## Classes and functions

- **class `Checkpoint(Artifact)`** [L22-43] decorators: @dataclass(frozen=True, eq=False) - Model weights at one training step. ``state`` is an opaque ``torch.save`` blob stored as
- **method `Checkpoint.validate`** [L39-43]: `def validate(self) -> None`
- **class `ActivationSet(Artifact)`** [L47-84] decorators: @dataclass(frozen=True, eq=False) - Activations at the analysis position for M histories.
- **method `ActivationSet.validate`** [L66-84]: `def validate(self) -> None`
- **class `DistanceArtifact(Artifact)`** [L88-120] decorators: @dataclass(frozen=True, eq=False) - Pairwise distances after deduplication.
- **method `DistanceArtifact.validate`** [L107-120]: `def validate(self) -> None`
- **class `Diagrams(Artifact)`** [L124-157] decorators: @dataclass(frozen=True, eq=False) - Persistence diagrams: ``rows: [n, 4] float64`` with columns (dim, birth, death, censored).
- **method `Diagrams.validate`** [L141-157]: `def validate(self) -> None`
- **class `MetricRow`** [L161-177] decorators: @dataclass(frozen=True) - One row of the long metric table. ``value=None`` means undefined or missing, never 0.
- **class `MetricRecords(Artifact)`** [L181-200] decorators: @dataclass(frozen=True, eq=False) - Long table of metric values (one ``MetricRow`` per value), stored as JSON.
- **method `MetricRecords.validate`** [L192-200]: `def validate(self) -> None`
- **class `GateCheck`** [L204-210] decorators: @dataclass(frozen=True) - One gate check: ``value`` and ``threshold`` are JSON scalars (or None).
- **class `GateReport(Artifact)`** [L214-234] decorators: @dataclass(frozen=True, eq=False) - Verdict of one gate. Invariants (``INVALID_CONFIG``): ``pass`` needs ≥ 1 check and all
- **method `GateReport.validate`** [L226-234]: `def validate(self) -> None`
- **class `RunManifest(Artifact)`** [L238-261] decorators: @dataclass(frozen=True, eq=False) - What ran: the artifact DAG (``id -> parent ids``), resolved config and its hash, seeds,
- **method `RunManifest.validate`** [L258-261]: `def validate(self) -> None`

