# `src/topo_pilot/experiment/x4f_probe.py`

- Source: [src/topo_pilot/experiment/x4f_probe.py](../../../../../../src/topo_pilot/experiment/x4f_probe.py)
- Kind: python
- Lines: 82

## Module docstring

> X4-F nested ridge (x4f-exec-v2 §4): inner leave-one-panel-out selection, calibration refit,
> one outer-validation score.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import r2_pooled, standardizer` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 13, 14)
- `scipy` (lines 15)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x4f_gates.py](x4f_gates.py.md) (line 29, import)
- [tests/c1prime/test_b_decoder.py](../../../tests/c1prime/test_b_decoder.py.md) (line 23, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../../tests/c2_readout/test_b_fwl_l1.py.md) (line 27, import)
- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 10, import)
- [tests/experiment/test_x4f_probe.py](../../../tests/experiment/test_x4f_probe.py.md) (line 9, import)
- [tools/c1prime/c1_fit.py](../../../tools/c1prime/c1_fit.py.md) (line 14, import)
- [tools/c2_readout/c2_stats.py](../../../tools/c2_readout/c2_stats.py.md) (line 29, import)
- [tools/d2a/d2a_eval.py](../../../tools/d2a/d2a_eval.py.md) (line 16, import)
- [tools/d2a/d2a_targets.py](../../../tools/d2a/d2a_targets.py.md) (line 19, import)
- [tools/k4b/k4b_decoder.py](../../../tools/k4b/k4b_decoder.py.md) (line 16, import)

## Top-level constants

- `GRID`

## Classes and functions

- **class `NestedResult`** [L23-31] decorators: @dataclass(frozen=True, eq=False) - Selected ``lam``, outer-validation ``r2`` (None + status if undefined), validation
- **function `_ridge_path`** [L34-48]: `def _ridge_path(X_fit: NDArray, Y_fit: NDArray, grid: tuple[float, ...], checkpoint=lambda _: None)` - Standardise on ``X_fit`` and return ``(mean, scale, y_bar, [W_lam])``.
- **function `_predict`** [L51-52]: `def _predict(X: NDArray, mean, scale, x_bar, y_bar, W) -> NDArray[np.float64]`
- **function `nested_ridge`** [L55-82]: `def nested_ridge(X_cal: NDArray, Y_cal: NDArray, panel_cal: NDArray, X_val: NDArray, Y_val: NDArray, grid: tuple[float, ...] = GRID, checkpoint=lambda _: None) -> NestedResult` - Leave-one-panel-out selection over calibration panels, refit, score once.

