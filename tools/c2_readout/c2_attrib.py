"""C2 attribution (closed forms at ln_final_out/32; d = d_named, dy = y1 - y2): the A partition,
the energies, the exact random-6-plane reference r, nu_S, the operator decomposition, psi_max,
E|A_S| and its Cauchy-Schwarz bound, the rotation arm and s_rot, the C2-M quantities, the
descriptive ratio intervals (seed 620518), the other §2.12 descriptives and the POST-DESC values
(API.md §10; C2-FROZEN-v1 §2.6, §2.8-§2.12, §5.7, §6.1).

The family stream arrays are assembled here in indicator form (API.md §11.1); bounds and
decisions are c2_decide's.
"""

from __future__ import annotations

from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c1_means
import c2_code as ck
import c2_oracle as co2
import numpy as np
from c1_records import C1GateFailure
from scipy.linalg import solve_triangular

UNDEFINED = "UNDEFINED"
LABEL = "unlicensed (gate {}); computed after the outcome"


def _f(x) -> np.ndarray:
    return np.asarray(x, dtype=np.float64)


def ind(s, E) -> np.ndarray:
    """Indicator form s 1_E; a non-finite s on an eligible row is FAIL_TECHNICAL/NUMERICAL."""
    s, E = _f(s), np.asarray(E, dtype=bool)
    if not np.all(np.isfinite(s[E])):
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "non-finite statistic on an eligible row")
    return np.where(E, s, 0.0)


# ---- partition and energies (§2.6, §2.9) -----------------------------------------------------
def half_dot(d, v) -> np.ndarray:
    """1/2 sum_v d_v v_v with the ordered C4 kernel of c1_endpoint.A_hat."""
    v = _f(v)
    return c1_endpoint.A_hat(d, v, np.zeros_like(v))


def centre(v) -> np.ndarray:
    v = _f(v)
    return v - v.mean(axis=1, keepdims=True)


def energy(v) -> np.ndarray:
    return np.sum(centre(v) ** 2, axis=1)


def _through(dy, P, M) -> np.ndarray:
    return (_f(dy) @ _f(P).T) @ _f(M).T


def partition(d, M, dy, P_S, P_G) -> dict:
    A_full = half_dot(d, _f(dy) @ _f(M).T)
    A_S, A_G = half_dot(d, _through(dy, P_S, M)), half_dot(d, _through(dy, P_G, M))
    return {"A_full": A_full, "A_S": A_S, "A_G": A_G, "A_rest": A_full - A_S - A_G}


def energies(M, dy, P_S) -> dict:
    return {"e_full": energy(_f(dy) @ _f(M).T), "e_S": energy(_through(dy, P_S, M))}


def _CM(M) -> np.ndarray:
    M = _f(M)
    return M - M.mean(axis=0)


def random_ref(M, Sigma, dy, e_full) -> dict:
    """r = a e_full + b tau_K w'w (Lemma RS2), tau_K = tr(C M Sigma M' C), w'w = dy' Sigma^-1 dy."""
    CM = _CM(M)
    tau_K = float(np.trace(CM @ _f(Sigma) @ CM.T))
    w = solve_triangular(np.linalg.cholesky(_f(Sigma)), _f(dy).T, lower=True)
    wtw = np.sum(w * w, axis=0)
    r = float(cc.RS_A) * _f(e_full) + float(cc.RS_B) * tau_K * wtw
    return {"r": r, "tau_K": tau_K, "wtw": wtw}


def pair(d, M, y1, y2, P_S, P_G, Sigma) -> dict:
    """The partition, energies and r of one arm pair under one projector problem."""
    dy = _f(y1) - _f(y2)
    out = dict(partition(d, M, dy, P_S, P_G), **energies(M, dy, P_S), dy=dy)
    out["r"] = random_ref(M, Sigma, dy, out["e_full"])["r"]
    return out


# ---- readout-null and operator decompositions, psi_max, E|A_S| (§2.12) -----------------------
def null_projector(M) -> np.ndarray:
    """J = I - V_r V_r', V_r the right singular vectors of C M at its matrix_rank (C-28)."""
    CM = _CM(M)
    r = int(np.linalg.matrix_rank(CM))
    V = np.linalg.svd(CM)[2][:r].T
    return np.eye(CM.shape[1]) - V @ V.T


def decomposition(d, M, dy, P, J) -> dict:
    I = np.eye(len(J))  # noqa: E741
    vis, null = _through(_f(dy) @ (I - _f(J)).T, P, M), _through(_f(dy) @ _f(J).T, P, M)
    return {
        "A_vis": half_dot(d, vis),
        "A_null": half_dot(d, null),
        "e_vis": energy(vis),
        "e_null": energy(null),
    }


def nu_S(J, P_S, dy) -> float:
    v = _f(dy) @ _f(P_S).T
    return float(np.mean(np.sum((v @ _f(J).T) ** 2, 1)) / np.mean(np.sum(v * v, 1)))


def psi_max(d, M, dy, E) -> float:
    """1/2 (sum of the 6 largest eigenvalues of sym E[ind(dy (M'd)')]) / E[ind(A_full)]."""
    E = np.asarray(E, dtype=bool)
    dyE, dE = _f(dy)[E], _f(d)[E]
    S = dyE.T @ (dE @ _f(M)) / len(E)
    lam = np.linalg.eigvalsh((S + S.T) / 2)
    A_full = ind(half_dot(d, _f(dy) @ _f(M).T), E)
    return float(0.5 * np.sum(lam[-cc.RS_K :]) / np.mean(A_full))


def cs_bound(d, e_S, E) -> float:
    E = np.asarray(E, dtype=bool)
    d2 = float(np.mean(np.sum(_f(d)[E] ** 2, axis=1)))
    return 0.5 * float(np.sqrt(d2)) * float(np.sqrt(np.mean(_f(e_S)[E])))


def abs_mean(A_S, E) -> float:
    return float(np.mean(np.abs(_f(A_S)[np.asarray(E, dtype=bool)])))


def _softmax(z) -> np.ndarray:
    z = _f(z)
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def fisher_energy(M, dy, P_S, z_p, z_m) -> np.ndarray:
    """v' (diag(p) - p p') v, v = C M P_S dy, p = (softmax(z+) + softmax(z-)) / 2 (reported)."""
    v, p = centre(_through(dy, P_S, M)), 0.5 * (_softmax(z_p) + _softmax(z_m))
    return np.sum(p * v * v, axis=1) - np.sum(p * v, axis=1) ** 2


def affine_readouts(Y_fit, w32_fit, nu_fit) -> dict:
    """OLS affine maps on FIT natural rows from y to onehot(w32) and to nu (C-26); slopes."""
    Y = _f(Y_fit)
    X = np.hstack((np.ones((len(Y), 1)), Y))
    onehot = (np.asarray(w32_fit)[:, None] == np.arange(cc.V)[None, :]).astype(np.float64)
    coef = {k: np.linalg.lstsq(X, T, rcond=None)[0][1:] for k, T in (("w", onehot), ("nu", nu_fit))}
    return {"R_w": coef["w"], "R_nu": coef["nu"]}


def readout_change(R, dy, P_S, E) -> np.ndarray:
    E = np.asarray(E, dtype=bool)
    return np.mean((_f(dy)[E] @ _f(P_S).T) @ _f(R), axis=0)


# ---- rotation arm (§2.11; report only) -------------------------------------------------------
def rotation_block(K, theta) -> np.ndarray:
    """Block k = [[cos k theta, -sin k theta], [sin k theta, cos k theta]] (frozen orientation)."""
    R = np.zeros((2 * int(K), 2 * int(K)))
    for k in range(1, int(K) + 1):
        c, s = np.cos(k * theta), np.sin(k * theta)
        R[2 * k - 2 : 2 * k, 2 * k - 2 : 2 * k] = ((c, -s), (s, c))
    return R


def y_rot(Y, alpha, w32, B, L_B, theta) -> np.ndarray:
    """y + B (R_K(theta) - I) f-hat, f-hat = L_B (y - alpha_w): the code rotates, the rest holds."""
    fh = ck.code_pair(Y, alpha, w32, L_B)
    R = rotation_block(fh.shape[1] // 2, theta) - np.eye(fh.shape[1])
    return _f(Y) + (fh @ R.T) @ _f(B).T


def rotation_arm(d_rot, M, y_p, y_m, G_rot, E) -> dict:
    E = np.asarray(E, dtype=bool)
    A = half_dot(d_rot, (_f(y_p) - _f(y_m)) @ _f(M).T)
    s_rot = float(np.count_nonzero(A[E] > 0)) / float(np.count_nonzero(E))
    return {"A_rot": A, "s_rot": s_rot, "theta_rot": float(np.mean(A[E]) / np.mean(_f(G_rot)[E]))}


# ---- C2-M (§2.10) ----------------------------------------------------------------------------
def cm_replacements(a2_H, a2_D, P2) -> dict:
    H, Dn, P2 = _f(a2_H), _f(a2_D), _f(P2)
    delta = Dn - H
    return {"F": Dn, "S": H + delta @ P2.T, "C": H + delta @ (np.eye(len(P2)) - P2).T}


def cm_quantities(d, z, A_full) -> dict:
    """A_M,X and e_M,X for X in F, S, C from z[X] = (z_X+, z_X-); I_M and A_M,ctx (reported)."""
    out = {}
    for X in ("F", "S", "C"):
        dz = _f(z[X][0]) - _f(z[X][1])
        out[f"A_{X}"], out[f"e_{X}"] = half_dot(d, dz), energy(dz)
    out["I_M"] = out["A_F"] - out["A_S"] - out["A_C"]
    out["A_ctx"] = _f(A_full) - out["A_F"]
    return out


def cm_placebo(dR, z_nat_H, z_S_R, z_F_R) -> dict:
    return {
        "AR_S": half_dot(dR, _f(z_nat_H) - _f(z_S_R)),
        "AR_F": half_dot(dR, _f(z_nat_H) - _f(z_F_R)),
    }


def ln_scale_ratio(rep, a2_H, eps) -> np.ndarray:
    """sqrt(Var(rep) + eps) / sqrt(Var(a2(H)) + eps) per row (C-30)."""
    return np.sqrt(np.var(_f(rep), axis=1) + eps) / np.sqrt(np.var(_f(a2_H), axis=1) + eps)


# ---- ratio intervals, POST-DESC (§2.10 NEW-5, §2.11, §5.7 NEW-6) -----------------------------
def ratio_intervals(nums, dens, pairs, seed, draws) -> dict:
    """One shared bootstrap_means stream over every array; per (num, den) the two-sided 95 %
    percentile interval (ranks 125 / 4,875 of 5,000) of the ratio of resampled means, or
    UNDEFINED on a zero (original or resampled) denominator or a non-finite value."""
    allm = c1_means.bootstrap_means({**nums, **dens}, seed, draws)
    out = {}
    for num, den in pairs:
        r = allm[num] / np.where(allm[den] == 0, np.nan, allm[den])
        bad = c1_means.tree_mean(dens[den]) == 0 or np.any(allm[den] == 0)
        bad = bad or not (np.all(np.isfinite(nums[num])) and np.all(np.isfinite(dens[den])))
        if bad or not np.all(np.isfinite(r)):
            out[f"{num}/{den}"] = UNDEFINED
            continue
        lo = c1_means.quantile_with_rank(r, cc.DESC_ALPHA)[0]
        hi = c1_means.quantile_with_rank(r, 1 - cc.DESC_ALPHA)[0]
        out[f"{num}/{den}"] = {"L": lo, "U": hi}
    return out


def desc_intervals(nums, dens, pairs) -> dict:
    """The C2-M descriptive stream: PCG64(620518), 5,000 draws, 24 arrays (NEW-5)."""
    return ratio_intervals(nums, dens, pairs, cc.seed("test_M_desc"), cc.DESC_DRAWS)


def post_desc(arrays) -> dict:
    """Eligible-row point ratios only, labelled unlicensed (NEW-6); no bound, no category."""
    out = {}
    for name, a in arrays.items():
        E = np.asarray(a["E"], dtype=bool)
        value = float(np.mean(_f(a["num"])[E]) / np.mean(_f(a["den"])[E]))
        out[name] = {"value": value, "label": LABEL.format(a["gate"])}
    return out


# ---- family stream arrays in indicator form (API.md §11.1) -----------------------------------
C = {"V3": float(cc.V3), "low": float(cc.PSI_LOW), "high": float(cc.PSI_HIGH)}
C.update(abs=float(cc.E_ABS), rand=float(cc.E_RAND), plac=float(cc.PLACEBO))


def threshold_arrays(q, E, prefix="") -> dict:
    """Z010, Z050, Vabs, Vrand of one pair() result (x pair, E_x)."""
    out = {"Z010": q["A_S"] - C["low"] * q["A_full"], "Z050": q["A_S"] - C["high"] * q["A_full"]}
    out.update(Vabs=q["e_S"] - C["abs"] * q["e_full"], Vrand=q["e_S"] - C["rand"] * q["r"])
    return {prefix + k: ind(v, E) for k, v in out.items()}


def r_arrays(qx, qy, G_x, E_x, E_y, variants=None, y_name="Y1") -> dict:
    """The R (or S*, y_name "Y1*") stream of one model: V3x, Y1, Z010, Z050, Vabs, Vrand, NEG
    and the variant arrays "<v>:Z010" ... (19 arrays with three variants)."""
    out = {"V3x": ind(c1_endpoint.Zfull_hat(qx["A_full"], G_x), E_x)}
    out[y_name] = ind(qy["A_S"] - C["plac"] * qy["A_full"], E_y)
    out.update(threshold_arrays(qx, E_x), NEG=ind(qx["A_S"], E_x))
    for v, qv in (variants or {}).items():
        out.update(threshold_arrays(qv, E_x, prefix=f"{v}:"))
    return out


def m_arrays(cm, cmR, A_full, AR_full, G_x, E_x, E_y) -> dict:
    """The M stream of one model: V3x, Ztau, ZM010, ZM050, VM, Y2, NEG (and Y2's activity)."""
    out = {"V3x": ind(c1_endpoint.Zfull_hat(A_full, G_x), E_x)}
    out["Ztau"] = ind(cm["A_F"] - float(cc.TAU_M) * _f(A_full), E_x)
    out["ZM010"] = ind(cm["A_S"] - C["low"] * cm["A_F"], E_x)
    out["ZM050"] = ind(cm["A_S"] - C["high"] * cm["A_F"], E_x)
    out["VM"] = ind(cm["e_S"] - C["abs"] * cm["e_F"], E_x)
    out["Y2"] = ind(cmR["AR_S"] - C["plac"] * cmR["AR_F"], E_y)
    out["Y2act"] = ind(cmR["AR_F"] - C["plac"] * _f(AR_full), E_y)
    out["NEG"] = ind(cm["A_S"], E_x)
    return out


def point_ratios(family, q, E) -> dict:
    """Eligible-row point estimates of a family (report.json `point`, API.md §15.2)."""
    E = np.asarray(E, dtype=bool)

    def ratio(a, b):
        den = float(np.mean(_f(b)[E]))
        return float(np.mean(_f(a)[E])) / den if den != 0 else float("nan")

    if family == "M":
        return {
            "tau_M": ratio(q["A_F"], q["A_full"]),
            "psi_M": ratio(q["A_S"], q["A_F"]),
            "eta_M": ratio(q["e_S"], q["e_F"]),
            "psi_M_C": ratio(q["A_C"], q["A_F"]),
        }
    out = {"psi": ratio(q["A_S"], q["A_full"]), "theta_full": ratio(q["A_full"], q["G"])}
    out.update(psi_G=ratio(q["A_G"], q["A_full"]), psi_rest=ratio(q["A_rest"], q["A_full"]))
    out.update(theta_S=ratio(q["A_S"], q["G"]), eta_S=ratio(q["e_S"], q["e_full"]))
    out["eta_R_bar"] = ratio(q["r"], q["e_full"])
    out["g"] = (
        float((Fraction(cc.RS_B) * cc.RS_N) / (Fraction(out["eta_R_bar"]) - cc.RS_A))
        if np.isfinite(out["eta_R_bar"]) and out["eta_R_bar"] != float(cc.RS_A)
        else float("nan")
    )
    return out


# ---- one model on one split (driver composition) ---------------------------------------------
def closed_streams(F, y, o, perm) -> dict:
    """The x/y pair quantities of every passing ln_final problem and the R and S* streams of one
    model on one split. F = {"M": M, "prob": {p: {"P_S", "P_G", "Sigma", "ok"}}}, y = {role: y},
    o = the split's ORACLE arrays (canonical q-bar; d converted to named order, RC-1)."""
    dx = co2.d_named(o["Hp_qbar"] - o["Hm_qbar"], perm)
    dR = co2.d_named(o["H_qbar"] - o["HR_qbar"], perm)
    Ex, Ey, M = np.asarray(o["E_x"], bool), np.asarray(o["E_y"], bool), F["M"]
    ok = {p: f for p, f in F["prob"].items() if f["ok"] and p != "M"}
    q = {p: pair(dx, M, y["Hp"], y["Hm"], f["P_S"], f["P_G"], f["Sigma"]) for p, f in ok.items()}
    for v in q.values():
        v["G"] = _f(o["G_x"])
    qy = {
        p: pair(dR, M, y["H"], y["HR"], ok[p]["P_S"], ok[p]["P_G"], ok[p]["Sigma"])
        for p in ("R", "S*")
        if p in ok
    }
    out = {"q": q, "qy": qy, "d_x": dx, "d_y": dR}
    if "R" in q:
        var = {v: q[v] for v in cc.VARIANTS if v in q}
        out["R"] = r_arrays(q["R"], qy["R"], o["G_x"], Ex, Ey, var)
    if "S*" in q:
        out["S*"] = r_arrays(q["S*"], qy["S*"], o["G_x"], Ex, Ey, y_name="Y1*")
    return out
