"""Reviewer check of section 5.7: for all 8 hybrid cells, map-free ceilings Pi of belief and
prediction clouds, belief kappa (world x-phase), prediction kappa with the symbol-column map, and a
prediction map defined through the WORLD state (linear readout of the next-state x-phase from
sqrt(q), fitted on an independent training cloud)."""
import json
import sys

import numpy as np
from ripser import ripser

from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation
from topo_pilot.world import WorldConfig, build_world
from theory_exact import N, amp, build, certificate, filt, hellinger_matrix, sample


def kap(D, th):
    r, d, w = certificate(D, th)
    return (r / d if np.isfinite(d) else 0.0), w


def Pi(D):
    dg = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
    dg = dg[np.isfinite(dg[:, 1]) & (dg[:, 0] > 0)]
    return float((dg[:, 1] / dg[:, 0]).max())


def cell(world, chart, permuted, n, rng):
    T, _, _ = build(world, "O", 1.25)
    _, E, a_of_w = build(chart, "O", 1.25)
    if permuted:
        sx, sy = draw_axis_permutation(build_world(WorldConfig(family=world)))
        E = E[axis_state_perm(sx, sy, (N, N))]
        if world == chart:
            _, EP, aP = build(world, "P", 1.25)
            assert np.allclose(EP, E) and np.array_equal(aP, a_of_w)
    xs = (np.arange(N * N) // N).astype(float)
    clouds = []
    for _ in range(2):
        b = filt(T, E, sample(T, E, n, 32, rng))
        clouds.append((b, b @ T @ E, b @ T))
    (btr, qtr, ntr), (b, q, nxt) = clouds
    target = lambda m: (m * np.exp(2j * np.pi * xs / N)[None, :]).sum(1)
    F = lambda qq: np.c_[np.sqrt(qq), np.ones(len(qq))]
    coef, *_ = np.linalg.lstsq(F(qtr), target(ntr), rcond=None)
    Db, Dq = hellinger_matrix(b), hellinger_matrix(q)
    out = {"world": world, "chart": chart, "permuted": permuted}
    out["belief_kappa"], _ = kap(Db, amp(b, xs, N)[0])
    out["pred_kappa_symbolmap"], _ = kap(Dq, amp(q, a_of_w.astype(float), 6)[0])
    out["pred_kappa_worldmap"], _ = kap(Dq, np.angle(F(q) @ coef))
    out["pred_worldmap_fit_r2"] = float(1 - np.mean(np.abs(F(q) @ coef - target(nxt)) ** 2)
                                        / np.mean(np.abs(target(nxt) - target(nxt).mean()) ** 2))
    out["Pi_belief"], out["Pi_pred"] = Pi(Db), Pi(Dq)
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    rows = []
    for seed in (11, 12, 13):
        rng = np.random.default_rng(seed)
        for permuted in (False, True):
            for world in ("cylinder", "square"):
                for chart in ("cylinder", "square"):
                    r = cell(world, chart, permuted, n, rng)
                    r["seed"] = seed
                    rows.append(r)
                    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}),
                          flush=True)
    json.dump(rows, open(f"check_hybrids_n{n}.json", "w"), indent=1)
