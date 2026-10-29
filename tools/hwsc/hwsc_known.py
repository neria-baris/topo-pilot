"""HWSC G0c and the known cases KC0-KC9 (API.md §5; protocol §4; rulings R-0176-G1, G2).
hwsc_driver is imported lazily inside g0c and run_kc (the hwsb_known.kb0 pattern)."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import importlib
import os
import re
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import hwsb_kb
import hwsb_known
import hwsc_bind
import hwsc_data
import hwsc_gates
import hwsc_registry
import k4b_cert
import k4b_config
import k4b_data
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore, SeedTree
from topo_pilot.contracts.backends import LocalFSBackend

KNOWN, AUTH_REFUSE = "FAIL_TECHNICAL/KNOWN_CASE", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
TEXT_SUFFIXES = (".json", ".jsonl", ".md", ".py", ".txt", ".yaml")
SKIP_DIRS = {".git", ".venv", "__pycache__", "sealed"}


# --------------------------------------------------------------------------- G0c (R-0176-G2)
def needle_in(needle, line) -> bool:
    if not needle.isdigit():
        return needle in line
    return re.search(rf"(?<![0-9A-Za-z_]){re.escape(needle)}(?![0-9A-Za-z_])", line) is not None


def _skip_dir(parent, name, groot) -> bool:
    low = name.lower()
    docs = low == "research_summary" and parent.name.lower() == "docs"
    return (name in SKIP_DIRS or low.startswith("00_read_me_first") or docs
            or cc.blinded(parent / name, groot))


def seed_search_c(root, needles, root_for_guard=None) -> list:
    groot, hits = Path(root_for_guard or root), []
    for folder, dirs, files in os.walk(root, topdown=True):
        here = Path(folder)
        dirs[:] = sorted(d for d in dirs if not _skip_dir(here, d, groot))
        for name in sorted(files):
            low = name.lower()
            if low.startswith("00_read_me_first") or not low.endswith(TEXT_SUFFIXES):
                continue
            if cc.blinded(here / name, groot):
                continue
            with open(here / name, encoding="utf-8", errors="replace") as handle:
                for i, line in enumerate(handle, 1):
                    found = [nd for nd in needles if needle_in(nd, line)]
                    hits += [{"path": str(here / name), "needle": nd, "line": i} for nd in found]
    return hits


def classify_hits_c(hits, fragments=None, job_scratch=None) -> dict:
    s = cc.CONTRACT["seeds"]
    return hwsb_known.classify_hits(
        hits, s["g0_declaration_fragments"] if fragments is None else fragments,
        s["g0_job_scratch"] if job_scratch is None else job_scratch, label="hwsc_declaration")


def _sha_ok(path, want) -> bool | None:
    p = Path(path)
    if not p.is_file():
        return None
    return stage_records.sha256(cc.guard(p)) == want


def g0c(out, stage, auth=None, sched=None, release=None, root=cc.ROOT, mailbox=cc.MAILBOX) -> dict:
    import hwsc_driver as hdr

    out, root, a = Path(out), Path(root), cc.CONTRACT["authority"]
    checks = {}
    for k in a["kc0_addenda"]:
        ok = _sha_ok(root / a["owner_addenda"][k]["path"], a["owner_addenda"][k]["sha256"])
        if ok is None:
            raise C1GateFailure(AUTH_REFUSE, f"addendum {k} absent")
        if not ok:
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", f"addendum {k} sha256")
        checks[f"addendum_{k}"] = True
    ra = a["run_approval"]
    if ra["path"] == "TO_FREEZE" or not (root / ra["path"]).is_file():
        raise C1GateFailure(AUTH_REFUSE, "no owner run approval")
    frz = cc.read_json(out / "FREEZE.json") if (out / "FREEZE.json").is_file() else {}
    sha = stage_records.sha256(root / ra["path"])
    if not (sha == ra["sha256"] == (auth or {}).get("run_approval_sha256")
            == frz.get("run_approval_sha256")):
        raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "run approval sha256")
    handoff = cc.load_handoff()
    hw = a["hwsb_freeze_json"]
    if handoff["freeze_sha256"] != hw["sha256"] or not _sha_ok(hw["path"], hw["sha256"]):
        raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "stage-B FREEZE binding")
    for name in ("selection_json", "hws_final_report"):
        if not _sha_ok(a[name]["path"], a[name]["sha256"]):
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", f"{name} sha256")
    res = classify_hits_c(seed_search_c(root, cc.NEEDLES))
    checks["lineage"] = hdr.lineage_c(out)  # D-0181-1: before G0C.json, which is recorded at stage end
    path = out / "stages" / stage / "G0C.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, res)
    if res["status"] != "PASS":
        raise C1GateFailure(res["status"], "G0c: seed-scope hits outside the declarations")
    sc = hdr.sched_ok(sched, stage)
    if not sc["ok"]:
        raise C1GateFailure(AUTH_REFUSE, f"SCHED: {sc['reason']}")
    if release is not None:
        need = ("w3_attestation", "kreg1_reservation", "seed_hits", "kreg1_certificate",
                "train_records", "obs_inventory_sha256")
        missing = [k for k in need if release.get(k) is None]
        if missing:
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"release A lacks {missing}")
        rh = classify_hits_c(release["seed_hits"])
        if rh["status"] != "PASS":
            raise C1GateFailure(rh["status"], "release A seed hits")
        eq = k4b_config.check_chart_equality()
        if not (eq["equal"] and eq["giant_equal"] and eq["val_support_equal"]):
            raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"chart cfg differs: {eq}")
        checks["chart_equality"] = eq
    checks["seed_hits"] = len(res["hits"])
    return checks


# ------------------------------------------------------------------------------- KC1, KC4
def kc1(store, masters=cc.MASTERS) -> tuple:
    proc = hwsc_data.build_process_c(store, masters)
    r = hwsc_data.process_identity(store, proc)
    return proc, {"status": "PASS" if r["ok"] else KNOWN, "checks": r["checks"],
                  "ids": r["ids"], "spec_checksums": r["spec_checksums"],
                  "arrays_sha256": r["arrays_sha256"]}


def kc4(proc_w0, proc_star, handoff) -> dict:
    r = hwsb_known.kb4(proc_w0, proc_star)
    z = r["w_star"].get("Z_bound")
    z_ok = z is not None and Fraction(z) == handoff["Z_bound"]
    f_ok = k4b_cert.F_plan(handoff["Z_bound"]) == handoff["F_plan"] and z is not None and \
        k4b_cert.F_plan(Fraction(z)) == handoff["F_plan"]
    return dict(r, status="PASS" if r["status"] == "PASS" and z_ok and f_ok else KNOWN,
                z_equal=z_ok, F_plan_equal=f_ok)


# ----------------------------------------------------------------------------------- KC7
def _fixture():
    rng = np.random.default_rng(7)
    T = rng.dirichlet(np.ones(12), size=12)
    E = rng.dirichlet(np.ones(36), size=12)
    w, v = np.linalg.eig(T.T)
    pi = np.real(v[:, np.argmin(np.abs(w - 1))])
    pi = pi / pi.sum()
    r = np.random.default_rng(77)
    Xm = {j: r.normal(0.02, 0.1, 3072) for j in cc.MASTERS}
    Xp = {j: Xm[j] + np.abs(r.normal(0, 0.01, 3072)) for j in cc.MASTERS}
    r4 = {j: np.abs(r.normal(0.2, 0.05, 3072)) for j in cc.MASTERS}
    return T, E, pi, Xm, Xp, r4


def _identity_calls(T, E, pi) -> dict:
    import k4b_stats

    canon, ids = k4b_data.sample_block(T, E, pi, "cal", 0)
    t = k4b_data.history_table(canon, ids, "cal", 0)
    return {"status": k4b_stats.model_status(0.02, 0.03, Fraction(1, 10**4), Fraction(1, 10**4)),
            "overall": k4b_stats.overall({j: "EXCLUDE" for j in k4b_config.MODELS}),
            "F_plan": k4b_cert.F_plan(Fraction(1, 10**12)),
            "margin": k4b_cert.margin(Fraction(1, 10**8), Fraction(1, 10**12)),
            "canon": canon.tobytes(), "ids": ids.tobytes(), "digest": list(t["digest"])}


def kc7(table=None) -> dict:
    T, E, pi, Xm, Xp, r4 = _fixture()
    res = {}
    unbound = _identity_calls(T, E, pi)
    with hwsc_bind.bound_stage_c(hwsc_bind.load_table(which="identity")):
        res["a_identity"] = _identity_calls(T, E, pi) == unbound
    before = {(r["module"], r["name"]): getattr(importlib.import_module(r["module"]), r["name"])
              for r in hwsc_bind.load_table()}
    with hwsc_bind.bound_stage_c(table):
        au = hwsc_bind.audit()
        res["b_audit"] = au["status"] == "PASS"
        tops = {(h["module"], h["top"]) for h in au["hits"]}
        res["b_defaults_listed"] = {("k4b_stats", "sd_upper.__defaults__"),
                                    ("k4b_stats", "centered.__defaults__")} <= tops
        D = {j: 0.01 for j in cc.MASTERS}
        F = Fraction(1, 10**4)
        a = hwsc_gates.p1c_ladder(Xm, Xp, r4, F, D)
        import hwsb_gates

        b = hwsb_gates.ladder_pilot(Xm, Xp, r4, F, models=cc.MASTERS, seeds=cc.P1C_SEEDS,
                                    D_bar=D, ladder=cc.LADDER)
        res["b_p1c"] = a == b
        g1 = k4b_data.history_generator("cal", 0).integers(0, 2**63, 64)
        g2 = SeedTree(0).generator("data", "hwsc-v1", "cal", 0, "cylinder", "overlap",
                                   "1.75").integers(0, 2**63, 64)
        res["b_stream"] = bool(np.array_equal(g1, g2))
    res["c_restored"] = all(getattr(importlib.import_module(m), n) is obj
                            for (m, n), obj in before.items())
    return {"status": "PASS" if all(res.values()) else KNOWN, "checks": res,
            "audit_unlisted": au["unlisted"]}


# ------------------------------------------------------------------------------ KC8, KC9
def kc8(job) -> dict:
    base = cc.SCRATCH / f"test_hwsc-{job}"
    base.mkdir(parents=True, exist_ok=True)
    junit = base / "kc8.xml"
    env = dict(os.environ, PYTHONPATH=str(cc.REPO / "src"), TEMP=str(base / "tmp"),
               TMP=str(base / "tmp"), TMPDIR=str(base / "tmp"))
    (base / "tmp").mkdir(exist_ok=True)
    cmd = [sys.executable, "-s", "-m", "pytest", "tests/hwsc/test_a_k4b_known_bound.py",
           "-p", "no:cacheprovider", "-q", f"--junitxml={junit}", f"--basetemp={base / 'pytest'}"]
    rc = subprocess.run(cmd, cwd=cc.REPO, env=env, capture_output=True, text=True).returncode
    text = junit.read_text(encoding="utf-8") if junit.is_file() else ""

    def attr(name):
        m = re.search(rf'{name}="(\d+)"', text)
        return int(m.group(1)) if m else -1

    n, f, e = attr("tests"), attr("failures"), attr("errors")
    ok = rc == 0 and n >= 1 and f == 0 and e == 0
    return {"status": "PASS" if ok else KNOWN, "returncode": rc, "tests": n, "failures": f,
            "errors": e}


def kc9(out) -> dict:
    m = hwsc_registry.build("REHEARSAL", Path(out) / "registry" / "rehearsal",
                            handoff=cc.load_handoff())
    return {"status": "PASS" if m["status"] == "PASS" else KNOWN,
            "registry_status": m["status"], "cpu_s": m["cpu_s"],
            "peak_memory_bytes": m["peak_memory_bytes"], "n_digests": m["n_digests"],
            "problems": m["problems"]}


# ---------------------------------------------------------------------------------- run_kc
def run_kc(out, auth, sched, job, store=None) -> dict:
    import hwsb_known as hk
    import hwsc_driver as hdr

    out = Path(out)
    store = store or ArtifactStore(LocalFSBackend(out / "artifacts"))
    t0, rec, ctx = time.process_time(), {}, {}
    handoff = cc.load_handoff()

    def step(name):
        if name == "KC0":
            return dict(g0c(out, "KC", auth, sched), status="PASS")
        if name == "KC1":
            ctx["proc"], r = kc1(store)
            return r
        if name == "KC2":
            ctx["w0"] = hk.w0_process()
            ctx["k23"] = hk.kb2_kb3(ctx["w0"])
            return ctx["k23"]["KB2"]
        if name == "KC3":
            return ctx["k23"]["KB3"]
        if name == "KC4":
            ctx["kc4"] = kc4(ctx["w0"], ctx["proc"], handoff)
            return ctx["kc4"]
        if name == "KC5":
            return hwsb_kb.kb5(ctx["proc"])
        if name == "KC6":
            return hwsb_kb.kb6(ctx["w0"], ctx["k23"]["ckpt100"])
        if name == "KC7":
            with hwsc_bind.suspended():  # D-0184-1: run_kc runs inside the stage-C binding
                return kc7()
        if name == "KC8":
            return kc8(job)
        return kc9(out)

    status = "PASS"
    for name in cc.CONTRACT["known_cases"]["order"]:
        if status not in ("PASS", "PASS_WITH_NUMERIC_DRIFT"):
            rec[name] = {"status": "NOT_RUN"}
            stage_records.record_gate(out, name, "NOT_RUN")
            continue
        hdr.pause_or_raise_c(out, "KC", t0, cc.STUDY_LEDGER)
        try:
            r = step(name)
        except Exception as exc:  # noqa: BLE001  every KC failure is recorded, then stops
            s = hdr.status_of(exc)
            r = {"status": s if name == "KC0" else KNOWN, "reason": str(exc)[:2000]}
        rec[name] = hwsb_known.jsonable(r)
        if rec[name].get("status") not in ("PASS", "PASS_WITH_NUMERIC_DRIFT"):
            rec[name]["status"] = rec[name]["status"] if name == "KC0" else KNOWN
            status = rec[name]["status"]
        stage_records.record_gate(out, name, rec[name]["status"])
    w = hwsb_known.jsonable((ctx.get("kc4") or {}).get("w_star", {}))
    record = {"status": status, "kc": rec, "reading": (ctx.get("k23") or {}).get("reading"),
              "deviation_flags": rec.get("KC2", {}).get("deviation_flags", []),
              "process_ids": hwsb_known.jsonable(ctx["proc"]["ids"]) if "proc" in ctx else None,
              "arrays_sha256": rec.get("KC1", {}).get("arrays_sha256"), "law_w_star": w,
              "Z_bound_w_star": w.get("Z_bound") if isinstance(w, dict) else None,
              "F_plan": str(handoff["F_plan"]),
              "threads": {k: rec.get(k, {}).get("threads") for k in ("KC2", "KC3")},
              "torch": (ctx.get("k23") or {}).get("torch"),
              "binding_audit": rec.get("KC7", {}).get("checks"),
              "registry_rehearsal": rec.get("KC9"), "protocol_sha256": cc.PROTOCOL_SHA256,
              "freeze_sha256": stage_records.sha256(out / "FREEZE.json")
              if (out / "FREEZE.json").exists() else None}
    path = out / "stages" / "KC" / "KC_RECORD.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, record)
    return record
