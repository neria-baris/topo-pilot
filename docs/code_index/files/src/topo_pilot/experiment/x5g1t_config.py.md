# `src/topo_pilot/experiment/x5g1t_config.py`

- Source: [src/topo_pilot/experiment/x5g1t_config.py](../../../../../../src/topo_pilot/experiment/x5g1t_config.py)
- Kind: python
- Lines: 399

## Module docstring

> X5 G1 study configuration (x5g1-train-v4 §10; API v4 §3): an exact-key ``StudyConfig``, the
> frozen ``PRODUCTION`` values and a READ-ONLY validator that every stage runs before any sampler,
> model or output. A distinct ``synthetic-fixture`` mode serves tiny tests and can never pass as
> production. Unknown, missing, mistyped or tampered values fail closed with ``ConfigInvalid``.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import X5_GRID` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 17, via package root)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 18, via package root)
- `from .x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 26, via relative)
- `from .x5g1_safety import verify_sources_full` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 27, via relative)
- `from .x5g1t_checks import canonical` -> [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 28, via relative)
- `from .x5g1t_lineage import ARMS, CODES, NAMESPACE, stream` -> [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 29, via relative)
- `from .x5g1t_train import study_train_config` -> [src/topo_pilot/experiment/x5g1t_train.py](x5g1t_train.py.md) (line 30, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `json` (lines 11)
- `math` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 15)
- `re` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_fixture.py](x5g1t_fixture.py.md) (line 22, import)
- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 25, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 41, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 45, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 31, dynamic)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 30, dynamic)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 30, dynamic)
- [tests/experiment/test_x5g1t_export_checks.py](../../../tests/experiment/test_x5g1t_export_checks.py.md) (line 24, dynamic)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 24, import)

## Top-level constants

- `MODES`
- `PRODUCTION`
- `_HEX64`
- `_NUM`
- `_TOP`
- `_TYPES`

## Classes and functions

- **class `ConfigInvalid(RuntimeError)`** [L36-37] - The study configuration is malformed, tampered or unsafe; nothing was computed.
- **class `StudyConfig`** [L50-105] decorators: @dataclasses.dataclass(frozen=True)
- **method `StudyConfig.from_dict`** [L76-93]: `def from_dict(cls, d) -> StudyConfig` decorators: @classmethod
- **method `StudyConfig.root`** [L96-97]: `def root(self) -> Path` decorators: @property
- **method `StudyConfig.expected_sources`** [L99-105]: `def expected_sources(self) -> dict` - ``{id: (cls, sha)}`` for the world, both transition kernels and the emission.
- **function `_pair`** [L108-111]: `def _pair(v, what: str) -> None`
- **function `_check_shapes`** [L114-141]: `def _check_shapes(d: dict) -> None`
- **function `load_config`** [L144-149]: `def load_config(path: Path) -> StudyConfig`
- **class `ProductionSpec`** [L153-177] decorators: @dataclasses.dataclass(frozen=True)
- **function `current_lineage`** [L180-181]: `def current_lineage() -> dict`
- **function `_norm`** [L228-229]: `def _norm(p) -> str`
- **function `_within`** [L232-235]: `def _within(path, root) -> bool` - ``path`` equals ``root`` or lies inside it (resolved, case-normalised).
- **function `_fail`** [L238-239]: `def _fail(what: str) -> ConfigInvalid`
- **function `read_chain`** [L241-247]: `def read_chain(roots)` - Read-through backend chain over ``roots`` (the first is the innermost); writes nothing.
- **function `read_store`** [L250-251]: `def read_store(roots) -> ArtifactStore`
- **function `_protocol_doc`** [L254-262]: `def _protocol_doc(cfg: StudyConfig, repo: Path) -> str`
- **function `_write_roots`** [L265-271]: `def _write_roots(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> None`
- **function `_verify_sources`** [L274-289]: `def _verify_sources(cfg: StudyConfig, store: ArtifactStore) -> dict`
- **function `_verify_stored_checkpoint`** [L292-311]: `def _verify_stored_checkpoint(cfg: StudyConfig, store: ArtifactStore, spec: ProductionSpec) -> None` - Metadata only (never weights): model config and E3 train config as stored.
- **function `_production`** [L314-349]: `def _production(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> dict`
- **function `_synthetic`** [L352-380]: `def _synthetic(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> dict`
- **function `validate_config`** [L383-399]: `def validate_config(cfg: StudyConfig, repo: Path, spec: ProductionSpec = PRODUCTION) -> dict` - Read-only report (resolved roots, mode, checked hashes); ``ConfigInvalid`` otherwise.

