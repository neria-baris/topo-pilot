"""HWSG process, identity and stage O (API.md §4; protocol §2.3, §2.6, §3; gates O0-O5)."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_bind
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import c1_means
import hws_exact
import hws_oracle
import hws_worlds
import hwsb_data
import hwsb_eval
import hwsb_law
import k4b_cert
import numpy as np
import oracle_profile
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore
from topo_pilot.contracts.backends import LocalFSBackend
from topo_pilot.contracts import WorldSpec
from topo_pilot.process.transition import TransitionBuilder

IDENT, ORACLE, LAW = "FAIL_TECHNICAL/IDENTITY", "FAIL_TECHNICAL/ORACLE", "FAIL_TECHNICAL/LAW_BOUND"


def build_process_g(store, w, masters=None) -> dict:
    d = gc.world(w)
    kw = dict(masters=tuple(masters) if masters is not None else d.masters,
              emission_cfg=d.emission_cfg, world_cfg=d.world_cfg, transition_cfg=d.transition_cfg)
    hwsg_bind.check_explicit("build_process", kw)
    proc = hwsb_data.build_process(store, **kw)
    proc["sigma"], proc["neighbour"] = d.sigma, d.neighbour
    return proc


def process_builder(key):
    return lambda store, masters=None: build_process_g(store, key, masters)


def identity(store, proc, w) -> dict:
    d, c = gc.world(w), gc.CONTRACT["world_common"]
    ck = hwsb_data.spec_checksums(store, proc)
    nb_ok = (proc["sigma"] == d.sigma and proc["neighbour"] == d.neighbour
             and (1 - d.p) / 4 == d.neighbour)
    world = store.load(WorldSpec, proc["ids"]["world"], consumer=hwsb_data.READER)
    from topo_pilot.process import TransitionConfig

    T_ref = np.asarray(TransitionBuilder().build(world, TransitionConfig(p_stay=d.p_float)).T)
    ecs = [e.tobytes() for e in proc["E_canon"].values()]
    try:
        oracle_profile.validate_process(proc["T"], proc["E_canon_shared"], proc["pi"],
                                        float(c["validate_tol"]))
        valid = True
    except Exception:  # noqa: BLE001
        valid = False
    checks = {
        "sigma_neighbour": bool(nb_ok),
        "world_id": proc["ids"]["world"] == c["WorldSpec_id_expected"],
        "world_payload": ck["WorldSpec"] == c["WorldSpec_payload_sha256"],
        "transition_rebuilt": bool(np.array_equal(np.asarray(proc["T"]), T_ref)),
        "E_canon_equal": len(set(ecs)) == 1,
        "validate_process": valid,
    }
    return {"ok": all(checks.values()), "checks": checks, "ids": proc["ids"],
            "arrays_sha256": hwsb_data.arrays_sha256(proc),
            "transition_id": proc["ids"]["transition"], "spec_checksums": ck}


def identity_checker(key):
    d = gc.world(key)

    def process_identity(store, proc) -> dict:
        r = identity(store, proc, d.tag)
        try:
            import hwsg_handoff

            h = hwsg_handoff.load(d.tag)["process_identities"]
            same = (json.loads(json.dumps(r["ids"], default=str)) == h.get("ids")
                    and r["arrays_sha256"] == h.get("arrays_sha256"))
        except C1GateFailure:
            same = False
        r["checks"]["handoff_identities"] = same
        r["ok"] = r["ok"] and same
        return r

    return process_identity


# ------------------------------------------------------------------------------------ O0
def _sha(path) -> str:
    return hashlib.sha256(gc.guard(path).read_bytes()).hexdigest()


def selection(report_path=None, s3_dir=None) -> dict:
    report_path = gc.REPORT_PATH if report_path is None else report_path
    s3_dir = gc.S3_DIR if s3_dir is None else s3_dir
    sel = gc.CONTRACT["selection"]
    if _sha(report_path) != sel["report_sha256"]:
        raise C1GateFailure(gc.BAD, "REPORT.json sha256 differs")
    for key, want in sel["s3_record_sha256"].items():
        if _sha(Path(s3_dir) / f"{key}.json") != want:
            raise C1GateFailure(gc.BAD, f"S3 record {key} sha256 differs")
    report = gc.read_json(report_path)
    order = [k for k in report["finalists"]["ordinary"] if k != gc.W_STAR]
    pool = [k for k in order if gc.read_json(Path(s3_dir) / f"{k}.json")["law_bound"]["status"]
            == "BOUNDED"]
    L3 = {k: float(report["s3"][k]["L3"]["D4"]) for k in pool}
    lo = min(pool, key=lambda k: (L3[k], pool.index(k)))
    hi = max(pool, key=lambda k: (L3[k], -pool.index(k)))
    rest = [k for k in pool if k not in (lo, hi)]
    tgt = (math.log(L3[lo]) + math.log(L3[hi])) / 2
    mid = min(rest, key=lambda k: (abs(math.log(L3[k]) - tgt), rest.index(k)))
    reg = sel["registered"]
    ok = (lo, mid, hi) == (reg["lo"], reg["mid"], reg["hi"])
    if not ok:
        raise C1GateFailure(gc.BAD, f"selection {(lo, mid, hi)} differs from the registered list")
    return {"pool": pool, "L3": L3, "lo": lo, "mid": mid, "hi": hi, "registered_ok": ok}


def _s3(w, s3_dir=None) -> dict:
    d = gc.world(w)
    p = Path(gc.S3_DIR if s3_dir is None else s3_dir) / f"{d.key}.json"
    if _sha(p) != gc.CONTRACT["selection"]["s3_record_sha256"][d.key]:
        raise C1GateFailure(gc.BAD, f"S3 record {d.key} sha256 differs")
    return gc.read_json(p)


# ------------------------------------------------------------------------------- O2, O3, O5
def law(proc, w, s3_dir=None) -> dict:
    d = gc.world(w)
    try:
        kw = dict(sigma=d.sigma, neighbour=d.neighbour)
        hwsg_bind.check_explicit("law_bound", kw)
        r = hwsb_law.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"],
                               **kw)
        z_ref = Fraction(d.stage_a["law_bound_Z_exact_upper"])
        s3 = _s3(d.tag, s3_dir) if s3_dir is not None else None
        if s3 is not None and Fraction(s3["law_bound"]["Z_bound"]["exact_upper"]) != z_ref:
            raise C1GateFailure(LAW, "S3 record Z_bound differs from the contract")
        f_plan = k4b_cert.F_plan(r["Z_bound"]) if r["Z_bound"] is not None else None
        ok = (r["status"] == "BOUNDED" and r["kappa"] < 1 and r["delta"] == 0
              and r["Z_bound"] == z_ref and f_plan <= gc.F_PLAN_MAX)
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(LAW, repr(exc)) from exc
    if not ok:
        raise C1GateFailure(LAW, f"law bound: {r['status']} Z={r['Z_bound']} delta={r['delta']}")
    return {"status": r["status"], "Z_bound": r["Z_bound"], "kappa": r["kappa"],
            "delta": r["delta"], "F_plan": f_plan, "Z_ref": z_ref}


def d2a(proc) -> dict:
    p = hws_exact.p_d2a(proc["T"], proc["E_canon_shared"], proc["pi"])
    value = gc.O3_ROWS * Fraction(float(p))
    ok = value <= gc.RISK_MAX
    r = {"p_D2a": float(p), "value": value, "ok": ok}
    if not ok:
        raise C1GateFailure("INCONCLUSIVE/REGISTRY_RISK", f"{gc.O3_ROWS} * p_D2a = {float(value)}")
    return r


def headroom(w, report) -> dict:
    d = gc.world(w)
    s3 = report["s3"][d.key]
    ok = s3.get("at_3x") is True and float(s3["L3"]["D4"]) >= 3 * float(gc.M)
    if not ok:
        raise C1GateFailure("INCONCLUSIVE/ORACLE_FEASIBILITY", f"{d.key}: at_3x / L3.D4 < 3M")
    return {"at_3x": True, "L3_D4": float(s3["L3"]["D4"]), "floor": 3 * float(gc.M)}


# ------------------------------------------------------------------------------------ O4
def _means(proc, tok) -> dict:
    q = hwsb_eval.oracle_predictives(proc, tok, (1, 4))
    m = hwsb_eval.moments(proc, tok)

    def c(x):
        return hws_oracle.circ_marginal(x, 6)

    def mean(x):
        return float(c1_means.tree_mean(x))

    return {"D4": mean(hwsb_eval.d4_rows(m)), "GC": mean(hws_oracle.kl_rows(q[32], q[1])),
            "G4": mean(hws_oracle.kl_rows(q[32], q[4])),
            "G4A": mean(hws_oracle.kl_rows(c(q[32]), c(q[4])))}


def reproduce(proc_hws, w, hist_path=None, s3_dir=None) -> dict:
    d = gc.world(w)
    rec = _s3(d.tag, s3_dir)
    tol = float(gc.CONTRACT["o4"]["tol"])
    look = hws_oracle.world_look(proc_hws, "S3", int(rec["n"]), tuple(rec["Ks"]), p4=False)
    tok = np.asarray(look["tok"])
    path = Path(hist_path) if hist_path is not None else gc.HWS_STORE / "hist" / "S3" / \
        f"{d.key}.npz"
    sha = stage_records.sha256(path)
    with np.load(path, allow_pickle=False) as z:
        stored = np.asarray(z["canon32"])
    adapt = {"T": proc_hws["T"], "E_canon_shared": proc_hws["E"], "pi": proc_hws["pi"],
             "features": proc_hws["features"]}
    got = _means(adapt, tok)
    ref = {q: float(rec["bounds"][q]["mean"]) for q in got}
    checks = {"hist_sha256": sha == rec["hist_sha256"],
              "tokens_equal": stored.shape == tok.shape and bool(np.array_equal(stored, tok)),
              "stream": list(look["stream"]) == list(rec["stream"]),
              "means": all(abs(got[q] - ref[q]) <= tol for q in got)}
    if not all(checks.values()):
        raise C1GateFailure(ORACLE, f"O4 {checks}")
    return {"checks": checks, "values": got, "references": ref, "tolerance": tol}


def stage_a_process(w):
    d = gc.world(w)
    return hws_worlds.build_process(hws_worlds.World(12, 1, d.sigma, d.p))


def store_for(wdir) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(wdir) / "artifacts"))


def _files(d) -> set:
    d = Path(d)
    return {p for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()


def run_o(out, auth, sched, job, store=None) -> dict:
    import hwsg_handoff
    import hwsg_records as rec
    import k4b_driver

    out = Path(out)
    pf = rec.preflight(out, "O", auth, sched)
    if pf.get("refused"):
        return pf
    record = {"selection": None, "worlds": {}, "protocol_sha256": gc.PROTOCOL_SHA}
    try:
        record["selection"] = selection()
        report = gc.read_json(gc.REPORT_PATH)
        stage_records.record_gate(out, "SELECTION", "PASS")
    except Exception as exc:  # noqa: BLE001  O0 is shared: every world ends
        status = rec.status_of(exc)
        stage_records.record_gate(out, "SELECTION", status, reason=str(exc)[:2000])
        for tag in gc.TAGS:
            wdir = gc.world_dir(out, tag)
            wdir.mkdir(parents=True, exist_ok=True)
            rec.terminal_result(wdir, tag, status, "O", "SELECTION", {"reason": str(exc)[:500]},
                                False)
        return {"status": status}
    files, new_handoffs = [], []
    for tag in gc.TAGS:
        wdir = gc.world_dir(out, tag)
        wdir.mkdir(parents=True, exist_ok=True)
        st, ctx = store_for(wdir), {}
        before = _files(wdir / "artifacts")

        def g_identity(tag=tag, st=st, ctx=ctx):
            ctx["proc"] = build_process_g(st, tag)
            r = identity(st, ctx["proc"], tag)
            ctx["ident"] = r
            if not r["ok"]:
                raise C1GateFailure(IDENT, f"checks {r['checks']}")
            return {"value": r["checks"], "transition_id": r["transition_id"]}

        def g_law(tag=tag, ctx=ctx):
            ctx["law"] = law(ctx["proc"], tag, gc.S3_DIR)
            return {"value": str(ctx["law"]["Z_bound"]), "reference": str(ctx["law"]["Z_ref"])}

        def g_d2a(ctx=ctx):
            ctx["d2a"] = d2a(ctx["proc"])
            return {"value": float(ctx["d2a"]["value"]), "reference": float(gc.RISK_MAX)}

        def g_repro(tag=tag, ctx=ctx):
            ctx["repro"] = reproduce(stage_a_process(tag), tag, s3_dir=gc.S3_DIR)
            return {"value": ctx["repro"]["values"], "tolerance": ctx["repro"]["tolerance"]}

        steps = [(f"PROCESS_IDENTITY_{tag}", g_identity), (f"LAW_BOUND_{tag}", g_law),
                 (f"D2A_RISK_{tag}", g_d2a), (f"ORACLE_REPRO_{tag}", g_repro),
                 (f"HEADROOM_{tag}", lambda tag=tag: headroom(tag, report))]
        with hwsg_bind.world(tag):
            a = hwsg_bind.audit(tag)
            stage_records.record_gate(out, f"BINDING_AUDIT_{tag}", a["status"],
                                      n_hits=a["n_hits"])
            recs = rec.run_gates_c(out, steps)
        bad = next((r for r in recs if r["status"] != "PASS"), None)
        entry = {"gates": {r["gate"]: {k: r.get(k) for k in ("status", "value", "reference",
                                                               "tolerance")} for r in recs},
                 "status": bad["status"] if bad else "PASS"}
        if bad:
            rec.terminal_result(wdir, tag, bad["status"], "O", bad["gate"],
                                {"reason": str(bad.get("reason", ""))[:500]}, False)
        else:
            h = hwsg_handoff.build(tag, {"law": ctx["law"], "identity": ctx["ident"],
                                         "p_D2a": ctx["d2a"]["p_D2a"]})
            hwsg_handoff.write(wdir, h)
            new_handoffs.append(wdir / hwsg_handoff.FILE)
            entry.update(process_identities=json.loads(json.dumps(ctx["ident"], default=str)),
                         law=json.loads(json.dumps(ctx["law"], default=str)),
                         p_D2a=ctx["d2a"]["p_D2a"], repro=ctx["repro"])
        record["worlds"][tag] = entry
        files += sorted(_files(wdir / "artifacts") - before)
    f = out / "stages" / "O" / "O_RECORD.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, json.loads(json.dumps(record, default=str)))
    k4b_driver.complete_stage(out, "O", [f] + new_handoffs + files)
    return record
