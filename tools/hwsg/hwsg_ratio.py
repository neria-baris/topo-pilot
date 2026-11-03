"""HWSG capture ratio rho = X- / Delta4_orc with its joint bootstrap (API.md §7; N1, N7)."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
from pathlib import Path

import c1_means
import k4b_fresh
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

D_KEY = "delta4_orc:all"
NUM = "FAIL_TECHNICAL/NUMERICAL"
UNRESOLVED = "RATIO_UNRESOLVED"


def draws(arrays, controls, seed) -> dict:
    return k4b_stats.joint_bootstrap(k4b_fresh.bootstrap_inputs(arrays, controls), int(seed))


def ratio_draws(dr, j) -> dict:
    d = np.asarray(dr[D_KEY], dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        return {"minus": np.asarray(dr[f"X:{j}:-"], dtype=np.float64) / d,
                "plus": np.asarray(dr[f"X:{j}:+"], dtype=np.float64) / d}


def _tm(x) -> float:
    return float(c1_means.tree_mean(np.asarray(x, dtype=np.float64)))


def model_ratio(dr, j, point_minus, point_D) -> dict:
    rd = ratio_draws(dr, j)
    low = k4b_stats.bounds(rd["minus"], rd["plus"])
    up = k4b_stats.bounds(rd["minus"], rd["minus"])
    return {"status": "DEFINED", "rho": float(point_minus) / float(point_D),
            "rhoL": float(low["L"][0]), "rhoL_rank": int(low["L"][1]),
            "rhoU": float(up["U"][0]), "rhoU_rank": int(up["U"][1]),
            "central95_minus": [float(low["central95_minus"][0][0]),
                                float(low["central95_minus"][1][0])],
            "central95_plus": [float(low["central95_plus"][0][0]),
                               float(low["central95_plus"][1][0])]}


def _lu(v):
    return float(v[0] if isinstance(v, (tuple, list)) else v)


def ratio_gate(ctx, result, world_b4_pass, seed, out=None) -> dict:
    out = Path(out) if out is not None else (
        Path(ctx["out"]) if "out" in ctx else Path(ctx["reservation_path"]).parent)
    arrays, controls = ctx["test_arrays"], ctx["controls"]
    dr = draws(arrays, controls, seed)
    per = result["per_model"]
    for j, p in per.items():
        b = k4b_stats.bounds(dr[f"X:{j}:-"], dr[f"X:{j}:+"])
        if _lu(b["L"]) != _lu(p["L"]) or _lu(b["U"]) != _lu(p["U"]):
            raise C1GateFailure(NUM, f"ratio re-derivation differs from the endpoint (model {j})")
    D = np.asarray(dr[D_KEY], dtype=np.float64)
    d_low = float(k4b_stats.bounds(D, D)["L"][0])
    unresolved = (not world_b4_pass) or d_low <= 0 or bool(np.any(D <= 0))
    point_D = _tm(controls["delta4_orc"]["all"]["X"])
    rec = {"status": UNRESOLVED if unresolved else "DEFINED", "D_L": d_low, "D_point": point_D,
           "per_model": {}, "seed": int(seed), "identity": True}
    rho = {}
    for j in per:
        if unresolved:
            rec["per_model"][str(j)] = {"status": UNRESOLVED}
            continue
        m = model_ratio(dr, j, _tm(arrays[j]["X_minus"]), point_D)
        rec["per_model"][str(j)] = m
        rho[f"rho_minus_{j}"] = ratio_draws(dr, j)["minus"]
    d = out / "stages" / "S8"
    d.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(d / "RATIO.json", rec)
    stage_records.save_npz(d / "RATIO_DRAWS.npz", **rho)
    rec["files"] = [d / "RATIO.json", d / "RATIO_DRAWS.npz"]
    return rec
