"""Gate and stage records for runner.py (API.md spec v2.4 items 1 and 8; builder-tested).

GATES.jsonl holds gate outcomes. STAGES.jsonl holds STARTED / COMPLETED / REFUSED stage events
with evidence hashes. begin() enforces the prerequisites before any stage work: completed prior
stage, its PASS gates, unchanged evidence, no non-PASS gate before a scientific stage, and no
second attempt of a stage (no retry or recompute, also after a kill). Refusals never write a
gate record.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
from errors import Invalid, JoinError, Unresolved

PREREQUISITE = {"identity": None, "oracle": "identity", "charts": "oracle", "precision": "charts"}


class StageRefused(RuntimeError):
    """Out-of-order, repeated or integrity-failed stage invocation (no gate record)."""


def _utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_new(path: Path, obj) -> None:
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, indent=1, sort_keys=True, default=str) + "\n")


def save_npz(path: Path, **arrays) -> None:
    with Path(path).open("xb") as handle:
        np.savez_compressed(handle, **arrays)


def _lines(path: Path) -> list:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def gates_so_far(out: Path) -> list:
    return _lines(Path(out) / "GATES.jsonl")


def stages_so_far(out: Path) -> list:
    return _lines(Path(out) / "STAGES.jsonl")


def _append(path: Path, entry: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, default=str) + "\n")


def record_gate(out: Path, gate: str, status: str, **details) -> str:
    entry = {"gate": gate, "status": status, "criterion_met": status == "PASS", "utc": _utc()}
    _append(Path(out) / "GATES.jsonl", dict(entry, **details))
    return status


def run_gate(out: Path, gate: str, fn):
    """Invalid/JoinError -> FAIL_TECHNICAL; Unresolved -> INCONCLUSIVE (spec v2.4 item 1)."""
    try:
        return fn()
    except (Invalid, JoinError) as exc:
        record_gate(out, gate, "FAIL_TECHNICAL", reason=f"{type(exc).__name__}: {exc}")
        raise
    except Unresolved as exc:
        record_gate(out, gate, "INCONCLUSIVE", reason=str(exc))
        raise


def refuse(out: Path, stage: str, reason: str, integrity: bool = False):
    _append(
        Path(out) / "STAGES.jsonl",
        {
            "stage": stage,
            "event": "REFUSED",
            "utc": _utc(),
            "reason": reason,
            "integrity": integrity,
        },
    )
    raise StageRefused(f"{stage}: {reason}")


def _check_prerequisite(out: Path, stage: str, models, stages: list, gates: list) -> None:
    prior = PREREQUISITE[stage]
    done = [r for r in stages if r["stage"] == prior and r["event"] == "COMPLETED"]
    if not done:
        refuse(out, stage, f"prerequisite stage {prior} not completed")
    for name, digest in done[-1]["evidence"].items():
        path = Path(out) / name
        if not path.exists() or sha256(path) != digest:
            refuse(out, stage, f"evidence {name} of {prior} changed or missing", integrity=True)
    passed = [g for g in gates if g["status"] == "PASS"]
    if stage == "oracle":
        if not any(g["gate"] == "identity" for g in passed):
            refuse(out, stage, "identity gate has not passed")
        ident = json.loads((Path(out) / "IDENTITY.json").read_text(encoding="utf-8"))
        rows = {int(m): ident["report"][str(m)]["rows"] for m in models}
        if any(r != ident["joined_rows"] for r in rows.values()):
            refuse(out, stage, f"identity does not join every model on the same rows: {rows}")
    elif stage == "charts":
        if not any(g["gate"] == "process_and_reference" for g in passed):
            refuse(out, stage, "process_and_reference gate has not passed")
    elif stage == "precision":
        certified = {g.get("model") for g in passed if g["gate"] == "row_score_certificates"}
        if certified != set(models):
            refuse(out, stage, f"row_score_certificates passed only for {sorted(certified)}")


def begin(out: Path, stage: str, models) -> None:
    """Refuse a repeated, out-of-order or integrity-failed invocation; else record STARTED."""
    out = Path(out)
    stages, gates = stages_so_far(out), gates_so_far(out)
    if any(r["stage"] == stage and r["event"] == "STARTED" for r in stages):
        refuse(out, stage, "stage already attempted; no retry or recompute")
    if stage in PREREQUISITE:
        stopped = [g for g in gates if g["status"] != "PASS"]
        if stopped:
            refuse(
                out, stage, f"cohort ended at gate {stopped[0]['gate']} ({stopped[0]['status']})"
            )
        if PREREQUISITE[stage] is not None:
            _check_prerequisite(out, stage, list(models), stages, gates)
    _append(out / "STAGES.jsonl", {"stage": stage, "event": "STARTED", "utc": _utc()})


def complete(out: Path, stage: str, files, outcome: str = "done") -> None:
    evidence = {name: sha256(Path(out) / name) for name in files}
    _append(
        Path(out) / "STAGES.jsonl",
        {
            "stage": stage,
            "event": "COMPLETED",
            "utc": _utc(),
            "evidence": evidence,
            "outcome": outcome,
        },
    )


def attempts_without_completion(out: Path) -> list:
    stages = stages_so_far(out)
    started = [r["stage"] for r in stages if r["event"] == "STARTED"]
    finished = {r["stage"] for r in stages if r["event"] == "COMPLETED"}
    return [s for s in started if s not in finished]
