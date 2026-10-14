"""X5 G1 audit repairs (job 0007): full-hash source verification before and after computation,
STOP/budget-guarded exports and immutable output directories."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from topo_pilot.contracts import ArtifactStore

from .x5g1_controls import BudgetExceeded, RunControls, StopRequested

T = TypeVar("T")


class OutputExists(FileExistsError):
    """A completed output version already exists; it is never overwritten."""


class SourceTampered(RuntimeError):
    """A source artifact failed full-hash or payload verification."""


def verify_sources_full(store: ArtifactStore, expected: dict[str, tuple[type, str]],
                        consumer: str = "experiment") -> list[str]:
    """Failures for artifacts whose metadata hash differs from the full expected hash or whose
    payload no longer loads (the store re-hashes it); never raises."""
    out = []
    for aid, (cls, sha) in expected.items():
        try:
            meta_sha = str(store.meta(aid).payload_sha256)
            if meta_sha != sha:
                out.append(f"{aid}: payload_sha256 {meta_sha} != expected {sha}")
                continue
            store.load(cls, aid, consumer=consumer)
        except Exception as exc:  # noqa: BLE001 - every failure is reported, never raised
            out.append(f"{aid}: {type(exc).__name__}: {exc}")
    return out


def checked_computation(store: ArtifactStore, expected: dict[str, tuple[type, str]],
                        fn: Callable[[], T]) -> T:
    """Verify sources, run ``fn``, verify again; any failure raises ``SourceTampered`` and an
    after-failure discards the result."""
    bad = verify_sources_full(store, expected)
    if bad:
        raise SourceTampered("before: " + "; ".join(bad))
    result = fn()
    bad = verify_sources_full(store, expected)
    if bad:
        raise SourceTampered("after: " + "; ".join(bad))
    return result


def ensure_new_output_dir(path: Path) -> Path:
    """Create ``path``; refuse (``OutputExists``) if it already holds anything."""
    p = Path(path)
    if p.exists() and any(p.iterdir()):
        raise OutputExists(f"output version {p} already exists and is not empty")
    p.mkdir(parents=True, exist_ok=True)
    return p


def guarded_export(ctl: RunControls, steps: list[tuple[str, Callable[[], None]]],
                   status_path: Path) -> None:
    """Run export steps with guards before and after each; on STOP/budget write only a small
    status record, skip the remaining steps and re-raise."""
    done: list[str] = []
    try:
        for name, fn in steps:
            ctl.guard(f"export {name}")
            fn()
            done.append(name)
            ctl.guard(f"export {name} done")
    except (StopRequested, BudgetExceeded) as exc:
        status = ("STOPPED_DURING_EXPORT" if isinstance(exc, StopRequested)
                  else "BUDGET_DURING_EXPORT")
        Path(status_path).parent.mkdir(parents=True, exist_ok=True)
        Path(status_path).write_text(json.dumps(
            {"status": status, "completed_steps": done,
             "cause": f"{type(exc).__name__}: {exc}"}, indent=1), encoding="utf-8")
        raise
