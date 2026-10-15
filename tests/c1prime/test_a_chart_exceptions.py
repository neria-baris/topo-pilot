"""Independent tests, author A (job 0026): the chart-specific exception mapping at the C1 gate
boundary (TEST_PLAN A-2; protocol section 14 'Failure classification' and section 16
conventions; API.md section 2 adapt_chart_exception / smoothing_diagnostics / run_c1_gate).

Every exception is raised by the frozen kernels themselves (cochain.integer_lift,
cochain.smooth_phase, cochain.check_closure, chart.extend, ...), so the originating frame is the
real one. smooth_phase is driven off its convergent path by replacing its module-level `lsqr`
name for one call (monkeypatch); the frozen file is not edited.
"""

from __future__ import annotations

import math
import sys
import traceback
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
import chart  # noqa: E402
import cochain  # noqa: E402
import errors  # noqa: E402
import stage_records  # noqa: E402

PATH3 = np.array([[0, 1], [1, 2]], dtype=np.int64)  # path 0-1-2, no triangle
BETA3 = np.array([1.0, 0.0])


def caught(fn):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001  the test inspects whatever the kernel raised
        return exc
    raise AssertionError("expected an exception")


def full(status, reason):
    status = str(status)
    if "/" in status or not reason:
        return status
    token = str(reason).split(":")[0].strip()
    return f"{status}/{token}" if token == "CHART_UNAVAILABLE" else status


def gate_outcome(tmp_path, fn, chart_boundary=True):
    with pytest.raises(c1_records.C1Stop) as info:
        c1_records.run_c1_gate(tmp_path, "C0-cal", fn, chart=chart_boundary)
    record = stage_records.gates_so_far(tmp_path)[-1]
    return info.value, record


def not_a_cocycle():
    """Triangle (0,1,2) with a = (1, 0, 0) on edges (01, 02, 12): D1 a = 1, not 0 mod 47."""
    edges = np.array([[0, 1], [0, 2], [1, 2]], dtype=np.int64)
    D1, tri = cochain.triangle_system(edges, 3)
    a = np.array([1, 0, 0], dtype=np.int64)
    return cochain.integer_lift(a, D1, edges, tri, 3, c1_config.chart_cfg())


def fake_lsqr(values):
    def lsqr(*args, **kwargs):
        return (np.asarray(values, dtype=np.float64),)
    return lsqr


def smoothing(monkeypatch, values, edges=PATH3, beta=BETA3):
    monkeypatch.setattr(cochain, "lsqr", fake_lsqr(values))
    n = int(edges.max()) + 1
    return lambda: cochain.smooth_phase(beta, edges, n)


def test_filtration_boundary_cocycle_error_is_chart_unavailable(tmp_path):
    exc = caught(not_a_cocycle)
    assert isinstance(exc, errors.Invalid) and str(exc) == "not a cocycle mod p"
    adapted = c1_records.adapt_chart_exception(exc)
    assert adapted is not None
    assert full(*adapted) == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert "float32/float64 filtration boundary" in str(adapted[1])
    stop, record = gate_outcome(tmp_path, not_a_cocycle)
    assert stop.status == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert "float32/float64 filtration boundary" in str(stop.reason)
    assert isinstance(stop.__cause__, errors.Invalid)
    assert full(record["status"], record.get("reason")) == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert record["exception"] == "Invalid" and record["operation"] == "integer_lift"


def test_cocycle_error_outside_the_chart_boundary_stays_technical(tmp_path):
    stop, record = gate_outcome(tmp_path, not_a_cocycle, chart_boundary=False)
    assert stop.status == "FAIL_TECHNICAL" and record["status"] == "FAIL_TECHNICAL"


def test_same_message_not_raised_by_integer_lift_is_technical(tmp_path):
    def impostor():
        raise errors.Invalid("not a cocycle mod p")

    assert c1_records.adapt_chart_exception(caught(impostor)) is None
    stop, _ = gate_outcome(tmp_path, impostor)
    assert stop.status == "FAIL_TECHNICAL"


def test_finite_smoothing_residual_above_tolerance_is_chart_unavailable(tmp_path, monkeypatch):
    fn = smoothing(monkeypatch, [0.3, 0.3])  # f = (0, 0.3, 0.3): residual 1.3 / 2 = 0.65
    exc = caught(fn)
    assert isinstance(exc, errors.Invalid) and str(exc).startswith("smoothing residual")
    residual = float(str(exc).split()[-1])
    assert math.isfinite(residual) and residual > 1e-8
    diag = c1_records.smoothing_diagnostics(exc)
    assert diag == {"f_finite": True, "residual": residual}
    status, reason = c1_records.adapt_chart_exception(exc)
    assert full(status, reason) == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert str(exc) in str(reason)  # original message preserved
    stop, record = gate_outcome(tmp_path, fn)
    assert stop.status == "INCONCLUSIVE/CHART_UNAVAILABLE" and str(exc) in str(stop.reason)
    assert record["operation"] == "smooth_phase" and record["exception"] == "Invalid"


def test_non_finite_f_is_technical(tmp_path, monkeypatch):
    fn = smoothing(monkeypatch, [float("nan"), 0.0])
    exc = caught(fn)
    assert isinstance(exc, errors.Invalid)
    assert bool(c1_records.smoothing_diagnostics(exc)["f_finite"]) is False
    assert c1_records.adapt_chart_exception(exc)[0] == "FAIL_TECHNICAL"
    stop, record = gate_outcome(tmp_path, fn)
    assert stop.status == "FAIL_TECHNICAL" and record["status"] == "FAIL_TECHNICAL"


def test_finite_f_with_infinite_residual_is_technical(tmp_path, monkeypatch):
    # f = (0, 1e308, -1e308): B f overflows on edge (1, 2), so the residual is +inf.
    fn = smoothing(monkeypatch, [1e308, -1e308])
    exc = caught(fn)
    diag = c1_records.smoothing_diagnostics(exc)
    assert bool(diag["f_finite"]) is True and diag["residual"] == float("inf")
    assert c1_records.adapt_chart_exception(exc)[0] == "FAIL_TECHNICAL"
    assert gate_outcome(tmp_path, fn)[0].status == "FAIL_TECHNICAL"


def test_finite_f_with_nan_residual_is_technical(tmp_path, monkeypatch):
    """A NaN normaliser makes the residual NaN while f stays finite."""
    monkeypatch.setattr(cochain, "lsqr", fake_lsqr([0.3, 0.3]))
    original = np.linalg.norm

    def fn():
        np.linalg.norm = lambda *args, **kwargs: float("nan")
        try:
            return cochain.smooth_phase(BETA3, PATH3, 3)
        finally:
            np.linalg.norm = original

    exc = caught(fn)
    diag = c1_records.smoothing_diagnostics(exc)
    assert bool(diag["f_finite"]) is True and math.isnan(diag["residual"])
    assert c1_records.adapt_chart_exception(exc)[0] == "FAIL_TECHNICAL"
    assert gate_outcome(tmp_path, fn)[0].status == "FAIL_TECHNICAL"


def test_unavailable_smoothing_diagnostics_are_technical(monkeypatch):
    exc = caught(smoothing(monkeypatch, [0.3, 0.3]))
    traceback.clear_frames(exc.__traceback__)  # the frame locals are gone
    assert c1_records.smoothing_diagnostics(exc) is None
    status, reason = c1_records.adapt_chart_exception(exc)
    assert status == "FAIL_TECHNICAL"
    assert "smoothing diagnostics unavailable" in str(reason)


def test_smoothing_style_invalid_without_a_smooth_phase_frame_is_technical(tmp_path):
    def fake():
        raise errors.Invalid("smoothing residual 0.5")

    exc = caught(fake)
    assert c1_records.smoothing_diagnostics(exc) is None
    assert gate_outcome(tmp_path, fake)[0].status == "FAIL_TECHNICAL"


def test_integer_certificate_defect_is_technical(tmp_path):
    edges = np.array([[0, 1], [0, 2], [1, 2]], dtype=np.int64)
    tri = np.array([[0, 1, 2]], dtype=np.int64)

    def closure():
        cochain.check_closure(np.array([1, 0, 0]), edges, tri)

    def congruence():
        cochain.check_congruence(np.array([1, 2, 3]), np.array([1, 2, 4]), 47)

    for fn in (closure, congruence):
        assert c1_records.adapt_chart_exception(caught(fn)) is None
        assert gate_outcome(tmp_path, fn)[0].status == "FAIL_TECHNICAL"


def test_conflicting_duplicate_landmarks_in_extension_are_technical(tmp_path):
    zero = np.zeros(0, dtype=np.int64)
    pts = np.array([[0.0, 0.0]] * 2 + [[np.cos(a), np.sin(a)] for a in np.arange(1, 9)])
    phi = np.array([0.0, np.pi] + [0.1 * k for k in range(8)])
    ch = chart.Chart(np.array([f"{k:020d}" for k in range(10)]), pts, phi, 0.5, 5.0,
                     np.ones(10), np.zeros((0, 2), dtype=np.int64), zero, zero, zero, zero,
                     np.zeros(10, dtype=np.int64), 1, {})
    gauge = chart.Gauge(sign=1, shift=0.0, alignment=1.0)

    def fn():
        return chart.extend(ch, gauge, np.array([[0.0, 0.0]]), c1_config.chart_cfg())

    assert "conflicting" in str(caught(fn))
    assert gate_outcome(tmp_path, fn)[0].status == "FAIL_TECHNICAL"


def test_lineage_join_error_is_technical(tmp_path):
    def fn():
        raise errors.JoinError("sequence ids differ across models")

    assert c1_records.adapt_chart_exception(caught(fn)) is None
    stop, record = gate_outcome(tmp_path, fn)
    assert stop.status == "FAIL_TECHNICAL" and record["exception"] == "JoinError"


def test_unresolved_chart_kernel_is_chart_unavailable(tmp_path):
    """Unresolved from a frozen chart kernel (protocol section 14: INCONCLUSIVE/
    CHART_UNAVAILABLE); here primitive_class on a disconnected two-component graph."""
    edges = np.array([[0, 1], [2, 3]], dtype=np.int64)
    tri = np.zeros((0, 3), dtype=np.int64)

    def fn():
        return cochain.primitive_class(np.array([1, 1]), edges, tri, 4, 47)

    assert isinstance(caught(fn), errors.Unresolved)
    stop, record = gate_outcome(tmp_path, fn)
    assert stop.status == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert full(record["status"], record.get("reason")) == "INCONCLUSIVE/CHART_UNAVAILABLE"
