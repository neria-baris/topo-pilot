"""HWSU oracle quantities, KO cases, Decimal rows, Lemma P arrays, problem O (API.md §3; protocol
§2.2, §2.3, §2.6, §4.2, §5.2). All arithmetic is in canonical symbol order (D-1)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import numpy as np

import c1_oracle
import c2_attrib
import c2_code
import c2_decide
import c2_oracle
import c2_stats
import oracle_profile
from c1_records import C1GateFailure
from topo_pilot.oracle import BayesFilter

ORACLE = "FAIL_TECHNICAL/ORACLE"
CASES = ("KO1", "KO2", "KO3")


def helmert(n=36):
    out = np.zeros((int(n), int(n) - 1))
    for k in range(1, int(n)):
        s = np.sqrt(k * (k + 1.0))
        out[:k, k - 1] = 1.0 / s
        out[k, k - 1] = -k / s
    return out


def arm_oracle(T, E, pi, canon32, coords) -> dict:
    o = c2_oracle.oracle_role(T, E, pi, canon32, coords)
    o["logq"] = np.log(o["qbar"])
    o["nuis"] = c2_oracle.nuisance5(o["b32"], coords)
    return o


def suffix_oracle(T, E, pi, canons, coords, suffix_len=4) -> list:
    arrs = [np.asarray(c) for c in canons]
    stacked = np.vstack(arrs)
    suf = stacked[:, stacked.shape[1] - suffix_len:]
    uniq, inv = np.unique(suf, axis=0, return_inverse=True)
    inv = np.asarray(inv).reshape(-1)
    r = BayesFilter(T, E, pi).run(uniq.astype(np.int64))
    q = r.q[:, suffix_len]
    q4bar_u = q / q.sum(1, keepdims=True)
    b4_u = r.b[:, suffix_len - 1]
    m4_u = c1_oracle.m32(b4_u, coords)
    out, lo = [], 0
    for a in arrs:
        idx = inv[lo:lo + len(a)]
        lo += len(a)
        q4 = q4bar_u[idx]
        out.append({"q4bar": q4, "logq4": np.log(q4), "b4": b4_u[idx], "m4": m4_u[idx]})
    return out


def m4_check(T, E, pi, canon32, coords, m4) -> dict:
    ref = oracle_profile.posterior_means(T, E, pi, canon32, [4],
                                         oracle_profile.circle_features(coords))[4]
    err = float(np.max(np.abs(np.asarray(ref) - np.asarray(m4))))
    return {"max_abs": err, "ok": bool(err <= uc.M4_TOL)}


def pair_core(o1, o2) -> dict:
    G, d = c1_oracle.G_hat(o1["qbar"], o2["qbar"])[:2]
    return {"G": G, "d": d}


# ------------------------------------------------------------------------- KO cases (§5.2)
def ko_logits(o, s, case):
    if case == "KO1":
        return o["logq"]
    if case == "KO2":
        return s["logq4"]
    if case == "KO3":
        return s["logq4"] + float(uc.LAMBDA_KO3) * (o["logq"] - s["logq4"])
    raise ValueError(f"unknown case {case!r}")


def readout_A(d, z1, z2, N):
    return c2_attrib.half_dot(d, ((z1 - z2) @ N) @ N.T)


def ko_identities(G, A) -> dict:
    G = np.asarray(G, dtype=np.float64)
    scale = 1e-12 * np.maximum(1.0, np.abs(G))
    target = {"KO1": G, "KO2": np.zeros_like(G), "KO3": G * 0.2}
    tol = {"KO1": scale, "KO2": np.full_like(G, 1e-12), "KO3": scale}
    out = {}
    for k in CASES:
        dev = np.abs(np.asarray(A[k], dtype=np.float64) - target[k])
        out[k] = {"n_fail": int(np.sum(~(dev <= tol[k]))), "max_dev": float(np.max(dev)),
                  "ok": bool(np.all(dev <= tol[k]))}
    return out


_CAT = {"USED": "RESPONDS", "PARTIAL": "WEAK_RESPONSE", "NOT_USED": "LOW_RESPONSE",
        "LOW_ALIGNED": "LOW_RESPONSE"}
_EXPECT = {"KO1": ("RESPONDS", False), "KO2": ("LOW_RESPONSE", False),
           "KO3": ("WEAK_RESPONSE", True)}


def ko_categories(G, A, seed, alpha=None, draws=None) -> dict:
    alpha = uc.ALPHA_VAL if alpha is None else alpha
    draws = uc.DRAWS if draws is None else draws
    G = np.asarray(G, dtype=np.float64)
    arrays = {}
    for k in CASES:
        a = np.asarray(A[k], dtype=np.float64)
        arrays[f"{k}:ZR010"], arrays[f"{k}:ZR030"], arrays[f"{k}:AF"] = a - 0.1 * G, a - 0.3 * G, a
    b = c2_decide.stream_bounds(arrays, seed, alpha, draws)
    g = {name: c2_decide.guard(arr) for name, arr in arrays.items()}
    res, ok = {}, True
    for k in CASES:
        st = {s: {"L": b[f"{k}:{s}"]["L"], "U": b[f"{k}:{s}"]["U"], "g": g[f"{k}:{s}"]}
              for s in ("ZR010", "ZR030")}
        raw = c2_decide._category(st, "ZR010", "ZR030", ())
        cat = _CAT.get(raw, raw)
        af = b[f"{k}:AF"]["L"]
        rule6 = bool(c2_decide.sign(af, g[f"{k}:AF"]) == 1
                     and c2_decide.sign(b[f"{k}:ZR030"]["U"], g[f"{k}:ZR030"]) == -1)
        good = (cat, rule6) == _EXPECT[k]
        ok = ok and good
        res[k] = {"category": cat, "rule6": rule6, "expected_ok": good,
                  "bounds": {s: {"L": v["L"], "U": v["U"], "g": v["g"]} for s, v in st.items()}}
    res["ok"] = ok
    return res


# ------------------------------------------------------------------------- Decimal rows
def decimal_rows(T, E, pi, a1, a2, o1, o2, s1, pc, k=None) -> dict:
    k = uc.DECIMAL_ROWS if k is None else int(k)
    tol, rows, ok = uc.DEC_TOL, [], True
    for i in range(k):
        try:
            r1 = c1_oracle.decimal_reference(T, E, pi, a1[i])
            r2 = c1_oracle.decimal_reference(T, E, pi, a2[i])
            b4 = c1_oracle.decimal_posterior60(T, E, pi, a1[i, 28:32])
            q4d = c1_oracle.decimal_predictive(b4, T, E, 80)
            Gd = c1_oracle.decimal_G(r1["q32"], r2["q32"])
        except C1GateFailure:
            raise
        except Exception as exc:  # noqa: BLE001  Decimal flags and reference-input errors
            raise C1GateFailure(ORACLE, f"decimal row {i}: {exc!r}") from exc
        pairs = {"q32_a1": (o1["qbar"][i], r1["q32"]), "q32_a2": (o2["qbar"][i], r2["q32"]),
                 "q4": (s1["q4bar"][i], q4d), "G": ([pc["G"][i]], [Gd])}
        agree = {n: bool(c1_oracle.rel_agree(x, ref, tol)) for n, (x, ref) in pairs.items()}
        h3 = {n: c1_oracle.h3_compare(x, ref, True, 0) for n, (x, ref) in pairs.items()}
        ok = ok and all(agree.values())
        rows.append({"row": i, "agree": agree, "h3": h3})
    return {"rows": rows, "ok": ok}


# ------------------------------------------------------------------------- Lemma P, shares
def lemma_p_arrays(o1, o2, s1, pc) -> dict:
    u = []
    for o in (o1, o2):
        phi, _ = c2_oracle.phi_star(o["m32"])
        u.append(np.column_stack((np.cos(phi), np.sin(phi))))
    pairU = 0.5 * np.sum((u[0] - u[1]) * (o1["m32"] - o2["m32"]), axis=1)
    rowU = np.sum(u[0] * (o1["m32"] - s1["m4"]), axis=1)
    rowG = np.sum((o1["qbar"] - s1["q4bar"]) * o1["logq"], axis=1)
    return {"pairU": pairU, "rowU": rowU, "pairG": np.asarray(pc["G"]), "rowG": rowG}


def label_share(qbar1, qbar2):
    n = len(qbar1)
    m1 = np.asarray(qbar1).reshape(n, 6, 6).sum(axis=2)
    m2 = np.asarray(qbar2).reshape(n, 6, 6).sum(axis=2)
    return 0.5 * np.sum((m1 - m2) * (np.log(m1) - np.log(m2)), axis=1)


def problem_o(o_fit, w32_fit, K=None, euclidean=False) -> dict:
    K = uc.K_HARM if K is None else int(K)
    N = helmert(36)
    Y = o_fit["logq"] @ N
    mu, sd = c2_code.standardise(o_fit["nuis"])
    zt = (o_fit["nuis"] - mu) / sd
    f = c2_code.fstar(o_fit["m32"], K)[0]
    pr = c2_stats.f1_problem(Y, w32_fit, zt, f, euclidean=euclidean)
    return dict(pr, N=N, mu=mu, sd=sd, K=K, euclidean=bool(euclidean))


def share_arrays(pr, pc, o1, o2) -> dict:
    N = pr["N"]
    dy = (o1["logq"] - o2["logq"]) @ N
    part = c2_attrib.partition(pc["d"], N, dy, pr["g"]["P_S"], pr["g"]["P_G"])
    return dict(part, dy=dy)


def share_guard_beta(pr, pc, dy) -> float:
    return c2_decide.beta_A(pc["d"], pr["N"], dy, c2_stats.delta_p(pr["ref"], "S"), 1.0)
