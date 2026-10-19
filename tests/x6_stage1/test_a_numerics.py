"""Author A: T-LOGTAB, T-EB and T-STAT (X6S1-FROZEN-v1 §4.7, §7.3-§7.5, §10.2 T14-T16/T21/T27,
§14.3; API.md §7 score/qstar, §8, §9 learned_*).

References here: Decimal logarithms at 110-140 digits, an independent Decimal evaluation of
Theorem EB, exact trinomial coverage enumeration, a full-row multinomial enumerator and replays of
the registered bootstrap draws on the same generator. All inputs are synthetic."""
from __future__ import annotations

import itertools
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_data as sd  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_stats as ss  # noqa: E402
import x6s1_decide as sdc  # noqa: E402

if str(REPO / "tools" / "x6_stage0") not in sys.path:  # reused code (the modules add it too)
    sys.path.append(str(REPO / "tools" / "x6_stage0"))
import x6_model as xm  # noqa: E402
from topo_pilot.contracts import SeedTree  # noqa: E402

EPS = Fraction(1, 10**6)
G8_S = "0.0088553050512358844408577637624772307516013467873269249611029142273162701006695055"
G8_LO = Fraction(G8_S)


def D(fr, prec):
    with localcontext() as c:
        c.prec = prec
        return Decimal(Fraction(fr).numerator) / Decimal(Fraction(fr).denominator)


def ref_ln(x, prec=110):
    with localcontext() as c:
        c.prec = prec
        return D(x, prec + 10).ln()


def ref_xlnx(x, prec=140):
    with localcontext() as c:
        c.prec = prec
        return D(x, prec + 10) * ref_ln(x, prec)


def my_qvals():
    out = {Fraction(1, 5), Fraction(1, 15)}
    for m in range(1, 33):
        lm = Fraction(49, 50) ** m
        out |= {Fraction(1, 5) * (lm + (1 - lm) / 3), Fraction(1, 5) * (1 - lm) / 3}
    return (Fraction(0),) + tuple(sorted(out))


def nearest(f, ref):
    """f is the float64 nearest to the Decimal ref (both neighbours are no closer)."""
    err = abs(Decimal(f) - ref)
    return all(abs(Decimal(math.nextafter(f, d)) - ref) >= err for d in (-math.inf, math.inf))


# ---------------------------------------------------------------- T-LOGTAB
def test_qvals_independent_set():
    assert tuple(ss.qvals()) == my_qvals() and len(my_qvals()) == 67


@pytest.mark.parametrize("kind", ["ln", "qlnq"])
def test_table_entries_against_independent_decimal(kind):
    Q = 2**20
    xs = [(1 - EPS) * Fraction(k, Q) + EPS / 18 for k in (0, 1, 2, 3, 1000, Q // 3, Q - 1, Q)]
    xs += list(my_qvals()[1:])
    for x in xs:
        e = ss.table_entry(x, kind)
        v80, v120 = Decimal(str(e["v80"])), Decimal(str(e["v120"]))
        want = ref_ln(x, 140) if kind == "ln" else ref_xlnx(x, 140)
        assert abs(v80 - want) <= Decimal("1e-76")
        assert abs(v120 - want) <= Decimal("1e-115")
        assert abs(v80 - v120) <= Decimal("1e-60")            # enclosure diagnostic (T14)
        assert e["float"] == float(v80) and nearest(e["float"], want)


@lru_cache(maxsize=None)
def small_tables():
    return ss.log_tables(Q=1024, eps=EPS)


def test_log_tables_small_q_complete_and_correctly_rounded():
    tab = small_tables()
    lnp = tab["lnp"]
    assert lnp.dtype == np.float64 and lnp.shape == (1025,)
    for k in range(1025):
        want = ref_ln((1 - EPS) * Fraction(k, 1024) + EPS / 18)
        assert lnp[k] == float(want), k
    qv = my_qvals()
    assert [Fraction(s) for s in tab["qvals"]] == list(qv)
    assert tab["fl_q"].tolist() == [float(q) for q in qv]
    assert tab["qlnq"][0] == 0.0 and tab["fl_q"][0] == 0.0
    for i in range(1, len(qv)):
        assert tab["qlnq"][i] == float(ref_xlnx(qv[i]))
    assert Decimal(tab["max_diag"]) <= Decimal("1e-60")
    assert len(tab["sha256"]) == 64 and tab["sha256"] == small_tables.__wrapped__()["sha256"]


def test_score_e_row_check_against_80_digit_decimal():
    """§7.4 item 3 / T15: |x_hat - X| <= 1e-13 with X recomputed in 80-digit Decimal."""
    tab, rng = small_tables(), np.random.default_rng(12)
    toks = np.zeros((60, 33), np.uint8)
    for i in range(60):
        v = int(rng.integers(16))
        for c in range(33):
            toks[i, c] = 15 + int(rng.integers(3)) if v == 10 else xm.tok(v)
            v = xm.NEIGHBOURS[v][int(rng.integers(5))]
    for t in (1, 12, 32):
        q, codes = se.qstar("NA", toks, t)
        k = np.array([rng.multinomial(1024, row / row.sum()) for row in q], np.int64)
        xhat = se.score(codes, k, tab)
        assert xhat.dtype == np.float64 and xhat.shape == (60,)
        for i in range(60):
            law = xm.closed_form("NA", tuple(int(w) for w in toks[i, :t]))["q"]
            with localcontext() as c:
                c.prec = 80
                X = sum((D(a, 90) * (ref_ln(a, 90) - ref_ln((1 - EPS) * Fraction(int(kj), 1024)
                                                            + EPS / 18, 90))
                         for a, kj in zip(law, k[i]) if a), Decimal(0))
            assert abs(Decimal(float(xhat[i])) - X) <= Decimal("1e-13")


@pytest.mark.slow
def test_full_log_tables_spot_checks():
    tab, Q = ss.log_tables(), 2**20
    assert tab["lnp"].shape == (Q + 1,)
    for k in [0, 1, 2, 3, Q // 7, Q - 1, Q] + list(np.random.default_rng(1).integers(0, Q, 40)):
        assert tab["lnp"][int(k)] == float(ref_ln((1 - EPS) * Fraction(int(k), Q) + EPS / 18))


# ---------------------------------------------------------------- T-EB
def my_U(xbar, zbar, n, delta, B=17, prec=100):
    """Theorem EB (§7.3), delta1 = delta2 = delta/2, plain high-precision evaluation."""
    with localcontext() as c:
        c.prec = prec
        m = n // 2
        L = D(Fraction(2) / Fraction(delta), prec).ln()
        a = B * (L / m).sqrt()
        b = B * B * L / (12 * m)
        sig = (a + (a * a + 4 * (D(zbar, prec) + b)).sqrt()) / 2
        return D(xbar, prec) + sig * (2 * L / n).sqrt() + B * L / (3 * n)


CASES = [(Fraction(1, 1000), Fraction(1, 10**4), 2**21, Fraction(1, 160)),
         (Fraction(0), Fraction(0), 2**21, Fraction(1, 160)),
         (Fraction(3, 1000), Fraction(5, 10**3), 2**21, Fraction(1, 40)),
         (Fraction(1), Fraction(2), 8, Fraction(1, 10)),
         (Fraction(17), Fraction(0), 4, Fraction(1, 10))]


@pytest.mark.parametrize("xbar,zbar,n,delta", CASES)
def test_eb_bound_outward_against_independent_decimal(xbar, zbar, n, delta):
    u = ss.eb_bound(xbar, zbar, n, delta)
    ref = my_U(xbar, zbar, n, delta)
    assert isinstance(u, Decimal) and u >= ref and u - ref <= Decimal("1e-50")    # T16
    assert abs(Decimal(ss.eb_reference(xbar, zbar, n, delta)) - ref) <= Decimal("1e-70")


def test_eb_constants_registered_table():
    table = {Fraction(1, 160): (5.768321, 3.98725e-2, 1.32485e-4, 1.55865e-5, 2.34544e-3),
             Fraction(1, 40): (4.382027, 3.47525e-2, 1.00645e-4, 1.18406e-5, 2.04427e-3)}
    for delta, vals in table.items():
        c = ss.eb_constants(delta, 2**21)
        for key, want in zip(("L", "a", "b", "BL3n", "sqrt2Ln"), vals):
            assert float(Decimal(c[key])) == pytest.approx(want, rel=1e-5), key   # 6-digit table
        L = ref_ln(Fraction(2) / delta)
        assert L <= Decimal(c["L"]) <= L + Decimal("1e-54")
    w = my_U(0, 0, 2**21, Fraction(1, 160))                  # zero-variance width (§7.3 remark)
    assert float(w) == pytest.approx(1.163e-4, rel=1e-3)


def test_eb_monotone_in_xbar_and_zbar():
    n, d = 2**21, Fraction(1, 160)
    base = ss.eb_bound(Fraction(2, 1000), Fraction(1, 1000), n, d)
    assert ss.eb_bound(Fraction(2, 1000) + Fraction(1, 10**9), Fraction(1, 1000), n, d) > base
    assert ss.eb_bound(Fraction(2, 1000), Fraction(11, 10000), n, d) > base
    assert ss.eb_bound(Fraction(2, 1000), Fraction(9, 10000), n, d) < base


@pytest.mark.parametrize("delta", [Fraction(1, 10), Fraction(1, 160)])
def test_eb_exact_coverage_two_point_laws(delta):
    """X in {0, B}: pair types (both 0, mixed, both B) are trinomial; P(mu <= U) >= 1 - delta."""
    B, fact = 17, math.factorial
    grid = [Fraction(k, 40) for k in range(41)] + [Fraction(1, 1000), Fraction(1, 100),
                                                   Fraction(999, 1000)]
    for m in (2, 4, 8, 16):
        n = 2 * m
        U = {(j, l): Fraction(ss.eb_bound(Fraction(B * (j + 2 * l), n), Fraction(j * B * B, 2 * m),
                                          n, delta))
             for j in range(m + 1) for l in range(m + 1 - j)}
        for p in grid:
            q0, q1, q2 = (1 - p) ** 2, 2 * p * (1 - p), p * p
            cov = sum(Fraction(fact(m), fact(m - j - l) * fact(j) * fact(l))
                      * q0 ** (m - j - l) * q1 ** j * q2 ** l
                      for (j, l), u in U.items() if p * B <= u)
            assert cov >= 1 - delta, (m, p)


def test_outward_inputs_exact():
    x = np.random.default_rng(5).uniform(0, 0.05, 1024)
    e = Fraction(1, 10**12)
    xp, zp = ss.outward_inputs(x)
    fx = [Fraction(float(v)) for v in x]
    assert xp == sum(fx) / 1024 + e
    assert zp == sum((abs(fx[2 * k] - fx[2 * k + 1]) + 2 * e) ** 2 / 2 for k in range(512)) / 512
    xp2, _ = ss.outward_inputs(x, e_row=Fraction(0))
    assert xp2 == sum(fx) / 1024


def test_eb_report_is_outward_bound_without_separation_term():
    x = np.random.default_rng(6).uniform(0, 0.02, 4096)
    for d in (Fraction(1, 160), Fraction(1, 40)):
        rep = ss.eb_report(x, d)
        xp, zp = ss.outward_inputs(x)
        assert Decimal(rep["U"]) == ss.eb_bound(xp, zp, 4096, d)        # U_report = U+ (RC1)
        assert rep["n"] == 4096 and rep["xbar"] == pytest.approx(float(np.mean(x)), rel=1e-12)
        assert abs(Fraction(rep["xbar_plus"]) - xp) <= Fraction(1, 10**40)
        fx = [Fraction(float(v)) for v in x]
        inner = my_U(sum(fx) / 4096, sum((fx[2 * k] - fx[2 * k + 1]) ** 2 / 2
                                         for k in range(2048)) / 2048, 4096, d)
        assert Decimal(rep["U"]) >= inner


# ---------------------------------------------------------------- T-STAT
def full_row_law(N, inf):
    law = {}
    for seq in itertools.product(range(N), repeat=N):
        c = tuple(seq.count(i) for i in inf)
        law[c] = law.get(c, 0) + Fraction(1, N ** N)
    return law


def two_stage_by_hand(N, n_inf):
    law, p = {}, Fraction(n_inf, N)
    for M in range(N + 1):
        pm = math.comb(N, M) * p ** M * (1 - p) ** (N - M)
        for seq in itertools.product(range(n_inf), repeat=M):
            c = tuple(seq.count(i) for i in range(n_inf))
            law[c] = law.get(c, 0) + pm * Fraction(1, n_inf ** M)
    return law


def test_two_stage_bootstrap_equals_full_row_multinomial():
    for N, inf in ((1, (0,)), (3, (1,)), (4, (0, 3)), (5, (1, 2, 4)), (6, (0, 5)), (6, (2, 3, 4))):
        want = full_row_law(N, inf)
        assert two_stage_by_hand(N, len(inf)) == want
        # API-AMBIGUITY: 'informative' read as the informative row indices; the law depends on
        # their number only, so an int-count signature is accepted as the same reading.
        try:
            got = ss.two_stage_law(N, list(inf))
        except TypeError:
            got = ss.two_stage_law(N, len(inf))
        assert {tuple(k): Fraction(v) for k, v in got.items()} == want


def test_cord_draws_replays_registered_scheme_and_common_indices():
    rng = np.random.default_rng(8)
    n_inf, N, B = 37, 500, 300
    den = rng.integers(1, 9, n_inf).astype(np.float64)
    base = rng.integers(-5, 6, n_inf).astype(np.float64)
    num = np.stack([base, base, 2 * base, den, -base])
    ns, ds = ss.cord_draws(num, den, N, B, np.random.default_rng(77))
    assert ns.shape == (B, 5) and ds.shape == (B,)
    g = np.random.default_rng(77)
    for b in range(B):
        M = g.binomial(N, n_inf / N)
        c = np.bincount(g.integers(0, n_inf, size=M), minlength=n_inf)
        assert ns[b].tolist() == (num @ c).tolist() and ds[b] == den @ c
    assert np.array_equal(ns[:, 0], ns[:, 1]) and np.array_equal(ns[:, 2], 2 * ns[:, 0])
    assert np.array_equal(ns[:, 3], ds) and np.array_equal(ns[:, 4], -ns[:, 0])


def test_ctrl_max_is_taken_inside_each_draw():
    rng = np.random.default_rng(9)
    betas = rng.normal(0.0, 0.05, (500, 16))         # columns: NA s1..4, init, AB, ZC
    adj = np.array([[betas[b, s] - sdc.ctrl(betas[b, 4 + s], list(betas[b, 8:12]),
                                             list(betas[b, 12:16])) for s in range(4)]
                    for b in range(500)])
    m_ab, m_zc = betas[:, 8:12].mean(1, keepdims=True), betas[:, 12:16].mean(1, keepdims=True)
    want = betas[:, :4] - np.maximum(betas[:, 4:8], np.maximum(m_ab, m_zc))
    assert np.allclose(adj, want, atol=1e-15)
    assert sdc.ctrl(0.1, [0.0, 0.0, 0.4, 0.0], [0.0] * 4) == 0.1
    assert sdc.ctrl(0.0, [0.4, 0.4, 0.4, 0.4], [0.0] * 4) == pytest.approx(0.4)
    assert sdc.ctrl(None, [0.0] * 4, [0.0] * 4) is None
    assert sdc.ctrl(0.0, [0.0, float("nan"), 0.0, 0.0], [0.0] * 4) is None


def test_boot_means_beta_and_stream():
    x = np.random.default_rng(10).integers(0, 50, 333).astype(np.float64)
    den = np.random.default_rng(11).integers(1, 4, 333).astype(np.float64)
    bm = ss.boot_means(x, 200, np.random.default_rng(3))
    bb = ss.boot_beta(x, den, 200, np.random.default_rng(3))
    g = np.random.default_rng(3)
    for b in range(200):
        idx = g.integers(0, 333, size=333)
        assert bm[b] == pytest.approx(x[idx].mean(), rel=1e-15)
    g = np.random.default_rng(3)
    for b in range(200):
        idx = g.integers(0, 333, size=333)
        assert bb[b] == x[idx].sum() / den[idx].sum()
    for sid, model in (("learn", "NA-s1"), ("cord", None), ("cseed", "s2")):
        want = SeedTree(sd.DATA_MASTER).generator("x6s1", "boot", sid, *([model] if model else []))
        got = ss.boot_stream(sid, model) if model else ss.boot_stream(sid)
        assert np.array_equal(got.integers(0, 2**62, 8), want.integers(0, 2**62, 8))
    assert ss.boot_stream("learn", "NA-s1").integers(0, 2**62) != \
        ss.boot_stream("learn", "NA-s2").integers(0, 2**62)


def test_quantile_wrapper_levels():
    assert ss.LB_975 == 0.025 and ss.UB_975 == 0.975
    assert ss.quantile(np.arange(101), ss.LB_975) == 2.5
    assert ss.quantile(np.arange(101), ss.UB_975) == 97.5
    x = np.random.default_rng(13).normal(size=2001)
    for lev in (0.025, 0.975, 0.5):
        assert ss.quantile(list(x), lev) == float(np.quantile(x, lev, method="linear"))


def test_tail_diagnostics_d1_d2():
    rng = np.random.default_rng(14)
    den = np.ones(1000)
    num = np.stack([rng.uniform(-1, 1, 1000), rng.uniform(-1, 1, 1000)])
    draws = rng.normal(0.3, 0.01, 2000)
    lb = ss.quantile(draws, 0.025)
    out = ss.tail(num, den, 0.3, lb, draws)
    sd_ = np.std(draws, ddof=1)
    assert out["D1"] and out["D2"] and out["status"] == "PASS"
    assert out["lb_norm"] == pytest.approx(0.3 - 1.959964 * sd_, abs=1e-14)
    edge = num.copy()
    edge[1, 5] = 10.0                                     # = 0.01 * sum(den): still allowed
    assert ss.tail(edge, den, 0.3, lb, draws)["D1"]
    edge[1, 5] = -10.5
    bad = ss.tail(edge, den, 0.3, lb, draws)
    assert not bad["D1"] and bad["status"] == "FAIL"
    far = ss.tail(num, den, 0.3, (0.3 - 1.959964 * sd_) - 0.03, draws)
    assert not far["D2"] and far["status"] == "FAIL"


def test_gate_pass_fail_unresolved():
    lo = float(G8_LO)
    while Fraction(lo) >= G8_LO:
        lo = math.nextafter(lo, 0)
    hi = math.nextafter(lo, math.inf)                      # first float >= G8_LO (never equal)
    assert sdc.learned_val(lo, G8_LO) == "PASS" and sdc.learned_val(hi, G8_LO) == "FAIL"
    for bad in (None, float("nan"), float("inf")):
        assert sdc.learned_val(bad, G8_LO) == "UNRESOLVED"
    assert sdc.learned_val(0.001, G8_LO, nonfinite=True) == "FAIL"
    cases = {("PASS", "FAIL"): "GO", ("FAIL", "PASS"): "GO", ("PASS", "UNRESOLVED"): "GO",
             ("FAIL", "FAIL"): "NOT_LEARNED", ("FAIL", "UNRESOLVED"): "LEARNING_UNRESOLVED",
             ("UNRESOLVED", "UNRESOLVED"): "LEARNING_UNRESOLVED"}
    for (a, b), want in cases.items():
        assert sdc.learn_decision(a, b) == want
    s = "0.0088553050512358844408577637624772307516013467873269249611029142273162701006695055"
    assert sdc.learned_test(s, G8_LO) == "FAIL"           # equality is not below
    with localcontext() as c:
        c.prec = 120
        below = str(Decimal(s) - Decimal("1e-82"))
    assert sdc.learned_test(below, G8_LO) == "PASS"
    assert sdc.learned_test(None, G8_LO) == "UNRESOLVED"
    assert sdc.learned_test("NaN", G8_LO) == "UNRESOLVED"
