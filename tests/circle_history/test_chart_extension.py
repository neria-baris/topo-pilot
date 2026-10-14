"""Independent synthetic tests, author A (spec v2.3): chart.extend, agreement, bins,
resultant and chart_gates (TEST_PLAN A11, A12, A15).

Written from tools/x4_circle_history/API.md, CONTRACT.json and TEST_PLAN.md only. Extension
values are recomputed here from the written formula (v2.2: w_j = exp(l_j - max l), no floor).
The extension landmarks are an INTEGER square ring, so every distance is sqrt of an exact integer
and every tie is exact regardless of how distances are computed.
"""

from __future__ import annotations

import dataclasses
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import chart  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

TWO_PI = 2.0 * math.pi
CHART_KEYS = (
    "field", "lift_bounds", "lift_node_limit", "lift_cpu_cap_s", "lift_rounding_tol",
    "local_passes", "local_vertices", "extension_k", "support_min_resultant",
    "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows", "overall_resultant_max",
    "smoothing_residual_max",
)
ARRAY_FIELDS = ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "integer_lift",
                "lift_correction", "primitive", "tree_potential")


def make_cfg(**overrides):
    chart_cfg = json.loads((PKG / "CONTRACT.json").read_text(encoding="utf-8"))["chart"]
    cfg = {key: chart_cfg[key] for key in CHART_KEYS}
    cfg["lift_bounds"] = list(cfg["lift_bounds"])
    cfg.update(overrides)
    return cfg


def make_ids(n):
    return np.array([f"h{k:04d}" for k in range(n)])


def circle_points(theta):
    r = 1.0 + 0.02 * np.cos(7 * theta + 0.4)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta),
                            0.03 * np.sin(3 * theta + 1.1), 0.02 * np.cos(5 * theta + 2.3)])


def square_ring(side=6):
    """Boundary of [0,6]^2, counter-clockwise from (0,0): k0..5 bottom, k6..11 right
    (6,0..5), k12..17 top (6..1,6), k18..23 left (0,6..1)."""
    pts = ([(x, 0) for x in range(side)] + [(side, y) for y in range(side)]
           + [(side - x, side) for x in range(side)] + [(0, side - y) for y in range(side)])
    return np.array([(x, y, 0) for x, y in pts], dtype=np.float64)


RING_X = square_ring()
PHI24 = TWO_PI * np.arange(24) / 24
Q_BELOW = np.array([3.0, -1.0, 0.0])
Q_CENTRE = np.array([3.0, 3.0, 0.0])
GAUGE0 = chart.Gauge(sign=1, shift=0.0, alignment=1.0)  # phi_g == phi for phi in [0, 2pi)


@pytest.fixture(scope="module")
def ring_chart():
    return chart.fit_chart(RING_X.copy(), make_ids(24), make_cfg())


def custom(base, **changes):
    return dataclasses.replace(base, **changes)


def circ_gap(a, b):
    return abs(float(np.angle(np.exp(1j * (a - b)))))


def ref_row(landmarks, phi_g, sigma, q, nearest=None):
    """Written formula: stable 8-NN, log-shifted Gaussian weights, exact-duplicate rule."""
    d = np.sqrt(np.sum((landmarks - q) ** 2, axis=1))
    order = np.argsort(d, kind="stable")
    zero = np.flatnonzero(d == 0.0)
    if zero.size:
        z = np.mean(np.exp(1j * phi_g[zero]))
    else:
        pick = order[:8] if nearest is None else np.asarray(nearest)
        ell = -0.5 * (d[pick] / sigma) ** 2
        w = np.exp(ell - ell.max())
        z = np.sum(w * np.exp(1j * phi_g[pick])) / np.sum(w)
    return float(np.mod(np.angle(z), TWO_PI)), float(abs(z)), float(d[order[7]])


# ---------------------------------------------------------------------------------------- A11
def test_extend_formula_and_stable_ties(ring_chart):
    c = custom(ring_chart, phi=PHI24.copy(), sigma=3.0, support_radius=10.0)
    Q = np.vstack([Q_BELOW, Q_CENTRE, [2.5, 4.0, 0.0]])
    sq_below = np.sum((RING_X - Q_BELOW) ** 2, axis=1)
    # d^2: k3=1; k2,k4=2; k1,k5=5; k0,k6=10; k7,k23=13 -> k7 (lower index) is the 8th.
    assert np.argsort(sq_below, kind="stable")[:8].tolist() == [3, 2, 4, 1, 5, 0, 6, 7]
    assert sq_below[7] == sq_below[23] == 13.0
    sq_centre = np.sum((RING_X - Q_CENTRE) ** 2, axis=1)
    # d^2 = 9 for k3, k9, k15, k21; eight points tie at 10, the four lowest indices are taken.
    assert np.argsort(sq_centre, kind="stable")[:8].tolist() == [3, 9, 15, 21, 2, 4, 8, 10]
    ext = chart.extend(c, GAUGE0, Q, make_cfg())
    for r, q in enumerate(Q):
        phase, res, e8 = ref_row(RING_X, PHI24, 3.0, q)
        assert circ_gap(ext.phase[r], phase) < 1e-12
        assert 0.0 <= ext.phase[r] < TWO_PI
        assert ext.resultant[r] == pytest.approx(res, abs=1e-12)
        assert ext.eighth_distance[r] == pytest.approx(e8, rel=1e-15)
        assert bool(ext.supported[r]) == (res >= 0.2 and e8 <= 10.0)
        assert not bool(ext.duplicate[r])
    # the opposite tie-break would be clearly visible
    alt_below = ref_row(RING_X, PHI24, 3.0, Q_BELOW, nearest=[3, 2, 4, 1, 5, 0, 6, 23])
    assert circ_gap(alt_below[0], ext.phase[0]) > 1e-3
    alt_centre = ref_row(RING_X, PHI24, 3.0, Q_CENTRE, nearest=[3, 9, 15, 21, 14, 16, 20, 22])
    assert circ_gap(alt_centre[0], ext.phase[1]) > 1e-3


def test_extend_eighth_distance_boundary(ring_chart):
    radius = math.sqrt(13.0)
    for support_radius, expected in ((radius, True), (float(np.nextafter(radius, 0.0)), False)):
        c = custom(ring_chart, phi=PHI24.copy(), sigma=3.0, support_radius=support_radius)
        ext = chart.extend(c, GAUGE0, Q_BELOW[None, :], make_cfg())
        assert ext.eighth_distance[0] == radius
        assert ext.resultant[0] >= 0.2
        assert bool(ext.supported[0]) is expected


def split_phases(at_zero):
    """Phases for the 8 nearest of Q_BELOW (k3,k2,k4,k1,k5,k0,k6,k7): `at_zero` of them 0."""
    phi = np.full(24, 1.0)
    nearest = [3, 2, 4, 1, 5, 0, 6, 7]
    phi[nearest[:at_zero]] = 0.0
    phi[nearest[at_zero:]] = math.pi
    return phi


def test_extend_resultant_boundary(ring_chart):
    # sigma = 1e10 makes every shifted log-weight round to exp(~-1e-19) == 1.0, so z is the plain
    # mean: 5 at 0 and 3 at pi gives |z| = |(5 - 3) + ~4e-16 i| / 8 = 0.25.
    c = custom(ring_chart, phi=split_phases(5), sigma=1e10, support_radius=10.0)
    ext = chart.extend(c, GAUGE0, Q_BELOW[None, :], make_cfg())
    r = float(ext.resultant[0])
    assert r == pytest.approx(0.25, abs=1e-15)
    assert bool(ext.supported[0])  # 0.25 >= 0.2
    # |z| = 0.2 cannot be produced exactly in floating point by 8 unit vectors, so the >= rule
    # is checked at the threshold read from cfg["support_min_resultant"] (assumed honoured).
    at_r = chart.extend(c, GAUGE0, Q_BELOW[None, :], make_cfg(support_min_resultant=r))
    assert bool(at_r.supported[0])
    above = make_cfg(support_min_resultant=float(np.nextafter(r, 1.0)))
    assert not bool(chart.extend(c, GAUGE0, Q_BELOW[None, :], above).supported[0])
    even = custom(ring_chart, phi=split_phases(4), sigma=1e10, support_radius=10.0)
    ext_even = chart.extend(even, GAUGE0, Q_BELOW[None, :], make_cfg())
    assert ext_even.resultant[0] < 1e-15 and not bool(ext_even.supported[0])


def test_extend_exact_duplicates_average_all(ring_chart):
    landmarks = RING_X.copy()
    landmarks[1] = landmarks[0]
    landmarks[12] = landmarks[0]  # three landmarks at (0,0,0), non-adjacent indices
    phi = PHI24.copy()
    phi[0], phi[1], phi[12] = 1.0, 1.0 + 2e-5, 1.0 + 1e-5
    c = custom(ring_chart, landmarks=landmarks, phi=phi, sigma=3.0, support_radius=10.0)
    Q = np.vstack([landmarks[0], Q_BELOW])
    ext = chart.extend(c, GAUGE0, Q, make_cfg())
    assert ext.duplicate.tolist() == [True, False]
    # mean of the three = e^{i(1+1e-5)} (1 + 2cos 1e-5)/3: first-match-only would give 1.0
    assert circ_gap(ext.phase[0], 1.0 + 1e-5) < 1e-12
    assert ext.resultant[0] == pytest.approx((1 + 2 * math.cos(1e-5)) / 3, abs=1e-14)
    for r, q in enumerate(Q):
        phase, res, e8 = ref_row(landmarks, phi, 3.0, q)
        assert circ_gap(ext.phase[r], phase) < 1e-12
        assert ext.resultant[r] == pytest.approx(res, abs=1e-12)
        assert ext.eighth_distance[r] == pytest.approx(e8, rel=1e-15)
    assert bool(ext.supported[0])
    clash = phi.copy()
    clash[12] = 1.0 + math.pi / 2  # conflicting copies: |z| ~ 0.745, 1 - |z| > 1e-8
    conflicted = custom(c, phi=clash)
    with pytest.raises(errors.Invalid):
        chart.extend(conflicted, GAUGE0, landmarks[:1], make_cfg())


def test_extend_never_mutates(ring_chart):
    c = custom(ring_chart, phi=PHI24.copy(), sigma=3.0, support_radius=10.0)
    gauge = chart.Gauge(sign=-1, shift=0.3, alignment=0.9)
    before = {name: np.array(getattr(c, name), copy=True) for name in ARRAY_FIELDS}
    Q = np.vstack([Q_BELOW, Q_CENTRE, RING_X[5]])
    q_before = Q.copy()
    chart.extend(c, gauge, Q, make_cfg())
    for name in ARRAY_FIELDS:
        assert np.array_equal(np.asarray(getattr(c, name)), before[name]), name
    assert (c.sigma, c.support_radius) == (3.0, 10.0)
    assert (gauge.sign, gauge.shift, gauge.alignment) == (-1, 0.3, 0.9)
    assert np.array_equal(Q, q_before)


def explicit_agreement(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return max(abs(np.mean(np.exp(1j * (a - s * b)))) for s in (1, -1))


def test_extend_held_out_circle_agrees_with_direct():
    theta = TWO_PI * np.arange(96) / 96
    lm_theta, out_theta = theta[0::2], theta[1::2]
    cfg = make_cfg()
    landmark_chart = chart.fit_chart(circle_points(lm_theta), make_ids(48), cfg)
    direct = chart.fit_chart(circle_points(out_theta), make_ids(48), cfg)
    gauge = chart.fit_gauge(landmark_chart, np.column_stack([np.cos(lm_theta),
                                                             np.sin(lm_theta)]))
    ext = chart.extend(landmark_chart, gauge, circle_points(out_theta), cfg)
    assert np.all(ext.supported) and not np.any(ext.duplicate)
    value = explicit_agreement(ext.phase, direct.phi)
    assert value >= 0.99
    assert chart.agreement(ext.phase, direct.phi) == pytest.approx(value, abs=1e-12)
    assert abs(np.mean(np.exp(1j * (ext.phase - out_theta)))) >= 0.99  # gauge aligned to theta


# ---------------------------------------------------------------------------------------- A15
def test_far_query_keeps_exact_normalised_weights(ring_chart):
    c = custom(ring_chart, phi=PHI24.copy(), sigma=3.0, support_radius=10.0)
    q = np.array([3.0, -1000.0, 0.0])
    d = np.sqrt(np.sum((RING_X - q) ** 2, axis=1))
    assert np.all(np.exp(-0.5 * (d / 3.0) ** 2) == 0.0)  # raw weights all underflow
    nearest = np.argsort(d, kind="stable")[:8]
    assert nearest.tolist() == [3, 2, 4, 1, 5, 0, 6, 7]  # k7 ties k23 at d^2 = 1002010
    ell = -0.5 * (d[nearest] / 3.0) ** 2
    log_norm = ell.max() + math.log(float(np.sum(np.exp(ell - ell.max()))))  # log-sum-exp
    z = complex(np.sum(np.exp(ell - log_norm) * np.exp(1j * PHI24[nearest])))
    ext = chart.extend(c, GAUGE0, q[None, :], make_cfg())
    assert np.isfinite(ext.phase[0]) and np.isfinite(ext.resultant[0])
    assert circ_gap(ext.phase[0], math.atan2(z.imag, z.real)) < 1e-9
    assert ext.resultant[0] == pytest.approx(abs(z), abs=1e-9)
    assert abs(z) > 0.5  # a floor-based formula would report |z| = 0 here
    assert ext.eighth_distance[0] == pytest.approx(math.sqrt(1002010.0), rel=1e-15)
    assert not bool(ext.supported[0])  # unsupported by the radius rule only


def test_far_query_with_fitted_scale_unsupported(ring_chart):
    ext = chart.extend(ring_chart, GAUGE0, np.array([[1000.0, 1000.0, 0.0]]), make_cfg())
    assert ext.eighth_distance[0] > ring_chart.support_radius
    assert np.isfinite(ext.phase[0]) and np.isfinite(ext.resultant[0])
    assert not bool(ext.supported[0])


@pytest.mark.parametrize("field", ["phi", "sigma"])
def test_extend_nonfinite_z_invalid(ring_chart, field):
    phi = PHI24.copy()
    sigma = 3.0
    if field == "phi":
        phi[3] = np.nan  # k3 is the nearest landmark of Q_BELOW
    else:
        sigma = math.nan
    c = custom(ring_chart, phi=phi, sigma=sigma, support_radius=10.0)
    with pytest.raises(errors.Invalid):
        chart.extend(c, GAUGE0, Q_BELOW[None, :], make_cfg())


# ---------------------------------------------------------------------------------------- A12
def test_agreement_known_answers():
    quarter = np.array([0.0, math.pi / 2, math.pi, 1.5 * math.pi])
    assert chart.agreement(quarter, np.zeros(4)) == pytest.approx(0.0, abs=1e-12)
    # s=+1: |(1 + e^{-i pi/2})/2| = sqrt(2)/2; s=-1 gives the same modulus
    assert chart.agreement(np.zeros(2), np.array([0.0, math.pi / 2])) == pytest.approx(
        math.sqrt(0.5), abs=1e-12)
    a = np.mod(np.arange(10) * 0.7, TWO_PI)
    assert chart.agreement(a, np.mod(-a + 0.3, TWO_PI)) == pytest.approx(1.0, abs=1e-12)
    assert chart.agreement(a, np.mod(a + 2.0, TWO_PI)) == pytest.approx(1.0, abs=1e-12)
    b = np.mod(np.arange(10) ** 2 * 0.37, TWO_PI)
    assert chart.agreement(a, b) == pytest.approx(explicit_agreement(a, b), abs=1e-12)


def centres(bins=12):
    return (np.arange(bins) + 0.5) * TWO_PI / bins


def test_phase_bin_counts_known_answers():
    wanted = [3, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 4]
    phi = np.concatenate([np.repeat(centres(), wanted), [0.0, TWO_PI]])
    counts = np.asarray(chart.phase_bin_counts(phi))
    # 0.0 -> bin 0; 2pi -> floor(12) = 12 clipped to bin 11
    assert counts.dtype == np.int64
    assert counts.tolist() == [4, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 5]
    four = np.asarray(chart.phase_bin_counts(np.repeat(centres(4), [1, 2, 0, 3]), bins=4))
    assert four.tolist() == [1, 2, 0, 3]


def test_overall_resultant_known_answers():
    assert chart.overall_resultant(np.array([0.0, math.pi])) == pytest.approx(0.0, abs=1e-15)
    assert chart.overall_resultant(np.array([0.0, 0.0, math.pi / 2])) == pytest.approx(
        math.sqrt(5.0) / 3.0, abs=1e-15)
    assert chart.overall_resultant(np.array([1.234])) == pytest.approx(1.0, abs=1e-15)


def make_ext(phase, supported=None):
    phase = np.asarray(phase, dtype=np.float64)
    n = phase.size
    supported = np.ones(n, dtype=bool) if supported is None else np.asarray(supported, bool)
    return chart.Extension(phase=phase, resultant=np.ones(n), eighth_distance=np.zeros(n),
                           supported=supported, duplicate=np.zeros(n, dtype=bool))


def overall(result):
    value = result["overall"]
    return value["status"] if isinstance(value, dict) else value


def gates(phase, direct=None, supported=None):
    phase = np.asarray(phase, dtype=np.float64)
    direct = phase.copy() if direct is None else np.asarray(direct, dtype=np.float64)
    result = chart.chart_gates(make_ext(phase, supported), direct, make_cfg())
    for name in ("support", "fidelity", "bins", "resultant"):
        rec = result[name]
        assert rec["status"] in ("PASS", "INCONCLUSIVE")
        assert bool(rec["criterion_met"]) == (rec["status"] == "PASS")
        assert "value" in rec and "threshold" in rec
    return result


EVEN = np.repeat(centres(), 8)  # 8 per bin, resultant ~ 0


def test_chart_gates_all_pass_with_exactly_eight_per_bin():
    result = gates(EVEN)
    assert [result[k]["status"] for k in ("support", "fidelity", "bins", "resultant")] == [
        "PASS"] * 4
    assert overall(result) == "PASS"
    assert result["fidelity"]["threshold"] == 0.8 and result["bins"]["threshold"] == 8
    assert result["resultant"]["threshold"] == 0.3
    assert result["fidelity"]["value"] == pytest.approx(1.0, abs=1e-12)


def test_chart_gates_seven_in_a_bin_is_inconclusive():
    result = gates(EVEN[1:])  # bin 0 now has 7
    assert result["bins"]["status"] == "INCONCLUSIVE" and not result["bins"]["criterion_met"]
    assert result["resultant"]["status"] == "PASS"  # 1/95
    assert overall(result) == "INCONCLUSIVE"


def test_chart_gates_fidelity_boundary():
    at = [0.0] * 9 + [math.pi]  # agreement with zeros: (9 - 1)/10 = 0.8 exactly
    rec = gates(at, direct=np.zeros(10))["fidelity"]
    assert rec["status"] == "PASS" and bool(rec["criterion_met"]) and rec["value"] == 0.8
    below = [1e-4] + [0.0] * 8 + [math.pi]
    expected = explicit_agreement(below, np.zeros(10))
    assert expected < 0.8
    res = gates(below, direct=np.zeros(10))
    assert res["fidelity"]["status"] == "INCONCLUSIVE"
    assert not bool(res["fidelity"]["criterion_met"])
    assert res["fidelity"]["value"] == pytest.approx(expected, abs=1e-15)
    assert overall(res) == "INCONCLUSIVE"


def test_chart_gates_resultant_boundary():
    rec = gates([0.0] * 13 + [math.pi] * 7)["resultant"]  # (13 - 7)/20 = 0.3 exactly
    assert rec["status"] == "PASS" and rec["value"] == 0.3
    over = gates([0.0] * 7 + [math.pi] * 3)["resultant"]  # 0.4
    assert over["status"] == "INCONCLUSIVE" and not bool(over["criterion_met"])
    assert over["value"] == pytest.approx(0.4, abs=1e-15)


def test_chart_gates_support_and_overall_order():
    flags = np.ones(96, dtype=bool)
    flags[17] = False
    result = gates(EVEN, supported=flags)
    assert result["support"]["status"] == "INCONCLUSIVE"
    # every later record is still computed with its value preserved
    assert [result[k]["status"] for k in ("fidelity", "bins", "resultant")] == ["PASS"] * 3
    assert overall(result) == "INCONCLUSIVE"
    # with only two possible statuses the order is visible only as "first non-PASS exists"
    both = gates(EVEN[1:], direct=np.zeros(95), supported=flags[1:])
    assert overall(both) == "INCONCLUSIVE"


def test_chart_gates_defects_invalid():
    bad = EVEN.copy()
    bad[5] = np.nan
    with pytest.raises(errors.Invalid):
        chart.chart_gates(make_ext(bad), EVEN.copy(), make_cfg())
    with pytest.raises(errors.Invalid):
        chart.chart_gates(make_ext(EVEN), EVEN[:-1].copy(), make_cfg())
