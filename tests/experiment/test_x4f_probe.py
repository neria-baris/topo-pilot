"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.

Nested leave-one-panel-out ridge (X4F_GATES_API section 3; x4f-exec-v2 section 4).
"""
import numpy as np
import pytest

from topo_pilot.experiment.x4f_probe import GRID, NestedResult, nested_ridge
from topo_pilot.prediction import RidgeProbe

pytestmark = pytest.mark.experiment


# --------------------------------------------------------------------------- reference (from spec)

def _std(X):
    mean = X.mean(0)
    sd = X.std(0, ddof=0)
    return mean, np.where(sd <= 1e-12, 1.0, sd)


def _ridge_pred(X_fit, Y_fit, X_new, lam):
    m, s = _std(X_fit)
    Xf, Xn = (X_fit - m) / s, (X_new - m) / s
    return RidgeProbe([lam]).fit(Xf, Y_fit, Xf, Y_fit).predict(Xn)


def _ref_fold_mse(X, Y, panel, grid):
    out = {}
    for lam in grid:
        mses = []
        for p in np.unique(panel):
            fit = panel != p
            pred = _ridge_pred(X[fit], Y[fit], X[~fit], lam)
            mses.append(float(np.mean((pred - Y[~fit].reshape(pred.shape)) ** 2)))
        out[float(lam)] = float(np.mean(mses))
    return out


def _ref_choice(fold):
    return max(fold, key=lambda lam: (-fold[lam], lam))   # minimal MSE; ties -> larger lambda


def _data(seed=0, per_panel=30, panels=(2, 3, 5, 7, 11, 13), noise=1.0, n_val=60):
    rng = np.random.default_rng(seed)
    panel = rng.permutation(np.repeat(np.array(panels), per_panel))
    n, d = panel.size, 5
    scales = np.array([1.0, 10.0, 0.1, 3.0, 50.0])
    offs = np.array([0.0, 5.0, -2.0, 100.0, 1.0])
    B = rng.normal(size=(d, 2)) / scales[:, None]
    X_cal = rng.normal(size=(n, d)) * scales + offs
    Y_cal = X_cal @ B + noise * rng.normal(size=(n, 2))
    X_val = rng.normal(size=(n_val, d)) * scales + offs
    Y_val = X_val @ B + noise * rng.normal(size=(n_val, 2)) + np.array([0.7, -0.4])
    return X_cal, Y_cal, panel, X_val, Y_val


# --------------------------------------------------------------------------- tests

def test_grid_constant():
    assert tuple(GRID) == (1e-3, 1e-2, 1e-1, 1.0, 10.0)


@pytest.mark.parametrize("seed,noise", [(0, 1.0), (1, 5.0), (2, 0.05)])
def test_selection_and_fold_mse_match_reference(seed, noise):
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=seed, noise=noise)
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    assert isinstance(res, NestedResult)
    ref = _ref_fold_mse(X_cal, Y_cal, panel, GRID)
    vals = sorted(ref.values())
    assert vals[1] - vals[0] > 1e-11 * vals[0]                 # fixture: a clear winner
    assert set(res.fold_mse) == set(GRID) and len(res.fold_mse) == len(GRID)
    for lam in GRID:
        assert res.fold_mse[lam] == pytest.approx(ref[lam], rel=1e-8)
    assert res.lam == _ref_choice(ref)


def test_predictions_equal_ridgeprobe_on_calibration_standardised_data():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=3)
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    pred = _ridge_pred(X_cal, Y_cal, X_val, res.lam)
    assert res.pred_val.shape == Y_val.shape
    np.testing.assert_allclose(res.pred_val, pred, rtol=0, atol=1e-8)


def test_r2_uses_calibration_mean_and_pooled_sst():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=4)
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    pred = _ridge_pred(X_cal, Y_cal, X_val, res.lam)
    sse = np.sum((Y_val - pred) ** 2)
    r2_cal = 1 - sse / np.sum((Y_val - Y_cal.mean(0)) ** 2)
    r2_valmean = 1 - sse / np.sum((Y_val - Y_val.mean(0)) ** 2)
    assert abs(r2_cal - r2_valmean) > 1e-3                      # fixture: the means differ
    assert res.r2_status == "ok"
    assert res.r2 == pytest.approx(r2_cal, abs=1e-8)


def test_validation_isolation_nan_poison():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=5)
    clean = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    nan_X = np.full_like(X_val, np.nan)
    nan_Y = np.full_like(Y_val, np.nan)
    both = nested_ridge(X_cal, Y_cal, panel, nan_X, nan_Y)
    assert both.lam == clean.lam
    assert both.fold_mse == clean.fold_mse
    assert both.r2 is None or np.isnan(both.r2)
    assert both.pred_val is None or np.all(np.isnan(both.pred_val))
    only_y = nested_ridge(X_cal, Y_cal, panel, X_val, nan_Y)
    assert only_y.lam == clean.lam and only_y.fold_mse == clean.fold_mse
    np.testing.assert_array_equal(only_y.pred_val, clean.pred_val)
    assert only_y.r2 is None or np.isnan(only_y.r2)


def test_inputs_not_mutated():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=6)
    copies = [a.copy() for a in (X_cal, Y_cal, panel, X_val, Y_val)]
    nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    for a, c in zip((X_cal, Y_cal, panel, X_val, Y_val), copies):
        np.testing.assert_array_equal(a, c)


def test_tie_rule_larger_lambda_wins():
    rng = np.random.default_rng(7)
    panel = np.repeat(np.arange(1, 7), 25)
    X_cal = np.tile([2.5, -1.0, 0.0], (panel.size, 1))         # zero-variance columns only
    Y_cal = rng.normal(size=(panel.size, 2))
    X_val = rng.normal(size=(20, 3))
    Y_val = rng.normal(size=(20, 2))
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    assert len(set(res.fold_mse.values())) == 1                 # predictions ignore lambda
    assert res.lam == 10.0
    res2 = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val, grid=(0.5, 3.0, 0.1))
    assert res2.lam == 3.0
    assert set(res2.fold_mse) == {0.5, 3.0, 0.1}
    # with nothing to fit, the prediction is the calibration mean
    np.testing.assert_allclose(res.pred_val, np.tile(Y_cal.mean(0), (20, 1)), atol=1e-12)


def test_fold_mse_is_unweighted_mean_over_sorted_panels():
    X_cal, Y_cal, _, X_val, Y_val = _data(seed=8)
    rng = np.random.default_rng(8)
    panel = rng.permutation(np.repeat(np.arange(6), [10, 20, 30, 40, 40, 40]))
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    ref = _ref_fold_mse(X_cal, Y_cal, panel, GRID)
    for lam in GRID:
        assert res.fold_mse[lam] == pytest.approx(ref[lam], rel=1e-8)


def test_determinism():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=9)
    a = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    b = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    assert a.lam == b.lam and a.fold_mse == b.fold_mse
    assert a.r2 == b.r2 and a.r2_status == b.r2_status
    np.testing.assert_array_equal(a.pred_val, b.pred_val)


def test_permuting_rows_within_calibration_does_not_change_result():
    X_cal, Y_cal, panel, X_val, Y_val = _data(seed=10)
    perm = np.random.default_rng(10).permutation(panel.size)
    a = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    b = nested_ridge(X_cal[perm], Y_cal[perm], panel[perm], X_val, Y_val)
    assert a.lam == b.lam
    for lam in GRID:
        assert b.fold_mse[lam] == pytest.approx(a.fold_mse[lam], rel=1e-9)
    np.testing.assert_allclose(b.pred_val, a.pred_val, atol=1e-8)


def test_zero_variance_validation_target_status():
    X_cal, Y_cal, panel, X_val, _ = _data(seed=11)
    Y_val = np.tile(Y_cal.mean(0), (X_val.shape[0], 1))
    res = nested_ridge(X_cal, Y_cal, panel, X_val, Y_val)
    assert res.r2 is None and res.r2_status == "R2_UNDEFINED_ZERO_VARIANCE"
