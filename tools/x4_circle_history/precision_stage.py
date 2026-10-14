"""Precision and export stage bodies for runner.py (API.md spec v2.4 items 8-10; builder-tested).

Validation rows are reordered by sequence_id (evaluation order). Before any bootstrap, every
model's sorted sequence_id array and canonical-history digests must be identical (Invalid ->
FAIL_TECHNICAL at B4_lower). The three fixed controls are reported with their intervals and
near-zero angular counts beside the oracle Z_bound; they are never gated or used to recentre.
PRECISION.json is written in every outcome.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import stage_records as sr
from errors import Invalid


def _load_npz(path: Path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _evaluation_rows(ctx) -> dict:
    from scores import history_digests

    rows = {}
    for model in ctx.models:
        orc = _load_npz(ctx.out / f"oracle_{model}.npz")
        phases = _load_npz(ctx.out / f"phases_{model}.npz")
        order = np.argsort(orc["validation_sequence_id"], kind="stable")
        rows[model] = {
            "sequence_id": orc["validation_sequence_id"][order],
            "digest": history_digests(orc["validation_canonical32"][order]),
            "canonical32": orc["validation_canonical32"][order],
            "phi": phases["validation"][order],
            **{f"m{K}": orc[f"validation_m{K}"][order] for K in (1, 4, 32)},
        }
    first = rows[ctx.models[0]]
    for model, r in rows.items():
        if not np.array_equal(r["sequence_id"], first["sequence_id"]):
            raise Invalid(f"model {model}: validation sequence_id differs across models")
        if r["digest"] != first["digest"]:
            raise Invalid(f"model {model}: canonical history digests differ across models")
    return rows


def _round_up(x: Fraction) -> float:
    value = float(x)
    return value if Fraction(value) >= x else math.nextafter(value, math.inf)


def _instability_bounds(oracle: dict, model, S: int) -> dict:
    """bound_K = exact max validation moment gap + moment envelope, rounded up (diagnostic)."""
    import error_bound as eb

    s = oracle["rows"][f"{model}/validation"]
    gaps = {
        1: Fraction(s["k1_all_rows_diagnostic"]["moment_check_max_exact"]["1"]),
        4: Fraction(s["all_rows"]["moment_check_max_exact"]["4"]),
    }
    return {
        K: _round_up(gap + eb.moment_envelope(eb.posterior_envelope(K, S), S))
        for K, gap in gaps.items()
    }


def _controls(ctx, rows, oracle) -> dict:
    import precision as pr
    from scores import CONTROL_NAMES, angular_instability, control_scores

    pc = ctx.contract["precision"]
    C = {name: {} for name in CONTROL_NAMES}
    counts = {}
    for model, r in rows.items():
        per = control_scores(r["m1"], r["m4"], r["m32"], r["canonical32"])
        for name in CONTROL_NAMES:
            C[name][model] = per[name]
        bounds = _instability_bounds(oracle, model, int(np.asarray(ctx.process["pi"]).shape[0]))
        counts[model] = {
            f"m{K}_unit": {"bound": b, "rows": int(np.sum(angular_instability(r[f"m{K}"], b)))}
            for K, b in bounds.items()
        }
    summary = pr.control_summary(C, ctx.models, pc["sd_seed"], pc["sd_draws"])
    return {"summary": summary, "angular_instability": counts}


def run(ctx) -> dict:
    import precision as pr
    from scores import r4_norms, scores, unit_vectors

    pc = ctx.contract["precision"]
    cfg = {k: pc[k] for k in ("delta", "alternative", "power", "alpha", "projected_N")}
    oracle = json.loads((ctx.out / "ORACLE.json").read_text(encoding="utf-8"))
    rows = sr.run_gate(ctx.out, "B4_lower", lambda: _evaluation_rows(ctx))
    X = {m: scores(unit_vectors(r["phi"]), r["m32"], r["m4"]) for m, r in rows.items()}
    R = {m: r4_norms(r["m32"], r["m4"]) for m, r in rows.items()}
    result = {
        "controls": _controls(ctx, rows, oracle),
        "Z_bound": oracle.get("process_law"),
        "scope": "validation panel only; controls reported, never gated or recentred",
    }
    n = len(next(iter(X.values())))
    sd, b4 = pr.sd_b4_draws(X, R, ctx.models, pc["sd_seed"], pc["sd_draws"], n)
    b4_point = {m: float(np.mean(R[m])) for m in ctx.models}
    result["B4"] = pr.b4_summary(b4, b4_point, ctx.models, cfg)
    if sr.record_gate(ctx.out, "B4_lower", result["B4"]["status"], summary=result["B4"]) != "PASS":
        result["stopped_at"] = "B4_lower"
        sr.write_new(ctx.out / "PRECISION.json", result)
        return result
    e = pr.centered_draws(
        X, ctx.models, pc["centered_seed"], pc["centered_draws"], cfg["projected_N"]
    )
    result["precision"] = pr.precision_summary(sd, e, ctx.models, cfg)
    sr.record_gate(
        ctx.out, "precision_projection", result["precision"]["status"], summary=result["precision"]
    )
    sr.write_new(ctx.out / "PRECISION.json", result)
    return result


def export_summary(out: Path) -> dict:
    gates = sr.gates_so_far(out)
    stages = sr.stages_so_far(out)
    integrity = [r for r in stages if r["event"] == "REFUSED" and r.get("integrity")]
    unfinished = sr.attempts_without_completion(out)
    killed = sorted(p.name for p in (Path(out) / "operations").glob("KILLED_*.json"))
    first = next((g for g in gates if g["status"] != "PASS"), None)
    if integrity or (first and first["status"] == "FAIL_TECHNICAL"):
        overall = "FAIL"
    elif first or [s for s in unfinished if s != "export"] or killed:
        overall = "INCONCLUSIVE"
    elif any(g["gate"] == "precision_projection" for g in gates):
        overall = "PASS"
    else:
        overall = "INCOMPLETE"
    return {
        "overall": overall,
        "first_non_pass": first,
        "gates": gates,
        "integrity_refusals": integrity,
        "attempts_without_completion": [s for s in unfinished if s != "export"],
        "killed_operations": killed,
        "scope": "operational-assay feasibility only; no Delta4 support, causal use or "
        "topology necessity is implied",
    }
