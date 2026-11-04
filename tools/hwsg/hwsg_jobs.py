"""HWSG jobs: REG1, E1-w, REG2, E2-w and the CLI (API.md §11.4-§11.7). Every world stage runs
inside hwsg_bind.world(w); the stage-C gate functions are reused unchanged."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_bind
import hwsg_handoff
import hwsg_known
import hwsg_ratio
import hwsg_records as rec
import hwsg_registry
import argparse
import json
from pathlib import Path

import c1_model
import c2_registry
import hwsc_data
import hwsc_gates
import hwsc_jobs
import hwsc_known
import hwsc_outcome
import k4b_config
import k4b_data
import k4b_driver
import k4b_fresh
import k4b_release
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import LocalFSBackend

CACHE: dict = {}


def _store(wd) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(wd) / "artifacts"))


def _files_under(d) -> set:
    d = Path(d)
    return {p for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()


def _audit_gate(out, tag) -> None:
    a = hwsg_bind.audit(tag)
    stage_records.record_gate(Path(out), "BINDING_AUDIT", a["status"], n_hits=a["n_hits"],
                              unlisted=[f"{h['module']}.{h['top']}" for h in a["unlisted"]])
    if a["status"] != "PASS":
        raise C1GateFailure(a["status"], "binding audit")


# --------------------------------------------------------------------------- REG1 / REG2
def _registry_job(out, auth, sched, stage, version, extra=None, worlds=gc.TAGS) -> dict:
    out = Path(out)
    pf = rec.preflight(out, stage, auth, sched)
    if pf.get("refused"):
        return pf
    k4b_driver.begin_stage(out, stage)
    rd = out / "registry"
    m = hwsg_registry.build(version, rd, root=gc.ROOT, worlds=worlds, extra=extra)
    cert = rd / f"{version.replace('K-', '')}_CERTIFICATE.json"
    stage_records.write_new(cert, {"version": version, "certificate": m["certificate"],
                                   "status": m["status"],
                                   "manifest_sha256": stage_records.sha256(rd / f"{version}.json")})
    files = [rd / f"{version}.json", rd / f"{version}_digests.npz", cert]
    files += sorted(_files_under(rd / "runs" / version))
    k4b_driver.complete_stage(out, stage, files)
    stage_records.record_gate(out, stage, m["status"] if m["status"] == "PASS"
                              else "INCONCLUSIVE/REGISTRY_INCOMPLETE")
    return m


def run_reg1(out, auth, sched, job=None) -> dict:
    return _registry_job(out, auth, sched, "REG1", "K-REG1")


def _tables(out, tag, blocks=("lgate", "cal", "val")) -> dict:
    wd, tabs = gc.world_dir(out, tag), {}
    for s in blocks:
        f = wd / "stages" / "S3" / hwsc_data.hist_name(s, 0)
        if f.is_file():
            with np.load(f, allow_pickle=False) as z:
                tabs[s] = {k: np.asarray(z[k]) for k in z.files}
    return tabs


def run_reg2(out, auth, sched, job=None) -> dict:
    out = Path(out)
    bar = rec.release_barrier(out)
    if not bar["ok"]:
        stage_records.record_gate(out, "R2", "NO_RELEASE", worlds=bar["worlds"])
        return {"status": "NO_RELEASE", "barrier": bar}
    extra = {f"{t}:{s}": tab for t in gc.TAGS for s, tab in _tables(out, t).items()}
    return _registry_job(out, auth, sched, "REG2", "K-REG2", extra=extra)


# ------------------------------------------------------------------------------------ E1
def _g0g(wd, out, auth, sched, rel):
    w = rec.window_ok(sched, gc.ROOT, own=out)
    if not w["ok"]:
        raise C1GateFailure("REFUSED", w["reason"])
    res = hwsc_known.classify_hits_c(CACHE.setdefault("hits", hwsg_known.seed_search_g(
        gc.ROOT, gc.NEEDLES)), gc.CONTRACT["seeds"]["kg0_declaration_fragments"], [])
    if res["status"] != "PASS":
        raise C1GateFailure(gc.BAD, "seed-scope hits outside the declarations")
    need = ("kreg1_certificate", "train_records", "obs_inventory_sha256", "seed_hits")
    missing = [k for k in need if rel.get(k) is None]
    if missing:
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"release A lacks {missing}")
    eq = k4b_config.check_chart_equality()
    if not (eq["equal"] and eq["giant_equal"] and eq["val_support_equal"]):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"chart cfg differs: {eq}")
    return {"seed_hits": len(CACHE["hits"])}


def e1_steps(out, wd, tag, ctx, handoff, auth, sched) -> list:
    store = _store(wd)

    def reg1_load():
        rel = ctx["release"]
        reg = json.loads((Path(out) / "registry" / "K-REG1.json").read_text(encoding="utf-8"))
        if rel.get("kreg1_certificate") != reg.get("certificate"):
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "K-REG1 certificate not bound")
        hwsg_registry.recheck(reg)
        ctx["reg1"] = c2_registry.Registry.load(out, "K-REG1")
        return {"certificate": reg["certificate"]}

    def h2():
        r = hwsc_data.h2c(wd, ctx)
        others = {t: _tables(out, t) for t in gc.TAGS if t != tag and _tables(out, t)}
        cross = hwsg_registry.separation_g(ctx["reg1"], dict(others, **{tag: ctx["tables"]}))
        if cross["status"] != "PASS":
            raise C1GateFailure(cross["status"], json.dumps(cross, default=str)[:2000])
        return dict(r, cross_world=cross["cross_collisions"])

    fns = {"G0C": lambda: _g0g(wd, out, auth, sched, ctx["release"]),
           "H1G": lambda: hwsc_gates.h1c(wd, ctx, handoff, store),
           "REG1_LOAD": reg1_load, "H2": h2, "L1": lambda: hwsc_gates.l1(wd, ctx),
           "ORACLE-VAL": lambda: k4b_driver.oracle_val(wd, ctx),
           "B4-VAL": lambda: k4b_driver.b4_val(wd, ctx),
           "C0-CAL": lambda: k4b_driver.c0_cal_stage(wd, ctx),
           "C0-VAL": lambda: k4b_driver.c0_val_stage(wd, ctx),
           "CERT-VAL": lambda: k4b_driver.cert_val(wd, ctx),
           "P1": lambda: hwsc_gates.p1c(wd, ctx, handoff)}
    return [(g, fns[g]) for g in gc.CONTRACT["gates"]["order_E1"]]


def run_e1(out, w, auth, sched, release_path=None, session=None, task_sha256=None,
           dry_continue=False) -> dict:
    out, d = Path(out), gc.world(w)
    wd = gc.world_dir(out, d.tag)
    pf = rec.preflight(out, "E1", auth, sched)
    if pf.get("refused"):
        return pf
    rp = Path(release_path) if release_path else wd / "RELEASE_A.json"
    with hwsg_bind.world(d.tag):
        r = k4b_release.verify_release(rp, "A", task_sha256, session, out / "FREEZE.json")
        if r["reservation"] != d.reservation_id:
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "release reservation id")
        handoff = hwsg_handoff.as_hwsc(hwsg_handoff.load(d.tag, out))
        ctx = {"release": r, "reservation_path": wd / "RESERVATION_W2.json", "handoff": handoff}
        _audit_gate(wd, d.tag)
        recs = rec.run_gates_c(wd, e1_steps(out, wd, d.tag, ctx, handoff, auth, sched),
                               dry_continue)
    rec.record_gate_files(wd, "E1", ("H1C.json", "L1.json"))
    bad = next((x for x in recs if x["status"] != "PASS"), None)
    if bad:
        p1 = any(x["gate"] == "P1" and x["status"] == "PASS" for x in recs)
        rec.terminal_result(wd, d.tag, bad["status"], "E1", bad["gate"],
                            {"reason": str(bad.get("reason", ""))[:500]}, p1)
        return {"status": bad["status"], "gates": recs}
    return {"status": "PASS", "gates": recs}


# ------------------------------------------------------------------------------------ E2
def run_e2(out, w, auth, sched, release_path=None, session=None, dry_continue=False) -> dict:
    out, d = Path(out), gc.world(w)
    wd = gc.world_dir(out, d.tag)
    pf = rec.preflight(out, "E2", auth, sched)
    if pf.get("refused"):
        return pf
    rp = Path(release_path) if release_path else wd / "RELEASE_B.json"
    ctx = {}

    def g_release():
        bar = rec.release_barrier(out)
        if not bar["ok"] or bar["release_b_missing"]:
            raise C1GateFailure("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", f"release barrier {bar}")
        ctx["release"] = k4b_fresh.require_release_b(out, rp, session)
        return {"N": ctx["release"]["N"], "k": ctx["release"]["k"]}

    def g_identity():
        handoff = hwsg_handoff.as_hwsc(hwsg_handoff.load(d.tag, out))
        ctx.update(hwsc_jobs.e2_context(wd, ctx["release"], handoff, False))
        reg2 = json.loads((out / "registry" / "K-REG2.json").read_text(encoding="utf-8"))
        hwsg_registry.recheck(reg2)
        ctx["test"] = hwsc_data.sample_test_c(wd, ctx["proc"], ctx["release"],
                                              ctx["reservation_path"], False)
        test = ctx["test"]
        ctx["test_acts"] = lambda j, s: c1_model.activations(
            ctx["models"][(j, s)], k4b_data.model_inputs(test["canon32"], ctx["proc"]["perm"][j]))
        return {"Z_bound": str(ctx["Z"]), "test_rows": int(len(ctx["test"]["canon32"]))}

    def g_ratio():
        rr = hwsg_ratio.ratio_gate(dict(ctx, out=wd), ctx["result"], True,
                                   d.seeds["endpoint"], out=wd)
        ctx["ratio"] = rr
        return {"ratio": rr["status"]}

    steps = [("RELEASE_B", g_release), ("H1G_E2", g_identity),
             ("H2-FRESH", lambda: hwsc_data.h2_fresh_c(out, ctx)),
             ("T-PRE", lambda: k4b_fresh.t_pre(wd, ctx)),
             ("ENDPOINT", lambda: k4b_fresh.endpoint_gate(ctx)), ("RATIO", g_ratio)]
    with hwsg_bind.world(d.tag):
        _audit_gate(wd, d.tag)
        recs = rec.run_gates_c(wd, steps, dry_continue)
    rec.record_gate_files(wd, "E2", ("H1C_E2.json",))
    bad = next((x for x in recs if x["status"] != "PASS"), None)
    if bad:
        rec.terminal_result(wd, d.tag, bad["status"], "E2", bad["gate"],
                            {"reason": str(bad.get("reason", ""))[:500]}, True)
        return {"status": bad["status"], "gates": recs}
    result = ctx["result"]
    ann = hwsc_outcome.annotations(result)
    oc = rec.outcome_g(hwsc_outcome.state_from_gates(stage_records.gates_so_far(wd),
                                                     result=result))
    stage_records.record_gate(wd, "OUTCOME", "PASS", outcome=oc["outcome"],
                              annotations=oc["annotations"])
    fill = hwsc_jobs._fill(result)
    f = rec.export_g(wd, result, oc, ann, fill, ctx["ratio"]["files"])
    return {"status": "PASS", "outcome": oc, "result": str(f)}


# ------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    import hwsg_cross
    import hwsg_oracle
    import hwsg_train

    ap = argparse.ArgumentParser(prog="hwsg_jobs")
    ap.add_argument("job", choices=("kc", "o", "train", "reg1", "e1", "reg2", "e2", "cross"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--world")
    ap.add_argument("--auth", required=True)
    ap.add_argument("--sched", required=True)
    ap.add_argument("--accept")
    ap.add_argument("--release")
    ap.add_argument("--session")
    ap.add_argument("--task-sha256")
    a = ap.parse_args(argv)
    load = lambda p: json.loads(Path(p).read_text(encoding="utf-8")) if p else None  # noqa: E731
    auth, sched = load(a.auth), load(a.sched)
    out = Path(a.out)
    fns = {"kc": lambda: hwsg_known.run_kc(out, auth, sched, a.name),
           "o": lambda: hwsg_oracle.run_o(out, auth, sched, a.name),
           "train": lambda: hwsg_train.run_train(out, a.world, auth, sched, load(a.accept),
                                                 a.name),
           "reg1": lambda: run_reg1(out, auth, sched, a.name),
           "e1": lambda: run_e1(out, a.world, auth, sched, a.release, a.session,
                                a.task_sha256),
           "reg2": lambda: run_reg2(out, auth, sched, a.name),
           "e2": lambda: run_e2(out, a.world, auth, sched, a.release, a.session),
           "cross": lambda: hwsg_cross.run_cross(out, auth, sched, a.name)}
    r = fns[a.job]()
    print(json.dumps(r, default=str)[:4000])
    st = str(r.get("status", "PASS")) if isinstance(r, dict) else "PASS"
    return 0 if st in ("PASS", "SUPPORT", "EXCLUSION", "MIXED") or r.get("refused") else 1


if __name__ == "__main__":
    raise SystemExit(main())
