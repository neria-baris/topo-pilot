"""Reviewer check: kappa <= Pi on the SAME cloud for every searched map (with winding), F2 vs F3
ceilings, and attainability of Pi by a cocycle-derived (de Silva style) circular coordinate."""
import json
import sys

import numpy as np
from ripser import ripser
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr

from theory_exact import N, amp, build, certificate, filt, hellinger_matrix, sample


def bars(D, p):
    dg = ripser(D, distance_matrix=True, maxdim=1, coeff=p)["dgms"][1]
    n_inf = int((~np.isfinite(dg[:, 1])).sum())
    dg = dg[np.isfinite(dg[:, 1]) & (dg[:, 0] > 0)]
    r = dg[:, 1] / dg[:, 0]
    k = int(np.argmax(r))
    return float(r[k]), dg[k], n_inf


def cocycle_map(D, p=47, fracs=(0.3, 0.6, 0.9, 0.99)):
    res = ripser(D, distance_matrix=True, maxdim=1, coeff=p, do_cocycles=True)
    dg, cocs = res["dgms"][1], res["cocycles"][1]
    ok = np.isfinite(dg[:, 1]) & (dg[:, 0] > 0)
    ratio = np.where(ok, dg[:, 1] / np.where(dg[:, 0] > 0, dg[:, 0], 1), 0)
    k = int(np.argmax(ratio))
    b, d = dg[k]
    c = cocs[k]
    n = len(D)
    out = []
    for fr in fracs:
        r = b * (d / b) ** fr
        iu = np.triu_indices(n, 1)
        m = D[iu] < r
        I, J = iu[0][m], iu[1][m]
        val = {}
        for i, j, v in c:
            i, j, v = int(i), int(j), int(v)
            v = v if v <= p // 2 else v - p
            if i < j:
                val[(i, j)] = v
            else:
                val[(j, i)] = -v
        nvec = np.array([val.get((i, j), 0) for i, j in zip(I, J)], float)
        E = len(I)
        A = coo_matrix((np.r_[np.ones(E), -np.ones(E)], (np.r_[np.arange(E), np.arange(E)], np.r_[J, I])),
                       shape=(E, n)).tocsr()
        phi = lsqr(A, -nvec, atol=1e-10, btol=1e-10)[0]  # alpha = n + (phi_j - phi_i)
        th = 2 * np.pi * phi
        rs, de, w = certificate(D, th)
        out.append({"frac": fr, "kappa": rs / de if np.isfinite(de) else 0.0, "winding": w})
    return float(ratio[k]), out


def run(family, n, seed):
    T, E, _ = build(family, "O", 1.25)
    rng = np.random.default_rng(seed)
    b = filt(T, E, sample(T, E, n, 32, rng))
    D = hellinger_matrix(b)
    P2, bar2, inf2 = bars(D, 2)
    P3, bar3, inf3 = bars(D, 3)
    xs, ys = (np.arange(N * N) // N).astype(float), (np.arange(N * N) % N).astype(float)
    maps = []
    th, _ = amp(b, xs, N)
    maps.append(("fixed", th))
    mx, my = b @ xs, b @ ys
    for cx, cy in rng.uniform(1.0, N - 2.0, size=(25, 2)):
        maps.append(("point", np.arctan2(my - cy, mx - cx)))
    R = np.sqrt(b)
    Rc = R - R.mean(0)
    _, _, Vt = np.linalg.svd(Rc, full_matrices=False)
    Pc = Rc @ Vt[:10].T
    for i in range(10):
        for j in range(i + 1, 10):
            maps.append(("pc", np.arctan2(Pc[:, j], Pc[:, i])))
    worst = 0.0
    best = {}
    viol = []
    winds = set()
    for name, th in maps:
        rs, de, w = certificate(D, th)
        if not np.isfinite(de):
            continue
        k = rs / de
        winds.add(w)
        best[name] = max(best.get(name, 0), k)
        if w % 2 and k > P2 * (1 + 1e-6):
            viol.append((name, k, w))
        worst = max(worst, k / P2)
    Pc_ratio, coc = cocycle_map(D)
    return {"family": family, "n": n, "seed": seed, "Pi_F2": P2, "Pi_F3": P3, "bar_F2": bar2.tolist(),
            "inf_bars": [inf2, inf3], "best": best, "max_kappa_over_Pi": worst, "windings": sorted(winds),
            "violations": viol, "cocycle_Pi_F47": Pc_ratio, "cocycle_maps": coc}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    rows = []
    for family in ("square", "cylinder"):
        for s in (1, 2, 3):
            r = run(family, n, 1000 * s + n)
            rows.append(r)
            print(json.dumps(r, default=float), flush=True)
    json.dump(rows, open(f"check_ceiling_n{n}.json", "w"), indent=1, default=float)
