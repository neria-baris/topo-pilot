"""Ceiling on kappa for any circle map (Corollary 2.2 of THEORY_TRACK_HE.md).

A certificate (delta, r*) implies an H1 bar [b, d) with b <= delta and d >= r*, so for every map
kappa = r*/delta <= max over bars of d/b. This script computes that ceiling (the largest
multiplicative persistence) with ripser for the oracle belief clouds of cylinder-O and square-O at
several sample sizes and seeds, next to the fixed x-phase kappa.
"""
import json
import sys

import numpy as np
from ripser import ripser

from theory_exact import N, amp, build, certificate, filt, hellinger_matrix, sample


def ceiling(D):
    dg = ripser(D, distance_matrix=True, maxdim=1)["dgms"][1]
    dg = dg[np.isfinite(dg[:, 1]) & (dg[:, 0] > 0)]
    ratio = dg[:, 1] / dg[:, 0]
    k = int(np.argmax(ratio))
    return float(ratio[k]), [float(dg[k, 0]), float(dg[k, 1])]


if __name__ == "__main__":
    sizes = [int(s) for s in sys.argv[1].split(",")] if len(sys.argv) > 1 else [500, 1000, 2000]
    seeds = range(1, 4)
    rows = []
    for family in ("cylinder", "square"):
        T, E, _ = build(family, "O", 1.25)
        for n in sizes:
            for seed in seeds:
                rng = np.random.default_rng(1000 * seed + n)
                b = filt(T, E, sample(T, E, n, 32, rng))
                D = hellinger_matrix(b)
                th, _ = amp(b, (np.arange(N * N) // N).astype(float), N)
                r, d, _ = certificate(D, th)
                c, bar = ceiling(D)
                row = {"family": family, "n": n, "seed": seed,
                       "fixed_kappa": r / d if np.isfinite(d) else 0.0,
                       "ceiling": c, "ceiling_bar": bar}
                rows.append(row)
                print(json.dumps(row), flush=True)
    with open(f"kappa_ceiling_{'_'.join(map(str, sizes))}.json", "w") as fh:
        json.dump(rows, fh, indent=1)
