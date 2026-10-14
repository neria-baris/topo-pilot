"""Bounded independent audit of exported job-0014 statistics (post-terminal; read-only inputs).

Recomputes, from the exported per-row NPZ only (no posterior recomputation, no sampling of
histories, no change to existing outputs): B_K/V_K point estimates, the full 5000-draw bootstrap
from the recorded SeedTree streams, all interval endpoints, split differences, and the exported
NPZ hashes; compares with PROFILE_TABLE/SPLIT_DIFFERENCE/bootstrap_draws. Optionally
(--reference-rows N) re-runs the independent Decimal reference on the first N fixed reference
rows per split and K. Writes a new audit/AUDIT_<utc>.json only.

Interface (Codex, after job 0014 is terminal; RUN.lock released by the worker):
  1. create OUT/RUN.lock exclusively with {"session": "<codex session id>", ...};
  2. base-python meter.py --mode audit --lock-owner <codex session id> --label audit-<n>
       -- <venv python> tools/x4_oracle_profile/audit.py [--reference-rows N]
     (PYTHONPATH = research src; thread variables are set by the meter; SAME ledger);
  3. delete RUN.lock. The meter enforces lock ownership, STOP/invalid-control/hold checks.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tests" / "oracle_profile"))
import inputs  # noqa: E402
import oracle_profile as op  # noqa: E402

CFG = inputs.load_config()
OUT = Path(CFG["output_root"])
PDIR = OUT / "profile"


def compare(a: float, b: float) -> float:
    return abs(float(a) - float(b))


def main() -> int:
    from topo_pilot.contracts import SeedTree

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reference-rows", type=int, default=0)
    args = parser.parse_args()
    manifest = json.loads((PDIR / "MANIFEST.json").read_text(encoding="utf-8"))
    hashes = {
        name: inputs.sha256(
            PDIR / f"{'rows_' + name if name != 'bootstrap' else 'bootstrap_draws'}.npz"
        )
        for name in manifest["npz_sha256"]
    }
    table = {
        (r["split"], r["K"], r["stat"]): r
        for r in json.loads((PDIR / "PROFILE_TABLE.json").read_text(encoding="utf-8"))
    }
    diffs = {
        (r["K"], r["stat"]): r
        for r in json.loads((PDIR / "SPLIT_DIFFERENCE.json").read_text(encoding="utf-8"))
    }
    with np.load(PDIR / "bootstrap_draws.npz", allow_pickle=False) as z:
        stored = {k: z[k] for k in z.files}
    bc, grid, worst, boots = CFG["bootstrap"], CFG["K_grid"], 0.0, {}
    for split in CFG["splits"]:
        with np.load(PDIR / f"rows_{split}.npz", allow_pickle=False) as z:
            rows = {k: z[k] for k in z.files}
        norm = {K: rows[f"norm{K}"] for K in grid}
        sq = {K: rows[f"sq{K}"] for K in grid}
        recomputed = op.residual_rows({K: rows[f"m{K}"] for K in grid}, CFG["full_K"])
        worst = max(
            [worst]
            + [
                float(np.max(np.abs(recomputed[s][K] - x[K])))
                for s, x in (("norm", norm), ("sq", sq))
                for K in grid
            ]
        )
        point = op.profile_point(norm, sq)
        rng = SeedTree(bc["seedtree_master"]).generator(bc["stream"], "bootstrap", split)
        boots[split] = op.bootstrap_profile(norm, sq, grid, rng, bc["draws"])
        for stat in ("B", "V"):
            worst = max(
                worst, float(np.max(np.abs(boots[split][stat] - stored[f"{split}_{stat}"])))
            )
            for k, K in enumerate(grid):
                ref = table[(split, K, stat)]
                q = op.percentile_interval(
                    boots[split][stat][:, k], [*bc["central95"], *bc["central90_old_convention"]]
                )
                worst = max(
                    worst,
                    compare(point[stat][K], ref["estimate"]),
                    compare(np.std(boots[split][stat][:, k], ddof=1), ref["se"]),
                    *(
                        compare(q[i], ref[name])
                        for i, name in enumerate(("q025", "q975", "q05", "q95"))
                    ),
                )
    for (K, stat), ref in diffs.items():
        k = grid.index(K)
        d = boots["validation"][stat][:, k] - boots["calibration"][stat][:, k]
        q = op.percentile_interval(d, [*bc["central95"]])
        worst = max(worst, compare(q[0], ref["q025"]), compare(q[1], ref["q975"]))
    audit = {
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "npz_hash_match": hashes == manifest["npz_sha256"],
        "max_abs_discrepancy": worst,
        "status": "CONSISTENT"
        if worst == 0.0 and hashes == manifest["npz_sha256"]
        else "DIFFERENT",
        "reference_rows": args.reference_rows,
    }
    if args.reference_rows:
        import validation

        proc = inputs.load_process(CFG)
        errs = []
        for split in CFG["splits"]:
            data = inputs.load_split(CFG, split)
            with np.load(PDIR / f"rows_{split}.npz", allow_pickle=False) as z:
                exported = {K: z[f"m{K}"] for K in grid}
            for row in validation.reference_rows(data["tokens"].shape[0])[: args.reference_rows]:
                for K in grid:
                    _, mean = validation.decimal_moments(proc, proc["E"], data["tokens"][row, -K:])
                    errs.append(float(np.max(np.abs(mean - exported[K][row]))))
        audit["reference_moment_max_abs"] = max(errs)
    (OUT / "audit").mkdir(exist_ok=True)
    inputs.dump_json(OUT / "audit" / f"AUDIT_{audit['utc'].replace(':', '')}.json", audit)
    print(json.dumps(audit))
    return 0 if audit["status"] == "CONSISTENT" else 1


if __name__ == "__main__":
    sys.exit(main())
