"""HWSD data: blocks and tables, H2-D separation, registry risk, ORACLE-D, reference persistence,
B4-TEST, LGATE-ORACLE, shared controls, obligations (J11), reservations, end_reservation, W2
attestation (API.md section 3 and section 22). Reused functions are called through their module
attributes at call time, so the binding applies."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import copy
import fnmatch
import os
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import hwsb_eval
import hwsc_data
import k4b_cert
import k4b_config
import k4b_data
import k4b_fresh
import k4b_release
import k4b_scores
import numpy as np
import reference_cache
import scores
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import SequenceLayout
from topo_pilot.dataset import HMMSampler

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
ARRAY_SUFFIXES = (".npz", ".npy", ".pt")
_ART_RE = re.compile(r"(?:.*/)?artifacts/(WorldSpec|TransitionSpec|EmissionSpec|Checkpoint)"
                     r"/[0-9a-f]+/(?:payload\.npz|state\.pt)")
MOMENT_KEYS = REF_KS = (1, 2, 4, 32)


def _obl():
    return dc.CONTRACT["obligation"]


# ------------------------------------------------------------------ blocks and tables (2.5)
def block_generator(split, scope=None, process=None):
    return hwsc_data.block_generator(split, 0, scope=scope or k4b_data.SCOPE,
                                     process=process or k4b_data.PROCESS)


def block_ids(split, n, scope=None, process=None) -> np.ndarray:
    return hwsc_data.block_ids(split, 0, n, scope=scope or k4b_data.SCOPE,
                               process=process or k4b_data.PROCESS)


def sample_block_d(T, E, pi, split, n, scope=None, process=None) -> tuple:
    tokens, states = HMMSampler(T, E, pi, SequenceLayout()).sample(
        int(n), block_generator(split, scope, process))
    canon32 = np.asarray(tokens[:, :32], dtype=np.uint8)
    del tokens, states
    ids = block_ids(split, n, scope, process)
    order = np.argsort(ids, kind="stable")
    return np.ascontiguousarray(canon32[order]), np.ascontiguousarray(ids[order])


def hist_name(split, dry=False) -> str:
    return f"{'DRYHIST' if dry else 'HIST'}_{split}_b0.npz"


def sample_tables(proc, scope=None, process=None, sizes=None) -> dict:
    sizes = dc.SIZES if sizes is None else sizes
    out = {}
    for split in dc.SPLITS:
        canon, ids = sample_block_d(proc["T"], proc["E_canon_shared"], proc["pi"], split,
                                    sizes[split], scope, process)
        out[split] = k4b_data.history_table(canon, ids, split, 0)
    return out


def save_tables(out, tables, dry=False) -> list:
    return [hwsc_data.save_table(Path(out) / "stages" / "S3" / hist_name(s, dry), tables[s])
            for s in dc.SPLITS]


def load_tables(out, dry=False) -> dict:
    res = {}
    for s in dc.SPLITS:
        t = dict(k4b_fresh.load_recorded(out, "S3", hist_name(s, dry)))
        t["split"], t["block"] = s, 0
        res[s] = t
    return res


# ------------------------------------------------------------ H2-D and the registry risk
def separation_d(reg, tables) -> dict:
    ordered = {s: tables[s] for s in dc.SPLITS if s in tables}
    r = hwsc_data.separation_c(reg, ordered)
    return dict(r, rows={s: int(len(t["seq_ids"])) for s, t in ordered.items()})


def registry_risk_d(p_d2a) -> dict:
    rows = 13312
    value = rows * Fraction(float(p_d2a))
    return {"rows": rows, "value": str(value), "ok": value <= Fraction(1, 100)}


# ------------------------------------------- ORACLE-D, references, B4-TEST, LGATE, controls
def oracle_d(proc, tables) -> dict:
    p, m = proc, {}
    for s in ("cal", "test"):
        m[s] = k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"],
                                         tables[s]["canon32"], p["features"])
    refs_test = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                                    tables["test"]["canon32"])
    r = np.asarray(tables["cal"]["ref_row"], dtype=bool)
    refs_cal = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                                   tables["cal"]["canon32"][r])
    c_test = k4b_cert.moment_check(m["test"], refs_test)
    c_cal = k4b_cert.moment_check({K: m["cal"][K][r] for K in m["cal"]}, refs_cal)
    if not (c_test["ok"] and c_cal["ok"]):
        n = c_test["n_fail"] + c_cal["n_fail"]
        raise C1GateFailure("FAIL_TECHNICAL/ORACLE", f"{n} rows above MOMENT_TOL")
    return {"moments": m, "refs_test": refs_test,
            "max_gap": str(max(c_test["max_gap"], c_cal["max_gap"])), "n_checked": 3076}


def _save(path, **arrays) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(path, **arrays)
    return path


def save_oracle(out, moments) -> list:
    d = Path(out) / "stages" / "S4"
    return [_save(d / f"ORACLE_{s}.npz", **{f"m{K}": np.asarray(moments[s][K], dtype=np.float64)
                                            for K in MOMENT_KEYS}) for s in ("cal", "test")]


def refs_to_json(refs, proc, test_table_sha256) -> dict:
    ident = reference_cache.identity(proc["T"], proc["E_canon_shared"], proc["pi"],
                                     proc["coords"])
    return {"schema": "hwsd-refs-v1", "identity": ident, "test_table_sha256": test_table_sha256,
            "Ks": list(REF_KS), "n": len(refs),
            "M": {str(K): [[str(r[K][0]), str(r[K][1])] for r in refs] for K in REF_KS}}


def refs_from_json(obj, proc, n, test_table_sha256) -> list:
    def bad(why):
        return C1GateFailure(LINEAGE, f"REFS_test: {why}")

    ident = reference_cache.identity(proc["T"], proc["E_canon_shared"], proc["pi"],
                                     proc["coords"])
    if not isinstance(obj, dict) or obj.get("schema") != "hwsd-refs-v1":
        raise bad("schema")
    if obj.get("identity") != ident:
        raise bad("identity")
    if obj.get("test_table_sha256") != test_table_sha256:
        raise bad("test table sha256")
    if obj.get("n") != int(n) or obj.get("Ks") != list(REF_KS):
        raise bad("n or Ks")
    M = obj.get("M", {})
    if sorted(M) != sorted(str(K) for K in REF_KS) or any(len(M[str(K)]) != int(n)
                                                           for K in REF_KS):
        raise bad("list lengths")
    return [{K: (Decimal(M[str(K)][i][0]), Decimal(M[str(K)][i][1])) for K in REF_KS}
            for i in range(int(n))]


def b4_test(m_test, refs_test, eps, Z, seed=None) -> dict:
    r4n = scores.r4_norms(m_test[32], m_test[4])
    Bn = max(k4b_cert.norm_bound(r4n[i], ref[32], ref[4], eps[4], eps[32])
             for i, ref in enumerate(refs_test))
    g = k4b_cert.b4_guard(r4n, Bn, Z, seed if seed is not None else k4b_config.SEEDS["fresh_b4"],
                          len(r4n))
    return dict(g, B_norm_max=Bn)


def lgate_oracle(proc, canon32) -> dict:
    q = hwsb_eval.oracle_predictives(proc, canon32, Ks=(1, 4))
    for K, a in q.items():
        a = np.asarray(a, dtype=np.float64)
        if not np.all(np.isfinite(a)) or float(np.max(np.abs(a.sum(axis=1) - 1.0))) > 1e-6:
            raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"LGATE oracle predictive K={K}")
    return q


def save_lgate_q(out, q) -> Path:
    return _save(Path(out) / "stages" / "S4" / "LGATE_Q.npz",
                 **{f"q{K}": np.asarray(q[K], dtype=np.float64) for K in (1, 4, 32)})


def shared_controls(m_test, canon32) -> dict:
    m = m_test

    def one(phi):
        return {"X": k4b_scores.phase_scores(phi, m[32], m[4]), "phi": phi}

    return {"m4_phase": {"all": one(k4b_scores.m4_phase(m[4]))},
            "sha_suffix": {"all": one(k4b_scores.sha_phase(canon32))},
            "delta4_orc": {"all": one(k4b_scores.oracle_phase(m[32]))}}


def save_shared(out, shared, bounds) -> list:
    d = Path(out) / "stages" / "S4"
    arrays = {}
    for name, e in shared.items():
        arrays[f"{name}_X"], arrays[f"{name}_phi"] = e["all"]["X"], e["all"]["phi"]
    npz = _save(d / "SHARED_CONTROLS.npz", **arrays)
    rec = {name: {"max_B": str(bounds[name]["all"]["max_B"]),
                  "certified": bool(bounds[name]["all"]["certified"])} for name in shared}
    js = d / "SHARED_CONTROLS.json"
    stage_records.write_new(js, rec)
    return [npz, js]


# ----------------------------------------------------------------- obligations (J11)
def _meta_type(store, rel):
    try:
        return dc.read_json((Path(store) / rel).parent / "meta.json").get("artifact_type")
    except Exception:  # noqa: BLE001
        return None


def classify_file(store, rel) -> tuple:
    o = _obl()
    if re.fullmatch(o["history_names"]["K4b history table"], rel):
        return "K4b history table", None
    if re.fullmatch(o["history_names"]["ObservationSet"], rel) and \
            _meta_type(store, rel) == "ObservationSet":
        return "ObservationSet", None
    m = _ART_RE.fullmatch(rel)
    if m and _meta_type(store, rel) == m.group(1):
        return "NON_HISTORY", "artifact"
    if "registry" in rel.split("/")[:-1]:
        return "NON_HISTORY", "registry"
    if any(re.fullmatch(r["regex"], rel) for r in o["name_rules"]):
        return "NON_HISTORY", "name_rule"
    raise C1GateFailure(LINEAGE, f"unclassifiable array file {rel}")


def is_checkpoint_payload(rel) -> bool:
    m = _ART_RE.fullmatch(rel)
    return bool(m) and m.group(1) == "Checkpoint"


def obligation_files(store) -> list:
    store, files = Path(store), []
    for dirpath, dirnames, filenames in os.walk(store):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            f = Path(dirpath) / name
            if f.suffix not in ARRAY_SUFFIXES:
                continue
            rel = f.relative_to(store).as_posix()
            cls, basis = classify_file(store, rel)
            ckpt = basis == "artifact" and is_checkpoint_payload(rel)
            files.append({"relpath": rel, "sha256": None if ckpt else stage_records.sha256(f),
                          "bytes": int(f.stat().st_size), "class": cls,
                          "reader": _obl()["readers"][cls], "basis": basis})
    return sorted(files, key=lambda e: e["relpath"])


def write_obligation(store, name, job, attempt, utc, reservation_id=None, dry_stores=(),
                     written_by="hwsd") -> tuple:
    if name != "REGISTRY_OBLIGATION.json" and name != f"REGISTRY_OBLIGATION_{job}-a{attempt}.json":
        raise ValueError(f"obligation name {name!r}")
    store = Path(store)
    rec = {"schema": _obl()["schema"], "store": store.as_posix(), "track": "D", "job": job,
           "attempt": attempt, "written_utc": utc, "written_by": written_by,
           "reservation_id": reservation_id, "name_rules": copy.deepcopy(_obl()["name_rules"]),
           "dry_stores": [Path(p).as_posix() for p in dry_stores],
           "files": obligation_files(store), "rule": "fail closed"}
    path = store / name
    stage_records.write_new(path, rec)
    return path, rec


def stop_obligation(store, job, attempt, reservation_id, utc) -> dict:
    path, rec = write_obligation(store, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", job,
                                 attempt, utc, reservation_id=reservation_id)
    return {"obligation": rec, "end": end_reservation(store, reservation_id, utc, path)}


# ------------------------------------------------------------- reservations (J8) and W2
def reservation_path(store, attempt) -> Path:
    return Path(store) / "reservations" / f"{dc.RESERVATION_PREFIX}{attempt}.json"


def start_reservation_d(store, attempt, utc) -> tuple:
    path = reservation_path(store, attempt)
    d = path.parent
    for f in sorted(d.glob("*.json")) if d.is_dir() else ():
        if f.name.endswith(".END.json") or f == path:
            continue
        try:
            active = dc.read_json(f).get("state") == "ACTIVE"
        except Exception:  # noqa: BLE001
            active = True
        if active and not reservation_ended(f)["ended"]:
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"live reservation {f.name}")
    d.mkdir(parents=True, exist_ok=True)
    return path, k4b_release.start_reservation(path, f"HWSD-W2-a{attempt}", utc)


def verify_reservation_d(path, reservation_id, sampling_began=False) -> dict:
    return k4b_release.verify_reservation(path, {"reservation": reservation_id}, sampling_began)


def end_reservation(store, reservation_id, utc, obligation_path,
                    written_by="hwsd_data.end_reservation") -> dict:
    store = Path(store)
    res = store / "reservations" / f"{reservation_id}.json"
    end = res.with_name(f"{reservation_id}.END.json")

    def refuse(why):
        return C1GateFailure(LINEAGE, f"end_reservation: {why}")

    if not res.is_file():
        raise refuse("reservation missing")
    if dc.read_json(res).get("state") != "ACTIVE":
        raise refuse("reservation not ACTIVE")
    ob = Path(obligation_path)
    if not ob.is_file():
        raise refuse("obligation missing")
    try:
        rel = ob.resolve().relative_to(store.resolve()).as_posix()
    except ValueError:
        raise refuse("obligation outside the store") from None
    if end.exists():
        raise refuse("END record exists")
    rec = {"schema": "hws-reservation-end-v1", "reservation_id": reservation_id,
           "reservation_file": f"reservations/{reservation_id}.json",
           "reservation_sha256": stage_records.sha256(res), "end_utc": utc,
           "obligation_file": rel, "obligation_sha256": stage_records.sha256(ob),
           "written_by": written_by}
    stage_records.write_new(end, rec)
    return rec


def reservation_ended(res_path, root=None) -> dict:
    root = Path(dc.ROOT if root is None else root)
    res_path = Path(res_path)
    try:
        rec = dc.read_json(res_path)
        rid = rec["id"]
    except Exception as exc:  # noqa: BLE001
        return {"ended": False, "rule": None, "reason": f"unreadable {exc!r}"}
    cur = stage_records.sha256(res_path)
    try:
        if rid == "RES-HWSC-W2":
            f = root / "agent-handoff" / "records" / "HWSC_W2_END.json"
            want = dc.CONTRACT["identity"]["rows"]["hwsc_w2_end"]["sha256"]
            ok = f.is_file() and stage_records.sha256(f) == want and \
                dc.read_json(f).get("reservation_file_sha256") == cur
            return {"ended": bool(ok), "rule": "a", "reason": "" if ok else "no matching END"}
        store = res_path.parent.parent if res_path.parent.name == "reservations" \
            else res_path.parent
        end = store / "reservations" / f"{rid}.END.json"
        if not end.is_file():
            return {"ended": False, "rule": "b", "reason": "no END record"}
        e = dc.read_json(end)
        rel = str(e.get("obligation_file", ""))  # R-0213-1: U writes it root-relative
        ob = next((c for c in (store / rel, root / rel) if c.is_file()), store / rel)
        if store.resolve() not in ob.resolve().parents:
            return {"ended": False, "rule": "b", "reason": "obligation outside the store"}
        ok = (e.get("schema") == "hws-reservation-end-v1" and e.get("reservation_sha256") == cur
              and ob.is_file() and e.get("obligation_sha256") == stage_records.sha256(ob))
        return {"ended": bool(ok), "rule": "b", "reason": "" if ok else "END record mismatch"}
    except Exception as exc:  # noqa: BLE001
        return {"ended": False, "rule": None, "reason": f"unreadable {exc!r}"}


def w2_attest(root=None, exclude=()) -> dict:
    root = Path(dc.ROOT if root is None else root)
    skip = {Path(p).resolve() for p in exclude}
    checked, live, bad = [], [], []
    seen = set()
    for pat in dc.CONTRACT["window"]["reservation_globs"]:
        for f in sorted(root.glob(pat)):
            if fnmatch.fnmatch(f.name, "*.END.json") or f.resolve() in skip or f in seen \
                    or not f.is_file():
                continue
            seen.add(f)
            try:
                rec = dc.read_json(f)
                if not isinstance(rec, dict) or "id" not in rec or "state" not in rec:
                    raise ValueError("not a reservation")
            except Exception:  # noqa: BLE001
                bad.append(str(f))
                continue
            ended = reservation_ended(f, root) if rec["state"] == "ACTIVE" else \
                {"ended": False, "rule": None}
            row = {"path": str(f), "id": rec["id"], "state": rec["state"],
                   "ended": ended["ended"], "rule": ended["rule"]}
            checked.append(row)
            if rec["state"] == "ACTIVE" and not ended["ended"]:
                live.append(row)
    status = "PASS" if not live and not bad else "INCONCLUSIVE/AUTHORITY"
    return {"status": status, "checked": checked, "live": live, "schema_failures": bad}
