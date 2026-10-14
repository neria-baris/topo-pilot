"""Coordinator release verification (standard library only). No release exists in job 0016.

A release is a coordinator-authored JSON file inside the mailbox job directory of the CURRENTLY
dispatched job. It is accepted only if it matches the live request.json (RUN_NEXT, job id, task
digest), the committed source HEAD, the freeze record and this contract. Scoring stays locked
unless the release explicitly carries an owner scoring release. Any mismatch refuses.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MAILBOX = Path(r"X:\Downloads\projects\topo-pilot\agent-handoff")
SCHEMA = "x4-circle-history-release-v1"
STAGES = {"identity", "oracle", "charts", "precision", "export", "implementation"}


class ReleaseError(RuntimeError):
    """Missing, malformed or mismatching coordinator release."""


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _head() -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


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
    if rel["schema"] != SCHEMA or rel["issued_by"] != "codex-coordinator":
        raise ReleaseError("release schema/issuer")
    if path.resolve().parent != (mailbox / "jobs" / job).resolve():
        raise ReleaseError("release must live in the dispatched job's mailbox directory")
    if (
        request.get("command"),
        request.get("job_id"),
        str(request.get("task_sha256", "")).upper(),
    ) != ("RUN_NEXT", job, str(rel["task_sha256"]).upper()):
        raise ReleaseError("release does not match the live RUN_NEXT request")
    task = mailbox / "jobs" / job / "task.md"
    if _sha(task).upper() != str(rel["task_sha256"]).upper():
        raise ReleaseError("task.md digest mismatch")
    if not set(rel["released_stages"]) <= STAGES:
        raise ReleaseError("unknown stage in release")
    if rel["source_commit"] != _head():
        raise ReleaseError("source HEAD differs from the released commit")
    if _sha(HERE / "CONTRACT.json") != rel["contract_sha256"]:
        raise ReleaseError("contract digest differs from the release")
    out = (
        Path(out)
        if out
        else Path(
            json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))["resources"][
                "output_root"
            ]
        )
    )
    freeze = out / "FREEZE.json"
    if not freeze.exists() or _sha(freeze) != rel["freeze_sha256"]:
        raise ReleaseError("freeze record missing or different from the release")
    if rel["scoring_released"] is not False and not rel.get("owner_scoring_release_ref"):
        raise ReleaseError("scoring may only be released with an explicit owner release reference")
    return rel
