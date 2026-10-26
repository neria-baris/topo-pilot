"""Independent tests, author A (job 0101; v2 update): T-GLS part 2, the G1 scale-invariance
fixture of D-0104-2 and the GLS-REF fixtures 1-6 of NEW-1 (C2-FROZEN-v2 2.5, 9.2, 13.3). T-GLS
part 1 (Lemmas G1-G3, the whitened-design fixtures) is in test_a_readout.py; T-LADDER moved to
test_a_oracle.py (the 400-line limit).

Targets (API.md 8.2, 9.1): ck.gls, ck.gls_identities, cs.gls_ref, cs.enclosure,
cs.dsolve, cs.dinverse, cs.dctx, cs.D. Expected values come from the
protocol and from an independent exact Fraction/Decimal implementation written in this file.
The protocol's fixture 1 (Sigma = I3, X = [e1, eps e2]) is evaluated literally by that
independent implementation; for the module it is embedded in R^8 with 5 nuisance columns and
K = 1, the column layout API.md 8.2 / 9.1 fix (L_G = rows 0..4, L_B = rows 5..).
"""

from __future__ import annotations

import decimal
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402,F401
import c2_code as ck  # noqa: E402
import c2_stats as cs  # noqa: E402

DEG = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"
EPS, DELTA = 1e-3, 1e-19


# ---- exact helpers (independent of the module under test) ----------------------------------
def _F(M):
    return [[Fraction(float(x)) for x in row] for row in np.atleast_2d(np.asarray(M, float))]


def _mm(A, B):
    cols = list(zip(*B))
    return [[sum((a * b for a, b in zip(r, c)), Fraction(0)) for c in cols] for r in A]


def _tr(A):
    return [list(r) for r in zip(*A)]


def _sub(A, B):
    return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]


def _f2(A):
    return sum((x * x for r in A for x in r), Fraction(0))


def _solve(A, B):
    n = len(A)
    M = [list(A[i]) + list(B[i]) for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]


def _dsqrt(fr):
    with decimal.localcontext(decimal.Context(prec=60)):
        return (Decimal(fr.numerator) / Decimal(fr.denominator)).sqrt()


def _fd(s):
    return Fraction(Decimal(str(s)))


def _exact_proj(A, Gamma, B):
    X = _F(np.hstack((Gamma, B)))
    Y = _solve(_F(A), X)
    L = _solve(_mm(_tr(X), Y), _tr(Y))
    m5 = Gamma.shape[1]
    return _mm(_F(B), L[m5:]), _mm(_F(Gamma), L[:m5]), L


def _problem(p=12, K=1, seed=0, spread=1.0):
    rng = np.random.default_rng(seed)
    Gamma, B = rng.normal(size=(p, 5)), rng.normal(size=(p, 2 * K))
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    Sigma = (U * np.exp(rng.uniform(-spread, spread, p))) @ U.T
    return Gamma, B, (Sigma + Sigma.T) / 2


# ---- the G1 scale-invariance fixture (D-0104-2; v2 2.5, 13.3 T-GLS) -------------------------
def _whit_asym(P, Sigma):
    R = np.linalg.cholesky(Sigma).T  # Sigma = R'R
    Pt = np.linalg.solve(R.T, P @ R.T)  # P~ = R^-T P R'
    return np.max(np.abs(Pt - Pt.T))


def _planted(g, Gamma, B, V):
    """An oblique projector in the metric V: every G1 identity except self-adjointness holds."""
    Xn = np.hstack((Gamma, B))
    L = np.linalg.solve(Xn.T @ V @ Xn, Xn.T @ V)
    out = dict(g, L=L, L_G=L[:5], L_B=L[5:], P_S=B @ L[5:], P_G=Gamma @ L[:5])
    out["P_rest"] = np.eye(len(Xn)) - out["P_S"] - out["P_G"]
    return out


def test_g1_check_is_scale_invariant_and_rejects_a_non_self_adjoint_projector():
    Gamma0, B0, Sigma0 = _problem(p=12, K=2, seed=19, spread=2.0)
    V = np.linalg.inv(_problem(p=12, K=2, seed=20, spread=2.0)[2])
    P_ref = ck.gls(Gamma0, B0, Sigma0)["P_S"]
    for c in (1e-8, 1.0, 1e8):  # Sigma by c, [Gamma, B] by sqrt(c)
        Gamma, B, Sigma = np.sqrt(c) * Gamma0, np.sqrt(c) * B0, c * Sigma0
        g = ck.gls(Gamma, B, Sigma)
        assert g["status"] == "PASS" and bool(ck.gls_identities(g, Gamma, B, Sigma)["ok"])
        assert np.max(np.abs(g["P_S"] - P_ref)) <= 1e-10  # P is unchanged up to rounding
        P = g["P_S"] + g["P_G"]
        assert _whit_asym(P, Sigma) <= 1e-10
        W = np.linalg.inv(Sigma)
        if c == 1e-8:  # v1's absolute check of W P - P'W scales with 1/lambda_min(Sigma)
            assert np.max(np.abs(W @ P - P.T @ W)) > 1e-10
        bad = _planted(g, Gamma, B, V)
        Xn = np.hstack((Gamma, B))
        assert np.max(np.abs(bad["L"] @ Xn - np.eye(9))) <= 1e-10
        assert np.max(np.abs(bad["P_S"] @ bad["P_S"] - bad["P_S"])) <= 1e-10
        assert _whit_asym(bad["P_S"] + bad["P_G"], Sigma) > 1e-6
        assert not bool(ck.gls_identities(bad, Gamma, B, Sigma)["ok"])  # fails at every c
        e = ck.gls(Gamma, B)  # Euclidean variant: the check is ||P - P'||_max
        Pe = e["P_S"] + e["P_G"]
        assert bool(ck.gls_identities(e, Gamma, B)["ok"]) and np.max(np.abs(Pe - Pe.T)) <= 1e-10
        assert not bool(ck.gls_identities(_planted(e, Gamma, B, V), Gamma, B)["ok"])


# ---- GLS-REF (NEW-1) -------------------------------------------------------------------------
def _embedded(delta=DELTA):
    p = 8
    I = np.eye(p)
    Gamma, B = I[:, :5].copy(), np.column_stack((I[:, 5], EPS * I[:, 6]))
    Ystar = np.hstack((Gamma, B))
    Ystar[:, 6] = EPS * I[:, 6] + delta * I[:, 7]
    return I, Gamma, B, Ystar


def _patch_dsolve(monkeypatch, p, m, first=None, second=None):
    """Replace the first solve Y* = A^-1 X_n (A is p x p) by `first`, or add `second` to the
    second solve L* = G*^-1 Y*' (G* is m x m, right-hand side m x p); calls are identified by
    their shapes, so an inverse computed through dsolve (m x m right-hand side) is untouched."""
    orig = cs.dsolve

    def fake(A, Bm):
        out = orig(A, Bm)
        if first is not None and len(A) == p and len(Bm[0]) == m:
            return cs.D(first)
        if second is not None and len(A) == m and len(Bm[0]) == p:
            return [[x + Decimal(float(e)) for x, e in zip(r, er)] for r, er in zip(out, second)]
        return out

    monkeypatch.setattr(cs, "dsolve", fake)


def test_fixture1_first_solve_error_propagation_independent_exact():
    eps, dlt = Fraction(EPS), Fraction(DELTA)
    X = [[Fraction(1), Fraction(0)], [Fraction(0), eps], [Fraction(0), Fraction(0)]]
    Ys = [[Fraction(1), Fraction(0)], [Fraction(0), eps], [Fraction(0), dlt]]
    L = _solve(_mm(_tr(X), X), _tr(X))
    Ls = _solve(_mm(_tr(X), Ys), _tr(Ys))  # exact second solve: R_C = R_G = 0
    err2 = _f2(_sub(Ls, L))
    assert err2 == (dlt / eps ** 2) ** 2  # ||L* - L||_F = delta / eps^2 = 1e-13 exactly
    e_Y = dlt  # omega_A = ||A^-1||_2 = 1 and ||R_A||_F = delta
    om_G = 1 / eps ** 2  # ||G^-1||_2 of G = diag(1, eps^2)
    nX, nL = _dsqrt(_f2(X)), _dsqrt(_f2(Ls))
    e_L = Decimal(om_G.numerator) / Decimal(om_G.denominator) * (
        Decimal(DELTA) * (1 + nX * nL))
    assert Decimal("0.9e-10") <= e_L <= Decimal("1.1e-10")
    assert Fraction(e_L) ** 2 >= err2
    v2 = 16 * DELTA / (np.sqrt(3.0) * np.sqrt(1 + EPS ** 2)) * float(_dsqrt(_f2(L)))
    assert 8.5e-16 < v2 < 9.9e-16 and Fraction(v2) ** 2 < err2  # the withdrawn v2 expression
    assert e_L / nL > Decimal("1e-20")  # rho_ref ~ 1e-13: the reference is not accepted


def test_fixture1_module_bound_covers_the_true_error_and_is_not_accepted(monkeypatch):
    A, Gamma, B, Ystar = _embedded()
    g = ck.gls(Gamma, B, A)
    _patch_dsolve(monkeypatch, 8, 7, first=Ystar)
    out = cs.gls_ref(A, Gamma, B, g["P_S"], g["P_G"])
    assert not bool(out["accepted"])
    assert out["status"] == "EXCLUDED/NUMERICAL"
    true = Fraction(DELTA) / Fraction(EPS) ** 2
    assert _fd(out["e_L"]) >= true
    assert _fd(out["e_L"]) <= Fraction(1, 10**8)
    assert _fd(out["rho_ref"]) > Fraction(1, 10**20)


def test_fixture2_perturbed_operator_residual_r_g(monkeypatch):
    Gamma, B, Sigma = _problem(p=8, K=1, seed=12)
    g = ck.gls(Gamma, B, Sigma)
    E = 1e-12 * np.random.default_rng(12).normal(size=(7, 8))
    _patch_dsolve(monkeypatch, 8, 7, second=E)
    out = cs.gls_ref(Sigma, Gamma, B, g["P_S"], g["P_G"])
    # the 80-digit L* is the exact L to ~1e-70, so ||L*_pert - L||_F >= 0.99 ||E||_F
    assert _fd(out["e_L"]) ** 2 >= _f2(_F(E)) * Fraction(99, 100)
    assert not bool(out["accepted"])  # rho_ref ~ 1e-12 > 1e-20


def _up(fr2):  # a verified upper bound on sqrt(fr2)
    return Fraction(_dsqrt(fr2)) * (1 + Fraction(1, 10**30))


def test_fixture2_independent_r_c_and_r_g_perturbations_lemma_gr():
    rng = np.random.default_rng(13)
    A = rng.normal(size=(4, 4))
    A = A @ A.T + 4 * np.eye(4)
    X = _F(rng.normal(size=(4, 2)))
    Y = _solve(_F(A), X)  # exact first solve: R_A = 0, e_Y = 0
    G = _mm(_tr(X), Y)
    L = _solve(G, _tr(Y))
    Gf = np.array([[float(x) for x in r] for r in G])
    om_G = Fraction(float(np.linalg.norm(np.linalg.inv(Gf), 2)) * (1 + 1e-9))
    for case in ("RC", "RG"):
        Gs = [[x + (Fraction(1, 10**9) if case == "RC" and i == j else 0)
               for j, x in enumerate(r)] for i, r in enumerate(G)]
        Ls = _solve(Gs, _tr(Y))
        if case == "RG":
            Ls = [[x + Fraction(3, 10**10) for x in r] for r in Ls]
        R_C, R_G = _sub(Gs, G), _sub(_mm(Gs, Ls), _tr(Y))
        assert (_f2(R_C) > 0) == (case == "RC") and (_f2(R_G) > 0) == (case == "RG")
        e_L = om_G * (_up(_f2(R_G)) + _up(_f2(R_C)) * _up(_f2(Ls)))  # Lemma GR, e_Y = 0
        assert e_L ** 2 >= _f2(_sub(Ls, L))


def test_fixture3_lemma_inv_bound_and_non_acceptance(monkeypatch):
    rng = np.random.default_rng(14)
    Mm = rng.normal(size=(4, 4)) + 3 * np.eye(4)
    V = np.linalg.inv(Mm) * (1 + 1e-3 * rng.normal(size=(4, 4)))
    th = _dsqrt(_f2(_sub([[Fraction(int(i == j)) for j in range(4)] for i in range(4)],
                         _mm(_F(V), _F(Mm))))) * Decimal("1.000001")
    assert th < 1
    exact_inv = np.array([[float(x) for x in r] for r in _solve(_F(Mm), _F(np.eye(4)))])
    assert np.linalg.norm(exact_inv, 2) <= np.linalg.norm(V, "fro") / (1 - float(th))
    Gamma, B, Sigma = _problem(p=8, K=1, seed=14)
    g = ck.gls(Gamma, B, Sigma)
    good = cs.gls_ref(Sigma, Gamma, B, g["P_S"], g["P_G"])
    assert bool(good["accepted"]) and _fd(good["theta_A"]) < 1
    assert float(_fd(good["omega_A"])) >= np.linalg.norm(np.linalg.inv(Sigma), 2)
    orig_inv = np.linalg.inv
    monkeypatch.setattr(np.linalg, "inv", lambda a: 0.1 * orig_inv(a))  # theta_A >= 1
    bad = cs.gls_ref(Sigma, Gamma, B, g["P_S"], g["P_G"])
    assert not bool(bad["accepted"]) and bad["status"] == "EXCLUDED/NUMERICAL"
    assert _fd(bad["theta_A"]) >= 1


def test_fixture4_euclidean_case_conditioning_differs_from_whitened():
    rng = np.random.default_rng(15)
    p = 10
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    s = np.logspace(0, -4, 7)
    Xn = (U[:, :7] * s) @ np.linalg.qr(rng.normal(size=(7, 7)))[0]
    Sigma = (U[:, :7] * s ** 2) @ U[:, :7].T + U[:, 7:] @ U[:, 7:].T
    Gamma, B = Xn[:, :5].copy(), Xn[:, 5:].copy()
    e, w = ck.gls(Gamma, B), ck.gls(Gamma, B, Sigma)
    assert e["cond_Xt"] > 1e3 * w["cond_Xt"]  # cond2(X_n) and cond2(X~) differ by orders
    out = cs.gls_ref(np.eye(p), Gamma, B, e["P_S"], e["P_G"], euclidean=True)
    assert bool(out["accepted"])
    smin = np.linalg.svd(Xn, compute_uv=False)[-1]
    assert float(_fd(out["omega_G"])) >= 0.999 / smin ** 2  # bounds ||(Xn'Xn)^-1||_2
    assert 1 / smin ** 2 > 1e6 * w["cond_Xt"] ** 2  # a kappa(X~)^2-based figure is far too small
    PS, PG, _ = _exact_proj(np.eye(p), Gamma, B)
    assert _fd(out["delta_P_S"]) ** 2 >= _f2(_sub(_F(e["P_S"]), PS))
    assert _fd(out["delta_P_G"]) ** 2 >= _f2(_sub(_F(e["P_G"]), PG))


def test_fixture5_reduced_precision_enclosure_and_trap():
    # API-AMBIGUITY: API.md 9.1 does not say whether u_D in theta/enclosure reads the active
    # context precision; protocol 13.3 fixture 5 needs a reduced-precision residual, so the test
    # sets decimal.localcontext(cs.dctx(12)) around both the residual and cs.enclosure.
    rng = np.random.default_rng(16)
    left, right = rng.normal(size=(5, 8)), rng.normal(size=(8, 4))
    fixed = left @ right  # nearly cancels: the 12-digit rounding dominates the residual
    exact = _sub(_F(fixed), _mm(_F(left), _F(right)))
    with decimal.localcontext(cs.dctx(12)):
        Lq, Rq, Fq = cs.D(left), cs.D(right), cs.D(fixed)
        prod = [[sum((a * b for a, b in zip(r, c)), Decimal(0)) for c in zip(*Rq)] for r in Lq]
        Rt = [[f - q for f, q in zip(fr, pr)] for fr, pr in zip(Fq, prod)]
        enc = cs.enclosure(Rt, Fq, Lq, Rq, 8)
    assert Fraction(enc) ** 2 >= _f2(exact)
    with decimal.localcontext(cs.dctx()):
        with pytest.raises(decimal.DivisionByZero):
            Decimal(1) / Decimal(0)
    Gamma, _, Sigma = _problem(p=8, K=1, seed=16)
    B = Gamma[:, :2].copy()  # exactly singular Gram matrix: elimination traps
    out = cs.gls_ref(Sigma, Gamma, B, np.zeros((8, 8)), np.zeros((8, 8)))
    assert not bool(out["accepted"]) and out["status"] == "EXCLUDED/NUMERICAL"
    assert out["trap"] is not None


def test_fixture6_eps_p_enters_delta_p_and_the_gate(monkeypatch):
    A, Gamma, B, Ystar = _embedded(delta=1e-17)
    g = ck.gls(Gamma, B, A)
    _patch_dsolve(monkeypatch, 8, 7, first=Ystar)
    out = cs.gls_ref(A, Gamma, B, g["P_S"], g["P_G"])
    dev, eps_p, dP = (_fd(out[k]) for k in ("dev_S", "eps_P_S", "delta_P_S"))
    assert abs(dP - (dev + eps_p)) <= Fraction(1, 10**50) * (dev + eps_p)
    assert eps_p >= Fraction(float(np.linalg.norm(B, "fro"))) * _fd(out["e_L"]) * Fraction(
        999999, 10**6)
    assert dev <= Fraction(1, 10**8)  # the deviation alone would pass the 1e-8 gate ...
    assert not bool(out["gate_S"])  # ... the reference uncertainty makes it fail


def test_accepted_reference_bounds_the_exact_projector_distance():
    Gamma, B, Sigma = _problem(p=10, K=1, seed=17)
    g = ck.gls(Gamma, B, Sigma)
    out = cs.gls_ref(Sigma, Gamma, B, g["P_S"], g["P_G"])
    assert bool(out["accepted"]) and out["status"] == "PASS" and out["trap"] is None
    assert _fd(out["rho_ref"]) <= Fraction(1, 10**20)
    assert _fd(out["theta_A"]) < 1 and _fd(out["theta_G"]) < 1
    assert bool(out["gate_S"]) and bool(out["gate_G"])
    PS, PG, L = _exact_proj(Sigma, Gamma, B)
    assert _fd(out["delta_P_S"]) ** 2 >= _f2(_sub(_F(g["P_S"]), PS))
    assert _fd(out["delta_P_G"]) ** 2 >= _f2(_sub(_F(g["P_G"]), PG))
    assert abs(_fd(out["L_star_norm"]) ** 2 - _f2(L)) <= Fraction(1, 10**40) * _f2(L)
    assert int(out["n"]) == 10 and int(out["m"]) == 7


def test_dctx_dsolve_dinverse_against_exact_rationals():
    ctx = cs.dctx()
    assert ctx.prec == 80 and ctx.rounding == decimal.ROUND_HALF_EVEN
    for t in (decimal.Overflow, decimal.Underflow, decimal.Subnormal, decimal.DivisionByZero,
              decimal.InvalidOperation):
        assert ctx.traps[t]
    assert not ctx.traps[decimal.Inexact] and not ctx.traps[decimal.Rounded]
    assert cs.D(np.array([[0.1]]))[0][0] == Decimal(0.1)
    A = np.array([[0.0, 2.0, 1.0], [1.0, 1.0, 0.0], [3.0, 0.0, 1.0]])  # needs a row pivot
    Bm = np.random.default_rng(18).normal(size=(3, 2))
    with decimal.localcontext(cs.dctx()):
        Xd = cs.dsolve(cs.D(A), cs.D(Bm))
        Vd = cs.dinverse(cs.D(A))
    Xe, Ve = _solve(_F(A), _F(Bm)), _solve(_F(A), _F(np.eye(3)))
    for got, ref in ((Xd, Xe), (Vd, Ve)):
        for r, s in zip(got, ref):
            for a, b in zip(r, s):
                assert abs(Fraction(a) - b) <= Fraction(1, 10**70) * (1 + abs(b))
