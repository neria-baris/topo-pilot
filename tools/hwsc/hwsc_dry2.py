"""HWSC dry-run cases DRC5-DRC14 (API.md §8; protocol §7; TEST_PLAN §4; rulings R-0176-G1..G5,
G9, G12). Split from hwsc_dry by size; every case is synthetic and reads EXACT."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
import math
from fractions import Fraction

import hwsb_eval
import hwsb_known
import hwsb_law
import hwsc_bind
import hwsc_data
import hwsc_gates
import hwsc_records
import hwsc_registry
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure
from hwsc_dry import _mem, case_dir



def _res(ok, **details) -> dict:
    return {"status": "PASS" if ok else "FAIL", "details": json.loads(json.dumps(details,
                                                                                default=str))}


def _raises(fn, status=None) -> bool:
    try:
        fn()
    except C1GateFailure as exc:
        return status is None or exc.status == status
    return False


# ------------------------------------------------------------------------- DRC5 decision
def drc5(out, ctx) -> dict:
    """Planted endpoint fixtures: decision boundaries in exact Fractions and the annotation."""
    M, F = Fraction(1, 100), Fraction(1, 2**30)
    cases = {}
    with hwsc_bind.bound_stage_c():
        ms = cc.MASTERS

        def st(L, U, Fm=F, Fp=F):
            return k4b_stats.model_status(L, U, Fm, Fp)

        cases["support"] = (
        k4b_stats.overall({j: st(0.05, 0.06)["status"] for j in ms})
        == "SUPPORT")
        cases["exclusion"] = (
        k4b_stats.overall({j: st(0.0, 0.005)["status"] for j in ms})
        == "EXCLUSION")
        cases["mixed"] = k4b_stats.overall(dict(zip(ms, ("SUPPORT", "EXCLUDE",
                                                         "UNRESOLVED")))) == "MIXED"
        cases["numerical"] = (
        st(0.0105, 0.02, Fraction(1, 1000), Fraction(0))["status"]
        == "UNRESOLVED/NUMERICAL")
        cases["negative"] = "NEGATIVE_ALIGNMENT" in st(-0.05, -0.02)["labels"]
        cases["boundary_L"] = st(0.02, 0.03, Fraction(0.02) - M)["status"].startswith("UNRESOL")
        cases["boundary_U"] = st(0.0, 0.005, F, M - Fraction(0.005))["status"].startswith("UNRES")
    pbm = hwsc_gates.positive_below_margin
    L0 = 0.003
    up = math.nextafter(L0, math.inf)
    F0 = Fraction(L0)
    cases["zero_not_positive"] = not pbm({1: {"L": L0, "F_minus": F0, "status": "EXCLUDE"}}
                                         )["positive"][1]
    cases["ulp_positive"] = pbm({1: {"L": up, "F_minus": str(F0), "status": "EXCLUDE"}}
                                )["per_model"][1] == "EXCLUDE"
    cases["unresolved_kind"] = pbm({1: {"L": up, "F_minus": F0, "status": "UNRESOLVED"}}
                                   )["per_model"][1] == "UNRESOLVED"
    cases["support_not_annotated"] = pbm({1: {"L": 0.5, "F_minus": F0, "status": "SUPPORT"}}
                                         )["per_model"][1] is None
    res = {"overall": "EXCLUSION", "per_model": {j: {"L": up, "F_minus": F0,
                                                     "status": "EXCLUDE", "labels": []}
                                                 for j in cc.MASTERS}}
    oc = hwsc_gates.outcome({"endpoint": res})
    cases["overall_annotation"] = (
        "POSITIVE_BELOW_MARGIN" in oc["annotations"]
        and oc["outcome"] == "EXCLUSION")
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ---------------------------------------------------------------------------- DRC6 ladder
def drc6(out, ctx) -> dict:
    cases = {}
    for nc in (3072, 6144):
        for n1 in (3072, 6144, 12288, None):
            r = hwsc_gates.choose_N(nc, {"N": n1})
            want = None if n1 is None else max(nc, n1)
            cases[f"{nc}/{n1}"] = r["N"] == want and (n1 is not None or r["status"] ==
                                                     "INCONCLUSIVE/UNDERPOWERED")
    rng = np.random.default_rng(66)
    Xm = {j: rng.normal(0.0, 0.08, 3072) for j in cc.MASTERS}
    Xp = {j: Xm[j] + np.abs(rng.normal(0, 0.01, 3072)) for j in cc.MASTERS}
    r4 = {j: np.abs(rng.normal(0.2, 0.05, 3072)) for j in cc.MASTERS}
    F = Fraction(1, 10**4)
    import hwsb_gates

    a = hwsc_gates.p1c_ladder(Xm, Xp, r4, F, None)
    b = hwsb_gates.ladder_pilot(Xm, Xp, r4, F, models=cc.MASTERS, seeds=(610101, 610105),
                                ladder=cc.LADDER)
    cases["seed_sensitive"] = a["sdU"] != b["sdU"]
    sh = hwsc_gates.p1c_ladder({j: x + 0.3 for j, x in Xm.items()},
                               {j: x + 0.3 for j, x in Xp.items()}, r4, F, None)
    cases["shift_invariant"] = all(
        sh["candidates"][N]["projection"] == a["candidates"][N]["projection"]
        for N in a["candidates"])
    return _res(all(cases.values()), cases=cases, reading="EXACT",
                seeds_note="620311/620315 on synthetic arrays only (R-0176-G5)")


# ------------------------------------------------------------------------------- DRC7 L1
def drc7(out, ctx) -> dict:
    rng = np.random.default_rng(77)
    n = 512
    q = {K: rng.dirichlet(np.ones(36), size=n) for K in (1, 4, 32)}
    cases = {"q32": abs(hwsb_eval.b1(q, q[32])["captured"] - 1) <= 1e-12,
             "q1": abs(hwsb_eval.b1(q, q[1])["captured"]) <= 1e-12}
    lo, hi = 0.0, 1.0
    for _ in range(60):
        w = (lo + hi) / 2
        c = hwsb_eval.b1(q, w * q[32] + (1 - w) * q[1])["captured"]
        lo, hi = (lo, w) if c >= 0.8 else (w, hi)
    r = hwsb_eval.b1(q, hi * q[32] + (1 - hi) * q[1])
    cases["boundary_pass"] = r["captured"] >= 0.8 and r["status"] == "PASS"
    d = case_dir(out, "DRC7")
    calls = []
    orig = (hwsb_eval.model_predictive, hwsb_eval.oracle_predictives)
    pred = {cc.MASTERS[0]: q[1], cc.MASTERS[1]: q[32], cc.MASTERS[2]: q[32]}
    try:
        hwsb_eval.oracle_predictives = lambda proc, lg: q
        hwsb_eval.model_predictive = lambda ck, lg, perm: calls.append(ck) or pred[ck]
        c = {"proc": {"perm": {j: None for j in cc.MASTERS}}, "tables": {"lgate": {
            "canon32": None}}, "ckpts": {(j, 5000): j for j in cc.MASTERS}}
        recs = hwsc_records.run_gates_c(d, [("L1", lambda: hwsc_gates.l1(d, c)),
                                            ("ORACLE-VAL", lambda: {"status": "PASS"})])
    finally:
        hwsb_eval.model_predictive, hwsb_eval.oracle_predictives = orig
    l1 = stage_records.gates_so_far(d)
    cases["not_learned_1of3"] = recs[0]["status"] == "INCONCLUSIVE/NOT_LEARNED" and \
        len(calls) == 3 and "1/3" in recs[0]["reason"]
    cases["later_not_run"] = recs[1]["status"] == "NOT_RUN" and len(l1) == 2
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ---------------------------------------------------------------------------- DRC8 law
def drc8(out, ctx) -> dict:
    cases = {}
    w0 = hwsb_known.w0_process()
    law0 = hwsb_law.law_bound(w0["T"], w0["E_canon_shared"], w0["pi"], w0["coords"],
                              Fraction(5, 4), Fraction(1, 5))
    cases["w0_delta0"] = law0["delta"] == 0 and law0["Z_bound"] == Fraction(
        cc.CONTRACT["known_cases"]["KC4"]["w0_Z_bound"])
    star = hwsc_data.build_process_c(_mem())
    h = cc.load_handoff()
    li = hwsc_gates.law_identity(star, h)
    cases["star_bounded_equal"] = li["Z_bound"] == h["Z_bound"]
    z = h["Z_bound"]
    planted = dict(h, Z_bound=Fraction(z.numerator + 1, z.denominator))
    cases["planted_refused"] = _raises(lambda: hwsc_gates.law_identity(star, planted),
                                       "FAIL_TECHNICAL/LAW_BOUND")
    fx = {"stage_c_exclusions": ("aaaa000011112222",)}
    cases["exclusion"] = not hwsc_gates.exclusion_check(["aaaa000011112222"], fx)["ok"] and \
        hwsc_gates.exclusion_check(["bbbb"], fx)["ok"]
    return _res(all(cases.values()), cases=cases, reading="EXACT")


# ------------------------------------------------------------------------- DRC9 registry
def _c2_table(path, digests, seq):
    d = np.array(digests, dtype="<U64")
    stage_records.save_npz(path, digest_H=d, digest_Hp=d, digest_Hm=d,
                           digest_HY=np.array([""] * len(d), dtype="<U64"),
                           sequence_id=np.asarray(seq, dtype=np.int64))


def drc9(out, ctx) -> dict:
    import c2_registry
    import x6s1_registry
    from hwsc_dry import stub_sources, synthetic_root

    d = case_dir(out, "DRC9")
    cases, rng = {}, np.random.default_rng(9)
    hexes = [bytes(rng.integers(0, 256, 32, dtype=np.uint8)).hex() for _ in range(4)]
    c2n = d / "syn" / "c2nd-store"
    (c2n / "hist").mkdir(parents=True)
    (c2n / "sealed").mkdir()
    _c2_table(c2n / "hist" / "HIST_fit_b0.npz", hexes[:2], [1, 2])
    (c2n / "sealed" / "ACT.npz").write_bytes(b"never opened")
    bound = {"hist/HIST_fit_b0.npz": stage_records.sha256(c2n / "hist" / "HIST_fit_b0.npz")}
    r2 = hwsc_registry.source_c2nd(c2n, bound)
    cases["R2"] = r2["status"] == "PASS" and set(hexes[:2]) <= r2["digests"]
    (c2n / "stray.npz").write_bytes(b"x")
    cases["R2_unlisted"] = hwsc_registry.source_c2nd(c2n, bound)["status"] != "PASS"
    dry = d / "syn" / "hwsb-dry-x"
    (dry / "a").mkdir(parents=True)
    tok = rng.integers(0, 3, (16, 32)).astype(np.uint8)
    np.savez(dry / "a" / "VAL.npz", canon32=tok)
    r5 = hwsc_registry.source_dry([dry])
    cases["R5"] = r5["status"] == "PASS" and set(
        __import__("scores").history_digests(tok)) <= r5["digests"]
    (dry / "a" / "BAD.npz").write_bytes(b"not an npz")
    cases["R5_unreadable"] = hwsc_registry.source_dry([dry])["status"] != "PASS"
    syn = synthetic_root(d / "syn2")
    (syn["scratch"] / "newdir").mkdir()
    np.savez(syn["scratch"] / "newdir" / "h.npz", canon32=tok)
    cases["R6_unlisted"] = hwsc_registry.scratch_check(syn["scratch"], table={})["status"] != \
        "PASS"
    (syn["scratch"] / "hwsb-empty").mkdir()
    t = {"newdir": {"decision": "READER", "readers": ["R5"], "frozen_files": {
        "h.npz": "history"}}, "hwsb-empty": {"decision": "EXCLUSION", "frozen_files": {}}}
    cases["R6_frozen"] = hwsc_registry.scratch_check(syn["scratch"], t, {"R5"})["status"] == \
        "PASS"
    np.savez(syn["scratch"] / "hwsb-empty" / "late.npz", canon32=tok)
    cases["R6_empty_fail_closed"] = hwsc_registry.scratch_check(
        syn["scratch"], t, {"R5"})["status"] != "PASS"
    hd = {"store_inventory": {}}
    m = hwsc_registry.build("K-REG1", d / "store" / "registry", root=syn["root"],
                            scratch=syn["scratch"], handoff=hd, own_expected={},
                            sources=stub_sources(hexes[2:]))
    reg = c2_registry.Registry.load(d / "store", "K-REG1")
    cases["build_loadable"] = m["status"] == "PASS" and bool(reg.contains(
        np.array(hexes[2:3], "<U64"))[0])
    big = d / "scale"
    planted = rng.integers(0, 256, (1, 32), dtype=np.uint8)

    def chunks():
        g = np.random.default_rng(99)
        for i in range(20):
            c = g.integers(0, 256, (1_000_000, 32), dtype=np.uint8)
            if i == 7:
                c[123] = planted[0]
            yield c

    ds = x6s1_registry.DigestSet.build(chunks(), big)
    r = c2_registry.Registry(set(), ds, {}, [], {})
    fresh = np.random.default_rng(5).integers(0, 256, (1, 32), dtype=np.uint8)
    hx = np.array([bytes(planted[0]).hex(), bytes(fresh[0]).hex()], "<U64")
    hit = r.contains(hx)
    cases["scale"] = ds.n >= 20_000_000 and bool(hit[0]) and not bool(hit[1])
    return _res(all(cases.values()), cases=cases, reading="EXACT")


from hwsc_dry3 import drc10, drc11, drc12, drc13, drc14  # noqa: E402,F401  (split by size)
