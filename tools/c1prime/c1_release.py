"""C1' coordinator release (API.md §13; protocol §17, §18 field 2). Same checks as K4's
release.py (provenance: tools/x4_circle_history/release.py, Claude-issuer branch), separately
versioned: schema c1prime-release-v1, C1 stages, issuer "claude-coordinator" only, plus the
stage-specific bindings of R1 (authority, registry v1) and R3 (N_test, k, registry v2)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import c1_config

MAILBOX = Path(r"X:\Downloads\projects\topo-pilot\agent-handoff")
SCHEMA = "c1prime-release-v1"
STAGES = {"oracle", "calibration", "validation", "fresh"}
ISSUER = "claude-coordinator"
CLAUDE_ACTIVE_MODE = "ACTIVE_CLAUDE_COORDINATOR"
ASSUMPTION_SCHEMA = "coordinator-assumption-v1"
REQUIRED = {"schema", "job_id", "task_sha256", "released_stages", "source_commit",
            "freeze_sha256", "contract_sha256", "issued_by", "coordinator_session_id",
            "coordinator_assumption_ref"}


class ReleaseError(RuntimeError):
    """Missing, malformed or mismatching C1 release."""


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ReleaseError(f"{Path(path).name} unreadable: {type(exc).__name__}") from exc


def _git_dirs(repo: Path) -> tuple:
    dot = Path(repo) / ".git"
    if dot.is_dir():
        return dot, dot
    text = dot.read_text(encoding="utf-8").strip()
    if not text.startswith("gitdir:"):
        raise ReleaseError("unrecognised .git file")
    gitdir = (Path(repo) / text.split(":", 1)[1].strip()).resolve()
    common = gitdir
    if (gitdir / "commondir").exists():
        common = (gitdir / (gitdir / "commondir").read_text(encoding="utf-8").strip()).resolve()
    return gitdir, common


def git_head(repo=c1_config.REPO) -> str:
    gitdir, common = _git_dirs(Path(repo))
    text = (gitdir / "HEAD").read_text(encoding="utf-8").strip()
    if not text.startswith("ref:"):
        return text
    ref = text.split(":", 1)[1].strip()
    for base in (gitdir, common):
        if (base / ref).exists():
            return (base / ref).read_text(encoding="utf-8").strip()
    packed = common / "packed-refs"
    if packed.exists():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line and not line.startswith(("#", "^")) and line.split(" ", 1)[1] == ref:
                return line.split(" ", 1)[0]
    raise ReleaseError(f"cannot resolve HEAD ref {ref}")


def _bound_file(ref, what) -> None:
    if not isinstance(ref, dict) or not {"path", "sha256"} <= set(ref):
        raise ReleaseError(f"{what} needs {{path, sha256}}")
    if not Path(ref["path"]).is_file() or _sha(ref["path"]) != str(ref["sha256"]).lower():
        raise ReleaseError(f"{what} missing or hash mismatch")


def _verify_issuer(rel: dict, mailbox: Path) -> None:
    runtime = _json(mailbox / "coordinator_runtime.json")
    if not isinstance(runtime, dict) or runtime.get("mode") != CLAUDE_ACTIVE_MODE:
        raise ReleaseError("coordinator runtime does not report the active Claude coordinator")
    ref = rel["coordinator_assumption_ref"]
    if not isinstance(ref, dict) or not {"path", "sha256"} <= set(ref):
        raise ReleaseError("coordinator_assumption_ref needs {path, sha256}")
    record, archive = Path(ref["path"]), (mailbox / "archive").resolve()
    if archive not in record.resolve().parents or not record.is_file():
        raise ReleaseError("coordinator assumption record must be a file under the archive")
    if _sha(record) != str(ref["sha256"]).lower():
        raise ReleaseError("coordinator assumption record hash mismatch")
    assumption = _json(record)
    if not isinstance(assumption, dict) or assumption.get("schema") != ASSUMPTION_SCHEMA:
        raise ReleaseError("coordinator assumption record schema")
    if assumption.get("coordinator_session_id") != rel["coordinator_session_id"]:
        raise ReleaseError("coordinator session differs from the assumption record")


def _stage_fields(rel: dict) -> None:
    stages = set(rel["released_stages"])
    if "oracle" in stages:
        auth = rel.get("authority")
        if not isinstance(auth, dict):
            raise ReleaseError("R1 needs authority {owner_decisions, diag_json, job_0023_accept}")
        for key in ("owner_decisions", "diag_json", "job_0023_accept"):
            _bound_file(auth.get(key), f"authority.{key}")
        _bound_file(rel.get("registry_v1"), "registry_v1")
    if "fresh" in stages:
        if rel.get("N_test") not in (4096, 8192, 16384):
            raise ReleaseError("R3 needs N_test in {4096, 8192, 16384}")
        if not isinstance(rel.get("k"), int) or not 1 <= rel["k"] <= 5:
            raise ReleaseError("R3 needs an integer k in 1..5")
        _bound_file(rel.get("registry_v2"), "registry_v2")


def authorized_worker(rel: dict, path) -> str:
    """The executing worker session (protocol §18: "the authorized executing worker session").
    A verified release may name it as `worker_session`; the dispatched task.md must name the
    same session. Without the field, the CONTRACT default applies (job-0026 behaviour)."""
    worker = rel.get("worker_session")
    if worker is None:
        return str(c1_config.CONTRACT["resources"]["worker_session"])
    task = Path(path).resolve().parent / "task.md"
    if not isinstance(worker, str) or not worker or worker not in task.read_text(encoding="utf-8"):
        raise ReleaseError("release worker_session must be a session named in the job's task.md")
    return worker


def verify(path, mailbox=MAILBOX, out=None, head=None,
           contract_path=c1_config.CONTRACT_PATH) -> dict:
    path, mailbox = Path(path), Path(mailbox)
    rel, request = _json(path), _json(mailbox / "request.json")
    if not isinstance(rel, dict) or not REQUIRED <= set(rel):
        raise ReleaseError("release missing required fields")
    if rel["schema"] != SCHEMA or rel["issued_by"] != ISSUER:
        raise ReleaseError("release schema/issuer")
    _verify_issuer(rel, mailbox)
    job = str(rel["job_id"])
    if path.resolve().parent != (mailbox / "jobs" / job).resolve():
        raise ReleaseError("release must live in the dispatched job's mailbox directory")
    live = (request.get("command"), request.get("job_id"),
            str(request.get("task_sha256", "")).upper())
    if live != ("RUN_NEXT", job, str(rel["task_sha256"]).upper()):
        raise ReleaseError("release does not match the live RUN_NEXT request")
    if _sha(mailbox / "jobs" / job / "task.md").upper() != str(rel["task_sha256"]).upper():
        raise ReleaseError("task.md digest mismatch")
    stages = rel["released_stages"]
    if not isinstance(stages, list) or not stages or not set(stages) <= STAGES:
        raise ReleaseError("released_stages must be a non-empty list of C1 stages")
    if rel["source_commit"] != (head if head is not None else git_head()):
        raise ReleaseError("source HEAD differs from the released commit")
    if _sha(contract_path) != rel["contract_sha256"]:
        raise ReleaseError("contract digest differs from the release")
    out = Path(out) if out is not None else Path(c1_config.CONTRACT["resources"]["output_root"])
    freeze = out / "FREEZE.json"
    if not freeze.exists() or _sha(freeze) != rel["freeze_sha256"]:
        raise ReleaseError("freeze record missing or different from the release")
    _stage_fields(rel)
    return rel
