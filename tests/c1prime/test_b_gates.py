"""Independent tests (author B, job 0026), TEST_PLAN B-3 part 3: damage, leakage, M2, V1, V2, M4.

Protocol §7 (decoder use, M4), §8 (D_w, D_y, leakage, M2 table), §10 (wrap, V1, V2); API.md §9-§10.
Written from the protocol and the four contract documents only; no tools/c1prime source was read
and nothing was executed by the author. Expected values are hand-built: boundary values are
dyadic or chosen so that the float comparisons are exact, and the V1/V2 fixtures are built so
that the median-tie, sign(0) and wrap rules each change the outcome.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_fit  # noqa: E402
import c1_gates  # noqa: E402

pytestmark = pytest.mark.analysis

TWO_PI = 2.0 * np.pi
FAM = "INCONCLUSIVE/FAMILY_UNMATCHED"
NUIS = "INCONCLUSIVE/NUISANCE_CONFOUNDED"


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


# --- damage metrics and leakage (§8.1, §8.3) ----------------------------------------------------


def test_D_w_counts_both_arms_over_2n():
    w = np.arange(10)
    wp, wm = w.copy(), w.copy()
    wp[3] = 30
    wm[[1, 8]] = 31
    assert c1_gates.D_w(w, [wp, wm]) == pytest.approx(3 / 20, rel=0, abs=1e-15)
    assert c1_gates.D_w(w, [w.copy(), w.copy()]) == 0.0


def test_D_y_and_leakage():
    rng = np.random.default_rng(1)
    y, yp, ym = rng.random((10, 12)), rng.random((10, 12)), rng.random((10, 12))
    tr = 0.37
    expected = (np.sum((yp - y) ** 2) + np.sum((ym - y) ** 2)) / 20 / tr
    assert c1_gates.D_y(y, [yp, ym], tr) == pytest.approx(expected, rel=1e-13)
    nu_p, nu_m = rng.random((10, 12)), rng.random((10, 12))
    L = np.sum((yp - ym) * (nu_p - nu_m)) / np.sum((nu_p - nu_m) ** 2)
    assert c1_gates.leakage(yp, ym, nu_p, nu_m) == pytest.approx(L, rel=1e-13)
    assert c1_gates.leakage(nu_p, nu_m, nu_p, nu_m) == pytest.approx(1.0, rel=1e-14)


# --- M2 (§8.2; leakage §8.3) --------------------------------------------------------------------


def _m2(Dw_T=0.0, Dy_T=0.0, Dw_C=None, Dy_C=None, L_T=None, active=False):
    Dw_C = [0.0] * 32 if Dw_C is None else Dw_C
    Dy_C = [0.0] * 32 if Dy_C is None else Dy_C
    return _status(c1_gates.m2(Dw_T, Dy_T, Dw_C, Dy_C, L_T=L_T, active=active))


def test_m2_primary_ceilings_are_inclusive():
    fw, fy = [2.0**-6] * 32, [3 * 2.0**-6] * 32  # family means exact: 0.015625, 0.046875
    assert _m2(0.02, 0.05, fw, fy) == "PASS"
    assert _m2(0.0200001, 0.05, fw, fy) == FAM
    assert _m2(0.02, 0.0500001, fw, fy) == FAM


def test_m2_matching_bounds_are_inclusive():
    assert _m2(Dw_T=0.01) == "PASS"
    assert _m2(Dw_T=0.0100001) == FAM
    assert _m2(Dy_T=0.02) == "PASS"
    assert _m2(Dy_T=0.0200001) == FAM


def test_m2_family_ceiling_fails_even_when_dispersion_holds():
    fw = [0.0] * 28 + [0.2] * 4  # 28/32 frames fine, but D_w(C bar) = 0.025 > 0.02
    assert _m2(0.02, 0.0, fw) == FAM


def test_m2_dispersion_needs_28_of_32_frames():
    bad = 3 * 2.0**-7  # 0.0234375 > 0.02
    assert _m2(Dw_C=[0.0] * 28 + [bad] * 4) == "PASS"
    assert _m2(Dw_C=[0.0] * 27 + [bad] * 5) == FAM
    dy = [0.0] * 32
    dy[0] = 0.0625  # a frame bad only in D_y also counts against dispersion
    assert _m2(Dw_C=[0.0] * 28 + [bad] * 4, Dy_C=dy) == FAM


def test_m2_leakage_only_when_active_and_after_family():
    assert _m2(L_T=0.25, active=True) == "PASS"
    assert _m2(L_T=0.2500001, active=True) == NUIS
    assert _m2(L_T=0.9, active=False) == "PASS"
    assert _m2(Dw_T=0.5, L_T=0.9, active=True) == FAM  # family/matching checked first


# --- wrap, V1, V2 (§10) --------------------------------------------------------------------------


def test_wrap_maps_into_minus_pi_exclusive_pi_inclusive():
    w = np.asarray(c1_gates.wrap(np.array([np.pi, -np.pi, 0.0, np.pi + 1e-9, 2.5, -2.5])))
    for value in w[:2]:  # both ends of the seam map to the closed end +pi
        assert np.pi - 1e-15 <= value <= np.pi
    assert w[2] == 0.0
    assert w[3] == pytest.approx(-np.pi + 1e-9, abs=1e-12)
    assert w[4] == pytest.approx(2.5, abs=1e-15) and w[5] == pytest.approx(-2.5, abs=1e-15)
    x = np.random.default_rng(2).uniform(-20.0, 20.0, 500)
    y = np.asarray(c1_gates.wrap(x))
    assert np.all(y > -np.pi) and np.all(y <= np.pi)
    k = (x - y) / TWO_PI
    np.testing.assert_allclose(k, np.round(k), rtol=0, atol=1e-12)


def _m32(theta):
    return 0.7 * np.column_stack((np.cos(theta), np.sin(theta)))


def _v1_fixture(row4_agrees):
    # |delta*| = .1 .2 .3 .4 .4 .5 .6 .683: inverted_cdf median 0.4 (a tie); counted rows 3..7.
    th_m = np.full(8, 0.5)
    th_p = 0.5 + np.array([0.1, -0.2, 0.3, 0.4, 0.4, -0.5, 0.6, 0.0])
    th_p[7], th_m[7] = 2.8, -2.8  # raw difference 5.6 wraps to -0.683
    sign_star = np.sign(np.array([0.1, -0.2, 0.3, 0.4, 0.4, -0.5, 0.6, -0.683]))
    agree = np.array([False, False, False, False, row4_agrees, True, True, True])
    step = np.where(agree, sign_star, -sign_star) * 0.05
    step[3] = 0.0  # delta exactly 0: sign(0) counts as disagreement
    phi_m = np.full(8, 1.0)
    return phi_m + step, phi_m, _m32(th_p), _m32(th_m)


def test_v1_counts_median_ties_wraps_and_treats_sign_zero_as_disagreement():
    assert _status(c1_gates.v1(*_v1_fixture(True))) == "PASS"  # 4 of 5 = 0.8
    assert _status(c1_gates.v1(*_v1_fixture(False))) == "INCONCLUSIVE/CHART_NOT_REGISTERING"


def test_v1_sign_zero_on_both_sides_is_still_disagreement():
    th_m, th_p = np.full(4, 0.5), np.array([0.5, 0.5, 0.5, 1.0])  # median |delta*| = 0
    phi_m = np.full(4, 2.0)
    phi_p = phi_m + np.array([0.0, 0.0, 0.0, 0.1])
    res = c1_gates.v1(phi_p, phi_m, _m32(th_p), _m32(th_m))
    assert _status(res) == "INCONCLUSIVE/CHART_NOT_REGISTERING"  # 1 of 4, not 4 of 4


def _v2(flips=(), scale=1.0, base=3.0, zero_arms=()):
    k = np.arange(1, 21) * 0.01
    d = k * np.array([1.0, -1.0] * 10)
    e = scale * d
    for j in flips:
        e[j] = -e[j]
    for j in zero_arms:
        d[j], e[j] = 0.0, 0.0
    phi_s = np.full(10, base)
    pm = ((base + d[:10]) % TWO_PI, (base + d[10:]) % TWO_PI)
    tm = ((base + e[:10]) % TWO_PI, (base + e[10:]) % TWO_PI)
    return phi_s, pm, tm


@pytest.mark.parametrize("kwargs,expected", [
    ({}, "PASS"),
    ({"flips": (9, 10)}, "PASS"),  # 9/11 arms at |d| >= median agree; kappa 0.8
    ({"flips": (9, 10, 11)}, "INCONCLUSIVE/MANIPULATION_FAILED"),  # 8/11; kappa 0.686
    ({"scale": 0.52}, "PASS"), ({"scale": 0.48}, "INCONCLUSIVE/MANIPULATION_FAILED"),
    ({"scale": 1.48}, "PASS"), ({"scale": 1.52}, "INCONCLUSIVE/MANIPULATION_FAILED"),
    ({"scale": 0.6, "base": 6.2}, "PASS"),  # needs wrap at the 2 pi seam
    ({"zero_arms": tuple(range(11))}, "INCONCLUSIVE/MANIPULATION_FAILED"),  # sign(0) arms
])
def test_v2_kappa_agreement_wrap_and_sign_zero(kwargs, expected):
    assert _status(c1_gates.v2(*_v2(**kwargs))) == expected


# --- M4 and the decoder argmax (§7) ---------------------------------------------------------------


def test_m4_boundaries():
    w_true = np.arange(20) % 36
    w19 = w_true.copy()
    w19[0] = 35
    w18 = w19.copy()
    w18[1] = 35
    y_true = np.array([[1.0], [-1.0], [1.0], [-1.0]])
    mean0 = np.array([0.0])
    half = np.array([[0.0], [0.0], [1.0], [-1.0]])  # SSE 2 of SST 4: r2 = 0.5 exactly
    worse = np.array([[0.0], [0.0], [0.0], [-1.0]])
    assert _status(c1_gates.m4(w19, w_true, half, y_true, mean0)) == "PASS"  # 0.95, 0.5
    bad = "INCONCLUSIVE/DECODER_INADEQUATE"
    assert _status(c1_gates.m4(w18, w_true, half, y_true, mean0)) == bad
    assert _status(c1_gates.m4(w19, w_true, worse, y_true, mean0)) == bad
    flat = np.zeros((4, 1))
    assert _status(c1_gates.m4(w19, w_true, flat, flat, mean0)) == bad  # r2 undefined


class _FixedDecoder:
    def __init__(self, scores):
        self.scores = np.asarray(scores, dtype=np.float64)

    def predict(self, a):
        return self.scores


def test_w_hat_breaks_ties_to_the_lowest_index():
    dec = _FixedDecoder([[0.1, 0.5, 0.5], [0.9, 0.9, 0.1], [0.2, 0.2, 0.2], [0.0, 0.0, 1.0]])
    got = np.asarray(c1_fit.w_hat(dec, np.zeros((4, 128))))
    assert got.tolist() == [1, 0, 0, 2]
