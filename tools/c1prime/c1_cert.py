"""C1' numerical certificate core (API.md §5; CERTIFICATE.md; protocol §15.3.2-15.3.7).

Certified kernels use numpy elementwise + - * / only, vectorised over rows: no BLAS, matmul,
dot, einsum, sum or mean. Every comparison is in exact rationals (fractions.Fraction)."""

from __future__ import annotations

import decimal
import hashlib
import math
from decimal import Decimal
from fractions import Fraction

import c1_config  # noqa: F401  (sys.path)
import c1_oracle
import error_bound
import numpy as np
from c1_records import C1GateFailure, CertificateFlag

U = Fraction(1, 2**53)
U1 = U / (1 - U)
ZETA = Fraction(1, 2**800)
TWO_M1000 = Fraction(1, 2**1000)
C1HAT, C3HAT = Fraction(0.1), Fraction(0.3)
DELTA1, DELTA3 = abs(C1HAT - Fraction(1, 10)), abs(C3HAT - Fraction(3, 10))
P2_LOGIT, P2_SCORE, P2_LEAF = 2**19, 2**21, 2**23


def gamma(n) -> Fraction:
    nu = int(n) * U
    return nu / (1 - nu)


def rho_bar_ref(L, N, d) -> Fraction:
    return (2 * (int(L) - 1) * (int(d) + 2) + 2 + 2 * int(N) + int(d)) * U1


def up(c) -> float:
    c = Fraction(c)
    f = float(c)
    return math.nextafter(f, math.inf) if Fraction(f) < c else f


def OUT(x) -> Fraction:
    return (1 + Fraction(1, 2**30)) * Fraction(x) + ZETA


def osum(cols) -> np.ndarray:
    acc = cols[0]
    for c in cols[1:]:
        acc = acc + c
    return acc


def supports(T) -> tuple:
    T = np.asarray(T, dtype=np.float64)
    cols = [np.flatnonzero(T[:, z] > 0) for z in range(T.shape[0])]
    rows = [np.flatnonzero(T[z, :] > 0) for z in range(T.shape[0])]
    return cols, rows


def reference_oracle(T, E, pi, tokens32) -> dict:
    """C0: the ordered float64 reference filter and predictive (certificate only)."""
    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    tok = np.asarray(tokens32, dtype=np.int64)
    R, L = tok.shape
    N, V = E.shape
    S_col, S_row = supports(T)
    b = np.empty((R, L, N))
    u = [pi[s] * E[s, tok[:, 0]] for s in range(N)]
    for t in range(L):
        D = osum(u)
        bt = [us / D for us in u]
        b[:, t, :] = np.stack(bt, axis=1)
        if t + 1 < L:
            w = tok[:, t + 1]
            u = []
            for z in range(N):
                a = osum([bt[zp] * T[zp, z] for zp in S_col[z]])
                u.append(a * E[z, w])
    TE = np.stack([osum([T[z, zp] * E[zp, :] for zp in S_row[z]]) for z in range(N)])
    q = osum([b[:, L - 1, z][:, None] * TE[z][None, :] for z in range(N)])
    finite = np.isfinite(b).all(axis=(1, 2))
    return {"b": b, "q_ref": q, "nu_min": b.min(axis=(1, 2)), "finite": finite, "TE_ref": TE}


def _digest(a) -> str:
    a = np.ascontiguousarray(a)
    return hashlib.sha256(str(a.dtype).encode() + str(a.shape).encode() + a.tobytes()).hexdigest()


def p0(T, E_list, pi) -> dict:
    """P0 in exact rationals (§15.3.3); not ok -> FAIL_TECHNICAL/IDENTITY."""
    T, pi = np.asarray(T, dtype=np.float64), np.asarray(pi, dtype=np.float64)
    E_list = [np.asarray(E, dtype=np.float64) for E in E_list]
    E = E_list[0]
    N, V = E.shape
    S_col, S_row = supports(T)
    d = max(max(len(c) for c in S_col), max(len(r) for r in S_row))
    eps_E = min(Fraction(float(x)) for x in E.ravel())
    pi_min = min(Fraction(float(x)) for x in pi)
    tau_plus = min(Fraction(float(x)) for x in T.ravel() if x > 0)
    identical = len({_digest(e) for e in E_list}) == 1
    rowsum = [sum((Fraction(float(x)) for x in E[z]), Fraction(0)) for z in range(N)]
    r = [sum((Fraction(float(T[z, zp])) * rowsum[zp] for zp in S_row[z]), Fraction(0))
         for z in range(N)]
    ok = bool((E > 0).all() and (pi > 0).all() and (T >= 0).all() and (np.diag(T) > 0).all()
              and T.shape == (N, N) and pi.shape == (N,) and pi_min * eps_E >= TWO_M1000
              and tau_plus * eps_E >= TWO_M1000 and identical
              and all(e.shape == E.shape for e in E_list))
    return {"ok": ok, "N": N, "V": V, "d": d, "eps_E": eps_E, "pi_min": pi_min,
            "tau_plus": tau_plus,
            "nu0": TWO_M1000 / (tau_plus * eps_E) if tau_plus * eps_E > 0 else None,
            "omega_TE": max(r) - min(r), "identical": identical,
            "E_digests": [_digest(e) for e in E_list]}


def p1(nu_min, finite, nu0) -> np.ndarray:
    return np.array([bool(f) and Fraction(float(v)) >= nu0
                     for v, f in zip(np.asarray(nu_min), np.asarray(finite))])


def discrepancy(q_hat, q_ref) -> list:
    out = []
    for qh, qr in zip(np.asarray(q_hat, dtype=np.float64), np.asarray(q_ref, dtype=np.float64)):
        out.append(max(abs(Fraction(float(a)) - Fraction(float(b))) / Fraction(float(b))
                       for a, b in zip(qh, qr)))
    return out


def rho_main(r_h, rho_bar) -> Fraction:
    r_h = Fraction(r_h)
    if r_h > Fraction(1, 2):
        raise C1GateFailure("FAIL_TECHNICAL/ORACLE", f"P4: r_h = {float(r_h)} > 1/2")
    return Fraction(rho_bar) + r_h / (1 - r_h)


def route_f(T, E, pi, tokens32, q_hat) -> list:
    """§15.3.7 steps 1-4 per history; x > 1/2 -> ok False (FAIL_TECHNICAL/ORACLE, P4)."""
    N = np.asarray(E).shape[0]
    single = np.asarray(tokens32).ndim == 1
    tokens32 = np.atleast_2d(np.asarray(tokens32))
    q_hat = np.atleast_2d(np.asarray(q_hat, dtype=np.float64))
    beta = Fraction(error_bound.posterior_envelope(32, N))
    beta_q = (1 + beta) * (1 + Fraction(error_bound.gamma_digits(2 * N + 2, 60))) - 1
    out = []
    for h, qh in zip(np.asarray(tokens32), np.asarray(q_hat, dtype=np.float64)):
        bt = c1_oracle.decimal_posterior60(T, E, pi, [int(x) for x in h])
        qt = c1_oracle.decimal_predictive(bt, T, E, 60)
        r = max(abs(Fraction(float(a)) - Fraction(b)) / Fraction(b) for a, b in zip(qh, qt))
        x = (1 + r) * (1 + beta_q) - 1
        ok = x <= Fraction(1, 2)
        out.append({"r": r, "x": x, "beta_q": beta_q, "ok": ok,
                    "rho_F": x / (1 - x) if ok else None})
    return out[0] if single else out


def measured_log_error(q_hat, l_hat) -> list:
    """M-ln: e_bar per row from correctly rounded 40-digit Decimal ln (§15.3.6)."""
    tiny = Fraction(1, 10**38)
    out = []
    with decimal.localcontext(error_bound.trapping_context(40)) as ctx:
        for qr, lr in zip(np.asarray(q_hat, dtype=np.float64), np.asarray(l_hat,
                                                                            dtype=np.float64)):
            worst = Fraction(0)
            for q, ell in zip(qr, lr):
                Ld = Fraction(Decimal(float(q)).ln())
                worst = max(worst, abs(Fraction(float(ell)) - Ld) + tiny * abs(Ld))
            out.append(Fraction(up(worst)))
        raised = [s.__name__ for s in c1_oracle.WATCHED if ctx.flags[s]]
    if raised:
        raise CertificateFlag(f"M-ln raised flags {raised}")
    return out


def _finite_le(arrays, limit, strict_positive=False) -> bool:
    for a in arrays:
        a = np.asarray(a, dtype=np.float64)
        if not np.isfinite(a).all() or (np.abs(a) > limit).any():
            return False
        if strict_positive and not (a > 0).all():
            return False
    return True


def p2_leaves(logits=(), q=(), l=(), scores=(), e_l=(), leaves=()) -> bool:  # noqa: E741
    return (_finite_le(logits, P2_LOGIT) and _finite_le(q, np.inf, strict_positive=True)
            and _finite_le(l, np.inf) and _finite_le(scores, P2_SCORE)
            and all(Fraction(x) <= P2_SCORE for x in e_l) and _finite_le(leaves, P2_LEAF))


def a1_selftest() -> dict:
    """The fixed A1 vectors of CERTIFICATE.md §3 (numpy float64 and Python floats)."""
    e53, e51 = 2.0 ** -53, 2.0 ** -51
    arr = (lambda x: np.array([x], dtype=np.float64))  # noqa: E731
    cases = {}

    def case(name, value, expected, required=True):
        cases[name] = {"value": repr(value), "expected": repr(expected),
                       "holds": bool(value == expected), "required": required}

    case("tie_down", float((arr(1.0) + arr(e53))[0]), 1.0)
    case("tie_up", float((arr(1.0) + arr(3 * e53))[0]), 1.0 + e51)
    case("div_1_3", float((arr(1.0) / arr(3.0))[0]), float(Fraction(1, 3)))
    case("div_2_3", float((arr(2.0) / arr(3.0))[0]), float(Fraction(2, 3)))
    case("mul_0.1_3", float((arr(0.1) * arr(3.0))[0]), float(Fraction(0.1) * 3))
    case("half", Fraction(float((arr(0.5) * arr(0.1))[0])), Fraction(0.1) / 2)
    case("thirty_second", Fraction(float((arr(2.0 ** -5) * arr(0.1))[0])), Fraction(0.1) / 32)
    sub = float((arr(2.0 ** -500) * arr(2.0 ** -560))[0])
    cases["subnormal"] = {"value": repr(sub), "mode": "gradual" if sub == 2.0 ** -1060 else
                          ("flush" if sub == 0.0 else "other"), "required": False,
                          "holds": sub in (2.0 ** -1060, 0.0)}
    step = arr(1.0) + arr(e53)
    case("no_extended", float((step - arr(1.0))[0]), 0.0)
    case("python_tie_up", 1.0 + 3 * e53, 1.0 + e51)
    ok = all(c["holds"] for c in cases.values() if c["required"]) and cases["subnormal"]["holds"]
    return {"ok": bool(ok), "cases": cases}
