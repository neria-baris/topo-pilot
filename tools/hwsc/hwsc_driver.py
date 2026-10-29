"""HWSC driver: the jobs KC, TRAIN, E1, REG2, E2, close and the CLI (API.md §7.3, §11; protocol
§5, §8). Records, gate runner, budget and export live in hwsc_records (split by size) and are
re-exported here under their API names. Every stage function runs inside bound_stage_c()."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
import time
from pathlib import Path

import hwsb_registry
import hwsb_train
import hwsc_bind
import hwsc_data
import hwsc_gates
import hwsc_known
import hwsc_registry
import k4b_driver
import k4b_fresh
import k4b_release
import stage_records
from c1_records import C1GateFailure
from hwsc_records import (  # noqa: F401  (API names)
    auth_ok, central, export_c, freeze_c, implementation_files, ledger_append, ledger_read,
    lineage_c, pause_check_c, pause_or_raise_c, preflight, run_gates_c, s0, sched_ok, status_of,
    utc, verify_freeze_c)

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import LocalFSBackend

REFUSE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
E1_GATES = ("G0C", "H1C", "REG1", "H2", "L1", "ORACLE-VAL", "B4-VAL", "C0-CAL", "C0-VAL",
            "CERT-VAL", "P1")


def _store(out) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(out) / "artifacts"))


def _files_under(d) -> set:
    d = Path(d)
    return {p for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()


def _audit_gate(out) -> None:
    a = hwsc_bind.audit()
    stage_records.record_gate(Path(out), "BINDING_AUDIT", "PASS" if a["status"] == "PASS"
                              else a["status"], n_hits=a["n_hits"],
                              unlisted=[f"{h['module']}.{h['top']}" for h in a["unlisted"]])
    if a["status"] != "PASS":
        raise C1GateFailure(a["status"], "binding audit")


# ---------------------------------------------------------------------------------- KC job
def run_kc(out, auth, sched, job) -> dict:
    out = Path(out)
    pf = preflight(out, "KC", auth, sched)
    if pf["refused"]:
        return pf
    before = _files_under(out / "artifacts")
    with hwsc_bind.bound_stage_c():
        _audit_gate(out)
        rec = hwsc_known.run_kc(out, auth, sched, job)
    new = sorted(_files_under(out / "artifacts") - before)
    files = [out / "stages" / "KC" / "KC_RECORD.json"] + new
    g0 = out / "stages" / "KC" / "G0C.json"
    k4b_driver.complete_stage(out, "KC", files + ([g0] if g0.is_file() else []))
    return rec


# ------------------------------------------------------------------------------- TRAIN (§11.1)
def run_train(out, auth, sched, master, kc_accept, cont=None, plan=None) -> dict:
    out, master = Path(out), int(master)
    plan = cc.HWSC_PLAN if plan is None else plan
    pf = preflight(out, "TRAIN", auth, sched)
    if pf["refused"]:
        return pf
    kc = out / "stages" / "KC" / "KC_RECORD.json"
    acc = kc_accept or {}
    if not (acc.get("accept") is True and kc.is_file()
            and acc.get("kc_record_sha256") == stage_records.sha256(kc)
            and cc.read_json(kc).get("status") == "PASS"):
        stage_records.record_gate(out, "KC_ACCEPT", REFUSE)
        return {"refused": True, "reason": "KC_ACCEPT"}
    stage_records.record_gate(out, "KC_ACCEPT", "PASS")
    d = out / "stages" / "TRAIN" / str(master)
    if (d / "TRAIN_RECORD.json").exists():
        raise C1GateFailure("FAIL_TECHNICAL/RERUN", f"TRAIN_RECORD of {master} exists")
    t0 = time.process_time()
    pause_or_raise_c(out, "TRAIN", t0, cc.STUDY_LEDGER, cont)
    before = _files_under(out / "artifacts")
    rec = {"master": master, "status": "COMPLETE"}
    with hwsc_bind.bound_stage_c():
        _audit_gate(out)
        try:
            store = _store(out)
            proc = hwsc_data.build_process_c(store)
            w = cc.CONTRACT["world"]
            if (proc["ids"]["world"], proc["ids"]["transition"]) != (
                    w["WorldSpec"]["id"], w["TransitionSpec"]["id"]):
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "process ids")
            obs = hwsc_data.make_train_dev_c(store, proc, master, plan)
            threads = hwsb_train.set_threads(1)
            hold = hwsb_train.HoldRule(d, cap_s=cc.HOLD_S, steps=cc.STEPS, from_step=cc.HOLD_FROM)
            res = hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, master,
                                   plan=plan, hold=hold)
            rk = list(cc.run_key(plan, master))
            steps = list(plan.train_cfg.checkpoint_steps)
            if list(res["run_key"]) != rk or sorted(res["checkpoint_ids"]) != sorted(steps):
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "run key or checkpoint steps")
            if res["summary"]["steps_done"] != plan.train_cfg.steps:
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "steps_done")
            rec.update(run_key=rk, observation_ids={"train": obs["train"], "dev": obs["dev"]},
                       streams=obs["streams"], sequence_id_replicates=obs["replicates"],
                       checkpoint_ids={str(k): v for k, v in res["checkpoint_ids"].items()},
                       checksums={str(k): v for k, v in res["checksums"].items()},
                       summary=res["summary"], threads=threads, holds=res["holds"],
                       process_ids=proc["ids"],
                       dev_ce={str(k): v for k, v in res["dev_ce"].items()})
        except Exception as exc:  # noqa: BLE001  the record keeps the stop status
            rec.update(status=status_of(exc), reason=str(exc)[:2000])
    rec["process_cpu_s"] = time.process_time()
    d.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(d / "TRAIN_RECORD.json", json.loads(json.dumps(rec, default=str)))
    files = [d / "TRAIN_RECORD.json"] + sorted(p for p in d.iterdir() if p.name.startswith(
        ("HOLD_", "DECISION_"))) + sorted(_files_under(out / "artifacts") - before)
    k4b_driver.complete_stage(out, f"TRAIN_{master}", files)
    stage_records.record_gate(out, f"TRAIN_{master}", "PASS" if rec["status"] == "COMPLETE"
                              else rec["status"])
    if rec["status"] == "COMPLETE" and all(
            (out / "stages" / "TRAIN" / str(j) / "TRAIN_RECORD.json").is_file()
            for j in cc.MASTERS) and master == cc.MASTERS[-1]:
        obs_inventory(out)
    return rec


def obs_inventory(out) -> dict:
    out = Path(out)
    for j in cc.MASTERS:
        r = cc.read_json(out / "stages" / "TRAIN" / str(j) / "TRAIN_RECORD.json")
        if r.get("status") != "COMPLETE":
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"TRAIN {j} not COMPLETE")
    inv = hwsb_registry.history_inventory(out)
    f = out / "stages" / "TRAIN" / "OBS_INVENTORY.json"
    stage_records.write_new(f, inv)
    k4b_driver.complete_stage(out, "TRAIN_INVENTORY", [f])
    return inv


# ---------------------------------------------------------------------------------- E1 (§11.2)
def _reg(out, version, handoff, extra=None) -> dict:
    inv = cc.read_json(Path(out) / "stages" / "TRAIN" / "OBS_INVENTORY.json")
    reg_dir = Path(out) / "registry"
    k4b_driver.begin_stage(out, version.replace("K-", ""))
    m = hwsc_registry.build(version, reg_dir, handoff=handoff, own_expected=inv, extra=extra)
    files = [reg_dir / f"{version}.json", reg_dir / f"{version}_digests.npz"]
    files += sorted(_files_under(reg_dir / "runs" / version))
    k4b_driver.complete_stage(out, version.replace("K-", ""), files)
    return m


def e1_steps(out, ctx, handoff, auth, sched) -> list:
    out, store = Path(out), _store(out)

    def reg1():
        rel = ctx["release"]
        if rel.get("kreg1_certificate") is None:
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", "no completeness certificate")
        inv = out / "stages" / "TRAIN" / "OBS_INVENTORY.json"
        if stage_records.sha256(inv) != rel.get("obs_inventory_sha256"):
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "OBS_INVENTORY not bound")
        m = _reg(out, "K-REG1", handoff)
        if m["status"] != "PASS":
            raise C1GateFailure(m["status"], "; ".join(m["problems"])[:2000])
        import c2_registry

        ctx["reg1"] = c2_registry.Registry.load(out, "K-REG1")
        return {"n_digests": m["n_digests"], "digests_sha256": m["digests_sha256"]}

    fns = {"G0C": lambda: hwsc_known.g0c(out, "E1", auth, sched, ctx["release"]),
           "H1C": lambda: hwsc_gates.h1c(out, ctx, handoff, store),
           "REG1": reg1, "H2": lambda: hwsc_data.h2c(out, ctx),
           "L1": lambda: hwsc_gates.l1(out, ctx),
           "ORACLE-VAL": lambda: k4b_driver.oracle_val(out, ctx),
           "B4-VAL": lambda: k4b_driver.b4_val(out, ctx),
           "C0-CAL": lambda: k4b_driver.c0_cal_stage(out, ctx),
           "C0-VAL": lambda: k4b_driver.c0_val_stage(out, ctx),
           "CERT-VAL": lambda: k4b_driver.cert_val(out, ctx),
           "P1": lambda: hwsc_gates.p1c(out, ctx, handoff)}
    t0 = time.process_time()

    def paused(name, fn):
        def run():
            r = fn()
            pause_or_raise_c(out, "E1", t0, ctx.get("ledger"), ctx.get("cont"))
            return r
        return (name, run)

    return [paused(g, fns[g]) for g in E1_GATES]


def run_e1(out, auth, sched, release_path, session, task_sha256, cont=None,
           dry_continue=False) -> dict:
    out = Path(out)
    pf = preflight(out, "E1", auth, sched)
    if pf["refused"]:
        return pf
    rel = k4b_release.verify_release(release_path, "A", task_sha256, session, out / "FREEZE.json")
    if rel["reservation"] != cc.RESERVATION_ID:
        raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "release reservation id")
    handoff = cc.load_handoff()
    ctx = {"release": rel, "reservation_path": out / cc.RESERVATION_FILE, "handoff": handoff,
           "ledger": cc.STUDY_LEDGER, "cont": cont}
    with hwsc_bind.bound_stage_c():
        _audit_gate(out)
        recs = run_gates_c(out, e1_steps(out, ctx, handoff, auth, sched), dry_continue)
    if any(r["status"] != "PASS" for r in recs):
        return run_close(out, recs)
    return {"status": "PASS", "gates": recs}


# --------------------------------------------------------------------------------- REG2 (§11.3)
def run_reg2(out, auth, sched, accept) -> dict:
    out = Path(out)
    pf = preflight(out, "REG2", auth, sched)
    if pf["refused"]:
        return pf
    with hwsc_bind.bound_stage_c():
        _audit_gate(out)  # CONTRACT gates.REG2: BINDING_AUDIT before ACCEPT
    vr = out / "stages" / "S5" / "VALIDATION_REPORT.json"
    if not (isinstance(accept, dict) and accept.get("verdict") == "ACCEPT" and vr.is_file()
            and accept.get("validation_report_sha256") == stage_records.sha256(vr)):
        stage_records.record_gate(out, "ACCEPT", REFUSE)
        return {"refused": True, "reason": "ACCEPT"}
    stage_records.record_gate(out, "ACCEPT", "PASS")
    res = k4b_release.verify_reservation(out / cc.RESERVATION_FILE,
                                         {"reservation": cc.RESERVATION_ID})
    if res["status"] != "PASS":
        stage_records.record_gate(out, "REG2", "INCONCLUSIVE/AUTHORITY", reason=res["reason"])
        return {"refused": True, "reason": res["reason"]}
    t0 = time.process_time()
    with hwsc_bind.bound_stage_c():
        tabs = {s: k4b_fresh.load_recorded(out, "S3", hwsc_data.hist_name(s, 0))
                for s in ("lgate", "cal", "val")}
        m = _reg(out, "K-REG2", cc.load_handoff(), extra=tabs)
    stage_records.record_gate(out, "REG2", m["status"], n_digests=m["n_digests"])
    pause_or_raise_c(out, "REG2", t0, cc.STUDY_LEDGER)
    return m


from hwsc_jobs import e2_context, main, run_close, run_e2  # noqa: E402,F401  (split by size)

if __name__ == "__main__":
    raise SystemExit(main())
