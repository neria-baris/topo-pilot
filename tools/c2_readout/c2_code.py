"""C2 code: the K = 1, 2, 3 FWL fit, Ledoit-Wolf, the whitened-design checks, the QR-route GLS
operator and its Euclidean variant, the Lemma G1 identities, the interchange, the code phase,
the R1 wrapper with the zero-modulus overrides, the N2 radial support screen, the Haar frames and
the masked S* features (API.md §8; C2-FROZEN-v1 §2.4, §2.5, §2.8, §2.10, §2.11, §6.6).

Activations and oracle quantities only: nothing here reads a logit (§5.3 L4). No column is ever
dropped for rank (§2.4); a deficient design is reported, never repaired.
"""

from __future__ import annotations

from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_fit
import c1_gates
import c2_oracle as co2
import numpy as np
from scipy.linalg import solve_triangular

from topo_pilot.analysis import x4f_scores
from topo_pilot.contracts import SeedTree

DEG = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"
RADIAL, NUMERICAL = "EXCLUDED/RADIAL_SUPPORT", "EXCLUDED/NUMERICAL"
N_CLASS = 36


def _le(x, limit) -> bool:
    """x <= the exact CONTRACT value `limit` (a non-finite x fails)."""
    return bool(np.isfinite(x)) and Fraction(float(x)) <= cc.frac(limit)


# ---- FWL (§2.4; API.md §8.1) -----------------------------------------------------------------
def harmonics(phi, K) -> np.ndarray:
    """(cos phi, sin phi, cos 2 phi, sin 2 phi, ..., cos K phi, sin K phi)."""
    phi = np.asarray(phi, dtype=np.float64)
    cols = []
    for k in range(1, int(K) + 1):
        cols += [np.cos(k * phi), np.sin(k * phi)]
    return np.column_stack(cols)


def standardise(z_fit) -> tuple:
    return c1_fit.standardise_nuisance(z_fit)


def fwl(Y, w32, zt, f) -> dict:
    """OLS of Y on [onehot(w32), zt, f] (36 + 5 + 2K columns) by numpy.linalg.lstsq."""
    Y = np.asarray(Y, dtype=np.float64)
    f = np.asarray(f, dtype=np.float64)
    X = c1_fit.fwl_design(w32, zt, f)
    coef, _, rank, sv = np.linalg.lstsq(X, Y, rcond=None)
    nz = np.asarray(zt).shape[1]
    B = coef[N_CLASS + nz :].T
    return {
        "alpha": coef[:N_CLASS],
        "Gamma": coef[N_CLASS : N_CLASS + nz].T,
        "B": B,
        "rank": int(rank),
        "cond": float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf"),
        "sv_B": np.linalg.svd(B, compute_uv=False),
        "resid": Y - X @ coef,
        "K": f.shape[1] // 2,
        "p": Y.shape[1],
    }


def f1_fwl(fit) -> str:
    """Design rank 41 + 2K, cond <= 1e8, sigma_max(B) > 0, sigma ratio >= 1e-6 (F1)."""
    s = fit["sv_B"]
    ok = (
        fit["rank"] == N_CLASS + cc.N_NUIS + 2 * fit["K"]
        and _le(fit["cond"], cc.COND_MAX)
        and s[0] > 0
        and Fraction(float(s[-1])) >= cc.frac(cc.SV_RATIO) * Fraction(float(s[0]))
    )
    return "PASS" if ok else DEG


def ledoit_wolf(resid) -> np.ndarray:
    return x4f_scores.ledoit_wolf(resid)[1]


def lw_ok(S) -> bool:
    lam = np.linalg.eigvalsh(np.asarray(S, dtype=np.float64))
    return bool(lam[0] > float(cc.frac(cc.LW_RATIO)) * lam[-1])


def partial_r2(Y, w32, zt, f) -> float:
    """Within-class partial R^2 of f (reported): 1 - RSS(full) / RSS(base)."""
    Y = np.asarray(Y, dtype=np.float64)

    def rss(X):
        return float(np.sum((Y - X @ np.linalg.lstsq(X, Y, rcond=None)[0]) ** 2))

    base = rss(c1_fit.fwl_design(w32, zt, np.zeros((len(Y), 0))))
    return 1.0 - rss(c1_fit.fwl_design(w32, zt, f)) / base if base > 0 else float("nan")


# ---- GLS, QR route (§2.5, §13.2; API.md §8.2) ------------------------------------------------
def gls(Gamma, B, Sigma=None) -> dict:
    """L = R_x^-1 Q_x' R_Sigma^-T with Sigma = Lc Lc' and X~ = Lc^-1 X_n = Q_x R_x (GLS), or the
    QR of X_n itself (Euclidean, Sigma None). Rank and cond2 are checked on X~ (RC-10)."""
    Gamma, B = np.asarray(Gamma, dtype=np.float64), np.asarray(B, dtype=np.float64)
    Xn = np.hstack((Gamma, B))
    p, m = Xn.shape
    nz = Gamma.shape[1]
    out = {"Xt": None, "rank_Xt": 0, "cond_Xt": float("inf"), "status": DEG}
    with np.errstate(all="ignore"):
        try:
            Lc = None if Sigma is None else np.linalg.cholesky(np.asarray(Sigma, np.float64))
            Xt = Xn if Lc is None else solve_triangular(Lc, Xn, lower=True)
            out.update(Xt=Xt, rank_Xt=int(np.linalg.matrix_rank(Xt)))
            out["cond_Xt"] = float(np.linalg.cond(Xt, 2))
            Qx, Rx = np.linalg.qr(Xt)
            rhs = Qx.T if Lc is None else solve_triangular(Lc, Qx, lower=True, trans="T").T
            L = solve_triangular(Rx, rhs)
        except (np.linalg.LinAlgError, ValueError):
            L = np.full((m, p), np.nan)
    ok = out["rank_Xt"] == m and _le(out["cond_Xt"], cc.COND_MAX) and np.all(np.isfinite(L))
    out["status"] = "PASS" if ok else DEG
    L_G, L_B = L[:nz], L[nz:]
    P_S, P_G = B @ L_B, Gamma @ L_G
    out.update(L=L, L_G=L_G, L_B=L_B, P_S=P_S, P_G=P_G, P_rest=np.eye(p) - P_S - P_G)
    return out


def gls_identities(g, Gamma, B, Sigma=None) -> dict:
    """Lemma G1 by max-abs <= 1e-10: L X_n = I, idempotence, orthogonality, P_S Gamma = 0,
    P_G B = 0 and W-self-adjointness (W = Sigma^-1, or I)."""
    Gamma, B = np.asarray(Gamma, dtype=np.float64), np.asarray(B, dtype=np.float64)
    Xn, PS, PG = np.hstack((Gamma, B)), g["P_S"], g["P_G"]
    P = PS + PG
    with np.errstate(all="ignore"):
        W = np.eye(len(P)) if Sigma is None else np.linalg.inv(np.asarray(Sigma, np.float64))
        devs = (
            g["L"] @ Xn - np.eye(Xn.shape[1]),
            PS @ PS - PS,
            PG @ PG - PG,
            PS @ PG,
            PG @ PS,
            PS @ Gamma,
            PG @ B,
            W @ P - P.T @ W,
        )
        worst = max(float(np.max(np.abs(x))) for x in devs)
    if not np.isfinite(worst):
        worst = float("inf")
    return {"max_abs": worst, "ok": _le(worst, cc.T_GLS_ID)}


def interchange(y1, y2, P_S) -> tuple:
    """(y_S^{2<-1}, y_S^{1<-2}): arm 2 receives arm 1's code, and the reverse (Lemma G2)."""
    y1, y2 = np.asarray(y1, dtype=np.float64), np.asarray(y2, dtype=np.float64)
    shift = (y1 - y2) @ np.asarray(P_S).T
    return y2 + shift, y1 - shift


def code_pair(Y, alpha, w32, L_B) -> np.ndarray:
    w = np.asarray(w32, dtype=np.int64)
    return (np.asarray(Y, dtype=np.float64) - np.asarray(alpha)[w]) @ np.asarray(L_B).T


def code_phase(Y, alpha, w32, L_B) -> tuple:
    """Phase and modulus of the centred first-harmonic code pair (first two coordinates)."""
    c = code_pair(Y, alpha, w32, L_B)
    return np.arctan2(c[:, 1], c[:, 0]), np.hypot(c[:, 0], c[:, 1])


def zero_code_threshold(mod_fit) -> float:
    """1e-12 x the inverted_cdf median of the FIT modulus (per model and family; NEW-3)."""
    med = float(np.quantile(np.asarray(mod_fit, np.float64), 0.5, method="inverted_cdf"))
    return cc.ZERO_CODE * med


# ---- R1 (§2.11, §6.6; API.md §8.3) -----------------------------------------------------------
def r1(phi_c_p, phi_c_m, mod_p, mod_m, m32_p, m32_m, thr_code) -> dict:
    """The zero overrides on c1_gates.v1's inputs (before its median and agreement), then v1
    unchanged; PASS iff agreement >= 3/4 (exact)."""
    pp, pm = np.array(phi_c_p, dtype=np.float64), np.array(phi_c_m, dtype=np.float64)
    mp, mm = np.array(m32_p, dtype=np.float64), np.array(m32_m, dtype=np.float64)
    zmod = (np.linalg.norm(mp, axis=1) <= cc.ZERO_MOD) | (np.linalg.norm(mm, axis=1) <= cc.ZERO_MOD)
    zcode = (np.asarray(mod_p) <= thr_code) | (np.asarray(mod_m) <= thr_code)
    mp[zmod] = (1.0, 0.0)
    mm[zmod] = (1.0, 0.0)
    pp[zcode] = 0.0
    pm[zcode] = 0.0
    v = c1_gates.v1(pp, pm, mp, mm)
    dc = c1_gates.wrap(pp - pm)
    ds = c1_gates.wrap(np.arctan2(mp[:, 1], mp[:, 0]) - np.arctan2(mm[:, 1], mm[:, 0]))
    sel = np.abs(ds) >= v["median"]
    den = float(np.sum(np.abs(ds)))
    return {
        "status": "PASS" if Fraction(v["agreement"]) >= cc.R1 else "FAIL",
        "agreement": v["agreement"],
        "median": v["median"],
        "n": v["n"],
        "kappa_reg": float(np.sum(dc * np.sign(ds))) / den if den > 0 else float("nan"),
        "overrides": {"zero_mod": int(np.count_nonzero(zmod)), "zero_code": int(zcode.sum())},
        "R1_ZERO": int(np.count_nonzero(sel & ((np.sign(dc) == 0) | (np.sign(ds) == 0)))),
        "R1_UNSELECTED": int(np.count_nonzero(~sel)),
    }


# ---- N2 radial support screen (§2.10; API.md §8.4, §19.1 E-16) -------------------------------
def n2_fit(a2_fit, w32_fit) -> dict:
    """FIT class means, Sigma_2w = Ledoit-Wolf of the class-centred states, W = Sigma^-1/2,
    q99 of the FIT natural Mahalanobis norms (dimension-agnostic)."""
    a = np.asarray(a2_fit, dtype=np.float64)
    w = np.asarray(w32_fit, dtype=np.int64)
    counts = np.bincount(w, minlength=N_CLASS)
    mu = np.full((N_CLASS, a.shape[1]), np.nan)
    for c in np.flatnonzero(counts):
        mu[c] = a[w == c].mean(axis=0)
    out = {"mu": mu, "W": None, "q99": float("nan"), "status": RADIAL}
    if np.any(counts == 0):
        return out  # a symbol class without FIT rows (API.md C-36)
    lam, vec = np.linalg.eigh(x4f_scores.ledoit_wolf(a - mu[w])[1])
    if not lam[0] > 0:
        return dict(out, status=NUMERICAL)
    out.update(W=(vec / np.sqrt(lam)) @ vec.T, status="PASS")
    out["q99"] = c1_gates.q99(dm(a, w, out))
    return out


def dm(h, w32, fit) -> np.ndarray:
    centred = np.asarray(h, dtype=np.float64) - fit["mu"][np.asarray(w32, dtype=np.int64)]
    return np.linalg.norm(centred @ np.asarray(fit["W"]).T, axis=1)


def n2_gate(fit, w32, D2, S, C) -> dict:
    """F = fraction of (row, arm) states beyond q99; PASS iff F_S and F_C <= max(1/20, F_D +
    1/50) (exact). A radial support screen only: no statement about the joint law (RC-6)."""
    w = np.concatenate([np.asarray(w32, dtype=np.int64)] * len(D2))
    F, cnt = {}, {}
    for key, states in (("D", D2), ("S", S), ("C", C)):
        d = dm(np.vstack(states), w, fit)
        F[key] = c1_gates.frac_beyond(d, fit["q99"])
        cnt[key] = Fraction(int(np.count_nonzero(d > fit["q99"])), int(d.size))
    cap = max(cc.N2_FLOOR, cnt["D"] + cc.N2_SLACK)
    ok = cnt["S"] <= cap and cnt["C"] <= cap
    return {
        "status": "PASS" if ok else RADIAL,
        "F_D": F["D"],
        "F_S": F["S"],
        "F_C": F["C"],
        "cap": cap,
    }


# ---- Haar frames and the S* features (§2.8, §2.11; API.md §8.5) ------------------------------
def _roots(Sigma) -> tuple:
    lam, vec = np.linalg.eigh(np.asarray(Sigma, dtype=np.float64))
    return (vec * np.sqrt(lam)) @ vec.T, (vec / np.sqrt(lam)) @ vec.T


def haar_frames(j, count, p, Sigma) -> list:
    """P_R = Sigma^1/2 Q Q' Sigma^-1/2, Q = qr_pos of the frame stream's p x 6 normal draw."""
    S_half, S_ihalf = _roots(Sigma)
    out = []
    for r in range(int(count)):
        g = SeedTree(0).generator(cc.SCOPE, "frame", int(j), int(r))
        Q = c1_fit.qr_pos(g.standard_normal((int(p), cc.RS_K)))
        out.append(S_half @ (Q @ Q.T) @ S_ihalf)
    return out


def fstar(m32, K) -> tuple:
    """Masked oracle-phase harmonics f*_K = m_valid (cos k phi*, sin k phi*) (NEW-3)."""
    phi, valid = co2.phi_star(m32)
    return valid[:, None] * harmonics(phi, K), valid


# ---- one projector problem (F1 composition) --------------------------------------------------
def problem(Y, w32, zt, f, euclidean=False, fit=None) -> dict:
    """FWL (or the given fit), Ledoit-Wolf Sigma_eps, GLS (or the Euclidean variant), the G1
    identities and the F1 status of the float part (GLS-REF and decoders: c2_stats)."""
    fit = fwl(Y, w32, zt, f) if fit is None else fit
    Sigma = ledoit_wolf(fit["resid"])
    g = gls(fit["Gamma"], fit["B"], None if euclidean else Sigma)
    ids = gls_identities(g, fit["Gamma"], fit["B"], None if euclidean else Sigma)
    status = f1_fwl(fit)
    if status == "PASS" and not lw_ok(Sigma):
        status = DEG
    status = g["status"] if status == "PASS" else status
    if status == "PASS" and not ids["ok"]:
        status = NUMERICAL
    return {
        "fit": fit,
        "Sigma": Sigma,
        "g": g,
        "ids": ids,
        "status": status,
        "euclidean": bool(euclidean),
    }
