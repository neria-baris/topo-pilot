"""Independent tests, author A (job 0026): fit_chart_lcc on a 512-landmark fixture whose largest
component has exactly 487 landmarks (TEST_PLAN A-1 items 2, 3, 5, 6 and 9; protocol section 14).

Fixture: a thin rectangular loop of 487 points plus 25 isolated satellites at interleaved
landmark positions (7, 27, ...). Every expected value is recomputed here by calling the frozen
K4 kernels (chart.py, cochain.py), ripser and scipy directly, step by step as protocol section 14
prescribes; c1_chart is never used to check itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

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
import chart  # noqa: E402
import cochain  # noqa: E402
import errors  # noqa: E402

FIELD, N, M = 47, 512, 487
TWO_PI = 2.0 * np.pi


def make_ids(n, base=10**9):
    return np.array([f"{base + 3 * k:020d}" for k in range(n)])


def loop_points(m, width=8.0):
    """m points on the perimeter (length m) of a (m/2 - width) x width rectangle, jittered."""
    k = np.arange(m, dtype=np.float64)
    t = k + 0.15 * np.sin(1.3 * k)
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


class Recorder:
    def __init__(self):
        self.items = []

    def __call__(self, name, record):
        self.items.append((name, dict(record)))


def pick(record, *names):
    for name in names:
        if name in record:
            return record[name]
    raise AssertionError(f"record lacks every one of {names}: {sorted(record)}")


@pytest.fixture(scope="module")
def built():
    loop, t = loop_points(M)
    n_sat = N - M
    sat = np.column_stack([10.0 + 8.0 * np.arange(n_sat), np.full(n_sat, -7.0),
                           np.zeros(n_sat)])
    sat_idx = 7 + 20 * np.arange(n_sat)
    loop_idx = np.setdiff1d(np.arange(N), sat_idx)
    X = np.empty((N, 3))
    X[loop_idx], X[sat_idx] = loop, sat
    ids, cfg, rec = make_ids(N), c1_config.chart_cfg(), Recorder()
    ch = c1_chart.fit_chart_lcc(X.copy(), ids, cfg, persist=rec)
    m32 = 0.9 * np.column_stack([np.cos(TWO_PI * t / M), np.sin(TWO_PI * t / M)])
    return SimpleNamespace(X=X, loop_idx=loop_idx, sat_idx=sat_idx, ids=ids, cfg=cfg, rec=rec,
                           ch=ch, m32=m32)


@pytest.fixture(scope="module")
def ref(built):
    """Section 14 steps 1-8 with the frozen kernels, independently of c1_chart."""
    X, cfg = built.X, built.cfg
    D = chart.cdist(X, X)
    res = ripser.ripser(D, maxdim=1, coeff=FIELD, distance_matrix=True, do_cocycles=True)
    dgm1 = res["dgms"][1]
    k = chart.select_h1_bar(dgm1)
    b, d = float(dgm1[k, 0]), float(dgm1[k, 1])
    r = (b + d) / 2.0
    E = cochain.edge_list(D, r)
    a = chart.cocycle_to_edges(res["cocycles"][1][k], E, FIELD)
    A = coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(N, N))
    count, labels = connected_components(A, directed=False)
    cstar = np.flatnonzero(labels == labels[built.loop_idx[0]])
    pos = np.full(N, -1, dtype=np.int64)
    pos[cstar] = np.arange(len(cstar))
    keep = (pos[E[:, 0]] >= 0) & (pos[E[:, 1]] >= 0)
    E_C, a_C = pos[E[keep]].astype(np.int64), a[keep]
    m = len(cstar)
    D1, tri = cochain.triangle_system(E_C, m)
    alpha, lift = cochain.integer_lift(a_C, D1, E_C, tri, m, cfg)
    beta, q, g = cochain.primitive_class(alpha, E_C, tri, m, FIELD)
    phi, resid = cochain.smooth_phase(beta, E_C, m)
    h0 = res["dgms"][0][:, 1]
    return SimpleNamespace(D=D, k=int(k), b=b, d=d, r=r, E=E, keep=keep, count=int(count),
                           labels=labels, cstar=cstar, E_C=E_C, a_C=a_C, alpha=alpha, lift=lift,
                           beta=beta, q=q, g=g, phi=phi, resid=resid,
                           l_max=float(h0[np.isfinite(h0)].max()))


def same(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()


def test_fixture_has_one_487_component_and_25_singletons(built, ref):
    assert ref.count == 26
    assert np.array_equal(ref.cstar, built.loop_idx)
    assert sorted(np.bincount(ref.labels).tolist(), reverse=True) == [487] + [1] * 25
    touched = np.unique(ref.E.ravel())  # satellites carry no edge at r
    assert np.intersect1d(touched, built.sat_idx).size == 0


def test_giant_487_passes_and_restriction_keeps_cstar_only(built, ref):
    ch = built.ch
    assert int(ch.info["m"]) == 487 and int(ch.info["n"]) == 512
    assert np.array_equal(np.asarray(ch.info["cstar"]), ref.cstar)
    assert [str(x) for x in ch.landmark_ids] == [str(x) for x in built.ids[ref.cstar]]
    assert same(ch.landmarks, built.X[ref.cstar])
    assert same(ch.edges, ref.E_C) and same(ch.cocycle, ref.a_C)
    assert np.asarray(ch.edges).tolist() == sorted(np.asarray(ch.edges).tolist())
    assert int(ch.info["n_components"]) == 26
    assert [int(s) for s in ch.info["component_sizes"]] == [487] + [1] * 25
    assert [str(x) for x in ch.info["excluded_ids"]] == [str(x) for x in built.ids[built.sat_idx]]
    assert ch.info["l_max"] == ref.l_max
    assert (ch.info["birth"], ch.info["death"], ch.info["radius"]) == (ref.b, ref.d, ref.r)
    assert ch.info["bar_index"] == ref.k
    assert ch.info["n_edges"] == len(ref.E_C)


def test_lift_primitive_smoothing_are_the_frozen_kernels_on_cstar(built, ref):
    ch = built.ch
    assert same(ch.integer_lift, ref.alpha)
    correction = ref.lift.get("correction", np.zeros(len(ref.E_C), dtype=np.int64))
    assert same(ch.lift_correction, np.asarray(correction, dtype=np.int64))
    assert same(ch.primitive, ref.beta) and same(ch.tree_potential, ref.q)
    assert ch.period_gcd == ref.g and ch.period_gcd != 0 and ch.period_gcd % FIELD != 0
    assert same(ch.phi, ref.phi)
    assert ch.info["smoothing_residual"] == float(ref.resid)
    assert ch.info["lift_kind"] == ref.lift["kind"] == ch.info["lift"]["kind"]


def test_scale_statistics_use_the_cstar_submatrix_only(built, ref):
    """Item 6: d8, sigma and support_radius from _neighbor_scale(D[np.ix_(C*, C*)])."""
    d8_c, sigma_c, support_c = chart._neighbor_scale(ref.D[np.ix_(ref.cstar, ref.cstar)])
    d8_all, sigma_all, support_all = chart._neighbor_scale(ref.D)
    ch = built.ch
    assert same(ch.d8, d8_c) and ch.sigma == sigma_c and ch.support_radius == support_c
    # the fixture makes the two domains differ (isolated points, nonconstant d8)
    assert np.unique(d8_c).size > 10
    assert len(d8_all) == 512 and sigma_all != sigma_c and support_all != support_c


def test_persist_order_and_values(built, ref):
    """Items 3 and 9: giant before the lift, then lift kind, g and the smoothing residual."""
    names = [name for name, _ in built.rec.items]
    assert names == ["giant", "lift", "primitive", "smoothing"]
    giant, lift, prim, smooth = (rec for _, rec in built.rec.items)
    assert pick(giant, "b", "birth") == ref.b and pick(giant, "d", "death") == ref.d
    assert pick(giant, "r", "radius") == ref.r and int(pick(giant, "k", "bar_index")) == ref.k
    assert pick(giant, "l_max", "ell_max", "lmax") == ref.l_max
    assert int(pick(giant, "n_components", "component_count")) == 26
    assert [int(s) for s in pick(giant, "component_sizes", "sizes")] == [487] + [1] * 25
    excluded = pick(giant, "excluded_ids", "excluded_landmark_ids", "excluded")
    assert [str(x) for x in excluded] == [str(x) for x in built.ids[built.sat_idx]]
    assert int(pick(giant, "m")) == 487 and int(pick(giant, "n")) == 512
    assert bool(pick(giant, "giant_pass", "pass", "passed", "giant")) is True
    assert lift["kind"] == ref.lift["kind"]
    assert int(prim["g"]) == ref.g
    assert float(smooth["residual"]) == float(ref.resid)


def test_excluded_landmarks_get_extension_phases_only(built):
    """Item 5: satellites are never charted neighbours; their phase comes from extend."""
    ch, cfg = built.ch, built.cfg
    gauge = c1_chart.fit_production_gauge(ch, built.m32)
    Q = built.X[built.sat_idx]
    ext = c1_chart.extend_phase(ch, gauge, Q, cfg)
    want = chart.extend(ch, gauge, Q, cfg)
    for name in ("phase", "resultant", "eighth_distance", "supported", "duplicate"):
        assert same(getattr(ext, name), getattr(want, name)), name
    assert not np.any(ext.duplicate)  # no satellite is a charted landmark
    assert np.all((ext.phase >= 0.0) & (ext.phase < TWO_PI))
    dist = chart.cdist(Q, np.asarray(ch.landmarks))
    assert dist.min() > 6.0
    on_chart = c1_chart.extend_phase(ch, gauge, built.X[built.loop_idx[:5]], cfg)
    assert np.all(on_chart.duplicate)


def test_gauge_points_are_the_cstar_landmarks_only(built):
    ch = built.ch
    gauge = c1_chart.fit_production_gauge(ch, built.m32)
    assert gauge == chart.fit_gauge(ch, built.m32)
    assert gauge.alignment > 0.0 and np.isfinite(gauge.alignment)
    m32_all = np.zeros((N, 2))
    m32_all[built.loop_idx] = built.m32
    with pytest.raises(errors.Invalid):
        c1_chart.fit_production_gauge(ch, m32_all)


def test_serialise_roles_and_identity_carrier(built):
    ch = built.ch
    gauge = c1_chart.fit_production_gauge(ch, built.m32)
    assert c1_chart.IDENTITY_CARRIER == chart.Gauge(sign=1, shift=0.0, alignment=0.0)
    prod = c1_chart.serialise(ch, gauge, "production")
    direct = c1_chart.serialise(ch, c1_chart.IDENTITY_CARRIER, "validation_only")
    base = chart.chart_to_arrays(ch, gauge)
    for name in ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "scalars"):
        assert same(prod[name], base[name]), name
    info_p, info_d = json.loads(str(prod["info_json"])), json.loads(str(direct["info_json"]))
    assert info_p["role"] == "production" and info_p["gauge_fitted"] is True
    assert info_d["role"] == "validation_only" and info_d["gauge_fitted"] is False
    assert np.asarray(direct["scalars"])[3:].tolist() == [1.0, 0.0, 0.0]
