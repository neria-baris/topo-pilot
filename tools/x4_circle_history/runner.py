"""Future feasibility stage driver (job 0016 builds it; it never runs a scientific stage here).

Usage (later, through meter_bind.py with a verified coordinator release only):
  python runner.py --release <mailbox>/jobs/<job>/RELEASE.json
      --stage identity|oracle|charts|precision|export

Every stage refuses (exit 3) unless release.verify() accepts the release AND the stage is
released. Stage bodies take an injected Context, so synthetic tests can drive them with a memory
store. Gates are appended to GATES.jsonl; after the first non-PASS gate every later stage
refuses. Importing this module has no side effects.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for extra in (HERE, HERE.parent / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

from errors import AccessDenied, Invalid, JoinError, Unresolved  # noqa: E402

STAGE_ORDER = ("identity", "oracle", "charts", "precision", "export")
SPLITS = (("calibration", 1), ("validation", 2))


@dataclass
class Context:
    out: Path
    store: object
    manifest: object
    models: list
    process: dict
    contract: dict
    guard: Callable[[], None] = lambda: None
    notes: dict = field(default_factory=dict)


def _write_new(path: Path, obj) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, indent=1, sort_keys=True, default=str) + "\n")


def _save_npz(path: Path, **arrays) -> None:
    with path.open("xb") as handle:
        np.savez_compressed(handle, **arrays)


def gates_so_far(out: Path) -> list:
    path = out / "GATES.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def record_gate(out: Path, gate: str, status: str, **details) -> str:
    entry = {
        "gate": gate,
        "status": status,
        "criterion_met": status == "PASS",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **details,
    }
    with (out / "GATES.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, default=str) + "\n")
    return status


def _require_open(out: Path) -> None:
    stopped = [g for g in gates_so_far(out) if g["status"] != "PASS"]
    if stopped:
        raise Unresolved(f"cohort ended at gate {stopped[0]['gate']} ({stopped[0]['status']})")


def _run_gate(ctx: Context, gate: str, fn) -> object:
    """Run one gate body; Invalid -> FAIL_TECHNICAL, Unresolved/JoinError -> INCONCLUSIVE."""
    try:
        return fn()
    except Invalid as exc:
        record_gate(ctx.out, gate, "FAIL_TECHNICAL", reason=str(exc))
        raise
    except (Unresolved, JoinError) as exc:
        record_gate(ctx.out, gate, "INCONCLUSIVE", reason=str(exc))
        raise


def _panel_rows(ctx: Context, model: int) -> dict:
    from adapter import RestrictedE4Adapter
    from scores import canonical_from_named

    adapter = RestrictedE4Adapter(ctx.store, ctx.manifest)
    data = adapter.panels(model, (1, 2))
    perm = ctx.process["perm"][model]
    for d in data.values():
        d["canonical32"] = canonical_from_named(d["named32"], perm)
    return data


def stage_identity(ctx: Context) -> dict:
    from adapter import RestrictedE4Adapter, cross_model_join

    _require_open(ctx.out)
    adapter = RestrictedE4Adapter(ctx.store, ctx.manifest)

    def body():
        if ctx.process.get("canonical_spread", 1.0) != 0.0:
            raise JoinError("canonical emissions differ across models; no shared oracle")
        report = adapter.identity_report()
        keys = {m: adapter.join_keys(m, ctx.process["perm"][m]) for m in ctx.models}
        joined = cross_model_join(keys)
        return {"report": report, "joined_rows": int(len(joined["sequence_id"]))}

    result = _run_gate(ctx, "identity", body)
    _write_new(ctx.out / "IDENTITY.json", result)
    record_gate(ctx.out, "identity", "PASS", joined_rows=result["joined_rows"])
    return result


def stage_oracle(ctx: Context) -> dict:
    import error_bound
    from scores import oracle_moments

    _require_open(ctx.out)
    p = ctx.process
    cache: dict = {}

    def body():
        summary = {}
        for model in ctx.models:
            ctx.guard()
            data = _panel_rows(ctx, model)
            arrays = {}
            for split, panel in SPLITS:
                d = data[panel]
                m = oracle_moments(p["T"], p["E"], p["pi"], d["canonical32"], p["features"])
                four = error_bound.reference_check_rows(
                    p["T"],
                    p["E"],
                    p["pi"],
                    p["coords"],
                    d["canonical32"][:4],
                    {K: m[K][:4] for K in (1, 4, 32)},
                    (1, 4, 32),
                    split,
                    cache=cache,
                )
                full = error_bound.reference_check_rows(
                    p["T"],
                    p["E"],
                    p["pi"],
                    p["coords"],
                    d["canonical32"],
                    m,
                    (4, 32),
                    split,
                    cache=cache,
                )
                if four["status"] != "PASS" or full["status"] != "PASS":
                    raise Invalid(f"model {model} {split}: reference moment check failed")
                summary[f"{model}/{split}"] = {"four_lowest": four, "all_rows": full}
                arrays.update(
                    {
                        f"{split}_{k}": v
                        for k, v in (
                            ("history_id", d["history_id"]),
                            ("sequence_id", d["sequence_id"]),
                            ("m1", m[1]),
                            ("m4", m[4]),
                            ("m32", m[32]),
                        )
                    }
                )
            _save_npz(ctx.out / f"oracle_{model}.npz", **arrays)
        return summary

    result = _run_gate(ctx, "process_and_reference", body)
    _write_new(ctx.out / "ORACLE.json", result)
    record_gate(ctx.out, "process_and_reference", "PASS")
    return result


def _load_oracle(ctx: Context, model: int) -> dict:
    with np.load(ctx.out / f"oracle_{model}.npz", allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def stage_charts(ctx: Context) -> dict:
    import chart as ch
    import error_bound
    from scores import scores, unit_vectors

    _require_open(ctx.out)
    cfg = dict(ctx.contract["chart"], field=ctx.contract["chart"]["field"])
    cfg.update(native_operation_wall_s=ctx.contract["resources"]["native_operation_wall_s"])
    p, results, constructions = ctx.process, {}, 0
    for model in ctx.models:
        ctx.guard()
        data, orc = _panel_rows(ctx, model), _load_oracle(ctx, model)
        cal, val = data[1], data[2]
        if constructions + 2 > ctx.contract["chart"]["max_chart_constructions"]:
            raise Invalid("chart construction limit would be exceeded")
        chart = _run_gate(
            ctx,
            "chart_calibration",
            lambda: ch.fit_chart(cal["activation"], cal["history_id"], cfg, ctx.guard),
        )
        constructions += 1
        gauge = _run_gate(ctx, "gauge", lambda: ch.fit_gauge(chart, orc["calibration_m32"]))
        _save_npz(ctx.out / f"chart_{model}.npz", **ch.chart_to_arrays(chart, gauge))
        _write_new(ctx.out / f"chart_{model}.json", {"info": chart.info, "gauge": gauge.__dict__})
        direct = _run_gate(
            ctx,
            "validation_direct_chart",
            lambda: ch.fit_chart(val["activation"], val["history_id"], cfg, ctx.guard),
        )
        constructions += 1
        ext = _run_gate(
            ctx, "extension_support", lambda: ch.extend(chart, gauge, val["activation"], cfg)
        )
        gates = ch.chart_gates(ext, direct.phi, cfg)
        for name, gate in (
            ("support", "extension_support"),
            ("fidelity", "fidelity_A"),
            ("bins", "phase_bins"),
            ("resultant", "overall_resultant"),
        ):
            if (
                record_gate(
                    ctx.out, gate, gates[name]["status"], model=model, value=gates[name]["value"]
                )
                != "PASS"
            ):
                return {"stopped_at": gate, "model": model, "gates": gates}
        phases = {"calibration": ch.apply_gauge(chart.phi, gauge), "validation": ext.phase}
        _save_npz(ctx.out / f"phases_{model}.npz", **phases)
        certs = {}
        for split, _ in SPLITS:
            u = unit_vectors(phases[split])
            x = scores(u, orc[f"{split}_m32"], orc[f"{split}_m4"])
            cal_rows = data[1 if split == "calibration" else 2]["canonical32"]
            certs[split] = error_bound.certify_rows(
                p["T"],
                p["E"],
                p["pi"],
                p["coords"],
                cal_rows,
                phases[split],
                x,
                orc[f"{split}_m4"],
                orc[f"{split}_m32"],
                split,
            )
        status = (
            "PASS"
            if all(c["status"] == "CERTIFIED" for c in certs.values())
            else "FAIL_TECHNICAL"
            if any(c["status"] == "FAIL_TECHNICAL" for c in certs.values())
            else "INCONCLUSIVE"
        )
        if (
            record_gate(
                ctx.out,
                "row_score_certificates",
                status,
                model=model,
                max_bound={k: c["max_bound"] for k, c in certs.items()},
            )
            != "PASS"
        ):
            return {"stopped_at": "row_score_certificates", "model": model}
        results[model] = {
            "gates": gates,
            "certificates": {
                k: {kk: vv for kk, vv in c.items() if kk != "bounds"} for k, c in certs.items()
            },
        }
    _write_new(ctx.out / "CHARTS.json", results)
    return results


def stage_precision(ctx: Context) -> dict:
    import precision as pr
    from scores import r4_norms, scores, unit_vectors

    _require_open(ctx.out)
    pc = ctx.contract["precision"]
    cfg = {k: pc[k] for k in ("delta", "alternative", "power", "alpha")}
    cfg["projected_N"] = pc["projected_N"]
    X, R, b4_point = {}, {}, {}
    for model in ctx.models:
        orc = _load_oracle(ctx, model)
        with np.load(ctx.out / f"phases_{model}.npz", allow_pickle=False) as z:
            phi = z["validation"]
        order = np.argsort(orc["validation_sequence_id"], kind="stable")
        X[model] = scores(unit_vectors(phi), orc["validation_m32"], orc["validation_m4"])[order]
        R[model] = r4_norms(orc["validation_m32"], orc["validation_m4"])[order]
        b4_point[model] = float(np.mean(R[model]))
    n = len(next(iter(X.values())))
    sd, b4 = pr.sd_b4_draws(X, R, ctx.models, pc["sd_seed"], pc["sd_draws"], n)
    e = pr.centered_draws(
        X, ctx.models, pc["centered_seed"], pc["centered_draws"], pc["projected_N"]
    )
    b4s = pr.b4_summary(b4, b4_point, ctx.models, cfg)
    if record_gate(ctx.out, "B4_lower", b4s["status"], summary=b4s) != "PASS":
        return {"stopped_at": "B4_lower", "B4": b4s}
    ps = pr.precision_summary(sd, e, ctx.models, cfg)
    record_gate(ctx.out, "precision_projection", ps["status"], summary=ps)
    result = {"B4": b4s, "precision": ps}
    _write_new(ctx.out / "PRECISION.json", result)
    return result


def stage_export(ctx: Context) -> dict:
    gates = gates_so_far(ctx.out)
    first = next((g for g in gates if g["status"] != "PASS"), None)
    overall = (
        "FAIL"
        if first and first["status"] == "FAIL_TECHNICAL"
        else "INCONCLUSIVE"
        if first
        else "PASS"
        if [g["gate"] for g in gates if g["gate"] == "precision_projection"]
        else "INCOMPLETE"
    )
    summary = {
        "overall": overall,
        "first_non_pass": first,
        "gates": gates,
        "scope": "operational-assay feasibility only; no Delta4 support, causal use or "
        "topology necessity is implied",
    }
    _write_new(ctx.out / "FEASIBILITY_SUMMARY.json", summary)
    return summary


STAGES = {
    "identity": stage_identity,
    "oracle": stage_oracle,
    "charts": stage_charts,
    "precision": stage_precision,
    "export": stage_export,
}


def main(argv=None) -> int:
    import argparse

    import release

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--release", required=True)
    parser.add_argument("--stage", required=True, choices=STAGE_ORDER)
    args = parser.parse_args(argv)
    try:
        rel = release.verify(Path(args.release))
    except release.ReleaseError as exc:
        print(json.dumps({"refused": str(exc)}))
        return 3
    if args.stage not in rel["released_stages"]:
        print(json.dumps({"refused": f"stage {args.stage} not released"}))
        return 3
    import live_context

    try:
        ctx = live_context.build(rel)
        print(
            json.dumps(
                {"stage": args.stage, "result": "done", "keys": sorted(STAGES[args.stage](ctx))},
                default=str,
            )
        )
    except (Invalid, Unresolved, JoinError, AccessDenied, live_context.StopRequested) as exc:
        print(json.dumps({"stage": args.stage, "stopped": type(exc).__name__, "reason": str(exc)}))
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
