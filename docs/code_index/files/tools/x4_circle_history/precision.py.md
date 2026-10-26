# `tools/x4_circle_history/precision.py`

- Source: [tools/x4_circle_history/precision.py](../../../../../tools/x4_circle_history/precision.py)
- Kind: python
- Lines: 146

## Module docstring

> Fixed-chart validation precision and B4 headroom gates (API.md precision.py).

## Imports

### Internal (repo files)

- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 9, via same directory)

### External (third-party)

- `numpy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `math` (lines 5)
- `statistics` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_precision.py](../../tests/c1prime/test_b_precision.py.md) (line 30, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 38, import)
- [tests/circle_history/test_controls.py](../../tests/circle_history/test_controls.py.md) (line 30, import)
- [tests/circle_history/test_scores_precision_gates.py](../../tests/circle_history/test_scores_precision_gates.py.md) (line 30, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 29, import)
- [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 14, import)
- [tools/c2_nd/nd_stage_val.py](../c2_nd/nd_stage_val.py.md) (line 24, import)
- [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 26, import)
- [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 18, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 72, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 92, import)

## Top-level constants

- `CONTROL_NAMES`
- `_CONTROL_Q`

## Classes and functions

- **function `_arrays`** [L12-19]: `def _arrays(values: dict, models) -> list[np.ndarray]`
- **function `sd_b4_draws`** [L22-36]: `def sd_b4_draws(X: dict, r4n: dict, models, seed, draws, size)` - Joint whole-trajectory resamples: ONE index per draw shared by every model.
- **function `centered_draws`** [L39-49]: `def centered_draws(X: dict, models, seed, draws, size)`
- **function `mde`** [L52-55]: `def mde(sd, cfg) -> float`
- **function `_q`** [L58-59]: `def _q(values, prob) -> float`
- **function `_draw_matrix`** [L62-70]: `def _draw_matrix(draws, models, name) -> np.ndarray`
- **function `precision_summary`** [L73-92]: `def precision_summary(sd, e, models, cfg) -> dict`
- **function `b4_summary`** [L95-108]: `def b4_summary(b4_draws, b4_point: dict, models, cfg) -> dict`
- **function `control_summary`** [L115-146]: `def control_summary(C: dict, models, seed, draws) -> dict` - Validation control means with joint whole-trajectory resampling (spec v2.4 item 10).

