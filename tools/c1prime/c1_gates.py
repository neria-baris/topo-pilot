"""C1' damage, leakage, support, registration and adequacy gates (API.md §10; protocol §7-§10).
All operational (not certified): fractions, inverted_cdf quantiles, inequalities as written."""

from __future__ import annotations

import c1_config  # noqa: F401  (sys.path)
import numpy as np

from topo_pilot.analysis.x4f_scores import r2_pooled

M2 = {"Dw_max": 0.02, "Dy_max": 0.05, "Dw_match": 0.01, "Dy_match": 0.02, "min_frames": 28,
      "leakage_max": 0.25}


def D_w(w_nat, w_pm_list) -> float:
    w_nat = np.asarray(w_nat)
    changed = sum(int(np.count_nonzero(np.asarray(w) != w_nat)) for w in w_pm_list)
    return changed / (2.0 * len(w_nat))


def D_y(y_nat, y_pm_list, tr_cov) -> float:
    y_nat = np.asarray(y_nat, dtype=np.float64)
    total = sum(float(np.sum((np.asarray(y, dtype=np.float64) - y_nat) ** 2)) for y in y_pm_list)
    return total / (2.0 * len(y_nat)) / float(tr_cov)


def leakage(y_p, y_m, nu_p, nu_m) -> float:
    dy = np.asarray(y_p, dtype=np.float64) - np.asarray(y_m, dtype=np.float64)
    dn = np.asarray(nu_p, dtype=np.float64) - np.asarray(nu_m, dtype=np.float64)
    return float(np.sum(dy * dn)) / float(np.sum(dn * dn))


def m2(Dw_T, Dy_T, Dw_C_list, Dy_C_list, L_T=None, active=False) -> dict:
    Dw_C, Dy_C = float(np.mean(Dw_C_list)), float(np.mean(Dy_C_list))
    ok_frames = sum(1 for w, y in zip(Dw_C_list, Dy_C_list)
                    if w <= M2["Dw_max"] and y <= M2["Dy_max"])
    crit = {"primary": Dw_T <= M2["Dw_max"] and Dy_T <= M2["Dy_max"],
            "family": Dw_C <= M2["Dw_max"] and Dy_C <= M2["Dy_max"],
            "matching": abs(Dw_T - Dw_C) <= M2["Dw_match"] and abs(Dy_T - Dy_C) <= M2["Dy_match"],
            "dispersion": ok_frames >= M2["min_frames"]}
    status = "PASS" if all(crit.values()) else "INCONCLUSIVE/FAMILY_UNMATCHED"
    if status == "PASS" and active:
        crit["leakage"] = L_T is not None and L_T <= M2["leakage_max"]
        if not crit["leakage"]:
            status = "INCONCLUSIVE/NUISANCE_CONFOUNDED"
    return {"Dw_T": Dw_T, "Dy_T": Dy_T, "Dw_C": Dw_C, "Dy_C": Dy_C, "frames_ok": ok_frames,
            "leakage": L_T, "leakage_active": bool(active), "criteria": crit, "status": status}


def mahalanobis(a, w, zt, fit, white) -> np.ndarray:
    a = np.asarray(a, dtype=np.float64)
    centred = a - fit["alpha"][np.asarray(w, dtype=np.int64)] - np.asarray(zt) @ fit["Gamma"] \
        - white["mean"]
    return np.linalg.norm(centred @ white["W"].T, axis=1)


def q99(DM_cal) -> float:
    return float(np.quantile(np.asarray(DM_cal, dtype=np.float64), 0.99, method="inverted_cdf"))


def frac_beyond(DM, q) -> float:
    DM = np.asarray(DM, dtype=np.float64)
    return float(np.count_nonzero(DM > q)) / float(DM.size)


def m3(F_S, F_D, F_T, F_C_list, Sup) -> dict:
    F_C = float(np.mean(F_C_list))
    cap = max(0.05, F_D + 0.02)
    crit = {"F_T": F_T <= cap, "F_C": F_C <= cap, "match": abs(F_T - F_C) <= 0.02,
            "sup": Sup["S"] >= 0.99 and Sup["D"] >= 0.98 and Sup["T"] >= 0.98
            and Sup["C"] >= 0.98}
    return {"F_S": F_S, "F_D": F_D, "F_T": F_T, "F_C": F_C, "Sup": dict(Sup), "criteria": crit,
            "status": "PASS" if all(crit.values()) else "INCONCLUSIVE/SUPPORT"}


def wrap(x) -> np.ndarray:
    """Angle to (-pi, pi]."""
    y = np.mod(np.asarray(x, dtype=np.float64) + np.pi, 2.0 * np.pi) - np.pi
    return np.where(y == -np.pi, np.pi, y)


def _med(x) -> float:
    return float(np.quantile(np.asarray(x, dtype=np.float64), 0.5, method="inverted_cdf"))


def v1(phi_p, phi_m, m32_p, m32_m) -> dict:
    delta = wrap(np.asarray(phi_p) - np.asarray(phi_m))
    ang = lambda m: np.arctan2(np.asarray(m)[:, 1], np.asarray(m)[:, 0])  # noqa: E731
    dstar = wrap(ang(m32_p) - ang(m32_m))
    med = _med(np.abs(dstar))
    sel = np.abs(dstar) >= med
    agree = (np.sign(delta[sel]) == np.sign(dstar[sel])) & (np.sign(dstar[sel]) != 0)
    frac = float(np.count_nonzero(agree)) / float(np.count_nonzero(sel))
    return {"median": med, "n": int(np.count_nonzero(sel)), "agreement": frac,
            "status": "PASS" if frac >= 0.75 else "INCONCLUSIVE/CHART_NOT_REGISTERING"}


def v2(phi_s, phi_pm, phi_T_pm) -> dict:
    d = np.concatenate([wrap(np.asarray(p) - np.asarray(phi_s)) for p in phi_pm])
    e = np.concatenate([wrap(np.asarray(p) - np.asarray(phi_s)) for p in phi_T_pm])
    kappa = float(np.sum(e * np.sign(d)) / np.sum(np.abs(d)))
    sel = np.abs(d) >= _med(np.abs(d))
    agree = (np.sign(e[sel]) == np.sign(d[sel])) & (np.sign(d[sel]) != 0)
    frac = float(np.count_nonzero(agree)) / float(np.count_nonzero(sel))
    ok = 0.5 <= kappa <= 1.5 and frac >= 0.80
    return {"kappa": kappa, "agreement": frac,
            "status": "PASS" if ok else "INCONCLUSIVE/MANIPULATION_FAILED"}


def m4(w_pred, w_true, y_pred, y_true, y_mean_cal) -> dict:
    acc = float(np.mean(np.asarray(w_pred) == np.asarray(w_true)))
    r2, why = r2_pooled(np.asarray(y_pred), np.asarray(y_true), np.asarray(y_mean_cal))
    ok = acc >= 0.95 and r2 is not None and r2 >= 0.50
    return {"accuracy": acc, "r2": r2, "r2_reason": why,
            "status": "PASS" if ok else "INCONCLUSIVE/DECODER_INADEQUATE"}
