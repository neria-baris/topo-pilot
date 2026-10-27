"""HWSB author A: B1, B2, B3 on planted predictives (protocol §4 B1-B3; DRB5).

Targets (API.md §4): hwsb_eval.softmax64, to_canonical, check_rows, b1, forcing, b2, b3;
hwsb_config.Z_B23. Expected values come from the protocol, CONTRACT.json and independent
computations written here (s3.py softmax formula, explicit KL loops, explicit marginals),
never from the functions under test. Synthetic arrays only.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_oracle_profile", "tools/x4_circle_history", "tools/c1prime_registry",
             "tools/c1prime", "tools/k4b", "tools/hws"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import c1_means  # noqa: E402
import hws_oracle  # noqa: E402

from topo_pilot.prediction.metrics import PredictiveMetrics  # noqa: E402

try:
    import hwsb_config as hc  # noqa: E402
    import hwsb_eval as he  # noqa: E402
except ImportError as _exc:  # the implementation is written in parallel
    hc = he = None
    MISSING = repr(_exc)
else:
    MISSING = None

V, N_AXIAL = 36, 6
TOL = 1e-12


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def stop_status(excinfo):
    return getattr(excinfo.value, "status", None)


def dirichlet(rng, n):
    rows = rng.dirichlet(np.ones(V), size=n)
    assert np.all(rows > 0)
    return rows


@pytest.fixture(scope="module")
def q():
    rng = np.random.default_rng(616101)
    return {1: dirichlet(rng, 64), 4: dirichlet(rng, 64), 32: dirichlet(rng, 64)}


def kl_ref(p, q_):
    """Independent mean-free KL per row: sum_v p (log p - log q) with math.log and fsum."""
    return np.array([math.fsum(pv * (math.log(pv) - math.log(qv))
                               for pv, qv in zip(pr, qr) if pv > 0)
                     for pr, qr in zip(p.tolist(), q_.tolist())])


def marg_ref(x):
    """Circular marginal by an explicit loop: label a sums the six symbols v = 6a + b."""
    x = np.asarray(x, dtype=np.float64)
    out = np.zeros((x.shape[0], V // N_AXIAL))
    for a in range(V // N_AXIAL):
        for b in range(N_AXIAL):
            out[:, a] += x[:, N_AXIAL * a + b]
    return out


def forcing_ref(q_full, q_base, p, z):
    base = hws_oracle.kl_rows(q_full, q_base)
    model = hws_oracle.kl_rows(q_full, p)
    d = base - model
    g = float(c1_means.tree_mean(base))
    r = float(c1_means.tree_mean(model))
    d_mean = float(c1_means.tree_mean(d))
    se = float(np.std(d, ddof=1)) / math.sqrt(d.shape[0])
    return {"G_hat": g, "r": r, "ratio": r / g if g > 0 else "undefined", "d_mean": d_mean,
            "se": se, "L": d_mean - z * se}


def assert_forcing(res, ref):
    for key in ("G_hat", "r", "d_mean"):
        assert float(res[key]) == pytest.approx(ref[key], rel=TOL, abs=1e-15), key
    assert float(res["se"]) == pytest.approx(ref["se"], rel=1e-12, abs=1e-15)
    assert float(res["L"]) == pytest.approx(ref["L"], rel=1e-12, abs=1e-15)
    if ref["ratio"] == "undefined":
        assert res["ratio"] == "undefined"
    else:
        assert float(res["ratio"]) == pytest.approx(ref["ratio"], rel=TOL, abs=1e-15)
    assert bool(res["not_suffix_only"]) is (ref["L"] > 0)


def exact_boundary_rows(rng):
    """Rows with captured == 0.8 exactly in float64 (k of n rows predicted by q1, 5k = n)."""
    for _ in range(200):
        q32, q1 = dirichlet(rng, 1), dirichlet(rng, 1)
        for n, k in ((5, 1), (10, 2), (15, 3), (20, 4)):
            Q32, Q1 = np.repeat(q32, n, 0), np.repeat(q1, n, 0)
            P = Q32.copy()
            P[:k] = Q1[:k]
            reg = float(c1_means.tree_mean(hws_oracle.kl_rows(Q32, P)))
            gc = float(c1_means.tree_mean(hws_oracle.kl_rows(Q32, Q1)))
            if PredictiveMetrics.captured(reg, gc) == 0.8:
                return {1: Q1, 4: Q32.copy(), 32: Q32}, P
    raise AssertionError("no exact 0.8 construction found")


# ------------------------------------------------------------- pure reference checks

def test_reference_z_b23_value():
    z = NormalDist().inv_cdf(float(1 - Fraction(1, 80)))
    assert z == pytest.approx(2.2414027276049464, abs=1e-12)
    assert abs(z - 2.2414) < 1e-4


def test_reference_marginal_matches_reused(q):
    for K in (1, 4, 32):
        m = marg_ref(q[K])
        assert np.allclose(m, hws_oracle.circ_marginal(q[K], N_AXIAL), rtol=0, atol=1e-15)
        assert np.all(np.abs(m.sum(axis=1) - 1.0) <= TOL)
        for a in range(6):
            assert np.allclose(m[:, a], q[K][:, 6 * a:6 * a + 6].sum(axis=1), atol=1e-15)


def test_reference_kl_matches_reused(q):
    assert np.allclose(kl_ref(q[32], q[1]), hws_oracle.kl_rows(q[32], q[1]),
                       rtol=1e-12, atol=1e-15)


def test_reference_boundary_construction():
    Q, P = exact_boundary_rows(np.random.default_rng(616102))
    reg = float(c1_means.tree_mean(hws_oracle.kl_rows(Q[32], P)))
    gc = float(c1_means.tree_mean(hws_oracle.kl_rows(Q[32], Q[1])))
    assert PredictiveMetrics.captured(reg, gc) == 0.8


# ------------------------------------------------------------- softmax and naming

def test_softmax64_bitwise_s3_formula():
    need()
    rng = np.random.default_rng(616103)
    logits = (rng.normal(0.0, 6.0, size=(97, V))).astype(np.float32)
    l64 = logits.astype(np.float64)
    expected = np.exp(l64 - l64.max(axis=1, keepdims=True))
    expected /= expected.sum(axis=1, keepdims=True)
    got = he.softmax64(logits)
    assert got.dtype == np.float64 and got.shape == (97, V)
    assert np.array_equal(got, expected)


def test_to_canonical_random_perm_exact():
    need()
    rng = np.random.default_rng(616104)
    perm = rng.permutation(V)
    p_named = dirichlet(rng, 40)
    got = he.to_canonical(p_named, perm)
    expected = np.empty_like(p_named)
    for v in range(V):
        expected[:, v] = p_named[:, perm[v]]
    assert np.array_equal(got, expected)


def test_model_equal_to_q_reindexes_to_q(q):
    need()
    perm = np.random.default_rng(616105).permutation(V)
    p_named = np.empty_like(q[32])
    p_named[:, perm] = q[32]          # named symbol perm[v] carries canonical symbol v
    assert np.array_equal(he.to_canonical(p_named, perm), q[32])


# ------------------------------------------------------------- check_rows

def _two_col(x):
    """A row [x - 0.5, 0.5]: both entries and the sum x are exact in float64."""
    row = np.array([[x - 0.5, 0.5]])
    assert row.sum() == x
    return row


def test_check_rows_boundary_at_tolerance():
    need()
    up = 1.0 + 1e-6          # the last float x with x - 1 <= 1e-6 (a few ulp steps)
    while up - 1.0 > 1e-6:
        up = math.nextafter(up, 0.0)
    while math.nextafter(up, 2.0) - 1.0 <= 1e-6:
        up = math.nextafter(up, 2.0)
    down = 1.0 - 1e-6        # the last float y with 1 - y <= 1e-6
    while 1.0 - down > 1e-6:
        down = math.nextafter(down, 2.0)
    while 1.0 - math.nextafter(down, 0.0) <= 1e-6:
        down = math.nextafter(down, 0.0)
    for ok in (up, down):
        row = _two_col(ok)
        assert np.array_equal(he.check_rows(row), row)
    for bad in (math.nextafter(up, 2.0), math.nextafter(down, 0.0)):
        with pytest.raises(hc.HwsbStop) as ei:
            he.check_rows(_two_col(bad))
        assert stop_status(ei) == "FAIL_TECHNICAL/NUMERICAL"


@pytest.mark.parametrize("row", [[float("nan"), 1.0], [-0.1, 1.1], [float("inf"), 0.0]])
def test_check_rows_refuses_nan_negative_inf(row):
    need()
    p = np.array([[0.25, 0.75], row])
    with pytest.raises(hc.HwsbStop) as ei:
        he.check_rows(p)
    assert stop_status(ei) == "FAIL_TECHNICAL/NUMERICAL"


# ------------------------------------------------------------- B1

def test_b1_oracle_model_captures_all(q):
    need()
    res = he.b1(q, q[32].copy())
    assert abs(res["regret"]) <= TOL
    assert abs(res["captured"] - 1.0) <= TOL
    assert res["status"] == "PASS"
    assert res["n"] == q[32].shape[0]


def test_b1_last_symbol_model_captures_nothing(q):
    need()
    res = he.b1(q, q[1].copy())
    assert abs(res["captured"]) <= TOL
    assert abs(res["regret"] - res["G_C"]) <= TOL
    assert res["status"] == "FAIL"


def test_b1_regret_and_gc_match_reference(q):
    need()
    rng = np.random.default_rng(616106)
    p = dirichlet(rng, q[32].shape[0])
    res = he.b1(q, p)
    rows, gc_rows = kl_ref(q[32], p), kl_ref(q[32], q[1])
    n = rows.shape[0]
    regret = float(sum(Fraction(x) for x in rows) / n)
    g_c = float(sum(Fraction(x) for x in gc_rows) / n)
    assert res["regret"] == pytest.approx(regret, rel=1e-12)
    assert res["G_C"] == pytest.approx(g_c, rel=1e-12)
    assert res["captured"] == pytest.approx(1.0 - regret / g_c, rel=1e-12)
    assert res["regret_sd"] == pytest.approx(float(np.std(rows, ddof=1)), rel=1e-10)
    assert res["G_C_sd"] == pytest.approx(float(np.std(gc_rows, ddof=1)), rel=1e-10)
    assert res["regret_se"] == pytest.approx(float(np.std(rows, ddof=1)) / math.sqrt(n),
                                             rel=1e-10)
    assert res["status"] == ("PASS" if res["captured"] >= 0.8 else "FAIL")


def test_b1_equality_at_point_eight_passes_and_just_below_fails():
    need()
    Q, P = exact_boundary_rows(np.random.default_rng(616102))
    res = he.b1(Q, P)
    assert res["captured"] == 0.8
    assert res["status"] == "PASS"
    worse = P.copy()          # one more row slightly pulled towards q1: regret just larger
    worse[-1] = 0.999 * Q[32][-1] + 0.001 * Q[1][-1]
    reg = float(c1_means.tree_mean(hws_oracle.kl_rows(Q[32], worse)))
    gc = float(c1_means.tree_mean(hws_oracle.kl_rows(Q[32], Q[1])))
    expected = PredictiveMetrics.captured(reg, gc)
    assert 0.8 - 1e-3 < expected < 0.8
    res = he.b1(Q, worse)
    assert res["captured"] == expected
    assert res["status"] == "FAIL"


def test_b1_inconclusive_when_gc_at_floor(q):
    need()
    same = {1: q[32].copy(), 4: q[4], 32: q[32]}
    res = he.b1(same, q[4])
    assert res["G_C"] <= 1e-6
    assert res["status"] == "INCONCLUSIVE"
    near = 0.99999 * q[32] + 0.00001 * q[1]
    near /= near.sum(axis=1, keepdims=True)
    tiny = {1: near, 4: q[4], 32: q[32]}
    assert float(c1_means.tree_mean(hws_oracle.kl_rows(q[32], near))) <= 1e-6
    assert he.b1(tiny, q[4])["status"] == "INCONCLUSIVE"


# ------------------------------------------------------------- B2 and B3

def test_z_b23_constant():
    need()
    assert hc.Z_B23 == NormalDist().inv_cdf(float(1 - Fraction(1, 80)))
    assert hc.ALPHA_B23 == Fraction(1, 80)


def test_forcing_suffix_model_has_zero_gain(q):
    need()
    res = he.forcing(q[32], q[4], q[4].copy())
    assert abs(res["d_mean"]) <= TOL and res["d_mean"] == 0.0
    assert res["L"] <= 0
    assert not res["not_suffix_only"]
    assert float(res["ratio"]) == pytest.approx(1.0, abs=TOL)
    assert_forcing(res, forcing_ref(q[32], q[4], q[4], hc.Z_B23))
    b2 = he.b2(q, q[4].copy())
    assert b2["d_mean"] == 0.0 and b2["L"] <= 0 and not b2["not_suffix_only"]


def test_forcing_oracle_model_has_positive_lower_bound(q):
    need()
    ref = forcing_ref(q[32], q[4], q[32], hc.Z_B23)
    assert ref["G_hat"] > 0 and ref["L"] > 0
    res = he.forcing(q[32], q[4], q[32].copy())
    assert_forcing(res, ref)
    assert float(res["ratio"]) == 0.0
    assert bool(res["not_suffix_only"]) is True
    assert_forcing(he.b2(q, q[32].copy()), ref)


def test_forcing_general_and_explicit_z(q):
    need()
    p = dirichlet(np.random.default_rng(616107), q[32].shape[0])
    assert_forcing(he.forcing(q[32], q[4], p), forcing_ref(q[32], q[4], p, hc.Z_B23))
    assert_forcing(he.forcing(q[32], q[4], p, z=1.0), forcing_ref(q[32], q[4], p, 1.0))
    assert_forcing(he.b2(q, p), forcing_ref(q[32], q[4], p, hc.Z_B23))


def test_forcing_ratio_undefined_without_gain(q):
    need()
    res = he.forcing(q[32], q[32].copy(), q[4])
    assert res["G_hat"] == 0.0
    assert res["ratio"] == "undefined"


def test_b3_is_forcing_on_circular_marginals(q):
    need()
    p = dirichlet(np.random.default_rng(616108), q[32].shape[0])
    c = {K: marg_ref(q[K]) for K in (4, 32)}
    cp = marg_ref(p)
    for x in (c[4], c[32], cp):
        assert np.all(np.abs(x.sum(axis=1) - 1.0) <= TOL)
    res = he.b3(q, p)
    assert_forcing(res, forcing_ref(c[32], c[4], cp, hc.Z_B23))
    reused = {K: hws_oracle.circ_marginal(q[K], 6) for K in (4, 32)}
    exact = he.forcing(reused[32], reused[4], hws_oracle.circ_marginal(p, 6))
    for key in ("G_hat", "r", "d_mean", "se", "L"):
        assert res[key] == exact[key], key
    assert res["not_suffix_only"] == exact["not_suffix_only"]


def test_b3_suffix_model_zero_and_oracle_positive(q):
    need()
    assert he.b3(q, q[4].copy())["d_mean"] == 0.0
    ref = forcing_ref(marg_ref(q[32]), marg_ref(q[4]), marg_ref(q[32]), hc.Z_B23)
    assert_forcing(he.b3(q, q[32].copy()), ref)
