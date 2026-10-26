"""Exact process-only computations for THEORY_TRACK_HE.md (owner go-ahead 2026-10-26).

A: symmetry group of the project's own T and E (square/cylinder x O/P, sigma candidates).
B: certified-loop numbers (Theorem 2.1) for oracle belief / prediction / window-k belief clouds.
No models, no project data: matrices are rebuilt with the project's builders; histories are
sampled here from those matrices with a fixed seed.
"""
import itertools
import json
import sys
import time

import numpy as np

from topo_pilot.contracts import SeedTree
from topo_pilot.process import AxisPermuted, EmissionConfig, OverlapGaussian, TransitionBuilder, TransitionConfig
from topo_pilot.world import WorldConfig, build_world

N = 12
TWO_PI = 2 * np.pi


def build(family, mode, sigma):
    world = build_world(WorldConfig(family=family))
    T = np.asarray(TransitionBuilder().build(world, TransitionConfig()).T, dtype=float)
    model = OverlapGaussian() if mode == "O" else AxisPermuted()
    spec = model.build(world, EmissionConfig(mode=model.mode, sigma=sigma), SeedTree(1729))
    E = np.asarray(spec.E, dtype=float)
    inv = np.argsort(np.asarray(spec.symbol_perm))  # public symbol w -> centre index j
    a_of_w = inv // 6
    return T, E, a_of_w


def grid_maps(periodic):
    shifts = range(N) if periodic else [0]
    for s, fx, fy, tr in itertools.product(shifts, (0, 1), (0, 1), (0, 1)):
        perm = np.zeros(N * N, int)
        for x in range(N):
            for y in range(N):
                X, Y = (y, x) if tr else (x, y)
                X = (N - 1 - X) if fx else X
                Y = (N - 1 - Y) if fy else Y
                perm[x * N + y] = ((X + s) % N) * N + Y
        yield (s, fx, fy, tr), perm


def symmetry_group(T, E, periodic):
    found = []
    for key, g in grid_maps(periodic):
        if not np.allclose(T[np.ix_(g, g)], T, atol=1e-14):
            continue
        Eg = np.empty_like(E)
        Eg[g] = E
        s = []
        for w in range(E.shape[1]):
            hits = np.where(np.all(np.isclose(Eg, E[:, [w]], rtol=0, atol=1e-13), axis=0))[0]
            if len(hits) != 1:
                break
            s.append(int(hits[0]))
        if len(s) == E.shape[1] and len(set(s)) == len(s):
            found.append(key)
    return found


def sample(T, E, n, L, rng):
    cumT, cumE = np.cumsum(T, 1), np.cumsum(E, 1)
    z = rng.integers(0, N * N, n)
    W = np.empty((n, L), int)
    for t in range(L):
        W[:, t] = (cumE[z] < rng.random((n, 1))).sum(1)
        z = (cumT[z] < rng.random((n, 1))).sum(1)
    return W


def filt(T, E, W):
    a = np.full((W.shape[0], N * N), 1.0 / (N * N))
    for t in range(W.shape[1]):
        b = a * E[:, W[:, t]].T
        b /= b.sum(1, keepdims=True)
        a = b @ T
    return b


def hellinger_matrix(P):
    R = np.sqrt(P)
    G = R @ R.T
    return np.sqrt(np.clip(1.0 - G, 0, None))  # = ||sqrt p - sqrt q|| / sqrt 2


def certificate(D, theta):
    """Theorem 2.1: r* and the smallest delta < r* that closes a nonzero-winding chain."""
    n = len(theta)
    iu = np.triu_indices(n, 1)
    d = D[iu]
    diff = np.angle(np.exp(1j * (theta[iu[1]] - theta[iu[0]])))  # signed, in (-pi, pi]
    far = np.abs(diff) >= 2 * np.pi / 3 - 1e-9  # conservative jump test (Thm 2.1, rule 3)
    r_star = float(d[far].min()) if far.any() else float("inf")
    keep = d < r_star
    order = np.argsort(d[keep], kind="stable")
    I, J, Dl, Df = iu[0][keep][order], iu[1][keep][order], d[keep][order], diff[keep][order]
    parent = np.arange(n)
    pot = np.zeros(n)  # lifted phase of node relative to its root

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        acc = 0.0
        for y in reversed(path):  # compress, accumulating potentials toward the root
            acc_y = pot[y] + (pot[parent[y]] if parent[y] != root else 0.0)
            pot[y] = acc_y
            parent[y] = root
        return root

    for i, j, dl, df in zip(I, J, Dl, Df):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri
            pot[rj] = pot[i] + df - pot[j]
        else:
            gap = pot[j] - pot[i] - df
            if abs(gap) > 1.0:  # a nonzero multiple of 2*pi
                return r_star, float(dl), int(round(-gap / TWO_PI))
    return r_star, float("inf"), 0


def amp(P, coord, period):
    zc = (P * np.exp(1j * TWO_PI * coord / period)[None, :]).sum(1)
    return np.angle(zc), np.abs(zc)


def run(family, mode, sigma, n, rng, ks=(1, 2, 4, 8, 16, 32)):
    T, E, a_of_w = build(family, mode, sigma)
    out = {"family": family, "mode": mode, "sigma": sigma, "n": n}
    out["group"] = len(symmetry_group(T, E, family == "cylinder"))
    W = sample(T, E, n, 32, rng)
    x_of_z = np.arange(N * N) // N
    full = None
    for k in sorted(ks, reverse=True):
        b = filt(T, E, W[:, -k:])
        if k == 32:
            full = b
        th, rho = amp(b, x_of_z, N)
        r_star, delta, wind = certificate(hellinger_matrix(b), th)
        row = {"r_star": r_star, "delta": delta, "kappa": r_star / delta, "winding": wind,
               "rho_min": float(rho.min()), "rho_med": float(np.median(rho))}
        if full is not None and k < 32:
            th_full, _ = amp(full, x_of_z, N)
            row["phase_agree_with_full"] = float(np.abs(np.mean(np.exp(1j * (th - th_full)))))
        out[f"belief_k{k}"] = row
        if k == 32:
            q = b @ T @ E
            thq, rq = amp(q, a_of_w.astype(float), 6)
            r2, d2, w2 = certificate(hellinger_matrix(q), thq)
            out["prediction"] = {"r_star": r2, "delta": d2, "kappa": r2 / d2, "winding": w2,
                                 "rho_min": float(rq.min()), "rho_med": float(np.median(rq))}
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    rng = np.random.default_rng(20261026)
    results = []
    for family, mode, sigma in [("cylinder", "O", 1.25), ("square", "O", 1.25), ("cylinder", "P", 1.25),
                                ("cylinder", "O", 0.75), ("cylinder", "O", 2.0)]:
        t0 = time.time()
        r = run(family, mode, sigma, n, rng)
        r["seconds"] = round(time.time() - t0, 1)
        results.append(r)
        print(json.dumps(r), flush=True)
    with open("theory_exact_results.json", "w") as fh:
        json.dump(results, fh, indent=1)
