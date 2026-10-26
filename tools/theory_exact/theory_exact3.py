"""Exact process-only computations, part 3.

E: searched null. How large can kappa get on the square-O belief cloud (no loop in the world) when
   the circle map is searched instead of fixed in advance? Three map families: angle around a point
   of the mean-position plane, angle of a pair of principal components, and a random linear map of
   sqrt(b) improved by hill climbing. The same search is run on the cylinder for comparison.
F: why the axis-permuted prediction cloud carries a certified loop. P keeps the emission chart and
   only scrambles which world cell uses which chart cell, so q = (bT) Pi E_O is a mixture of overlap
   bumps on the emission chart. Test with hybrids: world dynamics from one family, overlap emission
   (unpermuted) from the other.
G: Vietoris-Rips H1 barcodes (ripser) of the belief clouds: longest bars, square versus cylinder.
"""
import json
import sys
import time

import numpy as np
from ripser import ripser

from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation
from topo_pilot.world import WorldConfig, build_world
from theory_exact import N, TWO_PI, amp, build, certificate, filt, hellinger_matrix, sample


def kappa(D, th):
    r, d, _ = certificate(D, th)
    return r / d if np.isfinite(d) else 0.0


def searched_null(family, n, rng, n_points=25, n_pairs=10, n_random=30, n_climb=60):
    T, E, _ = build(family, "O", 1.25)
    b = filt(T, E, sample(T, E, n, 32, rng))
    D = hellinger_matrix(b)
    xs, ys = (np.arange(N * N) // N).astype(float), (np.arange(N * N) % N).astype(float)
    out = {"family": family, "n": n}
    th_fixed, _ = amp(b, xs, N)
    out["fixed_x_phase_kappa"] = kappa(D, th_fixed)
    # 1. angle around a point (cx, cy) of the mean-position plane (non-periodic means)
    mx, my = b @ xs, b @ ys
    best = 0.0
    for cx, cy in rng.uniform(1.0, N - 2.0, size=(n_points, 2)):
        best = max(best, kappa(D, np.arctan2(my - cy, mx - cx)))
    out["around_point_best"] = best
    # 2. angle of a pair of principal components of sqrt(b)
    R = np.sqrt(b)
    Rc = R - R.mean(0)
    _, _, Vt = np.linalg.svd(Rc, full_matrices=False)
    P = Rc @ Vt[:n_pairs].T
    best = 0.0
    for i in range(n_pairs):
        for j in range(i + 1, n_pairs):
            best = max(best, kappa(D, np.arctan2(P[:, j], P[:, i])))
    out["pc_pair_best"] = best
    # 3. random linear map of sqrt(b), then hill climbing on the best start
    starts = [rng.normal(size=(N * N, 2)) for _ in range(n_random)]
    vals = [kappa(D, np.arctan2(*(Rc @ A).T[::-1])) for A in starts]
    A, cur = starts[int(np.argmax(vals))], max(vals)
    out["random_map_median"] = float(np.median(vals))
    for _ in range(n_climb):
        A2 = A + 0.3 * rng.normal(size=A.shape)
        v = kappa(D, np.arctan2(*(Rc @ A2).T[::-1]))
        if v >= cur:
            A, cur = A2, v
    out["random_map_climbed_best"] = cur
    return out


def overlap_E(family, sigma=1.25):
    _, E, a_of_w = build(family, "O", sigma)
    return E, a_of_w


def prediction_certificates(n, rng):
    res = {}
    for world, chart in (("cylinder", "P"), ("square", "P")):
        T, E, a_of_w = build(world, "P", 1.25)
        b = filt(T, E, sample(T, E, n, 32, rng))
        q = b @ T @ E
        th, rho = amp(q, a_of_w.astype(float), 6)
        r, d, w = certificate(hellinger_matrix(q), th)
        res[f"{world}_world_axis_permuted"] = {"kappa": r / d if np.isfinite(d) else 0.0,
                                               "winding": w}
    for world, chart in (("square", "cylinder"), ("cylinder", "square"), ("cylinder", "cylinder"),
                         ("square", "square")):
        T, _, _ = build(world, "O", 1.25)
        E, a_of_w = overlap_E(chart)
        b = filt(T, E, sample(T, E, n, 32, rng))
        q = b @ T @ E
        th, _ = amp(q, a_of_w.astype(float), 6)
        r, d, w = certificate(hellinger_matrix(q), th)
        thb, _ = amp(b, (np.arange(N * N) // N).astype(float), N)
        rb, db, wb = certificate(hellinger_matrix(b), thb)
        res[f"{world}_world_{chart}_chart"] = {
            "prediction_kappa": r / d if np.isfinite(d) else 0.0, "prediction_winding": w,
            "belief_kappa": rb / db if np.isfinite(db) else 0.0, "belief_winding": wb}
    # axis-permuted with the other family's chart: which loop does P's prediction cloud carry?
    for world, chart in (("cylinder", "square"), ("square", "cylinder")):
        T, _, _ = build(world, "O", 1.25)
        E, a_of_w = overlap_E(chart)
        sx, sy = draw_axis_permutation(build_world(WorldConfig(family=world)))
        E = E[axis_state_perm(sx, sy, (N, N))]
        b = filt(T, E, sample(T, E, n, 32, rng))
        q = b @ T @ E
        th, _ = amp(q, a_of_w.astype(float), 6)
        r, d, w = certificate(hellinger_matrix(q), th)
        res[f"{world}_world_permuted_{chart}_chart"] = {
            "prediction_kappa": r / d if np.isfinite(d) else 0.0, "prediction_winding": w}
    return res


def barcodes(n, rng):
    res = {}
    for family, mode in (("cylinder", "O"), ("square", "O"), ("cylinder", "P"), ("square", "P")):
        T, E, a_of_w = build(family, mode, 1.25)
        b = filt(T, E, sample(T, E, n, 32, rng))
        for name, X in (("belief", b), ("prediction", b @ T @ E)):
            dg = ripser(hellinger_matrix(X), distance_matrix=True, maxdim=1)["dgms"][1]
            life = np.sort(dg[:, 1] - dg[:, 0])[::-1] if len(dg) else np.zeros(1)
            top = dg[np.argmax(dg[:, 1] - dg[:, 0])] if len(dg) else [0, 0]
            res[f"{family}_{mode}_{name}"] = {
                "longest": float(life[0]), "second": float(life[1]) if len(life) > 1 else 0.0,
                "longest_birth_death": [float(top[0]), float(top[1])],
                "ratio_death_birth": float(top[1] / top[0]) if top[0] > 0 else None,
                "n_bars": int(len(dg))}
    return res


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261028
    rng = np.random.default_rng(seed)
    out = {"n": n, "seed": seed}
    for key, fn in (("searched_null", lambda: [searched_null(f, n, rng) for f in ("square", "cylinder")]),
                    ("prediction_mechanism", lambda: prediction_certificates(n, rng)),
                    ("barcodes", lambda: barcodes(n, rng))):
        t0 = time.time()
        out[key] = fn()
        print(key, round(time.time() - t0, 1), "s", json.dumps(out[key]), flush=True)
    with open(f"theory_exact3_results_n{n}_s{seed}.json", "w") as fh:
        json.dump(out, fh, indent=1)
