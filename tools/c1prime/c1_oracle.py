"""C1' donors, symmetry and closed-form checks, the canonical oracle, G, covariates,
eligibility and the Decimal reference helpers (API.md §4; protocol §3, §4, §15.3.7)."""

from __future__ import annotations

import decimal
import hashlib
from decimal import Decimal
from fractions import Fraction

import c1_config  # noqa: F401  (sys.path)
import error_bound
import independent_reference
import numpy as np
from c1_records import CertificateFlag
from oracle_profile import circle_features

from topo_pilot.oracle import BayesFilter

N_SIDE_X = 12
WATCHED = (decimal.Underflow, decimal.Subnormal, decimal.Overflow)
A_H3 = Fraction(2, 10**12)


def F(x) -> Fraction:
    """Exact rational of a float, Decimal, int or Fraction; tolerance floats via their repr."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, (Decimal, int)):
        return Fraction(x)
    return Fraction(float(x))


def tol(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(repr(float(x)))


# ---- donors and symmetry (§3.1, §3.2) ---------------------------------------------------------
def tau(canonical, k) -> np.ndarray:
    j = np.asarray(canonical).astype(np.int64)
    return 6 * ((j // 6 + int(k)) % 6) + j % 6


def donors(canon32) -> tuple:
    H = np.asarray(canon32).astype(np.int64)
    out = [H.copy()]
    for k in (1, -1):
        D = H.copy()
        D[:, :31] = tau(H[:, :31], k)
        out.append(D)
    return tuple(out)


def rho_index(coords, k) -> np.ndarray:
    xy = np.rint(np.asarray(coords, dtype=np.float64)).astype(np.int64)
    pos = {(int(x), int(y)): i for i, (x, y) in enumerate(xy)}
    return np.array([pos[((int(x) + 2 * int(k)) % N_SIDE_X, int(y))] for x, y in xy],
                    dtype=np.int64)


def symmetry_report(T, E, pi, coords) -> dict:
    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    N, V = E.shape
    dev, exact, r_E = 0.0, True, Fraction(0)
    for k in (1, -1):
        rho, tk = rho_index(coords, k), tau(np.arange(V), k)
        dev = max(dev, float(np.abs(T[np.ix_(rho, rho)] - T).max()),
                  float(np.abs(E[rho][:, tk] - E).max()), float(np.abs(pi - 1.0 / N).max()))
        exact &= bool(np.array_equal(T[np.ix_(rho, rho)], T) and np.array_equal(pi[rho], pi))
        Er = E[rho][:, tk]
        for z in range(N):
            for v in range(V):
                r_E = max(r_E, abs(F(Er[z, v]) / F(E[z, v]) - 1))
    eps = r_E / (1 - r_E) if r_E < 1 else None
    return {"max_dev": dev, "symmetry_ok": dev <= 1e-14, "exact_invariance": exact,
            "r_E": r_E, "eps_sym": eps}


def closed_form_b32(b31, T, E, w32, rho) -> np.ndarray:
    b31 = np.asarray(b31, dtype=np.float64)
    t = np.zeros_like(b31)
    t[:, np.asarray(rho)] = b31
    u = (t @ np.asarray(T)) * np.asarray(E)[:, np.asarray(w32)].T
    return u / u.sum(axis=1, keepdims=True)


def closed_form_tolerance(eps_sym, delta=2e-12):
    if eps_sym is None:
        return None
    d = tol(delta)
    t = 2 * d / (1 - d) + 62 * F(eps_sym)
    return None if t > Fraction(3, 2) else (t, t + t * t)


def rel_agree(xhat, xref, tol_) -> bool:
    bound = tol(tol_)
    for a, b in zip(np.ravel(np.asarray(xhat, dtype=object)), np.ravel(np.asarray(xref,
                                                                                 dtype=object))):
        fa, fb = F(a), F(b)
        if fb == 0:
            if fa != 0:
                return False
            continue
        if abs(fa / fb - 1) > bound:
            return False
    return True


def interval_rule(xhat, xtilde, beta, a=2e-12) -> str:
    """§3.4 three-way rule against I_v = [x~/(1+beta), x~/(1-beta)], exact rationals."""
    a, beta = tol(a), F(beta)
    d_low = d_high = Fraction(0)
    for xh, xt in zip(np.ravel(np.asarray(xhat, dtype=object)),
                      np.ravel(np.asarray(xtilde, dtype=object))):
        if not np.isfinite(float(xh)):
            return "FAIL_TECHNICAL/ORACLE"
        x, lo, hi = F(xh), F(xt) / (1 + beta), F(xt) / (1 - beta)
        dist = lo - x if x < lo else (x - hi if x > hi else Fraction(0))
        d_low, d_high = max(d_low, dist), max(d_high, abs(x - lo), abs(x - hi))
    if d_high <= a:
        return "PASS"
    return "FAIL_TECHNICAL/ORACLE" if d_low > a else "INCONCLUSIVE/NUMERICAL"


# ---- the operational, canonical oracle (§3.3; C1, C3) ----------------------------------------
def run_oracle(T, E, pi, tokens32) -> dict:
    res = BayesFilter(T, E, pi).run(np.asarray(tokens32, dtype=np.int64))
    return {"b31": res.b[:, 30], "b32": res.b[:, 31], "q": res.q[:, 32], "s": res.ce[:, 31],
            "log_evidence": res.log_evidence, "b_all": res.b}


def _osum_dot(x, y) -> np.ndarray:
    acc = x[:, 0] * y[:, 0]
    for v in range(1, x.shape[1]):
        acc = acc + x[:, v] * y[:, v]
    return acc


def G_hat(qp, qm) -> tuple:
    qp, qm = np.asarray(qp, dtype=np.float64), np.asarray(qm, dtype=np.float64)
    lp, lm = np.log(qp), np.log(qm)
    d, lam = qp - qm, lp - lm
    return 0.5 * _osum_dot(d, lam), d, lam, lp, lm


def named_from_canonical(x, perm) -> np.ndarray:
    x = np.asarray(x)
    out = np.empty_like(x)
    out[..., np.asarray(perm)] = x
    return out


def canonical_from_named_cols(x, perm) -> np.ndarray:
    return np.asarray(x)[..., np.asarray(perm)]


def G_named(d, lam, perm) -> np.ndarray:
    return 0.5 * _osum_dot(named_from_canonical(d, perm), named_from_canonical(lam, perm))


# ---- covariates and eligibility (§3.3, §4) ------------------------------------------------------
def _y(coords) -> np.ndarray:
    return np.rint(np.asarray(coords, dtype=np.float64)[:, 1]).astype(np.int64)


def y_marginal(b, coords) -> np.ndarray:
    y = _y(coords)
    onehot = (y[:, None] == np.arange(int(y.max()) + 1)[None, :]).astype(np.float64)
    return np.asarray(b, dtype=np.float64) @ onehot


def m32(b, coords) -> np.ndarray:
    return np.asarray(b, dtype=np.float64) @ circle_features(np.asarray(coords, dtype=np.float64))


def nuisance(b, coords) -> np.ndarray:
    b, y = np.asarray(b, dtype=np.float64), _y(coords).astype(np.float64)
    ybar = b @ y
    var = b @ (y * y) - ybar * ybar
    return np.column_stack((ybar, var, np.linalg.norm(m32(b, coords), axis=1)))


def s_max(s_cal) -> float:
    return float(np.quantile(np.asarray(s_cal, dtype=np.float64), 0.999, method="inverted_cdf"))


def eligible(sp, sm, smax, le_H, le_Hp, le_Hm) -> np.ndarray:
    finite = np.isfinite(le_H) & np.isfinite(le_Hp) & np.isfinite(le_Hm)
    return (np.asarray(sp) <= smax) & (np.asarray(sm) <= smax) & finite


def eligible_fraction(mask) -> float:
    mask = np.asarray(mask, dtype=bool)
    return float(mask.sum()) / float(mask.size)


def kappa_nu(nu_p, nu_m, nu_nat_cal, elig_cal) -> float:
    e = np.asarray(elig_cal, dtype=bool)
    diff = (np.asarray(nu_p) - np.asarray(nu_m))[e]
    num = float(np.mean(np.sum(diff * diff, axis=1)))
    return num / float(np.trace(np.cov(np.asarray(nu_nat_cal, dtype=np.float64).T, ddof=0)))


def leakage_active(kappa) -> bool:
    return float(kappa) >= 0.01


# ---- Decimal reference (§3.4; route-F steps 1-2) ------------------------------------------------
def _flags_check(ctx) -> None:
    raised = [s.__name__ for s in WATCHED if ctx.flags[s]]
    if raised:
        raise CertificateFlag(f"watched Decimal flags {raised}")


def decimal_posterior60(T, E, pi, suffix) -> list:
    """Replica (provenance: K4 error_bound._reference_posterior, 8 lines) with C1's §16 mapping:
    Decimal exceptions and reference-input ValueErrors propagate unchanged; flags raise."""
    ctx = error_bound.trapping_context(60)
    with decimal.localcontext(ctx):
        post = independent_reference.decimal_suffix_posterior(T, E, pi, list(suffix), 60)
        _flags_check(decimal.getcontext())
    return post


_TE_CACHE: dict = {}


def _decimal_TE(T, E, digits) -> list:
    key = (hashlib.sha256(np.ascontiguousarray(T).tobytes() + np.ascontiguousarray(E).tobytes())
           .hexdigest(), int(digits))
    if key not in _TE_CACHE:
        Td = [[Decimal(float(x)) for x in row] for row in np.asarray(T)]
        Ed = [[Decimal(float(x)) for x in row] for row in np.asarray(E)]
        N, V = len(Ed), len(Ed[0])
        with decimal.localcontext(error_bound.trapping_context(digits)) as ctx:
            TE = [[sum((Td[z][s] * Ed[s][v] for s in range(N) if Td[z][s] != 0), Decimal(0))
                   for v in range(V)] for z in range(N)]
            _flags_check(ctx)
        _TE_CACHE[key] = TE
    return _TE_CACHE[key]


def decimal_predictive(b, T, E, digits=60) -> list:
    TE = _decimal_TE(T, E, digits)
    with decimal.localcontext(error_bound.trapping_context(digits)) as ctx:
        q = [sum((b[z] * TE[z][v] for z in range(len(TE))), Decimal(0))
             for v in range(len(TE[0]))]
        _flags_check(ctx)
    return q


def decimal_reference(T, E, pi, h32) -> dict:
    h = [int(x) for x in np.asarray(h32)]
    with decimal.localcontext(error_bound.trapping_context(80)) as ctx:
        b31 = decimal_posterior60(T, E, pi, h[:31])
        b32 = decimal_posterior60(T, E, pi, h)
        q31, q32 = decimal_predictive(b31, T, E, 80), decimal_predictive(b32, T, E, 80)
        ln_q32 = [x.ln() for x in q32]
        s = -q31[h[31]].ln()
        _flags_check(ctx)
    return {"b31": b31, "b32": b32, "q31": q31, "q32": q32, "ln_q32": ln_q32, "s": s}


def decimal_G(q_p, q_m) -> Decimal:
    with decimal.localcontext(error_bound.trapping_context(80)) as ctx:
        G = sum(((a - b) * (a.ln() - b.ln()) for a, b in zip(q_p, q_m)), Decimal(0)) / 2
        _flags_check(ctx)
    return G


def h3_compare(x_hat, x_dec, p1_ok, beta) -> str:
    if p1_ok:
        return "PASS" if rel_agree(x_hat, x_dec, A_H3) else "FAIL_TECHNICAL/ORACLE"
    return interval_rule(x_hat, x_dec, beta, A_H3)
