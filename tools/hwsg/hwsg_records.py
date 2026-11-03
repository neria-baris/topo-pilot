"""HWSG records: preflight, S0, FREEZE, lineage, ledger, outcome, terminal RESULT, export,
release barrier (API.md §9; protocol §7.1 S0/PF/WIN, §10.3). Stage-C record code is reused."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import fnmatch
import hashlib
import json
import os
import time
from fractions import Fraction
from pathlib import Path

import hwsc_outcome
import hwsc_records
import k4b_config
import k4b_driver
import stage_records
from c1_records import C1GateFailure
from hwsc_records import (  # noqa: F401  (reused unchanged)
    environment, record_gate_files, run_gates_c, status_of, superseded_ok, utc)

REFUSED, BAD, FREEZE = "REFUSED", gc.BAD, "FAIL_TECHNICAL/BINDING"
C = gc.CONTRACT
RECORD_PATTERNS = ("AUTH_*.json", "SCHED_*.json", "ACCEPT_*.json", "RELEASE_*.json",
                   "RESERVATION_*.json", "DECISION_*.json")
RECORD_NAMES = ("FREEZE.json", "KC_ACCEPT.json", "OPERATION_ACTIVE.json",
                "REGISTRY_OBLIGATION.json", "WORLD_HANDOFF.json", "REG1_CERTIFICATE.json",
                "GATES.jsonl", "STAGES.jsonl", "cpu_ledger.json", "SEALED_VALIDATION.json")
FREE_DIRS = ("logs", "operations", "tmp")
_G_INC = ("INCONCLUSIVE/REGISTRY_RISK", "INCONCLUSIVE/ORACLE_FEASIBILITY",
          "INCONCLUSIVE/REGISTRY_INCOMPLETE")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------------- lineage
def lineage_g(out) -> dict:
    out = Path(out)
    if not out.exists():
        return {"status": "PASS", "reason": "store absent"}
    saved = hwsc_records.RECORD_PATTERNS, hwsc_records.EXTRA_RECORDS
    hwsc_records.RECORD_PATTERNS = RECORD_PATTERNS
    hwsc_records.EXTRA_RECORDS = RECORD_NAMES
    n = 0
    try:
        for wd in sorted(p for p in (out / "worlds").glob("*") if p.is_dir()):
            n += hwsc_records.lineage_c(wd)["n_recorded"]
    finally:
        hwsc_records.RECORD_PATTERNS, hwsc_records.EXTRA_RECORDS = saved
    recorded, bad = set(), []
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            recorded |= set(e.get("files", {}).items())
    for f in out.rglob("*"):
        if not f.is_file() or gc.blinded(f):
            continue
        rel = f.relative_to(out)
        top = rel.parts[0]
        if top in ("worlds", "superseded") or top in FREE_DIRS or top.startswith("tmp-"):
            continue
        if len(rel.parts) == 1 and (top in RECORD_NAMES or any(
                fnmatch.fnmatch(top, p) for p in RECORD_PATTERNS)):
            continue
        if (rel.as_posix(), stage_records.sha256(f)) not in recorded:
            bad.append(rel.as_posix())
    if bad:
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"unrecorded files: {bad[:10]}")
    return {"status": "PASS", "n_recorded": n + len(recorded)}


# ------------------------------------------------------------------------- authority, window
def auth_ok(auth, stage, freeze=None) -> dict:
    if not isinstance(auth, dict):
        return {"ok": False, "reason": "no AUTH record"}
    want = C["authority"]["addendum_sha256"]["43"]
    reasons = []
    if stage not in auth.get("stages", []):
        reasons.append(f"stage {stage} not authorised")
    if auth.get("owner_auth_sha256") != want:
        reasons.append("owner_auth_sha256")
    fsha = freeze.get("freeze_sha256") if isinstance(freeze, dict) else freeze
    if stage != "DRY" and (not fsha or auth.get("freeze_sha256") != fsha):
        reasons.append("freeze_sha256")
    return {"ok": not reasons, "reason": "; ".join(reasons)}


def window_ok(sched, root=None, stage=None, own=None) -> dict:
    root = Path(gc.ROOT if root is None else root)
    reasons = []
    if not isinstance(sched, dict):
        return {"ok": False, "reason": "no SCHED record"}
    for f in sorted(root.glob("*/OPERATION_ACTIVE.json")):
        if own is not None and f.parent.resolve() == Path(own).resolve():
            continue
        try:
            if gc.read_json(f, root).get("active") is True:
                reasons.append(f"active operation in {f.parent.name}")
        except Exception:  # noqa: BLE001
            reasons.append(f"unreadable {f.parent.name}/OPERATION_ACTIVE.json")
    if sched.get("track_u_real_finished") is not True:
        reasons.append("track U real stages not finished")
    if sched.get("frozen_registries_awaiting_draw") != []:
        reasons.append("a frozen registry awaits its draw")
    return {"ok": not reasons, "reason": "; ".join(reasons)}


def verify_freeze_g(out, repo=None) -> dict:
    out, repo = Path(out), Path(gc.REPO if repo is None else repo)
    f = out / "FREEZE.json"
    if not f.is_file():
        raise C1GateFailure("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "no FREEZE.json")
    frz = json.loads(f.read_text(encoding="utf-8"))
    bad = [p for p, h in frz["implementation_files"].items()
           if not (repo / p).is_file() or _sha((repo / p).read_bytes()) != h]
    for key, name in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                      ("test_plan_sha256", "TEST_PLAN.md"),
                      ("protocol_sha256", "PROTOCOL_HWSG_v1.md")):
        if _sha((gc.HERE / name).read_bytes()) != frz[key]:
            bad.append(name)
    bad += [p for p, h in C["reuse_sha256"].items()
            if (repo / p).is_file() and _sha((repo / p).read_bytes()) != h]
    if bad:
        raise C1GateFailure(FREEZE, f"FREEZE mismatch: {bad[:10]}")
    return {"status": "PASS", "freeze_sha256": stage_records.sha256(f), "freeze": frz}


def preflight(out, stage, auth, sched, repo=None) -> dict:
    out = Path(out)
    try:
        v = verify_freeze_g(out, repo)
    except C1GateFailure as exc:
        if exc.status != "INCONCLUSIVE/RESOURCE_OR_AUTHORITY":
            raise
        stage_records.record_gate(out, "FREEZE", REFUSED, reason=exc.reason)
        return {"refused": True, "reason": exc.reason}
    stage_records.record_gate(out, "FREEZE", "PASS")
    own = out
    for gate, chk in (("AUTH", auth_ok(auth, stage, v)),
                      ("WINDOW", window_ok(sched, gc.ROOT, stage, own))):
        if not chk["ok"]:
            stage_records.record_gate(out, gate, REFUSED, reason=chk["reason"])
            return {"refused": True, "reason": chk["reason"]}
        stage_records.record_gate(out, gate, "PASS")
    return {"refused": False, "freeze": v["freeze"]}


# --------------------------------------------------------------------------- S0, FREEZE
def _git(repo, *args) -> bytes:
    return hwsc_records._git(repo, *args)


def s0(repo, r_ref, h_exec) -> dict:
    allow = tuple(C["s0"]["protected_allowlist"])
    diff = _git(repo, "diff", "--no-renames", "--name-status", r_ref, h_exec).decode().splitlines()
    bad = [ln for ln in diff if ln.strip() and not (
        ln.split("\t")[0] in ("A", "M") and ln.split("\t")[-1].startswith(allow))]
    mism = [p for p, h in C["reuse_sha256"].items()
            if _sha(_git(repo, "show", f"{h_exec}:{p}")) != h]

    def chart(ref):
        return json.loads(_git(repo, "show", f"{ref}:tools/c1prime/CONTRACT.json"))["chart"]

    def show(path):
        return json.loads(_git(repo, "show", f"{h_exec}:{path}"))

    checks = {
        "protocol": _sha(_git(repo, "show", f"{h_exec}:tools/hwsg/PROTOCOL_HWSG_v1.md"))
        == gc.PROTOCOL_SHA,
        "request": len(str(C["request_sha256"])) == 64,
        "diff_allowlist": not bad, "reuse": not mism,
        "margin": k4b_config.MARGIN == Fraction(1, 100),
        "chart_equal": chart(r_ref) == chart(h_exec) and bool(
            k4b_config.check_chart_equality()["equal"]),
        "recipe": show("tools/hwsb/CONTRACT.json")["recipe"]
        == show("tools/hwsc/CONTRACT.json")["recipe"]}
    return {"status": "PASS" if all(checks.values()) else "INVALID", "checks": checks,
            "offending": bad, "hash_mismatch": mism, "r_ref": r_ref, "h_exec": h_exec}


def freeze_g(out, repo, h_exec, dry_report, pf_record) -> dict:
    out, repo = Path(out), Path(repo)
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/hwsg",
                 "tests/hwsg").decode().splitlines()
    files = {p: _sha(_git(repo, "show", f"{h_exec}:{p}")) for p in names if p}
    impl = _sha(json.dumps(files, sort_keys=True).encode())
    reuse = {p: _sha(_git(repo, "show", f"{h_exec}:{p}")) for p in C["reuse_sha256"]}
    bad = [p for p, h in reuse.items() if C["reuse_sha256"][p] != h]
    if bad:
        raise C1GateFailure(FREEZE, f"reuse files differ at h_exec: {bad[:10]}")
    dry = json.loads(Path(dry_report).read_text(encoding="utf-8"))
    if dry.get("implementation_sha256") != impl:
        raise C1GateFailure(FREEZE, "dry report implementation_sha256 differs")
    doc = {n: _sha(_git(repo, "show", f"{h_exec}:tools/hwsg/{f}"))
           for n, f in (("contract_sha256", "CONTRACT.json"), ("api_sha256", "API.md"),
                        ("test_plan_sha256", "TEST_PLAN.md"),
                        ("protocol_sha256", "PROTOCOL_HWSG_v1.md"))}
    rec = dict(doc, protocol=C["protocol"], h_exec=h_exec, implementation_files=files,
               implementation_sha256=impl, reuse_sha256=reuse,
               dry_run_report_sha256=stage_records.sha256(dry_report),
               pf_record_sha256=stage_records.sha256(pf_record), environment=environment(),
               created_utc=utc())
    stage_records.write_new(out / "FREEZE.json", rec)
    return rec


# ----------------------------------------------------------------------------- ledger, budget
def ledger_read(path) -> dict:
    p = Path(path)
    if not p.exists():
        return {"study": "hwsg-v1", "entries": [], "cumulative_cpu_s": 0.0}
    return json.loads(p.read_text(encoding="utf-8"))


def ledger_append(path, label, job, stage, cpu_s, source, world=None, master=None) -> dict:
    p, led = Path(path), ledger_read(path)
    if any(e.get("label") == label for e in led["entries"]):
        raise C1GateFailure("FAIL_TECHNICAL/LEDGER", f"label {label} already in the ledger")
    led["entries"].append({"label": label, "job": job, "stage": stage, "world": world,
                           "master": master, "cpu_s": float(cpu_s), "source": str(source),
                           "utc": utc()})
    led["cumulative_cpu_s"] = float(sum(e["cpu_s"] for e in led["entries"]))
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return led


def central(stage, k=None) -> float:
    if stage == "E2":
        return 900.0 * int(k or 1) + 100.0
    return float(C["cpu"]["central_s"][stage])


def meter_caps(stage, k=None) -> dict:
    if stage == "TRAIN_child":
        cpu = float(C["cpu"]["train_child_max_cpu_s"])
    else:
        cpu = float(C["cpu"]["max_cpu_multiplier"]) * central(stage, k)
    wall = C["cpu"]["central_wall_s"]
    wall_s = None
    if isinstance(wall, dict) and stage in wall:
        wall_s = float(C["cpu"]["max_wall_multiplier"]) * float(wall[stage])
    return {"max_cpu": cpu, "max_wall": wall_s}


def output_cap(kind) -> int:
    return int(C["resources"]["output_cap_bytes_" + {"world": "world",
                                                     "registry": "registry"}[kind]])


def marker_replace(path, obj, retries=5, sleep_s=0.2) -> None:
    path = Path(path)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for i in range(int(retries)):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if i == int(retries) - 1:
                raise
            time.sleep(sleep_s)


# ------------------------------------------------------------------ outcome, licence, results
def outcome_g(state) -> dict:
    k = state.get("k4b")
    if k in _G_INC and not state.get("fail") and not state.get("resource"):
        return {"outcome": k, "label": k, "k": None, "models": state.get("models"),
                "criterion": state.get("criterion"), "annotations": [], "pbm": None}
    return hwsc_outcome.outcome(state)


def licence_g(oc, fill, world) -> str:
    fill = dict(fill or {}, world=world)
    head = oc["outcome"]
    if head in ("SUPPORT", "EXCLUSION"):
        text = C["licences"][head].format_map(hwsc_outcome._Fill(fill))
        pbm = oc.get("pbm") or {}
        if pbm.get("models"):
            text += " " + hwsc_outcome.LIC["POSITIVE_BELOW_MARGIN"].format_map(
                hwsc_outcome._Fill(fill, models=", ".join(str(m) for m in pbm["models"])))
        return text
    return hwsc_outcome.licence(oc, fill)


def terminal_result(world_dir, w, status, stage, gate, details, p1_passed) -> Path:
    d = gc.world(w)
    wd = Path(world_dir)
    oc = {"outcome": status, "label": status, "k": None, "models": None, "criterion": gate,
          "annotations": [], "pbm": None}
    body = {"world": d.key, "outcome": status, "label": status, "stage": stage, "gate": gate,
            "details": json.loads(json.dumps(details, default=str)), "annotations": [],
            "licence": licence_g(oc, {}, d.key), "lineage_disclosure": gc.DISCLOSURE,
            "protocol_sha256": gc.PROTOCOL_SHA, "p1_passed": bool(p1_passed)}
    f = wd / "stages" / "TERMINAL" / "RESULT.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, {k: body[k] for k in C["records"]["TERMINAL_RESULT"]})
    k4b_driver.complete_stage(wd, "TERMINAL", [f])
    return f


def export_g(world_dir, result, oc, ann, fill, ratio_files) -> Path:
    wd = Path(world_dir)
    d = wd / "stages" / "S8"
    d.mkdir(parents=True, exist_ok=True)
    sealed = wd / "SEALED_VALIDATION.json"
    if not sealed.is_file():
        raise C1GateFailure("FAIL_TECHNICAL/SEALING", "SEALED_VALIDATION.json absent")
    key = wd.name
    body = dict(result, world=key, outcome=oc["outcome"], outcome_detail=oc, annotations=ann,
                licence=licence_g(oc, fill, key), lineage_disclosure=gc.DISCLOSURE,
                does_not_establish=C["licences"]["does_not_establish"],
                protocol_sha256=gc.PROTOCOL_SHA)
    f = d / "RESULT.json"
    stage_records.write_new(f, json.loads(json.dumps(body, default=str)))
    g = d / "SEALED_OPENED.json"
    stage_records.write_new(g, json.loads(sealed.read_text(encoding="utf-8")))
    k4b_driver.complete_stage(wd, "S8", [f, g] + [Path(p) for p in ratio_files])
    return f


def _accepted(path, keys, want) -> bool:
    if not Path(path).is_file():
        return False
    rec = json.loads(Path(path).read_text(encoding="utf-8"))
    return any(rec.get(k) == want for k in keys) and rec.get("verdict", "ACCEPT") != "REJECT"


def release_barrier(store) -> dict:
    worlds, missing_b = {}, []
    for tag in gc.TAGS:
        wd = gc.world_dir(store, tag)
        term, val = wd / "stages/TERMINAL/RESULT.json", wd / "stages/S5/VALIDATION_REPORT.json"
        t_ok = term.is_file() and _accepted(
            wd / "ACCEPT_TERMINAL.json", ("terminal_result_sha256", "result_sha256", "sha256"),
            stage_records.sha256(term))
        v_ok = val.is_file() and _accepted(
            wd / "ACCEPT_VALIDATION.json", ("validation_report_sha256", "sha256"),
            stage_records.sha256(val))
        worlds[tag] = {"terminal": t_ok, "validation": v_ok}
        if v_ok and not (wd / "RELEASE_B.json").is_file():
            missing_b.append(tag)
    return {"ok": all(w["terminal"] or w["validation"] for w in worlds.values()),
            "worlds": worlds, "release_b_missing": missing_b}
