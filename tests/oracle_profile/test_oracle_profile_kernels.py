"""Independent tests of x4_oracle_profile helper kernels (job 0014; API.md section 4 items 7-11):
validate_process, circle_features, residual_rows, profile_point, bootstrap_profile and
percentile_interval. Written from ``tools/x4_oracle_profile/API.md`` only: production is imported,
never read. Randomness only through explicitly seeded np.random.Generator(np.random.PCG64(seed)).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.oracle

REPO_ROOT = Path(__file__).resolve().parents[2]
_path = str(REPO_ROOT / "tools" / "x4_oracle_profile")
if _path not in sys.path:
    sys.path.insert(0, _path)

import oracle_profile as op  # noqa: E402

KEYS = (
    "T_row_sum_max_abs_err", "E_row_sum_max_abs_err", "pi_sum_abs_err", "stationarity_max_abs_err"
)
# The asymmetric 3-state HMM of test_oracle_profile.py, pi = (72, 70, 33) / 175 exactly stationary.
T3 = np.array([[1 / 2, 1 / 3, 1 / 6], [1 / 5, 1 / 2, 3 / 10], [2 / 3, 1 / 3, 0.0]])
E3 = np.array([[2 / 3, 1 / 3, 0.0], [1 / 4, 3 / 4, 0.0], [1 / 5, 0.0, 4 / 5]])
PI3 = np.array([72.0, 70.0, 33.0]) / 175.0
# A dyadic 4-state cycle with uniform stationary pi: every check is exact in float64.
T4 = np.array([[.5, .5, 0, 0], [0, .5, .5, 0], [0, 0, .5, .5], [.5, 0, 0, .5]])
E4 = np.array([[1.0, 0.0], [0.0, 1.0], [0.5, 0.5], [0.25, 0.75]])
PI4 = np.full(4, 0.25)


def replaced(arr, index, value):
    out = np.array(arr, dtype=np.float64, copy=True)
    out[index] = value
    return out


def seeded(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------- item 7: validate_process
def test_validate_process_accepts_valid_models():
    for T, E, pi in ((T3, E3, PI3), (T4, E4, PI4)):
        out = op.validate_process(T, E, pi)
        for key in KEYS:
            assert isinstance(out[key], float) and 0.0 <= out[key] <= 1e-12
    exact = op.validate_process(T4, E4, PI4)
    assert all(exact[key] == 0.0 for key in KEYS)


def test_validate_process_reports_known_maxima():
    """Dyadic perturbations: row error 2^-10 in T, 2^-11 in E, pi sum error 2^-9.

    pi @ T - pi = (2^-10, 2^-12, 0, -2^-10), so the stationarity maximum is 2^-10.
    """
    T = replaced(T4, (0, 1), 0.5 + 2.0**-10)
    E = replaced(E4, (3, 1), 0.75 + 2.0**-11)
    pi = replaced(PI4, 3, 0.25 + 2.0**-9)
    out = op.validate_process(T, E, pi, tol=1e-2)
    expected = dict(zip(KEYS, (2.0**-10, 2.0**-11, 2.0**-9, 2.0**-10)))
    for key, value in expected.items():
        assert abs(out[key] - value) <= 1e-18, key
    with pytest.raises(op.ProfileError):
        op.validate_process(T, E, pi)


REJECT = {
    "non_stationary_pi": (T3, E3, np.array([0.5, 0.25, 0.25])),
    "T_row_not_stochastic": (replaced(T3, (1, 1), 0.6), E3, PI3),
    "E_row_not_stochastic": (T3, replaced(E3, (0, 1), 0.5), PI3),
    "pi_not_normalised": (T3, E3, PI3 * 1.01),
    "negative_E_entry_rows_still_sum_to_1": (T3, replaced(E3, 0, [1.25, -0.25, 0.0]), PI3),
    "negative_T_entry": (replaced(T4, 0, [0.75, 0.5, -0.25, 0.0]), E4, PI4),
    "nan_in_T": (replaced(T3, (0, 0), np.nan), E3, PI3),
    "nan_in_E": (T3, replaced(E3, (2, 2), np.nan), PI3),
    "nan_in_pi": (T3, E3, replaced(PI3, 1, np.nan)),
    "inf_in_E": (T3, replaced(E3, (1, 0), np.inf), PI3),
    "T_not_square": (T3[:, :2], E3, PI3),
    "T_one_dimensional": (T3[0], E3, PI3),
    "E_wrong_row_count": (T3, E3[:2], PI3),
    "pi_wrong_length": (T3, E3, PI3[:2]),
}


@pytest.mark.parametrize("name", sorted(REJECT))
def test_validate_process_rejects(name):
    T, E, pi = REJECT[name]
    with pytest.raises(op.ProfileError):
        op.validate_process(T, E, pi)


# ---------------------------------------------------------------- item 8: circle_features
def test_circle_features_known_answers():
    coords = np.array([[0, 7], [3, 1], [6, 11], [9, 2]], dtype=np.int64)
    expected = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    got = op.circle_features(coords)
    assert got.shape == (4, 2) and got.dtype == np.float64
    assert np.max(np.abs(got - expected)) <= 1e-15
    other_columns = coords.copy()
    other_columns[:, 1] = [5, 5, 0, 3]
    assert np.array_equal(op.circle_features(other_columns), got)
    assert np.max(np.abs(op.circle_features(coords[:, :1].astype(np.float64)) - expected)) <= 1e-15


def test_circle_features_all_twelve_positions():
    x = np.arange(12)
    got = op.circle_features(x[:, None])
    angle = 2 * np.pi * x / 12
    assert np.max(np.abs(got - np.column_stack([np.cos(angle), np.sin(angle)]))) <= 1e-15
    assert np.max(np.abs(np.hypot(got[:, 0], got[:, 1]) - 1.0)) <= 1e-15


@pytest.mark.parametrize("value", [1.5, 12, -1, np.nan, np.inf], ids=str)
def test_circle_features_rejects_bad_coordinates(value):
    coords = np.array([[0.0, 0.0], [value, 0.0]])
    with pytest.raises(op.ProfileError):
        op.circle_features(coords)


# ---------------------------------------------------------------- item 9: residual_rows, profile
def hand_means():
    return {
        1: np.array([[0.0, 0.0], [0.5, -0.5]]),
        4: np.array([[3.0, 2.0], [0.5, 0.5]]),
        32: np.array([[3.0, 4.0], [0.5, 0.5]]),
    }


def test_residual_rows_and_profile_point_known_answer():
    """r_1 = ((3, 4), (0, 1)) -> norm (5, 1), sq (25, 1); r_4 = ((0, 2), (0, 0)) -> (2, 0), (4, 0).

    B_1 = 3, V_1 = 13; B_4 = 1, V_4 = 2; B_32 = V_32 = 0.
    """
    res = op.residual_rows(hand_means())
    assert np.array_equal(res["r"][1], np.array([[3.0, 4.0], [0.0, 1.0]]))
    assert np.array_equal(res["r"][4], np.array([[0.0, 2.0], [0.0, 0.0]]))
    assert np.all(res["r"][32] == 0.0) and res["r"][32].shape == (2, 2)
    expected_norm = {1: [5.0, 1.0], 4: [2.0, 0.0], 32: [0.0, 0.0]}
    expected_sq = {1: [25.0, 1.0], 4: [4.0, 0.0], 32: [0.0, 0.0]}
    for K in (1, 4, 32):
        assert np.max(np.abs(res["norm"][K] - expected_norm[K])) <= 1e-15
        assert np.max(np.abs(res["sq"][K] - expected_sq[K])) <= 1e-15
    point = op.profile_point(res["norm"], res["sq"])
    for K, (b, v) in {1: (3.0, 13.0), 4: (1.0, 2.0), 32: (0.0, 0.0)}.items():
        assert isinstance(point["B"][K], float) and isinstance(point["V"][K], float)
        assert abs(point["B"][K] - b) <= 1e-15 and abs(point["V"][K] - v) <= 1e-15


def test_residual_rows_custom_full_and_errors():
    res = op.residual_rows(hand_means(), full=4)  # r_K = means[4] - means[K]
    assert np.array_equal(res["r"][32], np.array([[0.0, -2.0], [0.0, 0.0]]))
    assert np.all(res["r"][4] == 0.0)
    with pytest.raises(op.ProfileError):
        op.residual_rows({1: hand_means()[1], 4: hand_means()[4]})  # full = 32 missing
    with pytest.raises(op.ProfileError):
        op.residual_rows(hand_means(), full=8)
    bad = hand_means()
    bad[4] = np.zeros((3, 2))
    with pytest.raises(op.ProfileError):
        op.residual_rows(bad)


def test_jensen_bias_at_most_root_variance():
    rng = seeded(20261014)
    means = {K: rng.normal(size=(64, 2)) for K in (1, 2, 4, 8, 16, 32)}
    res = op.residual_rows(means)
    point = op.profile_point(res["norm"], res["sq"])
    for K in means:
        assert np.max(np.abs(res["sq"][K] - res["norm"][K] ** 2)) <= 1e-12
        assert point["B"][K] <= math.sqrt(point["V"][K]) + 1e-15
    hand = op.residual_rows(hand_means())
    hand_point = op.profile_point(hand["norm"], hand["sq"])
    assert all(hand_point["B"][K] <= math.sqrt(hand_point["V"][K]) + 1e-15 for K in (1, 4, 32))


# ---------------------------------------------------------------- item 10: bootstrap_profile
BASE = np.array([0.1, 0.7, 1.3, 2.9, 3.1, 5.3, 8.9])
N_ROWS = BASE.size


def boot_inputs():
    """norm differs by K (norm_4 = 2 norm_1 + 1); sq_1 = norm_1 so B and V share idx visibly."""
    norm = {1: BASE.copy(), 4: 2.0 * BASE + 1.0, 32: np.zeros(N_ROWS)}
    sq = {1: BASE.copy(), 4: BASE**2, 32: np.zeros(N_ROWS)}
    return norm, sq


def manual_bootstrap(norm, sq, Ks, rng, draws):
    """Re-implementation of the documented order: one rng.integers(0, n, size=n) call per draw."""
    B = np.empty((draws, len(Ks)))
    Vv = np.empty((draws, len(Ks)))
    for d in range(draws):
        idx = rng.integers(0, N_ROWS, size=N_ROWS)
        for k, K in enumerate(Ks):
            B[d, k] = np.mean(norm[K][idx])
            Vv[d, k] = np.mean(sq[K][idx])
    return B, Vv


@pytest.mark.parametrize("Ks", [[1, 4, 32], [32, 1, 4]])
def test_bootstrap_reproduces_documented_sampling_order(Ks):
    norm, sq = boot_inputs()
    draws, seed = 40, 14
    rng = seeded(seed)
    out = op.bootstrap_profile(norm, sq, Ks, rng, draws)
    assert out["B"].shape == (draws, len(Ks)) and out["V"].shape == (draws, len(Ks))
    assert out["B"].dtype == np.float64 and out["V"].dtype == np.float64
    rng_manual = seeded(seed)
    B, Vv = manual_bootstrap(norm, sq, Ks, rng_manual, draws)
    assert np.max(np.abs(out["B"] - B)) <= 1e-12
    assert np.max(np.abs(out["V"] - Vv)) <= 1e-12
    # Exactly `draws` calls consumed the generator: the next draws coincide.
    assert np.array_equal(rng.integers(0, 10**9, size=8), rng_manual.integers(0, 10**9, size=8))
    col = {K: k for k, K in enumerate(Ks)}
    # Same idx across K: norm_4 = 2 norm_1 + 1 row by row survives resampling only with one idx.
    assert np.max(np.abs(out["B"][:, col[4]] - (2.0 * out["B"][:, col[1]] + 1.0))) <= 1e-12
    # Same idx for B and V: sq_1 = norm_1.
    assert np.max(np.abs(out["V"][:, col[1]] - out["B"][:, col[1]])) <= 1e-12
    assert np.unique(out["B"][:, col[1]]).size > 1  # resampling actually varies
    assert np.all(out["B"][:, col[32]] == 0.0)


def test_bootstrap_error_paths():
    norm, sq = boot_inputs()
    Ks = [1, 4, 32]
    for draws in (0, -1):
        with pytest.raises(op.ProfileError):
            op.bootstrap_profile(norm, sq, Ks, seeded(1), draws)
    short_norm = dict(norm)
    short_norm[4] = norm[4][:-1]
    with pytest.raises(op.ProfileError):
        op.bootstrap_profile(short_norm, sq, Ks, seeded(1), 5)
    short_sq = dict(sq)
    short_sq[32] = sq[32][:-1]
    with pytest.raises(op.ProfileError):
        op.bootstrap_profile(norm, short_sq, Ks, seeded(1), 5)
    one_norm = {K: v[:1] for K, v in norm.items()}
    one_sq = {K: v[:1] for K, v in sq.items()}
    with pytest.raises(op.ProfileError):
        op.bootstrap_profile(one_norm, one_sq, Ks, seeded(1), 5)


# ---------------------------------------------------------------- item 11: percentile_interval
def test_percentile_interval_equals_inverted_cdf_quantile():
    samples = seeded(11).normal(size=(200, 3))
    probs = [0.025, 0.5, 0.975]
    expected = np.quantile(samples, probs, axis=0, method="inverted_cdf")
    got = op.percentile_interval(samples, probs)
    assert np.shape(got) == (3, 3) and np.array_equal(got, expected)


def test_percentile_interval_hand_case():
    """n = 4: inverted CDF picks x_(ceil(n p)): p = .25 -> 1, .3 -> 2, .5 -> 2, 1 -> 4."""
    samples = np.array([[4.0], [2.0], [1.0], [3.0]])
    got = op.percentile_interval(samples, [0.25, 0.3, 0.5, 1.0])
    assert np.array_equal(np.asarray(got), np.array([[1.0], [2.0], [2.0], [4.0]]))
