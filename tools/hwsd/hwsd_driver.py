"""HWSD driver: common job helpers and the jobs KD, SAMPLE, CLOSE, inventory (API.md §11, §15.1,
§15.2). SCORE, SUMMARY and the CLI live in hwsd_jobs (split by size, API erratum) and are
re-exported here under their API names. Every job runs its gates inside one bound_hwsd()."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import json
import time
from fractions import Fraction
from pathlib import Path

import hwsb_records
import hwsc_config
import hwsc_data
import hwsc_gates
import hwsd_bind
import hwsd_data
import hwsd_known
import hwsd_records
import hwsd_registry
import k4b_cert
import k4b_driver
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import LocalFSBackend

REFUSE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


def _files_under(d) -> set:
    d = Path(d)
    return {p for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()


def audit_gate(out) -> None:
    a = hwsd_bind.audit()
    stage_records.record_gate(Path(out), "BINDING_AUDIT", a["status"], n_hits=a["n_hits"],
                              unlisted=[f"{h['module']}.{h['top']}" for h in a["unlisted"]])
    if a["status"] != "PASS":
        raise C1GateFailure(a["status"], "binding audit")


def run_gates_d(out, steps, soft=()) -> list:
    """hwsc_records.run_gates_c, except that a gate named in `soft` records its status and does
    not stop the job (B4-TEST, decision 9)."""
    recs, stopped = [], False
    for gate, fn in steps:
        if stopped:
            stage_records.record_gate(Path(out), gate, "NOT_RUN")
            recs.append({"gate": gate, "status": "NOT_RUN"})
            continue
        try:
            details = fn() or {}
            status = details.pop("status", "PASS") if isinstance(details, dict) else "PASS"
        except Exception as exc:  # noqa: BLE001  every failure is recorded, then stops
            status = hwsd_records.status_of(exc)
            details = {"reason": str(getattr(exc, "reason", exc))[:2000]}
            if status == "PAUSE":
                stage_records.record_gate(Path(out), gate, "PAUSE", **details)
                raise
        details = json.loads(json.dumps(details, default=str))
        stage_records.record_gate(Path(out), gate, status, **details)
        recs.append(dict(details, gate=gate, status=status))
        stopped = stopped or (status != "PASS" and gate not in soft)
    return recs


def paused(out, stage, t0, fn, cont=None):
    def run():
        r = fn()
        hwsd_records.pause_or_raise_d(out, stage, t0, dc.STUDY_LEDGER, cont)
        return r
    return run


def end_obligation(out, job, attempt, reservation_id=None) -> Path:
    name = f"REGISTRY_OBLIGATION_{job}-a{attempt}.json"
    if (Path(out) / name).exists():
        return Path(out) / name
    return hwsd_data.write_obligation(out, name, job, attempt, hwsd_records.utc(),
                                      reservation_id=reservation_id)[0]


def refuse_exit(out, ret, job, attempt):
    """J10 item 2: a refused job that wrote anything into the store still writes its obligation."""
    out = Path(out)
    if out.is_dir() and any(out.iterdir()):
        end_obligation(out, job, attempt)
    return ret


def first_bad(recs, soft=()):
    return next((r["status"] for r in recs if r["status"] != "PASS" and r["gate"] not in soft),
                "PASS")


# ----------------------------------------------------------------------------------- KD job
def run_kd(out, auth, sched, job, attempt=1) -> dict:
    out = Path(out)
    pf = hwsd_records.preflight_d(out, "KD", auth, sched)
    if pf["refused"]:
        return refuse_exit(out, pf, job, attempt)
    with hwsd_bind.bound_hwsd():
        audit_gate(out)
        return hwsd_known.run_kd(out, auth, sched, job, attempt)


# -------------------------------------------------------------------------------- SAMPLE job
def _kd_accept_ok(out, kd_accept) -> bool:
    kd = Path(out) / "stages" / "KD" / "KD_RECORD.json"
    return bool(isinstance(kd_accept, dict) and kd_accept.get("accept") is True and kd.is_file()
                and kd_accept.get("kd_record_sha256") == stage_records.sha256(kd)
                and dc.read_json(kd).get("status") == "PASS")


def _h1d(out, ctx) -> dict:
    handoff, before = hwsc_config.load_handoff(), _files_under(Path(out) / "artifacts")
    ident = hwsd_known.ident_d(handoff=handoff)
    store = ArtifactStore(LocalFSBackend(Path(out) / "artifacts"))
    proc = hwsc_data.build_process_c(store)
    pid = hwsc_data.process_identity(store, proc)
    bad = "FAIL_TECHNICAL/IDENTITY"
    if not pid["ok"]:
        raise C1GateFailure(bad, json.dumps(pid["checks"], default=str)[:2000])
    ids = json.loads(json.dumps(proc["ids"], default=str))
    for j in dc.MASTERS:
        if dc.read_train_record(j)[1]["process_ids"] != ids:
            raise C1GateFailure(bad, f"process ids differ from TRAIN record {j}")
    law = hwsc_gates.law_identity(proc, handoff)
    result = dc.read_json(dc.HWSC_STORE / "stages" / "S8" / "RESULT.json")
    z = law["Z_bound"]
    if not (z == handoff["Z_bound"] == Fraction(dc.CONTRACT["identity"]["Z_bound"])
            == Fraction(str(result["Z_bound"]))):
        raise C1GateFailure("FAIL_TECHNICAL/LAW_BOUND", "Z_bound differs")
    if k4b_cert.F_plan(z) != handoff["F_plan"]:
        raise C1GateFailure(bad, "F_plan differs")
    pd = hwsc_data.p_d2a_check(proc, handoff["p_D2a"])
    if not pd["ok"]:
        raise C1GateFailure(bad, f"p_D2a rel diff {pd.get('rel_diff')}")
    import c1_cert
    import torch

    selftest, threads = c1_cert.a1_selftest(), torch.get_num_threads()
    if threads != 1:
        raise C1GateFailure(bad, f"{threads} threads")
    rec = {"identity": ident, "process_identity": {"ok": pid["ok"], "checks": pid["checks"]},
           "Z_bound": str(z), "F_plan": str(handoff["F_plan"]), "p_D2a": pd,
           "a1_selftest": selftest, "threads": threads}
    d = Path(out) / "stages" / "SAMPLE"
    d.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(d / "H1D.json", json.loads(json.dumps(rec, default=str)))
    ctx.update(proc=proc, Z=z, p_d2a=pd["p_D2a"], handoff=handoff, new_artifacts=sorted(
        _files_under(Path(out) / "artifacts") - before))
    return {"Z_bound": str(z), "threads": threads}


def _regd(out, ctx, root, scratch) -> dict:
    out = Path(out)
    try:
        w = hwsd_registry.build_d(out / "registry", root, scratch, ctx["handoff"])
    finally:  # whatever was written enters the lineage record
        files = sorted(_files_under(out / "registry"))
        if files:
            k4b_driver.complete_stage(out, "REGD", files)
    if w["status"] != "PASS":
        raise C1GateFailure(w["status"], "; ".join(map(str, w.get("problems", [])))[:2000])
    return {"inner_status": w["inner_status"]}


def _close_res(out, ctx, job, attempt) -> None:
    """J8: the obligation right after the four tables, then the reservation end (new code)."""
    out, rid, utc = Path(out), ctx["rid"], hwsd_records.utc()
    p = out / "REGISTRY_OBLIGATION.json"
    if not p.exists():
        p = hwsd_data.write_obligation(out, "REGISTRY_OBLIGATION.json", job, attempt, utc,
                                       reservation_id=rid)[0]
    if not ctx.get("ended"):
        hwsd_data.end_reservation(out, rid, utc, p)
        ctx["ended"] = True


def _s3d(out, ctx, job, attempt) -> dict:
    out, rid = Path(out), ctx["rid"]
    res = hwsd_data.reservation_path(out, attempt)
    v = hwsd_data.verify_reservation_d(res, rid)
    if v["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"reservation: {v.get('reason')}")
    k4b_driver.begin_stage(out, "S3")
    ctx["rows"] = True
    try:
        tables = hwsd_data.sample_tables(ctx["proc"])
        paths = hwsd_data.save_tables(out, tables)
        k4b_driver.complete_stage(out, "S3", paths)
        ctx["tables"] = tables
        v2 = hwsd_data.verify_reservation_d(res, rid, True)
    finally:
        _close_res(out, ctx, job, attempt)
    if v2["status"] != "PASS":
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"reservation breach: {v2.get('reason')}")
    return {"rows": {s: len(t["seq_ids"]) for s, t in tables.items()}}


def _h2d(out, ctx) -> dict:
    reg = hwsd_registry.load_d(Path(out))
    sep = hwsd_data.separation_d(reg, ctx["tables"])
    risk = hwsd_data.registry_risk_d(ctx["p_d2a"])
    stage_records.write_new(Path(out) / "stages" / "SAMPLE" / "H2D.json",
                            json.loads(json.dumps({"separation": sep, "risk": risk},
                                                  default=str)))
    if sep["status"] != "PASS":
        raise C1GateFailure(sep["status"], "H2-D separation")
    if not risk["ok"]:
        raise C1GateFailure("INCONCLUSIVE/REGISTRY_INCOMPLETE", f"registry risk {risk['value']}")
    return {"risk": risk["value"]}


def _oracle(out, ctx) -> dict:
    out, proc, t = Path(out), ctx["proc"], ctx["tables"]
    o = hwsd_data.oracle_d(proc, t)
    d = out / "stages" / "S4"
    files = hwsd_data.save_oracle(out, o["moments"])
    test_sha = stage_records.sha256(out / "stages" / "S3" / hwsd_data.hist_name("test"))
    f1, f2 = d / "REFS_test.json", d / "ORACLE_D.json"
    stage_records.write_new(f1, hwsd_data.refs_to_json(o["refs_test"], proc, test_sha))
    stage_records.write_new(f2, {"max_gap": o["max_gap"], "n_checked": o["n_checked"]})
    k4b_driver.complete_stage(out, "S4", files + [f1, f2])
    ctx["o"], ctx["eps"] = o, k4b_cert.envelopes()
    return {"max_gap": o["max_gap"], "n_checked": o["n_checked"]}


def _b4(out, ctx) -> dict:
    out, o = Path(out), ctx["o"]
    m, canon = o["moments"]["test"], ctx["tables"]["test"]["canon32"]
    g = hwsd_data.b4_test(m, o["refs_test"], ctx["eps"], ctx["Z"])
    d = out / "stages" / "S4"
    f = d / "B4_TEST.json"
    stage_records.write_new(f, json.loads(json.dumps(g, default=str)))
    shared = hwsd_data.shared_controls(m, canon)
    bounds = k4b_cert.control_bounds_all(shared, o["refs_test"], ctx["eps"])
    ctx["s4_files"] = [f] + hwsd_data.save_shared(out, shared, bounds)
    return {"status": g["status"], "B4": str(g.get("lower"))}


def _lgate(out, ctx) -> dict:
    p = hwsd_data.save_lgate_q(Path(out), hwsd_data.lgate_oracle(
        ctx["proc"], ctx["tables"]["lgate"]["canon32"]))
    ctx["s4_files"].append(p)
    return {}


def run_sample(out, auth, sched, job, attempt, kd_accept, root=dc.ROOT,
               scratch=dc.SCRATCH) -> dict:
    out, ctx, t0 = Path(out), {}, time.process_time()
    pf = hwsd_records.preflight_d(out, "SAMPLE", auth, sched)
    if pf["refused"]:
        return refuse_exit(out, pf, job, attempt)
    with hwsd_bind.bound_hwsd():
        audit_gate(out)
        if not _kd_accept_ok(out, kd_accept):
            stage_records.record_gate(out, "KD_ACCEPT", REFUSE)
            return refuse_exit(out, {"refused": True, "reason": "KD_ACCEPT"}, job, attempt)
        stage_records.record_gate(out, "KD_ACCEPT", "PASS")

        def reservation():
            a = hwsd_data.w2_attest(root)
            d = out / "stages" / "SAMPLE"
            d.mkdir(parents=True, exist_ok=True)
            stage_records.write_new(d / "W2.json", json.loads(json.dumps(a, default=str)))
            if a["status"] != "PASS":
                raise C1GateFailure("INCONCLUSIVE/AUTHORITY", "W2 attestation")
            _, rec = hwsd_data.start_reservation_d(out, attempt, hwsd_records.utc())
            ctx["rid"] = rec["id"]
            return {"reservation": rec["id"]}

        def b(fn):
            return paused(out, "SAMPLE", t0, fn)

        steps = [("G0D", b(lambda: hwsd_known.g0d(out, "SAMPLE", auth, sched, root))),
                 ("RESERVATION", b(reservation)), ("H1D", b(lambda: _h1d(out, ctx))),
                 ("REGD", b(lambda: _regd(out, ctx, root, scratch))),
                 ("S3D", b(lambda: _s3d(out, ctx, job, attempt))),
                 ("H2D", b(lambda: _h2d(out, ctx))),
                 ("ORACLE-D", b(lambda: _oracle(out, ctx))),
                 ("B4-TEST", b(lambda: _b4(out, ctx))),
                 ("LGATE-ORACLE", b(lambda: _lgate(out, ctx)))]
        try:
            recs = run_gates_d(out, steps, soft=("B4-TEST",))
        finally:
            if ctx.get("rid") and not ctx.get("rows") and not ctx.get("ended"):
                hwsd_data.stop_obligation(out, job, attempt, ctx["rid"], hwsd_records.utc())
                ctx["ended"] = True
            hwsd_records.record_gate_files(out, "SAMPLE", ("G0D.json", "H1D.json", "H2D.json",
                                                           "W2.json"))
            new = ctx.get("new_artifacts")
            if new:
                k4b_driver.complete_stage(out, "SAMPLE", new)
            if ctx.get("s4_files"):
                k4b_driver.complete_stage(out, "S4", ctx["s4_files"])
            end_obligation(out, job, attempt, ctx.get("rid"))
    return {"status": first_bad(recs, ("B4-TEST",)), "gates": recs}


# ---------------------------------------------------------------------- CLOSE and inventory
def state_from_gates(out) -> dict:
    """The outcome_d state keys (decision 10) read from GATES.jsonl and the SCORE folders."""
    st = {"fail": None, "resource": False, "registry": False, "headroom": False, "partial": []}
    for g in stage_records.gates_so_far(Path(out)):
        s = str(g.get("status"))
        if s.startswith("FAIL_TECHNICAL") and st["fail"] is None:
            st["fail"] = s
        elif s in ("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "INCONCLUSIVE/AUTHORITY",
                   "INCONCLUSIVE/RESOURCE", "PAUSE"):
            st["resource"] = s
        elif s == "INCONCLUSIVE/REGISTRY_INCOMPLETE":
            st["registry"] = s
        elif g.get("gate") == "B4-TEST" and s.startswith("INCONCLUSIVE"):
            st["headroom"] = s
    st["partial"] = [j for j in dc.MASTERS if (
        Path(out) / "stages" / "SCORE" / str(j) / "ACCEPTANCE.json").is_file()]
    return st


def run_close(out, status, reason, job, attempt) -> dict:
    import hwsd_summary

    out = Path(out)
    st = state_from_gates(out)
    if status and not any((st["fail"], st["resource"], st["registry"], st["headroom"])):
        if str(status).startswith("FAIL_TECHNICAL"):
            st["fail"] = status
        else:
            st["resource"] = str(status)
    oc = hwsd_summary.outcome_d(st)
    f = out / "stages" / "CLOSE" / "CLOSE.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, json.loads(json.dumps({"outcome": oc, "reason": reason},
                                                     default=str)))
    k4b_driver.complete_stage(out, "CLOSE", [f])
    end_obligation(out, job, attempt)
    return {"status": oc["outcome"], "outcome": oc, "record": str(f)}


def inventory(root, save=None, compare=None) -> dict:
    snap = hwsb_records.inventory_snapshot(
        root, tuple(dc.CONTRACT["registry"]["deep_scan_exclude"]))
    if save:
        stage_records.write_new(Path(save), snap)
    if compare is not None:
        before = compare if isinstance(compare, dict) else json.loads(
            Path(compare).read_text(encoding="utf-8"))
        return hwsb_records.inventory_diff(before, snap)
    return snap


from hwsd_jobs import main, run_score, run_summary  # noqa: E402,F401  (split by size)

if __name__ == "__main__":
    raise SystemExit(main())
