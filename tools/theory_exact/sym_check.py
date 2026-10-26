"""Brute-force: which grid automorphisms g admit a symbol permutation s with E[g z, s w] = E[z, w]
and T[g i, g j] = T[i, j], for the O emission on square/cylinder (built from the formula in
RESEARCH_PLAN §3.3, not from project code). Also P-type per-axis shuffles."""
import itertools
import numpy as np

N = 12


def dist(x1, y1, x2, y2, periodic):
    dx = abs(x1 - x2)
    if periodic:
        dx = min(dx, N - dx)
    return np.hypot(dx, y1 - y2)


def emission(periodic, sigma):
    cen = [(0.5 + 2 * a, 0.5 + 2 * b) for a in range(6) for b in range(6)]
    E = np.zeros((N * N, 36))
    for x in range(N):
        for y in range(N):
            d = np.array([dist(x, y, cx, cy, periodic) for cx, cy in cen])
            w = np.exp(-d ** 2 / (2 * sigma ** 2))
            E[x * N + y] = w / w.sum()
    return E


def transition(periodic):
    T = np.zeros((N * N, N * N))
    for x in range(N):
        for y in range(N):
            i = x * N + y
            T[i, i] += 0.2
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if periodic:
                    nx %= N
                if 0 <= nx < N and 0 <= ny < N:
                    T[i, nx * N + ny] += 0.2
                else:
                    T[i, i] += 0.2
    return T


def grid_maps(periodic):
    maps = {}
    shifts = range(N) if periodic else [0]
    for s, fx, fy, tr in itertools.product(shifts, (0, 1), (0, 1), (0, 1)):
        if tr and periodic:
            continue
        perm = np.zeros(N * N, int)
        for x in range(N):
            for y in range(N):
                X, Y = (y, x) if tr else (x, y)
                X = (N - 1 - X) if fx else X
                Y = (N - 1 - Y) if fy else Y
                X = (X + s) % N
                perm[x * N + y] = X * N + Y
        maps[(s, fx, fy, tr)] = perm
    return maps


def symbol_perm(E, g):
    """s with E[g z, s(w)] == E[z, w] for all z, w, or None."""
    Eg = np.zeros_like(E)
    Eg[g] = E  # Eg[g z] = E[z]
    s = []
    for w in range(E.shape[1]):
        hits = [v for v in range(E.shape[1]) if np.allclose(Eg[:, v], E[:, w], atol=1e-12)]
        if len(hits) != 1:
            return None
        s.append(hits[0])
    return s if len(set(s)) == len(s) else None


rng = np.random.default_rng(0)
for periodic in (False, True):
    T = transition(periodic)
    for sigma in (0.75, 1.25, 2.0):
        for cond in ("O", "P"):
            E = emission(periodic, sigma)
            if cond == "P":
                sx, sy = rng.permutation(N), rng.permutation(N)
                idx = np.array([sx[x] * N + sy[y] for x in range(N) for y in range(N)])
                E = E[idx]
            found = []
            for key, g in grid_maps(periodic).items():
                if not np.allclose(T[np.ix_(g, g)], T):
                    continue
                if symbol_perm(E, g) is not None:
                    found.append(key)
            print("cyl" if periodic else "sq ", sigma, cond, len(found), sorted(found)[:14])
