"""HWSU records: gate runner, stages, lineage, ledger, pauses, registry risk (API.md §5.1-§5.2).

The freeze/OF-B names (hwsu_freeze) and the reservation, obligation, name-rule and inventory names
(hwsu_resv) are split by size (API erratum) and stay reachable as hwsu_records.<name>.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import fnmatch
import hashlib
import json
import os
import time
from fractions import Fraction
from pathlib import Path

import hwsc_records
import k4b_release
import op_guard
import stage_records
from c1_records import C1GateFailure, classify_exception
from oracle_profile import ProfileError
from topo_pilot.contracts import StageFailure

class Paused(Exception):
    """Raised by pause_or_raise_u."""


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canon_sha(obj) -> str:
    return _sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def _append(path, entry) -> None:
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, default=str) + "\n")


def status_of(exc) -> str:
    if isinstance(exc, C1GateFailure):
        s = str(exc.status)
    elif isinstance(exc, Paused):
        return "PAUSE"
    elif isinstance(exc, ProfileError):
        s = "FAIL_TECHNICAL/IDENTITY"
    elif isinstance(exc, StageFailure):
        s = "FAIL_TECHNICAL/SAMPLER"
    else:
        s = str(classify_exception(exc)[0])
    return s if "/" in s or s == "PAUSE" else f"{s}/UNEXPECTED"


def run_gates_u(out, steps, continuing=("PASS", "SHARE_DROPPED"), dry_continue=False) -> list:
    recs, stopped = [], False
    for gate, fn in steps:
        if stopped and not dry_continue:
            stage_records.record_gate(Path(out), gate, "NOT_RUN")
            recs.append({"gate": gate, "status": "NOT_RUN"})
            continue
        try:
            details = fn() or {}
            status = details.pop("status", "PASS") if isinstance(details, dict) else "PASS"
        except Exception as exc:  # noqa: BLE001  every failure is recorded, then stops
            status = status_of(exc)
            details = {"reason": str(getattr(exc, "reason", exc))[:2000]}
            if status == "PAUSE":
                stage_records.record_gate(Path(out), gate, "PAUSE", **details)
                raise
        details = json.loads(json.dumps(details, default=str))
        stage_records.record_gate(Path(out), gate, status, **details)
        recs.append(dict(details, gate=gate, status=status))
        stopped = stopped or status not in continuing
    return recs


def begin_stage(out, stage) -> None:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    op_guard.write_marker(out, {"state": "idle", "stage": stage, "label": f"stage {stage}",
                                "seq": 0})
    _append(out / "STAGES.jsonl", {"stage": stage, "event": "BEGIN", "utc": utc()})


def complete_stage(out, stage, files) -> dict:
    out = Path(out)
    rel = {}
    for f in files:
        p = Path(f) if Path(f).is_absolute() else out / f
        rel[p.resolve().relative_to(out.resolve()).as_posix()] = stage_records.sha256(p)
    ev = {"stage": stage, "event": "STAGE_COMPLETE", "utc": utc(), "files": rel}
    _append(out / "STAGES.jsonl", ev)
    return ev


def lineage_u(out) -> dict:
    out = Path(out)
    if not out.exists():
        return {"status": "PASS", "reason": "store absent"}
    recorded = set()
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            recorded |= set(e.get("files", {}).items())
    tops = set(k4b_release.RECORD_FILES) | set(uc.CONTRACT["store_layout"]["top_level_records"])
    bad = hwsc_records.superseded_ok(out) if (out / "superseded").is_dir() else []
    for f in out.rglob("*"):
        if not f.is_file() or uc.blinded(f):
            continue
        rel = f.relative_to(out)
        top = rel.parts[0]
        if top in ("superseded", "logs", "operations", "tmp") or top.startswith("tmp-"):
            continue
        if len(rel.parts) == 1 and any(fnmatch.fnmatchcase(top, t) for t in tops):
            continue
        if top == "reservations" and len(rel.parts) == 2 and rel.name.endswith(".json"):
            continue
        if (rel.as_posix(), stage_records.sha256(f)) not in recorded:
            bad.append(rel.as_posix())
    if bad:
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"unrecorded files: {bad[:10]}")
    return {"status": "PASS", "n_recorded": len(recorded)}


# ------------------------------------------------------------------- budget, ledger (§10)
def central(stage, contract=None) -> float:
    c = (uc.CONTRACT if contract is None else contract)["cpu"]["central_s"]
    if stage not in c:
        raise ValueError(f"unknown stage {stage!r}")
    return float(c[stage])


def cumulative_central(stage, contract=None) -> float:
    c = (uc.CONTRACT if contract is None else contract)["cpu"]
    order = c["stage_order"]
    if stage not in order:
        raise ValueError(f"unknown stage {stage!r}")
    return float(sum(c["central_s"][s] for s in order[:order.index(stage) + 1]))


def pause_check_u(stage, stage_cpu, cum_cpu, contract=None) -> dict:
    m = (uc.CONTRACT if contract is None else contract)["cpu"]["multiplier"]
    st, ct = m * central(stage, contract), m * cumulative_central(stage, contract)
    bs, bc = stage_cpu > st, cum_cpu > ct
    trig = "BOTH" if bs and bc else "STAGE" if bs else "CUMULATIVE" if bc else None
    return {"pause": bs or bc, "trigger": trig, "stage_cpu": stage_cpu, "stage_threshold": st,
            "cum_cpu": cum_cpu, "cum_threshold": ct}


def ledger_read(path) -> dict:
    if not Path(path).exists():
        return {"study": "hwsu-v1", "entries": [], "cumulative_cpu_s": 0.0}
    return uc.read_json(path)


def ledger_append(path, label, job, stage, cpu_s, source) -> dict:
    p, led = Path(path), ledger_read(path)
    if any(e.get("label") == label for e in led["entries"]):
        raise C1GateFailure("FAIL_TECHNICAL/LEDGER", f"label {label} already in the ledger")
    led["entries"].append({"label": label, "job": job, "stage": stage, "cpu_s": float(cpu_s),
                           "source": str(source), "utc": utc()})
    led["cumulative_cpu_s"] = float(sum(e["cpu_s"] for e in led["entries"]))
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return led


def running_cpu(stage, ledger_path, t0) -> tuple:
    now = time.process_time() - t0
    led = ledger_read(ledger_path)
    return (sum(e["cpu_s"] for e in led["entries"] if e.get("stage") == stage) + now,
            float(led["cumulative_cpu_s"]) + now)


def pause_or_raise_u(out, stage, t0, ledger_path=None, cont=None) -> None:
    if ledger_path is None:
        return
    c = json.loads(Path(cont).read_text(encoding="utf-8")) if cont else {}
    if stage in c.get("stages", []):
        return
    sc, cum = running_cpu(stage, ledger_path, t0)
    chk = pause_check_u(stage, sc, cum)
    if chk["pause"]:
        _append(Path(out) / "STAGES.jsonl", {"stage": stage, "event": "PAUSE", "utc": utc()})
        stage_records.record_gate(Path(out), f"PAUSE_{stage}", "PAUSE", **chk)
        raise Paused(f"{stage}: {chk['trigger']}")


def registry_risk_u(p_d2a, rows) -> dict:
    value = int(rows) * Fraction(float(p_d2a))
    return {"rows": int(rows), "value": str(value), "ok": value <= Fraction(1, 100)}



_SPLIT = {"hwsu_resv": ("ARRAY_SUFFIXES", "name_class", "save_array", "reservation_file",
                        "write_reservation", "end_reservation", "w2_attestation",
                        "obligation_name", "write_obligation", "read_obligation",
                        "root_inventory"),
          "hwsu_freeze": ("implementation_files", "freeze_of", "verify_freeze_of", "of_b")}


def __getattr__(name):
    import importlib

    for mod, names in _SPLIT.items():
        if name in names:
            return getattr(importlib.import_module(mod), name)
    raise AttributeError(f"module 'hwsu_records' has no attribute {name!r}")
