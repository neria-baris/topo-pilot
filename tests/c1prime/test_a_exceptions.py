"""Independent tests, author A (job 0026): the exception mapping of protocol section 16
conventions (v4 review fix 5) and the generic C1 gate boundary run_c1_gate (TEST_PLAN A-6, third
bullet; API.md section 2 classify_exception, C1GateFailure, CertificateFlag, C1Stop).

One fixture per exception class and per exceptional StageFailure code. Reference-input and
Decimal exceptions are raised by the unchanged independent_reference / decimal code itself.
API.md writes some statuses as full strings ("FAIL_TECHNICAL/ORACLE") and records split them into
status prefix and reason suffix (section 0); `full` below accepts either form.
"""

from __future__ import annotations

import decimal
import re
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_config  # noqa: E402
import c1_records  # noqa: E402
import error_bound  # noqa: E402
import errors  # noqa: E402
import independent_reference  # noqa: E402
import oracle_profile  # noqa: E402
import stage_records  # noqa: E402
from topo_pilot.contracts import ErrorCode, StageFailure  # noqa: E402

KINDS = {"IDENTITY", "LINEAGE", "ORACLE", "NUMERICAL", "MODEL"}
REASONS = {"CHART_UNAVAILABLE", "ELIGIBILITY", "HEADROOM", "NUMERICAL", "PATCH_MODEL_DEGENERATE",
           "SUPPORT_DEGENERATE", "RBF_DEGENERATE", "FAMILY_UNMATCHED", "NUISANCE_CONFOUNDED",
           "SUPPORT", "DECODER_INADEQUATE", "CHART_NOT_REGISTERING", "MANIPULATION_FAILED",
           "MODEL_HEADROOM", "UNDERPOWERED", "TEST_GATE", "REGISTRY_INCOMPLETE", "RESOURCE"}


def full(status, reason):
    status = str(status)
    if "/" in status:
        return status
    match = re.match(r"[A-Z_]+", str(reason or ""))
    token = match.group(0) if match else ""
    if (status == "FAIL_TECHNICAL" and token in KINDS) or (
            status == "INCONCLUSIVE" and token in REASONS):
        return f"{status}/{token}"
    return status


def caught(fn):
    try:
        fn()
    except BaseException as exc:  # noqa: BLE001
        return exc
    raise AssertionError("expected an exception")


def failure(code, detail="detail text"):
    return StageFailure(code, "c1.test", "check_name", detail)


def gate_failed_with_status(status):
    exc = failure(ErrorCode.GATE_FAILED, "declared criterion unmet")
    object.__setattr__(exc, "c1_status", status)  # StageFailure is frozen; set it directly
    return exc


def reference_value_error():
    T, E, pi = np.full((2, 2), 0.5), np.full((2, 3), 1 / 3), np.full(2, 0.5)
    return caught(lambda: independent_reference.decimal_suffix_posterior(T, E, pi, [0], 30))


def decimal_underflow():
    def fn():
        with decimal.localcontext(error_bound.trapping_context(40)):
            return Decimal("1E-999999") / Decimal(10)
    return caught(fn)


def decimal_invalid_operation():
    def fn():
        with decimal.localcontext(error_bound.trapping_context(40)):
            return Decimal(-1).ln()
    return caught(fn)


CASES = [
    ("Invalid", lambda: errors.Invalid("integrity defect"), "FAIL_TECHNICAL"),
    ("JoinError", lambda: errors.JoinError("pairing mismatch"), "FAIL_TECHNICAL"),
    ("Unresolved", lambda: errors.Unresolved("criterion not met"), "INCONCLUSIVE"),
    ("ProfileError", lambda: oracle_profile.ProfileError("bad process"), "FAIL_TECHNICAL/ORACLE"),
    ("reference ValueError", reference_value_error, "FAIL_TECHNICAL/ORACLE"),
    ("Decimal underflow", decimal_underflow, "FAIL_TECHNICAL/NUMERICAL"),
    ("Decimal invalid op", decimal_invalid_operation, "FAIL_TECHNICAL/NUMERICAL"),
    ("bare DecimalException", lambda: decimal.DivisionByZero("x"), "FAIL_TECHNICAL/NUMERICAL"),
    ("CertificateFlag", lambda: c1_records.CertificateFlag("Subnormal"),
     "FAIL_TECHNICAL/NUMERICAL"),
    ("PH_RESOURCE_LIMIT", lambda: failure(ErrorCode.PH_RESOURCE_LIMIT), "INCONCLUSIVE/RESOURCE"),
    ("GATE_FAILED declared", lambda: gate_failed_with_status("INCONCLUSIVE/SUPPORT"),
     "INCONCLUSIVE/SUPPORT"),
    ("GATE_FAILED declared 2", lambda: gate_failed_with_status("INCONCLUSIVE/UNDERPOWERED"),
     "INCONCLUSIVE/UNDERPOWERED"),
    ("GATE_FAILED undeclared", lambda: failure(ErrorCode.GATE_FAILED), "FAIL_TECHNICAL"),
    ("other StageFailure", lambda: failure(ErrorCode.IMPOSSIBLE_HISTORY), "FAIL_TECHNICAL"),
    ("NUMERICAL_FAILURE code", lambda: failure(ErrorCode.NUMERICAL_FAILURE), "FAIL_TECHNICAL"),
    ("C1GateFailure", lambda: c1_records.C1GateFailure("INCONCLUSIVE/FAMILY_UNMATCHED", "m2"),
     "INCONCLUSIVE/FAMILY_UNMATCHED"),
    ("C1GateFailure technical", lambda: c1_records.C1GateFailure("FAIL_TECHNICAL/MODEL", "m0"),
     "FAIL_TECHNICAL/MODEL"),
    ("anything else", lambda: RuntimeError("surprise"), "FAIL_TECHNICAL"),
    ("plain ValueError", lambda: ValueError("not from the reference"), "FAIL_TECHNICAL"),
]


def test_fixtures_raise_what_they_claim():
    assert isinstance(reference_value_error(), ValueError)
    assert isinstance(decimal_underflow(), decimal.DecimalException)
    assert isinstance(decimal_invalid_operation(), decimal.InvalidOperation)


@pytest.mark.parametrize("name, make, expected", CASES, ids=[c[0] for c in CASES])
def test_classify_exception(name, make, expected):
    status, reason = c1_records.classify_exception(make())
    assert full(status, reason) == expected


@pytest.mark.parametrize("code", [ErrorCode.IMPOSSIBLE_HISTORY, ErrorCode.ALIGNMENT_ERROR,
                                  ErrorCode.CHECKSUM_MISMATCH])
def test_other_stage_failures_keep_code_and_message(code):
    exc = failure(code, "the original detail")
    status, reason = c1_records.classify_exception(exc)
    assert full(status, reason) == "FAIL_TECHNICAL"
    assert str(reason).startswith(code.value) and "the original detail" in str(reason)


@pytest.mark.parametrize("name, make, expected", CASES, ids=[c[0] for c in CASES])
def test_run_c1_gate_records_and_stops(tmp_path, name, make, expected):
    exc = make()

    def offending_operation():
        raise exc

    with pytest.raises(c1_records.C1Stop) as stop:
        c1_records.run_c1_gate(tmp_path, "H3", offending_operation)
    assert stop.value.gate == "H3" and stop.value.__cause__ is exc
    assert full(stop.value.status, stop.value.reason) == expected
    records = stage_records.gates_so_far(tmp_path)
    assert len(records) == 1
    rec = records[0]
    assert rec["gate"] == "H3" and rec["criterion_met"] is False
    assert full(rec["status"], rec.get("reason")) == expected
    assert rec["exception"] == type(exc).__name__
    assert rec["operation"] in ("offending_operation", innermost_name(exc))


def innermost_name(exc):
    tb = exc.__traceback__
    if tb is None:
        return None
    while tb.tb_next is not None:
        tb = tb.tb_next
    return tb.tb_frame.f_code.co_name


def test_operation_is_the_originating_function(tmp_path):
    def inner_kernel():
        raise oracle_profile.ProfileError("bad")

    def wrapper():
        inner_kernel()

    with pytest.raises(c1_records.C1Stop):
        c1_records.run_c1_gate(tmp_path, "H1", wrapper)
    assert stage_records.gates_so_far(tmp_path)[-1]["operation"] == "inner_kernel"


def test_returned_pass_dict_is_recorded_and_returned(tmp_path):
    result = {"status": "PASS", "value": 3}
    assert c1_records.run_c1_gate(tmp_path, "H4", lambda: result) is result
    rec = stage_records.gates_so_far(tmp_path)[-1]
    assert rec["gate"] == "H4" and rec["status"] == "PASS" and rec["criterion_met"] is True


@pytest.mark.parametrize("status", ["INCONCLUSIVE/ELIGIBILITY", "FAIL_TECHNICAL/LINEAGE"])
def test_returned_non_pass_dict_stops_the_cohort(tmp_path, status):
    with pytest.raises(c1_records.C1Stop) as stop:
        c1_records.run_c1_gate(tmp_path, "H2", lambda: {"status": status})
    assert stop.value.status == status and stop.value.gate == "H2"
    rec = stage_records.gates_so_far(tmp_path)[-1]
    prefix, suffix = status.split("/")
    assert rec["status"] == prefix and suffix in str(rec.get("reason"))


def test_status_of_splits_full_strings():
    assert c1_config.status_of("INCONCLUSIVE/SUPPORT") == ("INCONCLUSIVE", "SUPPORT")
    assert c1_config.status_of("FAIL_TECHNICAL/ORACLE") == ("FAIL_TECHNICAL", "ORACLE")
    assert c1_config.status_of("PASS") == ("PASS", None)


def test_c1stop_carries_gate_status_reason():
    stop = c1_records.C1Stop("V3", "INCONCLUSIVE/MODEL_HEADROOM", "lower bound <= -g")
    assert (stop.gate, stop.status, stop.reason) == ("V3", "INCONCLUSIVE/MODEL_HEADROOM",
                                                     "lower bound <= -g")
    failure_ = c1_records.C1GateFailure("INCONCLUSIVE/SUPPORT", "F(T) too large")
    assert (failure_.status, failure_.reason) == ("INCONCLUSIVE/SUPPORT", "F(T) too large")
