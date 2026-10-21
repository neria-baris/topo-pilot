"""Author B (job 0101): T-R1 (RC-14, NEW-3), T-N2 (RC-6), T-CMODE (RC-5, RC-6).

C2-FROZEN-v1 §13.3, §2.10, §2.11, §3.2, §6.4-§6.6; API.md §6.2, §8.3-§8.5, §10, §11. Written
from the protocol, API.md and CONTRACT.json only; tools/c2_readout/*.py never read. Synthetic
fixtures only.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402,F401  (first: the sys.path convention)
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_decide as cdc  # noqa: E402
import c2_oracle as co2  # noqa: E402
import c1_fit  # noqa: E402
import c1_gates  # noqa: E402

from topo_pilot.analysis import x4f_scores  # noqa: E402

RADIAL = "EXCLUDED/RADIAL_SUPPORT"


def _m(angle, r=0.5):
    a = np.asarray(angle, dtype=np.float64)
    return np.column_stack((r * np.cos(a), r * np.sin(a)))


def _r1(pp, pm, ap, am, mod_p=None, mod_m=None, thr=1e-12, mp=None, mm=None):
    n = len(pp)
    mod_p = np.ones(n) if mod_p is None else np.asarray(mod_p, dtype=float)
    mod_m = np.ones(n) if mod_m is None else np.asarray(mod_m, dtype=float)
    mp = _m(ap) if mp is None else mp
    mm = _m(am) if mm is None else mm
    return ck.r1(np.asarray(pp, float), np.asarray(pm, float), mod_p, mod_m, mp, mm, thr)


# ---- T-R1 ----
def test_r1_without_overrides_reproduces_c1_gates_v1_bitwise():
    rng = np.random.default_rng(141)
    n = 40
    pp, pm = rng.uniform(-np.pi, np.pi, n), rng.uniform(-np.pi, np.pi, n)
    ap, am = rng.uniform(-np.pi, np.pi, n), rng.uniform(-np.pi, np.pi, n)
    res = _r1(pp, pm, ap, am)
    ref = c1_gates.v1(pp, pm, _m(ap), _m(am))
    assert res["agreement"] == ref["agreement"] and res["median"] == ref["median"]
    assert res["n"] == ref["n"] and res["overrides"] == {"zero_mod": 0, "zero_code": 0}
    assert res["status"] == ("PASS" if Fraction(ref["agreement"]) >= Fraction(3, 4) else "FAIL")
    dc = c1_gates.wrap(pp - pm)
    ds = c1_gates.wrap(np.arctan2(_m(ap)[:, 1], _m(ap)[:, 0]) - np.arctan2(_m(am)[:, 1],
                                                                          _m(am)[:, 0]))
    kappa = float(np.sum(dc * np.sign(ds)) / np.sum(np.abs(ds)))
    assert res["kappa_reg"] == pytest.approx(kappa, rel=1e-12, abs=1e-15)


def test_r1_wraps_at_plus_minus_pi():
    k = np.array([0.0, 0.01, 0.02, 0.03])
    pp, pm = np.pi - 0.1 - k, -np.pi + 0.1 + k  # raw difference ~ +2pi - 0.2: wrapped < 0
    ap, am = 3.0 + k, -3.0 - k  # raw difference ~ +6: wrapped 6 - 2pi < 0
    res = _r1(pp, pm, ap, am)
    assert res["agreement"] == 1.0 and res["status"] == "PASS"


def test_r1_sign_zero_is_disagreement_and_three_quarters_passes():
    ap, am = np.full(4, 0.5), np.zeros(4)  # equal |delta*|: every row selected
    pm = np.zeros(4)
    res = _r1(np.array([0.3, 0.3, 0.0, 0.3]), pm, ap, am)
    assert res["n"] == 4 and res["agreement"] == 0.75 and res["status"] == "PASS"
    assert res["R1_ZERO"] == 1
    res = _r1(np.array([0.3, 0.0, 0.0, 0.3]), pm, ap, am)
    assert res["agreement"] == 0.5 and res["status"] == "FAIL"


def test_r1_median_ties_use_inverted_cdf():
    ap, am = np.array([0.1, 0.1, 0.2, 0.2]), np.zeros(4)
    pp = np.array([-0.3, -0.3, 0.3, 0.3])  # the two small-|delta*| rows disagree
    res = _r1(pp, np.zeros(4), ap, am)
    small = abs(float(np.arctan2(_m(0.1)[0, 1], _m(0.1)[0, 0])))
    assert res["median"] == pytest.approx(small, rel=1e-15)  # rank 2 of 4, not the midpoint
    assert res["n"] == 4 and res["agreement"] == 0.5 and res["status"] == "FAIL"


def test_r1_zero_modulus_override_before_median_and_no_row_deleted():
    pp, pm = np.array([0.4, 0.2, 0.4, 0.6]), np.zeros(4)
    ap, am = np.array([0.0, 0.2, 0.4, 0.6]), np.array([2.0, 0.0, 0.0, 0.0])
    mp, mm = _m(ap), _m(am)
    mp[0] = (1e-12, 0.0)  # |m32| = 1e-12 exactly: <= 1e-12 -> delta* := 0
    res = _r1(pp, pm, ap, am, mp=mp, mm=mm)
    sub_p, sub_m = mp.copy(), mm.copy()
    sub_p[0] = sub_m[0] = (1.0, 0.0)  # the wrapper's input substitution
    ref = c1_gates.v1(pp, pm, sub_p, sub_m)
    assert (res["agreement"], res["median"], res["n"]) == (ref["agreement"], ref["median"],
                                                           ref["n"])
    assert res["n"] == 3  # |delta*| = 0 entered the median (deleting the row would give 2)
    assert res["overrides"]["zero_mod"] == 1 and res["R1_UNSELECTED"] == 1
    mp2 = mp.copy()
    mp2[0] = (1e-13, 1e-13)  # tiny but non-zero: still overridden
    assert _r1(pp, pm, ap, am, mp=mp2, mm=mm)["overrides"]["zero_mod"] == 1
    mp3 = mp.copy()
    mp3[0] = (2e-12, 0.0)  # above the threshold: not overridden
    assert _r1(pp, pm, ap, am, mp=mp3, mm=mm)["overrides"]["zero_mod"] == 0


def test_zero_code_threshold_and_override():
    assert ck.zero_code_threshold(np.array([1.0, 2.0, 3.0, 4.0])) == 1e-12 * 2.0
    assert ck.zero_code_threshold(np.array([5.0, 1.0, 5.0, 1.0, 5.0])) == 1e-12 * 5.0
    thr = 2e-12
    pp, pm = np.full(4, 0.3), np.zeros(4)
    ap, am = np.full(4, 0.5), np.zeros(4)
    mod_p, mod_m = np.ones(4), np.ones(4)
    mod_p[0], mod_m[1], mod_p[2] = thr, thr / 2, 2 * thr  # rows 0, 1 overridden (<=)
    res = _r1(pp, pm, ap, am, mod_p=mod_p, mod_m=mod_m, thr=thr)
    sub_p, sub_m = pp.copy(), pm.copy()
    sub_p[:2] = sub_m[:2] = 0.0
    ref = c1_gates.v1(sub_p, sub_m, _m(ap), _m(am))
    assert res["agreement"] == ref["agreement"] == 0.5 and res["status"] == "FAIL"
    assert res["overrides"]["zero_code"] == 2 and res["R1_ZERO"] == 2


def test_r1_failure_routes_to_cnhs():
    # API-AMBIGUITY: API.md 11.2 overall(family, statuses, cnhs) does not define `cnhs`; it is
    # read as the list of CNHS models (protocol 6.5 rule 2, 7 row 16).
    statuses = {1729: "CNHS", 2718: "CNHS", 3141: "USED"}
    expect = {"R": "CIRCLE_NOT_HISTORY_SENSITIVE", "M": "CNHS-2",
              "S*": "X_PHASE_NOT_HISTORY_SENSITIVE"}
    for fam, outcome in expect.items():
        assert cdc.overall(fam, statuses, [1729, 2718]) == outcome


def test_masked_oracle_phase_features():
    m32 = np.array([[0.3, 0.4], [0.0, 0.0], [1e-12, 0.0], [2e-12, 0.0], [-0.5, 0.0]])
    phi, valid = co2.phi_star(m32)
    assert valid.tolist() == [True, False, False, True, True]
    assert phi[1] == 0.0 and phi[2] == 0.0  # placeholder only
    assert phi[0] == pytest.approx(np.arctan2(0.4, 0.3)) and phi[4] == pytest.approx(np.pi)
    f3, mv = ck.fstar(m32, 3)
    assert f3.shape == (5, 6) and mv.tolist() == valid.tolist()
    assert np.array_equal(f3[1], np.zeros(6)) and np.array_equal(f3[2], np.zeros(6))
    assert np.max(np.abs(f3[valid] - ck.harmonics(phi[valid], 3))) <= 1e-15
    f1 = ck.fstar(m32, 1)[0]  # the L1* target
    assert np.array_equal(f1[~valid], np.zeros((2, 2)))  # never the (1, 0) pairs


def test_s_star_fit_uses_masked_regressors_and_is_deterministic():
    rng = np.random.default_rng(1488)
    n = 36 * 20
    w32, zt = np.repeat(np.arange(36), 20), rng.standard_normal((n, 5))
    m32 = _m(rng.uniform(-np.pi, np.pi, n), r=0.4)
    m32[::50] = 0.0  # ZERO_MOD rows
    f = ck.fstar(m32, 3)[0]
    Y = rng.standard_normal((n, 127))
    a, b = ck.fwl(Y, w32, zt, f), ck.fwl(Y, w32, zt, f)
    for key in ("alpha", "Gamma", "B", "resid"):
        assert np.array_equal(a[key], b[key]), key
    X = c1_fit.fwl_design(w32, zt, f)
    assert np.array_equal(X[::50, 41:], np.zeros((len(X[::50]), 6)))
    coef = np.linalg.lstsq(X, Y, rcond=None)[0]
    assert np.max(np.abs(a["B"] - coef[41:].T)) <= 1e-12


# ---- T-N2 ----
def test_n2_fit_class_mean_mahalanobis_and_q99():
    rng = np.random.default_rng(2610)
    w = np.repeat(np.arange(36), 40)
    mu_true = 3.0 * rng.standard_normal((36, 128))
    a2 = mu_true[w] + rng.standard_normal((len(w), 128)) @ np.diag(np.linspace(0.5, 2, 128))
    fit = ck.n2_fit(a2, w)
    mu = np.vstack([a2[w == c].mean(axis=0) for c in range(36)])
    assert np.max(np.abs(fit["mu"] - mu)) <= 1e-12
    S = x4f_scores.ledoit_wolf(a2 - mu[w])[1]
    W = fit["W"]
    assert np.max(np.abs(W - W.T)) <= 1e-12 and np.max(np.abs(W @ S @ W - np.eye(128))) <= 1e-9
    dm = np.linalg.norm((a2 - mu[w]) @ W.T, axis=1)
    assert np.max(np.abs(ck.dm(a2, w, fit) - dm)) <= 1e-12 * np.max(dm)
    assert fit["q99"] == pytest.approx(c1_gates.q99(dm), rel=1e-12)
    bad = ck.n2_fit(a2[w != 7], w[w != 7])  # a class without FIT rows
    assert bad["status"] == RADIAL


def _states(norms):
    return np.column_stack((np.asarray(norms, dtype=float), np.zeros(len(norms))))


def _fixed_fit():
    return {"mu": np.zeros((36, 2)), "W": np.eye(2), "q99": 1.0, "status": "PASS"}


@pytest.mark.parametrize("d_beyond, s_beyond, status", [
    (4, 6, "PASS"), (4, 7, RADIAL), (0, 5, "PASS"), (0, 6, RADIAL)])
def test_n2_fraction_rule_and_cap_exact(d_beyond, s_beyond, status):
    # API-AMBIGUITY: API.md 8.4 sizes the states [., 128]; these fixtures (and the protocol's
    # paired-Gaussian counterexample) are two-dimensional, read as dimension-agnostic.
    def arms(k):  # 100 (row, arm) states, k strictly beyond q99 = 1 (one exactly at 1.0)
        norms = [2.0] * k + [1.0] + [0.5] * (99 - k)
        return [_states(norms[:50]), _states(norms[50:])]
    w = np.arange(50) % 36
    res = ck.n2_gate(_fixed_fit(), w, arms(d_beyond), arms(s_beyond), arms(1))
    assert res["F_D"] == d_beyond / 100 and res["F_S"] == s_beyond / 100
    cap = max(Fraction(1, 20), Fraction(d_beyond, 100) + Fraction(1, 50))
    assert Fraction(res["cap"]).limit_denominator(1000) == cap
    assert res["status"] == status


def test_n2_paired_gaussian_counterexample_passes_the_radial_screen():
    rng = np.random.default_rng(6060)
    w_fit = np.repeat(np.arange(36), 1000)
    fit = ck.n2_fit(rng.standard_normal((len(w_fit), 2)), w_fit)
    n = 20000
    w = rng.integers(0, 36, n)
    D2, S, C, src = [], [], [], []
    for _ in range(2):  # arms + and -
        s, t = rng.standard_normal(n), rng.standard_normal(n)
        src.append(np.column_stack((s, t)))
        D2.append(np.column_stack((t, s)))  # the natural donor state
        S.append(np.column_stack((t, t)))  # first-coordinate swap
        C.append(np.column_stack((s, s)))
    res = ck.n2_gate(fit, w, D2, S, C)
    assert res["status"] == "PASS"
    assert abs(res["F_S"] - 0.0319) <= 0.006 and res["F_S"] < 0.05  # P(2t^2 > 9.2103)
    assert abs(res["F_D"] - 0.01) <= 0.004
    assert np.corrcoef(S[0][:, 0], S[0][:, 1])[0, 1] == pytest.approx(1.0, abs=1e-12)
    assert abs(np.corrcoef(src[0][:, 0], src[0][:, 1])[0, 1]) < 5 / np.sqrt(n)
    words = [v for v in res.values() if isinstance(v, str)]
    assert all("natural" not in v.lower() for v in words)


# ---- T-CMODE ----
def _oblique(rng, p=128, k=6):
    A, Wm = rng.standard_normal((p, k)), rng.standard_normal((k, p))
    return A @ np.linalg.solve(Wm @ A, Wm)


def test_cm_replacements_F_S_C():
    rng = np.random.default_rng(7070)
    H, D = rng.standard_normal((9, 128)), rng.standard_normal((9, 128))
    P2 = _oblique(rng)
    r = ca.cm_replacements(H, D, P2)
    assert np.array_equal(r["F"], D)
    assert np.max(np.abs(r["S"] - (H + (D - H) @ P2.T))) <= 1e-12
    assert np.max(np.abs(r["C"] - (H + (D - H) @ (np.eye(128) - P2).T))) <= 1e-12
    assert np.max(np.abs((r["S"] - H) + (r["C"] - H) - (D - H))) <= 1e-12


def _cancellation():
    rng = np.random.default_rng(8080)
    n = 64
    q1, q2 = rng.dirichlet(np.ones(36), n), rng.dirichlet(np.ones(36), n)
    d = q1 - q2
    v = 2.0 * d / np.sum(d * d, axis=1, keepdims=True)  # 1/2 d.v = 1 on every row
    base = rng.standard_normal((n, 36))
    z = {"F": (base, base.copy()), "S": (base + v, base), "C": (base - v, base)}
    return d, z, np.ones(n)


def _bounds(arr, g=None):
    a = np.asarray(arr, dtype=float)
    return {"mean": float(a.mean()), "L": float(a.min()), "U": float(a.max()),
            "rank_L": 56, "rank_U": 19945, "g": cdc.guard(a, 0.0) if g is None else g}


def _m_bounds(stats):
    # API-AMBIGUITY: API.md 11.2 does not fix the layout of `b`; it is read as one model's
    # {statistic: {"mean", "L", "U", "rank_L", "rank_U", "g"}} (report keys of API.md 15.2).
    return {k: _bounds(v) for k, v in stats.items()}


def test_cm_quantities_and_cancellation_fixture_is_routed_around():
    d, z, A_full = _cancellation()
    q = ca.cm_quantities(d, z, A_full)
    half = (lambda pair: 0.5 * np.sum(d * (pair[0] - pair[1]), axis=1))
    for X in ("F", "S", "C"):
        assert np.max(np.abs(q["A_" + X] - half(z[X]))) <= 1e-12
        dz = z[X][0] - z[X][1]
        e = np.sum((dz - dz.mean(axis=1, keepdims=True)) ** 2, axis=1)
        assert np.max(np.abs(q["e_" + X] - e)) <= 1e-9 * max(1.0, float(np.max(e)))
    assert np.max(np.abs(q["I_M"] - (q["A_F"] - q["A_S"] - q["A_C"]))) <= 1e-12
    assert np.max(np.abs(q["A_ctx"] - (A_full - q["A_F"]))) <= 1e-12
    stats = {"V3x": A_full - 0.30 * 0.5, "Ztau": q["A_F"] - 0.10 * A_full,
             "ZM010": q["A_S"] - 0.10 * q["A_F"], "ZM050": q["A_S"] - 0.50 * q["A_F"],
             "VM": q["e_S"] - 0.10 * q["e_F"], "Y2": -np.ones(len(d)), "NEG": q["A_S"]}
    m = cdc.m_model(_m_bounds(stats), False)
    assert m["status"] == "ROUTED"  # U(Ztau) < 0 first, although the code effect is large
    assert cdc.overall("M", {1729: "ROUTED", 2718: "ROUTED", 3141: "ROUTED"}, []) \
        == "ROUTED_AROUND"
    assert cdc.overall("M", {1729: "ROUTED", 2718: "ROUTED", 3141: "UPSTREAM_USED"}, []) \
        == "ROUTED_AROUND"
    E = float(np.mean(A_full))  # descriptive quantities, reported after the outcome
    assert np.mean(q["A_S"]) / E == pytest.approx(1.0, abs=1e-12)
    assert np.mean(q["A_C"]) / E == pytest.approx(-1.0, abs=1e-12)
    assert np.mean(q["I_M"]) / E == pytest.approx(0.0, abs=1e-12)
    text = cdc.licence("M", "ROUTED_AROUND", {"k": 3, "tau_hat": 0.0})
    assert "below 10% of the natural contrast" in text
    assert ("This does not distinguish weak transfer, opposition, cancellation, interaction, "
            "context incompatibility, or compensation, and does not establish routing around "
            "the circle.") in text
    _m_licence_common(text)


def _m_licence_common(text):
    assert "defined by the layer-2 fit and projector" in text  # Q-CODE (C2-M wording)
    # API-AMBIGUITY: protocol 3.2 states the caveats "in every C2-M licence" (N2 is a radial
    # support screen; the residual skip is part of every M effect); API.md 11.2 licence() names
    # only the sentence and Q-CODE. The protocol is followed.
    assert "radial support screen" in text and "residual skip" in text
    assert "naturalness" not in text.lower() and "natural support" not in text.lower()


def _upstream_used_stats(n=32):
    one = np.ones(n)
    return {"V3x": 0.6 * one, "Ztau": 0.4 * one, "ZM010": 0.5 * one, "ZM050": 0.2 * one,
            "VM": 0.3 * one, "Y2": 0.2 * one, "NEG": 0.6 * one}


def test_upstream_used_licence_names_the_residual_skip_and_no_block3_claim():
    m = cdc.m_model(_m_bounds(_upstream_used_stats()), False)
    assert m["status"] == "UPSTREAM_USED"
    text = cdc.licence("M", "UPSTREAM_USED", {"k": 2, "tau_hat": 0.4, "psi_M_hat": 0.7})
    assert ("The layer-2 code intervention changes the final output after the remaining "
            "computation, including the residual skip.") in text
    low = text.lower()
    assert "block 3" not in low and "block-3" not in low and "reads the code" not in low
    _m_licence_common(text)


def test_y2_activity_and_resp_in_the_m_stream():
    stats = _upstream_used_stats()  # U(Y2) = 0.2: SPEC (Y2) not declared
    assert cdc.m_model(_m_bounds(stats), True)["status"] == "EXCLUDED/NUISANCE_IN_S"
    assert cdc.m_model(_m_bounds(stats), False)["status"] == "UPSTREAM_USED"
    stats["Y2"] = -0.2 * np.ones(32)
    assert cdc.m_model(_m_bounds(stats), True)["status"] == "UPSTREAM_USED"
    stats["V3x"] = np.full(32, 1e-12)  # inside the guard: RESP not declared
    assert cdc.m_model(_m_bounds(stats), True)["status"] == "EXCLUDED/MODEL_HEADROOM"
    assert co2.y_active(np.nextafter(0.01, 0.0)) and not co2.y_active(0.01)
    rng = np.random.default_rng(9)
    mH, mR = rng.standard_normal((50, 2)), rng.standard_normal((50, 2))
    Ey = rng.random(50) < 0.8
    want = np.mean(np.sum((mH - mR)[Ey] ** 2, axis=1)) / np.trace(np.cov(mH.T, ddof=0))
    assert co2.kappa_m(mH, mR, Ey, mH) == pytest.approx(want, rel=1e-12)
