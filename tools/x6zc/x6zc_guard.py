"""X6ZC guard: the stage harness shared by stages A, B and C (job 0137; API.md §20 C-54). The
dispatch record and mailbox identities, the live meter, the frozen-implementation binding, the
environment check with the thread exemption, the in-stage CPU measure, the attempt directories
with the G2 rerun limit, the crash record, the Stage-C statistics marker and the G-R1 INVALID
report (X6ZC-DESIGN-v1 §6 A1 item 6, §9.1, §13, §15; rulings R-0134-3..5)."""
# fmt: off

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
# isort: off
from x6zc_store import (_utc, _sha, _norm, _cj, xwrite, _lines, write_stage,  # noqa: E402
    x6s1_inventory, inventory_equal, env_check, closure_diff, meter_bind_check,  # noqa: E402
    ledger_cpu, pause_check, _head, rulings)  # noqa: E402
# isort: on

C = zc.CONTRACT
MAILBOX = C["paths"]["mailbox"]
DISPATCH_KEYS = ("job", "task_sha256", "worker_session", "meter_bind_sha256", "meter_import_dir")
PREDECESSOR = {"A": "0", "B": "A", "C": "B"}
MARKER = "STATISTICS_STARTED"
def technical(stop) -> bool:  # a G2-relevant technical failure (R-0134-5)
    return str(stop).startswith("CRASH:") or stop == "CHUNK_FAILED"
def restartable(stop) -> bool:  # a new attempt may follow (a setup error is not the G2 rerun)
    return technical(stop) or stop in ("SETUP_ERROR", "STAGE_B_GATE") or str(stop).startswith(
        "STOPPED:")

# ---- attempt directories (API §11.1; R-0134-5) ----
def _name(stage, k) -> str: return f"{stage}-r{k}" if k else stage
def _attempts(store, stage) -> list:  # [(directory, record | None)] of every attempt, in order
    out, k = [], 0
    while (Path(store) / "stages" / _name(stage, k)).is_dir():
        p = Path(store) / "stages" / _name(stage, k) / "record.json"
        out, k = out + [(_name(stage, k), json.loads(p.read_text("utf-8")) if p.exists()
                         else None)], k + 1
    return out
def _dirs(store, stage) -> list:  # the attempts that wrote a record
    return [d for d, r in _attempts(store, stage) if r is not None]
def _record(store, stage) -> tuple:  # (directory, record) of the latest recorded attempt
    d = _dirs(store, stage)[-1]
    return d, json.loads((Path(store) / "stages" / d / "record.json").read_text("utf-8"))
def refusal(store, stage) -> str | None:  # why a new attempt of `stage` may not start
    att = _attempts(store, stage)
    if sum(r is None or technical(r.get("stop")) for _, r in att) >= 2:
        return f"stage {stage}: the G2 rerun is used up (two technical failures)"
    if any(r is not None and not restartable(r.get("stop")) for _, r in att):
        return f"stage {stage}: an attempt already ended with a non-restartable result"
    if stage == "C" and list((Path(store) / "stages").glob(f"C*/{MARKER}")):
        return "stage C: a Stage-C statistic exists; no rerun (§13 G2)"
    if (Path(store) / "report.json").exists():
        return "report.json exists"
    p = PREDECESSOR[stage]
    if p == "0" and not _dirs(store, "0"):
        return None  # the stage-0 record exists only when the dry run was metered (C-22)
    if not _dirs(store, p):
        return f"stage {stage}: stage {p} has no record"
    stop = _record(store, p)[1].get("stop")
    if stop not in (None, "PAUSE"):
        return f"stage {stage}: the latest stage-{p} record stops with {stop} (F-14)"
    if stop == "PAUSE" and not any(r.get("check") == "PAUSE" and str(r.get("stage")) == p
                                   for r in rulings(store)):
        return f"stage {stage}: stage {p} paused and no coordinator release ruling exists"
    return None

# ---- dispatch, identities and the live meter (F-1, F-6) ----
def dispatch_record(path=None) -> dict:
    p = path or os.environ.get("X6ZC_DISPATCH")
    if not p:
        raise RuntimeError("no dispatch record (--dispatch or X6ZC_DISPATCH)")
    return json.loads(Path(p).read_text("utf-8-sig"))
def _pid_alive(pid) -> bool:
    if os.name != "nt":
        try:
            os.kill(int(pid), 0)
            return True
        except OSError:
            return False
    import ctypes
    k32, code = ctypes.windll.kernel32, ctypes.c_ulong()
    h = k32.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    try:
        return bool(k32.GetExitCodeProcess(h, ctypes.byref(code))) and code.value == 259
    finally:
        k32.CloseHandle(h)
def _in_job() -> bool:
    if os.name != "nt":
        return False
    import ctypes
    k32, res = ctypes.windll.kernel32, ctypes.c_int(0)
    return bool(k32.IsProcessInJob(k32.GetCurrentProcess(), None, ctypes.byref(res))) and bool(
        res.value)
def meter_live(store) -> list:  # METER_ACTIVE.lock names a live meter, the ledger's open entry
    a = json.loads((Path(store) / "METER_ACTIVE.lock").read_text("utf-8"))
    led = json.loads((Path(store) / "cpu_ledger.json").read_text("utf-8"))
    last = (led.get("entries") or [{}])[-1]
    return [why for why, ok in (
        ("METER_ACTIVE.lock: no live meter pid", isinstance(a.get("pid"), int)
         and _pid_alive(a["pid"])),
        ("cpu_ledger.json: the last entry is not this meter's STARTED entry",
         last.get("status") == "STARTED" and last.get("meter_pid") == a.get("pid")),
        ("this process is not inside the meter's job object", _in_job())) if not ok]
def identity_problems(store, fz, disp, job=None) -> list:
    import d2a_train
    out = [f"dispatch record lacks {k}" for k in DISPATCH_KEYS if not str(disp.get(k) or "")]
    if out:
        return out
    checks = (
        ("--job differs from the dispatch record", lambda: job in (None, disp["job"])),
        ("meter_bind_sha256 differs (dispatch, FREEZE, file)", lambda: str(
            disp["meter_bind_sha256"]).lower() == str(fz["meter_bind_sha256"]).lower() and (
            meter_bind_check(Path(store) / "x6zc_meter_bind.py", fz["meter_bind_sha256"],
                             fz["meter_import_dir"]) is None)),
        ("meter_import_dir differs (dispatch, FREEZE)", lambda: _norm(
            disp["meter_import_dir"]) == _norm(fz["meter_import_dir"]) == _norm(
            zc.METER_IMPORT_DIR)),
        ("mailbox identities (request, task.json, task.md, RUN.lock session)", lambda: (
            d2a_train.verify_identity(MAILBOX, disp["job"], disp["task_sha256"],
                                      disp["worker_session"], Path(store) / "RUN.lock") is None)))
    for why, fn in checks:
        out += _try(why, fn)
    return out + _try("meter", lambda: meter_live(store) or True)
def _try(why, fn) -> list:
    try:
        r = fn()
        return [] if r is True else [f"{why}: {r}" if isinstance(r, list) else why]
    except Exception as exc:  # noqa: BLE001  (an unreadable binding is a setup error)
        return [f"{why}: {type(exc).__name__}: {exc}"]

# ---- the frozen implementation and AUTH (F-5) ----
def _git(*args) -> str:
    return subprocess.run(["git", "-C", zc.WORKTREE, *args], capture_output=True, text=True,
                          check=True).stdout
def freeze_problems(store, fz) -> list:
    import topo_pilot
    wt, out = Path(zc.WORKTREE), []
    files = {**(fz.get("modules") or {}), **(fz.get("tests") or {})}
    out += _try("HEAD differs from FREEZE head", lambda: _git("rev-parse", "HEAD").strip()
                == str(fz.get("head")))
    out += _try("uncommitted changes under tools/x6zc or the closure", lambda: not _git(
        "status", "--porcelain", "--untracked-files=all", "--", "tools/x6zc", *zc.CLOSURE
    ).strip())
    out += _try("FREEZE modules and tests: sha256 differs", lambda: [
        p for p, r in files.items() if _sha((wt / p).read_bytes()) != str(r["sha256"]).lower()
    ] or bool(files))
    out += _try("a tools/x6zc module is not in FREEZE modules", lambda: [
        p for p in (f"tools/x6zc/{q.name}" for q in (wt / "tools/x6zc").glob("*.py"))
        if p not in (fz.get("modules") or {})] or True)
    out += _try("the executing checkout is not the X6ZC worktree", lambda: _norm(zc.REPO)
                == _norm(zc.WORKTREE))
    out += _try("topo_pilot is not imported from <worktree>/src", lambda: _norm(
        topo_pilot.__file__).startswith(_norm(wt / "src") + os.sep))
    return out + _try("AUTH.json", lambda: auth_problems(store) or True)
def auth_problems(store) -> list:
    fb = (Path(store) / "FREEZE.json").read_bytes()
    a, fz = json.loads((Path(store) / "AUTH.json").read_text("utf-8")), json.loads(fb)
    out = [f"missing {k}" for k in C["store"]["auth_fields"] if a.get(k) in (None, "", [], {})]
    return out + [why for why, ok in (
        ("schema", a.get("schema") == "x6zc-auth-v1"),
        ("protocol_sha256", str(a.get("protocol_sha256", "")).lower() == str(
            fz.get("protocol_sha256", "")).lower() == _sha(zc.PROTOCOL_FILE.read_bytes())),
        ("freeze_sha256", str(a.get("freeze_sha256", "")).lower() == _sha(fb))) if not ok]

# ---- begin, CPU, finish (F-2, F-7, F-8; R-0134-3..5) ----
def stage_cpu(ctx) -> float:  # this process + the completed chunk children (R-0134-3)
    return time.process_time() - ctx["t0"] + ctx["kids_cpu"]
def _job_cpu():
    try:
        import x6s1_run as sr
        return sr._job_cpu()
    except Exception:  # noqa: BLE001  (informative only: not inside a job object)
        return None
def _begin(store, stage, dispatch=None, job=None) -> dict:
    import x6s1_eval as se
    import x6s1_run as sr
    from x6zc_store import _frozen
    why = refusal(store, stage)
    if why:
        raise RuntimeError(f"refused: {why}")
    k = len(_attempts(store, stage))
    ctx = {"stage": stage, "dir": _name(stage, k), "t0": time.process_time(), "kids_cpu": 0.0,
           "kids": {}, "gates": {}, "values": {}, "setup": [], "env": None, "closure": [],
           "ec": {"status": "NOT_RUN", "changed": []}, "inv0": x6s1_inventory(), "cpu0": None}
    (Path(store) / "stages" / ctx["dir"]).mkdir(parents=True)  # the attempt exists from now on
    ctx["setup"] += _try("cpu_ledger.json", lambda: ctx.update(cpu0=ledger_cpu(store)) or True)
    try:
        fz, disp = _frozen(store), dispatch_record(dispatch)
    except Exception as exc:  # noqa: BLE001
        fz, disp = {}, {}
        ctx["setup"].append(f"FREEZE, AUTH or dispatch record: {type(exc).__name__}: {exc}")
    if fz and disp:
        ctx["setup"] += identity_problems(store, fz, disp, job) + freeze_problems(store, fz)
        sr._CTX.update(store=str(store), job=str(disp["job"]), task=str(disp["task_sha256"]))
    ctx.update(freeze=fz, dispatch={k: disp.get(k) for k in DISPATCH_KEYS})
    se.set_threads()
    ctx["env"] = sr.env_local()
    ctx["ec"], ctx["closure"] = env_check(ctx["env"]), closure_diff()
    ctx["setup"] += ["environment"] * (ctx["ec"]["status"] != "PASS") + [
        "closure differs from H3"] * bool(ctx["closure"])
    ctx["stop"] = "SETUP_ERROR" if ctx["setup"] else None
    return ctx
def _finish(store, ctx, stop=None, n=None) -> int:
    inv1, d = x6s1_inventory(), Path(store) / "stages" / ctx["dir"]
    sh = [xwrite(d / f"x6s1_inventory_{k}.json", _cj(v)) for k, v in (("before", ctx["inv0"]),
                                                                       ("after", inv1))]
    eq, st = inventory_equal(ctx["inv0"], inv1), stage_cpu(ctx)
    cum = (ctx["cpu0"] or 0.0) + st
    if ctx["stage"] == "C" and n is None:  # a Stage-C stop before n is passed: B9's n
        n = _record(store, "B")[1]["values"].get("b9", {}).get("n") if _dirs(store, "B") else None
    pc = pause_check(ctx["stage"], cum, st, n) if ctx["stage"] != "C" or n is not None else {
        "pause": False, "boundary": "C", "note": "n unknown: no pause check"}
    stop = stop or ctx["stop"] or (None if eq else "SETUP_ERROR") or (
        "PAUSE" if pc["pause"] else None)
    rec = {"stage": ctx["stage"], "head": _head(), "env_local": ctx["env"], "pause": pc,
           "env_diff": ctx["ec"]["changed"], "closure_diff": ctx["closure"], "setup": ctx["setup"],
           "gates": ctx["gates"], "values": ctx["values"], "dispatch": ctx.get("dispatch"),
           "inventory": {"before_sha256": sh[0], "after_sha256": sh[1], "equal": eq},
           "cpu_s": st, "cpu_cumulative_s": cum, "cpu_ledger_at_start_s": ctx["cpu0"],
           "cpu_children_s": ctx["kids_cpu"], "cpu_job_object_s": _job_cpu(),
           "error": ctx.get("error"), "stop": stop, "utc": _utc()}
    write_stage(store, ctx["dir"], rec)
    after = (d / MARKER).exists() and stop not in (None, "PAUSE")  # a statistic exists (§13 G2)
    if after or (technical(stop) and sum(
            r is None or technical(r.get("stop")) for _, r in _attempts(store, ctx["stage"])) >= 2):
        write_invalid(store, ctx, f"stage {ctx['stage']} ({ctx['dir']}) stopped with {stop}")
    return 2 if stop else 0
def run_guarded(store, stage, body, dispatch=None, job=None) -> int:
    """Every attempt writes its record: a setup error, a stop, or any exception (CRASH)."""
    ctx = _begin(store, stage, dispatch, job)
    if ctx["stop"]:
        return _finish(store, ctx)
    try:
        return body(store, ctx)
    except Exception as exc:  # noqa: BLE001  (recorded, then the CLI exits 1)
        import d2a_train
        ctx["error"] = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        print(traceback.format_exc(), file=sys.stderr)
        kind = "STOPPED" if isinstance(exc, d2a_train.D2AStop) else "CRASH"
        _finish(store, ctx, f"{kind}:{type(exc).__name__}")
        return 1
def stats_marker(store, ctx) -> str:  # written before the first Stage-C statistic (F-8)
    return xwrite(Path(store) / "stages" / ctx["dir"] / MARKER, _utc().encode("ascii"))

# ---- the G-R1 INVALID report (§9.1; R-0134-5) ----
def budget(store, ctx=None) -> dict:
    out = {}
    for s in ("0", "A", "B", "C"):
        if ctx is not None and s == ctx["stage"]:
            out[s] = stage_cpu(ctx)
        else:
            out[s] = _record(store, s)[1].get("cpu_s") if _dirs(store, s) else None
    return {"cpu_s": out, "pauses": [x for x in _lines(Path(store) / "STAGES.jsonl")
                                     if x.get("stop")]}
def write_invalid(store, ctx, why) -> str | None:
    from x6zc_pipeline import TOP, validate_report
    if (Path(store) / "report.json").exists():
        return None
    cell = {"rule": "G-R1", "outcome": "INVALID", "licence": "", "qualifiers": [], "b": None,
            "not_licensed": zc.not_licensed("INVALID"), "b_interval": [None, None],
            "beta_pp": None, "r": None, "undefined_frac": None, "beta_sb": None, "n": None,
            "descriptive": False}
    rep = {**dict.fromkeys(TOP), "schema": "x6zc-report-v1", "protocol_id": zc.PROTOCOL_ID,
           "protocol_sha256": zc.PROTOCOL_SHA256, "head": _head(), "x6zc_master": zc.X6ZC_MASTER,
           "outcome": "INVALID", "global_rule": "G-R1", "cells": {c: {
               "model": zc.CELLS[c]["model"], "family": zc.CELLS[c]["family"], **cell}
               for c in zc.CELL_ORDER}, "x6s1_statement": C["x6s1_statement"],
           "reuse_verdict": zc.reuse_verdict({}, {"global_outcome": "INVALID", "cells": {},
                                                  "headline": "INVALID"}),
           "budget": budget(store), "env": ctx.get("env"), "invalid": why,
           "stages": {x["stage"]: x["record_sha256"] for x in _lines(Path(store) / "STAGES.jsonl")}}
    if validate_report(rep):
        raise RuntimeError(f"INVALID report schema: {validate_report(rep)}")
    return xwrite(Path(store) / "report.json", _cj(rep))
