"""HWSU job OF: gate context, run_of and the CLI (API.md §9; protocol §4.2, §5)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_of as uof
import hwsu_records as ur
import hwsu_seed as us
import json
import sys
import time
from pathlib import Path

import stage_records
from c1_records import C1GateFailure

PASS_OUTCOMES = ("OF_PASS", "OF_PASS_RESPONSE_ONLY")
ORDER = ("OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2", "OF-3", "OF-4", "OF-5")


def build_ctx(out, job, attempt, reservation_id, root=uc.ROOT, mailbox=uc.MAILBOX,
              hwsc_store=uc.HWSC_STORE, scope=uc.SCOPE_OF, seeds=uc.SEEDS_OF, dry=False) -> dict:
    return {"out": Path(out), "job": job, "attempt": attempt, "reservation_id": reservation_id,
            "reservation_path": Path(out) / ur.reservation_file(reservation_id), "root": root,
            "mailbox": mailbox, "hwsc_store": hwsc_store, "scope": scope, "seeds": dict(seeds),
            "dry": bool(dry), "rows_drawn": False, "results": {}}


def _exit_code(outcome, gate, rows_drawn) -> int:
    if outcome in PASS_OUTCOMES:
        return 0
    if outcome == "PAUSE":
        return 4
    if gate in ("OF-0", "RESERVATION") and not rows_drawn:
        return 2
    if outcome.startswith("FAIL_TECHNICAL"):
        return 3
    return 5


def run_of(out, job, attempt=1, reservation_id="RES-HWSU-OF", repo=uc.REPO, ledger_path=None,
           cont=None, ctx=None, dry_continue=False) -> dict:
    out = Path(out)
    ctx = build_ctx(out, job, attempt, reservation_id) if ctx is None else ctx
    if ctx.get("dry") and not uc.dry_store_ok(out):
        return {"exit": 3, "outcome": "FAIL_TECHNICAL/BINDING", "records": [], "obligation": None,
                "rows_drawn": False}
    if not (ctx.get("dry") and ctx.get("dry_skip_of_b")):
        try:
            ur.of_b(out, repo)
        except C1GateFailure as exc:
            stage_records.record_gate(out, "OF-B", "INVALID", reason=str(exc.reason)[:2000])
            return {"exit": 2, "outcome": "INVALID", "records": [], "obligation": None,
                    "rows_drawn": False}
    stage_records.record_gate(out, "OF-B", "PASS")
    ur.begin_stage(out, "OF")
    t0 = time.process_time()
    fns = {"OF-0": lambda: us.g0_of(out, ctx), "OF-P": lambda: uof.of_p(ctx),
           "RESERVATION": lambda: uof.reservation_check(ctx), "OF-S": lambda: uof.of_s(out, ctx),
           "OF-H": lambda: uof.of_h(ctx), "OF-1": lambda: uof.of_1(ctx),
           "OF-2": lambda: uof.of_2(ctx), "OF-3": lambda: uof.of_3(ctx),
           "OF-4": lambda: uof.of_4(ctx), "OF-5": lambda: uof.of_5(ctx)}

    def wrap(gate):
        def run():
            ur.pause_or_raise_u(out, "OF", t0, ledger_path, cont)
            r = fns[gate]()
            ctx["results"][gate] = (r or {}).get("status", "PASS")
            return r
        return run

    try:
        records = ur.run_gates_u(out, [(g, wrap(g)) for g in ORDER], dry_continue=dry_continue)
        outcome = uof.of_outcome(records)
    except ur.Paused:
        records = [{"gate": g["gate"], "status": g["status"]}
                   for g in stage_records.gates_so_far(out)]
        outcome = "PAUSE"
    bad = next((r for r in records if r["status"] not in ("PASS", "SHARE_DROPPED", "NOT_RUN")),
               {"gate": None})
    ctx["cpu_s"] = time.process_time() - t0
    if (outcome in PASS_OUTCOMES or "fit" in ctx) and "eval" in ctx:
        try:
            uof.of_report(out, ctx, records)
        except Exception as exc:  # noqa: BLE001  a report failure is a technical failure
            if outcome in PASS_OUTCOMES:
                outcome = f"FAIL_TECHNICAL/LINEAGE: report {exc!r}"[:200]
    name = ur.obligation_name("OF") if outcome in PASS_OUTCOMES else ur.obligation_name(
        "OF", attempt)
    result = {"exit": _exit_code(outcome, bad["gate"], ctx["rows_drawn"]), "outcome": outcome,
              "records": records, "obligation": name, "rows_drawn": ctx["rows_drawn"]}
    try:
        ur.write_obligation(out, name, "OF", written_by=f"hwsu_driver_of job {job}",
                            dry=ctx.get("dry", False), attempt=attempt,
                            reservation_id=reservation_id)
        ur.end_reservation(out, reservation_id, ur.utc(), out / name)
    except C1GateFailure as exc:
        result["closing_error"] = f"{exc.status}: {exc.reason}"
    return result


def _parse(argv) -> tuple:
    cmd, opts, i = argv[0], {}, 1
    while i < len(argv):
        key = argv[i].lstrip("-").replace("-", "_")
        if key == "final":
            opts[key], i = True, i + 1
        else:
            opts.setdefault(key, []).append(argv[i + 1])
            i += 2
    return cmd, opts


def main(argv=None) -> int:
    cmd, opts = _parse(list(sys.argv[1:] if argv is None else argv))
    g = lambda k, d=None: opts[k][0] if k in opts else d  # noqa: E731
    out = Path(g("out")) if g("out") else (uc.DRY_STORE if cmd == "dry" else uc.STORE)
    code = 0
    if cmd not in ("of", "freeze-of", "reserve", "obligation", "end-reservation", "attest",
                   "audit", "ledger-append", "dry"):
        print(f"hwsu_driver_of: unknown subcommand {cmd!r}", file=sys.stderr)
        return 2
    if cmd == "of":
        res = run_of(out, g("job"), int(g("attempt", 1)), g("reservation", "RES-HWSU-OF"),
                     ledger_path=g("ledger"), cont=g("continue"))
        code = res["exit"]
    elif cmd == "freeze-of":
        res = ur.freeze_of(out, uc.REPO, g("h_exec"), g("dry_report"), opts.get("j_of", []),
                           g("written_by", "hwsu_driver_of freeze-of"))
    elif cmd == "reserve":
        res = str(ur.write_reservation(out, g("reservation"), g("scope", uc.SCOPE_OF), ur.utc(),
                                       g("written_by", "hwsu_driver_of reserve")))
    elif cmd == "obligation":
        att = int(g("attempt")) if g("attempt") else None
        name = ur.obligation_name(g("job"), att, bool(opts.get("final")))
        res = str(ur.write_obligation(out, name, g("job"), "hwsu_driver_of obligation",
                                      attempt=att))
    elif cmd == "end-reservation":
        res = str(ur.end_reservation(out, g("reservation"), ur.utc(), g("obligation")))
    elif cmd == "attest":
        res = ur.w2_attestation(uc.ROOT)
    elif cmd == "audit":
        import hwsu_bind

        res = hwsu_bind.audit()
        code = 0 if res["status"] == "PASS" else 3
    elif cmd == "ledger-append":
        res = ur.ledger_append(uc.STUDY_LEDGER, g("label"), g("job"), g("stage"),
                               float(g("cpu_s")), g("source"))
    else:
        import hwsu_dry

        only = g("only")
        res = hwsu_dry.run_dro(out, only.split(",") if only else None)
    print(json.dumps(res, indent=1, default=str))
    return code


if __name__ == "__main__":
    sys.exit(main())
