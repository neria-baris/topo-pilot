"""HWSC synthetic dry run: run_dry and DRC1-DRC4 (API.md §8; protocol §7; ruling R-0176-G3).
DRC5-DRC14 live in hwsc_dry2 (split by size). Streams only under the dry scopes, masters
629911-629913, seeds DRY_SEEDS (620311/620315 only on DRC6's synthetic arrays, R-0176-G5);
persisted histories only from the tiny world (DRYHIST_ names); w* rows stay in memory."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
import time
import traceback
from fractions import Fraction
from pathlib import Path

import c1_model
import hwsb_config
import hwsb_data
import hwsb_dry
import hwsb_dry2
import hwsb_train
import hwsc_bind
import hwsc_data
import hwsc_gates
import hwsc_known
import hwsc_records
import hwsc_registry
import k4b_driver
import k4b_fresh
import k4b_release
import numpy as np
import stage_records

from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend, SeedTree
from topo_pilot.contracts.backends import LocalFSBackend
from topo_pilot.learner.stage import LearnerStage

REGISTERED = ("PASS", "FAIL", "NOT_RUN", "PAUSE", "REPORTED")


def _registered(s) -> bool:
    return s in REGISTERED or str(s).startswith(("INCONCLUSIVE/", "FAIL_TECHNICAL/"))


def case_dir(out, case) -> Path:
    d = Path(out) / case / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d.mkdir(parents=True, exist_ok=False)
    return d


def _mem():
    return ArtifactStore(MemoryBackend())


def build_tiny_process_c(store, masters=cc.DRY_MASTERS) -> dict:
    return hwsb_dry.build_tiny_process(store, masters=tuple(masters))


def _stub(digests=(), status="PASS"):
    r = hwsc_registry._new()
    r.update(status=status, digests=set(digests))
    return r


def synthetic_root(base) -> dict:
    """A synthetic project root and scratch root (never the real ones; S2)."""
    base = Path(base)
    root, scratch = base / "root", base / "scratch"
    for d in (root / "agent-handoff", root / "topo-pilot" / "artifacts", scratch / "empty"):
        d.mkdir(parents=True, exist_ok=True)
    return {"root": root, "scratch": scratch}


def stub_sources(extra_digests=()) -> dict:
    """Synthetic replacements for the sources that need the real stores (DRC1, DRC9)."""
    tok = {"problems": [], "lineage": [], "a": ([], {}), "b": [], "c": [],
           "e": {"sources": [], "problems": [], "predicates": ["sealed_d2a"],
                 "sealed_ranges": {}, "ranges": {}}, "d": [], "k": None, "art": None,
           "store_a": None}
    x6 = {"status": "PASS", "digestset": None, "files": [], "other": [], "base": None}
    inv = {"status": "PASS", "inv": {}, "classes": {}, "unlisted": [], "violations": []}
    out = {"token_sources": lambda: dict(tok), "x6_source": lambda: dict(x6),
           "scratch": lambda readers_ok: _stub(), "inventory": lambda readers: dict(inv),
           "coverage": lambda src, seqs: {"ok": True, "missing": []}}
    for t in ("c2", "c2sup", "c2scratch", "hws", "x6zc", "c2nd", "hwsb", "dry"):
        out[t] = (lambda d=tuple(extra_digests) if t == "dry" else (): _stub(d))
    return out


# --------------------------------------------------------------------------------- DRC1
def _train_tiny(d, store, proc, plan) -> dict:
    recs = {}
    for m in cc.DRY_MASTERS:
        obs = hwsc_data.make_train_dev_c(store, proc, m, plan)
        res = hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, m, plan=plan)
        rec = {"master": m, "status": "COMPLETE", "run_key": res["run_key"],
               "checkpoint_ids": {str(k): v for k, v in res["checkpoint_ids"].items()},
               "checksums": {str(k): v for k, v in res["checksums"].items()}}
        p = d / "stages" / "TRAIN" / str(m) / "TRAIN_RECORD.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        stage_records.write_new(p, rec)
        k4b_driver.complete_stage(d, f"TRAIN_{m}", [p])
        stage_records.record_gate(d, f"TRAIN_{m}", "PASS")
        recs[m] = rec
    return recs


def drc1(out, ctx) -> dict:
    d = case_dir(out, "DRC1")
    plan = cc.dry_plan("dry_tiny", "DRC1")
    store = ArtifactStore(LocalFSBackend(d / "artifacts"))
    syn = synthetic_root(d / "synthetic")
    table = hwsc_bind.load_table(which="dry", case="DRC1", case_dir=d)
    with hwsc_bind.bound_stage_c(table):
        proc = build_tiny_process_c(store)
        recs = _train_tiny(d, store, proc, plan)
        ck = {(m, s): store.load(Checkpoint, recs[m]["checkpoint_ids"][str(s)],
                                 consumer="experiment")
              for m in cc.DRY_MASTERS for s in (plan.gate_step, 0)}
        rel = {"reservation": cc.RESERVATION_ID, "k": 1, "N": 3072}
        k4b_release.start_reservation(d / cc.RESERVATION_FILE, "HWSC-W2", hwsc_records.utc())
        c = {"release": rel, "reservation_path": d / cc.RESERVATION_FILE, "dry": True,
             "proc": proc, "Z": Fraction(1, 10**12), "p_d2a": 1e-15,
             "ckpts": {(m, 5000): ck[(m, plan.gate_step)] for m in cc.DRY_MASTERS},
             "models": {(m, "step5000" if s else "step0"): c1_model.load_model64(ck[(m, s)])[0]
                        for (m, s) in ck}}
        inv = hwsb_data.history_inventory(d) if hasattr(hwsb_data, "history_inventory") else {}
        handoff = {"store_inventory": {}, "N_C": 3072, "Z_bound": c["Z"], "F_plan": None,
                   "p_D2a": 1e-15, "stage_c_exclusions": ()}

        def reg(version, extra=None):
            m = hwsc_registry.build(version, d / "registry", root=syn["root"],
                                    scratch=syn["scratch"], handoff=handoff, own_expected=inv,
                                    extra=extra, sources=stub_sources())
            if version == "K-REG1":
                import c2_registry

                c["reg1"] = c2_registry.Registry.load(d, "K-REG1")
            return {"status": m["status"]}

        sch = {"live_history_reservations": [], "frozen_registries_awaiting_draw": []}

        def outcome():
            st = hwsc_gates.state_from_gates(stage_records.gates_so_far(d))
            return {"status": "PASS", "outcome": hwsc_gates.outcome(st)["outcome"]}

        e1 = [("G0C", lambda: hwsc_known.g0c(d, "E1", {}, sch, None, root=syn["root"])),
              ("H1C", lambda: hwsc_gates.h1c(d, dict(c), handoff, store)),
              ("REG1", lambda: reg("K-REG1")), ("H2", lambda: hwsc_data.h2c(d, c)),
              ("L1", lambda: hwsc_gates.l1(d, c)),
              ("ORACLE-VAL", lambda: k4b_driver.oracle_val(d, c)),
              ("B4-VAL", lambda: k4b_driver.b4_val(d, c)),
              ("C0-CAL", lambda: k4b_driver.c0_cal_stage(d, c)),
              ("C0-VAL", lambda: k4b_driver.c0_val_stage(d, c)),
              ("CERT-VAL", lambda: k4b_driver.cert_val(d, c)),
              ("P1", lambda: hwsc_gates.p1c(d, c, handoff)),
              ("REG2", lambda: reg("K-REG2", c.get("tables"))),
              ("H2-FRESH", lambda: hwsc_data.h2_fresh_c(d, c)),
              ("T-PRE", lambda: k4b_fresh.t_pre(d, c)),
              ("ENDPOINT", lambda: k4b_fresh.endpoint_gate(c)), ("OUTCOME", outcome)]
        recs_g = hwsc_records.run_gates_c(d, e1, dry_continue=True)
    from hwsc_jobs import run_close

    close = run_close(d, recs_g)
    gates = stage_records.gates_so_far(d)
    names = [g["gate"] for g in gates]
    want = [f"TRAIN_{m}" for m in cc.DRY_MASTERS] + [g for g, _ in e1]
    ok = (all(names.count(g) == 1 for g in want) and all(_registered(g["status"])
                                                         for g in gates)
          and not any(p.name.startswith("HIST_") for p in d.rglob("*.npz"))
          and all(r["status"] == "COMPLETE" for r in recs.values()))
    return {"status": "PASS" if ok else "FAIL",
            "details": {"gates": {g["gate"]: g["status"] for g in gates},
                        "readings": {g: "EXACT" if g.startswith("TRAIN_") else "VALUE"
                                     for g in want},
                        "records": "EXACT (one registered record per gate; no HIST_* name)",
                        "outcome": close["status"]}}


# --------------------------------------------------------------------------------- DRC2
def e4_eval_check_c(store, ckpt_id, proc, m, plan_b, case_dir_) -> dict:
    import k4b_cert
    import k4b_charts
    import k4b_config
    import k4b_scores

    res = {"abc": dict(hwsb_dry2.e4_eval_check(store, ckpt_id, None, proc, m, plan_b),
                       reading="EXACT")}
    blk = hwsb_data.make_block(proc, "CAL", plan_b)
    canon, ids = blk["canon32"], blk["seq_ids"]
    mom = k4b_scores.oracle_moments(proc["T"], proc["E_canon_shared"], proc["pi"], canon,
                                    proc["features"])
    low = np.argsort(ids, kind="stable")[:4]
    refs = k4b_cert.references(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"],
                               canon[low])
    chk = k4b_cert.moment_check({K: v[low] for K, v in mom.items()}, refs)
    res["d"] = {"ok": bool(chk["ok"]), "max_gap": str(chk["max_gap"]), "reading": "EXACT"}
    ck = store.load(Checkpoint, ckpt_id, consumer="experiment")
    X = c1_model.activations(c1_model.load_model64(ck)[0],
                             hwsb_data.model_inputs(canon, proc["perm"][m]))
    trained, _ = k4b_charts.open_ledgers(case_dir_)
    try:
        r = k4b_charts.build_chart(X[:512], ids[:512], mom[32][:512], trained, m, "production",
                                   k4b_config.chart_cfg())
        st = r["status"]
    except Exception as exc:  # noqa: BLE001  reading VALUE: a recorded status
        st = hwsc_records.status_of(exc)
    res["e"] = {"ok": _registered(st), "status": st, "reading": "VALUE"}
    return res


def drc2(out, ctx) -> dict:
    d = case_dir(out, "DRC2")
    plan = cc.dry_plan("dry_e4", "DRC2")
    plan_b = hwsb_config.dry_plan("dry_e4", "DRC2")
    import dataclasses

    plan_b = dataclasses.replace(plan_b, masters=cc.DRY_MASTERS)
    det = {}
    with hwsc_bind.bound_stage_c():
        m = cc.DRY_MASTERS[0]
        runs = []
        for _ in range(2):
            st = _mem()
            proc = hwsc_data.build_process_c(st, masters=cc.DRY_MASTERS)
            runs.append((st, proc, hwsc_data.make_train_dev_c(st, proc, m, plan)))
        (sa, pa, ia), (sb, _, ib) = runs
        a = hwsb_train.train(sa, {"train": ia["train"], "dev": ia["dev"]}, m, plan=plan)
        b = LearnerStage().run(ib["train"], ib["dev"], plan.model_cfg, plan.train_cfg,
                               SeedTree(m), cc.run_key(plan, m), sb)
        steps = sorted(a["checkpoint_ids"])
        det["run_key"] = a["run_key"] == ["hwsc-v1", "DRY", "DRC2", m]
        det["bitwise"] = [a["checkpoint_ids"][s] for s in steps] == list(b)
        det["eval"] = e4_eval_check_c(sa, a["checkpoint_ids"][steps[-1]], pa, m, plan_b, d)
    ok = det["run_key"] and det["bitwise"] and det["eval"]["abc"]["ok"] and \
        det["eval"]["d"]["ok"] and det["eval"]["e"]["ok"]
    return {"status": "PASS" if ok else "FAIL", "details": det}


# ---------------------------------------------------------------------------- DRC3, DRC4
def drc3(out, ctx) -> dict:
    import types

    import hwsc_known

    k7 = hwsc_known.kc7()
    det = {"kc7": k7["checks"]}
    mod = types.ModuleType("planted_drc3")
    mod.__file__ = str(cc.HERE / "planted_drc3.py")
    mod.X = (1729, 2718, 3141)

    def f(a=610101):
        return a

    f.__module__ = "planted_drc3"
    mod.f = f
    mod.P = hwsb_config.Plan("real", (620201, 620202), None, None)
    a = hwsc_bind.audit(modules=[mod])
    tops = {h["top"] for h in a["unlisted"]}
    det["planted"] = sorted(tops)
    try:
        with hwsc_bind.bound_stage_c():
            raise RuntimeError("planted")
    except RuntimeError:
        pass
    det["restored"] = not hwsc_bind.check_old(hwsc_bind.load_table())
    ok = (k7["status"] == "PASS" and {"X", "f.__defaults__", "P"} <= tops
          and a["status"] != "PASS" and det["restored"])
    return {"status": "PASS" if ok else "FAIL", "details": det}


def drc4(out, ctx) -> dict:
    case = "DRC4"
    plan_b = hwsb_config.dry_plan("dry_tiny", case)
    m = plan_b.masters[0]
    res = []
    for fn in ("mirror", "hwsb"):
        st = _mem()
        proc = hwsb_dry.build_tiny_process(st, masters=(m,))
        r = (hwsc_data.make_train_dev_c(st, proc, m, plan_b, scope="hwsb-v1") if fn == "mirror"
             else hwsb_data.make_train_dev(st, proc, m, plan_b))
        res.append((st, r))
    (sa, ra), (sb, rb) = res
    same = all(ra[s] == rb[s] and sa.meta(ra[s]).payload_sha256 == sb.meta(rb[s]).payload_sha256
               for s in ("train", "dev"))
    d = Path(out) / case
    with hwsc_bind.bound_stage_c(hwsc_bind.load_table(which="dry", case=case, case_dir=d)):
        plan = cc.dry_plan("dry_tiny", case)
        mc = plan.masters[0]
        ids_c = hwsc_data.sequence_ids_c("train", 4096, plan, mc)
    ids_b = hwsb_data.sequence_ids("train", 4096, plan_b, m)
    disjoint = not (set(ids_c.tolist()) & set(np.asarray(ids_b).tolist()))
    return {"status": "PASS" if same and disjoint else "FAIL",
            "details": {"bitwise_with_hwsb_v1": same, "hwsc_disjoint": disjoint}}


# --------------------------------------------------------------------------------- run_dry
def run_dry(out=None, sched=None, only=None) -> dict:
    import hwsc_dry2

    out = Path(cc.DRY_STORE if out is None else out)
    if not hwsc_records.sched_ok(sched, "DRY")["ok"]:
        return {"status": "REFUSED", "reason": "SCHED W2 rule"}
    cases = {f"DRC{i}": globals().get(f"drc{i}") or getattr(hwsc_dry2, f"drc{i}")
             for i in range(1, 15)}
    results = {}
    for name, fn in cases.items():
        if only and name not in only:
            continue
        try:
            results[name] = fn(out, {})
        except Exception as exc:  # noqa: BLE001  a crashing case is a FAIL
            results[name] = {"status": "FAIL", "details": {
                "error": f"{type(exc).__name__}: {exc}",
                "trace": traceback.format_exc()[-2000:]}}
    h = hwsc_records._git(cc.REPO, "rev-parse", "HEAD").decode().strip()
    files = hwsc_records.implementation_files(cc.REPO, h)
    rep = {"cases": results, "all_pass": all(r["status"] == "PASS" for r in results.values())
           and not only, "implementation_files": files,
           "implementation_sha256": hwsc_records._sha(json.dumps(files, sort_keys=True).encode()),
           "h_exec": h, "tree_clean": not hwsc_records._git(cc.REPO, "status", "--porcelain",
                                                            "--", "tools/hwsc",
                                                            "tests/hwsc").strip()}
    p = out / "stages" / "DRY" / "DRY_REPORT.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, json.loads(json.dumps(rep, default=str)))
    return rep
