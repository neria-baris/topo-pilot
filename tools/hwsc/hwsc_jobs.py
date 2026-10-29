"""HWSC E2 job (release B), the close record and the CLI (API.md §7.3, §11.4; split from
hwsc_driver by size, API erratum; re-exported by hwsc_driver)."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import argparse
import json
import time
from pathlib import Path

import c1_model
import hwsb_driver
import hwsb_records
import hwsc_bind
import hwsc_data
import hwsc_gates
import k4b_data
import k4b_driver
import k4b_fresh
import stage_records
from c1_records import C1GateFailure
from hwsc_records import (
    export_c, freeze_c, pause_or_raise_c, preflight, run_gates_c, s0, status_of)

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import LocalFSBackend

E2_GATES = ("RELEASE_B", "H1C_E2", "H2-FRESH", "T-PRE", "ENDPOINT")
STEPS = ("step5000", "step0")


def e2_context(out, rel, handoff, dry=False) -> dict:
    """Release-B context exactly as k4b_fresh.main assembles it (identity re-checked first)."""
    out = Path(out)
    ctx = {"release": rel, "reservation_path": out / cc.RESERVATION_FILE, "dry": dry}
    hwsc_gates.h1c(out, ctx, handoff, ArtifactStore(LocalFSBackend(out / "artifacts")),
                   stage="E2")
    proc, models = ctx["proc"], ctx["models"]
    tables = {s: k4b_fresh.load_recorded(out, "S3", hwsc_data.hist_name(s, 0, dry))
              for s in ("lgate", "cal", "val")}
    stored = k4b_fresh.load_recorded(out, "S4a", "ACTS_cal_b0.npz")
    frozen = k4b_fresh.load_frozen(out)

    def acts(canon32, j, s):
        return c1_model.activations(models[(j, s)],
                                    k4b_data.model_inputs(canon32, proc["perm"][j]))

    ctx.update(frozen, tables=tables, stored_cal_acts=stored,
               recompute_cal_acts=lambda: {f"{j}_{s}": acts(tables["cal"]["canon32"], j, s)
                                           for j in cc.MASTERS for s in STEPS})
    return ctx


def _fill(result) -> dict:
    d4 = ((result.get("controls") or {}).get("delta4_orc") or {}).get("all") or {}
    per = result.get("per_model") or {}
    return {"N": result.get("N"), "values": json.dumps({str(j): {"L": p.get("L"),
                                                                  "U": p.get("U")}
                                                        for j, p in per.items()}),
            "B4": (result.get("fresh_B4") or {}).get("point"),
            "delta4_orc": d4.get("point"), "delta4_orc_lower": d4.get("alpha_bound"),
            "delta4_orc_certified": d4.get("certified")}


def run_e2(out, auth, sched, release_path, session, dry=False, dry_continue=False) -> dict:
    out = Path(out)
    pf = preflight(out, "E2", auth, sched)
    if pf["refused"]:
        return pf
    handoff, ctx, t0 = cc.load_handoff(), {}, time.process_time()

    def g_release():
        ctx["release"] = k4b_fresh.require_release_b(out, release_path, session)
        return {"N": ctx["release"]["N"], "k": ctx["release"]["k"]}

    def g_identity():
        ctx.update(e2_context(out, ctx["release"], handoff, dry))
        ctx["test"] = hwsc_data.sample_test_c(out, ctx["proc"], ctx["release"],
                                              ctx["reservation_path"], dry)
        test = ctx["test"]
        ctx["test_acts"] = lambda j, s: c1_model.activations(
            ctx["models"][(j, s)], k4b_data.model_inputs(test["canon32"], ctx["proc"]["perm"][j]))
        return {"Z_bound": str(ctx["Z"]), "test_rows": int(len(test["canon32"]))}

    def paused(fn):
        def run():
            r = fn()
            pause_or_raise_c(out, "E2", t0, cc.STUDY_LEDGER, None,
                             int(ctx["release"]["k"]) if "release" in ctx else None)
            return r
        return run

    steps = [("RELEASE_B", g_release), ("H1C_E2", g_identity),
             ("H2-FRESH", lambda: hwsc_data.h2_fresh_c(out, ctx)),
             ("T-PRE", lambda: k4b_fresh.t_pre(out, ctx)),
             ("ENDPOINT", lambda: k4b_fresh.endpoint_gate(ctx))]
    with hwsc_bind.bound_stage_c():
        stage_records.record_gate(out, "BINDING_AUDIT", hwsc_bind.audit()["status"])
        recs = run_gates_c(out, [(g, paused(f)) for g, f in steps], dry_continue)
    if any(r["status"] != "PASS" for r in recs):
        return run_close(out, recs)
    result = ctx["result"]
    ann = hwsc_gates.annotations(result)
    oc = hwsc_gates.outcome(hwsc_gates.state_from_gates(stage_records.gates_so_far(out),
                                                        result=result))
    stage_records.record_gate(out, "OUTCOME", "PASS", outcome=oc["outcome"],
                              annotations=oc["annotations"])
    f = export_c(out, result, oc, ann, _fill(result))
    return {"status": "PASS", "outcome": oc, "result": str(f)}


def run_close(out, recs=None, reason=None) -> dict:
    out = Path(out)
    gates = stage_records.gates_so_far(out)
    l1 = out / "stages" / "E1" / "L1.json"
    st = hwsc_gates.state_from_gates(gates, cc.read_json(l1) if l1.is_file() else None)
    if reason and not any(st.values()):
        st["resource"] = reason
    oc = hwsc_gates.outcome(st)
    rec = {"outcome": oc, "licence": hwsc_gates.licence(oc, {}), "reason": reason,
           "gates": recs, "lineage_disclosure": cc.DISCLOSURE, "utc": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    d = out / "stages" / "CLOSE"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"CLOSE_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    stage_records.write_new(f, json.loads(json.dumps(rec, default=str)))
    k4b_driver.complete_stage(out, "CLOSE", [f])
    return {"status": oc["outcome"], "outcome": oc, "record": str(f)}


def _load(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if p else None


def _exit(res) -> int:
    if res.get("refused"):
        return 2
    s = str(res.get("status", "PASS"))
    if s == "PASS" or s in ("SUPPORT", "EXCLUSION", "MIXED") or s == "COMPLETE":
        return 0
    return 3 if s.startswith("FAIL_TECHNICAL") else 5


def main(argv=None) -> int:
    import hwsc_driver as hdr

    ap = argparse.ArgumentParser(prog="hwsc_driver")
    ap.add_argument("cmd", choices=("s0", "kc", "train", "obs-inventory", "e1", "reg2", "e2",
                                    "close", "dry", "freeze", "inventory"))
    for opt in ("--out", "--auth", "--sched", "--kc-accept", "--master", "--release", "--accept",
                "--session", "--task-sha256", "--mailbox", "--continue", "--reason", "--h-exec",
                "--r-ref", "--dry-report", "--pf-record", "--run-approval", "--save",
                "--compare", "--job"):
        ap.add_argument(opt, default=None)
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else (cc.DRY_STORE if a.cmd == "dry" else cc.STORE)
    auth, sched = _load(a.auth), _load(a.sched)
    try:
        if a.cmd == "inventory":
            snap = hwsb_records.inventory_snapshot(cc.ROOT)
            if a.save:
                stage_records.write_new(Path(a.save), snap)
                return 0
            diff = hwsb_records.inventory_diff(_load(a.compare), snap)
            print(json.dumps(diff, indent=1))
            return 0 if diff["ok"] else 3
        if a.cmd == "s0":
            r = s0(cc.REPO, a.r_ref, a.h_exec)
            print(json.dumps(r, indent=1))
            return 0 if r["status"] == "PASS" else 2
        if a.cmd == "freeze":
            freeze_c(out, cc.REPO, a.h_exec, a.dry_report, a.pf_record, a.run_approval)
            return 0
        if a.cmd == "dry":
            import hwsc_dry

            return 0 if hwsc_dry.run_dry(out, sched).get("all_pass") else 3
        if a.cmd == "kc":
            res = hdr.run_kc(out, auth, sched, a.job)
        elif a.cmd == "train":
            res = hdr.run_train(out, auth, sched, int(a.master), _load(a.kc_accept), a.__dict__[
                "continue"])
        elif a.cmd == "obs-inventory":
            hdr.obs_inventory(out)
            return 0
        elif a.cmd == "e1":
            res = hdr.run_e1(out, auth, sched, a.release, a.session, a.task_sha256,
                             a.__dict__["continue"])
        elif a.cmd == "reg2":
            res = hdr.run_reg2(out, auth, sched, _load(a.accept))
        elif a.cmd == "e2":
            res = run_e2(out, auth, sched, a.release, a.session)
        else:
            res = run_close(out, None, a.reason or "INCONCLUSIVE/RESOURCE_OR_AUTHORITY")
    except hwsb_driver.Paused:
        return 4
    except C1GateFailure as exc:
        print(f"{status_of(exc)}: {exc.reason}")
        return 3
    print(json.dumps(res, indent=1, default=str)[:4000])
    return _exit(res if isinstance(res, dict) else {})
