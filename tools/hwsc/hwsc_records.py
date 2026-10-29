"""HWSC records: exception map, gate runner, lineage, authority, FREEZE, S0, budget, ledger and the
D6 export (API.md §7.1, §7.2, §7.3 export_c; split from hwsc_driver by size, API erratum; the
driver re-exports every name)."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import fnmatch
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import hwsb_config
import hwsb_driver
import hws_records
import k4b_config
import k4b_driver
import k4b_release
import stage_records
from c1_records import C1GateFailure, classify_exception

REFUSE, FREEZE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "FAIL_TECHNICAL/FREEZE"
C = cc.CONTRACT
RECORD_PATTERNS = ("AUTH_*.json", "SCHED_*.json", "ACCEPT_*.json", "DECISION_*.json")
EXTRA_RECORDS = ("FREEZE.json", "KC_ACCEPT.json", "RELEASE_A.json", "RELEASE_B.json",
                 cc.RESERVATION_FILE, "REGISTRY_OBLIGATION.json")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def status_of(exc) -> str:
    import hws_worlds

    from topo_pilot.contracts import ErrorCode, StageFailure

    if isinstance(exc, (C1GateFailure, hwsb_config.HwsbStop, hws_worlds.HwsStop)):
        s = str(exc.status)
    elif isinstance(exc, StageFailure) and exc.code == ErrorCode.NONFINITE_LOSS:
        s = "FAIL_TECHNICAL/NONFINITE"
    elif isinstance(exc, StageFailure) and exc.code == ErrorCode.SPLIT_OVERLAP:
        s = "FAIL_TECHNICAL/LINEAGE"
    elif isinstance(exc, hwsb_driver.Paused):
        return "PAUSE"
    else:
        s = str(classify_exception(exc)[0])
    return s if "/" in s else f"{s}/UNEXPECTED"


def run_gates_c(out, steps, dry_continue=False) -> list:
    recs, stopped = [], False
    for gate, fn in steps:
        if stopped and not dry_continue:
            stage_records.record_gate(Path(out), gate, "NOT_RUN")
            recs.append({"gate": gate, "status": "NOT_RUN"})
            continue
        try:
            details = fn() or {}
            status = details.pop("status", "PASS") if isinstance(details, dict) else "PASS"
        except Exception as exc:  # noqa: BLE001  every failure is recorded, then stops
            status = status_of(exc)
            details = {"reason": str(getattr(exc, "reason", exc))[:2000]}
            if status == "PAUSE":
                stage_records.record_gate(Path(out), gate, "NOT_RUN", **details)
                raise
        details = json.loads(json.dumps(details, default=str))
        stage_records.record_gate(Path(out), gate, status, **details)
        recs.append(dict(details, gate=gate, status=status))
        stopped = stopped or status != "PASS"
    return recs


def lineage_c(out) -> dict:
    out = Path(out)
    if not out.exists():
        return {"status": "PASS", "reason": "store absent"}
    recorded = set()
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            recorded |= {(k, v) for k, v in e.get("files", {}).items()}
    bad = k4b_release._superseded_ok(out) if (out / "superseded").is_dir() else []
    tops = set(k4b_release.RECORD_FILES) | set(EXTRA_RECORDS)
    for f in out.rglob("*"):
        if not f.is_file() or cc.blinded(f):
            continue
        rel = f.relative_to(out)
        top = rel.parts[0]
        if top == "superseded" or top in ("logs", "operations", "tmp") or top.startswith("tmp-"):
            continue
        if len(rel.parts) == 1 and (top in tops or any(fnmatch.fnmatch(top, p)
                                                       for p in RECORD_PATTERNS)):
            continue
        if rel.name.startswith(("HOLD_", "DECISION_")) or rel.as_posix() in (
                "tests/ACCEPTED.json",):
            continue
        if (rel.as_posix(), stage_records.sha256(f)) not in recorded:
            bad.append(rel.as_posix())
    if bad:
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"unrecorded files: {bad[:10]}")
    return {"status": "PASS", "n_recorded": len(recorded)}


def auth_ok(auth, stage, freeze=None) -> dict:
    if not isinstance(auth, dict):
        return {"ok": False, "reason": "no AUTH record"}
    sha34 = C["authority"]["owner_addenda"]["34"]["sha256"]
    reasons = []
    if stage not in auth.get("stages", []):
        reasons.append(f"stage {stage} not authorised")
    if auth.get("owner_auth_sha256") != sha34:
        reasons.append("owner_auth_sha256")
    if stage != "DRY" and (freeze is None or auth.get("run_approval_sha256")
                           != freeze.get("run_approval_sha256")):
        reasons.append("run_approval_sha256")
    return {"ok": not reasons, "reason": "; ".join(reasons)}


def sched_ok(sched, stage) -> dict:
    if not isinstance(sched, dict):
        return {"ok": False, "rule_w2": False, "rule_w3": False, "reason": "no SCHED record"}
    w2 = sched.get("live_history_reservations") == []
    w3 = sched.get("frozen_registries_awaiting_draw") == []
    ok = w2 if stage == "DRY" else (w2 and w3)
    return {"ok": ok, "rule_w2": w2, "rule_w3": w3, "reason": "" if ok else "W2/W3 rule"}


def _git(repo, *args) -> bytes:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, check=True).stdout


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def environment() -> dict:
    import numpy
    import torch

    return {"python": sys.version, "executable": sys.executable, "platform": platform.platform(),
            "numpy": numpy.__version__, "torch": torch.__version__}


def implementation_files(repo, h_exec) -> dict:
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/hwsc", "tests/hwsc")
    return {p: _sha(_git(repo, "show", f"{h_exec}:{p}"))
            for p in names.decode("utf-8").splitlines() if p}


def freeze_c(out, repo, h_exec, dry_report, pf_record, run_approval) -> dict:
    out, repo = Path(out), Path(repo)
    files = implementation_files(repo, h_exec)
    impl_sha = _sha(json.dumps(files, sort_keys=True).encode())
    reuse = {p: _sha(_git(repo, "show", f"{h_exec}:{p}")) for p in C["reuse_sha256"]}
    bad = [p for p, h in reuse.items() if C["reuse_sha256"][p] != h]
    if bad:
        raise C1GateFailure(FREEZE, f"reuse files differ at h_exec: {bad[:10]}")
    dry = json.loads(Path(dry_report).read_text(encoding="utf-8"))
    if dry.get("implementation_sha256") != impl_sha:
        raise C1GateFailure(FREEZE, "dry report implementation_sha256 differs")
    doc = {n: _sha(_git(repo, "show", f"{h_exec}:tools/hwsc/{f}"))
           for n, f in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                        ("test_plan_sha256", "TEST_PLAN.md"))}
    rec = dict(doc, protocol=C["protocol"], protocol_sha256=cc.PROTOCOL_SHA256, h_exec=h_exec,
               implementation_files=files, implementation_sha256=impl_sha, reuse_sha256=reuse,
               dry_run_report_sha256=stage_records.sha256(dry_report),
               dry_run_report_path=str(dry_report),
               pf_record_sha256=stage_records.sha256(pf_record),
               run_approval_sha256=stage_records.sha256(run_approval) if run_approval else None,
               environment=environment(), created_utc=utc())
    stage_records.write_new(out / "FREEZE.json", rec)
    return rec


def verify_freeze_c(out, repo=cc.REPO) -> dict:
    out, repo = Path(out), Path(repo)
    f = out / "FREEZE.json"
    if not f.is_file():
        raise C1GateFailure(REFUSE, "no FREEZE.json")
    frz = json.loads(f.read_text(encoding="utf-8"))
    bad = [p for p, h in frz["implementation_files"].items()
           if not (repo / p).is_file() or _sha((repo / p).read_bytes()) != h]
    for key, name in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                      ("test_plan_sha256", "TEST_PLAN.md")):
        if _sha((cc.HERE / name).read_bytes()) != frz[key]:
            bad.append(name)
    if _sha(cc.PROTOCOL_PATH.read_bytes()) != frz["protocol_sha256"]:
        bad.append("protocol")
    h = frz["h_exec"]
    if _git(repo, "diff", "--name-only", h, "--", *C["s0"]["protected_paths"]).strip():
        bad.append("protected paths differ from h_exec")
    if bad:
        raise C1GateFailure(FREEZE, f"FREEZE mismatch: {bad[:10]}")
    return {"status": "PASS", "freeze_sha256": stage_records.sha256(f), "freeze": frz}


def s0(repo, r_ref, h_exec) -> dict:
    s = C["s0"]
    diff = _git(repo, "diff", "--no-renames", "--name-status", r_ref, h_exec, "--",
                *s["protected_paths"]).decode("utf-8").splitlines()
    bad = [ln for ln in diff if ln.strip() and not (
        ln.split("\t")[0] == "A" and ln.split("\t")[-1].startswith(tuple(s["allowlist_prefixes"])))]
    mism = [p for p, h in C["reuse_sha256"].items()
            if _sha(_git(repo, "show", f"{h_exec}:{p}")) != h]

    def chart(ref):
        return json.loads(_git(repo, "show", f"{ref}:tools/c1prime/CONTRACT.json"))["chart"]

    proto = _sha(_git(repo, "show", f"{h_exec}:tools/hwsc/PROTOCOL_HWSC_v1.md"))
    ok = (not bad and not mism and chart(r_ref) == chart(h_exec) and proto == cc.PROTOCOL_SHA256
          and k4b_config.MARGIN == Fraction(1, 100))
    return {"status": "PASS" if ok else "INVALID", "offending": bad, "hash_mismatch": mism,
            "protocol_sha256": proto, "r_ref": r_ref, "h_exec": h_exec}


def preflight(out, stage, auth, sched, repo=cc.REPO) -> dict:
    try:
        frz = verify_freeze_c(out, repo)["freeze"]
    except C1GateFailure as exc:
        if exc.status != REFUSE:
            raise
        stage_records.record_gate(Path(out), "FREEZE", REFUSE, reason=exc.reason)
        return {"refused": True, "reason": exc.reason}
    stage_records.record_gate(Path(out), "FREEZE", "PASS")
    for gate, chk in (("AUTH", auth_ok(auth, stage, frz)), ("SCHED", sched_ok(sched, stage))):
        if not chk["ok"]:
            stage_records.record_gate(Path(out), gate, REFUSE, reason=chk["reason"])
            return {"refused": True, "reason": chk["reason"]}
        stage_records.record_gate(Path(out), gate, "PASS")
    return {"refused": False, "freeze": frz}


# ------------------------------------------------------------------------------ budget (§7.2)
def central(stage, k=None, R=None) -> float:
    if stage in ("E2", "REG2"):
        R = C["cpu"]["E2_planning"]["R"] if R is None else R
        return float(R) + 1720.1 * int(k or 1)
    return float(C["cpu"]["central_s"][stage])


def _cumulative(stage, k=None) -> float:
    if stage in ("E2", "REG2"):
        return float(C["cpu"]["cumulative_central_s"]["E1"]) + central("E2", k)
    return float(C["cpu"]["cumulative_central_s"][stage])


def pause_check_c(stage, stage_cpu, cum_cpu, k=None) -> dict:
    m = C["cpu"]["multiplier"]
    st, ct = m * central(stage, k), m * _cumulative(stage, k)
    bs, bc = stage_cpu > st, cum_cpu > ct
    trig = "BOTH" if bs and bc else "STAGE" if bs else "CUMULATIVE" if bc else None
    return {"pause": bs or bc, "trigger": trig, "stage_cpu": stage_cpu, "stage_threshold": st,
            "cum_cpu": cum_cpu, "cum_threshold": ct}


def ledger_read(path) -> dict:
    p = Path(path)
    if not p.exists():
        return {"study": "hwsc-v1", "entries": [], "cumulative_cpu_s": 0.0}
    return json.loads(p.read_text(encoding="utf-8"))


def ledger_append(path, label, job, stage, cpu_s, source, master=None) -> dict:
    p, led = Path(path), ledger_read(path)
    if any(e.get("label") == label for e in led["entries"]):
        raise C1GateFailure("FAIL_TECHNICAL/LEDGER", f"label {label} already in the ledger")
    led["entries"].append({"label": label, "job": job, "stage": stage, "cpu_s": float(cpu_s),
                           "source": str(source), "master": master, "utc": utc()})
    led["cumulative_cpu_s"] = float(sum(e["cpu_s"] for e in led["entries"]))
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return led


def pause_or_raise_c(out, stage, t0, ledger_path=None, cont=None, k=None) -> None:
    if ledger_path is None:
        return
    c = json.loads(Path(cont).read_text(encoding="utf-8")) if cont else {}
    if stage in c.get("stages", []):
        return
    led_stage = "E2" if stage == "REG2" else stage
    sc, cum = hwsb_driver.running_cpu(led_stage, ledger_path=ledger_path, t0=t0)
    chk = pause_check_c(stage, sc, cum, k)
    if chk["pause"]:
        hws_records.append_stage_event(Path(out), {"event": "PAUSE", "stage": stage,
                                                   "check": chk})
        stage_records.record_gate(Path(out), f"PAUSE_{stage}", "PAUSE", **chk)
        raise hwsb_driver.Paused(f"{stage}: {chk['trigger']}")


# ------------------------------------------------------------------------------- export (D6)
def export_c(out, result, oc, ann, fill) -> Path:
    import hwsc_gates

    out = Path(out)
    d = out / "stages" / "S8"
    d.mkdir(parents=True, exist_ok=True)
    sealed = out / "SEALED_VALIDATION.json"
    if not sealed.is_file():
        raise C1GateFailure("FAIL_TECHNICAL/SEALING", "SEALED_VALIDATION.json absent")
    body = dict(result, outcome=oc["outcome"], outcome_detail=oc, annotations=ann,
                licence=hwsc_gates.licence(oc, fill), lineage_disclosure=cc.DISCLOSURE,
                does_not_establish=C["licences"]["does_not_establish"],
                protocol_sha256=cc.PROTOCOL_SHA256)
    f = d / "RESULT.json"
    stage_records.write_new(f, json.loads(json.dumps(body, default=str)))
    g = d / "SEALED_OPENED.json"
    stage_records.write_new(g, json.loads(sealed.read_text(encoding="utf-8")))
    k4b_driver.complete_stage(out, "S8", [f, g])
    return f
