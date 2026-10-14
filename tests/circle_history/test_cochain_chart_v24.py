"""Independent synthetic tests, author A (spec v2.4): integer_lift entry/exit timer and the
fit_chart / extend timed hook (TEST_PLAN A16, A17; API.md "Spec v2.4 clarifications" 5 and 6).

Written from tools/x4_circle_history/API.md, CONTRACT.json and TEST_PLAN.md only. Clocks are
injected value sequences; nothing waits in real time.

Reading-count technique (A16): a successful call is run once with an all-zero counting clock to
learn its number R of clock readings (deterministic for fixed inputs). By item 5 the first reading
is the entry reading and the LAST reading of every successful return is the cap check after the
final exact checks, so a second run whose clock is 0.0 for readings 1..R-1 and past the cap at
reading R exceeds the cap ONLY at that final check.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import chart  # noqa: E402
import cochain  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

P = 47
TWO_PI = 2.0 * math.pi
CHART_KEYS = (
    "field", "lift_bounds", "lift_node_limit", "lift_cpu_cap_s", "lift_rounding_tol",
    "local_passes", "local_vertices", "extension_k", "support_min_resultant",
    "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows", "overall_resultant_max",
    "smoothing_residual_max",
)
FIT_LABELS = ["distance", "ph", "edges", "two_skeleton", "integer_lift", "primitive",
              "smoothing"]
ARRAY_FIELDS = ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "integer_lift",
                "lift_correction", "primitive", "tree_potential")
INFO_KEYS = ("birth", "death", "radius", "bar_index", "n_edges", "n_triangles",
             "smoothing_residual")


def make_cfg(**overrides):
    chart_cfg = json.loads((PKG / "CONTRACT.json").read_text(encoding="utf-8"))["chart"]
    cfg = {key: chart_cfg[key] for key in CHART_KEYS}
    cfg["lift_bounds"] = list(cfg["lift_bounds"])
    cfg.update(overrides)
    return cfg


def as_int(values):
    return np.asarray(values, dtype=np.int64)


def edge_index(edges):
    return {(int(i), int(j)): e for e, (i, j) in enumerate(np.asarray(edges).tolist())}


def triangle_sums(c, edges, triangles):
    idx = edge_index(edges)
    vals = [int(v) for v in np.asarray(c).tolist()]
    tris = np.asarray(triangles, dtype=np.int64).reshape(-1, 3).tolist()
    return [vals[idx[(j, k)]] - vals[idx[(i, k)]] + vals[idx[(i, j)]] for i, j, k in tris]


def reference_d1(edges, triangles):
    idx = edge_index(edges)
    tris = np.asarray(triangles, dtype=np.int64).reshape(-1, 3).tolist()
    rows, cols, vals = [], [], []
    for t, (i, j, k) in enumerate(tris):
        for pair, sign in (((j, k), 1), ((i, k), -1), ((i, j), 1)):
            rows.append(t)
            cols.append(idx[pair])
            vals.append(sign)
    return scipy.sparse.csr_matrix((as_int(vals), (as_int(rows), as_int(cols))),
                                   shape=(len(tris), len(idx)), dtype=np.int64)


class SeqClock:
    """Returns `values` in order, then `tail` forever; counts readings."""

    def __init__(self, values=(), tail=0.0):
        self._it = itertools.chain(values, itertools.repeat(tail))
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return float(next(self._it))


class Marker(Exception):
    pass


K4_EDGES = as_int([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
K4_TRIS = as_int([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
D1_K4 = reference_d1(K4_EDGES, K4_TRIS)
EXACT_K4 = [3, -5, 7, -8, 4, 12]      # delta(0, 3, -5, 7): zero defect
A_K4 = [50, 42, -40, 39, 51, 59]      # 47*(1,1,-1,1,1,1) + EXACT_K4: defect 47*(1,3,3,1)


def lift(a, clock, guard=None, cfg=None):
    return cochain.integer_lift(as_int(a), D1_K4, K4_EDGES, K4_TRIS, 4,
                                make_cfg() if cfg is None else cfg, guard=guard, clock=clock)


def test_fixture_defects():
    assert triangle_sums(EXACT_K4, K4_EDGES, K4_TRIS) == [0, 0, 0, 0]
    assert triangle_sums(A_K4, K4_EDGES, K4_TRIS) == [47, 141, 141, 47]


# ---------------------------------------------------------------------------------------- A16
@pytest.mark.parametrize("late", [31.0, 30.0])  # 30.0: elapsed == cap fails (>=)
def test_a16_closed_branch_past_cap_at_return_is_unresolved(late):
    clock = SeqClock([0.0], tail=late)  # entry reads 0, every later reading is past the cap
    with pytest.raises(errors.Unresolved):
        lift(EXACT_K4, clock)
    assert clock.calls >= 2  # entry + the cap check before returning


def test_a16_closed_branch_below_cap_returns_exact_lift():
    clock = SeqClock([0.0], tail=29.5)
    alpha, info = lift(EXACT_K4, clock)
    assert np.asarray(alpha).tolist() == EXACT_K4
    assert triangle_sums(alpha, K4_EDGES, K4_TRIS) == [0, 0, 0, 0]
    assert info["kind"] == "centered_exact"
    assert clock.calls >= 2


def test_a16_closed_branch_cap_only_at_final_check():
    counter = SeqClock()
    lift(EXACT_K4, counter)
    readings = counter.calls
    assert readings >= 2
    with pytest.raises(errors.Unresolved):
        lift(EXACT_K4, SeqClock([0.0] * (readings - 1), tail=1000.0))


@pytest.mark.parametrize("overrides", [{}, {"local_passes": 0}])
def test_a16_corrected_branch_cap_only_at_final_check(overrides):
    cfg = make_cfg(**overrides)
    counter = SeqClock()
    alpha, info = lift(A_K4, counter, cfg=cfg)
    assert info["kind"] == "corrected_exact"
    assert triangle_sums(alpha, K4_EDGES, K4_TRIS) == [0, 0, 0, 0]
    assert all((x - y) % P == 0 for x, y in zip(A_K4, np.asarray(alpha).tolist()))
    readings = counter.calls
    assert readings >= 4  # entry, check (a), check (b), final check at least
    late = SeqClock([0.0] * (readings - 1), tail=1000.0)
    with pytest.raises(errors.Unresolved):
        lift(A_K4, late, cfg=cfg)
    assert late.calls == readings  # the run got all the way to the final check
    # control: the same clock one reading later never passes the cap
    again, _ = lift(A_K4, SeqClock([0.0] * readings, tail=1000.0), cfg=cfg)
    assert np.asarray(again).tolist() == np.asarray(alpha).tolist()


def test_a16_first_clock_call_precedes_defect():
    def clock():
        raise Marker()

    calls = []
    malformed = [1, 2, 3, 4, 5]  # length 5 against a [4, 6] D1: D1 @ a would fail
    with pytest.raises(Marker):
        lift(malformed, clock, guard=lambda: calls.append(1))
    with pytest.raises(Marker):  # also on a valid input: nothing runs before the clock
        lift(A_K4, clock, guard=lambda: calls.append(1))
    assert calls == []


# ---------------------------------------------------------------------------------------- A17
THETA = TWO_PI * np.arange(48) / 48


def circle_points(theta):
    r = 1.0 + 0.02 * np.cos(7 * theta + 0.4)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta),
                            0.03 * np.sin(3 * theta + 1.1), 0.02 * np.cos(5 * theta + 2.3)])


def make_ids(n):
    return np.array([f"h{k:04d}" for k in range(n)])


class RecordingTimed:
    def __init__(self, raise_at=None, error=None):
        self.labels, self.raise_at, self.error = [], raise_at, error

    def __call__(self, label, fn):
        self.labels.append(label)
        assert callable(fn)
        if label == self.raise_at:
            raise self.error
        return fn()  # zero-argument callable; result returned unchanged


@pytest.fixture(scope="module")
def plain_chart():
    return chart.fit_chart(circle_points(THETA), make_ids(48), make_cfg())


def test_a17_fit_chart_labels_in_order_and_same_chart(plain_chart):
    timed = RecordingTimed()
    timed_chart = chart.fit_chart(circle_points(THETA), make_ids(48), make_cfg(), timed=timed)
    assert timed.labels == FIT_LABELS
    for name in ARRAY_FIELDS:
        got = np.asarray(getattr(timed_chart, name))
        want = np.asarray(getattr(plain_chart, name))
        assert got.dtype == want.dtype and np.array_equal(got, want), name
    assert timed_chart.sigma == plain_chart.sigma
    assert timed_chart.support_radius == plain_chart.support_radius
    assert int(timed_chart.period_gcd) == int(plain_chart.period_gcd)
    for key in INFO_KEYS:
        assert timed_chart.info[key] == plain_chart.info[key], key


def test_a17_timed_exception_propagates_and_stops():
    error = errors.Unresolved("operation exhausted (test marker)")
    timed = RecordingTimed(raise_at="two_skeleton", error=error)
    with pytest.raises(errors.Unresolved) as excinfo:
        chart.fit_chart(circle_points(THETA), make_ids(48), make_cfg(), timed=timed)
    assert excinfo.value is error  # propagated unchanged
    assert timed.labels == FIT_LABELS[:4]  # no later label is called


def test_a17_extend_wraps_extension_distance(plain_chart):
    gauge = chart.Gauge(sign=1, shift=0.0, alignment=1.0)
    queries = circle_points(THETA + 0.05)
    timed = RecordingTimed()
    with_timed = chart.extend(plain_chart, gauge, queries, make_cfg(), timed=timed)
    plain = chart.extend(plain_chart, gauge, queries, make_cfg())
    # Literal reading: ONE wrapped distance computation per extend call.
    assert timed.labels == ["extension_distance"]
    for name in ("phase", "resultant", "eighth_distance", "supported", "duplicate"):
        assert np.array_equal(getattr(with_timed, name), getattr(plain, name)), name
