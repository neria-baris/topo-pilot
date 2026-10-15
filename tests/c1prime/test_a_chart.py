"""Independent tests, author A (job 0026): the C1' chart wrapper (TEST_PLAN A-1 items 1-4 and 9).

Protocol section 14, steps 1-10. Expected values come from the frozen K4 kernels (chart.py,
cochain.py) called directly, from ripser and scipy, or are hand-derived; c1_chart never checks
itself. Synthetic fixtures built here:
- a thin rectangular loop (one dominant H1 bar, birth ~1.2, death ~8.1, so the midpoint graph is
  sparse: about three neighbours per side, no edge across the width 8);
- isolated satellites 7 away from the loop, i.e. singleton components at the midpoint (~4.6);
- a straight chain plus a far ring centred on the chain axis: the selected class lives on the
  ring, so it is trivial on the chain (C*).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import ripser
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_chart  # noqa: E402
import c1_config  # noqa: E402
import c1_records  # noqa: E402
import chart  # noqa: E402
import cochain  # noqa: E402
import errors  # noqa: E402
import stage_records  # noqa: E402

FIELD = 47
ARRAYS = ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "integer_lift",
          "lift_correction", "primitive", "tree_potential")
ADDED_INFO = ("n", "m", "l_max", "n_components", "component_sizes", "excluded_ids", "lift_kind",
              "cstar")


def make_ids(n, base=10**9):
    """20-digit zero-padded sequence-id strings (protocol section 14, correction C-15)."""
    return np.array([f"{base + 3 * k:020d}" for k in range(n)])


def loop_points(m, width=8.0):
    """m points on the perimeter (length m) of a (m/2 - width) x width rectangle, jittered."""
    k = np.arange(m, dtype=np.float64)
    t = k + 0.15 * np.sin(1.3 * k)  # arclength; steps in [0.82, 1.18]
    length = m / 2.0 - width
    xy = np.empty((m, 2))
    for i, s in enumerate(t):
        if s < length:
            xy[i] = (s, 0.0)
        elif s < length + width:
            xy[i] = (length, s - length)
        elif s < 2 * length + width:
            xy[i] = (2 * length + width - s, width)
        else:
            xy[i] = (0.0, 2 * length + 2 * width - s)
    return np.column_stack([xy, 0.05 * np.sin(2.1 * k)]), t


def with_satellites(m_loop, n_sat, n=512):
    """Loop plus n_sat isolated satellites at interleaved landmark positions 7, 27, 47, ..."""
    assert m_loop + n_sat == n
    loop, t = loop_points(m_loop)
    sat = np.column_stack([10.0 + 8.0 * np.arange(n_sat), np.full(n_sat, -7.0),
                           np.zeros(n_sat)])
    sat_idx = 7 + 20 * np.arange(n_sat)
    loop_idx = np.setdiff1d(np.arange(n), sat_idx)
    X = np.empty((n, 3))
    X[loop_idx], X[sat_idx] = loop, sat
    return X, loop_idx, sat_idx, t


def chain_and_ring():
    """492-point straight chain (spacing 0.9) and a 20-point unit ring 1000 beyond its end, in
    the plane normal to the chain axis: every ring point is equidistant from each chain point."""
    chain_x = 0.9 * np.arange(492)
    chain_pts = np.column_stack([chain_x, np.zeros(492), np.zeros(492)])
    ang = 2.0 * np.pi * np.arange(20) / 20
    ring = np.column_stack([np.full(20, chain_x[-1] + 1000.0), np.cos(ang), np.sin(ang)])
    return np.vstack([chain_pts, ring]), np.arange(492), np.arange(492, 512)


def my_components(E, n):
    A = coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n))
    return connected_components(A, directed=False)


def reference_geometry(X):
    """Section 14 steps 1-4 with the frozen kernels, computed independently of c1_chart."""
    D = chart.cdist(X, X)
    res = ripser.ripser(D, maxdim=1, coeff=FIELD, distance_matrix=True, do_cocycles=True)
    dgm1 = res["dgms"][1]
    k = chart.select_h1_bar(dgm1)
    b, d = float(dgm1[k, 0]), float(dgm1[k, 1])
    r = (b + d) / 2.0
    E = cochain.edge_list(D, r)
    a = chart.cocycle_to_edges(res["cocycles"][1][k], E, FIELD)
    h0 = res["dgms"][0][:, 1]
    count, labels = my_components(E, X.shape[0])
    return dict(D=D, k=int(k), b=b, d=d, r=r, E=E, a=a, l_max=float(h0[np.isfinite(h0)].max()),
                count=int(count), labels=labels)


class Recorder:
    """persist(name, dict) callable that keeps every record in call order."""

    def __init__(self):
        self.items = []

    def __call__(self, name, record):
        self.items.append((name, dict(record)))

    @property
    def names(self):
        return [name for name, _ in self.items]


def pick(record, *names):
    """API.md names the giant-record fields but not their keys; accept protocol or info names."""
    for name in names:
        if name in record:
            return record[name]
    raise AssertionError(f"giant record lacks every one of {names}: {sorted(record)}")


def check_giant_record(rec, ref, ids, excluded_idx, m, passed):
    assert pick(rec, "b", "birth") == ref["b"]
    assert pick(rec, "d", "death") == ref["d"]
    assert pick(rec, "r", "radius") == ref["r"]
    assert int(pick(rec, "k", "bar_index")) == ref["k"]
    assert pick(rec, "l_max", "ell_max", "lmax") == ref["l_max"]
    assert int(pick(rec, "n_components", "component_count")) == ref["count"]
    sizes = sorted(np.bincount(ref["labels"]).tolist(), reverse=True)
    assert [int(s) for s in pick(rec, "component_sizes", "sizes")] == sizes
    excluded = [str(x) for x in pick(rec, "excluded_ids", "excluded_landmark_ids", "excluded")]
    assert excluded == [str(x) for x in ids[excluded_idx]]
    assert int(pick(rec, "m")) == m and int(pick(rec, "n")) == 512
    assert bool(pick(rec, "giant_pass", "pass", "passed", "giant")) is passed


def full_status(status, reason):
    """Join a record's status prefix and reason suffix (API.md section 0)."""
    status = str(status)
    if "/" in status or not reason:
        return status
    token = str(reason).split(":")[0].strip()
    return f"{status}/{token}" if token == "CHART_UNAVAILABLE" else status


def innermost(exc):
    tb = exc.__traceback__
    while tb.tb_next is not None:
        tb = tb.tb_next
    return tb.tb_frame.f_code.co_name


def test_landmark_ids_are_20_digit_zero_padded_strings():
    got = c1_chart.landmark_ids(np.array([0, 7, 123456789012], dtype=np.int64))
    assert [str(x) for x in got] == ["0" * 20, "0" * 19 + "7", "00000000123456789012"]


def test_connected_graph_equals_fit_chart_bitwise():
    """Item 1: m = n, so steps 1-9 are fit_chart's operations; only info gains keys."""
    X, _ = loop_points(40)
    ids = make_ids(40)
    cfg = c1_config.chart_cfg()
    ref = chart.fit_chart(X.copy(), ids, cfg)
    got = c1_chart.fit_chart_lcc(X.copy(), ids, cfg)
    assert isinstance(got, chart.Chart)
    for name in ARRAYS:
        a, b = np.asarray(getattr(ref, name)), np.asarray(getattr(got, name))
        assert (a.dtype, a.shape) == (b.dtype, b.shape), name
        assert a.tobytes() == b.tobytes(), name
    for name in ("sigma", "support_radius", "period_gcd"):
        assert type(getattr(ref, name)) is type(getattr(got, name)), name
        assert getattr(ref, name) == getattr(got, name), name
    for key, value in ref.info.items():
        assert got.info[key] == value, key
    assert set(ADDED_INFO) <= set(got.info) - set(ref.info)
    assert got.info["n"] == got.info["m"] == 40 and got.info["n_components"] == 1
    assert list(got.info["excluded_ids"]) == []
    assert np.array_equal(np.asarray(got.info["cstar"]), np.arange(40))
    assert got.info["lift_kind"] == ref.info["lift"]["kind"]


def test_components_partition_and_sizes():
    edges = np.array([[0, 1], [1, 2], [3, 4], [4, 5], [6, 7]], dtype=np.int64)
    labels, sizes = c1_chart.components(edges, 10)
    labels, sizes = np.asarray(labels), np.asarray(sizes)
    groups = [{0, 1, 2}, {3, 4, 5}, {6, 7}, {8}, {9}]
    assert len(sizes) == 5 and labels.shape == (10,)
    for g in groups:
        assert len({int(labels[i]) for i in g}) == 1
        assert all(int(sizes[labels[i]]) == len(g) for i in g)
    assert len({int(labels[min(g)]) for g in groups}) == 5
    lone, lone_sizes = c1_chart.components(np.zeros((0, 2), dtype=np.int64), 4)
    assert len(set(np.asarray(lone).tolist())) == 4 and np.asarray(lone_sizes).tolist() == [1] * 4


@pytest.mark.parametrize(
    "labels, sizes, expected",
    [
        ([0, 1, 1, 1, 2], [1, 3, 1], [1, 2, 3]),  # unique largest
        ([0, 0, 0, 1, 1, 1, 2], [3, 3, 1], [0, 1, 2]),  # tie, first label holds index 0
        ([1, 1, 1, 0, 0, 0, 2], [3, 3, 1], [0, 1, 2]),  # tie, smallest index has label 1
        ([2, 0, 0, 1, 1, 2, 1, 0], [3, 3, 2], [1, 2, 7]),  # tie between labels 0 and 1
    ],
)
def test_giant_largest_component_ties_to_smallest_index(labels, sizes, expected):
    cstar, m = c1_chart.giant(np.array(labels, dtype=np.int64), np.array(sizes, dtype=np.int64))
    assert np.asarray(cstar).tolist() == expected and int(m) == len(expected)


def test_restrict_reindexes_ascending_and_keeps_matching_cocycle_entries():
    edges = np.array([[0, 1], [0, 3], [1, 3], [2, 4], [3, 5]], dtype=np.int64)
    cocycle = np.array([7, -3, 5, 11, 2], dtype=np.int64)
    edges_c, a_c = c1_chart.restrict(edges, cocycle, np.array([0, 1, 3, 5]), 6)
    edges_c, a_c = np.asarray(edges_c), np.asarray(a_c)
    # 0->0, 1->1, 3->2, 5->3; edge (2, 4) leaves C*
    assert edges_c.tolist() == [[0, 1], [0, 2], [1, 2], [2, 3]]
    assert a_c.tolist() == [7, -3, 5, 2]
    assert edges_c.dtype == np.int64
    assert edges_c.tolist() == sorted(edges_c.tolist())


@pytest.mark.parametrize("m, n, ok", [(487, 512, True), (486, 512, False), (512, 512, True),
                                      (95, 100, True), (94, 100, False), (19, 20, True)])
def test_giant_pass_integer_rule(m, n, ok):
    assert bool(c1_chart.giant_pass(m, n)) is ok
    if n == 512:
        assert bool(c1_chart.giant_pass(m)) is ok


def test_giant_486_of_512_stops_after_the_pre_raise_record(tmp_path):
    """Item 3 (fail side): GIANT_BELOW_0.95, with the step-5 record persisted first."""
    X, loop_idx, sat_idx, _ = with_satellites(486, 26)
    ids, cfg, rec = make_ids(512), c1_config.chart_cfg(), Recorder()
    with pytest.raises(c1_records.C1Stop) as caught:
        c1_records.run_c1_gate(
            tmp_path, "C0-cal", lambda: c1_chart.fit_chart_lcc(X, ids, cfg, persist=rec),
            chart=True,
        )
    stop = caught.value
    assert stop.gate == "C0-cal" and stop.status == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert "GIANT_BELOW_0.95" in str(stop.reason)
    cause = stop.__cause__
    assert isinstance(cause, c1_records.C1GateFailure)
    assert cause.status == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert "GIANT_BELOW_0.95" in str(cause.reason)
    ref = reference_geometry(X)
    assert ref["count"] == 27 and np.array_equal(np.flatnonzero(
        ref["labels"] == ref["labels"][loop_idx[0]]), loop_idx)  # fixture as designed
    assert rec.names == ["giant"]
    check_giant_record(rec.items[0][1], ref, ids, sat_idx, m=486, passed=False)
    gate = stage_records.gates_so_far(tmp_path)[-1]
    assert gate["gate"] == "C0-cal"
    assert full_status(gate["status"], gate.get("reason")) == "INCONCLUSIVE/CHART_UNAVAILABLE"


def test_trivial_restricted_class_stops_unresolved_after_lift_record(tmp_path):
    """Items 4 and 9: g = 0 on C* -> primitive_class raises Unresolved, which the chart gate
    records as INCONCLUSIVE/CHART_UNAVAILABLE (protocol section 14 'Failure classification');
    the giant and lift records written before it are preserved, and no later record exists."""
    X, chain_idx, ring_idx = chain_and_ring()
    ids, cfg, rec = make_ids(512), c1_config.chart_cfg(), Recorder()
    ref = reference_geometry(X)
    assert ref["count"] == 2  # fixture: chain and ring are the two components at r
    with pytest.raises(c1_records.C1Stop) as caught:
        c1_records.run_c1_gate(
            tmp_path, "C0-cal", lambda: c1_chart.fit_chart_lcc(X, ids, cfg, persist=rec),
            chart=True,
        )
    stop = caught.value
    assert stop.status == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert isinstance(stop.__cause__, errors.Unresolved)
    assert innermost(stop.__cause__) == "primitive_class"
    assert rec.names == ["giant", "lift"]
    check_giant_record(rec.items[0][1], ref, ids, ring_idx, m=492, passed=True)
    assert rec.items[1][1]["kind"] == "centered_exact"  # the cocycle vanishes on chain edges
    gate = stage_records.gates_so_far(tmp_path)[-1]
    assert full_status(gate["status"], gate.get("reason")) == "INCONCLUSIVE/CHART_UNAVAILABLE"


def test_invalid_landmark_ids_are_a_technical_failure(tmp_path):
    """Input defects keep FAIL_TECHNICAL even at the chart boundary."""
    X, _ = loop_points(40)
    ids = make_ids(40)[::-1]  # descending: chart._check_landmarks raises Invalid
    cfg = c1_config.chart_cfg()
    with pytest.raises(c1_records.C1Stop) as caught:
        c1_records.run_c1_gate(tmp_path, "C0-cal",
                               lambda: c1_chart.fit_chart_lcc(X, ids, cfg), chart=True)
    assert caught.value.status == "FAIL_TECHNICAL"
    assert isinstance(caught.value.__cause__, errors.Invalid)
