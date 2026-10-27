"""HWSB G0 and the known cases KB0-KB7 (API.md §7; protocol §3).

References are read at run time from the cited JSON records and must equal CONTRACT. E4 data
are regenerated in memory only (authorised deterministic regeneration); no E4 checkpoint
payload is opened. KB5 reads the S3 w* history table of hws-store (AUTH-named, sha256-checked).
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import json
import time
from fractions import Fraction
from pathlib import Path

import hws_driver
import hwsb_data as hd
import hwsb_law as hl
import hwsb_train as ht
import numpy as np
import process_law
import stage_records

from topo_pilot.contracts import (
    ArtifactStore,
    LocalFSBackend,
    MemoryBackend,
    ObservationSet,
    SeedTree,
    payload_checksum,
)
from topo_pilot.dataset.checks import make_sequence_ids, process_code

KNOWN = "FAIL_TECHNICAL/KNOWN_CASE"
KC = hc.CONTRACT["known_cases"]
E4 = 1729


def jsonable(x):
    """JSON-safe copy: Fractions as str, numpy scalars as Python, (j, s) keys as 'j:s'."""
    if isinstance(x, dict):
        return {
            (f"{k[0]}:{k[1]}" if isinstance(k, tuple) else str(k)): jsonable(v)
            for k, v in x.items()
        }
    if isinstance(x, (list, tuple, set)):
        return [jsonable(v) for v in (sorted(x) if isinstance(x, set) else x)]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x)
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, (Fraction,)) or type(x).__name__ == "Decimal":
        return str(x)
    return x if x is None or isinstance(x, (str, int)) else str(x)


def _ok(flag) -> str:
    return "PASS" if flag else KNOWN


def _read_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------- G0


def classify_hits(hits, fragments=None, job_scratch=None, label="hwsb_declaration") -> dict:
    """Mirror of hws_driver.classify_seed_hits with the lists as arguments (RC-3)."""
    frags = [
        f.lower()
        for f in (
            hc.CONTRACT["seeds"]["g0_declaration_fragments"] if fragments is None else fragments
        )
    ]
    jobs = [
        j.lower()
        for j in (hc.CONTRACT["seeds"]["g0_job_scratch"] if job_scratch is None else job_scratch)
    ]
    out = []
    for h in hits:
        p = str(h["path"]).replace("\\", "/").lower()
        ok = any(f in p for f in frags) or any(p.startswith(j) for j in jobs)
        out.append(dict(h, kind=label if ok else "unclassified"))
    bad = any(h["kind"] != label for h in out)
    return {"status": "FAIL_TECHNICAL/SEED_SCOPE" if bad else "PASS", "hits": out}


def g0(out, root=hc.ROOT) -> dict:
    res = classify_hits(hws_driver.seed_search(root, list(hc.NEEDLES)))
    path = Path(out) / "stages" / "KB" / "G0.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, res)
    stage_records.record_gate(Path(out), "G0", res["status"], hits=len(res["hits"]))
    if res["status"] != "PASS":
        raise hc.HwsbStop(res["status"], "G0: seed-scope hits outside the declarations")
    return res


# ---------------------------------------------------------------------------------- KB0-KB1


def kb0(out, auth, sched) -> dict:
    import hwsb_driver as hdr

    a, s = hdr.auth_ok(auth, "KB"), hdr.sched_ok(sched, "KB")
    frz = hdr.verify_freeze(out, hc.REPO)
    k0 = KC["KB0"]
    hashes = {
        name: stage_records.sha256(k0[name]["path"]) == k0[name]["sha256"]
        for name in ("selection_json", "final_report_json")
    }
    if not (a["ok"] and s["ok"]):
        raise hc.HwsbStop("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", f"{a['reason']} {s['reason']}")
    if not all(hashes.values()):
        raise hc.HwsbStop(KNOWN, f"stage-A record hashes: {hashes}")
    res = g0(out)
    return {
        "status": "PASS",
        "auth": a,
        "sched": s,
        "hashes": hashes,
        "freeze_sha256": frz.get("freeze_sha256"),
        "g0_hits": len(res["hits"]),
    }


def kb1(store) -> tuple:
    proc = hd.build_process(store)
    k1, ck = KC["KB1"], hd.spec_checksums(store, proc)
    sel = _read_json(KC["KB0"]["selection_json"]["path"])["sha256"]
    sha = hd.arrays_sha256(proc)
    checks = {
        "world_id": proc["ids"]["world"] == k1["WorldSpec"]["id"],
        "transition_id": proc["ids"]["transition"] == k1["TransitionSpec"]["id"],
        "world_payload": ck["WorldSpec"] == k1["WorldSpec"]["payload_sha256"],
        "transition_payload": ck["TransitionSpec"] == k1["TransitionSpec"]["payload_sha256"],
        "selection_equals_contract": sel == k1["selection_sha256"],
    }
    for k in ("E", "T", "pi", "coords"):
        checks[f"sha_{k}"] = sha[k] == sel.get(k) == k1["selection_sha256"][k]
    for m in proc["E_canon"]:
        checks[f"E_canon_{m}"] = hd._sha_array(proc["E_canon"][m]) == sel.get("E")
    rec = {
        "status": _ok(all(checks.values())),
        "checks": checks,
        "ids": proc["ids"],
        "spec_checksums": ck,
        "arrays_sha256": sha,
    }
    return proc, rec


def w0_process(store=None) -> dict:
    store = store or ArtifactStore(MemoryBackend())
    proc = hd.build_process(store, masters=(E4,), emission_cfg=hc.W0_EMIS_CFG)
    proc["spec_checksums"] = hd.spec_checksums(store, proc)
    return proc


# -------------------------------------------------------------------------------- KB2, KB3


def _e4_obs(proc, split, n, rng, rep) -> ObservationSet:
    tok = hd.sample_observations(
        proc["T"], proc["E_named"][E4], proc["pi"], proc["perm"][E4], n, rng, split
    )
    ids = make_sequence_ids(process_code("cylinder", "overlap", "1.25", rep), split, n)
    return ObservationSet(split=split, V=36, sequence_id=ids, tokens=tok)


def _ck(obj) -> str:
    return payload_checksum(*obj.to_payload())


def kb2_kb3(proc_w0) -> dict:
    k2, k3 = KC["KB2"], KC["KB3"]
    obs = {
        s: _e4_obs(
            proc_w0,
            s,
            k2[f"ObservationSet_{s}"]["n"],
            SeedTree(E4).generator("data", s, "cylinder", "overlap", "1.25", E4),
            E4,
        )
        for s in ("train", "dev")
    }
    obs_ok = all(_ck(obs[s]) == k2[f"ObservationSet_{s}"]["payload_sha256"] for s in obs)
    if not obs_ok:
        raise hc.HwsbStop(KNOWN, "KB2: regenerated E4 ObservationSet checksums differ")
    args = (obs["train"], obs["dev"], E4, tuple(k2["run_key"]), k2["run_id"], k2["observation_id"])
    ref_ck = {int(s): v["payload_sha256"] for s, v in k2["checkpoints"].items()}
    ref_ce = {int(s): float(v) for s, v in k2["dev_ce"].items()}
    six = ht.train_known(*args, stop_after=int(k2["stop_after_step"]), threads=int(k2["threads"]))
    bitwise = all(six["checksums"].get(s) == v for s, v in ref_ck.items()) and all(
        six["dev_ce"].get(s) == v for s, v in ref_ce.items()
    )
    tol = float(k2["secondary_reading"]["dev_ce_abs_tol"])
    drift = six["checksums"].get(0) == ref_ck[0] and all(
        abs(six["dev_ce"][s] - v) <= tol for s, v in ref_ce.items()
    )
    reading = "BITWISE" if bitwise else ("PASS_WITH_NUMERIC_DRIFT" if drift else None)
    one = ht.train_known(*args, stop_after=int(k2["stop_after_step"]), threads=int(k3["threads"]))
    again = ht.train_known(
        *args, stop_after=int(k3["determinism_rerun_to_step"]), threads=int(k3["threads"])
    )
    k3_ok = all(abs(one["dev_ce"][s] - v) <= float(k3["dev_ce_abs_tol"]) for s, v in ref_ce.items())
    det = again["checksums"].get(50) == one["checksums"].get(50)
    kb2 = {
        "status": reading or KNOWN,
        "reading": reading,
        "checksums": six["checksums"],
        "dev_ce": six["dev_ce"],
        "threads": six["threads"],
        "observation_sets_equal": obs_ok,
        "deviation_flags": [] if reading == "BITWISE" else ["KB2_SECONDARY_READING"],
    }
    kb3 = {
        "status": _ok(k3_ok and det),
        "dev_ce": one["dev_ce"],
        "determinism": det,
        "checksums": one["checksums"],
        "threads": one["threads"],
        "equal_to_six_threads": one["checksums"] == six["checksums"],
    }
    return {
        "KB2": kb2,
        "KB3": kb3,
        "reading": reading,
        "torch": ht.torch_versions(),
        "ckpt100": six["checkpoints"].get(100),
    }


# -------------------------------------------------------------------------------- KB4-KB7


def kb4(proc_w0, proc_star) -> dict:
    k4 = KC["KB4"]
    ck = proc_w0.get("spec_checksums") or {}
    ids_ok = (
        ck.get("EmissionSpec", {}).get(E4) == KC["KB2"]["EmissionSpec_1729"]["payload_sha256"]
        and ck.get("WorldSpec") == KC["KB1"]["WorldSpec"]["payload_sha256"]
        and ck.get("TransitionSpec") == KC["KB1"]["TransitionSpec"]["payload_sha256"]
    )
    rec_path = k4["w0"]["record"]["path"]
    rec_ok = stage_records.sha256(rec_path) == k4["w0"]["record"]["sha256"]
    ref = Fraction(k4["w0"]["Z_bound"])
    rec_z = Fraction(_read_json(rec_path)["Z_bound"]) if rec_ok else None
    p = proc_w0
    w0 = hl.law_bound(
        p["T"], p["E_canon_shared"], p["pi"], p["coords"], Fraction(5, 4), Fraction(1, 5)
    )
    states = process_law.lattice_states(p["coords"])
    original = process_law.softmax_enclosure
    with hl.bound_law(Fraction(5, 4), Fraction(1, 5)):
        a, b = hl.softmax_enclosure_rounded(states), original(states)
    same = (
        a[1] == b[1]
        and a[2] == b[2]
        and all(x == y for ra, rb in zip(a[0], b[0]) for x, y in zip(ra, rb))
    )
    s = proc_star
    star = hl.law_bound(s["T"], s["E_canon_shared"], s["pi"], s["coords"], hc.SIGMA, hc.NEIGHBOUR)
    ok_w0 = w0["status"] == "BOUNDED" and w0["Z_bound"] == ref == rec_z and w0["delta"] == 0
    ok_star = star["status"] == "BOUNDED" and star["kappa"] is not None and star["kappa"] < 1
    return {
        "status": _ok(ids_ok and rec_ok and ok_w0 and same and ok_star),
        "w0": {k: v for k, v in w0.items() if k != "raw"},
        "w0_enclosure_identical": same,
        "w0_ids": ids_ok,
        "record_sha_ok": rec_ok,
        "w_star": {k: v for k, v in star.items() if k != "raw"},
    }


def run_kb(out, auth, sched, store=None) -> dict:
    """KB0 -> KB6 as gates; the first failure stops with later items NOT_RUN."""
    import hwsb_driver as hdr

    out = Path(out)
    store = store or ArtifactStore(LocalFSBackend(out / "artifacts"))
    t0, items, rec = time.process_time(), ("KB0", "KB1", "KB2", "KB3", "KB4", "KB5", "KB6"), {}
    ctx = {}

    def step(name):
        if name == "KB0":
            return kb0(out, auth, sched)
        if name == "KB1":
            ctx["proc"], r = kb1(store)
            return r
        if name == "KB2":
            ctx["w0"] = w0_process()
            ctx["k23"] = kb2_kb3(ctx["w0"])
            return ctx["k23"]["KB2"]
        if name == "KB3":
            return ctx["k23"]["KB3"]
        if name == "KB4":
            ctx["kb4"] = kb4(ctx["w0"], ctx["proc"])
            return ctx["kb4"]
        if name == "KB5":
            return __getattr__("kb5")(ctx["proc"])
        return __getattr__("kb6")(ctx["w0"], ctx["k23"]["ckpt100"])

    status = "PASS"
    for name in items:
        if status not in ("PASS", "PASS_WITH_NUMERIC_DRIFT"):
            rec[name] = {"status": "NOT_RUN"}
            stage_records.record_gate(out, name, "NOT_RUN")
            continue
        hdr.pause_or_raise(out, "KB", t0)
        try:
            r = step(name)
        except hc.HwsbStop as exc:
            r = {"status": exc.status if name == "KB0" else KNOWN, "reason": exc.reason}
        rec[name] = jsonable(r)
        stage_records.record_gate(out, name, rec[name]["status"])
        if rec[name]["status"] not in ("PASS", "PASS_WITH_NUMERIC_DRIFT"):
            status = rec[name]["status"]
    kb4r = ctx.get("kb4", {}).get("w_star", {})
    record = {
        "status": status,
        "kb": rec,
        "reading": ctx.get("k23", {}).get("reading"),
        "process_ids": jsonable(ctx["proc"]["ids"]) if "proc" in ctx else None,
        "arrays_sha256": rec.get("KB1", {}).get("arrays_sha256"),
        "law_w_star": jsonable(kb4r),
        "Z_bound_w_star": jsonable(kb4r.get("Z_bound")),
        "torch": ctx.get("k23", {}).get("torch"),
        "protocol_sha256": hc.CONTRACT["protocol_sha256"],
    }
    path = out / "stages" / "KB" / "KB_RECORD.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, record)
    return record


def __getattr__(name):
    """kb5, kb6 and kb7 live in hwsb_kb (split by size), re-exported lazily."""
    if name in ("kb5", "kb6", "kb7"):
        import hwsb_kb

        return getattr(hwsb_kb, name)
    raise AttributeError(f"module 'hwsb_known' has no attribute {name!r}")
