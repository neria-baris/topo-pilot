"""X5 G1 study exports under the full study controls (x5g1-train-v4 §8, §11; API v4 §4).

Every JSON/npz write, the manifest and the completion record are bracketed by
``StudyControls.boundary`` (all STOP sources, live holds, budget, resources). A stop writes only a
small status record. Later stages advance only on a COMPLETE status with matching hashes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from .x5g1_controls import BudgetExceeded, StopRequested
from .x5g1t_runtime import ResourceExceeded, StudyControls

STATUS, MANIFEST = "EXPORT_STATUS.json", "MANIFEST.json"
_STOPS = {StopRequested: "STOPPED_DURING_EXPORT", BudgetExceeded: "BUDGET_DURING_EXPORT",
          ResourceExceeded: "RESOURCE_DURING_EXPORT"}


class ExportIncomplete(RuntimeError):
    """A prerequisite export is missing, stopped, tampered or has unexpected files."""


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    return obj


def study_export(sc: StudyControls, out: Path, files: dict, arrays: dict | None = None,
                 reserve: float = 0.0) -> None:
    """Guarded JSON files, npz arrays, manifest and COMPLETE status (in that order)."""
    out = Path(out)
    done: list[str] = []

    def write_json(name: str, obj) -> None:
        (out / name).write_text(json.dumps(_jsonable(obj), indent=1, default=str),
                                encoding="utf-8")

    def write_npz(name: str, arrs: dict) -> None:
        with open(out / name, "wb") as fh:
            np.savez(fh, **arrs)

    def manifest() -> None:
        write_json(MANIFEST, {n: _sha(out / n) for n in done})

    steps = [(n, (lambda n=n, o=o: write_json(n, o))) for n, o in files.items()]
    steps += [(n, (lambda n=n, a=a: write_npz(n, a))) for n, a in (arrays or {}).items()]
    steps.append((MANIFEST, manifest))
    steps.append((STATUS, lambda: write_json(STATUS, {"status": "COMPLETE",
                                                      "completed_steps": list(done)})))
    try:
        for name, fn in steps:
            sc.boundary(f"export {name}", 1.0, reserve)
            fn()
            if name not in (MANIFEST, STATUS):
                done.append(name)
            sc.boundary(f"export {name} done", 1.0, reserve)
    except tuple(_STOPS) as exc:
        status = next(v for k, v in _STOPS.items() if isinstance(exc, k))
        (out / STATUS).write_text(json.dumps(
            {"status": status, "completed_steps": done,
             "cause": f"{type(exc).__name__}: {exc}"}, indent=1), encoding="utf-8")
        raise


def verify_export_complete(out: Path) -> dict:
    """Manifest of a COMPLETE export whose files match exactly; else ``ExportIncomplete``."""
    out = Path(out)
    try:
        status = json.loads((out / STATUS).read_text(encoding="utf-8"))
        manifest = json.loads((out / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ExportIncomplete(f"{out}: status/manifest unreadable: {exc}") from exc
    if not isinstance(status, dict) or status.get("status") != "COMPLETE":
        raise ExportIncomplete(f"{out}: export status {status!r} is not COMPLETE")
    if not isinstance(manifest, dict) or not manifest:
        raise ExportIncomplete(f"{out}: empty or invalid manifest")
    present = {p.name for p in out.iterdir()}
    expected = set(manifest) | {MANIFEST, STATUS}
    if present != expected:
        raise ExportIncomplete(f"{out}: files {sorted(present ^ expected)} differ from manifest")
    bad = [n for n, h in manifest.items() if _sha(out / n) != h]
    if bad:
        raise ExportIncomplete(f"{out}: manifest hash mismatch {bad}")
    return manifest
