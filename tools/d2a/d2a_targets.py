"""D-2a oracle targets, window baselines, band-edge beta and stage 0 (D2A-FROZEN-v1 §3, §5, §6;
tools/d2a/API.md §2.2). Existing kernels only: BayesFilter, FutureOperator, suffix_posterior."""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d2a_world as W  # noqa: E402
from d2a_world import d1  # noqa: E402
from oracle_profile import suffix_posterior  # noqa: E402

from topo_pilot.analysis import kl_rows  # noqa: E402
from topo_pilot.experiment.x4f_probe import nested_ridge  # noqa: E402
from topo_pilot.oracle import BayesFilter, FutureOperator  # noqa: E402

HALF, A, B = 0.5, W.A_, W.B_
Q1_DEC = np.array([0.2, 0.2, 0.6, 0.0, 0.0])
_K: dict = {}


def kernels(proc: str) -> dict:
    """Cached filters, future operators and 3-step observability blocks for a process."""
    if proc not in _K:
        p, w = W.process(proc), W.world_kernels(proc)
        fo = {"mix": FutureOperator(p["T"], p["E"]), "C": FutureOperator(w["T_C"], w["E"]),
              "M": FutureOperator(w["T_M"], w["E"])}
        _K[proc] = {"p": p, "fo": fo, "TE": p["T"] @ p["E"],
                    "filt": {"mix": BayesFilter(p["T"], p["E"], p["mu"]),
                             "C": BayesFilter(w["T_C"], w["E"], w["mu_C"]),
                             "M": BayesFilter(w["T_M"], w["E"], w["mu_M"])},
                    "O3": {k: f.observability_matrices(3)[2][30:155] for k, f in fo.items()}}
    return _K[proc]


def window_prior(t: int, m: int, proc: str = "CM") -> np.ndarray:
    p = kernels(proc)["p"]
    return p["mu"] @ np.linalg.matrix_power(p["T"], t - min(m, t))


def window_posterior(tokens, t: int, m: int, proc: str = "CM") -> np.ndarray:
    p = kernels(proc)["p"]
    return suffix_posterior(p["T"], p["E"], window_prior(t, m, proc),
                            np.asarray(tokens)[:, :t].astype(np.int64), min(m, t))


def _filtered(tok: np.ndarray, proc: str) -> dict:
    k = kernels(proc)["filt"]
    res = {f: k[f].run(tok) for f in ("mix", "C", "M")}
    return {"b": res["mix"].b, "q": res["mix"].q, "b_C": res["C"].b, "b_M": res["M"].b,
            "lev_C": -np.cumsum(res["C"].ce, axis=1), "lev_M": -np.cumsum(res["M"].ce, axis=1)}


def _quantities(F: dict, loc: np.ndarray, ts: np.ndarray, tok: np.ndarray, proc: str) -> dict:
    K, i = kernels(proc), ts - 1
    b, bC, bM = F["b"][loc, i], F["b_C"][loc, i], F["b_M"][loc, i]
    pi = b[:, 12:].sum(axis=1)
    out = {"pi": pi, "b_mix": b, "b_C": bC, "b_M": bM, "logev_C": F["lev_C"][loc, i],
           "logev_M": F["lev_M"][loc, i], "Q1_filter": F["q"][loc, ts]}
    for name, bel, fo in (("", b, "mix"), ("_C", bC, "C"), ("_M", bM, "M")):
        out["Q1" + name] = K["fo"][fo].F1(bel)
        out["J2" + name] = K["fo"][fo].F2(bel).reshape(len(loc), 25)
        out["J3" + name] = bel @ K["O3"][fo].T
    for key in ("Q1", "J2", "J3"):
        out[key + "_half"] = 0.5 * (out[key + "_C"] + out[key + "_M"])
    out["T2"] = (pi - HALF)[:, None] * (out["J2_M"] - out["J2_C"])
    out["T3"] = (pi - HALF)[:, None] * (out["J3_M"] - out["J3_C"])
    out["G2"] = 0.5 * np.abs(out["T2"]).sum(axis=1)
    for m in (1, 4, 8):
        post = np.empty((len(loc), 24))
        for t in np.unique(ts):
            sel = ts == t
            post[sel] = window_posterior(tok[loc[sel]], int(t), m, proc)
        out[f"pi{m}"] = post[:, 12:].sum(axis=1)
        if m == 8:
            out["Q1_w8"] = post @ K["TE"]
    return out


def oracle_rows(tokens, positions, proc: str = "CM") -> tuple[np.ndarray, dict]:
    """Oracle quantities at one position per row (``positions [R]``, 0 = no row), in row order."""
    tok, pos = np.asarray(tokens), np.asarray(positions, dtype=np.int64)
    rows = np.flatnonzero(pos > 0)
    parts: list[dict] = []
    for c0 in range(0, tok.shape[0], W.CHUNK):
        sel = rows[(rows >= c0) & (rows < c0 + W.CHUNK)]
        if sel.size == 0:
            continue
        chunk = tok[c0:c0 + W.CHUNK, :int(pos[sel].max())].astype(np.int64)
        F = _filtered(chunk, proc)
        parts.append(_quantities(F, sel - c0, pos[sel], chunk, proc))
    keys = parts[0].keys() if parts else []
    return rows, {k: np.concatenate([p[k] for p in parts]) for k in keys}


def oracle_at(tokens, t: int, proc: str = "CM") -> dict:
    tok = np.asarray(tokens)
    return oracle_rows(tok, np.full(tok.shape[0], t), proc)[1]


def beta(r, d) -> tuple[float | None, str]:
    r, d = np.asarray(r, float).ravel(), np.asarray(d, float).ravel()
    den = float(np.sum(d * d))
    if not (np.isfinite(den) and den > 0):
        return None, "UNDEFINED"
    val = float(np.sum(r * d)) / den
    return (val, "ok") if np.isfinite(val) else (None, "UNDEFINED")


def _ab(x) -> np.ndarray:
    return x[:, A] - x[:, B]


def band_edge_table(tokens, q_model=None) -> dict:
    """All (row, p), p = 1..32 with w_p in {σ0, σ2}: oracle d, window-8 r8 and model rm."""
    tok = np.asarray(tokens)
    keys = ("ep", "p", "d", "r8") + (() if q_model is None else ("rm",))  # rm only with q_model
    out = {k: [] for k in keys}
    for p in range(1, 33):
        pos = np.where(np.isin(tok[:, p - 1], (W.S0_, W.S2_)), p, 0)
        rows, q = oracle_rows(tok, pos)
        if rows.size == 0:
            continue
        half = _ab(q["Q1_half"])
        out["ep"].append(rows)
        out["p"].append(np.full(rows.size, p))
        out["d"].append(_ab(q["Q1"]) - half)
        out["r8"].append(_ab(q["Q1_w8"]) - half)
        if q_model is not None:
            out["rm"].append(_ab(np.asarray(q_model)[rows, p]) - half)
    return {k: np.concatenate(v) if v else np.zeros(0) for k, v in out.items()}


def _gate(checks: dict, values: dict) -> dict:
    return {"status": "PASS" if all(checks.values()) else "FAIL", "values": values,
            "checks": {k: bool(v) for k, v in checks.items()}}


def _f(x) -> np.ndarray:
    return np.array([float(v) for v in x])


def _tv(p, q) -> float:
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


def _q2d(J2) -> np.ndarray:
    return np.asarray(J2).reshape(-1, 5, 5).sum(axis=1)[0]


def g0_fix() -> dict:
    """D-2a float pipeline against d1_seam.exact_history at the named histories (§5.2)."""
    names = {"H_STAR": d1.H_STAR, "H_A": d1.H_A, "H_B": d1.H_B, "H_EDGE": d1.H_EDGE,
             "H_MAX": d1.H_MAX}
    fl, ex, err = {}, {}, {}
    for n, h in names.items():
        fl[n] = oracle_at(W.pad(h)[None], len(h))
        ex[n] = d1.exact_history(h)
        e, f = ex[n], fl[n]
        err[n] = {"beliefs_Q1_J2": max(
            max(float(np.abs(f[k][0] - _f(e[k])).max()) for k in ("b_C", "b_M", "Q1_C", "Q1_M",
                                                                 "Q1")),
            max(float(np.abs(f[k][0] - _f(sum(e[j], []))).max())
                for k, j in (("J2_C", "J_C"), ("J2_M", "J_M"), ("J2", "J")))),
            "pi": abs(float(f["pi"][0]) - float(e["pi"]))}
    s, a, b_, e_, m = (fl[k] for k in names)
    tvs = {"h_star_joint": _tv(s["J2_C"], s["J2_M"]),
           "h_star_distant": _tv(_q2d(s["J2_C"]), _q2d(s["J2_M"])),
           "pair_joint": _tv(a["J2"], b_["J2"]), "pair_distant": _tv(_q2d(a["J2"]), _q2d(b_["J2"])),
           "h_edge_Q1": _tv(e_["Q1_C"], e_["Q1_M"]), "h_max_joint": _tv(m["J2_C"], m["J2_M"]),
           "h_max_distant": _tv(_q2d(m["J2_C"]), _q2d(m["J2_M"]))}
    want = {"h_star_joint": 1 / 50, "h_star_distant": 1 / 50, "pair_joint": 1 / 100,
            "pair_distant": 1 / 100, "h_edge_Q1": 1 / 10, "h_max_joint": 3 / 200,
            "h_max_distant": 1 / 100}
    checks = {f"{n}_entries": v["beliefs_Q1_J2"] <= 1e-12 for n, v in err.items()}
    checks |= {f"{n}_pi": v["pi"] <= 1e-11 for n, v in err.items()}
    checks |= {f"tv_{k}": abs(tvs[k] - want[k]) <= 1e-12 for k in want}
    return _gate(checks, {"errors": err, "tv": tvs})


def _parity(tok: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per-position seam parity and 'informed' flag (d1_seam.parity_profile, vectorised)."""
    cross = np.zeros(tok.shape, dtype=bool)
    cross[:, 1:] = ((tok[:, 1:] == W.S3_) & (tok[:, :-1] == W.S0_)) | (
        (tok[:, 1:] == W.S0_) & (tok[:, :-1] == W.S3_))
    par = np.cumsum(cross, axis=1) % 2
    informed = np.cumsum(np.isin(tok, (A, B)) & (par == 1), axis=1) > 0
    return par, informed


def _delta(b12: np.ndarray) -> np.ndarray:
    return b12[:, 0::3].sum(axis=1) - b12[:, 2::3].sum(axis=1)


def g0_num(tok0, tok0N) -> dict:
    """Numerical identities on stage0 (decision and band-edge t <= 32) and stage0N (§5.2)."""
    tok0, tok0N = np.asarray(tok0), np.asarray(tok0N)
    mx = {k: 0.0 for k in ("thmA", "band_edge", "mixture_b", "mixture_pi", "row_sums",
                           "J3_marginal", "T_identity", "support", "Q1_filter",
                           "uninformed_pi", "null_pi", "null_tv")}
    _, informed = _parity(tok0[:, :32])
    a_, inc = float(d1.a), {"V1": [], "V2": [], "V3": []}
    for t in range(1, 33):
        cls = tok0[:, t - 1]
        rows, q = oracle_rows(tok0, np.full(tok0.shape[0], t))
        dec, edge = cls[rows] == W.S3_, np.isin(cls[rows], (W.S0_, W.S2_))
        kl = {k: kl_rows(q[k], q[k + "_half"])[0] for k in ("Q1", "J2", "J3")}
        inc["V1"].append(float(np.mean(kl["Q1"])))
        inc["V2"].append(float(np.mean(np.where(dec, kl["J2"], 0.0))) if t <= 31 else 0.0)
        inc["V3"].append(float(np.mean(np.where(dec, kl["J3"], 0.0))) if t <= 30 else 0.0)
        if not (dec | edge).any():
            continue
        pi = q["pi"]
        if dec.any():
            mx["thmA"] = max(mx["thmA"], float(np.abs(q["Q1"][dec] - Q1_DEC).max()))
            off2 = np.delete(np.arange(25), W.S2)
            off3 = np.delete(np.arange(125), W.S3)
            mx["support"] = max(mx["support"], float(np.abs(q["T2"][dec][:, off2]).max()),
                                float(np.abs(q["T3"][dec][:, off3]).max()))
        if edge.any():
            lhs = q["Q1"][edge, A] - q["Q1_half"][edge, A]
            rhs = a_ / 4 * (pi[edge] - HALF) * (_delta(q["b_M"][edge]) - _delta(q["b_C"][edge]))
            mx["band_edge"] = max(mx["band_edge"], float(np.abs(lhs - rhs).max()))
        q = {k: v[dec | edge] for k, v in q.items()}
        rows, pi, dec, edge = rows[dec | edge], pi[dec | edge], dec[dec | edge], edge[dec | edge]
        mixb = np.hstack([(1 - pi)[:, None] * q["b_C"], pi[:, None] * q["b_M"]])
        expit = 1.0 / (1.0 + np.exp(-(q["logev_M"] - q["logev_C"])))
        sums = [np.abs(q[k].sum(axis=1) - 1).max() for k in ("J2", "J3", "J2_C", "J3_C", "J2_M",
                                                               "J3_M")]
        terms = [(q["T2"], q["J2"] - q["J2_half"]), (q["T3"], q["J3"] - q["J3_half"])]
        for key, val in (("mixture_b", np.abs(q["b_mix"] - mixb).max()),
                         ("mixture_pi", np.abs(pi - expit).max()), ("row_sums", max(sums)),
                         ("J3_marginal", np.abs(q["J3"].reshape(-1, 25, 5).sum(2) - q["J2"]).max()),
                         ("T_identity", max(float(np.abs(x - y).max()) for x, y in terms)),
                         ("Q1_filter", np.abs(q["Q1"] - q["Q1_filter"]).max())):
            mx[key] = max(mx[key], float(val))
        unin = ~informed[rows, t - 1]
        if unin.any():
            mx["uninformed_pi"] = max(mx["uninformed_pi"], float(np.abs(pi[unin] - HALF).max()))
        _, n = oracle_rows(tok0N, np.full(tok0N.shape[0], t), "CC")
        mx["null_pi"] = max(mx["null_pi"], float(np.abs(n["pi"] - HALF).max()))
        mx["null_tv"] = max(mx["null_tv"], float(0.5 * np.abs(n["Q1_C"] - n["Q1_M"]).sum(1).max()),
                            float(0.5 * np.abs(n["J2_C"] - n["J2_M"]).sum(1).max()))
    prior = max(abs(float(window_prior(t, m).sum()) - 1) for t in range(1, 33) for m in (1, 4, 8))
    rows16 = W.decision_rows(tok0, 16)
    whole = window_posterior(tok0[rows16], 16, 16)[:, 12:].sum(1)
    cross = float(np.abs(whole - oracle_at(tok0[rows16], 16)["pi"]).max())
    tol = {"thmA": 1e-12, "band_edge": 1e-12, "mixture_b": 1e-12, "mixture_pi": 1e-10,
           "row_sums": 1e-12, "J3_marginal": 1e-12, "T_identity": 1e-12, "support": 1e-12,
           "Q1_filter": 1e-12, "uninformed_pi": 1e-11, "null_pi": 1e-11, "null_tv": 1e-12}
    checks = {k: mx[k] <= tol[k] for k in tol}
    checks |= {"window_prior_sums": prior <= 1e-12, "window_whole_history": cross <= 1e-11}
    incentive = {k: {"per_t": v, "total": float(sum(v)),
                     "per_bin": {b: float(sum(v[lo - 1:hi])) for b, lo, hi in W.BINS}}
                 for k, v in inc.items()}
    return _gate(checks, dict(mx, window_prior_sums=prior, window_whole_history=cross,
                              incentive=incentive))


def g0_tpl() -> dict:
    """Exact (Fractions) checks of the canonical pair and every registered template (§5.2)."""
    y_law = [Fr(0)] * 9 + [Fr(2, 3), Fr(1, 3), Fr(0)]
    d30 = [Fr(int(s == 9)) for s in range(12)]
    q1 = [Fr(1, 5), Fr(1, 5), Fr(3, 5), Fr(0), Fr(0)]
    fails, n = [], 0
    pairs = [(11, d1.H_A, d1.H_B)] + [(t, a_, b_) for t in (16, 28)
                                       for a_, b_ in W.registered_templates(t)]
    for t, ha, hb in pairs:
        n += 1
        try:
            ea, eb = d1.exact_history(ha), d1.exact_history(hb)
        except ValueError:
            fails.append([t, "unreachable"])
            continue
        want_b, want_tv = (d30, Fr(1, 100)) if t == 11 else (y_law, Fr(1, 150))
        ok = {"reachable": ea["P"] > 0 and eb["P"] > 0,
              "pi": (ea["pi"], eb["pi"]) == (Fr(1, 4), Fr(3, 4)),
              "beliefs": all(e["b_C"] == e["b_M"] == want_b for e in (ea, eb)),
              "Q1": ea["Q1"] == eb["Q1"] == q1,
              "tv_joint": d1.tv(ea["J"], eb["J"]) == want_tv,
              "tv_distant": d1.tv(ea["Q2dist"], eb["Q2dist"]) == want_tv,
              "window": t == 11 or tuple(ha[-8:]) == tuple(hb[-8:])}
        fails += [[t, k] for k, v in ok.items() if not v]
    return _gate({"all_pairs": not fails}, {"pairs_checked": n, "failures": fails[:50],
                                            "hashes": {t: W.template_hashes(t) for t in (16, 28)}})


def _split(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    i = np.arange(n)
    return i % 4 != 3, i % 4 == 3, 1 + i % 6


def g0_pos(tok0) -> dict:
    tok0, vals = np.asarray(tok0), {}
    for t in W.POSITIONS:
        rows = W.decision_rows(tok0, t)
        q = oracle_at(tok0[rows], t)
        fit, held, panel = _split(tok0.shape[0])
        f, h = fit[rows], held[rows]
        res = nested_ridge(q["b_mix"][f], q["pi"][f], panel[rows][f], q["b_mix"][h], q["pi"][h])
        vals[t] = {"r2": res.r2, "status": res.r2_status, "lam": res.lam}
    return _gate({f"t{t}": v["r2"] is not None and v["r2"] >= 0.99 for t, v in vals.items()},
                 vals)


def g0_feas(tok0) -> dict:
    tok0, vals, checks = np.asarray(tok0), {}, {}
    be = band_edge_table(tok0)
    b8, st = beta(be["r8"], be["d"])
    for t in W.POSITIONS:
        rows = W.decision_rows(tok0, t)
        q = oracle_at(tok0[rows], t)
        pi, var = q["pi"], float(np.var(q["pi"]))
        v8 = float(np.mean((pi - q["pi8"]) ** 2))
        ratio = v8 / var if var > 0 else None
        v = {"rows": int(rows.size), "var_pi": var, "hi": int(np.sum(pi - HALF >= 0.05)),
             "lo": int(np.sum(HALF - pi >= 0.05)), "V8": v8, "V8_ratio": ratio,
             "G2_rows": int(np.sum(q["G2"] >= 1e-4)), "beta1_w8": b8, "beta1_w8_status": st}
        vals[t] = v
        checks |= {f"t{t}_coverage": v["rows"] >= 8192, f"t{t}_variation": var >= 1e-4,
                   f"t{t}_spread": v["hi"] >= 256 and v["lo"] >= 256,
                   f"t{t}_headroom": v8 >= 1e-4 and ratio is not None and ratio >= 0.20,
                   f"t{t}_sensitivity": v["G2_rows"] >= 256,
                   f"t{t}_band_edge_headroom": b8 is not None and b8 <= 0.80}
    return _gate(checks, vals)


def reported(tok0, zN_rate: float) -> dict:
    """§5.2 'reported, not gated' quantities (descriptive)."""
    tok0, out = np.asarray(tok0), {}
    _, informed = _parity(tok0[:, :32])
    bins = W.bin_positions(tok0, "stage0")
    for t in W.POSITIONS:
        rows = W.decision_rows(tok0, t)
        q = oracle_at(tok0[rows], t)
        pi, var = q["pi"], float(np.var(q["pi"]))
        kl = {k: kl_rows(q[k], q[k + "_half"])[0] for k in ("Q1", "J2", "J3")}
        out[t] = {"hist": np.histogram(pi, bins=20, range=(0, 1))[0].tolist(),
                  "frac_05": float(np.mean(np.abs(pi - HALF) >= 0.05)),
                  "frac_15": float(np.mean(np.abs(pi - HALF) >= 0.15)),
                  "E_max": float(np.mean(np.maximum(pi, 1 - pi))),
                  "mean_pi_minus_half": float(np.mean(pi - HALF)), "var_pi": var,
                  "V_m": {m: float(np.mean((pi - q[f"pi{m}"]) ** 2)) for m in (1, 4, 8)},
                  "informed_frac": float(np.mean(informed[rows, t - 1])),
                  "incentive_mean_kl": {k: None if v is None else float(np.mean(v))
                                        for k, v in kl.items()}}
        out[t]["R2_window"] = {m: (1 - v / var) if var > 0 else None
                               for m, v in out[t]["V_m"].items()}
        fit, held, panel = _split(tok0.shape[0])
        f, h = fit[rows], held[rows]
        for name, X in (("full_belief", q["b_mix"]), ("world_conditional",
                        np.hstack([q["b_C"], q["b_M"]])), ("J2_to_pi", q["J2"])):
            r = nested_ridge(X[f], pi[f], panel[rows][f], X[h], pi[h])
            out[t][f"ceiling_{name}"] = r.r2
    out["bin_rows"] = {b: int((bins[b - 1] > 0).sum()) for b, _, _ in W.BINS}
    out["stage0N_block_tag_rate"] = zN_rate
    return out


def stage0(store_root=W.STORE) -> str:
    """CLI ``stage0``: S0, pools, gates in §10.6 order, STAGE0.json; returns the outcome."""
    root = Path(store_root)
    s0 = W.s0_bindings(root)
    (root / "S0_stage0.json").write_text(json.dumps(s0, indent=1, default=str), "utf-8")
    rec: dict = {"S0": s0, "gates": {}}
    if s0["status"] != "PASS":
        rec["outcome"] = "INVALID"
    else:
        pools = W.save_pools(root)
        tok0, tok0N = W.load_tokens("stage0", root), W.load_tokens("stage0N", root)
        for name, fn in (("G0-FIX", g0_fix), ("G0-NUM", lambda: g0_num(tok0, tok0N)),
                         ("G0-TPL", g0_tpl), ("G0-POS", lambda: g0_pos(tok0))):
            rec["gates"][name] = fn()
            if rec["gates"][name]["status"] != "PASS":
                rec["outcome"] = "CONSTRUCTION_FAIL"
                break
        else:
            rec["gates"]["G0-FEAS"] = g0_feas(tok0)
            rec["outcome"] = "GO" if rec["gates"]["G0-FEAS"]["status"] == "PASS" \
                else "FEASIBILITY_NO_GO"
        rec["reported"] = reported(tok0, float(np.mean(W.load_private("stage0N", root)[1])))
        rec["test_coverage"] = {p: pools[p]["coverage"] for p in W.GUARDED}
        rec["template_hashes"] = {t: W.template_hashes(t) for t in (16, 28)}
    (root / "stage0").mkdir(exist_ok=True)
    with (root / "stage0" / "STAGE0.json").open("x", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, default=str)
    return rec["outcome"]
