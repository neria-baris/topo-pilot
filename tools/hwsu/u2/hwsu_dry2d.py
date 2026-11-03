"""HWSU dry run DRU-REG: the planted-defect registry fixtures of API_U2.md section 6
(R-0223-9 part 3): renamed, missing, unreadable and re-hashed S3 tables of the stage-C store,
the planted Checkpoint payload.npz and sealed/ never opened (an audit hook records zero opens),
the S-2 superset diagnostic and the K-REG2 digest file, the hwsd-store READER fixtures and the
obligation fixtures (DRO9 through read_obligation_u2, a stopped E1, the KC obligation).
Synthetic stores under the helper folder only.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_dry2c as d2c
import hwsu_records as ur
import hwsu_registry as ureg
import hwsu_regsrc as rs
import u2  # noqa: F401
import json
import sys
from pathlib import Path

import hwsc_dry
import k4b_data
import numpy as np
import stage_records

INC = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
OPENS = []
WATCH = [False]
WATCHED = ("payload.npz", "SEALED_PLANT")


def _audit(event, args):
    if WATCH[0] and event == "open" and args and any(w in str(args[0]) for w in WATCHED):
        OPENS.append(str(args[0]))


sys.addaudithook(_audit)


def _table(path, n=16, seed=1) -> None:
    rng = np.random.default_rng(seed)
    canon = rng.integers(0, 36, size=(n, 32)).astype(np.uint8)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(Path(path), canon32=canon, digest=np.array(k4b_data.digests(canon)),
                           seq_ids=np.arange(n, dtype=np.int64) + 1000 * seed)


def _contract(hist) -> dict:
    C = json.loads(json.dumps(uc.CONTRACT))
    C["stage_c_u2"]["u2_hist"] = dict(hist)
    C["stage_c_u2"]["obs_inventory"] = {"relpath": "stages/TRAIN/OBS_INVENTORY.json",
                                        "sha256": None, "stage": "TRAIN_INVENTORY"}
    return C


HIST = {"stages/S3/HIST_lgate_b0.npz": "S3", "stages/S3/HIST_cal_b0.npz": "S3",
        "stages/S3/HIST_val_b0.npz": "S3", "stages/S7/HIST_test_b0.npz": "S7"}


def hwsc_fixture(base, mutate=None, extra=None):
    """A synthetic stage-C store with the four U2 tables and the observation inventory."""
    store = Path(base)
    C = _contract(HIST)
    inv = store / "stages" / "TRAIN" / "OBS_INVENTORY.json"
    inv.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(inv, {})
    for i, rel in enumerate(HIST):
        if mutate == "unreadable" and i == 0:
            (store / rel).parent.mkdir(parents=True, exist_ok=True)
            (store / rel).write_bytes(b"not an npz file")
        else:
            _table(store / rel, seed=i + 1)
    for stage in ("TRAIN_INVENTORY", "S3", "S7"):
        files = [inv] if stage == "TRAIN_INVENTORY" else [store / r for r, s in HIST.items()
                                                          if s == stage]
        ur.complete_stage(store, stage, files)
    C["stage_c_u2"]["obs_inventory"]["sha256"] = stage_records.sha256(inv)
    first = store / next(iter(HIST))
    if mutate == "missing":
        first.unlink()
    elif mutate == "renamed":
        first.rename(first.with_name("HIST_renamed_b0.npz"))
    elif mutate == "rehash":
        first.write_bytes(first.read_bytes() + b"\0")
    for rel in extra or ():
        p = store / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"opaque payload, not an npz")
    return store, C


def s3_defects(base) -> dict:
    base, r = Path(base), {}
    st, C = hwsc_fixture(base / "ok")
    r["baseline"] = rs.source_hwsc(st, C)["status"]
    for m in ("missing", "renamed", "unreadable", "rehash"):
        st, C = hwsc_fixture(base / m, mutate=m)
        r[m] = rs.source_hwsc(st, C)["status"]
    return {"ok": r["baseline"] == "PASS" and all(r[m] == INC for m in (
        "missing", "renamed", "unreadable", "rehash")), "status": r}


def never_opened(base) -> dict:
    ck = "artifacts/Checkpoint/ck1"
    st, C = hwsc_fixture(Path(base) / "np", extra=(f"{ck}/payload.npz",
                                                     "sealed/SEALED_PLANT.npz"))
    stage_records.write_new(st / ck / "meta.json", {"artifact_type": "Checkpoint"})
    OPENS.clear()
    WATCH[0] = True
    try:
        decoy = Path(base) / "decoy_payload.npz"
        decoy.write_bytes(b"x")
        decoy.read_bytes()  # the hook must see an open
        alive = len(OPENS) >= 1
        OPENS.clear()
        out = rs.source_hwsc(st, C)
    finally:
        WATCH[0] = False
    classed = f"{ck}/payload.npz" in out["non_history"]
    return {"ok": out["status"] == "PASS" and classed and not OPENS and alive,
            "status": out["status"], "payload_classed": classed, "opens": list(OPENS)}


def kreg2(base) -> dict:
    """S-2: the K-REG2 digest file holds a digest the reader-built union lacks."""
    base, res = Path(base), {}
    missing = "f" * 64
    for tag, good in (("sha_ok", True), ("sha_bad", False)):
        d = base / tag
        st = d / "hwsc-store"
        f = st / "registry" / "K-REG2_digests.npz"
        f.parent.mkdir(parents=True, exist_ok=True)
        stage_records.save_npz(f, digests=np.array(["a" * 63 + "1", missing], dtype="<U64"),
                               seq_ids=np.array([1, 2], dtype=np.int64))
        C = json.loads(json.dumps(uc.CONTRACT))
        C["stage_c_u2"]["k_reg2"] = {"digest_file": "registry/K-REG2_digests.npz",
                                     "digest_file_sha256": stage_records.sha256(f) if good
                                     else "0" * 64}
        syn = hwsc_dry.synthetic_root(d / "syn")
        src = d2c.registry_sources()
        src["kreg2_c"] = lambda st=st, C=C: rs.source_kreg2_c(st, C)
        ho = {"store_inventory": {}, "N_C": 3072, "Z_bound": None, "F_plan": None,
              "p_D2a": 1e-15, "stage_c_exclusions": ()}
        man = ureg.build_u("K-REG1", d / "reg", syn["root"], syn["scratch"], ho, own={},
                           sources=src)
        with np.load(d / "reg" / "K-REG1_digests.npz", allow_pickle=False) as z:
            held = missing in z["digests"].astype(str).tolist()
        res[tag] = {"status": man["status"], "diag": man.get("superset_diagnostic"),
                    "held": held}
    diag = res["sha_ok"]["diag"] or {}
    ok = (res["sha_ok"]["status"] == "PASS" and res["sha_ok"]["held"]
          and diag.get("n_missing") == 1 and missing in str(diag)
          and res["sha_bad"]["status"] == INC)
    return {"ok": ok, **res}


def hwsd_reader(base) -> dict:
    """A conforming hwsd-store obligation is read (READER U5); a stray array is not."""
    base = Path(base)
    syn = hwsc_dry.synthetic_root(base / "syn")
    st = syn["root"] / "hwsd-store"
    _table(st / "stages" / "OF" / "HIST_OF_fit_b0.npz", seed=7)
    ur.write_obligation(st, "REGISTRY_OBLIGATION.json", "OF", "dru_reg", attempt=1)
    good = rs.source_hwsd(syn["root"], syn["scratch"])
    _table(st / "stages" / "OF" / "HIST_OF_eval_a1_b0.npz", seed=8)
    stray = rs.source_hwsd(syn["root"], syn["scratch"])
    return {"ok": good["status"] == "PASS" and len(good["digests"]) == 16
            and stray["status"] == INC, "good": good["status"], "stray": stray["status"]}


def obligations(base) -> dict:
    """DRO9 through read_obligation_u2, a stopped E1 and the KC obligation."""
    base, r = Path(base), {}
    full = ("artifacts/Checkpoint/ab/payload.npz", "registry/digests.npz",
            "stages/OF/ORACLE_a.npz")
    s1 = base / "c1"
    for rel in full:
        (s1 / rel).parent.mkdir(parents=True, exist_ok=True)
        stage_records.save_npz(s1 / rel, x=np.arange(3))
    _table(s1 / "stages/OF/HIST_OF_fit_b0.npz")
    ob = ur.write_obligation(s1, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    r["complete"] = rs.read_obligation_u2(s1)["status"]
    rec = json.loads(ob.read_text(encoding="utf-8"))
    s2 = base / "c2"
    s2.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(s2 / "REGISTRY_OBLIGATION_OF.json", dict(rec, extra_key=1))
    r["mutated"] = rs.read_obligation_u2(s2)["status"]
    stage_records.save_npz(s1 / "stages/OF/CHART_1.npz", x=np.arange(2))
    r["unlisted"] = rs.read_obligation_u2(s1)["status"]
    s3 = base / "c3"
    s3.mkdir(parents=True, exist_ok=True)
    ur.write_obligation(s3, "REGISTRY_OBLIGATION_OF.json", "OF", "dro9", attempt=1)
    r["records_only"] = rs.read_obligation_u2(s3)["status"]
    sr = d2c.synthetic_root_u(base / "jobs")
    store = uc.SCRATCH / f"hwsu-dry-u2-{abs(hash(str(base))) % 10**8}-ob"
    k = d2c.run_stage(store, sr, "DRU-OB-KC", "KC", d2c.planted_default(sr))
    r["kc_obligation"] = [p.name for p in store.glob("REGISTRY_OBLIGATION_KC*.json")]
    r["kc_reader"] = rs.read_obligation_u2(store)["status"]
    bad = {"H1-U": lambda ctx: (_ for _ in ()).throw(ValueError("planted stop before S3"))}
    e1 = d2c.run_stage(store, sr, "DRU-OB-E1", "E1", dict(d2c.planted_default(sr), **bad),
                       reservation_id="RES-HWSU-U", dry_continue=False)
    ur.write_reservation(store, "RES-HWSU-U-a2", uc.SCOPE_DRY, ur.utc(), "dru_reg")
    r["e1_stopped"] = {"rows_drawn": e1["result"]["rows_drawn"],
                       "reservation_ended": (store / "reservations" /
                                             "RES-HWSU-U.END.json").is_file(),
                       "rerun_reservation": (store / ur.reservation_file(
                           "RES-HWSU-U-a2")).is_file(),
                       "reader": rs.read_obligation_u2(store)["status"]}
    ok = (r["complete"] == "PASS" and r["mutated"] == INC and r["unlisted"] == INC
          and r["records_only"] == "PASS" and r["kc_obligation"] and k["gates"]
          and r["kc_reader"] == "PASS" and not r["e1_stopped"]["rows_drawn"]
          and r["e1_stopped"]["reservation_ended"] and r["e1_stopped"]["rerun_reservation"]
          and r["e1_stopped"]["reader"] == "PASS")
    return {"ok": bool(ok), **r}


def rerun(base) -> dict:
    """R-0223-10 item 2: E1 fails after REG1 (attempt 1); the pre-attempt archive moves its
    outputs to superseded/<job>-a1/ with SHA256SUMS and attempt 2 passes on RES-HWSU-U-a2."""
    base = Path(base)
    sr = d2c.synthetic_root_u(base / "jobs")
    store = uc.SCRATCH / f"hwsu-dry-u2-{abs(hash(str(base))) % 10**8}-rr"
    pl = d2c.planted_default(sr)
    d2c.run_stage(store, sr, "DRU-RR-KC", "KC", pl)
    bad = {"S3": lambda ctx: (_ for _ in ()).throw(ValueError("planted failure after REG1"))}
    a1 = d2c.run_stage(store, sr, "DRU-RR", "E1", dict(pl, **bad), reservation_id="RES-HWSU-U",
                       dry_continue=False)
    (store / "RELEASE_A.json").unlink()  # the coordinator issues a new release per attempt
    a2 = d2c.run_stage(store, sr, "DRU-RR", "E1", pl, reservation_id="RES-HWSU-U-a2", attempt=2)
    arch = store / "superseded" / "DRU-RR-a1"
    sums = (arch / "SHA256SUMS").read_text(encoding="utf-8").splitlines() if arch.is_dir() else []
    moved = [ln.partition("  ")[2] for ln in sums if ln.strip()]

    ok = (a1["result"]["outcome"] != "E1_PASS" and a2["result"]["outcome"] == "E1_PASS"
          and a2["result"]["archived"] == str(arch)
          and "registry/K-REG1.json" in moved and not ur.lineage_u(store).get("bad"))
    return {"ok": bool(ok), "attempt1": a1["result"]["outcome"],
            "attempt2": a2["result"]["outcome"], "archived": moved[:6]}


def fixtures(base) -> dict:
    base = Path(base)
    out = {"s3_tables": s3_defects(base / "s3"), "never_opened": never_opened(base / "nv"),
           "kreg2": kreg2(base / "k2"), "hwsd": hwsd_reader(base / "hd"),
           "obligations": obligations(base / "ob"), "rerun": rerun(base / "rr")}
    return {"ok": all(v["ok"] for v in out.values()), **out}
