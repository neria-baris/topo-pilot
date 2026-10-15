"""C1' stage records, gate boundary and exception mapping (API.md §2; protocol §16 conventions,
§18 field 2). Reuses K4 stage_records unchanged with the C1 PREREQUISITE rebinding and the C1
PASS-gate-set checks; classifies every exception before recording (run_gate is not relied on)."""

from __future__ import annotations

import decimal
import math

import c1_config  # noqa: F401  (sys.path)
import numpy as np
import stage_records
from errors import Invalid, JoinError, Unresolved
from oracle_profile import ProfileError

from topo_pilot.contracts import StageFailure

PREREQUISITE = {"oracle": None, "calibration": "oracle", "validation": "calibration",
                "fresh": "validation"}
GATE_ORDER = (
    ("0", "pre-data", "G0"), ("1", "S3", "H1"), ("2", "S3", "H2"), ("3", "S3", "H3"),
    ("4", "S3", "H4"), ("4a", "S3", "N0"), ("5", "S3", "H5"), ("6", "S4", "M0"),
    ("7", "S4", "C0-cal"), ("8", "S4", "F1"), ("9", "S4", "M1"), ("10", "S4", "M2-cal"),
    ("11", "S4", "M3-cal"), ("12", "S5", "C0-val"), ("13", "S5", "M4"), ("14", "S5", "M2-val"),
    ("15", "S5", "M3-val"), ("16", "S5", "V1"), ("17", "S5", "V2"), ("18", "S5", "V3"),
    ("19", "S5", "P1"), ("—", "S6", "ACCEPT"), ("20", "S7", "T-PRE"), ("21", "S7", "NUM"),
    ("22", "S7", "ENDPOINT"))
STAGE_GATES = {"oracle": ["G0", "H1", "H2", "H3", "H4", "N0", "H5"],
               "calibration": ["M0", "C0-cal", "F1", "M1", "M2-cal", "M3-cal"],
               "validation": ["C0-val", "M4", "M2-val", "M3-val", "V1", "V2", "V3", "P1"],
               "fresh": ["T-PRE", "NUM", "ENDPOINT"]}
REQUIRED_PASS = {k: list(v) for k, v in STAGE_GATES.items() if k != "fresh"}
COCYCLE_MESSAGE = "not a cocycle mod p"


class C1GateFailure(Exception):
    """A declared unmet criterion or defect raised by a C1 kernel (.status is the full status)."""

    def __init__(self, status: str, reason: str = ""):
        super().__init__(f"{status}: {reason}")
        self.status, self.reason = status, reason


class CertificateFlag(Exception):
    """A watched Decimal flag in a certificate computation (P3)."""


class C1Stop(Exception):
    """The first non-PASS gate stops the cohort."""

    def __init__(self, gate: str, status: str, reason: str = ""):
        super().__init__(f"{gate}: {status} {reason}")
        self.gate, self.status, self.reason = gate, status, reason


def bind_stage_records():
    stage_records.PREREQUISITE = dict(PREREQUISITE)
    return stage_records


def check_pass_set(out, stage) -> None:
    prior = PREREQUISITE[stage]
    gates = stage_records.gates_so_far(out)
    bad = [g for g in gates if g["status"] != "PASS"]
    if bad:
        stage_records.refuse(out, stage, f"cohort ended at gate {bad[0]['gate']}")
    passed = {g["gate"] for g in gates if g["status"] == "PASS"}
    missing = [g for g in REQUIRED_PASS[prior] if g not in passed]
    if missing:
        stage_records.refuse(out, stage, f"prerequisite PASS gates missing: {missing}")


def begin_stage(out, stage, models) -> None:
    bind_stage_records()
    if PREREQUISITE[stage] is not None:
        check_pass_set(out, stage)
    stage_records.begin(out, stage, models)


def _code(exc) -> str:
    code = getattr(exc, "code", None)
    return getattr(code, "value", str(code))


def classify_exception(exc) -> tuple:
    """The §16 exception mapping (review fix 5) -> (status, reason)."""
    if isinstance(exc, C1GateFailure):
        return exc.status, exc.reason
    if isinstance(exc, (Invalid, JoinError)):
        return "FAIL_TECHNICAL", f"{type(exc).__name__}: {exc}"
    if isinstance(exc, Unresolved):
        return "INCONCLUSIVE", str(exc)
    if isinstance(exc, ProfileError):
        return "FAIL_TECHNICAL/ORACLE", f"ProfileError: {exc}"
    if isinstance(exc, ValueError) and _raised_in(exc, "independent_reference"):
        return "FAIL_TECHNICAL/ORACLE", f"reference input: {exc}"
    if isinstance(exc, (decimal.DecimalException, CertificateFlag)):
        return "FAIL_TECHNICAL/NUMERICAL", f"{type(exc).__name__}: {exc}"
    if isinstance(exc, StageFailure):
        code = _code(exc)
        if code == "PH_RESOURCE_LIMIT":
            return "INCONCLUSIVE/RESOURCE", str(exc)
        if code == "GATE_FAILED":
            declared = getattr(exc, "c1_status", None) or getattr(exc, "check", "")
            if str(declared).startswith("INCONCLUSIVE/"):
                return str(declared), str(exc)
        return "FAIL_TECHNICAL", f"{code}: {exc}"
    return "FAIL_TECHNICAL", f"{type(exc).__name__}: {exc}"


def _frames(exc):
    tb = getattr(exc, "__traceback__", None)
    while tb is not None:
        yield tb.tb_frame
        tb = tb.tb_next


def _raised_in(exc, module_name: str) -> bool:
    return any(f.f_globals.get("__name__") == module_name for f in _frames(exc))


def _frame_of(exc, func: str):
    found = None
    for f in _frames(exc):
        if f.f_code.co_name == func and f.f_globals.get("__name__") == "cochain":
            found = f
    return found


def smoothing_diagnostics(exc):
    """f and residual from the failed smooth_phase frame (never rerun); None if unavailable."""
    frame = _frame_of(exc, "smooth_phase")
    if frame is None or "f" not in frame.f_locals or "residual" not in frame.f_locals:
        return None
    try:
        f = np.asarray(frame.f_locals["f"], dtype=np.float64)
        residual = float(frame.f_locals["residual"])
    except (TypeError, ValueError):
        return None
    return {"f_finite": bool(np.isfinite(f).all()), "residual": residual}


def adapt_chart_exception(exc):
    """The two chart-specific Invalid cases of §14 / rulings 1, 2, 6; else None."""
    if not isinstance(exc, Invalid) or isinstance(exc, JoinError):
        return None
    if str(exc) == COCYCLE_MESSAGE and _frame_of(exc, "integer_lift") is not None:
        return "INCONCLUSIVE", "CHART_UNAVAILABLE: float32/float64 filtration boundary"
    if _frame_of(exc, "smooth_phase") is not None:
        diag = smoothing_diagnostics(exc)
        if diag is None:
            return "FAIL_TECHNICAL", "smoothing diagnostics unavailable"
        if not diag["f_finite"] or not math.isfinite(diag["residual"]):
            return "FAIL_TECHNICAL", f"non-finite smoothing: {exc}"
        if diag["residual"] > 1e-8:
            return "INCONCLUSIVE", f"CHART_UNAVAILABLE: {exc}"
        return "FAIL_TECHNICAL", f"undiagnosed smoothing Invalid: {exc}"
    return None


def _operation(exc) -> str:
    last = None
    for f in _frames(exc):
        last = f.f_code.co_name
    return last or "?"


def _record(out, gate, full, reason, **extra) -> None:
    status, suffix = c1_config.status_of(full)
    text = suffix if not reason else (f"{suffix}: {reason}" if suffix else reason)
    stage_records.record_gate(out, gate, status, reason=text, full_status=full, **extra)


def run_c1_gate(out, gate, fn, chart=False):
    """Run fn(); classify and record any failure, then raise C1Stop; record a returned status."""
    try:
        result = fn()
    except C1Stop:
        raise
    except Exception as exc:  # noqa: BLE001  every failure receives a gate record (§16)
        adapted = adapt_chart_exception(exc) if chart else None
        status, reason = adapted if adapted is not None else classify_exception(exc)
        if status == "INCONCLUSIVE" and chart:
            status, reason = "INCONCLUSIVE/CHART_UNAVAILABLE", reason
        _record(out, gate, status, reason, exception=type(exc).__name__,
                operation=_operation(exc))
        raise C1Stop(gate, status, reason) from exc
    if isinstance(result, dict) and "status" in result:
        full = result["status"]
        details = {k: v for k, v in result.items() if k not in ("status", "reason")}
        _record(out, gate, full, result.get("reason", ""), values=_jsonable(details))
        if full != "PASS":
            raise C1Stop(gate, full, result.get("reason", ""))
    return result


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist() if x.size <= 64 else f"<array {x.shape}>"
    return x


class LogitPolicy:
    """The computation-order rule (§2.2) as a gate-indexed permission (API.md §2)."""

    ALLOWED = {"identity_check": {"M0", "P1", "T-PRE"},
               "donor": {"V3", "P1", "T-PRE", "NUM", "ENDPOINT"},
               "endpoint": {"P1", "NUM", "ENDPOINT"}}
    ORDER = [g for _, _, g in GATE_ORDER]

    def __init__(self, done=()):
        self.current, self.done = None, list(done)

    def begin(self, gate: str) -> None:
        expected = self.ORDER[len(self.done)] if len(self.done) < len(self.ORDER) else None
        if expected == "ACCEPT" and gate == "T-PRE":  # ACCEPT is a coordinator record (S6)
            self.done.append("ACCEPT")
            expected = "T-PRE"
        if gate != expected or self.current is not None:
            raise C1GateFailure("FAIL_TECHNICAL", f"gate {gate} out of order (expected "
                                f"{expected})")
        self.current = gate

    def passed(self, gate: str) -> None:
        if gate != self.current:
            raise C1GateFailure("FAIL_TECHNICAL", f"gate {gate} is not the current gate")
        self.done.append(gate)
        self.current = None

    def require(self, kind: str) -> None:
        gate = self.current
        ok = gate in self.ALLOWED.get(kind, set())
        if ok and kind == "endpoint" and gate in ("NUM", "ENDPOINT"):
            ok = "T-PRE" in self.done
        if not ok:
            raise C1GateFailure("FAIL_TECHNICAL", f"{kind} logits not allowed at gate {gate}")
