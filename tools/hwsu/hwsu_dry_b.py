"""HWSU dry run DRO5-DRO9 and the J11 obligation reader fixture (API.md §10; split from hwsu_dry by
size, API erratum; every name is reachable as hwsu_dry.<name>)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_dry as dry
import hwsu_of as uof
import hwsu_oracle as uo
import hwsu_pairs as up
import hwsu_records as ur
import hwsu_seed as us
import copy
import json
from pathlib import Path

import c2_decide
import numpy as np
import stage_records
from c1_records import C1GateFailure

SEEDS = uc.DRY_SEEDS_OF


def obligation_reader_fixture(store) -> dict:
    return ur.read_obligation(store)


def _lemma_ctx(w, a1, a2) -> dict:
    T, E, pi, co = w["T"], w["E_canon_shared"], w["pi"], w["coords"]
    o1, o2 = uo.arm_oracle(T, E, pi, a1, co), uo.arm_oracle(T, E, pi, a2, co)
    s1 = uo.suffix_oracle(T, E, pi, [a1, a2], co)[0]
    return {"o1": o1, "o2": o2, "s1": s1, "pc": uo.pair_core(o1, o2), "seeds": SEEDS, "draws": 300}


def dro5(base) -> dict:
    w, pr = dry.tiny_pairs(2048)
    real = uof.of_5(_lemma_ctx(w, pr["a1"], pr["a2"]))
    orig = up.bridge
    up.bridge = lambda pi, beta: np.tile(np.asarray(pi), (len(beta), 1))
    try:
        biased = up.sample_pairs(w["T"], w["E_canon_shared"], w["pi"], uc.SCOPE_DRY, "of-eval",
                                 0, 2048)
    finally:
        up.bridge = orig
    bad = uof.of_5(_lemma_ctx(w, biased["a1"], biased["a2"]))
    ok = real.get("status", "PASS") == "PASS" and bad.get("status") == "FAIL_TECHNICAL/SAMPLER"
    return {"status": "PASS" if ok else "FAIL", "details": {
        "real": {q: real[q]["ok"] for q in "UG"}, "biased_status": bad.get("status")}}


def dro6(base) -> dict:
    root = Path(base) / "root"
    plant = {"hwsd-store/secret.json": 1, "hwsc-store/stages/S8/x.json": 1,
             "hwsc-store/stages/S5/x.json": 1, "agent-handoff/jobs/hws-dyn-x/a.md": 1,
             "agent-handoff/records/HWSD_x.json": 1, "00_READ_ME_FIRST_x/x.md": 1,
             "hwsd-store/reservations/a.json": 0, "tools/hwsu/ok.py": 0, "other/stray.md": 0}
    for rel in plant:
        dry._w(root / rel, '{"scope": "hwsu-v1"}\n')
    opened = []
    us.open = lambda f, *a, **k: (opened.append(str(f)), open(f, *a, **k))[1]
    try:
        hits = us.seed_search_u(root, us.needles())
    finally:
        del us.open
    blinded_opens = [p for p in opened if uc.blinded(p, root) or uc.public_summary(p)]
    c = us.classify_hits_u(hits, ["/tools/hwsu/", "/hwsd-store/"], [])
    kinds = {Path(h["path"]).relative_to(root).as_posix(): h["kind"] for h in c["hits"]}
    ok = (not blinded_opens and "other/stray.md" in kinds
          and kinds["other/stray.md"] == "unclassified"
          and c["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
          and kinds.get("tools/hwsu/ok.py") == "hwsu_declaration"
          and "hwsd-store/reservations/a.json" in kinds and "hwsd-store/secret.json" not in kinds)
    return {"status": "PASS" if ok else "FAIL", "details": {
        "blinded_opens": blinded_opens, "kinds": kinds, "status": c["status"]}}


def _freeze_record(repo: Path) -> dict:
    C = uc.CONTRACT
    files = {p: ur._sha((repo / p).read_bytes()) for p in C["phase1_files"]
             if (repo / p).is_file()}
    h = lambda n: ur._sha((repo / "tools" / "hwsu" / n).read_bytes())  # noqa: E731
    return {"implementation_files": files,
            "api_bytes": (repo / "tools/hwsu/API.md").stat().st_size,
            "test_plan_bytes": (repo / "tools/hwsu/TEST_PLAN.md").stat().st_size,
            "protocol_sha256": h("PROTOCOL_HWSU_v1.md"),
            "contract_of_sha256": h("CONTRACT_OF.json"),
            "reuse_sha256": dict(C["reuse_sha256"])}


def dro7(base) -> dict:
    base, det = Path(base), {}
    # OF-H planted sealed-D-2a row: the stop comes before any oracle value
    z = np.zeros((4, 32), dtype=np.uint8)
    det["of_h"] = uof.of_h({"fit": {"canon32": z}, "eval": {"a1": z, "a2": z}}).get("status")
    # OF-B refusal after a phase-1 file change past FREEZE_OF
    rec, good, bad = _freeze_record(uc.REPO), base / "freeze_ok", base / "freeze_bad"
    for d in (good, bad):
        d.mkdir(parents=True, exist_ok=True)
    tam = copy.deepcopy(rec)
    k = next(iter(tam["implementation_files"]))
    tam["implementation_files"][k] = "0" * 64
    stage_records.write_new(good / "FREEZE_OF.json", rec)
    stage_records.write_new(bad / "FREEZE_OF.json", tam)
    det["freeze_ok"] = ur.verify_freeze_of(good, uc.REPO)["status"]
    try:
        ur.verify_freeze_of(bad, uc.REPO)
        det["freeze_bad"] = "accepted"
    except C1GateFailure as exc:
        det["freeze_bad"] = exc.status
    # a track-D token overlapping an HWSU token
    u, d = uc.CONTRACT["namespace"]["U"], copy.deepcopy(uc.CONTRACT["namespace"]["D_declared"])
    det["overlap_clean"] = us.namespace_overlap(u, d)
    d["scopes"].append("hwsu-v1")
    det["overlap_planted"] = bool(us.namespace_overlap(u, d))
    # J8: end_reservation and attestation incl. a track-D-form end record
    sr = dry.synthetic_root(base / "j8")
    root, mb, C = sr["root"], sr["mailbox"], sr["contract"]
    w2 = dict(w2_end=mb / "records" / "HWSC_W2_END.json",
              w2_end_sha256=C["authority"]["records"]["HWSC_W2_END"]["sha256"])
    st = sr["hwsu_store"]
    ur.write_reservation(st, "RES-HWSU-OF", uc.SCOPE_DRY, ur.utc(), "hwsu_dry.dro7")
    live = ur.w2_attestation(root, **w2)
    own = ur.w2_attestation(root, own="RES-HWSU-OF", **w2)
    ob = ur.write_obligation(st, "REGISTRY_OBLIGATION_OF.json", "OF", "hwsu_dry.dro7", dry=True,
                             attempt=1, reservation_id="RES-HWSU-OF")
    ur.end_reservation(st, "RES-HWSU-OF", ur.utc(), ob)
    ended = ur.w2_attestation(root, **w2)
    try:
        ur.end_reservation(st, "RES-HWSU-OF", ur.utc(), ob)
        again = "accepted"
    except C1GateFailure as exc:
        again = exc.status
    hd = root / "hwsd-store"
    dry._w(hd / "RESERVATION_D.json", json.dumps({"id": "RES-HWSD-X", "state": "ACTIVE"}))
    dry._w(hd / "REGISTRY_OBLIGATION.json", json.dumps({"fixture": True}))
    dry._w(hd / "reservations" / "RES-HWSD-X.END.json", json.dumps({
        "schema": "hws-reservation-end-v1", "reservation_id": "RES-HWSD-X",
        "reservation_file": "hwsd-store/RESERVATION_D.json",
        "reservation_sha256": dry._h(hd / "RESERVATION_D.json"), "end_utc": ur.utc(),
        "obligation_file": "hwsd-store/REGISTRY_OBLIGATION.json",
        "obligation_sha256": dry._h(hd / "REGISTRY_OBLIGATION.json"), "written_by": "track D"}))
    dform = ur.w2_attestation(root, **w2)
    det["j8"] = {"live": live["status"], "own_excluded": own["status"], "ended": ended["status"],
                 "again": again, "d_form": dform["status"], "d_ended": dform["ended"]}
    dstore = Path(base) / "dstore"
    dstore.mkdir(parents=True, exist_ok=True)
    ur.write_obligation(dstore, "REGISTRY_OBLIGATION.json", "DRO", "hwsu_dry.dro7", dry=True)
    ok = (det["of_h"] == "INCONCLUSIVE/REGISTRY_INCOMPLETE" and det["freeze_ok"] == "PASS"
          and det["freeze_bad"] == "INVALID" and det["overlap_clean"] == []
          and det["overlap_planted"] and live["status"] == "INCONCLUSIVE/AUTHORITY"
          and own["status"] == "PASS" and ended["status"] == "PASS"
          and again == "FAIL_TECHNICAL/LINEAGE" and dform["status"] == "PASS"
          and dform["ended"].get("RES-HWSD-X") == "b")
    return {"status": "PASS" if ok else "FAIL", "details": det}


def dro8(base) -> dict:
    g = ["OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2", "OF-3", "OF-4", "OF-5"]
    rec = lambda **ov: [{"gate": x, "status": ov.get(x, "PASS")} for x in g]  # noqa: E731
    rng = np.random.default_rng(SEEDS["share"])
    G = 1.0 + 0.1 * rng.standard_normal(2048)
    Z = 0.1 * G + 0.01 * rng.standard_normal(2048) - 0.2 * G
    b, _ = uof._bounds({"Z": Z}, SEEDS["share"], uc.ALPHA_VAL, 300)
    planted = "PASS" if c2_decide.sign(b["Z"]["L"], c2_decide.guard(Z)) == 1 else "SHARE_DROPPED"
    out = {"planted_of3": planted,
           "dropped": uof.of_outcome(rec(**{"OF-3": planted, "OF-4": "SHARE_DROPPED"})),
           "plain": uof.of_outcome(rec()),
           "resp_fail": uof.of_outcome(rec(**{"OF-4": "INCONCLUSIVE/ORACLE_FEASIBILITY"}))}
    ok = (planted == "SHARE_DROPPED" and out["dropped"] == "OF_PASS_RESPONSE_ONLY"
          and out["plain"] == "OF_PASS" and out["resp_fail"] == "INCONCLUSIVE/ORACLE_FEASIBILITY")
    return {"status": "PASS" if ok else "FAIL", "details": out}


def _arr(path, **kw):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(Path(path), **(kw or {"x": np.arange(3)}))


def dro9(base) -> dict:
    base, res = Path(base), {}
    full = ("artifacts/Checkpoint/ab/payload.npz", "artifacts/EmissionSpec/cd/payload.npz",
            "registry/digests.npz", "stages/OF/ORACLE_a.npz", "stages/OF/HIST_OF_fit_b0.npz")
    s1 = base / "c1"
    for r in full:
        _arr(s1 / r)
    ob = ur.write_obligation(s1, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    res["1_complete"] = obligation_reader_fixture(s1)["status"]
    rec = json.loads(ob.read_text(encoding="utf-8"))
    res["1_checkpoint_sha_null"] = [e["sha256"] for e in rec["files"] if "Checkpoint" in e[
        "relpath"]] == [None]
    mut = dict(rec, extra_key=1)
    s1m = base / "c1m"
    s1m.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(s1m / "REGISTRY_OBLIGATION_OF.json", mut)
    res["1_mutated"] = obligation_reader_fixture(s1m)["status"]
    s2 = base / "c2"
    for r in full:
        _arr(s2 / r)
    ur.write_obligation(s2, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    _arr(s2 / "stages/OF/CHART_1.npz")
    res["2_unlisted"] = obligation_reader_fixture(s2)["status"]
    s3 = base / "c3"
    s3.mkdir(parents=True, exist_ok=True)
    ur.write_obligation(s3, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    res["3_records_only"] = obligation_reader_fixture(s3)["status"]
    s4 = base / "c4"
    for r in full:
        _arr(s4 / r)
    ur.write_obligation(s4, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    new = json.loads((s4 / "REGISTRY_OBLIGATION_OF.json").read_text(encoding="utf-8"))
    new["files"] = new["files"][:-1]
    new["written_utc"] = "2999-01-01T00:00:00Z"
    stage_records.write_new(s4 / "REGISTRY_OBLIGATION_OF-a2.json", new)
    res["4_newer_omits"] = obligation_reader_fixture(s4)["status"]
    s5 = base / "c5"
    ur.write_reservation(s5, "RES-HWSU-OF", uc.SCOPE_DRY, ur.utc(), "dro9")
    nm = ur.obligation_name("OF", 1)
    o5 = ur.write_obligation(s5, nm, "OF", "dro9", attempt=1, reservation_id="RES-HWSU-OF")
    ur.end_reservation(s5, "RES-HWSU-OF", ur.utc(), o5)
    ur.write_reservation(s5, "RES-HWSU-OF-a2", uc.SCOPE_DRY, ur.utc(), "dro9")
    res["5_rerun"] = {"end": (s5 / "reservations" / "RES-HWSU-OF.END.json").is_file(),
                      "reader": obligation_reader_fixture(s5)["status"],
                      "file": ur.reservation_file("RES-HWSU-OF-a2")}
    s6 = base / "c6"
    _arr(s6 / "stages/OF/ORACLE_a.npz")
    res["6_aborted"] = obligation_reader_fixture(s6)["status"]
    ur.write_obligation(s6, "REGISTRY_OBLIGATION.json", "DRO", "coordinator", dry=True)
    res["6_after_coordinator"] = obligation_reader_fixture(s6)["status"]
    try:
        ur.save_array(base / "c7", "stages/X/OTHER_1.npz", x=np.arange(2))
        res["7_other"] = "accepted"
    except C1GateFailure as exc:
        res["7_other"] = exc.status
    inc = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
    ok = (res["1_complete"] == "PASS" and res["1_checkpoint_sha_null"] and
          res["1_mutated"] == inc and res["2_unlisted"] == inc and res["3_records_only"] == "PASS"
          and res["4_newer_omits"] == inc and res["5_rerun"]["end"]
          and res["5_rerun"]["reader"] == "PASS" and res["6_aborted"] == inc
          and res["6_after_coordinator"] == "PASS" and res["7_other"] == "FAIL_TECHNICAL/LINEAGE")
    return {"status": "PASS" if ok else "FAIL", "details": res}
