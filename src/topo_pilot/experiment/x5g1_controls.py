"""X5 G1 run controls (x5g1-feas-v2 §7): STOP/budget guard and a crash-safe cumulative ledger."""

from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, StageFailure


class StopRequested(RuntimeError):
    """The mailbox STOP file exists."""


class BudgetExceeded(RuntimeError):
    """The per-run or cumulative CPU cap was reached."""


class LedgerCorrupt(RuntimeError):
    """The existing ledger cannot be parsed; it is left untouched."""


class RunControls:
    """Guard before/after operations and always persist a ledger entry on exit.

    The ledger ``{"entries": [...], "cumulative_cpu_s": float}`` is appended atomically (temp file
    plus ``os.replace``), never reset; the exit status is ``ok``, ``stopped``, ``budget`` or
    ``error:<ExceptionName>`` and ``cause`` holds the exception text; exceptions are never
    suppressed. ``try/finally`` cannot record CPU of a process killed abruptly (task kill, power
    loss); such costs are absent from the ledger and must be reported as unknown.
    """

    def __init__(self, ledger_path: Path, cap_s: float, stop_path: Path, job: str,
                 cumulative_cap_s: float) -> None:
        self.ledger_path, self.stop_path = Path(ledger_path), Path(stop_path)
        self.cap_s, self.cumulative_cap_s, self.job = cap_s, cumulative_cap_s, job
        self.steps: list[dict] = []
        self.outcome: str | None = None
        self.prior = self._read()["cumulative_cpu_s"]
        self.t0 = time.process_time()

    def _read(self) -> dict:
        if not self.ledger_path.exists():
            return {"entries": [], "cumulative_cpu_s": 0.0}
        try:
            data = json.loads(self.ledger_path.read_text(encoding="utf-8"))
            cum = data["cumulative_cpu_s"]
            entries = data["entries"]
        except (ValueError, KeyError, TypeError) as exc:
            raise LedgerCorrupt(f"{self.ledger_path}: {exc}") from exc
        if (isinstance(cum, bool) or not isinstance(cum, (int, float)) or not math.isfinite(cum)
                or cum < 0):
            raise LedgerCorrupt(f"{self.ledger_path}: invalid cumulative_cpu_s {cum!r}")
        if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
            raise LedgerCorrupt(f"{self.ledger_path}: entries must be a list of objects")
        return data

    def cpu(self) -> float:
        return time.process_time() - self.t0

    def guard(self, step: str) -> None:
        used = self.cpu()
        self.steps.append({"step": step, "cpu_s": round(used, 3)})
        if self.stop_path.exists():
            raise StopRequested(step)
        if used > self.cap_s or self.prior + used > self.cumulative_cap_s:
            raise BudgetExceeded(f"{used:.1f} CPU s at {step}")

    def __enter__(self) -> RunControls:
        self.t0 = time.process_time()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        status = ("ok" if exc_type is None else "stopped" if exc_type is StopRequested
                  else "budget" if exc_type is BudgetExceeded else f"error:{exc_type.__name__}")
        ledger = self._read()
        cpu = self.cpu()
        ledger["entries"].append({"job": self.job, "cpu_s": round(cpu, 3), "status": status,
                                  "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                  "outcome": self.outcome,
                                  "cause": None if exc_type is None else
                                  f"{exc_type.__name__}: {exc}", "steps": self.steps})
        ledger["cumulative_cpu_s"] = round(float(ledger["cumulative_cpu_s"]) + cpu, 3)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.ledger_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(ledger, indent=1), encoding="utf-8")
        os.replace(tmp, self.ledger_path)
        return False


def verify_parents(store: ArtifactStore, expected: dict[str, str]) -> list[str]:
    """Failures for artifacts that are missing or whose payload_sha256 lacks the expected
    prefix; never raises."""
    out = []
    for aid, prefix in expected.items():
        try:
            meta = store.meta(aid)
        except StageFailure as exc:
            out.append(f"{aid}: missing ({exc.code.value})")
            continue
        except Exception as exc:  # noqa: BLE001 - never raise; any backend error is a failure
            out.append(f"{aid}: unreadable ({type(exc).__name__})")
            continue
        if not str(meta.payload_sha256).startswith(prefix):
            out.append(f"{aid}: payload_sha256 {meta.payload_sha256[:16]} != {prefix}")
    return out
