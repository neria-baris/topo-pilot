"""Coordinator release verification (standard library only; no subprocess). No release exists in
job 0016.

A release is a coordinator-authored JSON file in the mailbox directory of the CURRENTLY dispatched
job. It is accepted only if it matches all of these:
- the live request.json (RUN_NEXT, job id, task digest);
- the source HEAD, read directly from the git files without spawning a process;
- this contract;
- the freeze record.

Issuer (spec v2.5 item 1): "claude-coordinator" releases are bound to the designated
coordinator's assumption record under the mailbox archive and to the live coordinator runtime
mode; "codex-coordinator" releases verify as before but are refused while the Claude
coordinator is active (Codex relinquished).

`scoring_released` must be a strict boolean. Scoring is unlocked only by `scoring_authority()`,
which requires scoring_released is True AND an owner_scoring_release_ref naming an existing
immutable owner-approval record by path, sha256 and a scope that includes "scoring". A
feasibility release never yields scored access.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from errors import ScoringAuthority

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MAILBOX = Path(r"X:\Downloads\projects\topo-pilot\agent-handoff")
SCHEMA = "x4-circle-history-release-v1"
STAGES = {"identity", "oracle", "charts", "precision", "export", "implementation"}
ISSUERS = ("claude-coordinator", "codex-coordinator")
CLAUDE_FIELDS = ("coordinator_session_id", "coordinator_assumption_ref")
CLAUDE_ACTIVE_MODE = "ACTIVE_CLAUDE_COORDINATOR"
ASSUMPTION_SCHEMA = "coordinator-assumption-v1"


class ReleaseError(RuntimeError):
    """Missing, malformed or mismatching coordinator release."""


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git_dir(repo: Path) -> tuple[Path, Path]:
    dot = repo / ".git"
    if dot.is_dir():
        return dot, dot
    text = dot.read_text(encoding="utf-8").strip()
    if not text.startswith("gitdir:"):
        raise ReleaseError("unrecognised .git file")
    gitdir = (repo / text.split(":", 1)[1].strip()).resolve()
    common = gitdir
    if (gitdir / "commondir").exists():
        common = (gitdir / (gitdir / "commondir").read_text(encoding="utf-8").strip()).resolve()
    return gitdir, common


def _head(repo: Path = REPO) -> str:
    """HEAD commit id read from the git files (worktree aware; loose or packed refs)."""
    gitdir, common = _git_dir(Path(repo))
    head = (gitdir / "HEAD").read_text(encoding="utf-8").strip()
    if not head.startswith("ref:"):
        return head
    ref = head.split(":", 1)[1].strip()
    for base in (gitdir, common):
        loose = base / ref
        if loose.exists():
            return loose.read_text(encoding="utf-8").strip()
    packed = common / "packed-refs"
    if packed.exists():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line and not line.startswith(("#", "^")) and line.split(" ", 1)[1] == ref:
                return line.split(" ", 1)[0]
    raise ReleaseError(f"cannot resolve HEAD ref {ref}")


def verify(path: Path, mailbox: Path = MAILBOX, out: Path | None = None) -> dict:
    """Return the release dict if every binding holds; ReleaseError otherwise."""
    path = Path(path)
    try:
        rel = json.loads(path.read_text(encoding="utf-8-sig"))
        request = json.loads((mailbox / "request.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ReleaseError(f"release or request unreadable: {type(exc).__name__}") from exc
    required = {
        "schema",
        "job_id",
        "task_sha256",
        "released_stages",
        "source_commit",
        "freeze_sha256",
        "contract_sha256",
        "scoring_released",
        "issued_by",
    }
    if not isinstance(rel, dict) or not required <= set(rel):
        raise ReleaseError("release missing required fields")
    job = str(rel["job_id"])
    if rel["schema"] != SCHEMA or rel["issued_by"] not in ISSUERS:
        raise ReleaseError("release schema/issuer")
    _verify_issuer(rel, mailbox)
    if path.resolve().parent != (mailbox / "jobs" / job).resolve():
        raise ReleaseError("release must live in the dispatched job's mailbox directory")
    live = (
        request.get("command"),
        request.get("job_id"),
        str(request.get("task_sha256", "")).upper(),
    )
    if live != ("RUN_NEXT", job, str(rel["task_sha256"]).upper()):
        raise ReleaseError("release does not match the live RUN_NEXT request")
    if _sha(mailbox / "jobs" / job / "task.md").upper() != str(rel["task_sha256"]).upper():
        raise ReleaseError("task.md digest mismatch")
    if not isinstance(rel["released_stages"], list) or not set(rel["released_stages"]) <= STAGES:
        raise ReleaseError("released_stages must be a list of known stages")
    if rel["source_commit"] != _head():
        raise ReleaseError("source HEAD differs from the released commit")
    if _sha(HERE / "CONTRACT.json") != rel["contract_sha256"]:
        raise ReleaseError("contract digest differs from the release")
    if out is None:
        contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
        out = Path(contract["resources"]["output_root"])
    freeze = Path(out) / "FREEZE.json"
    if not freeze.exists() or _sha(freeze) != rel["freeze_sha256"]:
        raise ReleaseError("freeze record missing or different from the release")
    if not isinstance(rel["scoring_released"], bool):
        raise ReleaseError("scoring_released must be a strict boolean")
    if rel["scoring_released"]:
        _owner_record(rel)
    return rel


def _runtime_mode(mailbox: Path):
    try:
        runtime = json.loads((mailbox / "coordinator_runtime.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ReleaseError(f"coordinator_runtime.json unreadable: {type(exc).__name__}") from exc
    return runtime.get("mode") if isinstance(runtime, dict) else None


def _verify_issuer(rel: dict, mailbox: Path) -> None:
    """Bind the issuer: Claude by its assumption record; Codex only while not relinquished."""
    mode = _runtime_mode(Path(mailbox))
    if rel["issued_by"] == "codex-coordinator":
        if any(k in rel for k in CLAUDE_FIELDS):
            raise ReleaseError("codex-coordinator release must not carry Claude coordinator fields")
        if mode == CLAUDE_ACTIVE_MODE:
            raise ReleaseError("codex-coordinator relinquished; the Claude coordinator is active")
        return
    session, ref = rel.get("coordinator_session_id"), rel.get("coordinator_assumption_ref")
    if not isinstance(session, str) or not session:
        raise ReleaseError("claude-coordinator release needs coordinator_session_id")
    if not isinstance(ref, dict) or not {"path", "sha256"} <= set(ref):
        raise ReleaseError(
            "claude-coordinator release needs coordinator_assumption_ref {path, sha256}"
        )
    record = Path(ref["path"])
    archive = (Path(mailbox) / "archive").resolve()
    if archive not in record.resolve().parents or not record.is_file():
        raise ReleaseError(
            "coordinator assumption record must be an existing file under the archive"
        )
    if _sha(record) != str(ref["sha256"]).lower():
        raise ReleaseError("coordinator assumption record hash mismatch")
    try:
        assumption = json.loads(record.read_text(encoding="utf-8-sig"))
    except ValueError as exc:
        raise ReleaseError("coordinator assumption record is not JSON") from exc
    if not isinstance(assumption, dict) or assumption.get("schema") != ASSUMPTION_SCHEMA:
        raise ReleaseError("coordinator assumption record schema")
    if assumption.get("coordinator_session_id") != session:
        raise ReleaseError("coordinator session differs from the assumption record")
    if mode != CLAUDE_ACTIVE_MODE:
        raise ReleaseError("coordinator runtime does not report the active Claude coordinator")


def _owner_record(rel: dict) -> dict:
    ref = rel.get("owner_scoring_release_ref")
    if not isinstance(ref, dict) or not {"path", "sha256", "scope"} <= set(ref):
        raise ReleaseError("scoring release needs owner_scoring_release_ref {path, sha256, scope}")
    record = Path(ref["path"])
    if not record.is_file() or _sha(record) != str(ref["sha256"]).lower():
        raise ReleaseError("owner scoring record missing or hash mismatch")
    if "scoring" not in list(ref["scope"]):
        raise ReleaseError("owner scoring record scope does not include scoring")
    return ref


def scoring_authority(rel: dict) -> ScoringAuthority:
    """The ONLY issuer of ScoringAuthority: a verified release with an owner scoring record."""
    if rel.get("scoring_released") is not True:
        raise ReleaseError("feasibility release: scoring is not released")
    ref = _owner_record(rel)
    return ScoringAuthority(
        owner_record_path=str(ref["path"]),
        owner_record_sha256=str(ref["sha256"]).lower(),
        scope=tuple(ref["scope"]),
        release_job_id=str(rel["job_id"]),
    )
