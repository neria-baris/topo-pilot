"""Synthetic cost probe for the all-row Decimal certificate (job 0016; no real data).

Times the UNCHANGED job-0014 reference (decimal_suffix_posterior, 60 digits) on a SYNTHETIC
dense-in-structure process of the real size (S = 144 lazy x-periodic lattice walk, V = 36,
softmax-like emissions built from integer geometry). It then projects the time to every released
cal/val history: 1024 unique canonical histories x (K1 + K4 + K32 = 37 steps), plus the
four-lowest checks. Writes OUT/cost_probe.json.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tests" / "oracle_profile"))

import error_bound  # noqa: E402

N_SIDE, V = 12, 36


def synthetic_process():
    coords = np.array([(x, y) for x in range(N_SIDE) for y in range(N_SIDE)], dtype=float)
    S = len(coords)
    T = np.zeros((S, S))
    index = {(int(x), int(y)): i for i, (x, y) in enumerate(coords)}
    for (x, y), i in index.items():
        for nx, ny in (((x + 1) % N_SIDE, y), ((x - 1) % N_SIDE, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) in index:
                T[i, index[(nx, ny)]] = 0.2
        T[i, i] = 1.0 - T[i].sum()
    grid = np.array([(0.5 + 2 * a, 0.5 + 2 * b) for a in range(6) for b in range(6)])
    dx = np.abs(coords[:, None, 0] - grid[None, :, 0])
    dx = np.minimum(dx, N_SIDE - dx)
    d2 = dx**2 + (coords[:, None, 1] - grid[None, :, 1]) ** 2
    logits = -d2 / (2 * 1.25**2)
    E = np.exp(logits - logits.max(axis=1, keepdims=True))
    E /= E.sum(axis=1, keepdims=True)
    return T, E, np.full(S, 1.0 / S), coords


def main() -> int:
    T, E, pi, coords = synthetic_process()
    tokens = ((np.arange(32) * 7 + 3) % V).astype(np.int64)[None, :]
    timings = {}
    for K in (1, 4, 32):
        start = time.process_time()
        error_bound.reference_moments(T, E, pi, coords, np.vstack([tokens] * 1), (K,), cache={})
        timings[K] = time.process_time() - start
    per_history = sum(timings.values())
    projected = 1024 * per_history + 3 * 2 * 4 * (timings[1] + timings[4] + timings[32])
    result = {
        "synthetic": True,
        "S": int(len(pi)),
        "V": V,
        "seconds_by_K": timings,
        "per_history_K1_K4_K32_s": per_history,
        "projected_all_row_reference_s": projected,
        "oracle_stage_ceiling_s": 400,
        "fits_with_margin": projected <= 0.6 * 400,
        "note": "single synthetic history per K; projection excludes process checks and I/O",
    }
    out = Path(
        json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))["resources"]["output_root"]
    )
    with (out / "cost_probe.json").open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
