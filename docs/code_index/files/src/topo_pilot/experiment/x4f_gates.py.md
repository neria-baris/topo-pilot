# `src/topo_pilot/experiment/x4f_gates.py`

- Source: [src/topo_pilot/experiment/x4f_gates.py](../../../../../../src/topo_pilot/experiment/x4f_gates.py)
- Kind: python
- Lines: 213

## Module docstring

> X4-F gates G1-G5 for one model (x4f-exec-v2 §4-§10); numbers only, no I/O.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import apply_map, kl_rows, leading_components, pc_scores, r2_pooled, rbf_bandwidth, rbf_features, rbf_map, readout_projector, standardizer` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 13, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.learner import forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 26, via package root)
- `from .x4f_data import INDEX, ModelData` -> [src/topo_pilot/experiment/x4f_data.py](x4f_data.py.md) (line 28, via relative)
- `from .x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](x4f_probe.py.md) (line 29, via relative)

### External (third-party)

- `numpy` (lines 10)
- `torch` (lines 11)

### Standard library

- `__future__` (lines 6)
- `functools` (lines 84)
- `hashlib` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x4f_damage.py](x4f_damage.py.md) (line 19, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 38, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 8, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 11, import)
- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 10, import)

## Top-level constants

- `CONTROLS`
- `STREAM`

## Classes and functions

- **function `gen`** [L37-38]: `def gen(*scope) -> np.random.Generator`
- **function `_split`** [L41-42]: `def _split(d: ModelData, X)`
- **function `probe`** [L45-49]: `def probe(d: ModelData, X, Y, checkpoint=lambda _: None) -> dict` - Nested ridge of ``X -> Y`` (calibration selection, one validation score).
- **function `shuffled`** [L52-64]: `def shuffled(d: ModelData, X, Y, target: str, checkpoint=lambda _: None) -> dict` - 20 shuffled-calibration-target refits through the identical pipeline; q95.
- **function `rbf_probe`** [L67-79]: `def rbf_probe(d: ModelData, Xc_feat, Xv_feat, Yc, Yv, checkpoint=lambda _: None) -> dict` - RBF random-feature ridge (calibration standardisation and median bandwidth).
- **function `g1`** [L82-121]: `def g1(d: ModelData, checkpoint=lambda _: None) -> dict` - G1-primary, G1-r2 and the descriptive short-context comparators.
- **function `weights_hash`** [L124-129]: `def weights_hash(model: torch.nn.Module) -> str`
- **function `_softmax`** [L132-135]: `def _softmax(logits: np.ndarray) -> np.ndarray`
- **class `ValForward`** [L138-157] - Frozen model on the validation inputs: base logits, captured hooks, patched runs.
- **method `ValForward.__init__`** [L141-149]: `def __init__(self, model, d: ModelData)`
- **method `ValForward.patch`** [L151-153]: `def patch(self, site: str, repl: np.ndarray)`
- **method `ValForward.kl`** [L155-157]: `def kl(self, logits_I) -> tuple[float | None, str]`
- **function `final_null`** [L160-176]: `def final_null(vf: ValForward, model) -> dict` - u-space effective-null projection, y' = u' diag(gamma) + beta, float64 algebra.
- **function `g2`** [L179-202]: `def g2(d: ModelData, model, vf: ValForward, primary) -> dict` - Identity, causality (primary eraser), final-null and frozen-weight checks.
- **function `control_targets`** [L205-213]: `def control_targets(d: ModelData) -> dict[str, np.ndarray]` - Calibration-fitted control targets over all rows (PCs fitted on calibration only).

