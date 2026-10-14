"""Future feasibility stage driver (job 0016 builds it; it never runs a scientific stage here).

Usage (later, through meter_bind.py with a verified coordinator release only):
  python runner.py --release <mailbox>/jobs/<job>/RELEASE.json
      --stage identity|oracle|charts|precision|export

Every stage refuses (exit 3) unless release.verify() accepts the release AND the stage is
released. Stage bodies take an injected Context, so synthetic tests can drive them with a memory
store. stage_records enforces prerequisites, no retry and evidence integrity (spec v2.4 item 8);
gates go to GATES.jsonl. Importing this module has no side effects.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for extra in (HERE, HERE.parent / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

import stage_records as sr  # noqa: E402
from errors import AccessDenied, Invalid, JoinError, Unresolved  # noqa: E402
from stage_records import gates_so_far, record_gate  # noqa: E402,F401  (public re-exports)

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
    timed: Callable = None
    notes: dict = field(default_factory=dict)


def _panel_rows(ctx: Context, model: int) -> dict:
    from adapter import RestrictedE4Adapter
    from scores import canonical_from_named

    data = RestrictedE4Adapter(ctx.store, ctx.manifest).panels(model, (1, 2))
    for d in data.values():
        d["canonical32"] = canonical_from_named(d["named32"], ctx.process["perm"][model])
    return data


def _ptuple(p):
    return p["T"], p["E"], p["pi"], p["coords"]


def stage_identity(ctx: Context) -> dict:
    from adapter import RestrictedE4Adapter, cross_model_join

    sr.begin(ctx.out, "identity", ctx.models)
    adapter = RestrictedE4Adapter(ctx.store, ctx.manifest)

    def body():
        if ctx.process.get("canonical_spread", 1.0) != 0.0:
            raise JoinError("canonical emissions differ across models; no shared oracle")
        report = adapter.identity_report()
        keys = {m: adapter.join_keys(m, ctx.process["perm"][m]) for m in ctx.models}
        joined = cross_model_join(keys)
        return {"report": report, "joined_rows": int(len(joined["sequence_id"]))}

    result = sr.run_gate(ctx.out, "identity", body)
    sr.write_new(ctx.out / "IDENTITY.json", result)
    record_gate(ctx.out, "identity", "PASS", joined_rows=result["joined_rows"])
    sr.complete(ctx.out, "identity", ["IDENTITY.json"])
    return result


def _oracle_split(ctx, model, split, panel, d, cache):
    import error_bound as eb
    from reference_cache import row_record
    from scores import oracle_moments

    p = ctx.process
    m = oracle_moments(p["T"], p["E"], p["pi"], d["canonical32"], p["features"])

    def check(rows, Ks):
        moments = {K: m[K][rows] for K in Ks}
        tok = d["canonical32"][rows]
        return eb.reference_check_rows(*_ptuple(p), tok, moments, Ks, split, cache=cache)

    four = check(slice(0, 4), (1, 4, 32))
    full = check(slice(None), (4, 32))
    k1 = check(slice(None), (1,))
    if four["status"] != "PASS" or full["status"] != "PASS":
        raise Invalid(f"model {model} {split}: reference moment check failed")
    arrays = {
        f"{split}_history_id": d["history_id"],
        f"{split}_sequence_id": d["sequence_id"],
        f"{split}_canonical32": d["canonical32"],
        **{f"{split}_m{K}": m[K] for K in (1, 4, 32)},
    }
    record = row_record(model, split, panel, d["history_id"], d["sequence_id"], d["canonical32"])
    summary = {"four_lowest": four, "all_rows": full, "k1_all_rows_diagnostic": k1}
    return summary, arrays, record


def stage_oracle(ctx: Context) -> dict:
    import process_law
    import reference_cache as rc

    sr.begin(ctx.out, "oracle", ctx.models)
    p, cache, rows, files = ctx.process, {}, [], []

    def body():
        summary = {}
        for model in ctx.models:
            ctx.guard()
            data, arrays = _panel_rows(ctx, model), {}
            for split, panel in SPLITS:
                s, a, r = _oracle_split(ctx, model, split, panel, data[panel], cache)
                summary[f"{model}/{split}"] = s
                arrays.update(a)
                rows.append(r)
            sr.save_npz(ctx.out / f"oracle_{model}.npz", **arrays)
            files.append(f"oracle_{model}.npz")
        return {"rows": summary, "process_law": process_law.process_law_bound(*_ptuple(p))}

    result = sr.run_gate(ctx.out, "process_and_reference", body)
    ident = rc.identity(*_ptuple(p))
    sr.write_new(ctx.out / "REFERENCE_CACHE.json", rc.export_cache(cache, ident, rows))
    result["reference_cache"] = {
        "path": "REFERENCE_CACHE.json",
        "sha256": sr.sha256(ctx.out / "REFERENCE_CACHE.json"),
        "identity": ident,
    }
    sr.write_new(ctx.out / "ORACLE.json", result)
    record_gate(ctx.out, "process_and_reference", "PASS")
    sr.complete(ctx.out, "oracle", ["ORACLE.json", "REFERENCE_CACHE.json", *files])
    return result


def _load_reference(ctx: Context) -> tuple[dict, dict]:
    """Verified (cache file object, cache) of the oracle stage; no recomputation (item 9)."""
    import reference_cache as rc

    meta = json.loads((ctx.out / "ORACLE.json").read_text(encoding="utf-8"))["reference_cache"]
    path = ctx.out / meta["path"]
    if sr.sha256(path) != meta["sha256"]:
        raise Invalid("reference cache file differs from the hash recorded in ORACLE.json")
    ident = rc.identity(*_ptuple(ctx.process))
    if ident != meta["identity"]:
        raise Invalid("reference cache identity differs from the current process/sources")
    obj = json.loads(path.read_text(encoding="utf-8"))
    return obj, rc.load_cache(obj, ident)


def _load_npz(path: Path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _check_alignment(model, data, orc, ref_obj) -> None:
    """Saved oracle IDs must equal the reloaded rows EXACTLY (Invalid -> FAIL_TECHNICAL)."""
    from reference_cache import verify_rows

    for split, panel in SPLITS:
        d = data[panel]
        for key in ("history_id", "sequence_id", "canonical32"):
            saved, now = orc[f"{split}_{key}"], np.asarray(d[key])
            if saved.shape != now.shape or not np.array_equal(saved, now):
                raise Invalid(f"model {model} {split}: saved oracle {key} differs from reload")
        verify_rows(
            ref_obj, model, split, panel, d["history_id"], d["sequence_id"], d["canonical32"]
        )


def _chart_model(ctx, model, cfg, ref_obj, ref_cache, budget) -> dict:
    import chart as ch
    import error_bound as eb
    from scores import scores, unit_vectors

    out, timed = ctx.out, ctx.timed
    data, orc = _panel_rows(ctx, model), _load_npz(ctx.out / f"oracle_{model}.npz")
    cal, val = data[1], data[2]

    def fit(rows):
        if budget["constructions"] + 1 > ctx.contract["chart"]["max_chart_constructions"]:
            raise Invalid("chart construction limit would be exceeded")
        budget["constructions"] += 1
        return ch.fit_chart(rows["activation"], rows["history_id"], cfg, ctx.guard, timed)

    def calibration():
        _check_alignment(model, data, orc, ref_obj)
        return fit(cal)

    chart = sr.run_gate(out, "chart_calibration", calibration)
    gauge = sr.run_gate(out, "gauge", lambda: ch.fit_gauge(chart, orc["calibration_m32"]))
    sr.save_npz(out / f"chart_{model}.npz", **ch.chart_to_arrays(chart, gauge))
    sr.write_new(out / f"chart_{model}.json", {"info": chart.info, "gauge": gauge.__dict__})
    direct = sr.run_gate(out, "validation_direct_chart", lambda: fit(val))
    ext = sr.run_gate(
        out, "extension_support", lambda: ch.extend(chart, gauge, val["activation"], cfg, timed)
    )
    gates = ch.chart_gates(ext, direct.phi, cfg)
    for name, gate in (
        ("support", "extension_support"),
        ("fidelity", "fidelity_A"),
        ("bins", "phase_bins"),
        ("resultant", "overall_resultant"),
    ):
        status = gates[name]["status"]
        if record_gate(out, gate, status, model=model, value=gates[name]["value"]) != "PASS":
            return {"stopped_at": gate, "model": model, "gates": gates}
    phases = {"calibration": ch.apply_gauge(chart.phi, gauge), "validation": ext.phase}
    sr.save_npz(out / f"phases_{model}.npz", **phases)
    certs = {}
    for split, panel in SPLITS:
        x = scores(unit_vectors(phases[split]), orc[f"{split}_m32"], orc[f"{split}_m4"])
        certs[split] = sr.run_gate(
            out,
            "row_score_certificates",
            lambda: eb.certify_rows(
                *_ptuple(ctx.process),
                data[panel]["canonical32"],
                phases[split],
                x,
                orc[f"{split}_m4"],
                orc[f"{split}_m32"],
                split,
                cache=ref_cache,
                cache_only=True,
            ),
        )
    statuses = {c["status"] for c in certs.values()}
    status = (
        "PASS"
        if statuses == {"CERTIFIED"}
        else "FAIL_TECHNICAL"
        if "FAIL_TECHNICAL" in statuses
        else "INCONCLUSIVE"
    )
    max_bound = {k: c["max_bound"] for k, c in certs.items()}
    if (
        record_gate(out, "row_score_certificates", status, model=model, max_bound=max_bound)
        != "PASS"
    ):
        return {"stopped_at": "row_score_certificates", "model": model}
    trimmed = {k: {kk: vv for kk, vv in c.items() if kk != "bounds"} for k, c in certs.items()}
    return {"gates": gates, "certificates": trimmed}


def stage_charts(ctx: Context) -> dict:
    sr.begin(ctx.out, "charts", ctx.models)
    cfg = dict(ctx.contract["chart"])
    cfg.update(native_operation_wall_s=ctx.contract["resources"]["native_operation_wall_s"])
    ref_obj, ref_cache = sr.run_gate(ctx.out, "chart_calibration", lambda: _load_reference(ctx))
    results, budget, files = {}, {"constructions": 0}, ["CHARTS.json"]
    for model in ctx.models:
        ctx.guard()
        res = _chart_model(ctx, model, cfg, ref_obj, ref_cache, budget)
        results[model] = res
        files += [f"chart_{model}.npz", f"chart_{model}.json"]
        if "stopped_at" in res:
            sr.write_new(ctx.out / "CHARTS.json", results)
            sr.complete(
                ctx.out, "charts", ["CHARTS.json"], outcome=f"stopped_at {res['stopped_at']}"
            )
            return res
        files.append(f"phases_{model}.npz")
    sr.write_new(ctx.out / "CHARTS.json", results)
    sr.complete(ctx.out, "charts", files)
    return results


def stage_precision(ctx: Context) -> dict:
    import precision_stage

    sr.begin(ctx.out, "precision", ctx.models)
    result = precision_stage.run(ctx)
    sr.complete(ctx.out, "precision", ["PRECISION.json"], outcome=result.get("stopped_at", "done"))
    return result


def stage_export(ctx: Context) -> dict:
    import precision_stage

    sr.begin(ctx.out, "export", ctx.models)
    summary = precision_stage.export_summary(ctx.out)
    sr.write_new(ctx.out / "FEASIBILITY_SUMMARY.json", summary)
    sr.complete(ctx.out, "export", ["FEASIBILITY_SUMMARY.json"])
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
        keys = sorted(STAGES[args.stage](ctx))
        live_context.check_loaded_modules(ctx)
        print(json.dumps({"stage": args.stage, "result": "done", "keys": keys}, default=str))
    except sr.StageRefused as exc:
        print(json.dumps({"stage": args.stage, "refused": str(exc)}))
        return 3
    except (Invalid, Unresolved, JoinError, AccessDenied, live_context.StopRequested) as exc:
        print(json.dumps({"stage": args.stage, "stopped": type(exc).__name__, "reason": str(exc)}))
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
