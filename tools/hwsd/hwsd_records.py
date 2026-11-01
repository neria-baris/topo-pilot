"""HWSD records: lineage, AUTH/SCHED, FREEZE, S0, preflight, budget and pauses, ledger, H-1
checks and archive (API.md §10, §19). Reused hwsc_records names are re-exported (called through
the module at call time)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import fnmatch
import json
import re
import time
from fractions import Fraction
from pathlib import Path

import hwsb_driver
import hws_records
import hwsc_records
import k4b_config
import k4b_release
import stage_records
from c1_records import C1GateFailure

REFUSE, FREEZE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "FAIL_TECHNICAL/FREEZE"
RECORD_FILES_D = frozenset(k4b_release.RECORD_FILES) | {
    "FREEZE.json", "KD_ACCEPT.json", "ACCEPT_SAMPLE.json", "REGISTRY_OBLIGATION.json"}
RECORD_PATTERNS_D = ("AUTH_*.json", "SCHED_*.json", "ACCEPT_*.json", "DECISION_*.json",
                     "REGISTRY_OBLIGATION_*.json")
FREE_FOLDERS_D = ("logs", "operations", "tmp")
RES_NAME = re.compile(r"RES-HWSD-W2-a\d+(\.END)?\.json")

# reused unchanged (called through the module at call time)
status_of = hwsc_records.status_of
utc = hwsc_records.utc


def run_gates_c(*a, **k):
    return hwsc_records.run_gates_c(*a, **k)


def superseded_ok(out):
    return hwsc_records.superseded_ok(out)


def sched_ok(sched, stage):
    return hwsc_records.sched_ok(sched, stage)


def record_gate_files(out, stage, names):
    return hwsc_records.record_gate_files(out, stage, names)


def ledger_append(*a, **k):
    return hwsc_records.ledger_append(*a, **k)


# ------------------------------------------------------------------------------------ lineage
def lineage_d(out) -> dict:
    out = Path(out)
    if not out.exists():
        return {"status": "PASS", "reason": "store absent"}
    recorded = set()
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            recorded |= {(k, v) for k, v in e.get("files", {}).items()}
    bad = superseded_ok(out) if (out / "superseded").is_dir() else []
    for f in out.rglob("*"):
        if not f.is_file() or dc.blinded(f):
            continue
        rel = f.relative_to(out)
        top = rel.parts[0]
        if top == "reservations":
            if len(rel.parts) != 2 or not RES_NAME.fullmatch(rel.name):
                bad.append(rel.as_posix())
            continue
        if top == "superseded" or top in FREE_FOLDERS_D or top.startswith("tmp-"):
            continue
        if len(rel.parts) == 1 and (top in RECORD_FILES_D or any(
                fnmatch.fnmatch(top, p) for p in RECORD_PATTERNS_D)):
            continue
        if rel.name.startswith(("HOLD_", "DECISION_")) or rel.as_posix() == "tests/ACCEPTED.json":
            continue
        if (rel.as_posix(), stage_records.sha256(f)) not in recorded:
            bad.append(rel.as_posix())
    if bad:
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"unrecorded files: {bad[:10]}")
    return {"status": "PASS", "n_recorded": len(recorded)}


# ------------------------------------------------------------------------- authority, FREEZE
def auth_ok_d(auth, stage, freeze=None) -> dict:
    if not isinstance(auth, dict):
        return {"ok": False, "reason": "no AUTH record"}
    sha = dc.CONTRACT["authority"]["owner_addenda"]["37"]["sha256"]
    reasons = []
    if stage not in auth.get("stages", []):
        reasons.append(f"stage {stage} not authorised")
    if auth.get("owner_auth_sha256") != sha:
        reasons.append("owner_auth_sha256")
    if stage != "DRY" and (freeze is None or auth.get("run_approval_sha256")
                           != freeze.get("run_approval_sha256")):
        reasons.append("run_approval_sha256")
    return {"ok": not reasons, "reason": "; ".join(reasons)}


def _git(repo, *args) -> bytes:
    return hwsc_records._git(repo, *args)


def _sha(data: bytes) -> str:
    return hwsc_records._sha(data)


def implementation_files_d(repo, h_exec) -> dict:
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/hwsd", "tests/hwsd")
    return {p: _sha(_git(repo, "show", f"{h_exec}:{p}"))
            for p in names.decode("utf-8").splitlines() if p}


def freeze_d(out, repo, h_exec, dry_report, pf_record, kd4_params, run_approval) -> dict:
    out, repo, C = Path(out), Path(repo), dc.CONTRACT
    files = implementation_files_d(repo, h_exec)
    impl_sha = _sha(json.dumps(files, sort_keys=True).encode())
    reuse = {p: _sha(_git(repo, "show", f"{h_exec}:{p}")) for p in C["reuse_sha256"]}
    bad = [p for p, h in reuse.items() if C["reuse_sha256"][p] != h]
    if bad:
        raise C1GateFailure(FREEZE, f"reuse files differ at h_exec: {bad[:10]}")
    dry = json.loads(Path(dry_report).read_text(encoding="utf-8"))
    if dry.get("implementation_sha256") != impl_sha:
        raise C1GateFailure(FREEZE, "dry report implementation_sha256 differs")
    doc = {n: _sha(_git(repo, "show", f"{h_exec}:tools/hwsd/{f}"))
           for n, f in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                        ("test_plan_sha256", "TEST_PLAN.md"))}
    rec = dict(doc, protocol=C["protocol"], protocol_sha256=dc.PROTOCOL_SHA256, h_exec=h_exec,
               implementation_files=files, implementation_sha256=impl_sha, reuse_sha256=reuse,
               dry_run_report_sha256=stage_records.sha256(dry_report),
               dry_run_report_path=str(dry_report),
               pf_record_sha256=stage_records.sha256(pf_record),
               kd4_parameters_sha256=stage_records.sha256(kd4_params),
               run_approval_sha256=stage_records.sha256(run_approval) if run_approval else None,
               environment=hwsc_records.environment(), created_utc=utc())
    stage_records.write_new(out / "FREEZE.json", rec)
    return rec


def verify_freeze_d(out, repo=dc.REPO) -> dict:
    out, repo = Path(out), Path(repo)
    f = out / "FREEZE.json"
    if not f.is_file():
        raise C1GateFailure(REFUSE, "no FREEZE.json")
    frz = json.loads(f.read_text(encoding="utf-8"))
    bad = [p for p, h in frz["implementation_files"].items()
           if not (repo / p).is_file() or _sha((repo / p).read_bytes()) != h]
    for key, name in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                      ("test_plan_sha256", "TEST_PLAN.md")):
        if _sha((dc.HERE / name).read_bytes()) != frz[key]:
            bad.append(name)
    if _sha(dc.PROTOCOL_PATH.read_bytes()) != frz["protocol_sha256"]:
        bad.append("protocol")
    if _git(repo, "diff", "--name-only", frz["h_exec"], "--",
            *dc.CONTRACT["s0"]["protected_paths"]).strip():
        bad.append("protected paths differ from h_exec")
    if bad:
        raise C1GateFailure(FREEZE, f"FREEZE mismatch: {bad[:10]}")
    return {"status": "PASS", "freeze_sha256": stage_records.sha256(f), "freeze": frz}


def s0_d(repo, r_ref, h_exec) -> dict:
    s, C = dc.CONTRACT["s0"], dc.CONTRACT
    diff = _git(repo, "diff", "--no-renames", "--name-status", r_ref, h_exec, "--",
                *s["protected_paths"]).decode("utf-8").splitlines()
    bad = [ln for ln in diff if ln.strip() and not (
        ln.split("\t")[0] == "A" and ln.split("\t")[-1].startswith(tuple(s["allowlist_prefixes"])))]
    mism = [p for p, h in C["reuse_sha256"].items()
            if _sha(_git(repo, "show", f"{h_exec}:{p}")) != h]

    def chart(ref):
        return json.loads(_git(repo, "show", f"{ref}:tools/c1prime/CONTRACT.json"))["chart"]

    proto = _sha(_git(repo, "show", f"{h_exec}:tools/hwsd/PROTOCOL_HWSD_v1.md"))
    ok = (not bad and not mism and chart(r_ref) == chart(h_exec) and proto == dc.PROTOCOL_SHA256
          and k4b_config.MARGIN == Fraction(1, 100))
    return {"status": "PASS" if ok else "INVALID", "offending": bad, "hash_mismatch": mism,
            "protocol_sha256": proto, "r_ref": r_ref, "h_exec": h_exec}


def preflight_d(out, stage, auth, sched, repo=dc.REPO) -> dict:
    try:
        frz = verify_freeze_d(out, repo)["freeze"]
    except C1GateFailure as exc:
        if exc.status != REFUSE:
            raise
        stage_records.record_gate(Path(out), "FREEZE", REFUSE, reason=exc.reason)
        return {"refused": True, "reason": exc.reason}
    stage_records.record_gate(Path(out), "FREEZE", "PASS")
    for gate, chk in (("AUTH", auth_ok_d(auth, stage, frz)), ("SCHED", sched_ok(sched, stage))):
        if not chk["ok"]:
            stage_records.record_gate(Path(out), gate, REFUSE, reason=chk["reason"])
            return {"refused": True, "reason": chk["reason"]}
        stage_records.record_gate(Path(out), gate, "PASS")
    return {"refused": False, "freeze": frz}


# ------------------------------------------------------------------------- budget and pauses
def central_d(stage) -> float:
    if stage not in dc.CONTRACT["cpu"]["central_s"]:
        raise ValueError(f"unknown stage {stage}")
    return float(dc.CONTRACT["cpu"]["central_s"][stage])


def cumulative_d(stage) -> float:
    if stage not in dc.CONTRACT["cpu"]["cumulative_central_s"]:
        raise ValueError(f"unknown stage {stage}")
    return float(dc.CONTRACT["cpu"]["cumulative_central_s"][stage])


def pause_check_d(stage, stage_cpu, cum_cpu, job_cpu=None) -> dict:
    st, ct = 3 * central_d(stage), 3 * cumulative_d(stage)
    mt = 3 * float(dc.CONTRACT["cpu"]["score_per_model_central_s"]) if stage == "SCORE" else None
    conds = [("STAGE", stage_cpu > st), ("CUMULATIVE", cum_cpu > ct),
             ("MODEL", stage == "SCORE" and job_cpu is not None and job_cpu > mt)]
    names = [n for n, b in conds if b]
    return {"pause": bool(names), "trigger": "+".join(names) or None, "stage_cpu": stage_cpu,
            "stage_threshold": st, "cum_cpu": cum_cpu, "cum_threshold": ct, "job_cpu": job_cpu,
            "model_threshold": mt}


def pause_or_raise_d(out, stage, t0, ledger_path=None, cont=None) -> None:
    if ledger_path is None:
        return
    c = json.loads(Path(cont).read_text(encoding="utf-8")) if cont else {}
    if stage in c.get("stages", []):
        return
    sc, cum = hwsb_driver.running_cpu(stage, ledger_path=ledger_path, t0=t0)
    chk = pause_check_d(stage, sc, cum, time.process_time() - t0)
    if chk["pause"]:
        hws_records.append_stage_event(Path(out), {"event": "PAUSE", "stage": stage,
                                                   "check": chk})
        stage_records.record_gate(Path(out), f"PAUSE_{stage}", "PAUSE", **chk)
        raise hwsb_driver.Paused(f"{stage}: {chk['trigger']}")


def ledger_init(path) -> dict:
    p = Path(path)
    if not p.exists():
        stage_records.write_new(p, {"study": "hwsd-v1", "entries": [], "cumulative_cpu_s": 0.0})
    led = json.loads(p.read_text(encoding="utf-8"))
    if led.get("study") != "hwsd-v1":
        raise C1GateFailure("FAIL_TECHNICAL/LEDGER", f"ledger study {led.get('study')}")
    return led


def ledger_append_d(path, label, job, stage, cpu_s, source, master=None) -> dict:
    ledger_init(path)
    if stage not in dc.CONTRACT["cpu"]["stage_order"]:
        raise ValueError(f"unknown stage {stage}")
    return ledger_append(path, label, job, stage, cpu_s, source, master)


# --------------------------------------------------------------------------- H-1 and archive
def no_value_check(obj) -> None:
    keys = set(dc.CONTRACT["records"]["value_keys"])
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys:
                raise C1GateFailure("FAIL_TECHNICAL/SEALING", str(k))
            no_value_check(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            no_value_check(v)


def acceptance_check(rec) -> None:
    sp = dc.CONTRACT["records"]["SCORE_ACCEPTANCE"]

    def fail(msg):
        raise C1GateFailure("FAIL_TECHNICAL/SEALING", msg)

    if not isinstance(rec, dict) or set(rec) != set(sp["keys"]):
        fail("acceptance key set")
    c = rec["counts"]
    if (not isinstance(c, dict) or set(c) != set(sp["counts_keys"])
            or any(type(v) is not int for v in c.values()) or sum(c.values()) != 12):
        fail("acceptance counts")
    ft = rec["fail_technical"]
    if ft is not None and not (isinstance(ft, str) and ft.startswith("FAIL_TECHNICAL/")):
        fail("acceptance fail_technical")
    fs = rec["files_sha256"]
    if not isinstance(fs, dict) or any(
            not isinstance(k, str) or not isinstance(v, str)
            or not re.fullmatch(r"[0-9a-f]{64}", v) for k, v in fs.items()):
        fail("acceptance files_sha256")
    no_value_check(rec)


def archive_attempt_d(out, job, attempt, files, suffixes=None) -> Path:
    return k4b_release.archive_attempt(out, f"{job}-a{attempt}", files, suffixes)
