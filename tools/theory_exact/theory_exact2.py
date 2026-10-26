"""Exact process-only computations, part 2.

C: isotypic (Fourier over the symbol column a) structure of the optimal centred log-prediction
   y* = C log q* in cylinder-O: variance per harmonic, effective rank per harmonic, and the share of
   the response to the symmetry shift a -> a+1 carried by each harmonic.
D: rank-2 certificate on a torus (formula-built, not in the project registry) versus cylinder and
   square: rank of the winding vectors of all short cycles under the x- and y-phase maps.
"""
import json

import numpy as np

from theory_exact import N, TWO_PI, build, filt, hellinger_matrix, sample


def isotypic(n, rng):
    T, E, _ = build("cylinder", "O", 1.25)
    W = sample(T, E, n, 32, rng)
    q = filt(T, E, W) @ T @ E
    y = np.log(q)
    y -= y.mean(1, keepdims=True)
    # reorder public symbols into a (6 x 6) grid (a, b) using the centre index j = a*6 + b
    from topo_pilot.contracts import SeedTree
    from topo_pilot.process import EmissionConfig, OverlapGaussian
    from topo_pilot.world import WorldConfig, build_world
    world = build_world(WorldConfig(family="cylinder"))
    spec = OverlapGaussian().build(world, EmissionConfig(mode="overlap", sigma=1.25), SeedTree(1729))
    perm = np.asarray(spec.symbol_perm)  # centre j -> public symbol
    Y = y[:, perm].reshape(n, 6, 6)  # [h, a, b]
    F = np.fft.fft(Y, axis=1)  # harmonic k over a
    Fc = F - F.mean(0, keepdims=True)
    out = {"n": n}
    total = (np.abs(Fc) ** 2).sum()
    for k in range(6):
        M = Fc[:, k, :]  # n x 6 (one complex coefficient per b)
        sv = np.linalg.svd(M, compute_uv=False)
        out[f"k{k}"] = {"var_share": float((np.abs(M) ** 2).sum() / total),
                        "top1_share_within": float(sv[0] ** 2 / (sv ** 2).sum())}
    # response to the shift a -> a+1: harmonic k is multiplied by exp(-2 pi i k / 6)
    resp = np.array([np.abs(np.exp(-1j * TWO_PI * k / 6) - 1) ** 2 * (np.abs(F[:, k, :]) ** 2).sum()
                     for k in range(6)])
    out["shift_response_share"] = {f"k{k}": float(resp[k] / resp.sum()) for k in range(6)}
    return out


def lattice(periodic_x, periodic_y, sigma=1.25):
    def ax(d, per):
        d = abs(d)
        return min(d, N - d) if per else d
    cen = [(0.5 + 2 * a, 0.5 + 2 * b) for a in range(6) for b in range(6)]
    E = np.zeros((N * N, 36))
    T = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            i = x * N + y
            d2 = np.array([ax(x - cx, periodic_x) ** 2 + ax(y - cy, periodic_y) ** 2 for cx, cy in cen])
            w = np.exp(-d2 / (2 * sigma ** 2))
            E[i] = w / w.sum()
            T[i, i] += 0.2
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if periodic_x:
                    nx %= N
                if periodic_y:
                    ny %= N
                if 0 <= nx < N and 0 <= ny < N:
                    T[i, nx * N + ny] += 0.2
                else:
                    T[i, i] += 0.2
    return T, E


def rank_certificate(D, thetas):
    """Largest rank of winding vectors over cycles of the graph {d < delta}, as delta grows to
    min r*; returns (r*_min, [(delta, rank)...])."""
    n = D.shape[0]
    iu = np.triu_indices(n, 1)
    d = D[iu]
    diffs = [np.angle(np.exp(1j * (th[iu[1]] - th[iu[0]]))) for th in thetas]
    r_star = min(float(d[np.abs(df) >= 2 * np.pi / 3 - 1e-9].min()) if (np.abs(df) >= 2 * np.pi / 3 - 1e-9).any()
                 else np.inf for df in diffs)
    keep = d < r_star
    order = np.argsort(d[keep], kind="stable")
    I, J, Dl = iu[0][keep][order], iu[1][keep][order], d[keep][order]
    Df = np.stack([df[keep][order] for df in diffs], 1)
    m = len(thetas)
    parent = np.arange(n)
    pot = np.zeros((n, m))

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        for y in reversed(path):
            if parent[y] != x:
                pot[y] += pot[parent[y]]
            parent[y] = x
        return x

    gaps, events = [], []
    for i, j, dl, df in zip(I, J, Dl, Df):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri
            pot[rj] = pot[i] + df - pot[j]
        else:
            g = np.round((pot[j] - pot[i] - df) / TWO_PI)
            if np.any(g != 0):
                rk = np.linalg.matrix_rank(np.array(gaps + [g]))
                if rk > (np.linalg.matrix_rank(np.array(gaps)) if gaps else 0):
                    gaps.append(g)
                    events.append((float(dl), int(rk), g.astype(int).tolist()))
                    if rk == m:
                        break
    return r_star, events


def topo(n, rng):
    res = {}
    for name, px, py in (("torus", True, True), ("cylinder", True, False), ("square", False, False)):
        T, E = lattice(px, py)
        W = sample(T, E, n, 32, rng)
        b = filt(T, E, W)
        xs, ys = np.arange(N * N) // N, np.arange(N * N) % N
        th = [np.angle((b * np.exp(1j * TWO_PI * c / N)).sum(1)) for c in (xs, ys)]
        r_star, ev = rank_certificate(hellinger_matrix(b), th)
        res[name] = {"r_star_min": r_star, "rank_events": ev}
    return res


if __name__ == "__main__":
    rng = np.random.default_rng(20261027)
    out = {"isotypic": isotypic(3000, rng), "topology_rank": topo(3000, rng)}
    print(json.dumps(out, indent=1))
    json.dump(out, open("theory_exact2_results.json", "w"), indent=1)
