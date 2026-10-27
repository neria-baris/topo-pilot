"""HWSB driver: preflight, the KB/TRAIN/EVAL stages, pauses, the study ledger, inventories,
FREEZE and the CLI (API.md §8, §12, §13; protocol §5, §6.4, §8.2).

EVAL's B9a hashes and reads stage B's own history payloads in its own store (ruling c7).
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import hws_records
import hwsb_data as hd
import hwsb_gates as hg
import hwsb_known as hk
import hwsb_stages as hs
import hwsb_train as ht
import stage_records
from hwsb_records import (  # noqa: F401  (API.md §8 names)
    freeze,
    implementation_files,
    inventory_diff,
    inventory_snapshot,
    ledger_append,
    ledger_read,
    verify_freeze,
)
from hwsb_stages import train_core  # noqa: F401  (API.md §8 name)

from topo_pilot.contracts import ArtifactStore, LocalFSBackend

REFUSE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
FREEZE = "FAIL_TECHNICAL/FREEZE"
C = hc.CONTRACT


class Paused(RuntimeError):
    """A 3x trigger fired at an item boundary; nothing new is started (exit 4)."""


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _gate(out, gate, status, **details) -> str:
    return stage_records.record_gate(Path(out), gate, status, **hk.jsonable(details))


def _json(x):
    if x is None or isinstance(x, dict):
        return x
    return json.loads(Path(x).read_text(encoding="utf-8"))


def status_of(exc) -> str:
    """Choice 20 exception map."""
    import errors
    import hws_worlds
    import oracle_profile
    from c1_records import C1GateFailure

    from topo_pilot.contracts import ErrorCode, StageFailure

    if isinstance(exc, (hc.HwsbStop, hws_worlds.HwsStop)):
        return exc.status
    if isinstance(exc, C1GateFailure):
        s = str(getattr(exc, "status", ""))
        return (
            s if s.startswith(("FAIL_TECHNICAL/", "INCONCLUSIVE/")) else "FAIL_TECHNICAL/NUMERICAL"
        )
    if isinstance(exc, StageFailure):
        return {
            ErrorCode.NONFINITE_LOSS: "FAIL_TECHNICAL/NONFINITE",
            ErrorCode.SPLIT_OVERLAP: "FAIL_TECHNICAL/LINEAGE",
        }.get(exc.code, "FAIL_TECHNICAL/BUILD")
    if isinstance(exc, (oracle_profile.ProfileError, errors.Invalid)):
        return "FAIL_TECHNICAL/NUMERICAL"
    return "FAIL_TECHNICAL/UNEXPECTED"


# ------------------------------------------------------------------- authority and P-SCHED


def auth_ok(auth, stage) -> dict:
    a = _json(auth)
    if not a:
        return {"ok": False, "reason": "no AUTH record"}
    ok = stage in a.get("stages", []) and a.get("owner_auth_sha256") == hc.ADDENDUM_32_SHA
    return {"ok": ok, "reason": "" if ok else f"AUTH does not cover {stage} under addendum 32"}


def sched_ok(sched, stage) -> dict:
    s = _json(sched)
    if not s:
        return {"ok": False, "rule2": False, "rule3": False, "reason": "no P-SCHED record"}
    r2 = s.get("live_history_reservations") == []
    r3 = bool(
        (s.get("c2nd_s5_accepted") and not s.get("c2nd_pending_s5_rerun")) or s.get("c2nd_terminal")
    )
    need = C["p_sched"]["required"][stage]
    ok = all({"rule2": r2, "rule3": r3}[r] for r in need)
    return {
        "ok": ok,
        "rule2": r2,
        "rule3": r3,
        "reason": "" if ok else f"P-SCHED {need} not met for {stage}",
    }


def preflight(out, stage, auth, sched, repo=hc.REPO) -> dict:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if not (out / "FREEZE.json").exists():
        _gate(out, "FREEZE", REFUSE, reason="FREEZE.json missing; nothing sampled")
        return {"refused": True}
    frz = verify_freeze(out, repo)
    _gate(out, "FREEZE", "PASS", freeze_sha256=frz["freeze_sha256"])
    for name, chk in (("AUTH", auth_ok(auth, stage)), ("SCHED", sched_ok(sched, stage))):
        if not chk["ok"]:
            _gate(out, name, REFUSE, reason=chk["reason"])
            return {"refused": True}
        _gate(out, name, "PASS")
    return {"refused": False, "freeze_sha256": frz["freeze_sha256"]}


# ------------------------------------------------------------------------ pauses and ledger


def pause_check(stage, stage_cpu, cum_cpu) -> dict:
    s_fc, c_fc = C["cpu"]["central_s"][stage], C["cpu"]["cumulative_central_s"][stage]
    k = C["cpu"]["multiplier"]
    by_s, by_c = stage_cpu > k * s_fc, cum_cpu > k * c_fc
    trig = "BOTH" if by_s and by_c else "STAGE" if by_s else "CUMULATIVE" if by_c else None
    return {
        "pause": by_s or by_c,
        "trigger": trig,
        "stage_cpu": stage_cpu,
        "stage_threshold": k * s_fc,
        "cum_cpu": cum_cpu,
        "cum_threshold": k * c_fc,
    }


def running_cpu(stage, ledger_path=hc.STUDY_LEDGER, t0=0.0) -> tuple:
    led = ledger_read(ledger_path)
    run = time.process_time() - t0
    st = sum(e["cpu_s"] for e in led["entries"] if e["stage"] == stage) + run
    return st, float(led["cumulative_cpu_s"]) + run


def pause_or_raise(out, stage, t0, ledger_path=hc.STUDY_LEDGER, cont=None) -> None:
    """Both 3x triggers at an item boundary; a continued stage is exempt."""
    if ledger_path is None or stage in (_json(cont) or {}).get("stages", []):
        return
    chk = pause_check(stage, *running_cpu(stage, ledger_path, t0))
    if chk["pause"]:
        hws_records.append_stage_event(out, {"event": "PAUSE", "stage": stage, "check": chk})
        _gate(out, f"PAUSE_{stage}", "PAUSE", **chk)
        raise Paused(f"{stage}: {chk['trigger']}")


# ------------------------------------------------------------------------ inventory, FREEZE


def _store(out) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(out) / "artifacts"))


def run_train(out, auth, sched, master, kb_accept, cont=None, threads=1) -> dict:
    out, master = Path(out), int(master)
    if preflight(out, "TRAIN", auth, sched)["refused"]:
        return {"status": "REFUSED"}
    acc, kbp = _json(kb_accept), out / "stages" / "KB" / "KB_RECORD.json"
    kb = json.loads(kbp.read_text(encoding="utf-8")) if kbp.exists() else {}
    if not (
        acc
        and acc.get("accept") is True
        and kbp.exists()
        and acc.get("kb_record_sha256") == stage_records.sha256(kbp)
        and kb.get("status") == "PASS"
    ):
        _gate(out, "KB_ACCEPT", REFUSE, reason="no coordinator KB_ACCEPT bound to a PASS record")
        return {"status": "REFUSED"}
    _gate(out, "KB_ACCEPT", "PASS")
    if (out / "stages" / "TRAIN" / str(master) / "TRAIN_RECORD.json").exists():
        raise hc.HwsbStop("FAIL_TECHNICAL/RERUN", f"TRAIN_RECORD of {master} exists")
    pause_or_raise(out, "TRAIN", 0.0, cont=cont)
    store = _store(out)
    proc = hd.build_process(store)
    if hk.jsonable(proc["ids"]) != kb.get("process_ids"):
        raise hc.HwsbStop("FAIL_TECHNICAL/IDENTITY", "process ids differ from the KB record")
    ht.set_threads(threads)
    cap = (
        C["recipe"]["six_thread_fallback"]["per_model_hold_s"]
        if int(threads) == 6
        else C["cpu"]["per_model_hold_s"]
    )
    hold = ht.HoldRule(
        out / "stages" / "TRAIN" / str(master),
        cap_s=float(cap),
        from_step=int(C["cpu"]["hold_from_step"]),
    )
    rec = train_core(out, store, proc, master, hc.REAL_PLAN, hold)
    _gate(out, f"TRAIN_{master}", "PASS", holds=len(rec["holds"]))
    return rec


# ----------------------------------------------------------------------------------- EVAL


def run_eval(out, auth, sched, cont=None) -> dict:
    out = Path(out)
    pf = preflight(out, "EVAL", auth, sched)
    if pf["refused"]:
        return {"status": "REFUSED"}
    recs = {}
    for m in hc.MASTERS:
        p = out / "stages" / "TRAIN" / str(m) / "TRAIN_RECORD.json"
        recs[m] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        if recs[m].get("status") != "COMPLETE":
            _gate(out, "TRAIN_COMPLETE", REFUSE, master=m)
            return {"status": "REFUSED"}
    _gate(out, "TRAIN_COMPLETE", "PASS")
    store = _store(out)
    proc = hd.build_process(store)
    kb = json.loads((out / "stages" / "KB" / "KB_RECORD.json").read_text(encoding="utf-8"))
    sel = json.loads(Path(C["known_cases"]["KB0"]["selection_json"]["path"]).read_text("utf-8"))
    hws = hd.hws_store_digests()["digests"]
    t0 = time.process_time()
    return hs.eval_core(
        out,
        hc.REAL_PLAN,
        proc,
        store,
        recs,
        hws,
        sel["p_D2a"],
        Fraction(kb["Z_bound_w_star"]),
        hc.STUDY_LEDGER,
        pause=lambda: pause_or_raise(out, "EVAL", t0, cont=cont),
        freeze_sha256=pf["freeze_sha256"],
    )


def run_close(out, reason) -> dict:
    rep = {
        "outcome": REFUSE,
        "licence": hg.licence({"outcome": REFUSE}, {}),
        "reason": reason,
        "label": "pilot, uncertified",
        "protocol_sha256": C["protocol_sha256"],
    }
    stage_records.write_new(Path(out) / "REPORT.json", rep)
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="hwsb_driver")
    ap.add_argument("cmd", choices=("kb", "train", "eval", "close", "dry", "freeze", "inventory"))
    for opt in (
        "--out",
        "--auth",
        "--sched",
        "--kb-accept",
        "--master",
        "--continue",
        "--reason",
        "--h-exec",
        "--dry-report",
        "--save",
        "--compare",
        "--threads",
    ):
        ap.add_argument(opt, default=None)
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else (hc.DRY_STORE if a.cmd == "dry" else hc.STORE)
    try:
        if a.cmd == "inventory":
            snap = inventory_snapshot()
            if a.save:
                stage_records.write_new(Path(a.save), snap)
                return 0
            diff = inventory_diff(json.loads(Path(a.compare).read_text(encoding="utf-8")), snap)
            print(json.dumps(diff, indent=1))
            return 0 if diff["ok"] else 3
        if a.cmd == "kb":
            if preflight(out, "KB", a.auth, a.sched)["refused"]:
                return 2
            res = hk.run_kb(out, a.auth, a.sched)
            return 0 if res["status"] == "PASS" else 3
        if a.cmd == "train":
            res = run_train(
                out,
                a.auth,
                a.sched,
                int(a.master),
                a.kb_accept,
                getattr(a, "continue"),
                int(a.threads or 1),
            )
        elif a.cmd == "eval":
            res = run_eval(out, a.auth, a.sched, getattr(a, "continue"))
        elif a.cmd == "close":
            res = run_close(out, a.reason or "")
        elif a.cmd == "dry":
            import hwsb_dry

            res = hwsb_dry.run_dry(out, a.sched)
        else:
            res = freeze(out, hc.REPO, a.h_exec, a.dry_report)
    except Paused:
        return 4
    except Exception as exc:  # noqa: BLE001  every failure is recorded as a STOP
        st, why = status_of(exc), f"{type(exc).__name__}: {exc}"
        hws_records.append_stage_event(
            out, {"event": "STOP", "stage": a.cmd, "status": st, "reason": why}
        )
        _gate(out, "STOP", st, reason=why)
        return 5 if st == REFUSE else 3
    return 2 if res.get("status") == "REFUSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
