"""hwsd dry-run cases DRD5, DRD7, DRD8-DRD11 (API.md §12; TEST_PLAN §4). Split from hwsd_dry by
size; DRD5 and DRD7 are re-exported from hwsd_dry by its lazy __getattr__. Every case is
synthetic: arrays and stores live under test_hwsd-<job>/dry/<case>/ (decision 6)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import builtins
import io
import json
import math
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import c1_means
import c2_registry
import hwsb_eval
import k4b_release
import numpy as np
import scores
import stage_records
from c1_records import C1GateFailure

import hwsd_bind as db
import hwsd_data as dd
import hwsd_readers as drd
import hwsd_records as drec
import hwsd_registry as dr
import hwsd_score as ds
import hwsd_statements as dst
import hwsd_summary as dsum
from hwsd_dry import _job, _res, fresh_fixture

M, F9 = Fraction(1, 100), Fraction(1, 10**9)
UTC = "2026-11-01T00:00:00Z"


def _raises(fn, status=None) -> bool:
    try:
        fn()
    except C1GateFailure as exc:
        return status is None or exc.status == status
    return False

# --------------------------------------------------------------------------------- DRD5
_K = {"EX": ("SCORED", True, -0.001, 0.002), "SUP": ("SCORED", True, 0.05, 0.06),
      "UNR": ("SCORED", True, 0.0, 0.05), "UNC": ("UNCERTIFIED", True, 0.05, 0.06),
      "SUa": ("SCORED_UNVALIDATED", False, 0.05, 0.06),
      "SUl": ("SCORED_UNVALIDATED", False, -0.001, 0.002), "CU": ("CHART_UNAVAILABLE", False,
                                                                None, None)}


def _r(kind, i=0, learn=False, bp=None, **kw) -> dict:
    s, v, lo, hi = _K[kind]
    f = None if lo is None else F9
    row = {"status": s, "valid": v, "L": lo, "U": hi, "L_S": lo, "U_S": hi, "F_minus": f,
           "F_plus": f, "learn_pass": learn, "B2_L_zS": bp, "step": i}
    return dict(row, **kw)


def _ev(*seqs, **kw) -> dict:
    seqs = list(seqs) * (3 // len(seqs)) if len(seqs) in (1, 3) else seqs
    return dst.evaluate({629951 + i: [_r(k, n) if isinstance(k, str) else k
                                     for n, k in enumerate(s)] for i, s in enumerate(seqs)}, **kw)


def _st(ev, d) -> tuple:
    s = ev["statements"][d]
    return s["reading"], sorted(s["reasons"])


def drd5(out, ctx) -> dict:
    c = {}
    o = lambda s, a="chart": dst.order([_r(k, i) for i, k in enumerate(s)], a)["category"]  # noqa: E731
    c["AFTER"] = o(["CU", "EX", "EX", "SUP"]) == "AFTER"
    c["WITH"] = o(["CU", "SUP", "SUP"]) == "WITH"
    c["BEFORE"] = o(["CU", "SUa", "SUP", "SUP"]) == "BEFORE"
    c["NEVER"] = o(["CU", "EX", "EX"]) == "NEVER"
    c["NO_CHART"] = o(["CU", "CU"]) == "NO_CHART"
    c["CHART_AT_INIT"] = o(["EX", "SUP"]) == "CHART_AT_INIT"
    c["UNCERTIFIED_AT_ANCHOR"] = o(["CU", "UNC", "SUP"]) == "UNCERTIFIED_AT_ANCHOR"
    c["FINAL_NA"] = o(["CU", "EX", "UNC"]) == "FINAL_NA"
    c["UNRESOLVED"] = o(["CU", "EX", "UNR"]) == "UNRESOLVED"
    rl = [_r("CU", 0), _r("EX", 1, learn=True), _r("EX", 2), _r("SUP", 3)]
    c["learn_AFTER"] = dst.order(rl, "learning")["category"] == "AFTER"
    c["NO_LEARNING"] = dst.order([_r("EX", 0)], "learning")["category"] == "NO_LEARNING"
    c["LEARNING_BEFORE_CHART"] = dst.order(
        [_r("CU", 0, learn=True), _r("CU", 1), _r("SUP", 2)], "learning")["category"] == (
        "LEARNING_BEFORE_CHART")
    c["D1"] = [_st(_ev(["CU", "EX", s]), "D1")[0] for s in ("SUP", "EX", "UNR")] == [
        "TRUE", "FALSE", "NOT_EVALUABLE"]
    c["D3"] = _st(_ev(["CU", "EX", "SUP"]), "D3")[0] == "TRUE" and _st(
        _ev(["CU", "SUP", "SUP"]), "D3")[0] == "FALSE"
    c["D4"] = _st(_ev(rl), "D4")[0] == "TRUE" and _st(_ev(["CU", "SUP"]), "D4")[1] == [
        "NO_LEARNING"]
    c["D5"] = _st(_ev(["CU", "SUP"]), "D5")[1] == ["NO_PREDICTIVE_ONSET"] and _st(_ev(
        [_r("CU", 0), _r("SUP", 1, bp=0.1)]), "D5")[0] == "TRUE"
    inf = [_r("SUl", 0), _r("SUP", 1), _r("SUP", 2)]  # EST before the chart, informative
    uninf = [_r("SUa", 0, L_S=0.5, U_S=0.5, F_minus=Fraction(0), F_plus=Fraction(0)), _r("SUP", 1)]
    bc = ["CU", "SUP", "SUP"]
    c["D2_true_informative"] = _st(_ev(inf, bc, bc), "D2")[0] == "TRUE"
    c["D2_bc_one_two_three"] = [_st(_ev(*([bc] * 3)), "D2")] == [("NOT_EVALUABLE",
                                                               ["BY_CONSTRUCTION"])]
    c["D2_uninformative"] = _st(_ev(uninf[:1] + [_r("SUP", 1)], bc, bc), "D2")[0] in (
        "NOT_EVALUABLE", "FALSE")
    eq = _r("SUl", 0, L_S=0.5, F_minus=Fraction(1, 2) - M)
    c["equal_not_above"] = not dst.above_s(eq) and dst.above_s(
        dict(eq, L_S=math.nextafter(0.5, math.inf)))
    q = _r("SUl", 0, U_S=0.005, F_plus=M - Fraction(0.005))
    c["D2_boundary_uninformative"] = _st(_ev([q, _r("SUP", 1), _r("SUP", 2)], bc, bc), "D2") == (
        "NOT_EVALUABLE", ["UNINFORMATIVE_PRE_CHART"])
    ini = ["EX", "SUP", "SUP"]
    c["RC4_D3"] = _st(_ev(ini, ["CU", "EX", "SUP"], ["CU", "EX", "SUP"]), "D3")[0] == "NOT_EVALUABLE" \
        and _st(_ev(ini, ["CU", "SUP", "SUP"], ["CU", "SUP", "SUP"]), "D3")[0] == "FALSE"
    c["F2_D2"] = _st(_ev(ini, inf, inf), "D2") == ("NOT_EVALUABLE", ["CHART_AT_INIT"])
    c["D6_vacuous"] = _st(_ev(["CU", "EX", "EX"]), "D6")[1] == ["NO_STRONG_CROSSING"]
    est_only = [_r("CU", 0), _r("SUa", 1), _r("EX", 2), _r("SUP", 3)]
    ev = _ev(est_only)
    c["S3_est_loss_labelled"] = _st(ev, "D6")[0] != "FALSE" and any(
        v["est_loss"] for v in ev["diagnostics"].values())
    c["S1_line"] = set(ev["onset_order_line"]) == set(ev["onsets"])
    c["headroom_resource"] = {_st(_ev(["CU", "SUP"], headroom_ok=False), "D1")[1][0],
                              _st(_ev(["CU", "SUP"], resource_ok=False, headroom_ok=False),
                                  "D1")[1][0]} == {"HEADROOM", "RESOURCE"}
    x = np.random.default_rng(5).normal(size=512)
    with db.bound_hwsd():
        a = c1_means.bootstrap_means({"a": x}, dc.SEEDS["endpoint"], 50)["a"]
        b = c1_means.bootstrap_means({"a": x}, db.strong_seed(), 50)["a"]
        c["seeds"] = dc.SEEDS["endpoint"] == 620413 and db.strong_seed() == 620416 \
            and not np.array_equal(a, b) and np.array_equal(
            dsum.main_bootstrap({"a": x}, dc.SEEDS["endpoint"])["a"],
            c1_means.bootstrap_means({"a": x}, 620413, dc.DRAWS)["a"])
    d50 = c1_means.bootstrap_means({"-": x, "+": x}, 620416, dc.STRONG_DRAWS)
    sb = dsum.strong_bounds(d50["-"], d50["+"])
    c["ranks"] = (sb["L_S_rank"], sb["U_S_rank"]) == (70, 49931)
    return _res(all(c.values()), cases=c)


# --------------------------------------------------------------------------------- DRD7
def drd7(out, ctx) -> dict:
    rng = np.random.default_rng(77)
    q = {K: rng.dirichlet(np.ones(36), size=512) for K in (1, 4, 32)}
    orig, cases = hwsb_eval.model_predictive, {}

    def learn(p):
        hwsb_eval.model_predictive = lambda ck, lg, perm: p
        return ds.learning_one(None, None, None, q)

    try:
        a, b = learn(q[32]), learn(q[1])
        cases["q32"] = abs(a["captured"] - 1) <= 1e-12 and a["learn_pass"]
        cases["q1"] = abs(b["captured"]) <= 1e-12 and not b["learn_pass"]
        lo, hi = 0.0, 1.0
        for _ in range(60):
            w = (lo + hi) / 2
            c = learn(w * q[32] + (1 - w) * q[1])["captured"]
            lo, hi = (lo, w) if c >= 0.8 else (w, hi)
        r = learn(hi * q[32] + (1 - hi) * q[1])
        cases["reaches_0.8"] = r["captured"] >= 0.8 and r["learn_pass"]
        e = learn(q[4])
        cases["q4"] = e["B2_z"]["d_mean"] == 0 and e["B2_L_zS"] <= 0
        cases["z_S"] = abs(e["z_S"] - NormalDist().inv_cdf(1 - 1 / 720)) <= 1e-12 and \
            dc.Z_S == NormalDist().inv_cdf(1 - 1 / 720)
    finally:
        hwsb_eval.model_predictive = orig
    return _res(all(cases.values()), cases=cases)



# --------------------------------------------------------------------------------- DRD8
def _table(path, n=8, seed=1) -> Path:
    c = np.random.default_rng(seed).integers(0, 3, (n, 32)).astype(np.uint8)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, canon32=c, seq_ids=np.arange(n, dtype=np.int64) + seed * 1000,
             digest=np.array(scores.history_digests(c), dtype="<U64"))
    return path


def _obl(store, name="REGISTRY_OBLIGATION.json", job="DRD8", attempt=1):
    return dd.write_obligation(Path(store), name, job, attempt, UTC)


def _rewrite(store, fn, name="REGISTRY_OBLIGATION.json"):
    p = Path(store) / name
    o = json.loads(p.read_text(encoding="utf-8"))
    fn(o)
    p.write_text(json.dumps(o), encoding="utf-8")


class _Hook:
    def __init__(self, token):
        self.token, self.seen = token, []

    def __enter__(self):
        self.o = (builtins.open, io.open)

        def mk(f):
            def w(file, *a, **k):
                if self.token in str(file):
                    self.seen.append(str(file))
                return f(file, *a, **k)
            return w

        builtins.open, io.open = mk(self.o[0]), mk(self.o[1])
        return self

    def __exit__(self, *e):
        builtins.open, io.open = self.o


def drd8(out, ctx) -> dict:
    fx, c = fresh_fixture(_job(ctx), "DRD8"), {}
    ok = lambda s: s["status"] == "PASS"  # noqa: E731
    a = fx / "a"
    _table(a / "stages" / "S3" / "HIST_cal_b0.npz")
    c["r10_no_obligation"] = not ok(drd.obligation_check(a))
    _obl(a)
    c["r10_valid"] = ok(drd.obligation_check(a))
    (a / "stages" / "S4").mkdir(parents=True)
    np.savez(a / "stages" / "S4" / "ORACLE_cal.npz", m1=np.zeros(2))
    c["r10_unlisted"] = not ok(drd.obligation_check(a))
    b = fx / "b"
    _table(b / "stages" / "S3" / "HIST_cal_b0.npz")
    _obl(b)
    _rewrite(b, lambda o: o["files"][0].update({"class": "mystery"}))
    c["r10_unknown_class"] = not ok(drd.obligation_check(b))
    e = fx / "e"
    _table(e / "stages" / "S3" / "HIST_cal_b0.npz")
    _obl(e)
    _rewrite(e, lambda o: o.update({"extra": 1}))
    c["r10_mutated_key"] = not ok(drd.obligation_check(e))
    k = fx / "kd"
    k.mkdir()
    _obl(k)
    c["kd_only_store"] = ok(drd.obligation_check(k))
    u = fx / "u"
    for rel, kind in (("artifacts/WorldSpec/abc1/payload.npz", "WorldSpec"),
                      ("registry/K-REG1_digests.npz", None),
                      ("stages/SCORE/629951/s0/CHART.npz", None)):
        p = u / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        np.savez(p, x=np.zeros(3))
        if kind:
            (p.parent / "meta.json").write_text(json.dumps({"artifact_type": kind}))
    _obl(u, "REGISTRY_OBLIGATION_DRD8-a1.json", attempt=1)
    c["r10_nonhistory_pass"] = ok(drd.obligation_check(u))
    np.savez(u / "stages" / "SCORE" / "629951" / "s0" / "DECODER.npz", x=np.zeros(1))
    np.savez(u / "stages" / "SCORE" / "629951" / "s0" / "STRAY.npz", x=np.zeros(1))
    c["r10_unlisted_chart"] = not ok(drd.obligation_check(u))
    with _Hook("sealed") as h:
        (a / "sealed").mkdir()
        (a / "sealed" / "ACT.npz").write_bytes(b"never opened")
        drd.obligation_check(a)
    c["sealed_zero_opens"] = not h.seen
    # scratch-side: hwsu-dry with/without obligation, unreadable hwsu array, unlisted folder
    root, scr = fx / "root", fx / "scratch"
    (root / "agent-handoff").mkdir(parents=True)
    _table(scr / "hwsu-dry-x" / "stages" / "S3" / "DRYHIST_cal_b0.npz")
    c["hwsu_dry_no_obligation"] = not ok(drd.source_hwsu(root, scr))
    _obl(scr / "hwsu-dry-x")
    c["hwsu_dry_with_obligation"] = ok(drd.source_hwsu(root, scr))
    (scr / "hwsu-bad").mkdir()
    (scr / "hwsu-bad" / "bad.npz").write_bytes(b"not an npz")
    c["hwsu_unreadable"] = not ok(drd.source_hwsu(root, scr))
    _table(scr / "newdir" / "h.npz")
    c["unlisted_folder"] = not ok(dr.scratch_check_d(scr, table={}))
    s2 = fx / "scratch2"
    _table(s2 / "hwsd-dry-x" / "DRD1" / "20261101T000000Z" / "stages" / "S3" / "DRYHIST_cal_b0.npz")
    c["hwsd_dry_repeat"] = ok(dr.scratch_check_d(s2, readers_ok={"R5"}))
    # superset (R9 f): a K-REG2 digest missing from the build is INCOMPLETE
    hs = fx / "hwsc"
    t = _table(hs / "stages" / "S7" / "HIST_test_b0.npz", seed=2)
    dg = np.array(sorted(np.load(t)["digest"].astype(str).tolist()), dtype="<U64")
    (hs / "registry").mkdir()
    np.savez(hs / "registry" / "K-REG2_digests.npz", digests=dg)
    (hs / "registry" / "K-REG2.json").write_text(json.dumps({
        "digest_file_sha256": stage_records.sha256(hs / "registry" / "K-REG2_digests.npz")}))
    c["superset_missing"] = not ok(drd.superset_check(c2_registry.Registry(set(), None, {}, [], {}),
                                                      hs))
    c["superset_ok"] = ok(drd.superset_check(c2_registry.Registry(set(dg.tolist()), None, {}, [],
                                                                  {}), hs))
    return _res(all(c.values()), cases=c)

# --------------------------------------------------------------------------------- DRD9
def drd9(out, ctx) -> dict:
    fx, c = fresh_fixture(_job(ctx), "DRD9"), {}
    root = fx / "root"
    hs = root / "hwsc-store"
    tr = hs / "stages" / "TRAIN"
    rec = {k: v for k, v in zip(dc.TRAIN_WHITELIST, ("COMPLETE", ["x"], {"0": "i"}, {"0": "s"},
                                                      {"m": "p"}))}
    (tr / "629951").mkdir(parents=True)
    (tr / "629951" / "TRAIN_RECORD.json").write_text(json.dumps(dict(rec, dev_ce={"0": 1.5})))
    (hs / "logs").mkdir()
    (hs / "logs" / "x.json").write_text("{}")
    (fx / "scr" / "hwsc-job-0181").mkdir(parents=True)
    (fx / "scr" / "hwsc-job-0181" / "log.txt").write_text("x")
    blind = [tr / "629951" / "TRAIN_RECORD.json", hs / "logs" / "x.json",
             fx / "scr" / "hwsc-job-0181" / "log.txt"]
    c["blinded"] = all(dc.blinded(p, root, fx / "scr") for p in blind)
    c["guard_refuses"] = all(_raises(lambda p=p: dc.guard(p, root), "FAIL_TECHNICAL/BLINDNESS")
                             for p in blind[:2] + [root / "00_READ_ME_FIRST_x" / "a.pdf"])
    c["read_json_refuses"] = _raises(lambda: dc.read_json(blind[0], root),
                                     "FAIL_TECHNICAL/BLINDNESS")
    sha, r = dc.read_train_record(629951, hs)
    c["whitelist_five"] = tuple(r) == dc.TRAIN_WHITELIST and "dev_ce" not in r
    inv = {"stages/x.json": "0" * 64}
    (tr / "OBS_INVENTORY.json").write_text(json.dumps(inv))
    c["obs_wrong_sha"] = _raises(lambda: dc.read_obs_inventory(hs), "FAIL_TECHNICAL/IDENTITY")
    good = stage_records.sha256(tr / "OBS_INVENTORY.json")
    c["obs_map_only"] = dc.read_obs_inventory(hs, good) == inv
    return _res(all(c.values()), cases=c)


# --------------------------------------------------------------------------------- DRD10
def drd10(out, ctx) -> dict:
    sp = dc.CONTRACT["records"]["SCORE_ACCEPTANCE"]
    rec = {"job": "j", "master": 629951, "attempt": 1,
           "counts": {"SCORED": 6, "SCORED_UNVALIDATED": 2, "CHART_UNAVAILABLE": 3,
                      "UNCERTIFIED": 1}, "fail_technical": None, "files_sha256": {"a": "0" * 64},
           "cpu_s": 1.0, "protocol_sha256": "0" * 64, "freeze_sha256": "0" * 64, "utc": UTC}
    c = {"keys": set(sp["keys"]) == set(rec)}
    drec.acceptance_check(rec)
    c["valid_accepted"] = True
    for bad in (dict(rec, mean=0.1), dict(rec, bound=1), dict(rec, captured=1.0),
                dict(rec, counts=[("SCORED", "k=1")]), dict(rec, counts={"SCORED": 12}),
                dict(rec, files_sha256={"a": "nothex"}), {k: v for k, v in rec.items() if k != "utc"}):
        c[f"refused_{len(c)}"] = _raises(lambda b=bad: drec.acceptance_check(b),
                                          "FAIL_TECHNICAL/SEALING")
    c["value_key_nested"] = _raises(lambda: drec.no_value_check({"a": [{"L": 1}]}),
                                    "FAIL_TECHNICAL/SEALING")
    return _res(all(c.values()), cases=c)


# --------------------------------------------------------------------------------- DRD11
def drd11(out, ctx) -> dict:
    fx, c = fresh_fixture(_job(ctx), "DRD11"), {}
    stage_records.write_new(fx / "x.json", {"a": 1})
    try:
        stage_records.write_new(fx / "x.json", {"a": 2})
        c["exclusive"] = False
    except FileExistsError:
        c["exclusive"] = True
    sha = stage_records.sha256(fx / "x.json")
    drec.archive_attempt_d(fx, "job", 1, [fx / "x.json"], {})
    stage_records.write_new(fx / "x.json", {"a": 1})
    c["regenerated"] = k4b_release.regenerated_identical(sha, fx / "x.json")
    p, cd = drec.pause_check_d, drec.central_d
    c["pause"] = (p("KD", 3 * cd("KD") + 1, 0)["trigger"] == "STAGE"
                  and not p("KD", 3 * cd("KD"), 0)["pause"]
                  and p("SAMPLE", 0, 3 * drec.cumulative_d("SAMPLE") + 1)["trigger"] == "CUMULATIVE"
                  and p("SCORE", 0, 0, job_cpu=2401)["trigger"] == "MODEL"
                  and not p("SCORE", 0, 0, job_cpu=2400)["pause"])
    root = fx / "root"
    store = root / "hwsd-store"
    path, _ = dd.start_reservation_d(store, 1, UTC)
    rid = "RES-HWSD-W2-a1"
    c["start_refused_while_live"] = _raises(lambda: dd.start_reservation_d(store, 2, UTC),
                                            "INCONCLUSIVE/AUTHORITY")
    c["live_attest"] = dd.w2_attest(root)["status"] == "INCONCLUSIVE/AUTHORITY"
    c["end_needs_obligation"] = _raises(lambda: dd.end_reservation(store, rid, UTC, store / "no"),
                                        "FAIL_TECHNICAL/LINEAGE")
    ob, _ = dd.write_obligation(store, "REGISTRY_OBLIGATION.json", "DRD11", 1, UTC, rid)
    dd.end_reservation(store, rid, UTC, ob)
    c["end_once"] = _raises(lambda: dd.end_reservation(store, rid, UTC, ob),
                            "FAIL_TECHNICAL/LINEAGE")
    c["ended_attest"] = dd.w2_attest(root)["status"] == "PASS"
    raw = path.read_bytes()
    path.write_text(json.dumps(dict(json.loads(raw), start_utc="changed")), encoding="utf-8")
    c["changed_after_end_live"] = dd.w2_attest(root)["status"] == "INCONCLUSIVE/AUTHORITY"
    path.write_bytes(raw)
    other = root / "hwsu-store"
    (other / "reservations").mkdir(parents=True)
    (other / "OB.json").write_text("{}")
    r2 = other / "reservations" / "RES-HWSU-1.json"
    r2.write_text(json.dumps({"id": "RES-HWSU-1", "state": "ACTIVE"}))
    c["other_live"] = dd.w2_attest(root)["status"] != "PASS"
    stage_records.write_new(r2.with_name("RES-HWSU-1.END.json"), {
        "schema": "hws-reservation-end-v1", "reservation_id": "RES-HWSU-1",
        "reservation_file": "reservations/RES-HWSU-1.json",
        "reservation_sha256": stage_records.sha256(r2), "end_utc": UTC, "obligation_file": "OB.json",
        "obligation_sha256": stage_records.sha256(other / "OB.json"), "written_by": "u"})
    c["other_end_accepted"] = dd.w2_attest(root)["status"] == "PASS"
    s2 = root / "hwsd-store2"
    (s2 / "reservations").mkdir(parents=True)
    (s2 / "reservations" / "RES-HWSD-W2-a9.json").write_text(json.dumps(
        {"id": "RES-HWSD-W2-a9", "state": "DONE"}))
    c["not_active_refused"] = _raises(lambda: dd.end_reservation(s2, "RES-HWSD-W2-a9", UTC, ob),
                                      "FAIL_TECHNICAL/LINEAGE")
    s3 = root / "hwsd-store3"
    dd.start_reservation_d(s3, 1, UTC)  # a SAMPLE stopped by REG-D INCOMPLETE
    r = dd.stop_obligation(s3, "DRD11", 1, "RES-HWSD-W2-a1", UTC)
    o = json.loads(Path(s3 / "REGISTRY_OBLIGATION_DRD11-a1.json").read_text(encoding="utf-8"))
    c["stop_no_history"] = o["files"] == [] and r["end"]["reservation_id"] == "RES-HWSD-W2-a1"
    p2, _ = dd.start_reservation_d(s3, 2, UTC)
    c["rerun_new_id"] = p2.name == "RES-HWSD-W2-a2.json"
    return _res(all(c.values()), cases=c)
