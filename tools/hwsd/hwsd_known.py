"""HWSD G0d and the known cases KD0-KD6 (API.md §9; protocol §6, §9). hwsd_driver and hwsd_dry are
imported lazily inside run_kd (API §0 dependency order)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

import hwsb_kb
import hwsb_known
import hwsc_bind
import hwsc_config
import hwsc_gates
import hwsc_known
import hwsd_bind
import hwsd_data
import hwsd_readers
import hwsd_records
import k4b_config
import k4b_driver
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import SeedTree

KNOWN, AUTH_REFUSE = "FAIL_TECHNICAL/KNOWN_CASE", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
TEXT_SUFFIXES = (".json", ".jsonl", ".md", ".py", ".txt", ".yaml")
SKIP_DIRS = {".git", ".venv", "__pycache__", "sealed"}
needle_in = hwsc_known.needle_in
from hwsd_known2 import c0_val_line, kd2, repro_c  # noqa: E402,F401  (re-export, API erratum)


# ---------------------------------------------------------------------------------- G0d
def _skip_dir(parent, name, root, scratch) -> bool:
    low = name.lower()
    docs = low == "research_summary" and parent.name.lower() == "docs"
    return (name in SKIP_DIRS or low.startswith("00_read_me_first") or docs
            or dc.search_pruned(parent / name, root, scratch))


def seed_search_d(root, needles, scratch=dc.SCRATCH) -> list:
    root, hits = Path(root), []
    for folder, dirs, files in os.walk(root, topdown=True):
        here = Path(folder)
        dirs[:] = sorted(d for d in dirs if not _skip_dir(here, d, root, scratch))
        for name in sorted(files):
            low = name.lower()
            if low.startswith("00_read_me_first") or not low.endswith(TEXT_SUFFIXES):
                continue
            if dc.search_pruned(here / name, root, scratch):
                continue
            with open(here / name, encoding="utf-8", errors="replace") as handle:
                for i, line in enumerate(handle, 1):
                    found = [nd for nd in needles if needle_in(nd, line)]
                    hits += [{"path": str(here / name), "needle": nd, "line": i} for nd in found]
    return hits


def _ints(track) -> list:
    return [str(i) for a, b in track["seed_blocks"] for i in range(int(a), int(b) + 1)]


def needles_d(namespace) -> dict:
    u = namespace["tracks"]["U"]
    return {"own": list(dc.NEEDLES), "other": list(u["scopes"]) + _ints(u)}


def _reserved(track) -> set:
    return set(track["scopes"]) | {track["store"], track["dry_store_glob"],
                                   track["test_root_glob"]} | set(_ints(track))


def overlap_check(namespace) -> dict:
    common = sorted(_reserved(namespace["tracks"]["D"]) & _reserved(namespace["tracks"]["U"]))
    return {"status": "FAIL_TECHNICAL/SEED_SCOPE" if common else "PASS", "common": common}


def _hash(path, exempt=False) -> str:
    p = Path(path)
    return hashlib.sha256(p.read_bytes() if exempt else dc.read_bytes(p)).hexdigest()


def _sha_check(root, rel, want, absent=AUTH_REFUSE, differ="FAIL_TECHNICAL/AUTHORITY",
               exempt=False) -> None:
    p = Path(root) / rel
    if not p.is_file():
        raise C1GateFailure(absent, f"{rel} absent")
    if _hash(p, exempt) != want:
        raise C1GateFailure(differ, f"{rel} sha256 differs")


def g0d(out, stage, auth=None, sched=None, root=dc.ROOT) -> dict:
    out, root, C = Path(out), Path(root), dc.CONTRACT
    a, checks = C["authority"], {}
    for k in a["kd0_addenda"]:
        _sha_check(root, a["owner_addenda"][k]["path"], a["owner_addenda"][k]["sha256"])
        checks[f"addendum_{k}"] = True
    ra, frz = a["run_approval"], {}
    if (out / "FREEZE.json").is_file():
        frz = dc.read_json(out / "FREEZE.json")
    if ra["path"] == "TO_FREEZE" or not (root / ra["path"]).is_file():
        raise C1GateFailure(AUTH_REFUSE, "no owner run approval")
    sha = _hash(root / ra["path"])
    if not (sha == ra["sha256"] == (auth or {}).get("run_approval_sha256")
            == frz.get("run_approval_sha256")):
        raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "run approval sha256")
    df = a["design_freeze"]
    _sha_check(root, df["path"], df["sha256"])
    checks["design_freeze"] = True
    for name, row in C["identity"]["rows"].items():
        _sha_check(root, row["path"], row["sha256"], absent=AUTH_REFUSE,
                   differ="FAIL_TECHNICAL/IDENTITY",
                   exempt=name == "obs_inventory")
    handoff = hwsc_config.load_handoff()
    result = dc.read_json(root / C["identity"]["rows"]["hwsc_result"]["path"])
    zc = Fraction(C["identity"]["Z_bound"])
    if not (Fraction(handoff["Z_bound"]) == Fraction(str(result["Z_bound"])) == zc):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "Z_bound differs")
    checks["identity"] = True
    ns = dc.read_json(root / C["identity"]["rows"]["namespace"]["path"])
    ov = overlap_check(ns)
    if ov["status"] != "PASS":
        raise C1GateFailure(ov["status"], f"namespace overlap {ov['common'][:5]}")
    nd = needles_d(ns)
    hits = seed_search_d(root, nd["own"] + nd["other"])
    res = hwsc_known.classify_hits_c(hits, fragments=C["seeds"]["g0_declaration_fragments"],
                                     job_scratch=[])
    checks["lineage"] = hwsd_records.lineage_d(out)
    path = out / "stages" / stage / "G0D.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, res)
    if res["status"] != "PASS":
        raise C1GateFailure("FAIL_TECHNICAL/SEED_SCOPE", "G0d: seed-scope hits outside the "
                            "declarations")
    sc = hwsd_records.sched_ok(sched, stage)
    if not sc["ok"]:
        raise C1GateFailure(AUTH_REFUSE, f"SCHED: {sc['reason']}")
    checks["seed_hits"] = len(res["hits"])
    return checks


# ------------------------------------------------------------------------------------ KD1
def ident_d(masters=dc.MASTERS, steps=dc.STEPS, hwsc=dc.HWSC_STORE, handoff=None) -> dict:
    hwsc = Path(hwsc)
    handoff = handoff if handoff is not None else hwsc_config.load_handoff()
    try:
        rel_b = dc.read_json(hwsc / "RELEASE_B.json")
        per, ids = {}, []
        for j in masters:
            relp = f"stages/TRAIN/{j}/TRAIN_RECORD.json"
            sha, rec = dc.read_train_record(j, hwsc)
            if not (sha == rel_b["train_records"][str(j)] == hwsd_readers.stage_complete_sha(
                    hwsc / "STAGES.jsonl", relp, f"TRAIN_{j}")):
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"TRAIN record {j} not bound")
            if rec["status"] != "COMPLETE":
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"TRAIN record {j} status")
            seeds = set()
            for step in steps:
                row = dc.CHECKPOINTS[(j, step)]
                if row["id"] != rec["checkpoint_ids"][str(step)] or \
                        row["payload_sha256"] != rec["checksums"][str(step)]:
                    raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"checkpoint row {j}:{step}")
                exp = hwsc_gates.expected_meta_c(j, step, rec)
                meta = k4b_driver.checkpoint_meta(hwsc / "artifacts", row["id"])
                r = k4b_config.check_checkpoint_meta(meta, exp)
                if r["status"] != "PASS":
                    raise C1GateFailure("FAIL_TECHNICAL/IDENTITY",
                                        json.dumps(r["mismatches"], default=str)[:2000])
                seeds.add(meta["seed_map"][exp["init_seed_key"]])
                ids.append(row["id"])
            if len(seeds) != 1:
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"init seeds differ for {j}")
            per[j] = {"train_record_sha256": sha, "init_seed": seeds.pop()}
        if not hwsc_gates.exclusion_check(ids, handoff)["ok"]:
            raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "excluded checkpoint ids")
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001  any KD1 defect is an identity defect
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", repr(exc)) from exc
    return {"n": len(masters) * len(steps), "per_master": per}


# ---------------------------------------------------------------------------- KD5, KD6, run
def kd5() -> dict:
    import hwsb_eval

    w0 = hwsb_known.w0_process()
    r = hwsb_kb.kb6(w0, None)
    k6 = hwsb_kb.KC["KB6"]
    obs = hwsb_kb._e4_obs(w0, "test", k6["ObservationSet_test"]["n"],
                          SeedTree(0).generator("data", "test", "cylinder", "overlap", "1.25"),
                          "shared")
    canon = hwsb_kb.hd.canonical32(obs.tokens, w0["perm"][hwsb_kb.E4])
    q = hwsb_eval.oracle_predictives(w0, canon, (1, 4))
    ok = bool(r["ids_ok"]) and abs(r["G_C"] - 0.2648737252067266) <= 1e-12
    c1 = abs(hwsb_eval.b1(q, q[32])["captured"] - 1.0) <= 1e-12
    c2 = abs(hwsb_eval.b1(q, q[1])["captured"]) <= 1e-12
    c3 = hwsb_eval.forcing(q[32], q[4], q[4])["d_mean"] == 0
    return {"status": "PASS" if ok and c1 and c2 and c3 else KNOWN,
            "kb6": {"ids_ok": r["ids_ok"], "G_C": r["G_C"]}, "planted": [c1, c2, bool(c3)]}


def kd6(job) -> dict:
    base = dc.SCRATCH / f"test_hwsd-{job}"
    (base / "tmp").mkdir(parents=True, exist_ok=True)
    junit = base / "kd6.xml"
    env = dict(os.environ, PYTHONPATH=str(dc.REPO / "src"), TEMP=str(base / "tmp"),
               TMP=str(base / "tmp"), TMPDIR=str(base / "tmp"))
    cmd = [sys.executable, "-s", "-m", "pytest", "tests/hwsd/test_a_known_bound.py",
           "-p", "no:cacheprovider", "-q", f"--junitxml={junit}", f"--basetemp={base / 'pytest'}"]
    rc = subprocess.run(cmd, cwd=dc.REPO, env=env, capture_output=True, text=True).returncode
    text = junit.read_text(encoding="utf-8") if junit.is_file() else ""

    def attr(name):
        mt = re.search(rf'{name}="(\d+)"', text)
        return int(mt.group(1)) if mt else -1

    n, f, e = attr("tests"), attr("failures"), attr("errors")
    return {"status": "PASS" if rc == 0 and n >= 1 and f == 0 and e == 0 else KNOWN,
            "returncode": rc, "tests": n, "failures": f, "errors": e}


def run_kd(out, auth, sched, job, attempt=1, cont=None) -> dict:
    import hwsd_dry

    out, t0, rec, status = Path(out), time.process_time(), {}, "PASS"
    led = dc.STUDY_LEDGER

    def step(name):
        if name == "KD0":
            return dict(g0d(out, "KD", auth, sched), status="PASS")
        if name == "KD1":
            return dict(ident_d(), status="PASS")  # R-0209-1: ident_d raises on any mismatch
        if name == "KD2":
            return kd2()
        if name == "KD3":
            return repro_c(out)
        if name == "KD4":  # R-0209-2: unbound (seq_cases binds the dry table); scratch out
            with hwsc_bind.suspended(), tempfile.TemporaryDirectory(prefix="kd4") as tmp:
                return hwsd_dry.seq_cases(out=Path(tmp) / "SEQ")
        if name == "KD5":
            return kd5()
        return kd6(job)

    for name in dc.CONTRACT["known_cases"]["order"]:
        if status != "PASS":
            rec[name] = {"status": "NOT_RUN"}
            stage_records.record_gate(out, name, "NOT_RUN")
            continue
        hwsd_records.pause_or_raise_d(out, "KD", t0, led, cont)
        try:
            r = step(name)
        except Exception as exc:  # noqa: BLE001  every KD failure is recorded, then stops
            s = hwsd_records.status_of(exc)
            if s == "PAUSE":
                raise
            r = {"status": s if name == "KD0" else KNOWN, "reason": str(exc)[:2000]}
        rec[name] = hwsb_known.jsonable(r)
        st = rec[name].get("status")
        if st != "PASS":
            rec[name]["status"] = st if name == "KD0" else KNOWN
            status = rec[name]["status"]
        stage_records.record_gate(out, name, rec[name]["status"])
    record = {"status": status, "kd": {k: {"status": v.get("status"), "details": v}
                                       for k, v in rec.items()},
              "protocol_sha256": dc.PROTOCOL_SHA256,
              "freeze_sha256": stage_records.sha256(out / "FREEZE.json")
              if (out / "FREEZE.json").exists() else None,
              "binding_audit": _audit()}
    path = out / "stages" / "KD" / "KD_RECORD.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, json.loads(json.dumps(record, default=str)))
    files = [path] + sorted((out / "stages" / "KD").glob("G0D.json")) + sorted(
        (out / "stages" / "KD" / "REPRO").rglob("*.json"))
    k4b_driver.complete_stage(out, "KD", files)
    hwsd_data.write_obligation(out, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", job, attempt,
                               hwsd_records.utc())
    return record


def _audit() -> dict:
    au = hwsd_bind.audit()
    return {"status": au["status"], "n_hits": au["n_hits"]}
