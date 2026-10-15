"""Independent tests of tools/x2a_stage0 (job 0025), part 2: credits, the additive score,
statistics, decision labels, verdict logic and the PH readings on hand-made inputs.

Written from X2A-FROZEN-v1 and tools/x2a_stage0/API.md only. The module is imported, never read.
Expected values are derived by hand from the protocol's rules (Lemmas A and C, sections 5.6, 5.9,
6.3 and 7); the toy-HMM references are coded here and import nothing from the module."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.oracle import BayesFilter
from topo_pilot.world import WORLD_REGISTRY

pytestmark = pytest.mark.oracle

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "x2a_stage0"), ("tools", "x4_oracle_profile"),
               ("tests", "oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

import x2a_mc as xc  # noqa: E402
import x2a_ph as xp  # noqa: E402

INF = np.inf
GATES = ("PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5")


def rows(*bars) -> np.ndarray:  # (dim, birth, death) -> DiagramResult.rows (+ censored = 0)
    return np.array([[d, b, e, 0.0] for d, b, e in bars], dtype=np.float64).reshape(-1, 4)
def blockdiag(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros((a.shape[0] + b.shape[0],) * 2)
    out[:a.shape[0], :a.shape[0]], out[a.shape[0]:, a.shape[0]:] = a, b
    return out
def ref_loglik(T, E, pi, w) -> float:  # log P(w_1..w_k): unnormalised forward, emit first
    a = pi * E[:, w[0]]
    for s in w[1:]:
        a = (a @ T) * E[:, s]
    return math.log(a.sum())
def approx2(pair, expected) -> bool:
    return tuple(float(v) for v in pair) == pytest.approx(expected, abs=1e-12)


def test_decision_tie_rule():  # 8.4 test 6; Lemma C tie rule, |pi - 1/2| <= tau is a tie
    tau, u = 2.0**-40, 2.0**-52  # offsets from 1/2 that are exact in float64
    pi_d = np.array([0.5, 0.5 + tau, 0.5 - tau, 0.5 + tau + u, 0.5 - tau - u, 0.9, 0.1])
    d = np.asarray(xc.decision(pi_d, tau=tau))
    assert d.dtype == np.int8 and d.tolist() == [-1, -1, -1, 1, 0, 1, 0]
    dflt = np.asarray(xc.decision(np.array([0.5 + 5e-13, 0.5 - 5e-13, 0.5 + 2e-12, 0.5 - 2e-12])))
    assert dflt.tolist() == [-1, -1, 1, 0]  # default tau = 1e-12
def test_lemma_C_credits():  # 8.4 test 6; Lemma C (1) and (2)
    pf = np.array([0.8, 0.8, 0.8, 0.3, 0.3, 0.3])
    pd = np.array([0.7, 0.2, 0.5, 0.6, 0.4, 0.5 + 1e-13])
    assert np.max(np.abs(np.asarray(xc.credit(pf, pd)) - [0.8, 0.2, 0.5, 0.3, 0.7, 0.5])) <= 1e-15
    rng = np.random.default_rng(0)
    pf, pd = rng.random(2000), rng.random(2000)
    pd[::7] = 0.5
    cr, cr32 = np.asarray(xc.credit(pf, pd)), np.asarray(xc.credit(pf, pf))
    assert np.max(np.abs(cr32 - np.maximum(pf, 1 - pf))) <= 1e-15
    dec, best = np.where(pd > 0.5, 1, np.where(pd < 0.5, 0, -1)), np.where(pf > 0.5, 1, 0)
    gap = np.abs(2 * pf - 1) * (((dec != best) & (dec != -1)) + 0.5 * (dec == -1))
    assert np.max(np.abs((cr32 - cr) - gap)) <= 1e-15
    assert np.all(cr32 - cr >= -1e-15) and np.all(cr32 - cr <= 1 + 1e-15)
    pa, pb = np.array([0.4, 0.3, 0.2, 0.1]), np.array([0.1, 0.2, 0.3, 0.4])  # four histories
    post = pb / (pa + pb)  # equal priors
    cr = np.asarray(xc.credit(post, np.array([0.2, 0.5, 0.9, 0.3])))  # decide A, tie, B, A
    p_correct = 0.5 * (0.4 + 0.5 * (0.3 + 0.2) + 0.3 + 0.1)
    assert math.isclose(float(np.sum(0.5 * (pa + pb) * cr)), p_correct, rel_tol=1e-14)


def test_additive_score_iid_toy_equals_full_llr():  # 8.4 test 7; Lemma A(2)
    pa, pb = np.array([0.5, 0.3, 0.2]), np.array([0.2, 0.2, 0.6])
    ea = np.array([[0.7, 0.1, 0.1, 0.1], [0.1, 0.6, 0.2, 0.1], [0.25, 0.25, 0.25, 0.25]])
    eb = np.array([[0.1, 0.1, 0.4, 0.4], [0.3, 0.3, 0.2, 0.2], [0.6, 0.1, 0.1, 0.2]])
    Tt = blockdiag(np.tile(pa, (3, 1)), np.tile(pb, (3, 1)))  # every row = the component's law
    Et, pit = np.vstack((ea, eb)), np.concatenate((pa, pb)) / 2
    tok = np.random.default_rng(7).integers(0, 4, size=(6, 6))
    s_add = np.asarray(xc.additive_score(Tt, Et, pit, tok, n_A=3, block=2, n_blocks=3))
    qa, qb = pa @ ea, pb @ eb  # blocks are independent given c: LLR = sum_t log qB / qA
    llr = np.log(qb[tok]).sum(axis=1) - np.log(qa[tok]).sum(axis=1)
    assert s_add.shape == (6,) and np.max(np.abs(s_add - llr)) <= 1e-12
    b = BayesFilter(Tt, Et, pit).run(tok).b[:, -1]
    assert np.max(np.abs(np.log(b[:, 3:].sum(1)) - np.log(b[:, :3].sum(1)) - llr)) <= 1e-12
def test_additive_score_uses_disjoint_stationary_blocks():  # Lemma A(1); 6.1 blocks
    ta, tb = np.array([[0.9, 0.1], [0.1, 0.9]]), np.full((2, 2), 0.5)  # A sticky, B i.i.d.
    e = np.array([[0.9, 0.1], [0.2, 0.8]])  # one emission for both components
    Tt, Et, pit, u = blockdiag(ta, tb), np.vstack((e, e)), np.full(4, 0.25), np.full(2, 0.5)
    tok = np.array([[0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1], [1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0]])
    s_add = np.asarray(xc.additive_score(Tt, Et, pit, tok, n_A=2, block=2, n_blocks=3))
    ref = [sum(ref_loglik(tb, e, u, r[2 * k:2 * k + 2]) - ref_loglik(ta, e, u, r[2 * k:2 * k + 2])
               for k in range(3)) for r in tok]
    assert np.max(np.abs(s_add - np.array(ref))) <= 1e-12
    full = ref_loglik(tb, e, u, tok[0]) - ref_loglik(ta, e, u, tok[0])
    assert abs(s_add[0] - full) > 1e-6  # dependent blocks: s_add is not the full LLR here
    longer = np.hstack((tok, np.ones((4, 1), dtype=tok.dtype)))  # symbols after the blocks
    s_long = np.asarray(xc.additive_score(Tt, Et, pit, longer, n_A=2, block=2, n_blocks=3))
    assert np.max(np.abs(s_long - s_add)) <= 1e-15


def test_entropy_mass_logit_and_expit():  # 4.2 stable arithmetic (RC 8)
    h = np.asarray(xc.entropy_b(np.array([0.0, 1.0, 0.5, 0.25])))
    h_ref = [0.0, 0.0, math.log(2), -(0.25 * math.log(0.25) + 0.75 * math.log(0.75))]
    assert np.all(np.isfinite(h)) and np.max(np.abs(h - h_ref)) <= 1e-15
    b = np.array([[1e-20, 0.0, 0.5, 0.5], [0.25, 0.25, 0.25, 0.25], [0.6, 0.1, 0.2, 0.1]])
    logit = np.asarray(xc.mass_logit(b, n_A=2))  # the first row's pi rounds to 1 in float64
    assert np.max(np.abs(logit - [math.log(1e20), 0.0, math.log(0.3 / 0.7)])) <= 1e-12
    assert np.max(np.abs(np.asarray(xc.mass_pi(b, n_A=2)) - [1.0, 0.5, 0.3])) <= 1e-15
    with np.errstate(over="raise", invalid="raise"):
        s = np.asarray(xc.expit_pi(np.array([-800.0, 0.0, 800.0, math.log(3.0)])))
    assert np.all(np.isfinite(s)) and 0.0 <= s[0] <= 1e-300 and s[2] == 1.0
    assert abs(s[1] - 0.5) <= 1e-16 and abs(s[3] - 0.75) <= 1e-15
def test_stratified_se_interval_and_hoeffding():  # 5.5 SE, 0 notation, 6.3 Hoeffding
    xa, xb = np.array([1.0, 2.0, 3.0, 4.0]), np.array([10.0, 12.0, 11.0])
    mean, se = xc.strat_mean_se(xa, xb)
    se_ref = math.sqrt(0.25 * (np.var(xa, ddof=1) / 4 + np.var(xb, ddof=1) / 3))
    assert math.isclose(mean, 6.75, rel_tol=1e-15) and math.isclose(se, se_ref, rel_tol=1e-12)
    assert approx2(xc.interval(1.0, 0.1), (1.0 - 0.2576, 1.0 + 0.2576))
    assert approx2(xc.interval(1.0, 0.1, z=1.0), (0.9, 1.1))
    for R, value in ((math.log(2), 0.001823157), (0.5, 0.001315130), (1.0, 0.002630260)):
        h = xc.hoeffding(R, 2**20, 1e-6)
        assert math.isclose(h, R * math.sqrt(math.log(2e6) / 2**21), rel_tol=1e-12)
        assert abs(h - value) <= 2e-9


def test_p3_p4_a3_labels():  # 8.4 test 12; 5.6 with z = 2.576 and tau = 1e-12
    assert xc.p3_label(0.2, 0.01) == "PASS"
    assert xc.p3_label(0.11, 0.0038) == "PASS"  # L99 = 0.1002112
    assert xc.p3_label(0.11, 0.0040) == "THRESHOLD_INCONCLUSIVE"  # L99 = 0.099696
    assert xc.p3_label(0.05, 0.01) == "FAIL"  # U99 = 0.07576 < 0.10
    assert xc.p3_label(0.10 + 2e-12, 0.0) == "PASS"
    assert xc.p3_label(0.10 + 5e-13, 0.0) == "THRESHOLD_INCONCLUSIVE"  # L99 >= 0.10, L99 - tau not
    assert xc.p3_label(0.10, 0.0) == "THRESHOLD_INCONCLUSIVE"  # U99 = 0.10 is not < 0.10
    assert xc.p3_label(0.10 - 1e-9, 0.0) == "FAIL"
    assert xc.p4_label(0.05, 0.001, 0.3, 0.002) == "PASS"  # U99(I8) 0.052576 <= 0.147424
    assert xc.p4_label(0.2, 0.001, 0.3, 0.002) == "FAIL"  # L99(I8) 0.197424 > 0.152576
    assert xc.p4_label(0.15, 0.001, 0.3, 0.002) == "THRESHOLD_INCONCLUSIVE"
    assert xc.p4_label(0.14, 0.004, 0.3, 0.004) == "THRESHOLD_INCONCLUSIVE"  # separate bounds
    assert xc.p4_label(0.125, 0.0, 0.25, 0.0) == "PASS"  # equality passes (<=)
    assert xc.a3_label(0.05, 0.005) == "NONADDITIVE"  # L99 = 0.03712
    assert xc.a3_label(0.05, 0.01) == "ADDITIVE"  # L99 = 0.02424
    assert xc.a3_label(0.03, 0.0) == "NONADDITIVE" and xc.a3_label(0.0, 0.0) == "ADDITIVE"
def test_scientific_outcome():  # 5.9
    for p3 in ("PASS", "FAIL", "THRESHOLD_INCONCLUSIVE"):
        for p4 in ("PASS", "FAIL", "THRESHOLD_INCONCLUSIVE"):
            for a3 in ("NONADDITIVE", "ADDITIVE"):
                go = p3 == p4 == "PASS"
                exp = ("GO_P1_" + a3) if go else "STOP_P1"
                assert xc.scientific_outcome(p3, p4, a3) == exp, (p3, p4, a3)
def _st(bad: str | None = None, status: str = "FAIL", after: str = "NOT_RUN") -> dict:
    out, hit = {}, False
    for g in GATES:
        hit = hit or g == bad
        out[g] = status if g == bad else (after if hit else "PASS")
    return out
def test_validity_rule():  # 5.9, 5.10; API validity()
    cases = [(_st(), ("PASS", None)), (_st("PF"), ("INVALID", "PF")),
             (_st("PF", "NOT_RUN"), ("INVALID", "PF")), (_st("S0"), ("INVALID", "S0")),
             (_st("G0", "INVALID"), ("INVALID", "G0")), (_st("G2", "NOT_RUN"), ("INVALID", "G2")),
             (_st("G3"), ("FAIL", "G3")), (_st("G4"), ("FAIL", "G4")), (_st("G5"), ("FAIL", "G5")),
             (_st("G5", "INVALID"), ("INVALID", "G5")),
             (_st("G1", after="PASS") | {"G4": "INVALID"}, ("FAIL", "G1"))]
    for statuses, expected in cases:
        assert tuple(xp.validity(statuses)) == expected, statuses
def test_released_and_withheld_labels():  # 5.0 sealing; S3 for G5
    labels = {"P3": "PASS", "P4": "PASS", "A3": "NONADDITIVE", "outcome": "GO_P1_NONADDITIVE",
              "Q1": "PASS", "Q2": "NOT_SEPARATED"}
    def pick(verdict, first):
        out = xp.released(verdict, first, dict(labels))
        return {k: out[k] for k in labels}
    assert pick("PASS", None) == labels
    assert pick("FAIL", "G5") == dict.fromkeys(labels, "WITHHELD")
    for verdict, first in (("FAIL", "G3"), ("FAIL", "G4"), ("INVALID", "PF"), ("INVALID", "S0")):
        assert pick(verdict, first) == dict.fromkeys(labels, "NOT_RUN"), (verdict, first)
def test_q1_and_q2_outcomes():  # 7.5, RC 9; INVALID takes precedence
    assert xp.q1_outcome(7, 7, 6) == "PASS" and xp.q1_outcome(8, 8, 0) == "PASS"
    assert xp.q1_outcome(8, 7, 7) == "NON_SPECIFIC" and xp.q1_outcome(8, 8, 8) == "NON_SPECIFIC"
    assert xp.q1_outcome(6, 8, 0) == "FAIL" and xp.q1_outcome(8, 6, 8) == "FAIL"
    assert xp.q1_outcome(8, 8, 0, invalid=True) == "INVALID"
    assert xp.q2_outcome(8, 7, 0) == "SEPARATED_FULL_ONLY" and xp.q2_outcome(7, 8, 0) == (
        "SEPARATED_FULL_ONLY")
    assert xp.q2_outcome(7, 0, 7) == "SEPARATED_BOTH" and xp.q2_outcome(8, 1, 7) == (
        "SEPARATED_BOTH")
    assert xp.q2_outcome(8, 6, 2) == "WINDOW_UNRESOLVED" and xp.q2_outcome(7, 3, 5) == (
        "WINDOW_UNRESOLVED")
    for counts in ((6, 8, 0), (6, 0, 8), (0, 0, 0)):
        assert xp.q2_outcome(*counts) == "NOT_SEPARATED", counts
    for counts in ((8, 8, 0), (8, 0, 8), (8, 6, 2), (0, 0, 0)):
        assert xp.q2_outcome(*counts, invalid=True) == "INVALID", counts


def test_band_select_plateau_intersection():  # 8.4 test 11; 7.3 K1
    d1 = rows((0, 0, INF), (0, 0, 0.3), (1, 0.4, 0.9), (1, 0.45, 0.85))  # S = [0.45, 0.85)
    d2 = rows((0, 0, INF), (0, 0, 0.2), (1, 0.5, 0.95), (1, 0.35, 0.8))  # S = [0.5, 0.8)
    d3 = rows((0, 0, INF), (1, 0.2, 0.75), (1, 0.25, 0.625), (1, 0.625, 0.9))  # S = [0.25, 0.75)
    out = xp.band_select([d1, d2, d3])
    assert out["status"] == "OK" and approx2(out["interval"], (0.5, 0.75))
    assert approx2(out["band"], (0.5625, 0.6875))  # the central half
    assert np.allclose(np.asarray(out["S"], dtype=float).reshape(-1, 2), [[0.5, 0.75]],
                       rtol=0, atol=1e-12)
def test_band_select_longest_tie_width_and_beta0():  # 8.4 test 11; 7.3 steps 2-5
    base = (0, 0, INF)
    longest = rows(base, (1, 0.125, 0.625), (1, 0.125, 0.25), (1, 0.375, 0.625))
    out = xp.band_select([longest])  # S = [0.125, 0.25) u [0.375, 0.625)
    assert out["status"] == "OK" and approx2(out["interval"], (0.375, 0.625))
    assert approx2(out["band"], (0.4375, 0.5625))
    tie = rows(base, (1, 0.125, 0.625), (1, 0.125, 0.25), (1, 0.5, 0.625))
    out = xp.band_select([tie])  # equal widths 0.125: the smaller l wins
    assert out["status"] == "OK" and approx2(out["interval"], (0.125, 0.25))
    assert approx2(out["band"], (0.15625, 0.21875))
    assert np.allclose(np.asarray(out["S"], dtype=float).reshape(-1, 2),
                       [[0.125, 0.25], [0.5, 0.625]], rtol=0, atol=1e-12)
    narrow = rows(base, (1, 0.5, 0.5625), (1, 0.5, 0.75))  # width 0.0625 < 0.08
    out = xp.band_select([narrow])
    assert out["status"] == "CALIBRATION_INCONCLUSIVE" and out["band"] is None
    out = xp.band_select([narrow], min_width=0.05)
    assert out["status"] == "OK" and approx2(out["interval"], (0.5, 0.5625))
    wide = rows(base, (1, 0.5, 0.59375), (1, 0.5, 0.75))  # width 0.09375 >= 0.08
    assert xp.band_select([wide])["status"] == "OK"
    out = xp.band_select([rows(base, (1, 0.25, 0.75))])  # beta1 never 2: S is empty
    assert out["status"] == "CALIBRATION_INCONCLUSIVE"
    assert out["interval"] is None and out["band"] is None
    two_h0 = rows(base, (0, 0, 0.25), (1, 0.125, 0.5), (1, 0.125, 0.5))  # beta0 = 2 below 0.25
    out = xp.band_select([two_h0])
    assert out["status"] == "OK" and approx2(out["interval"], (0.25, 0.5))
def test_betti_at_beta1_band_and_k2():  # 7.2 H1 spanning rule; 7.3 K2
    r = rows((0, 0, INF), (0, 0, 0.5), (1, 0.25, 0.5))
    assert [xp.betti_at(r, 0, t) for t in (0.25, 0.5, 5.0)] == [2, 1, 1]
    assert [xp.betti_at(r, 1, t) for t in (0.1, 0.25, 0.5)] == [0, 1, 0]
    r = rows((0, 0, INF), (0, 0.25, 1.0), (1, 0.5, 0.75), (1, 0.5, 0.8), (1, 0.55, 0.9),
             (1, 0.25, 1.0), (1, 0.6, 0.7))
    assert xp.beta1_band(r, (0.5, 0.75)) == 2  # birth <= inf B and death > sup B, H1 only
    k2 = xp.k2_check(rows((0, 0, INF), (0, 0, 3.0), (1, 1.0, 4.0), (1, 1.0, 4.0),
                          *[(1, 1.0, 1.41421356)] * 3))
    assert k2["n_bars"] == 2 and bool(k2["ok"])
    k3 = xp.k2_check(rows((0, 0, INF), (1, 1.0, 4.0), (1, 1.0, 4.0), (1, 1.0, 2.0)))
    assert k3["n_bars"] == 3 and not k3["ok"]  # persistence exactly 1.0 counts
def test_clusters_count_original_points_through_dedup_map():  # 7.2 H0 reading; 10.2 C23
    xs = np.array([0.0, 0.25, 4.0])  # three deduplicated representatives on a line
    D, dmap = np.abs(xs[:, None] - xs[None, :]), np.repeat([0, 1, 2], [20, 10, 30])
    out = xp.clusters_at(D, 0.5, dmap)
    lab = np.asarray(out["labels"])
    assert out["count"] == 2 and lab.shape == (60,) and sorted(set(lab.tolist())) == [0, 1]
    assert len(set(lab[:30].tolist())) == 1 and len(set(lab[30:].tolist())) == 1
    assert lab[0] != lab[30] and out["retained_fraction"] == pytest.approx(1.0)
    assert xp.clusters_at(D, 0.25, dmap)["count"] == 2  # an MST edge of exactly h is not cut
    out = xp.clusters_at(D, 0.125, dmap)  # sizes 20, 10, 30: only the 30-point cluster is kept
    lab = np.asarray(out["labels"])
    assert out["count"] == 1 and np.all(lab[:30] == -1) and np.all(lab[30:] == 0)
    assert out["retained_fraction"] == pytest.approx(0.5)
    dmap = np.repeat([0, 1, 2], [20, 10, 25])  # 25 < 26 original points: not retained
    out = xp.clusters_at(D, 0.5, dmap)
    lab = np.asarray(out["labels"])
    assert out["count"] == 1 and np.all(lab[30:] == -1) and np.all(lab[:30] == 0)
    assert out["retained_fraction"] == pytest.approx(30 / 55)
    assert xp.clusters_at(D, 0.5, dmap, min_size=25)["count"] == 2
def test_split_check():  # 7.5 Q2 purity rule
    lab = np.array([0] * 20 + [1] * 20 + [-1] * 5)
    out = xp.split_check(lab, np.array([0] * 19 + [1] + [1] * 20 + [0] * 5))
    assert out["split"] and out["purity"] == pytest.approx(0.95)
    out = xp.split_check(lab, np.array([0] * 18 + [1] * 2 + [1] * 20 + [0] * 5))
    assert not out["split"] and out["purity"] == pytest.approx(0.9)
    assert not xp.split_check(lab, np.array([0] * 35 + [1] * 5 + [1] * 5))["split"]  # same label
    out = xp.split_check(np.array([0] * 40 + [-1] * 5), np.array([0] * 20 + [1] * 25))
    assert not out["split"] and out["purity"] == 0.0
    out = xp.split_check(np.repeat([0, 1, 2], 10), np.repeat([0, 1, 0], 10))
    assert not out["split"] and out["purity"] == 0.0
def test_h0_star():  # 7.4 K3
    xh = [rows((0, 0, 0.1), (0, 0, 0.3), (0, 0, INF), (1, 0.6, 0.9)),  # the H1 bar is ignored
          rows((0, 0, 0.5), (0, 0, INF))]
    x1 = [rows((0, 0, 0.2), (0, 0, 0.4), (0, 0, 1.0), (0, 0, INF)),  # second-largest finite
          rows((0, 0, 0.25), (0, 0, 1.0), (0, 0, INF))]
    out = xp.h0_star(xh, x1)  # m = max(0.3, 0.4, 0.5, 0.25)
    assert out["m"] == pytest.approx(0.5) and out["ok"] and out["h0"] == pytest.approx(0.75)
    one_inf = rows((0, 0, 1.0), (0, 0, INF))
    out = xp.h0_star([rows((0, 0, 0.1), (0, 0, INF))], [np.vstack((rows((0, 0, 0.6)), one_inf))])
    assert out["m"] == pytest.approx(0.6) and out["ok"] and out["h0"] == pytest.approx(0.8)
    out = xp.h0_star([rows((0, 0, 0.96), (0, 0, INF))], [np.vstack((rows((0, 0, 0.2)), one_inf))])
    assert out["m"] == pytest.approx(0.96) and not out["ok"]  # 1 - m = 0.04 is not > 0.05


def test_run_with_failed_preflight_is_invalid(tmp_path):  # 5.1 PF; 5.10; registry after run
    before = dict(WORLD_REGISTRY)
    report = xp.run(tmp_path, {"regression_suites": False})
    assert report["verdict"] == "INVALID" and report["first_failed"] == "PF"
    st = {str(k): (v["status"] if isinstance(v, dict) else v) for k, v in report["gates"].items()}
    assert st["PF"] != "PASS" and all(st[g] == "NOT_RUN" for g in GATES[1:]), st
    written = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert written["verdict"] == "INVALID"
    assert dict(WORLD_REGISTRY) == before
