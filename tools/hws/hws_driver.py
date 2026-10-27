"""HWS driver: G0, stages S0, S1, X1, S2, S3, the null re-check, pauses, resume and the CLI
(API.md §6.2, §10, §11; erratum E8-E10, E14). Records, report and SELECTION writers live in
hws_records (R-0118-6) and are re-exported here under their API names. The synthetic dry run
(DR1-DR13) and stage S0 live in hws_known/hws_dry (erratum E16); running them is metered work.
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import argparse
import json
import os
import re
import time
from pathlib import Path

import hws_worlds as hw
import hws_exact as he
import hws_oracle as ho
import hws_records as hr
import hws_select as hsel
import hws_stats as hs
import stage_records
from hws_records import append_stage_event, archive_partial, freeze, save_hist  # noqa: F401
from hws_records import look_record, tree_sha  # noqa: F401
from topo_pilot.contracts import SequenceLayout

C, S0C = hw.CONTRACT, hw.CONTRACT["s0"]
KNOWN, REFUSE = "FAIL_TECHNICAL/KNOWN_CASE", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
SWEEP = ("S1", "X1", "S2", "S3")
TEXT_SUFFIXES = (".json", ".jsonl", ".md", ".py", ".txt", ".yaml")
SKIP_DIRS = {".git", ".venv", "__pycache__", "sealed"}
N_SCREEN, N_S3 = 4096, 32768
TINY = SequenceLayout(n_obs=9, context=8, analysis_position=8)


class Paused(RuntimeError):
    """A 3x trigger fired at a world or stage boundary (§9.3); exit 4."""


def _rel(out, path) -> str:
    return Path(path).relative_to(out).as_posix()


def _gate(out, gate, status, **details) -> str:
    return stage_records.record_gate(Path(out), gate, status, **hr.num(details))


# ------------------------------------------------------------------------------ G0 search


def _skip_dir(parent: Path, name: str) -> bool:
    low = name.lower()
    docs = low == "research_summary" and parent.name.lower() == "docs"
    return name in SKIP_DIRS or low.startswith("00_read_me_first") or docs


def _needle_in(needle, line) -> bool:
    """D-0127-1: an all-digit needle matches only as a whole token; others stay substrings."""
    if not needle.isdigit():
        return needle in line
    return re.search(rf"(?<![0-9A-Za-z_]){re.escape(needle)}(?![0-9A-Za-z_])", line) is not None


def seed_search(root, needles) -> list:
    """§6.6 G0 discovery search; excluded folders are pruned before any listing or open."""
    hits = []
    for folder, dirs, files in os.walk(root, topdown=True):
        here = Path(folder)
        dirs[:] = sorted(d for d in dirs if not _skip_dir(here, d))
        for name in sorted(files):
            low = name.lower()
            if low.startswith("00_read_me_first") or not low.endswith(TEXT_SUFFIXES):
                continue
            with open(here / name, encoding="utf-8", errors="replace") as handle:
                for i, line in enumerate(handle, 1):
                    found = [nd for nd in needles if _needle_in(nd, line)]
                    hits += [{"path": str(here / name), "needle": nd, "line": i} for nd in found]
    return hits


def classify_seed_hits(hits) -> dict:
    frags = [f.lower() for f in C["seeds"]["g0_declaration_fragments"]]
    jobs = [j.lower() for j in C["seeds"]["g0_hws_job_scratch"]]
    out = []
    for h in hits:
        p = str(h["path"]).replace("\\", "/").lower()
        ok = any(f in p for f in frags) or any(p.startswith(j) for j in jobs)
        out.append(dict(h, kind="hws_declaration" if ok else "unclassified"))
    bad = any(h["kind"] != "hws_declaration" for h in out)
    return {"status": "FAIL_TECHNICAL/SEED_SCOPE" if bad else "PASS", "hits": out}


def g0(out, root=hw.ROOT, stage="S0") -> dict:
    res = classify_seed_hits(seed_search(root, C["seeds"]["g0_needles"]))
    path = Path(out) / "stages" / stage / "G0.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, res)
    _gate(out, "G0", res["status"], hits=len(res["hits"]), record=_rel(out, path))
    if res["status"] != "PASS":
        raise hw.HwsStop(res["status"], "G0: seed-scope hits outside the declarations")
    return res


# ---------------------------------------------------------------------- authority, pauses


def _json(path):
    return None if path is None else json.loads(Path(path).read_text(encoding="utf-8"))


def _preflight(out, stages, auth):
    """FREEZE (missing: refusal; mismatch: FAIL_TECHNICAL/FREEZE) and AUTH, before sampling."""
    out.mkdir(parents=True, exist_ok=True)
    if not (out / "FREEZE.json").exists():
        _gate(out, "FREEZE", REFUSE, reason="FREEZE.json missing; nothing sampled")
        return None
    frz = hr.verify_freeze(out, hw.REPO)
    _gate(out, "FREEZE", "PASS", freeze_sha256=frz["freeze_sha256"])
    a = _json(auth)
    if not a or not set(stages) <= set(a.get("stages", [])):
        _gate(out, "AUTH", REFUSE, reason=f"no owner authority for {list(stages)}")
        return None
    _gate(out, "AUTH", "PASS", job_id=a.get("job_id"), owner=a.get("owner_auth_sha256"))
    return frz


def _ledger_cpu(out) -> float:
    path = Path(out) / "cpu_ledger.json"
    return float(json.loads(path.read_text("utf-8"))["cumulative_cpu_s"]) if path.exists() else 0.0


def _pause(ctx, stage, stage_cpu, stage_fc) -> None:
    """§9.3 both triggers at a world or stage boundary; a continued stage is exempt."""
    if stage in ctx["cont"]:
        return
    cum = _ledger_cpu(ctx["out"]) + time.process_time()
    check = hsel.pause_check(stage_cpu, stage_fc, cum, ctx["cum_fc"])
    if check["pause"]:
        append_stage_event(ctx["out"], {"event": "PAUSE", "stage": stage, "check": check})
        _gate(ctx["out"], f"PAUSE_{stage}", "PAUSE", **check)
        raise Paused(f"{stage}: {check['trigger']}")


# ------------------------------------------------------------------------------ world-looks


def _spot(proc, tok) -> dict:
    """§8 S3 spot checks (E6) and the tier-0 report-only law bound."""
    if proc["W"] == 12:
        spot = he.decimal_spot_check(proc, tok[:4], (4, 32))
    else:
        spot = he.bayes_cross_check(proc, tok[:256])
    if not spot["pass"]:
        raise hw.HwsStop("FAIL_TECHNICAL/E6", f"{proc['key']}: S3 spot check failed {spot}")
    law = he.law_bound_report(proc) if proc.get("tier") == 0 else None
    return {"spot_check": spot, "law_bound": law}


def null_recheck(out, proc, stage, look, n, Ks) -> dict:
    """§5.3 item 5: one fresh NULLCHK look; halt only if the same null exceeds again."""
    first = [k for k, v in look["rows"]["nulls"].items() if hs.null_z(v)["exceeds"]]
    nc = ho.world_look(proc, "NULLCHK", n, Ks, origin=stage, layout=look.get("layout"))
    path = save_hist(out, "NULLCHK", proc["key"], nc["tok"], origin=stage)
    again = {k: hs.null_z(v) for k, v in nc["rows"]["nulls"].items()}
    rep = [k for k in first if again[k]["exceeds"]]
    res = {"first": first, "recheck": again, "reproduced": rep, "hist": _rel(out, path)}
    _gate(out, f"NULL_{stage}_{proc['key']}", "FAIL" if rep else "REPORTED", **res)
    if rep:
        raise hw.HwsStop(KNOWN if stage == "S0" else "FAIL_TECHNICAL/NULL", f"{proc['key']}: {rep}")
    return res


def world_record(out, proc, exact, stage, n, Ks, floors, seed=None, known=False, origin=None):
    """One world-look: sample once, keep the tokens, aggregate, null rule, write the record."""
    t0 = time.process_time()
    p4, layout = stage == "S3", SequenceLayout() if proc["W"] != 6 else TINY
    look = ho.world_look(proc, stage, n, Ks, origin=origin, layout=layout, p4=p4)
    look["layout"] = layout
    hp = save_hist(out, stage, proc["key"], look["tok"], origin)
    look.update(hist=_rel(out, hp), hist_sha256=stage_records.sha256(hp))
    extra = _spot(proc, look["tok"]) if stage == "S3" else {}
    rec = look_record(proc, exact, look, stage, n, floors=floors, seed=seed)
    if rec["e6"]["null_exceeds"] and not known:
        rec["nulls"]["recheck"] = null_recheck(out, proc, stage, look, n, Ks)
    rec.update(hr.num(extra), cpu_s=time.process_time() - t0)
    path = hr.write_look(out, rec, origin)
    files = {_rel(out, p): stage_records.sha256(p) for p in (hp, path)}
    if "recheck" in rec["nulls"]:
        files[rec["nulls"]["recheck"]["hist"]] = stage_records.sha256(
            out / rec["nulls"]["recheck"]["hist"]
        )
    return rec, look, files


def run_s0(out, auth) -> dict:
    """§3 stage S0 (KC1-KC14); implemented in hws_known (erratum E16)."""
    import hws_known

    return hws_known.run_s0(out, auth)


def run_dry(out=hw.DRY_STORE) -> dict:
    """§13 synthetic dry run DR1-DR13; implemented in hws_known (erratum E16)."""
    import hws_dry

    return hws_dry.run_dry(out)


# ------------------------------------------------------------------------- stages S1 to S3


def _stage(ctx, stage, worlds, kinds=None) -> list:
    """One stage over its worklist with resume at world boundaries (RC-5, choice 40)."""
    out, s3 = ctx["out"], stage == "S3"
    ev = [e for e in hr.stage_events(out) if e.get("stage") == stage]
    done = {e["key"]: e for e in ev if e.get("event") == "WORLD_COMPLETE"}
    complete = any(e.get("event") == "STAGE_COMPLETE" for e in ev)
    procs = [(w, hw.build_process(w)) for w in worlds]
    exs = {w.key: he.exact_world(p) for w, p in procs}
    fc = hsel.forecast(stage, [w for w in worlds if exs[w.key]["status"] == "PASS"])
    ctx["cum_fc"] += fc
    ctx["cpu"][stage] = {"forecast_s": fc, "threshold_s": 3 * fc}
    if not complete and any(e.get("event") == "STAGE_BEGIN" for e in ev):
        archive_partial(out, stage)
    elif not complete:
        begin = {"event": "STAGE_BEGIN", "stage": stage, "worklist": [w.key for w in worlds]}
        append_stage_event(out, dict(begin, forecast_s=fc))
    t0, spent = time.process_time(), sum(float(e.get("cpu_s", 0)) for e in done.values())
    recs = []
    for w, proc in procs:
        path = out / "stages" / stage / "worlds" / f"{w.key}.json"
        if w.key in done:
            rec = json.loads(path.read_text(encoding="utf-8"))
        else:
            _pause(ctx, stage, spent + time.process_time() - t0, fc)
            if exs[w.key]["status"] != "PASS":
                rec = hr.exact_record(proc, exs[w.key], stage)
                p = hr.write_look(out, rec)
                files = {_rel(out, p): stage_records.sha256(p)}
            else:
                n, ks, seed = (N_S3, ho.KS_S3, 620103) if s3 else (N_SCREEN, ho.KS_SCREEN, None)
                args = (out, proc, exs[w.key], stage, n, ks, ctx["floors"])
                rec, _, files = world_record(*args, seed=seed)
            ev = {"event": "WORLD_COMPLETE", "stage": stage, "key": w.key, "files": files}
            append_stage_event(out, dict(ev, cpu_s=rec.get("cpu_s", 0.0)))
        if s3:
            ctx["s3"][w.key] = hsel.s3_evaluate(rec, ctx["floors"], kinds[w.key])
            ctx["s3procs"][w.key] = (proc, rec)
        ctx["latest"][w.key] = rec
        ctx["history"].setdefault(w.key, []).append({"path": _rel(out, path), "record": rec})
        recs.append(rec)
    ctx["cpu"][stage]["measured_s"] = spent + time.process_time() - t0
    _pause(ctx, stage, ctx["cpu"][stage]["measured_s"], fc)
    if not complete:
        files = hr._files(out, [f"stages/{stage}", f"hist/{stage}", f"hist/NULLCHK/{stage}"])
        append_stage_event(out, {"event": "STAGE_COMPLETE", "stage": stage, "files": files})
        _gate(out, f"STAGE_{stage}", "PASS", worlds=len(recs))
    return recs


def _accept(out, s0_accept):
    acc, s0p = _json(s0_accept), out / "stages" / "S0" / "S0_RECORD.json"
    sha = stage_records.sha256(s0p) if s0p.exists() else None
    if not acc or acc.get("accept") is not True or acc.get("s0_record_sha256") != sha:
        _gate(out, "S0_ACCEPT", REFUSE, reason="no coordinator S0 ACCEPT bound to S0_RECORD")
        return None
    _gate(out, "S0_ACCEPT", "PASS", s0_record_sha256=sha)
    return dict(json.loads(s0p.read_text(encoding="utf-8")), sha256=sha)


def _world_of(r):
    return hw.World(int(r["W"]), int(r["q"]), hsel.Fraction(r["sigma"]), hsel.Fraction(r["p"]))


def run_sweep(out, auth, s0_accept, cont=None) -> dict:
    """S1 -> (X1) -> (S2) -> S3 under the frozen rules (§6), then the outcome and report."""
    out = Path(out)
    frz = _preflight(out, SWEEP, auth)
    s0 = _accept(out, s0_accept) if frz is not None else None
    if s0 is None:
        return {"status": "REFUSED"}
    c = _json(cont) or {}
    fl = hsel.floors(s0["G4hat_w0"], s0["G4Ahat_w0"])
    ctx = {"out": out, "floors": fl, "latest": {}, "history": {}, "cpu": {}, "s3": {}}
    ctx.update(s3procs={}, cum_fc=hsel.forecast("S0", []), cont=set())
    if c.get("continue") is True:
        ctx["cont"] = set(c.get("stages", [c.get("stage")]))
        cev = {"event": "CONTINUE", "stage": sorted(ctx["cont"])}
        append_stage_event(out, dict(cev, decision_sha256=c.get("decision_sha256")))
    s1 = _stage(ctx, "S1", hw.grid())
    x1 = hsel.x1_trigger(s1)
    if x1["fire"]:
        cells = hw.cells_of([_world_of(r) for r in s1 if r["class"] != "INELIGIBLE/E3"])
        _stage(ctx, "X1", hw.x1_worlds(x1["add_p"], x1["add_sigma"], cells))
    s2 = hsel.s2_worklist(ctx["latest"].values())
    if s2:
        _stage(ctx, "S2", s2)
    fin = hsel.finalists(ctx["latest"].values())
    kinds = {k: "ordinary" for k in fin["ordinary"]}
    kinds.update({k: "fallback_only" for k in fin["fallback_only"]})
    if kinds:
        _stage(ctx, "S3", [_world_of(ctx["latest"][k]) for k in kinds], kinds)
    state = {"fail": None, "complete": True, "records": ctx["latest"], "finalists": fin}
    state.update(s3=ctx["s3"], floors=fl)
    oc = hsel.outcome(state)
    extra = {"x1": x1, "s2": [w.key for w in s2], "cpu": ctx["cpu"], "h_exec": frz["h_exec"]}
    extra.update(s0_record_sha256=s0["sha256"], freeze_sha256=frz["freeze_sha256"])
    lat = ctx["latest"].items()
    extra["nulls"] = {k: r["nulls"]["recheck"] for k, r in lat if "recheck" in r.get("nulls", {})}
    pv = {k: r.get("e6", {}).get("pinsker_violations", 0) for k, r in lat}
    extra["pinsker_flags"] = {k: v for k, v in pv.items() if v}
    rp = hr.write_report(out, hr.report_record(state, oc, extra))
    hr.write_world_summaries(out, ctx["history"])
    if oc["selected"]:
        proc, rec = ctx["s3procs"][oc["selected"]]
        extra["search_record"] = {"path": _rel(out, rp), "sha256": stage_records.sha256(rp)}
        disc = ["data", "hws-v1", "S1|X1|S2", oc["selected"]]
        extra["streams"] = {"discovery": disc, "confirmation": rec["stream"]}
        hr.write_selection(out, hr.selection_record(proc, rec, oc, extra))
    _gate(out, "OUTCOME", oc["outcome"], report=_rel(out, rp))
    return {"status": "PASS", "outcome": oc["outcome"], "report": str(rp)}


# ------------------------------------------------------------------------------------- CLI


def status_of(exc) -> str:
    """Choice 43 exception map."""
    import errors  # noqa: I001
    import oracle_profile
    from c1_records import C1GateFailure
    from topo_pilot.contracts import StageFailure

    if isinstance(exc, hw.HwsStop):
        return exc.status
    if isinstance(exc, (oracle_profile.ProfileError, errors.Invalid, C1GateFailure)):
        return "FAIL_TECHNICAL/NUMERICAL"
    return "FAIL_TECHNICAL/BUILD" if isinstance(exc, StageFailure) else "FAIL_TECHNICAL/UNEXPECTED"


def main(argv=None) -> int:
    """Exit codes: 0 complete, 2 refused (nothing sampled), 3 STOP, 4 PAUSE."""
    ap = argparse.ArgumentParser(prog="hws_driver")
    ap.add_argument("cmd", choices=("s0", "sweep", "dry", "freeze"))
    for opt in ("--out", "--auth", "--s0-accept", "--continue", "--h-exec", "--dry-report"):
        ap.add_argument(opt, default=None)
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else (hw.DRY_STORE if a.cmd == "dry" else hw.STORE)
    try:
        if a.cmd == "s0":
            res = run_s0(out, a.auth)
        elif a.cmd == "sweep":
            res = run_sweep(out, a.auth, a.s0_accept, getattr(a, "continue"))
        elif a.cmd == "dry":
            res = run_dry(out)
        else:
            res = freeze(out, hw.REPO, a.h_exec, a.dry_report)
    except Paused:
        return 4
    except Exception as exc:  # noqa: BLE001  every failure is recorded as a technical STOP
        st, why = status_of(exc), f"{type(exc).__name__}: {exc}"
        append_stage_event(out, {"event": "STOP", "stage": a.cmd, "status": st, "reason": why})
        _gate(out, "STOP", st, reason=why)
        return 3
    return 2 if res.get("status") == "REFUSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
