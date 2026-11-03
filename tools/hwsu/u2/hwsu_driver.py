"""HWSU jobs KC, E1, REG2, E2, the metered entry point and the CLI (API_U2.md section 5).

No pause check is made (owner addenda 41-43); the CPU is returned and the coordinator books it.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_decide as ud
import hwsu_driver_of as udo
import hwsu_gates as ug
import hwsu_known as uk
import hwsu_meter_bind as umb
import hwsu_model as um
import hwsu_of as uof
import hwsu_records as ur
import hwsu_registry as ureg
import u2  # noqa: F401
import importlib
import json
import os
import sys
import time
from pathlib import Path

import k4b_meter_bind
import meter
import op_guard
import stage_records
import winjob
from c1_records import C1GateFailure

STAGES = ("KC", "E1", "REG2", "E2")
EXIT = {"0": "PASS or a registered outcome", "2": "refused", "3": "FAIL_TECHNICAL",
        "5": "INCONCLUSIVE"}


def build_ctx_u(out, job, attempt, stage, reservation_id=None, root=uc.ROOT, mailbox=uc.MAILBOX,
                hwsc_store=uc.HWSC_STORE, scope=uc.SCOPE_U, seeds=None, dry=False) -> dict:
    S = uc.CONTRACT["seeds"]
    ctx = {"out": Path(out), "job": job, "attempt": attempt, "stage": stage,
           "reservation_id": reservation_id, "root": root, "mailbox": mailbox,
           "hwsc_store": hwsc_store, "scope": scope, "dry": bool(dry), "rows_drawn": False,
           "results": {}, "policy": um.UPolicy(),
           "seeds": dict(S["dry_u2"] if dry else S["model_phase_reserved"] if seeds is None
                         else seeds)}
    if reservation_id is not None:
        ctx["reservation_path"] = Path(out) / ur.reservation_file(reservation_id)
    return ctx


def reg2(out, ctx) -> dict:
    out = Path(out)
    hd = json.loads(uc.read_bytes(ctx.get("handoff_path", uc.HANDOFF_PATH)).decode("utf-8"))
    pre = "DRYHIST" if ctx.get("dry") else "HIST"
    own = ug.of_hist(ctx.get("dry")) + [f"stages/E1/{pre}_{n}.npz" for n in (
        "fit_s_b0", "fit_s_b1", "val_a1_b0", "val_a2_b0")]
    man = ureg.build_u("K-REG2", out / "registry", root=ctx["root"],
                       scratch=ctx.get("scratch", uc.SCRATCH), handoff=hd, own=own,
                       sources=ctx.get("registry_sources"))
    if man["status"] != "PASS":
        raise C1GateFailure(man["status"], f"K-REG2 {man['problems'][:5]}")
    ug.register_new(out, "REG2", "registry")
    return {"n_digests": man["n_digests"], "manifest_sha256": stage_records.sha256(
        out / "registry" / "K-REG2.json"), "superset_diagnostic": man["superset_diagnostic"],
        "cpu_s": man.get("cpu_s")}


def steps(stage, ctx) -> list:
    out, sd = ctx["out"], ug.share_dropped
    f = {"KC0": lambda: uk.kc0(out, ctx), "KC1": lambda: uk.kc1(ctx), "KC2": lambda: uk.kc2(ctx),
         "KC3": lambda: uk.kc3(ctx), "KC4": lambda: uk.kc4(ctx), "KC5": lambda: uk.kc5(out, ctx),
         "KC6": lambda: uk.kc6(out, ctx), "G0U": lambda: ug.g0u_e1(out, ctx),
         "H1-U": lambda: ug.h1_u(out, ctx), "REG1": lambda: ug.reg1(out, ctx),
         "RESERVATION": lambda: uof.reservation_check(ctx),
         "S3": lambda: ug.sample_e1(out, ctx), "H2-U": lambda: ug.h2_u(ctx),
         "H3-U": lambda: ug.h3_u(ctx), "H5-U": lambda: ug.h5_u(ctx),
         "BASIS": lambda: ug.basis_step(ctx), "SUP": lambda: sd(ctx), "F1": lambda: sd(ctx),
         "L1": lambda: sd(ctx), "R1-U": lambda: sd(ctx), "DX": lambda: sd(ctx),
         "M0": lambda: ug.m0_step(ctx), "X1": lambda: ug.x1_step(ctx),
         "KC-U": lambda: ug.kc_u(ctx), "P1": lambda: ug.p1_step(out, ctx),
         "REG2": lambda: reg2(out, ctx), "RELEASE-B": lambda: ug.release_b_check(out, ctx),
         "S7": lambda: ug.sample_e2(out, ctx), "H2-FRESH-U": lambda: ug.h2_fresh(ctx),
         "T-PRE": lambda: ug.t_pre(out, ctx), "NUM": lambda: ug.num_gate(out, ctx),
         "ENDPOINT": lambda: ug.endpoint(out, ctx)}
    if ctx.get("dry"):  # planted adapters exist in the dry run only (R-0223-9)
        f.update({g: (lambda fn=fn: fn(ctx)) for g, fn in ctx.get("planted_u2", {}).items()})
    names = [g for g in uc.CONTRACT["gates_u2"]["jobs"][stage] if g not in ("S0", "AUTH")]

    def wrap(g):
        def run():
            r = f[g]()
            ctx["results"][g] = (r or {}).get("status", "PASS")
            return r
        return run
    return [(g, wrap(g)) for g in names]


def memory_cap_u2(stage) -> int:
    caps = uc.CONTRACT["resources"]["u2_memory_cap_bytes"]
    if stage not in caps:
        raise ValueError(f"unknown stage {stage!r}")
    return int(caps[stage])


def job_paths_u2(job, kind) -> dict:
    if kind in ("test", "store"):
        return umb.job_paths(job, kind)
    if kind == "dru":
        tr = uc.SCRATCH / f"test_hwsu-{job}"
        return {"kind": kind, "out": uc.SCRATCH / f"hwsu-dry-u2-{job}", "temp_root": tr,
                "basetemp": tr / "pytest"}
    raise ValueError(f"unknown job kind {kind!r}")


def _exit_code(outcome, registered) -> int:
    o = str(outcome)
    return 3 if o.startswith("FAIL_TECHNICAL") else 5 if o.startswith(
        "INCONCLUSIVE") and not registered else 0


def _unrecorded(out, rels) -> list:
    out, done = Path(out), set()
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            done |= set(e.get("files", {}))
    found = []
    for rel in rels:
        base = out / rel
        fs = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file()) \
            if base.is_dir() else []
        found += [p.relative_to(out).as_posix() for p in fs]
    return [f for f in dict.fromkeys(found) if f not in done]


def _outcome(stage, records, ctx) -> str:
    bad = next((r for r in records if r["status"] not in uc.CONTRACT["gates_u2"][
        "continuing_statuses"] and r["status"] != "NOT_RUN"), None)
    if stage == "E2" and "resp" in ctx:
        return ud.study_outcome([{"status": r["status"]} for r in records], ctx["resp"])
    return bad["status"] if bad else f"{stage}_PASS"


def run_job(stage, out, job, attempt=1, reservation_id=None, repo=uc.REPO, ledger_path=None,
            ctx=None, dry_continue=False) -> dict:
    out = Path(out)
    ctx = build_ctx_u(out, job, attempt, stage, reservation_id) if ctx is None else ctx
    refused = {"exit": 2, "records": [], "obligation": None, "rows_drawn": False}
    if ctx.get("dry") and not uc.dry_store_ok(out):
        return dict(refused, exit=3, outcome="FAIL_TECHNICAL/BINDING")
    out.mkdir(parents=True, exist_ok=True)
    if not ctx.get("dry_skip_s0"):
        try:
            uk.s0_u(out, repo)
        except C1GateFailure as exc:
            stage_records.record_gate(out, "S0", "INVALID", reason=str(exc.reason)[:2000])
            return dict(refused, outcome="INVALID")
    stage_records.record_gate(out, "S0", "PASS")
    try:
        uk.auth_u(out, job, stage, ctx["mailbox"], ctx.get("contract"))
    except C1GateFailure as exc:
        stage_records.record_gate(out, "AUTH", exc.status, reason=str(exc.reason)[:2000])
        return dict(refused, outcome=exc.status)
    stage_records.record_gate(out, "AUTH", "PASS")
    ur.begin_stage(out, stage)
    t0 = time.process_time()
    records = ur.run_gates_u(out, steps(stage, ctx),
                             continuing=tuple(uc.CONTRACT["gates_u2"]["continuing_statuses"]),
                             dry_continue=dry_continue)
    ctx["cpu_s"] = time.process_time() - t0
    outcome = _outcome(stage, records, ctx)
    rep = []
    try:
        if stage == "KC":
            rep.append(uk.kc_report(out, records))
        elif stage == "E1" and "pc" in ctx:
            rep.append(ug.validation_report(out, ctx, records))
        elif stage == "E2" and "resp" in ctx:
            rep.append(ug.report_u(out, ctx, records))
    except Exception as exc:  # noqa: BLE001  a report failure is a technical failure
        outcome = f"FAIL_TECHNICAL/LINEAGE: report {exc!r}"[:200]
    complete = stage == "E2" and "resp" in ctx
    name = ur.obligation_name(stage, attempt, final=complete)
    result = {"exit": _exit_code(outcome, complete), "outcome": outcome,
              "records": records, "obligation": name, "rows_drawn": ctx["rows_drawn"],
              "cpu_s": ctx["cpu_s"]}
    try:
        ob = ur.write_obligation(out, name, stage, written_by=f"hwsu_driver job {job}",
                                 dry=ctx.get("dry", False), attempt=attempt,
                                 reservation_id=reservation_id)
        extra = ["SEALED_VALIDATION.json"] if (out / "SEALED_VALIDATION.json").is_file() \
            and stage == "E1" else []
        ur.complete_stage(out, stage, _unrecorded(out, [f"stages/{stage}", *extra, ob.name]))
        end = complete or (stage in ("E1", "E2") and not ctx["rows_drawn"])
        if end and reservation_id is not None:
            ur.end_reservation(out, reservation_id, ur.utc(), ob)
    except C1GateFailure as exc:
        result["closing_error"] = f"{exc.status}: {exc.reason}"
    return result


def meter_main(argv=None) -> int:
    argv, opts = list(sys.argv[1:] if argv is None else argv), {}
    for flag in ("--job", "--task-sha256", "--session", "--kind", "--stage"):
        argv, opts[flag] = umb._pop(argv, flag)
    missing = [f for f, v in opts.items() if v is None]
    if missing:
        print(f"hwsu_driver: missing {missing}", file=sys.stderr)
        return 2
    job, session = opts["--job"], opts["--session"]
    try:
        paths = job_paths_u2(job, opts["--kind"])
        cap = memory_cap_u2(opts["--stage"])
    except ValueError as exc:
        print(f"hwsu_driver: {exc}", file=sys.stderr)
        return 2
    out = Path(paths["out"])
    if not umb.placement_ok(dict(paths, kind="dry" if paths["kind"] == "dru" else paths["kind"]
                                 ))["ok"]:
        print("hwsu_driver: placement refused", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    umb.bind(job, opts["--task-sha256"], out, session, "OF", paths["temp_root"])
    winjob.MEMORY_CAP = cap
    if meter.LOCK.exists() and session not in meter.LOCK.read_text("utf-8"):
        print("hwsu_driver: RUN.lock names another session", file=sys.stderr)
        return 3
    if not meter.ACTIVE.exists():
        op_guard.archive_stale(meter.OUT)
    meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=meter.OUT / op_guard.MARKER)
    os.environ.update(umb.child_env_u(job))
    sys.argv = [sys.argv[0]] + k4b_meter_bind.rewrite_argv(argv)
    return meter.main()


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("reserve", "obligation", "end-reservation", "attest",
                            "ledger-append"):
        return udo.main(argv)
    cmd, opts = udo._parse(argv)
    g = lambda k, d=None: opts[k][0] if k in opts else d  # noqa: E731
    job = g("job", "0")
    out = Path(g("out")) if g("out") else (
        uc.SCRATCH / f"hwsu-dry-u2-{job}" if cmd == "dry" else uc.STORE)
    code = 0
    if cmd in ("kc", "e1", "reg2", "e2"):
        res = run_job(cmd.upper(), out, job, int(g("attempt", 1)), g("reservation"),
                      ledger_path=g("ledger"))
        code = res["exit"]
    elif cmd == "freeze":
        res = uk.freeze_u(out, uc.REPO, g("h_exec"), g("dry_report"), opts.get("j_u", []),
                          g("written_by", "hwsu_driver freeze"))
    elif cmd == "s0":
        res = uk.s0_u(out, uc.REPO)
    elif cmd == "audit":
        res = importlib.import_module("hwsu_bind_u2").audit_u2()
        code = 0 if res["status"] == "PASS" else 3
    elif cmd == "dry":
        only = g("only")
        res = importlib.import_module("hwsu_dry2").run_dru(out, only.split(",") if only else None)
        code = 0 if res.get("all_pass") else 3
    else:
        print(f"hwsu_driver: unknown subcommand {cmd!r}", file=sys.stderr)
        return 2
    print(json.dumps(res, indent=1, default=str))
    return code


if __name__ == "__main__":
    sys.exit(main())
