"""X2a stage 0, part 3 (X2A-FROZEN-v1; API.md): PH route (K1 band, K2 C-world, K3 H0 height),
clouds and readings, PH controls, noise floor, outcome logic, S0 and run (report and NPZ)."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path[:0] = [p for p in (str(Path(__file__).resolve().parent),) if p not in sys.path]

import x2a_mc as xc  # noqa: E402
import x2a_model as xm  # noqa: E402
from scipy.sparse import coo_matrix  # noqa: E402
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree  # noqa: E402

from topo_pilot.contracts import SeedTree, Status  # noqa: E402
from topo_pilot.topology import (  # noqa: E402
    DistancePipeline,
    Euclidean,
    Hellinger,
    NullClouds,
    PersistenceComputer,
    PHConfig,
    Summaries,
)

GATES = ("PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5")
PLANNING = xm.REPO.parent / "agent-handoff" / "planning"
BOUND = {"protocol": ("responses/X2A-FROZEN-v1.md", xm.PROTOCOL_SHA256),
         "request": ("requests/coord-x2a-stage0-20261015.md", xm.REQUEST_SHA256)}
RHOS, PANELS, MIN_SIZE = (0.75, 1.0, 1.25), 8, 26

# ---- readings on diagrams (§7.2-§7.5) ----------------------------------------------------------
def _bars(rows, dim):
    rows = np.asarray(rows, dtype=np.float64).reshape(-1, 4)
    return rows[rows[:, 0] == dim]

def betti_at(rows, dim, r):
    b = _bars(rows, dim)
    return int(((b[:, 1] <= r) & (r < b[:, 2])).sum())

def _segments(rows, lo, hi):
    r = np.asarray(rows, dtype=np.float64).reshape(-1, 4)[:, 1:3].ravel()
    cuts = np.unique(np.concatenate([[lo, hi], r[np.isfinite(r) & (r > lo) & (r < hi)]]))
    return [(a, b) for a, b in zip(cuts[:-1], cuts[1:])
            if betti_at(rows, 0, (a + b) / 2) == 1 and betti_at(rows, 1, (a + b) / 2) == 2]

def _merge(S):
    out = []
    for a, b in sorted(S):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out

def band_select(diagrams, lo=0.0, hi=0.99, min_width=0.08):
    S = _merge(_segments(diagrams[0], lo, hi))
    for d in diagrams[1:]:
        S = _merge([(max(a1, a2), min(b1, b2)) for a1, b1 in S
                    for a2, b2 in _merge(_segments(d, lo, hi)) if max(a1, a2) < min(b1, b2)])
    if not S:
        return {"status": "CALIBRATION_INCONCLUSIVE", "interval": None, "band": None, "S": []}
    lo_, u = max(S, key=lambda iv: (iv[1] - iv[0], -iv[0]))
    ok = u - lo_ >= min_width
    return {"status": "OK" if ok else "CALIBRATION_INCONCLUSIVE", "interval": (lo_, u),
            "band": (lo_ + (u - lo_) / 4, u - (u - lo_) / 4) if ok else None,
            "S": [list(iv) for iv in S]}

def beta1_band(rows, band):
    b = _bars(rows, 1)
    return int(((b[:, 1] <= band[0]) & (b[:, 2] > band[1])).sum())

def k2_check(rows):
    b = _bars(rows, 1)
    n = int(((b[:, 2] - b[:, 1]) >= 1.0).sum())
    return {"n_bars": n, "ok": n == 2}

def clusters_at(D, h, dedup_map, min_size=MIN_SIZE):
    D = np.asarray(D, dtype=np.float64)
    n, lab = len(D), np.zeros(len(D), dtype=np.int64)
    if n > 1:  # exact zeros would read as missing edges in scipy's MST; keep them as edges
        W = np.where((D == 0) & ~np.eye(n, dtype=bool), np.finfo(float).tiny, D)
        t = minimum_spanning_tree(W).tocoo()
        k = t.data <= h
        _, lab = connected_components(coo_matrix((np.ones(k.sum()), (t.row[k], t.col[k])),
                                                 shape=(n, n)), directed=False)
    orig = lab[np.asarray(dedup_map, dtype=np.int64)]
    sizes = np.bincount(orig)
    keep = np.flatnonzero(sizes >= min_size)
    remap = np.full(len(sizes), -1, dtype=np.int64)
    remap[keep] = np.arange(len(keep))
    labels = remap[orig]
    return {"count": int(len(keep)), "labels": labels, "sizes": sizes[keep].tolist(),
            "retained_fraction": float((labels >= 0).mean())}

def split_check(labels, truth, purity=0.95):
    labels, truth = np.asarray(labels), np.asarray(truth)
    ids = [c for c in np.unique(labels) if c >= 0]
    if len(ids) != 2:
        return {"split": False, "purity": 0.0}
    maj, pur = [], []
    for c in ids:
        vals, cnt = np.unique(truth[labels == c], return_counts=True)
        maj.append(vals[cnt.argmax()])
        pur.append(cnt.max() / cnt.sum())
    p = float(min(pur))
    return {"split": bool(p >= purity and maj[0] != maj[1]), "purity": p}

def _h0_deaths(rows):
    d = _bars(rows, 0)[:, 2]
    return np.sort(d[np.isfinite(d)])[::-1]

def h0_star(xhalf_rows, x1_rows):
    vals = []
    for xh, x1 in zip(xhalf_rows, x1_rows):
        dh, d1 = _h0_deaths(xh), _h0_deaths(x1)
        vals.append(max(dh[0] if len(dh) else 0.0, d1[1] if len(d1) > 1 else 0.0))
    m = float(max(vals))
    return {"m": m, "ok": bool(1 - m > 0.05), "h0": (m + 1) / 2}

# ---- outcome logic (§5.9, §7.5, §7.6) ----------------------------------------------------------
def q1_outcome(n_a, n_b, n_pref, invalid=False):
    if invalid:
        return "INVALID"
    if n_a >= 7 and n_b >= 7:
        return "PASS" if n_pref < 7 else "NON_SPECIFIC"
    return "FAIL"

def q2_outcome(n_full_split, n_win_connected, n_win_split, invalid=False):
    if invalid:
        return "INVALID"
    if n_full_split < 7:
        return "NOT_SEPARATED"
    if n_win_connected >= 7:
        return "SEPARATED_FULL_ONLY"
    return "SEPARATED_BOTH" if n_win_split >= 7 else "WINDOW_UNRESOLVED"

def validity(statuses):
    for g in GATES:
        s = statuses.get(g, "NOT_RUN")
        if s != "PASS":
            return ("INVALID" if g in ("PF", "S0") or s in ("INVALID", "NOT_RUN") else "FAIL"), g
    return "PASS", None

def released(verdict, first_failed, labels):
    if verdict == "PASS":
        return dict(labels)
    return {k: "WITHHELD" if first_failed == "G5" else "NOT_RUN" for k in labels}

# ---- PH route (§7) -------------------------------------------------------------------------------
_PH = {d: PersistenceComputer(PHConfig(maxdim=d, coeff_p=2, threshold="auto")) for d in (0, 1)}

def _ph(X, maxdim, metric=None):
    dr = DistancePipeline(metric or Hellinger(), pca_dims=None).compute(
        np.asarray(X, dtype=np.float64), [str(i) for i in range(len(X))])
    res = _PH[maxdim].diagrams(dr.D)
    if res.status == Status.CENSORED:
        raise RuntimeError("CENSORED PH result (S8)")
    return dr, res.rows

def _cond(b, c):
    blk = b[:, xm.N:] if c else b[:, :xm.N]
    return blk / blk.sum(1, keepdims=True)

def _g0(rows):
    d = _h0_deaths(rows)
    return float(d[0] / d[1]) if len(d) > 1 and d[1] > 0 else None

def _item(fn, store, key):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001  (S8) the affected PH item is INVALID; continue
        store[key] = {"status": "INVALID", "error": repr(exc)}
        return None

def ph_route(spec, models, keepA, keepB, pref_B, ctl_b32, tree, H_t, diags):
    P, inval = {}, {"Q1": False, "Q2": False}
    k1 = _item(lambda: [_ph(np.exp(-spec.dist**2 / (2 * r**2)) / np.exp(-spec.dist**2 / (
        2 * r**2)).sum(1, keepdims=True), 1)[1] for r in RHOS], P, "K1")
    if k1 is not None:
        diags.update({f"K1_rho{r}": d for r, d in zip(RHOS, k1)})
        P["K1"] = band_select(k1)
    band = (P.get("K1") or {}).get("band")
    k2 = _item(lambda: _PH[1].diagrams(spec.dist).rows, P, "K2")
    if k2 is not None:
        diags["K2"], P["K2"] = k2, k2_check(k2)
    inval["Q1"] = band is None or not (P.get("K2") or {}).get("ok", False)
    ce = _item(lambda: _ph(models["main"]["E1"], 1), P, "C-emis")
    if ce is not None and band is not None:
        b1 = _bars(ce[1], 1)
        P["C-emis"] = {"beta1_band": beta1_band(ce[1], band), "n_bars_ge_0.25s": int(
            ((b1[:, 2] - b1[:, 1]) >= 0.25 * ce[0].scale_s).sum())}
    q1 = {"A": [], "B": [], "P-ref": []}
    for p in range(PANELS):
        sl = slice(512 * p, 512 * p + 512)
        for key, X in (("A", _cond(keepA["b32"][sl], 0)), ("B", _cond(keepB["b32"][sl], 1)),
                       ("P-ref", _cond(pref_B[sl], 1))):
            r = _item(lambda X=X: _ph(X, 1)[1], P, f"Q1_{key}_{p}")
            inval["Q1"] |= r is None
            if r is not None and band is not None:
                diags[f"Q1_{key}_{p}"] = r
                q1[key].append(beta1_band(r, band))
    n2 = {k: sum(v == 2 for v in q1[k]) for k in q1}
    P["Q1"] = {"beta1": q1, "panels_eq_2": n2,
               "outcome": q1_outcome(n2["A"], n2["B"], n2["P-ref"], inval["Q1"])}
    if band is not None:
        noise = []
        for c, b in (("A", _cond(keepA["b32"][:512], 0)), ("B", _cond(keepB["b32"][:512], 1))):
            for draw in range(20):
                Y = NullClouds.covariance_matched(np.sqrt(b) / np.sqrt(2),
                                                  tree.generator("x2a0_null", c, draw))
                r = _item(lambda Y=Y: _ph(Y, 1, Euclidean()), P, f"noise_{c}_{draw}")
                if r is not None:
                    noise.append({"c": c, "draw": draw, "beta1": beta1_band(r[1], band),
                                  "S": Summaries.S(r[1], 1, r[0].scale_s)})
        P["noise_floor"] = {"draws": noise, "any_beta1_2": any(x["beta1"] == 2 for x in noise)}
    q2 = _q2(keepA, keepB, ctl_b32, P, diags, H_t)
    P.update(q2)
    return P

def _q2(kA, kB, ctl, P, diags, H_t):
    rows = [slice(512 * p, 512 * p + 256) for p in range(PANELS)]
    truth = np.r_[np.zeros(256, int), np.ones(256, int)]
    cloud = (lambda key, p: np.vstack((kA[key][rows[p]], kB[key][rows[p]])))  # noqa: E731
    x1 = [np.vstack((np.hstack((_cond(kA["b32"][s], 0), 0 * kA["b32"][s][:, xm.N:])),
                     np.hstack((0 * kB["b32"][s][:, :xm.N], _cond(kB["b32"][s], 1)))))
          for s in rows]
    xh = [np.hstack((0.5 * _cond(c[:, :], 0), 0.5 * _cond(c[:, :], 1)))
          for c in (cloud("b32", p) for p in range(PANELS))]
    out, bad = {}, False
    try:
        d1 = [_ph(x, 0) for x in x1]
        dh = [_ph(x, 0) for x in xh]
        k3 = h0_star([r for _, r in dh], [r for _, r in d1])
    except Exception as exc:  # noqa: BLE001  (S8)
        return {"K3": {"status": "INVALID", "error": repr(exc)}, "Q2": {"outcome": "INVALID"}}
    out["K3"], h = k3, k3["h0"]
    bad |= not k3["ok"]

    def reading(X):
        dr, r = _ph(X, 0)
        cl = clusters_at(dr.D, h, dr.dedup_map)
        return {"beta0": cl["count"], "retained_fraction": cl["retained_fraction"],
                "status": dr.status.value, "g0": _g0(r), **split_check(cl["labels"], truth)}, r

    res = {}
    for key, gen in (("full", lambda p: cloud("b32", p)), ("win", lambda p: cloud("bw8", p)),
                     ("X1", lambda p: x1[p]), ("N-iso", lambda p: _ctl(ctl["N-iso"], p)),
                     ("N-id", lambda p: _ctl(ctl["N-id"], p))):
        res[key] = []
        for p in range(PANELS):
            try:
                rd, r = reading(gen(p))
                diags[f"Q2_{key}_{p}"] = r
                res[key].append(rd)
            except Exception as exc:  # noqa: BLE001  (S8) a required Q2 cloud raised
                res[key].append({"status": "INVALID", "error": repr(exc)})
                bad = True
    curve = {}
    for i, t in enumerate(xc.CURVE_T):
        curve[t] = [reading(np.vstack((kA["bcurve"][rows[p], i], kB["bcurve"][rows[p], i])))[0]
                    for p in range(PANELS)]
        curve[t] = {"panels": curve[t], "E_Hb": float(H_t[t - 1])}
    ok = (lambda rd, f: "beta0" in rd and f(rd))  # noqa: E731
    ctl_ok = {"N-iso": sum(ok(r, lambda r: r["beta0"] == 1) for r in res["N-iso"]) == 8,
              "N-id": sum(r.get("status") == Status.COLLAPSED.value for r in res["N-id"]) == 8,
              "X1": sum(ok(r, lambda r: r["beta0"] == 2 and r["purity"] == 1.0)
                        for r in res["X1"]) == 8}
    bad |= not all(ctl_ok.values())
    nfs = sum(ok(r, lambda r: r["split"]) for r in res["full"])
    nwc = sum(ok(r, lambda r: r["beta0"] == 1) for r in res["win"])
    nws = sum(ok(r, lambda r: r["split"]) for r in res["win"])
    out["Q2"] = {"panels": res, "controls_ok": ctl_ok, "curve": curve,
                 "counts": {"full_split": nfs, "win_connected": nwc, "win_split": nws},
                 "outcome": q2_outcome(nfs, nwc, nws, bad)}
    return out

def _ctl(pair, p):
    return np.vstack((pair[0][256 * p:256 * p + 256], pair[1][256 * p:256 * p + 256]))

# ---- S0 and run (§5.0, §5.1, §8.3) ---------------------------------------------------------------
def s0_check():
    h = {k: hashlib.sha256((PLANNING / f).read_bytes()).hexdigest().upper()
         for k, (f, _) in BOUND.items()}
    code, diff = xm._git("diff", xm.BASE_COMMIT, "HEAD", "--", "src", "tools/x4_oracle_profile",
                      "tests/oracle_profile")
    return {"protocol_sha256_ok": h["protocol"] == BOUND["protocol"][1],
            "request_sha256_ok": h["request"] == BOUND["request"][1],
            "kernel_diff_empty": code == 0 and diff == "", "head": xm._git("rev-parse", "HEAD")[1],
            "hashes": h}

def _stages(st, rep, data, tree):
    m = data["models"] = {v: xm.variant_model(v, data["spec"]) for v in xm.VARIANTS}
    mm = m["main"]
    yield "G0", lambda: xm.gate_G0(data["spec"], mm["T"])
    yield "G1", lambda: xm.gate_G1(m)
    yield "G2", lambda: xm.gate_G2(m)
    data["exact"] = rep["gates"]["G2"].pop("exact")
    data["tok"] = [xc.sample(mm["T"], mm[E], xc.MC_SIZES["main"], tree.generator("x2a0_mc",
                                                                                   "main", c))
                   for E, c in (("E1", "A"), ("E2", "B"))]
    yield "G3", lambda: xc.gate_G3(mm, *data["tok"])
    A, B = (xc.row_stats(mm, t, label=i, keep=4096) for i, t in enumerate(data["tok"]))
    data["keep"] = [{k: s.pop(k) for k in ("b32", "bw8", "bcurve")} for s in (A, B)]
    S = data["S"] = xc.summarise(A, B)
    del A, B
    yield "G4", lambda: xc.gate_G4(data["exact"], S)

def run(out_dir, preflight):
    out, t0 = Path(out_dir), time.process_time()
    out.mkdir(parents=True, exist_ok=True)
    st = dict.fromkeys(GATES, "NOT_RUN")
    rep = {"protocol": "X2A-FROZEN-v1", "protocol_sha256": xm.PROTOCOL_SHA256,
           "gates": {g: {"status": "NOT_RUN"} for g in GATES}, "preflight": dict(preflight)}
    st["PF"] = "PASS" if preflight and all(preflight.values()) else "FAIL"
    rep["gates"]["PF"]["status"], tree, data, diags = st["PF"], SeedTree(xm.MASTER_X2A0), {}, {}
    if st["PF"] == "PASS":
        s0 = s0_check()
        st["S0"] = "PASS" if all(s0[k] for k in s0 if k.endswith("_ok") or k.endswith(
            "empty")) else "FAIL"
        rep["gates"]["S0"] = {"status": st["S0"], **s0}
    reached_D = False
    if st["S0"] == "PASS":
        try:
            data["spec"] = xm.build_world()  # S2: builder/validation exception -> INVALID
            for g, fn in _stages(st, rep, data, tree):
                res = fn()
                rep["gates"][g], st[g] = res, res["status"]
                if st[g] != "PASS":
                    break
            reached_D = st["G4"] == "PASS"
        except Exception as exc:  # noqa: BLE001  inability to evaluate a gate -> INVALID
            g = next(g for g in GATES if st[g] == "NOT_RUN")
            st[g], rep["gates"][g] = "INVALID", {"status": "INVALID", "error": repr(exc)}
    if reached_D:
        m, S = data["models"], data["S"]
        D = xc.gate_D(S)  # values computed now, labels sealed until G5
        ctl = xc.control_tokens(m, tree)
        rep["descriptive"], bel = xc.descriptive_mc(m, ctl, data["exact"])
        ctl_b32 = {v: [xc.row_stats(m[v], t[:2048], keep=2048)["b32"] for t in ctl[v]]
                   for v in ("N-iso", "N-id")}
        H_t = xm.LN2 - S["I_t"]["est"]
        try:
            PH = ph_route(data["spec"], m, *data["keep"], bel["P-ref_B"], ctl_b32, tree, H_t,
                          diags)
        except Exception as exc:  # noqa: BLE001  (S8) PH failure affects only the PH outcome
            PH = {"status": "INVALID", "error": repr(exc), "Q1": {"outcome": "INVALID"},
                  "Q2": {"outcome": "INVALID"}}
        try:
            g5 = xc.gate_G5(m, data["exact"], ctl, data["tok"])
        except Exception as exc:  # noqa: BLE001
            g5 = {"status": "INVALID", "error": repr(exc)}
        rep["gates"]["G5"], st["G5"] = g5, g5["status"]
        rep["descriptive"]["long_horizon"] = xc.long_horizon(m["main"], tree)
        V32 = {k: S["V_t"][k][31] for k in ("est", "se", "L99", "U99")}
        V32["flag"] = ("INCENTIVE_ABOVE_0.01" if V32["L99"] >= 0.01 else "INCENTIVE_BELOW_0.01"
                       if V32["U99"] < 0.01 else "INCENTIVE_STRADDLES")
        rep.update(D_values=D, PH_values=PH, P5=V32, curves=S, exact=data["exact"])
    verdict, first = validity(st)
    lab = {"P3": None, "P4": None, "A3": None, "outcome": None, "Q1": None, "Q2": None}
    if reached_D:
        lab.update(D["labels"], outcome=D["outcome"], Q1=PH["Q1"]["outcome"],
                   Q2=PH["Q2"]["outcome"])
    rep.update(verdict=verdict, first_failed=first, released=released(verdict, first, lab))
    if reached_D and verdict != "PASS":  # sealed: values kept, labels withheld (§5.0)
        rep["D_values"] = {k: v for k, v in D.items() if k in ("values", "block_boundaries")}
        for q in ("Q1", "Q2"):
            PH.get(q, {}).pop("outcome", None)
    if "models" in data:
        m = data["models"]
        arrays = {"T": m["main"]["T"], "e": xm.field_e(), "E_A": m["main"]["E1"],
                  "E_B": m["main"]["E2"], "E_N": m["N-local"]["E2"], "E_P": m["P-ref"]["E2"]}
        np.savez(out / "model.npz", **arrays)
        rep["model_sha256"] = {k: hashlib.sha256(v.tobytes()).hexdigest()
                               for k, v in arrays.items()}
        h = SeedTree(0)
        rep["seeds"] = {"main_tree_master": xm.MASTER_X2A0, "main_tree_issued": dict(tree.issued),
                        "P-ref_helper": {"master": 0, "seed": h.seed("axis_permutation", xm.FAMILY),
                                         **{k: m["P-ref"][k] for k in ("sx", "sy", "state_perm")}}}
    np.savez(out / "ph_diagrams.npz", **diags)
    rep["cpu_s"] = time.process_time() - t0
    rep = xm._jsonable(rep)
    (out / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True), encoding="utf-8")
    return rep

if __name__ == "__main__":
    args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
    pre = json.loads(Path(args["--preflight"]).read_text(encoding="utf-8"))
    print(json.dumps(run(Path(args["--out"]), pre)["verdict"]))
