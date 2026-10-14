"""Independent contract tests for ``topo_pilot.analysis.x5_endpoint`` (part 2 of 2).

Written by an independent test writer from the API contract only
(docs/proposals/X5_G1_TRAINING_API.md §1 and §8 "Endpoint"; protocol x5g1-train-v3 §4-§6),
without reading the implementation.

Covers: ``paired_bootstrap_endpoint`` (one shared ``rng.integers(0, R, size=R)`` whole-row
index draw per replicate, reproduced here with an identically seeded generator and an
independent reference; censored draws kept; guard strings; shape errors), ``pair_evidence``,
``pair_flags`` and the ``cohort_verdict`` truth table.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from topo_pilot.analysis.x5_endpoint import (
    DELAY,
    DiffBounds,
    PairEvidence,
    cohort_verdict,
    difference_bounds,
    grid_event,
    pair_evidence,
    pair_flags,
    paired_bootstrap_endpoint,
)
from topo_pilot.contracts import SeedTree

pytestmark = pytest.mark.analysis

G5 = (0, 10, 20, 30, 40)
GC_C, GC_F = 0.2, 0.25
# Per-history regret curves [R=7, K=5]; mixed so that resampling yields both observed and
# censored events in each arm (R is odd on purpose: a single batched integers() call for all
# draws would not reproduce the per-draw stream).
REG_C = 0.03 * np.array([
    [1, 1, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 0], [1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 0, 0, 1]], dtype=float)
REG_F = 0.0375 * np.array([
    [1, 1, 1, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 1, 0, 0]], dtype=float)


def _gen(name: str = "boot") -> np.random.Generator:
    return SeedTree(5).generator("t", name)


def _ref_event(passes, grid) -> tuple[float, float, bool]:
    for j in range(len(grid) - 2):
        if passes[j] and passes[j + 1] and passes[j + 2]:
            return float(grid[j]), float(grid[j]), False
    return float(grid[-3]), math.inf, True


def _ref_boot(rc, rf, gcc, gcf, gen, n, grid, thr=0.05):
    r = rc.shape[0]
    lo, hi, cc, cf = [], [], [], []
    for _ in range(n):
        idx = gen.integers(0, r, size=r)
        lc, uc, c_c = _ref_event(rc[idx].mean(axis=0) / gcc <= thr, grid)
        lf, uf, c_f = _ref_event(rf[idx].mean(axis=0) / gcf <= thr, grid)
        lo.append(lc - uf)
        hi.append(uc - lf)
        cc.append(c_c)
        cf.append(c_f)
    return np.array(lo), np.array(hi), np.array(cc), np.array(cf)


def _ref_q(values, q) -> float:
    s = sorted(float(v) for v in values)
    return s[max(1, math.ceil(q * len(s) - 1e-9)) - 1]


# ------------------------------------------------------------ paired_bootstrap_endpoint


def test_bootstrap_reproduces_shared_whole_row_draws() -> None:
    n = 60
    res = paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=n, batch=20,
                                    grid=G5)
    lo, hi, cc, cf = _ref_boot(REG_C, REG_F, GC_C, GC_F, _gen(), n, G5)
    # Fixture sanity: both arms have censored and observed draws.
    assert 0 < cc.mean() < 1 and 0 < cf.mean() < 1
    assert np.asarray(res.d_low).shape == (n,) and np.asarray(res.d_high).shape == (n,)
    assert np.array_equal(np.asarray(res.d_low, dtype=float), lo)
    assert np.array_equal(np.asarray(res.d_high, dtype=float), hi)
    assert not np.isnan(res.d_low).any() and not np.isnan(res.d_high).any()
    assert np.array_equal(np.asarray(res.censored_curved, dtype=bool), cc)
    assert np.array_equal(np.asarray(res.censored_flat, dtype=bool), cf)


def test_bootstrap_keeps_censored_draws_and_fractions() -> None:
    n = 60
    res = paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=n, batch=30,
                                    grid=G5)
    _, _, cc, cf = _ref_boot(REG_C, REG_F, GC_C, GC_F, _gen(), n, G5)
    assert len(res.d_low) == n  # nothing dropped
    assert res.censored_curved_frac == pytest.approx(cc.mean(), abs=1e-12)
    assert res.censored_flat_frac == pytest.approx(cf.mean(), abs=1e-12)
    assert np.isinf(res.d_high).sum() >= 1 or np.isinf(res.d_low).sum() >= 1


def test_bootstrap_quantiles_are_inverted_cdf_order_statistics() -> None:
    n = 60
    res = paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=n, batch=20,
                                    grid=G5)
    lo, hi, _, _ = _ref_boot(REG_C, REG_F, GC_C, GC_F, _gen(), n, G5)
    assert res.q025_low == _ref_q(lo, 0.025)
    assert res.q975_high == _ref_q(hi, 0.975)


def test_bootstrap_consumes_exactly_one_integers_call_per_draw() -> None:
    gen = _gen()
    paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, gen, n_draws=9, batch=3, grid=G5)
    ref = _gen()
    for _ in range(9):
        ref.integers(0, REG_C.shape[0], size=REG_C.shape[0])
    assert gen.integers(0, 2**62) == ref.integers(0, 2**62)


def test_bootstrap_guard_strings_per_batch() -> None:
    calls: list[str] = []
    paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=6, batch=3,
                              grid=G5, guard=calls.append)
    assert calls == ["bootstrap 0", "bootstrap 0 done", "bootstrap 3", "bootstrap 3 done"]


def test_bootstrap_guard_brackets_the_draws() -> None:
    gen = _gen()
    seen: list[str] = []
    probe_state: list[int] = []

    def guard(msg: str) -> None:
        seen.append(msg)
        probe_state.append(gen.bit_generator.state["state"]["state"])

    paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, gen, n_draws=4, batch=2, grid=G5,
                              guard=guard)
    assert seen == ["bootstrap 0", "bootstrap 0 done", "bootstrap 2", "bootstrap 2 done"]
    # Draws happen between "start" and "done" of a batch, none between batches.
    assert probe_state[0] != probe_state[1]
    assert probe_state[1] == probe_state[2]
    assert probe_state[2] != probe_state[3]


def test_bootstrap_threshold_passthrough() -> None:
    res = paired_bootstrap_endpoint(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=8, batch=4,
                                    grid=G5, threshold=10.0)
    assert np.all(np.asarray(res.d_low) == 0) and np.all(np.asarray(res.d_high) == 0)
    assert res.censored_curved_frac == 0 and res.censored_flat_frac == 0


def test_bootstrap_default_grid_27_points() -> None:
    rc = np.zeros((3, 27))
    rc[:, :5] = 1.0  # PASS from index 5 (step 500)
    rf = np.zeros((3, 27))
    res = paired_bootstrap_endpoint(rc, rf, 1.0, 1.0, _gen(), n_draws=4, batch=2)
    assert np.all(np.asarray(res.d_low) == 500) and np.all(np.asarray(res.d_high) == 500)
    assert res.q025_low == 500 and res.q975_high == 500


@pytest.mark.parametrize("rc_shape,rf_shape", [((7, 5), (6, 5)), ((7, 5), (7, 4)),
                                               ((7, 4), (7, 4))])
def test_bootstrap_shape_errors(rc_shape, rf_shape) -> None:
    with pytest.raises(ValueError):
        paired_bootstrap_endpoint(np.zeros(rc_shape), np.zeros(rf_shape), 1.0, 1.0, _gen(),
                                  n_draws=4, batch=2, grid=G5)


# ------------------------------------------------------------------------ pair_evidence


def test_pair_evidence_point_from_full_sample_and_quantiles_from_bootstrap() -> None:
    ev = pair_evidence(REG_C, REG_F, GC_C, GC_F, _gen(), n_draws=60, batch=20, grid=G5)
    pc = REG_C.mean(axis=0) / GC_C <= 0.05
    pf = REG_F.mean(axis=0) / GC_F <= 0.05
    ec, ef = grid_event(list(map(bool, pc)), grid=G5), grid_event(list(map(bool, pf)), grid=G5)
    assert ev.events == (ec, ef)
    assert ev.point == difference_bounds(ec, ef)
    lo, hi, _, _ = _ref_boot(REG_C, REG_F, GC_C, GC_F, _gen(), 60, G5)
    assert ev.q025_low == _ref_q(lo, 0.025) and ev.q975_high == _ref_q(hi, 0.975)


def test_pair_evidence_deterministic_observed() -> None:
    rc = np.zeros((4, 5))
    rc[:, 0] = 1.0  # curved PASS from step 10
    rf = np.zeros((4, 5))  # flat PASS from step 0
    ev = pair_evidence(rc, rf, 1.0, 1.0, _gen(), n_draws=6, batch=3, grid=G5)
    assert ev.events[0].tau == 10 and ev.events[1].tau == 0
    assert (ev.point.low, ev.point.high) == (10, 10)
    assert ev.q025_low == 10 and ev.q975_high == 10


# --------------------------------------------------------------------------- pair_flags

_EVENTS = (grid_event([True] * 5, grid=G5), grid_event([True] * 5, grid=G5))


def _pe(low: float, q025: float, q975: float, high: float = math.inf) -> PairEvidence:
    point = DiffBounds(low=low, high=high, low_strict=False, high_strict=False)
    return PairEvidence(point=point, q025_low=q025, q975_high=q975, events=_EVENTS)


@pytest.mark.parametrize("low,q025,q975,want", [
    (250.0, 1e-9, math.inf, (True, False)),     # D_low equality counts
    (249.999, 10.0, math.inf, (False, False)),
    (500.0, 0.0, math.inf, (False, False)),     # q025 must be strictly > 0
    (500.0, -math.inf, 1000.0, (False, False)),
    (math.inf, 10.0, math.inf, (True, False)),
    (-math.inf, -math.inf, 249.999, (False, True)),
    (-math.inf, -math.inf, 250.0, (False, False)),  # strict < DELAY
    (300.0, 10.0, 200.0, (True, True)),
])
def test_pair_flags(low, q025, q975, want) -> None:
    assert DELAY == 250
    sup, rej = pair_flags(_pe(low, q025, q975))
    assert (bool(sup), bool(rej)) == want


# ----------------------------------------------------------------------- cohort_verdict

S = _pe(500.0, 100.0, math.inf)               # supported only
R_ = _pe(-math.inf, -math.inf, 100.0)         # rejected only
B = _pe(300.0, 10.0, 200.0)                   # supported and rejected
N = _pe(0.0, -100.0, 1000.0)                  # neither


@pytest.mark.parametrize("pairs,kw,want", [
    ([S, S, S], {}, "SUPPORTED"),
    ([S, S, R_], {}, "REJECTED"),
    ([R_, N, N], {}, "REJECTED"),
    ([R_, R_, R_], {}, "REJECTED"),
    ([B, N, N], {}, "REJECTED"),
    ([S, S, B], {}, "INCONCLUSIVE"),          # contradiction
    ([B, B, B], {}, "INCONCLUSIVE"),          # contradiction
    ([S, S, None], {}, "INCONCLUSIVE"),
    ([R_, R_, None], {}, "INCONCLUSIVE"),
    ([S, S, S], {"failures": ("a020 seed 2 INCOMPLETE",)}, "INCONCLUSIVE"),
    ([R_, R_, R_], {"failures": ["integrity"]}, "INCONCLUSIVE"),
    ([S, S], {}, "INCONCLUSIVE"),
    ([S, S, S, S], {}, "INCONCLUSIVE"),
    ([], {}, "INCONCLUSIVE"),
    ([S, S], {"n_required": 2}, "SUPPORTED"),
    ([S, S, S], {"n_required": 2}, "INCONCLUSIVE"),
    ([S, S, N], {}, "INCONCLUSIVE"),
    ([N, N, N], {}, "INCONCLUSIVE"),
    ([S, N, S], {}, "INCONCLUSIVE"),
])
def test_cohort_verdict_truth_table(pairs, kw, want) -> None:
    verdict, reason = cohort_verdict(pairs, **kw)
    assert verdict == want
    assert isinstance(reason, str) and reason.strip()


def test_cohort_verdict_accepts_tuple() -> None:
    assert cohort_verdict((S, S, S))[0] == "SUPPORTED"
