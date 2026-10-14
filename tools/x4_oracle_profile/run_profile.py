"""Job-0014 driver: numerical validation (pre-freeze) and the frozen full profile.

Usage (always via meter.py; venv interpreter; PYTHONPATH = research src):
  python run_profile.py validate   # identity, K8 reproduction FIRST, stored values, references
  python run_profile.py profile    # only after FREEZE.json; RUN_ONCE; all K, bootstrap, tables

Every stage checks runtime controls at safe boundaries: STOP/INVALID stop the stage (partial
outputs kept), HOLD waits in place with live state until the control clears.
"""

from __future__ import annotations

import csv
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
SPLITS = tuple(CFG["splits"])


from runtime import Stopped, guard, save_npz  # noqa: E402
from validation import validate  # noqa: E402


def split_profile(proc, split, tokens) -> dict:
    means = {}
    for K in CFG["K_grid"]:
        guard(f"profile/{split}/K{K}")
        means[K] = op.posterior_means(
            proc["T"], proc["E"], proc["pi"], tokens, (K,), proc["features"]
        )[K]
    rows = op.residual_rows(means, CFG["full_K"])
    return {"means": means, **rows, "point": op.profile_point(rows["norm"], rows["sq"])}


def bootstrap(split, rows) -> tuple[dict, dict]:
    from topo_pilot.contracts import SeedTree

    bc = CFG["bootstrap"]
    tree = SeedTree(bc["seedtree_master"])
    rng = tree.generator(bc["stream"], "bootstrap", split)
    draws, chunk = {"B": [], "V": []}, 500
    for start in range(0, bc["draws"], chunk):
        guard(f"bootstrap/{split}/{start}")
        part = op.bootstrap_profile(
            rows["norm"], rows["sq"], CFG["K_grid"], rng, min(chunk, bc["draws"] - start)
        )
        draws["B"].append(part["B"])
        draws["V"].append(part["V"])
    return {k: np.concatenate(v) for k, v in draws.items()}, dict(tree.issued)


def summarise(point: float, draws: np.ndarray) -> dict:
    bc = CFG["bootstrap"]
    q95 = op.percentile_interval(draws, bc["central95"])
    q90 = op.percentile_interval(draws, bc["central90_old_convention"])
    return {
        "estimate": point,
        "se": float(np.std(draws, ddof=1)),
        "q025": float(q95[0]),
        "q975": float(q95[1]),
        "q05": float(q90[0]),
        "q95": float(q90[1]),
    }


def diagnostics(res: dict) -> dict:
    out = {}
    for split, r in res.items():
        grid = CFG["K_grid"]
        V = [r["point"]["V"][K] for K in grid]
        B = [r["point"]["B"][K] for K in grid]
        m32sq = np.sum(r["means"][32] ** 2, axis=1)
        out[split] = {
            "V_successive_differences": [V[i] - V[i + 1] for i in range(len(grid) - 1)],
            "V_empirically_nonincreasing": all(V[i] >= V[i + 1] for i in range(len(grid) - 1)),
            "B_successive_differences": [B[i] - B[i + 1] for i in range(len(grid) - 1)],
            "B_le_sqrtV": {K: bool(B[i] <= np.sqrt(V[i]) + 1e-15) for i, K in enumerate(grid)},
            "tower_identity_gap": {
                K: float(
                    r["point"]["V"][K]
                    - (np.mean(m32sq) - np.mean(np.sum(r["means"][K] ** 2, axis=1)))
                )
                for K in grid
            },
            "cross_term_mean_mK_dot_rK": {
                K: float(np.mean(np.sum(r["means"][K] * r["r"][K], axis=1))) for K in grid
            },
            "max_norm_rK": {K: float(np.max(r["norm"][K])) for K in grid},
            "max_norm_mK": {K: float(np.max(np.linalg.norm(r["means"][K], axis=1))) for K in grid},
            "min_sq": {K: float(np.min(r["sq"][K])) for K in grid},
            "K32_residual_exactly_zero": bool(np.all(r["r"][32] == 0.0)),
        }
    return out


def write_tables(table: list, diff: list) -> None:
    pdir = OUT / "profile"
    inputs.dump_json(pdir / "PROFILE_TABLE.json", table)
    inputs.dump_json(pdir / "SPLIT_DIFFERENCE.json", diff)
    for name, rows in (("PROFILE_TABLE.csv", table), ("SPLIT_DIFFERENCE.csv", diff)):
        with (pdir / name).open("x", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def profile() -> int:
    import freeze

    bad = freeze.verify()
    if bad:
        raise op.ProfileError(f"freeze mismatch: {bad}")
    guard("profile/start")
    with (OUT / "RUN_ONCE.json").open("x", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "protocol": CFG["protocol"],
                    "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "freeze_sha256": inputs.sha256(OUT / "FREEZE.json"),
                }
            )
        )
    pdir = OUT / "profile"
    pdir.mkdir(exist_ok=False)
    env = inputs.environment()
    inputs.verify_input_hashes(CFG)
    proc = inputs.load_process(CFG)
    data = {s: inputs.load_split(CFG, s) for s in SPLITS}
    res, boots, streams, table, diff, npz = {}, {}, {}, [], [], {}
    for split in SPLITS:
        res[split] = split_profile(proc, split, data[split]["tokens"])
        r = res[split]
        npz[split] = save_npz(
            pdir / f"rows_{split}.npz",
            ids=data[split]["ids"],
            **{f"m{K}": r["means"][K] for K in CFG["K_grid"]},
            **{f"norm{K}": r["norm"][K] for K in CFG["K_grid"]},
            **{f"sq{K}": r["sq"][K] for K in CFG["K_grid"]},
        )
        boots[split], streams[split] = bootstrap(split, r)
        for k, K in enumerate(CFG["K_grid"]):
            for stat in ("B", "V"):
                row = {
                    "split": split,
                    "K": K,
                    "stat": stat,
                    "n": int(data[split]["tokens"].shape[0]),
                }
                row.update(summarise(r["point"][stat][K], boots[split][stat][:, k]))
                table.append(row)
    for k, K in enumerate(CFG["K_grid"]):
        for stat in ("B", "V"):
            point = res["validation"]["point"][stat][K] - res["calibration"]["point"][stat][K]
            d = boots["validation"][stat][:, k] - boots["calibration"][stat][:, k]
            diff.append(
                {
                    "K": K,
                    "stat": stat,
                    "contrast": "validation_minus_calibration",
                    "n_validation": CFG["splits"]["validation"],
                    "n_calibration": CFG["splits"]["calibration"],
                    **summarise(point, d),
                }
            )
    npz["bootstrap"] = save_npz(
        pdir / "bootstrap_draws.npz",
        K=np.array(CFG["K_grid"]),
        **{f"{s}_{stat}": boots[s][stat] for s in SPLITS for stat in ("B", "V")},
    )
    guard("profile/export")
    write_tables(table, diff)
    inputs.dump_json(pdir / "DIAGNOSTICS.json", diagnostics(res))
    inputs.dump_json(
        pdir / "MANIFEST.json",
        {
            "environment": env,
            "streams_issued": streams,
            "npz_sha256": npz,
            "bootstrap": CFG["bootstrap"],
            "K_grid": CFG["K_grid"],
            "freeze_sha256": inputs.sha256(OUT / "FREEZE.json"),
            "interval_labels": "pointwise, descriptive; not "
            "simultaneous/familywise; split differences use independently resampled splits",
            "peak_working_set_bytes": inputs.peak_working_set(),
        },
    )
    print(json.dumps({"stage": "profile", "status": "COMPLETE"}))
    return 0


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        sys.exit({"validate": validate, "profile": profile}[command]())
    except Stopped as exc:
        print(json.dumps({"stage": command, "status": "STOPPED", "reason": str(exc)}))
        sys.exit(6)
