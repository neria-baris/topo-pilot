"""HWSC data: process, train/dev mirror, evaluation blocks, H2, H2-FRESH, registry risk
(API.md §3; protocol §2.3, §2.4, §3.3, §3.4). Reused functions are called through their module
attributes at call time, so the binding of hwsc_bind applies."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import c2_registry
import hwsb_config
import hwsb_data
import hws_exact
import k4b_data
import k4b_driver
import k4b_fresh
import k4b_release
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import check_disjoint, make_sequence_ids, process_code
from topo_pilot.dataset.public import assert_public

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"


# ------------------------------------------------------------------------------ process (§3.1)
def build_process_c(store, masters=cc.MASTERS) -> dict:
    return hwsb_data.build_process(store, masters=tuple(int(m) for m in masters))


def process_identity(store, proc) -> dict:
    w = cc.CONTRACT["world"]
    ck = hwsb_data.spec_checksums(store, proc)
    sel = cc.read_json(cc.SELECTION_PATH)["sha256"]
    sha = hwsb_data.arrays_sha256(proc)
    checks = {
        "world_id": proc["ids"]["world"] == w["WorldSpec"]["id"],
        "transition_id": proc["ids"]["transition"] == w["TransitionSpec"]["id"],
        "world_payload": ck["WorldSpec"] == w["WorldSpec"]["payload_sha256"],
        "transition_payload": ck["TransitionSpec"] == w["TransitionSpec"]["payload_sha256"],
        "selection_equals_contract": sel == w["selection_sha256"],
    }
    for k in ("E", "T", "pi", "coords"):
        checks[f"sha_{k}"] = sha[k] == sel.get(k) == w["selection_sha256"][k]
    for m, e in proc["E_canon"].items():
        h = hwsb_data.arrays_sha256({"T": proc["T"], "E_canon_shared": e, "pi": proc["pi"],
                                     "coords": proc["coords"]})["E"]
        checks[f"E_canon_{m}"] = h == sel.get("E")
    return {"ok": all(checks.values()), "checks": checks, "ids": proc["ids"],
            "spec_checksums": ck, "arrays_sha256": sha}


# ---------------------------------------------------------------------- train/dev mirror (§3.1)
def sequence_ids_c(role, n, plan, master, scope=cc.SCOPE) -> np.ndarray:
    if role not in ("train", "dev"):
        raise ValueError(f"sequence_ids_c serves train/dev only, not {role!r}")
    hwsb_data.stream_record(role, plan, master)  # the role/master refusals
    rep = f"{scope}/DRY/{plan.key}/{role}/{int(master)}" if plan.dry else \
        f"{scope}/{role}/{int(master)}"
    return make_sequence_ids(process_code(*plan.process, rep), role, int(n))


def make_train_dev_c(store, proc, master, plan, scope=cc.SCOPE) -> dict:
    """hwsb_data.make_train_dev line for line, with `scope` in place of the literal hwsb-v1."""
    m, tree = int(master), SeedTree(int(master))
    tok, ids, reps = {}, {}, {}
    for split in ("train", "dev"):
        n = int(plan.sizes[split])
        tok[split] = hwsb_data.sample_observations(
            proc["T"], proc["E_named"][m], proc["pi"], proc["perm"][m], n,
            hwsb_data.data_generator(split, plan, m, tree), split)
        ids[split] = sequence_ids_c(split, n, plan, m, scope)
        reps[split] = (f"{scope}/DRY/{plan.key}/{split}/{m}" if plan.dry
                       else f"{scope}/{split}/{m}")
    check_disjoint(train=ids["train"], dev=ids["dev"])
    out = {"streams": {}, "n": {}, "replicates": reps}
    for split in ("train", "dev"):
        obs = assert_public(
            ObservationSet(split=split, V=proc["V"], sequence_id=ids[split], tokens=tok[split]))
        cfg = {"family": "cylinder", "mode": "overlap", "sigma": plan.process[2],
               "V": proc["V"], "N": proc["N"], "split": split, "n": int(plan.sizes[split]),
               "replicate": m, "study": hwsb_config.SCOPE, "key": plan.key}
        out[split] = store.save(obs, config=cfg,
                                parents=[proc["ids"]["transition"], proc["ids"]["emission"][m]],
                                seed_map=dict(tree.issued), consumer="dataset")
        out["streams"][split] = hwsb_data.stream_record(split, plan, m)
        out["n"][split] = int(plan.sizes[split])
    return out


# ---------------------------------------------------------------------- evaluation blocks (§3.2)
def block_generator(split, block, scope=None, process=None):
    return SeedTree(0).generator("data", scope or k4b_data.SCOPE, split, int(block),
                                 *(process or k4b_data.PROCESS))


def block_ids(split, block, n, scope=None, process=None) -> np.ndarray:
    code = process_code(*(process or k4b_data.PROCESS),
                        f"{scope or k4b_data.SCOPE}/{split}/b{int(block)}")
    return np.asarray(make_sequence_ids(code, "test", int(n)), dtype=np.int64)


def sample_block_c(T, E_canon, pi, split, block, n) -> tuple:
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(
        int(n), block_generator(split, block))
    canon32 = np.asarray(tokens[:, :32], dtype=np.uint8)
    del tokens, states
    ids = block_ids(split, block, n)
    order = np.argsort(ids, kind="stable")
    return np.ascontiguousarray(canon32[order]), np.ascontiguousarray(ids[order])


def sample_lgate(proc) -> tuple:
    return sample_block_c(proc["T"], proc["E_canon_shared"], proc["pi"], "lgate", 0, cc.LGATE_N)


def sample_eval(proc, split, block=0) -> tuple:
    if split == "lgate":
        return sample_lgate(proc)
    if split in ("cal", "val", "test"):
        return k4b_data.sample_block(proc["T"], proc["E_canon_shared"], proc["pi"], split, block)
    raise ValueError(f"unknown evaluation split {split!r}")


def hist_name(split, block, dry=False) -> str:
    return f"{'DRYHIST' if dry else 'HIST'}_{split}_b{int(block)}.npz"


def save_table(path, table) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(path, **{k: v for k, v in table.items() if isinstance(v, np.ndarray)})
    return path


def sample_test_c(out, proc, release, reservation_path, dry) -> dict:
    """Real run: k4b_fresh.sample_test unchanged; dry run: its mirror with DRYHIST_ names."""
    if not dry:
        return k4b_fresh.sample_test(out, proc, release, reservation_path)
    res = k4b_release.verify_reservation(reservation_path, release)
    if res["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"{res['status']}: {res['reason']}")
    k4b_driver.begin_stage(out, "S7")
    d = Path(out) / "stages" / "S7"
    d.mkdir(parents=True, exist_ok=True)
    tabs, files = [], []
    for b in range(int(release["k"])):
        canon, ids = k4b_data.sample_block(proc["T"], proc["E_canon_shared"], proc["pi"],
                                           "test", b)
        t = k4b_data.history_table(canon, ids, "test", b)
        files.append(save_table(d / hist_name("test", b, True), t))
        tabs.append(t)
    k4b_driver.complete_stage(out, "S7", files)
    return {"canon32": np.concatenate([t["canon32"] for t in tabs]),
            "seq_ids": np.concatenate([t["seq_ids"] for t in tabs]),
            "digest": np.concatenate([t["digest"] for t in tabs]), "blocks": tabs}


# ------------------------------------------------------------------------- H2, H2-FRESH (§3.3)
def separation_c(reg, tables) -> dict:
    names = list(tables)
    coll = {}
    for s in names:
        d = np.asarray(tables[s]["digest"]).astype("<U64")
        coll[f"{s}_R"] = int(np.count_nonzero(reg.contains(d)))
    for a, b in combinations(names, 2):
        coll[f"{a}_{b}"] = len(set(np.asarray(tables[a]["digest"]).astype(str).tolist())
                               & set(np.asarray(tables[b]["digest"]).astype(str).tolist()))
    seq = k4b_data.seq_disjoint({s: tables[s]["seq_ids"] for s in names}, reg.seq_ids,
                                list(reg.sealed_ranges.values()))
    pred = {s: k4b_data.predicate_check(tables[s]["canon32"], reg.predicates) for s in names}
    dup = {s: k4b_data.duplicates(tables[s]["canon32"]) for s in names}
    if any(coll.values()):
        status = LINEAGE
    elif seq["status"] != "PASS":
        status = seq["status"]
    elif any(p["status"] != "PASS" for p in pred.values()):
        status = INCOMPLETE
    else:
        status = "PASS"
    return {"status": status, "collisions": coll, "seq_disjoint": seq, "predicates": pred,
            "duplicates": dup}


def h2c(out, ctx) -> dict:
    out = Path(out)
    res = k4b_release.verify_reservation(ctx["reservation_path"], ctx["release"])
    if res["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"{res['status']}: {res['reason']}")
    k4b_driver.begin_stage(out, "S3")
    d, files, tabs = out / "stages" / "S3", [], {}
    for split in ("lgate", "cal", "val"):
        canon, ids = sample_eval(ctx["proc"], split, 0)
        tabs[split] = t = k4b_data.history_table(canon, ids, split, 0)
        files.append(save_table(d / hist_name(split, 0, ctx.get("dry", False)), t))
    k4b_driver.complete_stage(out, "S3", files)
    ctx["tables"] = tabs
    r = separation_c(ctx["reg1"], tabs)
    if r["status"] != "PASS":
        raise C1GateFailure(r["status"], json.dumps(r, default=str)[:2000])
    return {k: v for k, v in r.items() if k != "status"}


def h2_fresh_c(out, ctx) -> dict:
    res = k4b_release.verify_reservation(ctx["reservation_path"], ctx["release"],
                                         sampling_began=True)
    if res["status"] != "PASS":
        raise C1GateFailure(res["status"], res["reason"])
    reg2 = c2_registry.Registry.load(Path(out), "K-REG2")
    test, tabs = ctx["test"], ctx["tables"]
    own = set()
    for s in ("lgate", "cal", "val"):
        own |= set(np.asarray(tabs[s]["seq_ids"], dtype=np.int64).tolist())
    blocks = {f"test_b{i}": t["seq_ids"] for i, t in enumerate(test["blocks"])}
    blocks.update({s: tabs[s]["seq_ids"] for s in ("lgate", "cal", "val")})
    hits = int(np.count_nonzero(reg2.contains(np.asarray(test["digest"]).astype("<U64"))))
    checks = {
        "separation": {"collisions": {"test_R2": hits}, "status": "PASS" if not hits else LINEAGE},
        "seq_disjoint": k4b_data.seq_disjoint(blocks, set(reg2.seq_ids) - own,
                                              list(reg2.sealed_ranges.values())),
        "predicates": k4b_data.predicate_check(test["canon32"], reg2.predicates),
    }
    for r in checks.values():
        if r["status"] != "PASS":
            raise C1GateFailure(r["status"], json.dumps(r, default=str)[:2000])
    return checks


# ------------------------------------------------------------------------ registry risk (§3.4)
def p_d2a_check(proc, p_ref) -> dict:
    p = float(hws_exact.p_d2a(proc["T"], proc["E_canon_shared"], proc["pi"]))
    rel = abs(p - float(p_ref)) / abs(float(p_ref))
    return {"p_D2a": p, "p_D2a_ref": float(p_ref), "rel_diff": rel, "ok": rel <= 1e-12}


def registry_risk(p_d2a, N) -> dict:
    rows = cc.LGATE_N + cc.BLOCK + cc.BLOCK + int(N)
    value = rows * Fraction(float(p_d2a))
    return {"N": int(N), "rows": rows, "value": str(value), "ok": value <= Fraction(1, 100)}
