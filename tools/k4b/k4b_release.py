"""K4b releases, pin check, freeze, reservation records and the rerun/lineage rule (API.md §12.1).

Protocol §11.5 (S0 commit binding), §11.7 (store), §11.8 (rerun and lineage), RC8
(reservations), R10 (worker session from the release, re-implemented here).
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import k4b_config
import stage_records
from c1_records import C1GateFailure

AUTHORITY = "FAIL_TECHNICAL/AUTHORITY"
LINEAGE = "FAIL_TECHNICAL/LINEAGE"
FIELDS = ("kind", "job_id", "task_sha256", "worker_session", "protocol_sha256",
          "freeze_sha256", "reservation")
FIELDS_B = ("N", "k", "kreg2_sha256", "kreg2_sources", "accept")
RECORD_FILES = ("GATES.jsonl", "STAGES.jsonl", "CHART_CONSTRUCTIONS_trained.json",
                "CHART_CONSTRUCTIONS_init.json", "FREEZE.json", "SEALED_VALIDATION.json",
                "cpu_ledger.json", "cpu_ledger.emergency.jsonl", "RUN.lock", "METER_ACTIVE.lock",
                "OPERATION_ACTIVE.json", "OPERATIONS.jsonl")
FREE_DIRS = ("logs", "operations")


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def authorized_worker(release, session) -> bool:
    w = release.get("worker_session") if isinstance(release, dict) else None
    return isinstance(w, str) and isinstance(session, str) and bool(w) and w == session


def verify_release(path, kind, task_sha256, session, freeze_path=None) -> dict:
    try:
        rel = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001  missing or malformed release
        raise C1GateFailure(AUTHORITY, f"release unreadable: {exc!r}") from exc
    need = FIELDS + (FIELDS_B if kind == "B" else ())
    missing = [f for f in need if rel.get(f) is None]
    if missing:
        raise C1GateFailure(AUTHORITY, f"release fields missing: {missing}")
    if rel["kind"] != kind:
        raise C1GateFailure(AUTHORITY, f"release kind {rel['kind']} != {kind}")
    if str(rel["task_sha256"]).upper() != str(task_sha256).upper():
        raise C1GateFailure(AUTHORITY, "release task_sha256 mismatch")
    if rel["protocol_sha256"] != k4b_config.CONTRACT["protocol_sha256"]:
        raise C1GateFailure(AUTHORITY, "release protocol_sha256 mismatch")
    if not authorized_worker(rel, session):
        raise C1GateFailure(AUTHORITY, "worker session not authorised by the release")
    if freeze_path is not None and stage_records.sha256(freeze_path) != rel["freeze_sha256"]:
        raise C1GateFailure(AUTHORITY, "release freeze_sha256 mismatch")
    return rel


def _git(repo, *args) -> bytes:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, check=True).stdout


def _chart_section(repo, ref) -> dict:
    return json.loads(_git(repo, "show", f"{ref}:tools/c1prime/CONTRACT.json"))["chart"]


def pin_check(repo, r_ref, h_exec) -> dict:
    """S0 (§11.5): only allowlisted additions on the protected paths; reuse hashes at h_exec."""
    c = k4b_config.CONTRACT
    diff = _git(repo, "diff", "--no-renames", "--name-status", r_ref, h_exec, "--",
                *c["s0"]["protected_paths"]).decode("utf-8").splitlines()
    bad = [ln for ln in diff if ln.strip() and not (
        ln.split("\t")[0] == "A" and ln.split("\t")[-1].startswith(("tools/k4b/", "tests/k4b/")))]
    hashes = dict(c["reuse_sha256"], **c["protected_sha256"])
    mism = [p for p, h in hashes.items() if _sha_bytes(_git(repo, "show", f"{h_exec}:{p}")) != h]
    chart_equal = _chart_section(repo, h_exec) == _chart_section(repo, r_ref)
    gap = c["authority"]["gap_doc"]
    gap_ok = _sha_bytes(_git(repo, "show", f"{h_exec}:{gap['path']}")) == gap["blob_sha256"]
    ok = not bad and not mism and chart_equal and gap_ok
    return {"status": "PASS" if ok else "INVALID", "r_ref": r_ref, "h_exec": h_exec,
            "n_diff": len(diff), "offending": bad, "hash_mismatch": mism,
            "c1prime_chart_equal": chart_equal, "gap_doc_ok": gap_ok}


def environment() -> dict:
    import numpy

    return {"python": sys.version, "executable": sys.executable, "platform": platform.platform(),
            "numpy": numpy.__version__}


def accept_tests(out, record) -> str:
    """tests/ACCEPTED.json (exclusive create): counts, junit and the sha256 of every test file."""
    path = Path(out) / "tests" / "ACCEPTED.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, dict(record, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                 time.gmtime())))
    return stage_records.sha256(path)


def freeze(out, repo, h_exec, accepted_sha256=None) -> dict:
    """FREEZE.json (exclusive create): protocol, h_exec, k4b and reuse file sha256, environment."""
    c = k4b_config.CONTRACT
    names = _git(repo, "ls-tree", "-r", "--name-only", h_exec, "--", "tools/k4b", "tests/k4b")
    files = {p: _sha_bytes(_git(repo, "show", f"{h_exec}:{p}"))
             for p in names.decode("utf-8").splitlines()}
    reuse = {p: _sha_bytes(_git(repo, "show", f"{h_exec}:{p}"))
             for p in list(c["reuse_sha256"]) + list(c["protected_sha256"])}
    record = {"scope": k4b_config.SCOPE, "protocol_sha256": c["protocol_sha256"],
              "contract_sha256": files.get("tools/k4b/CONTRACT.json"), "r_ref": c["commits"][
                  "r_ref"], "h_exec": h_exec, "k4b_files": files, "reuse_files": reuse,
              "accepted_tests_sha256": accepted_sha256, "environment": environment(),
              "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    stage_records.write_new(Path(out) / "FREEZE.json", record)
    return record


def start_reservation(path, scope, utc) -> dict:
    rec = {"id": f"RES-{scope}", "scope": scope, "start_utc": utc, "end_utc": None,
           "state": "ACTIVE", "interruptions": [], "job_states": {}}
    stage_records.write_new(path, rec)
    return rec


def verify_reservation(path, release, sampling_began=False) -> dict:
    breach = "STOP/LINEAGE_REVIEW" if sampling_began else "CANCEL_RELEASE"
    try:
        rec = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"status": breach, "reason": f"reservation unreadable: {exc!r}"}
    if rec.get("id") != release.get("reservation"):
        return {"status": breach, "reason": "reservation id differs from the release"}
    if rec.get("state") != "ACTIVE" or rec.get("interruptions"):
        return {"status": breach, "reason": f"reservation {rec.get('state')}, "
                f"{len(rec.get('interruptions') or [])} interruptions"}
    return {"status": "PASS", "record": rec}


def archive_attempt(out, job, files, record_suffixes) -> Path:
    """§11.8: move the attempt's files and record suffixes to superseded/<job>/ + SHA256SUMS."""
    out = Path(out)
    dest = out / "superseded" / str(job)
    dest.mkdir(parents=True, exist_ok=False)
    sums = []
    for f in files:
        f = Path(f)
        rel = f.resolve().relative_to(out.resolve())
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), str(target))
        sums.append(f"{stage_records.sha256(target)}  {rel.as_posix()}")
    for name, text in (record_suffixes or {}).items():
        target = dest / "records" / f"{name}.suffix"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8", newline="") as handle:
            handle.write(text)
        sums.append(f"{stage_records.sha256(target)}  records/{name}.suffix")
    (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    return dest


def restore_records(out, verified) -> None:
    out = Path(out)
    for name, data in verified.items():
        (out / name).write_bytes(data)
        if (out / name).read_bytes() != data:
            raise C1GateFailure(LINEAGE, f"{name} not restored byte-exactly")


def _superseded_ok(out) -> list:
    bad = []
    for job in sorted(p for p in (out / "superseded").glob("*") if p.is_dir()):
        sums = job / "SHA256SUMS"
        listed = {}
        if sums.is_file():
            for line in sums.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    h, _, rel = line.partition("  ")
                    listed[rel] = h
        for f in job.rglob("*"):
            if f.is_file() and f != sums:
                rel = f.relative_to(job).as_posix()
                if listed.get(rel) != stage_records.sha256(f):
                    bad.append(str(f))
    return bad


def lineage_ok(out) -> dict:
    """PASS iff the store is absent or holds only this lineage's recorded files (§11.8 item 7)."""
    out = Path(out)
    if not out.exists():
        return {"status": "PASS", "reason": "store absent"}
    recorded = {}
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            recorded.update(e.get("files", {}))
    bad = _superseded_ok(out)
    for f in out.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(out)
        top = rel.parts[0]
        if top == "superseded" or (len(rel.parts) == 1 and top in RECORD_FILES):
            continue
        if top in FREE_DIRS or top.startswith("tmp-") or rel.as_posix() == "tests/ACCEPTED.json":
            continue
        if recorded.get(rel.as_posix()) != stage_records.sha256(f):
            bad.append(rel.as_posix())
    if bad:
        raise C1GateFailure(LINEAGE, f"unrecorded prior files: {bad[:10]}")
    return {"status": "PASS", "n_recorded": len(recorded)}


def regenerated_identical(old_sha, new_path) -> bool:
    if stage_records.sha256(new_path) != old_sha:
        raise C1GateFailure(LINEAGE, f"{Path(new_path).name} did not regenerate bit-identically")
    return True


def needs_owner(correction) -> bool:
    """True iff an outcome-bearing quantity would change, or was computed at/after failure."""
    return any(q.get("outcome_bearing") and (q.get("changed") or q.get("at_or_after_failure"))
               for q in correction.get("quantities", []))
