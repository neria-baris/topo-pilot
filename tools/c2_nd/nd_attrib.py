"""C2ND attribution (closed forms; d = d_named; dy = y1 - y2; arm 1 = H+, arm 2 = H-): the N-R
complement quantities and stream (Lemma N1), the N-M stream on the C2-M quantities, the D stream
and the known-case arrays under a refit projector, the estimation leak, canonical angles and
kappa_leak, the LN-scale split, the oracle response identity and the descriptive ratios (API.md
§7, §20; C2ND-DESIGN-v1 §2.3, §2.4, §2.8, §2.9, §3 row 9, §4.2).

Arrays are formed in indicator form with the unchanged C2 kernels (c2_attrib.ind, half_dot,
energy, threshold_arrays, r_arrays, cm_quantities; c1_endpoint.Zfull_hat). The D and known-case
arrays refuse any projector not tagged with a refit problem (S12; ND-C26). Bounds and decisions
are nd_decide's. Every dimension comes from the inputs (ND-C33).
"""

from __future__ import annotations

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_endpoint
import c1_oracle
import c2_attrib as ca
import c2_decide as cdc
import numpy as np
from c1_records import C1GateFailure

LEAKAGE = "INVALID/LEAKAGE"
C = {"low": float(nc.PSI_LOW), "high": float(nc.PSI_HIGH), "p90": float(nc.PSI_090)}
C.update(neg=float(nc.NEG_LOW), abs=float(nc.E_ABS), tau=float(nc.TAU_M))
NR_KEYS = ("V3x", "Y1", "Zc010", "Zc050", "Wc", "Vc", "NEGc", "Zc090", "Zc100", "Z090")
NM_KEYS = ("V3x", "Ztau", "ZMc010", "ZMc050", "WMc", "VMc", "NEGMc")
NEC_KEYS = ("Zc010", "Zc050", "Wc", "Vc", "NEGc")
NEC_CASES = ("DONLY", "DDOSE")  # the known cases with a listed necessity category (§5.2)


def _f(x) -> np.ndarray:
    return np.asarray(x, dtype=np.float64)


def _comp(P) -> np.ndarray:
    P = _f(P)
    return np.eye(P.shape[0]) - P


# ---- N-R: the complement interchange (§2.3, Lemma N1; API.md §7.1) ---------------------------
def comp_arm(y1, y2, P_S) -> np.ndarray:
    """y_C^{2<-1} = y2 + (I - P_S)(y1 - y2): arm 2 receives arm 1's complement."""
    y1, y2 = _f(y1), _f(y2)
    return y2 + (y1 - y2) @ _comp(P_S).T


def nr_quantities(d, M, y1, y2, P_S) -> dict:
    """A_full, A_S, A_comp = A_full - A_S (by subtraction), e_full, e_S, e_comp and the cross
    term e_full - e_S - e_comp (energy is not additive)."""
    dy, M = _f(y1) - _f(y2), _f(M)
    A_full = ca.half_dot(d, dy @ M.T)
    A_S = ca.half_dot(d, (dy @ _f(P_S).T) @ M.T)
    out = {"A_full": A_full, "A_S": A_S, "A_comp": A_full - A_S}
    out.update(ca.energies(M, dy, P_S))
    out["e_comp"] = ca.energy((dy @ _comp(P_S).T) @ M.T)
    out["cross"], out["dy"] = out["e_full"] - out["e_S"] - out["e_comp"], dy
    return out


def a_comp_direct(d, z_C, z_2) -> np.ndarray:
    """The patched complement arm against arm 2's natural logits (X1 compares it with A_comp)."""
    return ca.half_dot(d, _f(z_C) - _f(z_2))


def nr_stream(q, qy, G_x, E_x, E_y, variants=None) -> dict:
    """The N-R family stream of one model (§4.2): 10 arrays plus 2 per variant (16 with three);
    Y1 on the frozen C2 projector; the variants v:Zc010, v:Zc050 use A_S of {v}_P_S."""
    A_full, A_S, A_comp = _f(q["A_full"]), _f(q["A_S"]), _f(q["A_comp"])
    out = {"V3x": ca.ind(c1_endpoint.Zfull_hat(A_full, G_x), E_x)}
    out["Y1"] = ca.ind(_f(qy["A_S"]) - float(nc.PLACEBO) * _f(qy["A_full"]), E_y)
    out["Zc010"] = ca.ind(A_comp - C["low"] * A_full, E_x)
    out["Zc050"] = ca.ind(A_comp - C["high"] * A_full, E_x)
    out["Wc"] = ca.ind(A_comp - C["neg"] * A_full, E_x)
    out["Vc"] = ca.ind(_f(q["e_comp"]) - C["abs"] * _f(q["e_full"]), E_x)
    out["NEGc"] = ca.ind(A_comp, E_x)
    out["Zc090"] = ca.ind(A_comp - C["p90"] * A_full, E_x)
    out["Zc100"] = ca.ind(A_comp - A_full, E_x)
    out["Z090"] = ca.ind(A_S - C["p90"] * A_full, E_x)
    for v in nc.VARIANTS:
        if v in (variants or {}):
            comp_v = A_full - _f(variants[v]["A_S"])
            out[f"{v}:Zc010"] = ca.ind(comp_v - C["low"] * A_full, E_x)
            out[f"{v}:Zc050"] = ca.ind(comp_v - C["high"] * A_full, E_x)
    return out


# ---- N-M (§2.4; API.md §7.2) -----------------------------------------------------------------
cm_replacements, cm_quantities, ln_scale_ratio = (
    ca.cm_replacements,
    ca.cm_quantities,
    ca.ln_scale_ratio,
)


def nm_stream(cm, A_full, G_x, E_x) -> dict:
    """The N-M family stream of one model (7 arrays): categories on A_C against A_F only."""
    A_F, A_C, A_full = _f(cm["A_F"]), _f(cm["A_C"]), _f(A_full)
    out = {"V3x": ca.ind(c1_endpoint.Zfull_hat(A_full, G_x), E_x)}
    out["Ztau"] = ca.ind(A_F - C["tau"] * A_full, E_x)
    out["ZMc010"] = ca.ind(A_C - C["low"] * A_F, E_x)
    out["ZMc050"] = ca.ind(A_C - C["high"] * A_F, E_x)
    out["WMc"] = ca.ind(A_C - C["neg"] * A_F, E_x)
    out["VMc"] = ca.ind(_f(cm["e_C"]) - C["abs"] * _f(cm["e_F"]), E_x)
    out["NEGMc"] = ca.ind(A_C, E_x)
    return out


# ---- D and the known cases under a refit projector (§2.8, §4.2, §5.2; API.md §7.3) -----------
def check_refit(refit, allowed=nc.REFITS) -> str:
    """The refit tag of a projector dict; the construction projector or the C2 FIT problem R in
    a method statistic is a stop-rule S12 violation -> INVALID/LEAKAGE (§2.8; §20 A-4)."""
    prob = refit.get("problem") if isinstance(refit, dict) else None
    if prob not in allowed or (isinstance(refit, dict) and refit.get("construction")):
        raise C1GateFailure(LEAKAGE, f"projector {prob!r} in a method statistic (S12)")
    return prob


def d_stream(qx, qy, G_x, E_x, E_y, qx_r=None, refit=None, refit_r=None) -> dict:
    """The D family stream of one model: the seven C2 R arrays of D-NULL under the RD refit, and
    (report-only) the five DNULLR: arrays of D-NULL-R under the RT refit (`refit_r`)."""
    check_refit(refit, ("RD",))
    out = ca.r_arrays(qx, qy, G_x, E_x, E_y)
    if qx_r is not None:
        check_refit(refit_r, ("RT",))
        out.update(ca.threshold_arrays(qx_r, E_x, prefix="DNULLR:"))
        out["DNULLR:NEG"] = ca.ind(qx_r["A_S"], E_x)
    return out


def case_arrays(case, qx, qy, G_x, G_y, E_x, E_y, refit=None) -> dict:
    """KC / KC-R arrays of one case (keys "<case>:<stat>"): the R arrays, the case's own y
    response V3y (its Y1 activity, ND-C31) and, for DONLY and DDOSE, the N-R necessity arrays
    with A_comp = A'_full - A'_S under the refit projector (qx must then hold "e_comp")."""
    if refit is not None:
        check_refit(refit, ("RT",) if case in nc.KCR_CASES else ("RD",))
    out = ca.r_arrays(qx, qy, G_x, E_x, E_y)
    out["V3y"] = ca.ind(c1_endpoint.Zfull_hat(qy["A_full"], G_y), E_y)
    if case in NEC_CASES:
        q = dict(qx, A_comp=_f(qx["A_full"]) - _f(qx["A_S"]))
        nr = nr_stream(q, qy, G_x, E_x, E_y)
        out.update({k: nr[k] for k in NEC_KEYS})
    return {f"{case}:{k}": v for k, v in out.items()}


def leak(d, M_prime, dy, P_hat, P_S) -> np.ndarray:
    """1/2 d' M' (P_hat - P_S) dy: the D-NULL refit code share is this leak (T-LEAK)."""
    return ca.half_dot(d, (_f(dy) @ (_f(P_hat) - _f(P_S)).T) @ _f(M_prime).T)


def canonical_angles(B_hat, B) -> np.ndarray:
    """The principal angles between col(B_hat) and col(B), ascending (radians)."""
    Q1, Q2 = np.linalg.qr(_f(B_hat))[0], np.linalg.qr(_f(B))[0]
    s = np.linalg.svd(Q1.T @ Q2, compute_uv=False)
    return np.sort(np.arccos(np.clip(s, -1.0, 1.0)))


def kappa_leak(M, P_S, B_hat) -> float:
    """||C M (I - P_S) B_hat||_2 / ||C M B_hat||_2 (blind S2 diagnostic; reported, not gated)."""
    CM = _f(M) - _f(M).mean(axis=0)
    B_hat = _f(B_hat)
    return float(np.linalg.norm(CM @ _comp(P_S) @ B_hat, 2) / np.linalg.norm(CM @ B_hat, 2))


# ---- guards (§4.4; API.md §8.1, ND-C16; aliased in nd_decide) ------------------------------
NR_A = ("Zc010", "Zc050", "Wc", "NEGc", "Zc090", "Zc100", "Z090")


def nr_guards(arrays, geo) -> dict:
    """N-R guards: beta_A (coefficient 1, delta_P of the frozen C2 projector) on every
    A_comp-type array (ND-C16), Y1 on the y pair, beta_E with I - P_S for Vc, delta_P(v) for the
    variant arrays; V3x none."""
    M, (d, dy, Ex), (dY, dyY, Ey), dP = geo["M"], geo["x"], geo["y"], geo["delta_P"]
    out = {}
    for name, s in arrays.items():
        v, _, stat = name.rpartition(":")
        if v:
            beta = cdc.beta_A(d, M, dy, geo["variants"][v][1], 1, Ex)
        elif stat == "Y1":
            beta = cdc.beta_A(dY, M, dyY, dP, 1, Ey)
        elif stat == "Vc":
            beta = cdc.beta_E(M, dy, np.eye(len(geo["P_S"])) - np.asarray(geo["P_S"]), dP, 1, Ex)
        else:
            beta = cdc.beta_A(d, M, dy, dP, 1, Ex) if stat in NR_A else 0.0
        out[name] = cdc.guard(s, beta)
    return out


def d_guards(arrays, geo_D, geo_R=None) -> dict:
    """c2_decide.stream_guards on the DNULL arrays (M', RD refit delta_P) and on the "DNULLR:"
    arrays (g_D M, the y @ T.T rows, RT refit delta_P); no construction-error term (MD-15)."""
    main = {k: v for k, v in arrays.items() if not k.startswith("DNULLR:")}
    out = cdc.stream_guards(main, geo_D)
    rest = {k: v for k, v in arrays.items() if k.startswith("DNULLR:")}
    return dict(out, **(cdc.stream_guards(rest, geo_R) if rest else {}))


def nm_guards(arrays) -> dict:
    return {k: cdc.guard(s, 0.0) for k, s in arrays.items()}


# ---- LN-scale split (§2.9; API.md §7.3, §20 A-1) ---------------------------------------------
def sigma(a3, eps) -> np.ndarray:
    """sqrt(Var(a3_i) + eps) per row of the resid_post_3 rows at position 32 ([n, d_model])."""
    return np.sqrt(np.var(_f(a3), axis=1) + float(eps))


def ln_split(y1, y2, s1, s2) -> tuple:
    """(dy_dir, dy_sig): dy_sig = (1 - s1/s2) y1, dy_dir = (s1/s2) y1 - y2 (exact split)."""
    y1, y2 = _f(y1), _f(y2)
    r = (_f(s1) / _f(s2))[:, None]
    return r * y1 - y2, (1.0 - r) * y1


def ln_sym(y1, y2, s1, s2) -> np.ndarray:
    """The symmetric sigma part over both arm orders."""
    return 0.5 * (ln_split(y1, y2, s1, s2)[1] - ln_split(y2, y1, s2, s1)[1])


def ln_arrays(d, M, P_S, y1, y2, s1, s2, M_prime=None) -> dict:
    """Per-row numerators of the LN-scale shares: 1/2 d' M (I - P_S) dy_sig (complement), with
    P_S (code), their symmetric versions, and 1/2 d' M' dy_sig for a decoy head M'."""
    M, out = _f(M), {}
    for tag, dsig in (("", ln_split(y1, y2, s1, s2)[1]), ("_sym", ln_sym(y1, y2, s1, s2))):
        out["ln_comp" + tag] = ca.half_dot(d, (dsig @ _comp(P_S).T) @ M.T)
        out["ln_code" + tag] = ca.half_dot(d, (dsig @ _f(P_S).T) @ M.T)
    if M_prime is not None:
        out["ln_decoy"] = ca.half_dot(d, ln_split(y1, y2, s1, s2)[1] @ _f(M_prime).T)
    return out


# ---- ORACLE-FEAS (i) (§3 row 9; API.md §7.4) -------------------------------------------------
def oracle_identity(qbar_p, qbar_m, d_named, perm, G) -> dict:
    """A_full with the oracle's own log-predictive equals G per row within 1e-12 max(1, |G|)."""
    lp_p = c1_oracle.named_from_canonical(np.log(_f(qbar_p)), perm)
    lp_m = c1_oracle.named_from_canonical(np.log(_f(qbar_m)), perm)
    A_or, G = ca.half_dot(d_named, lp_p - lp_m), _f(G)
    dev = np.abs(A_or - G)
    over = ~(dev <= float(nc.frac(nc.ORACLE_ID)) * np.maximum(1.0, np.abs(G)))
    max_dev = float(np.max(np.where(np.isfinite(dev), dev, np.inf))) if dev.size else 0.0
    n_over = int(np.count_nonzero(over))
    return {"max_dev": max_dev, "n_over": n_over, "ok": n_over == 0}


# ---- descriptives (§2.8, §2.9; API.md §7.5; report only) -------------------------------------
def point_ratios_nd(nums, dens, pairs, E) -> dict:
    """Eligible-row point ratios mean(num)/mean(den); nan on a zero denominator."""
    E, out = np.asarray(E, dtype=bool), {}
    for num, den in pairs:
        dv = float(np.mean(_f(dens[den])[E]))
        out[f"{num}/{den}"] = float(np.mean(_f(nums[num])[E])) / dv if dv != 0 else float("nan")
    return out


def descriptives_nd(nums, dens, pairs, E, extra=None) -> dict:
    """The point ratios and one c2_attrib.ratio_intervals call (seed 630508, 5,000 draws; ranks
    125 / 4,875; UNDEFINED on a zero or non-finite denominator, no redraw), plus `extra`
    (canonical angles, kappa_leak, the leak decomposition, the C2 §2.12 set) passed through.
    `nums`/`dens` are indicator-form arrays (lambda_D, LN-scale shares, eta_comp, iota_M, ...)."""
    out = {"point": point_ratios_nd(nums, dens, pairs, E)}
    out["intervals"] = ca.ratio_intervals(nums, dens, pairs, nc.seed("desc"), nc.DESC_DRAWS)
    out.update(extra or {})
    return out
