"""C1' row bounds, certified constants and signed guards (API.md §7; CERTIFICATE.md §7-§8;
protocol §15.3.8-15.3.11). Bounds use only binary + and * in the displayed shapes, on numpy
arrays (float64, constants up(c)) or on Sym counting values (L5 counts)."""

from __future__ import annotations

from fractions import Fraction

import c1_cert as cc
import c1_config  # noqa: F401  (sys.path)

FLOOR = Fraction(1, 10**9)


def bound_constants() -> dict:
    exact = {"half": Fraction(1, 2), "u1": cc.U1, "gamma_V": cc.gamma(36),
             "gamma31_32": cc.gamma(31) / 32, "inv_1mu": 1 / (1 - cc.U),
             "c1_term": cc.U1 * cc.C1HAT + cc.DELTA1, "c3_term": cc.U1 * cc.C3HAT + cc.DELTA3,
             "tenth": Fraction(1, 10), "three_tenths": Fraction(3, 10),
             "thirty_second": Fraction(1, 32), "zeta": cc.ZETA, "two": Fraction(2)}
    return {k: cc.up(v) for k, v in exact.items()}


def _sum(terms):
    acc = terms[0]
    for t in terms[1:]:
        acc = acc + t
    return acc


def _rho_bar(rho):
    return rho + rho * rho


def _eps_d(d_v, qp_v, qm_v, rbp, rbm, c):
    return c["u1"] * d_v + rbp * qp_v + rbm * qm_v


def b_G(d, lam, qp, qm, rho_p, rho_m, e_l, c):
    """Theorem 2; d, lam are |d_v|, |lam_v| lists (length V)."""
    rbp, rbm = _rho_bar(rho_p), _rho_bar(rho_m)
    terms = []
    for v in range(len(d)):
        ed = _eps_d(d[v], qp[v], qm[v], rbp, rbm, c)
        el = c["u1"] * lam[v] + c["two"] * e_l + rho_p + rho_m
        terms.append(ed * lam[v] + (d[v] + ed) * el + c["gamma_V"] * d[v] * lam[v])
    return c["half"] * _sum(terms) + c["zeta"]


def b_A(d, Delta, qp, qm, rho_p, rho_m, max_abs_Delta, omega_TE, c):
    """Theorem 3; d, Delta are |d_v|, |Delta_v| lists (length V)."""
    rbp, rbm = _rho_bar(rho_p), _rho_bar(rho_m)
    first = (c["gamma_V"] + c["u1"]) * _sum([d[v] * Delta[v] for v in range(len(d))])
    second = _sum([_eps_d(d[v], qp[v], qm[v], rbp, rbm, c) * Delta[v] for v in range(len(d))])
    return c["half"] * (first + c["inv_1mu"] * (second + omega_TE * max_abs_Delta)) + c["zeta"]


def b_Y(Y, bA_T, bA_C_list, A_C_list, c):
    """Theorem 4 (Y); Y and A_C entries are absolute values."""
    return (c["u1"] * Y + bA_T + c["thirty_second"] * _sum(list(bA_C_list))
            + c["gamma31_32"] * _sum(list(A_C_list)) + c["zeta"])


def b_Z(Z, bY, G, bG, c):
    return c["u1"] * Z + bY + c["c1_term"] * G + c["tenth"] * bG \
        + c["zeta"]


def b_Zf(Zf, bA_full, G, bG, c):
    return c["u1"] * Zf + bA_full + c["c3_term"] * G \
        + c["three_tenths"] * bG + c["zeta"]


def B_constant(max_b, max_abs, n) -> Fraction:
    d_n = (int(n) - 1).bit_length()  # ceil(log2 n) for n >= 1
    return cc.OUT(max_b) + cc.gamma(d_n + 1) * Fraction(float(max_abs)) + cc.ZETA


def _F(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(float(x))


def guard_endpoint(L, U, B) -> dict:
    """(E): per model F = max(B, 1e-9); |L| <= F or |U| <= F -> INCONCLUSIVE/NUMERICAL."""
    per = {}
    for j in L:
        F_j = max(_F(B[j]), FLOOR)
        per[j] = {"F": F_j, "hit": abs(_F(L[j])) <= F_j or abs(_F(U[j])) <= F_j}
    hit = any(v["hit"] for v in per.values())
    return {"per_model": per, "status": "INCONCLUSIVE/NUMERICAL" if hit else "PASS"}


def guard_H5(lower, B_H) -> str:
    gam, g = _F(lower) - Fraction(1, 100), max(_F(B_H), FLOOR)
    if gam > g:
        return "PASS"
    return "INCONCLUSIVE/HEADROOM" if gam <= -g else "INCONCLUSIVE/NUMERICAL"


def guard_V3(L_list, B_list) -> str:
    pairs = [(_F(L), max(_F(B), FLOOR)) for L, B in zip(L_list, B_list)]
    if all(gam > g for gam, g in pairs):
        return "PASS"
    if any(gam <= -g for gam, g in pairs):
        return "INCONCLUSIVE/MODEL_HEADROOM"
    return "INCONCLUSIVE/NUMERICAL"


class Sym:
    """Counting value for L5: nodes, formal monomials (with multiplicity) and degree."""

    __slots__ = ("nodes", "monomials", "degree")

    def __init__(self, nodes=0, monomials=1, degree=1):
        self.nodes, self.monomials, self.degree = nodes, monomials, degree

    @classmethod
    def leaf(cls):
        return cls()

    @staticmethod
    def _as(x):
        return x if isinstance(x, Sym) else Sym()

    def __add__(self, other):
        o = self._as(other)
        return Sym(self.nodes + o.nodes + 1, self.monomials + o.monomials,
                   max(self.degree, o.degree))

    __radd__ = __add__

    def __mul__(self, other):
        o = self._as(other)
        return Sym(self.nodes + o.nodes + 1, self.monomials * o.monomials,
                   self.degree + o.degree)

    __rmul__ = __mul__

    @property
    def leaves(self) -> int:
        return self.nodes + 1

    def __repr__(self):
        return f"Sym(nodes={self.nodes}, monomials={self.monomials}, degree={self.degree})"


def row_certificate(ctx, r, idx, batch=512) -> dict:
    """N0 / H3 row certificate for oracle rows idx of r (§15.3.6-15.3.8): C0 reference and P1
    per donor history, r_h and P4 (route F where P1 fails), M-ln, P2, b^G per row and B^H."""
    import numpy as np

    T, E, pi, p0 = ctx.data["T"], ctx.data["E"], ctx.data["pi"], ctx.data["p0"]
    idx = np.asarray(idx, dtype=np.int64)
    rho_ref = cc.rho_bar_ref(32, p0["N"], p0["d"])
    rho, n_f, status = {}, 0, "PASS"
    for key in ("Hp", "Hm"):
        vals = []
        for s in range(0, len(idx), batch):
            rows = idx[s:s + batch]
            q_hat = r["o"][key]["q"][rows]
            ref = cc.reference_oracle(T, E, pi, r[key][rows])
            ok1 = cc.p1(ref["nu_min"], ref["finite"], p0["nu0"])
            r_h = cc.discrepancy(q_hat, ref["q_ref"])
            fail = np.flatnonzero(~ok1)
            routed = cc.route_f(T, E, pi, r[key][rows][fail], q_hat[fail]) if fail.size else []
            n_f += len(routed)
            got = {}
            for j, out in zip(fail.tolist(), routed):
                if not out["ok"]:
                    status = "FAIL_TECHNICAL/ORACLE"
                got[j] = out["rho_F"] if out["ok"] else Fraction(1)
            for j in range(len(rows)):
                if j in got:
                    vals.append(got[j])
                elif r_h[j] > Fraction(1, 2):
                    status, _ = "FAIL_TECHNICAL/ORACLE", vals.append(Fraction(1))
                else:
                    vals.append(cc.rho_main(r_h[j], rho_ref))
        rho[key] = vals
    qp, qm = r["o"]["Hp"]["q"][idx], r["o"]["Hm"]["q"][idx]
    e_l = cc.measured_log_error(np.hstack((qp, qm)), np.hstack((r["lp"][idx], r["lm"][idx])))
    rp = np.array([cc.up(x) for x in rho["Hp"]])
    rm = np.array([cc.up(x) for x in rho["Hm"]])
    el = np.array([float(x) for x in e_l])
    d, lam, G = np.abs(r["d"][idx]), np.abs(r["lam"][idx]), r["G"][idx]
    ok2 = cc.p2_leaves(q=(qp, qm), l=(r["lp"][idx], r["lm"][idx]), scores=(G,), e_l=e_l,
                       leaves=(qp, qm, d, lam, rp, rm, el))
    if not ok2 and status == "PASS":
        status = "FAIL_TECHNICAL/NUMERICAL"
    c = bound_constants()
    V = d.shape[1]
    bG = b_G([d[:, v] for v in range(V)], [lam[:, v] for v in range(V)],
             [qp[:, v] for v in range(V)], [qm[:, v] for v in range(V)], rp, rm, el, c)
    B_H = B_constant(float(np.max(bG)), float(np.max(np.abs(G))), len(idx))
    return {"status": status, "rho_p": rho["Hp"], "rho_m": rho["Hm"], "e_l": e_l,
            "bG": [float(x) for x in bG], "B_H": B_H, "route_F_count": n_f,
            "rho_bar_ref": rho_ref}
