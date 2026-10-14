"""Independent synthetic tests, author A (spec v2.3): cochain.integer_lift
(TEST_PLAN A2, A3 lift part, A4, A5, A14).

Written from tools/x4_circle_history/API.md (v2.2 incl. clarifications), CONTRACT.json and
TEST_PLAN.md only. Certificates are re-verified HERE with explicit triangle sums and congruences;
the coboundary matrix handed to integer_lift is built in this file from the written definition.

Key hand case (K4 boundary = 2-sphere, so every integer 1-cocycle is exact). Edge order
(0,1),(0,2),(0,3),(1,2),(1,3),(2,3); triangles (0,1,2),(0,1,3),(0,2,3),(1,2,3).
z* = (1,1,-1,1,1,1) gives b = D1 z* = (1,3,3,1). Triangle sums 3 on (0,1,3) and (0,2,3) force
z13=z23=z01=z02=1, z03=-1, then z12=1: z* is the UNIQUE solution with |z| <= 1, so the first
bound B=1 returns exactly z* whatever the MILP path. Vertex moves d_v = delta e_v:
d0=(-1,-1,-1,0,0,0), d1=(1,0,0,-1,-1,0), d2=(0,1,0,1,0,-1), d3=(0,0,1,0,1,1).
Pass 1: v0 z+d0=(0,0,-2,1,1,1) L1 6->5 kept; v1 z+d1=(1,0,-2,0,0,1) L1 5->4 kept; v2, v3 and
all of pass 2: every trial has L1 >= 5 > 4, nothing kept. Final z = (1,0,-2,0,0,1), ||z||_1 = 4.
Tie-break note: ||z+d||_1 + ||z-d||_1 >= 2||z||_1 (convexity), so at most ONE of the two trials
can be strictly below ||z||_1; the (L1, tuple) tie rule is therefore unobservable and untested.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import cochain  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

P = 47
CHART_KEYS = (
    "field", "lift_bounds", "lift_node_limit", "lift_cpu_cap_s", "lift_rounding_tol",
    "local_passes", "local_vertices", "extension_k", "support_min_resultant",
    "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows", "overall_resultant_max",
    "smoothing_residual_max",
)


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
    """Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints."""
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


def coboundary(f, edges):
    return [int(f[j]) - int(f[i]) for i, j in np.asarray(edges).tolist()]


def lift(a, edges, triangles, n, cfg=None, **kwargs):
    edges = as_int(edges).reshape(-1, 2)
    triangles = as_int(triangles).reshape(-1, 3)
    cfg = make_cfg() if cfg is None else cfg
    return cochain.integer_lift(as_int(a), reference_d1(edges, triangles), edges, triangles,
                                n, cfg, **kwargs)


def certified_correction(alpha, a, edges, triangles):
    """Explicit closure, congruence and D1 z = b; returns z = (a - alpha) / p."""
    alpha = np.asarray(alpha)
    assert alpha.dtype == np.int64 and alpha.shape == (len(a),)
    assert triangle_sums(alpha, edges, triangles) == [0] * len(triangles)
    diff = [int(x) - int(y) for x, y in zip(a, alpha.tolist())]
    assert all(d % P == 0 for d in diff)
    z = [d // P for d in diff]
    defect = triangle_sums(a, edges, triangles)
    assert all(s % P == 0 for s in defect)
    assert triangle_sums(z, edges, triangles) == [s // P for s in defect]
    return z


class JumpClock:
    """0.0 for the first `zero_calls` readings, then `late` (far beyond the 30 s cap)."""

    def __init__(self, zero_calls, late=1000.0):
        self.zero_calls, self.late, self.calls = zero_calls, late, 0

    def __call__(self):
        self.calls += 1
        return 0.0 if self.calls <= self.zero_calls else self.late


class SteppingClock:
    """Reading k (k = 0, 1, ...) returns k * step."""

    def __init__(self, step):
        self.step, self.calls = step, 0

    def __call__(self):
        value = self.calls * self.step
        self.calls += 1
        return float(value)


class FirstThenClock:
    def __init__(self, first, rest):
        self.first, self.rest, self.calls = first, rest, 0

    def __call__(self):
        self.calls += 1
        return self.first if self.calls == 1 else self.rest


K4_EDGES = as_int([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
K4_TRIS = as_int([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
Z_STAR = [1, 1, -1, 1, 1, 1]
G_K4 = [0, 3, -5, 7]
EXACT_K4 = coboundary(G_K4, K4_EDGES)            # (3, -5, 7, -8, 4, 12)
A_K4 = [P * z + c for z, c in zip(Z_STAR, EXACT_K4)]  # (50, 42, -40, 39, 51, 59)
TRI_EDGES = as_int([[0, 1], [0, 2], [1, 2]])
TRI = as_int([[0, 1, 2]])
SHIFT = 127  # K4 on vertices 127..130 inside n = 131
K4_SHIFT_EDGES = K4_EDGES + SHIFT
K4_SHIFT_TRIS = K4_TRIS + SHIFT


def test_fixture_arithmetic():
    assert EXACT_K4 == [3, -5, 7, -8, 4, 12]
    assert A_K4 == [50, 42, -40, 39, 51, 59]
    assert triangle_sums(Z_STAR, K4_EDGES, K4_TRIS) == [1, 3, 3, 1]
    assert triangle_sums(A_K4, K4_EDGES, K4_TRIS) == [47, 141, 141, 47]
    assert not issubclass(errors.Unresolved, errors.Invalid)
    assert not issubclass(errors.Invalid, errors.Unresolved)


# ----------------------------------------------------------------------------------------- A2
def test_closed_cocycle_is_centered_exact():
    # v2.2: the cap clock starts with the bounded search, which the exact path never enters.
    alpha, info = lift(EXACT_K4, K4_EDGES, K4_TRIS, 4, clock=SteppingClock(1000.0))
    assert np.asarray(alpha).dtype == np.int64 and np.asarray(alpha).tolist() == EXACT_K4
    assert info["kind"] == "centered_exact"
    assert info["solver_calls"] == 0 and info["l1_correction"] == 0
    cycle = as_int([[0, 1], [0, 3], [1, 2], [2, 3]])  # closed (no triangles), not exact
    alpha_c, info_c = lift([1, 0, 0, 0], cycle, np.zeros((0, 3)), 4)
    assert np.asarray(alpha_c).tolist() == [1, 0, 0, 0]
    assert info_c["kind"] == "centered_exact"


def test_single_triangle_centred_modular_cocycle_is_lifted():
    a = [20, -7, 20]  # centred values; integral sum 20 + 7 + 20 = 47
    alpha, info = lift(a, TRI_EDGES, TRI, 3)
    z = certified_correction(alpha, a, TRI_EDGES, TRI)
    # The six |z|<=1 solutions of z01 - z02 + z12 = 1 all reach L1 = 1 within one pass, so the
    # result is one of the three unit corrections.
    assert z in ([1, 0, 0], [0, -1, 0], [0, 0, 1])
    assert np.asarray(alpha).tolist() in ([-27, -7, 20], [20, 40, 20], [20, -7, -27])
    assert info["kind"] == "corrected_exact"
    assert info["l1_correction"] == 1 == sum(abs(v) for v in z)
    assert info["solver_calls"] == 1


def test_wheel_disk_lift_certificate():
    edges = as_int([[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 2], [1, 6], [2, 3],
                    [3, 4], [4, 5], [5, 6]])
    tris = as_int([[0, 1, 2], [0, 1, 6], [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 6]])
    w = [0] * 12
    w[0], w[9], w[11] = 1, -1, 2  # +(0,1) -(3,4) +2(5,6)
    a = [c + P * x for c, x in zip(coboundary([0, 5, -3, 11, 2, -9, 4], edges), w)]
    assert triangle_sums(a, edges, tris) == [47, 47, 0, -47, 0, 94]
    alpha, info = lift(a, edges, tris, 7)
    z = certified_correction(alpha, a, edges, tris)
    assert info["kind"] == "corrected_exact"
    assert info["l1_correction"] == sum(abs(v) for v in z)


# ------------------------------------------------------------------------------ A3 (lift part)
def test_not_cocycle_mod_p_is_invalid_before_any_cap():
    with pytest.raises(errors.Invalid):
        lift([1, 0, 0, 0, 0, 0], K4_EDGES, K4_TRIS, 4)  # sum on (0,1,2) is 1
    with pytest.raises(errors.Invalid):  # step 2 precedes the bounded search and its clock
        lift([20, -7, 21], TRI_EDGES, TRI, 3, clock=SteppingClock(1000.0))


# ----------------------------------------------------------------------------------------- A4
def test_local_passes_hand_case():
    alpha, info = lift(A_K4, K4_EDGES, K4_TRIS, 4)
    z = certified_correction(alpha, A_K4, K4_EDGES, K4_TRIS)
    assert z == [1, 0, -2, 0, 0, 1]
    assert np.asarray(alpha).tolist() == [3, 42, 54, 39, 51, 12]  # a - 47 z
    assert info["kind"] == "corrected_exact"
    assert info["l1_correction"] == 4
    assert info["solver_calls"] == 1


@pytest.mark.parametrize("overrides, z_final", [
    ({"local_vertices": 1}, [0, 0, -2, 1, 1, 1]),   # only v0 moves; pass 2 keeps nothing
    ({"local_vertices": 2}, [1, 0, -2, 0, 0, 1]),
    ({"local_passes": 1}, [1, 0, -2, 0, 0, 1]),
    ({"local_passes": 0}, Z_STAR),                   # exactly zero passes: MILP answer kept
])
def test_local_passes_follow_cfg(overrides, z_final):
    alpha, info = lift(A_K4, K4_EDGES, K4_TRIS, 4, cfg=make_cfg(**overrides))
    assert certified_correction(alpha, A_K4, K4_EDGES, K4_TRIS) == z_final
    assert info["l1_correction"] == sum(abs(v) for v in z_final)


def test_local_passes_stop_at_vertex_128():
    # Same K4 on vertices 127..130 of n = 131: only v = 127 < min(128, 131) may move, so the
    # result equals the local_vertices=1 case; vertices 0..126 are isolated (d = 0, no gain).
    a = [P * z for z in Z_STAR]
    alpha, info = lift(a, K4_SHIFT_EDGES, K4_SHIFT_TRIS, 131)
    z = certified_correction(alpha, a, K4_SHIFT_EDGES, K4_SHIFT_TRIS)
    assert z == [0, 0, -2, 1, 1, 1]
    assert np.asarray(alpha).tolist() == [47, 47, 47, 0, 0, 0]
    assert info["l1_correction"] == 5


# ----------------------------------------------------------------------------------------- A5
@pytest.mark.parametrize("step", [31.0, 30.0])  # 30.0: elapsed == cap must already fail (>=)
def test_cap_exceeded_before_first_bound(step):
    with pytest.raises(errors.Unresolved):
        lift(A_K4, K4_EDGES, K4_TRIS, 4, clock=SteppingClock(step))


def test_cap_not_reached_succeeds():
    alpha, _ = lift(A_K4, K4_EDGES, K4_TRIS, 4, clock=FirstThenClock(0.0, 29.5))
    assert certified_correction(alpha, A_K4, K4_EDGES, K4_TRIS) == [1, 0, -2, 0, 0, 1]


def test_unsatisfiable_within_all_bounds_is_unresolved():
    # b = 2303 / 47 = 49 on one triangle, but |z01 - z02 + z12| <= 48 when |z| <= 16.
    calls = []
    with pytest.raises(errors.Unresolved):
        lift([2303, 0, 0], TRI_EDGES, TRI, 3, guard=lambda: calls.append(1),
             clock=lambda: 0.0)
    assert len(calls) == 5  # guard() once per bound in (1, 2, 4, 8, 16)


def test_guard_exception_propagates():
    class Stop(Exception):
        pass

    def guard():
        raise Stop()

    with pytest.raises(Stop):
        lift(A_K4, K4_EDGES, K4_TRIS, 4, guard=guard)


# ---------------------------------------------------------------------------------------- A14
def test_a14_over_cap_before_first_call():
    with pytest.raises(errors.Unresolved):  # start reads 0, every later reading is 1000
        lift(A_K4, K4_EDGES, K4_TRIS, 4, clock=JumpClock(1))


def test_a14_cap_passed_during_successful_solve_is_rejected():
    """The B=1 solve succeeds (unique z*), but the clock is past the cap afterwards.

    The clock arms at guard() and jumps at the 3rd reading after it. With one pre-call reading
    (check a, time_limit from the same elapsed) the jump is seen by check (d); with a separate
    time_limit reading it is check (b). local_passes = 0 removes check (c). Both are mandated
    Unresolved, and no reading before the native call is ever past the cap (no negative limit).
    """
    state = {"armed": False, "since": 0}

    def guard():
        state["armed"] = True

    def clock():
        if state["armed"]:
            state["since"] += 1
            if state["since"] >= 3:
                return 1000.0
        return 0.0

    cfg = make_cfg(local_passes=0)
    with pytest.raises(errors.Unresolved):
        lift(A_K4, K4_EDGES, K4_TRIS, 4, cfg=cfg, guard=guard, clock=clock)
    assert state["since"] >= 3
    alpha, info = lift(A_K4, K4_EDGES, K4_TRIS, 4, cfg=cfg, clock=lambda: 0.0)  # control
    assert certified_correction(alpha, A_K4, K4_EDGES, K4_TRIS) == Z_STAR
    assert info["l1_correction"] == 6


def test_a14_cap_reached_during_local_passes():
    # At most 5 readings precede the passes (start, check a, time_limit, check b, + one spare);
    # the 2 passes take 2 * 128 vertex-step readings, so reading 41 lands inside them.
    a = [P * z for z in Z_STAR]
    with pytest.raises(errors.Unresolved):
        lift(a, K4_SHIFT_EDGES, K4_SHIFT_TRIS, 131, clock=JumpClock(40))
    alpha, _ = lift(a, K4_SHIFT_EDGES, K4_SHIFT_TRIS, 131, clock=JumpClock(10 ** 9))
    assert np.asarray(alpha).tolist() == [47, 47, 47, 0, 0, 0]


def test_a14_highs_options_pinned():
    pinned = cochain.HIGHS_PINNED
    assert pinned == {"threads": 1, "parallel": False}
    assert type(pinned["threads"]) is int and pinned["parallel"] is False
