"""Author A (job 0198): the exact conditional prefix sampler (protocol §2.1, Lemma P0, §5.1
KS-PAIR; DRO2). Expected values are computed here, independently, by exact enumeration in
Fractions on the CONTRACT_OF ``dry_run.ks_pair_chain`` (non-reversible, L = 8, suffix 4)."""

from __future__ import annotations  # noqa: I001

import itertools
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_pairs as up  # noqa: E402
import c1_records  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
from topo_pilot.dataset import sampler as tsampler  # noqa: E402

L, S = 8, 4
P = L - S
SAMPLER = "FAIL_TECHNICAL/SAMPLER"


def _chain():
    c = uc.CONTRACT["dry_run"]["ks_pair_chain"]
    TF = [[Fraction(x) for x in row] for row in c["T"]]
    EF = [[Fraction(x) for x in row] for row in c["E"]]
    PF = [Fraction(x) for x in c["pi"]]
    assert (c["L"], c["suffix_len"]) == (L, S)
    return TF, EF, PF


TF, EF, PF = _chain()
NS, V = len(PF), len(EF[0])


def obj(m):
    return np.array(m, dtype=object)


def flt(m):
    return np.array([[float(x) for x in r] for r in m]) if isinstance(m[0], list) else \
        np.array([float(x) for x in m])


def joint_law(T, E, pi, length):
    """P(w_1..w_length) for every word, exact forward recursion (no backward message)."""
    out = {}
    for w in itertools.product(range(V), repeat=length):
        a = [pi[z] * E[z][w[0]] for z in range(NS)]
        for t in range(1, length):
            a = [sum(a[y] * T[y][z] for y in range(NS)) * E[z][w[t]] for z in range(NS)]
        out[w] = sum(a)
    return out


JOINT = joint_law(TF, EF, PF, L)
SUFFIXES = list(itertools.product(range(V), repeat=S))
PREFIXES = list(itertools.product(range(V), repeat=P))
P_S = {s: sum(JOINT[p + s] for p in PREFIXES) for s in SUFFIXES}
COND = {s: {p: JOINT[p + s] / P_S[s] for p in PREFIXES} for s in SUFFIXES}


def implied_law(bridge, T_rev, E):
    """API §2.1: Σ_{z1..zP} bridge[zP] Π E[z_t, w'_t] Π_{t=2..P} T_rev[z_t, z_{t-1}]."""
    law = {}
    for p in PREFIXES:
        tot = Fraction(0)
        for zs in itertools.product(range(NS), repeat=P):
            v = Fraction(bridge[zs[-1]])
            for t in range(P):
                v *= E[zs[t]][p[t]]
            for t in range(1, P):
                v *= T_rev[zs[t]][zs[t - 1]]
            tot += v
        law[p] = tot
    return law


def my_beta(s):
    """β_P(z) = P(w_{P+1..L} = s | z_P = z), by direct enumeration of z_{P+1..L}."""
    out = []
    for z in range(NS):
        tot = Fraction(0)
        for zs in itertools.product(range(NS), repeat=S):
            v, prev = Fraction(1), z
            for t in range(S):
                v *= TF[prev][zs[t]] * EF[zs[t]][s[t]]
                prev = zs[t]
            tot += v
        out.append(tot)
    return out


def my_time_reversal(T, pi):
    return [[pi[zp] * T[zp][z] / pi[z] for zp in range(NS)] for z in range(NS)]


def status_of_raise(fn, *a, **k):
    with pytest.raises(c1_records.C1GateFailure) as ei:
        fn(*a, **k)
    return ei.value.status


# ---- (a) time reversal and check_process -----------------------------------------------------
def test_time_reversal_exact_and_differs_from_T():
    got = up.time_reversal(obj(TF), obj(PF))
    want = my_time_reversal(TF, PF)
    for z in range(NS):
        for zp in range(NS):
            assert isinstance(got[z, zp], Fraction)
            assert got[z, zp] == want[z][zp]
    assert any(got[z, zp] != TF[z][zp] for z in range(NS) for zp in range(NS))  # non-reversible
    gf = up.time_reversal(flt(TF), flt(PF))
    assert gf.dtype == np.float64
    assert np.allclose(gf, flt(want), rtol=0, atol=1e-15)


def test_check_process_accepts_chain_and_refuses_bad_pi():
    up.check_process(flt(TF), flt(EF), flt(PF))
    assert up.stationarity_error(flt(TF), flt(PF)) <= 1e-12
    bad = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
    # πT = (1/4, 7/16, 5/16): max |πT − π| = 1/4 (hand computation)
    assert up.stationarity_error(obj(TF), obj(bad)) == 0.25
    assert status_of_raise(up.check_process, flt(TF), flt(EF), flt(bad)) == SAMPLER
    zero = np.array([0.0, 0.5, 0.5])
    assert status_of_raise(up.check_process, flt(TF), flt(EF), zero) == SAMPLER


# ---- (b) implied prefix law = brute-force Bayes conditional, exactly -------------------------
def test_backward_messages_and_bridge_exact():
    for s in SUFFIXES:
        row = np.array([[0] * P + list(s)])
        beta = up.backward_messages(obj(TF), obj(EF), row, S)[0]
        assert list(beta) == my_beta(s)
        br = up.bridge(obj(PF), np.array([beta], dtype=object))[0]
        w = [PF[z] * my_beta(s)[z] for z in range(NS)]
        assert list(br) == [x / sum(w) for x in w]


@pytest.mark.parametrize("s", SUFFIXES)
def test_implied_prefix_law_equals_bayes_conditional(s):
    k = up.prefix_kernels(obj(TF), obj(EF), obj(PF), list(s), P)
    assert all(isinstance(x, Fraction) for x in k["bridge"])
    law = implied_law(list(k["bridge"]), k["T_rev"].tolist(), k["E"].tolist())
    assert law == COND[s]
    assert sum(law.values()) == 1


def test_arm2_marginal_equals_process_law():
    """(c) Σ_s P(s)·P_impl(prefix | s) = P(w_1..w_8) for every word (Lemma P0 (i))."""
    for s in SUFFIXES:
        k = up.prefix_kernels(obj(TF), obj(EF), obj(PF), list(s), P)
        law = implied_law(list(k["bridge"]), k["T_rev"].tolist(), k["E"].tolist())
        for p in PREFIXES:
            assert P_S[s] * law[p] == JOINT[p + s]


def test_planted_defective_samplers_are_caught():
    """(d) T in place of T~, and π in place of the bridge (β dropped): each fails (b)."""
    TR = my_time_reversal(TF, PF)
    wrong_T = wrong_beta = False
    for s in SUFFIXES:
        b = my_beta(s)
        br = [PF[z] * b[z] / sum(PF[y] * b[y] for y in range(NS)) for z in range(NS)]
        wrong_T |= implied_law(br, TF, EF) != COND[s]
        wrong_beta |= implied_law(PF, TR, EF) != COND[s]
        assert implied_law(br, TR, EF) == COND[s]  # the correct test-side kernels agree
    assert wrong_T and wrong_beta


# ---- (e) Monte Carlo against the exact law ---------------------------------------------------
def test_sample_prefix_frequencies_within_4se():
    rows = [(1, 1, 0, 0, 0, 1, 1, 0), (0, 0, 1, 1, 1, 0, 1, 1)]
    n = 100_000
    arm1 = np.repeat(np.array(rows, dtype=np.uint8), n, axis=0)
    rng = np.random.Generator(np.random.PCG64(19801))
    arm2 = up.sample_prefix(flt(TF), flt(EF), flt(PF), arm1, rng)
    assert arm2.dtype == arm1.dtype and arm2.shape == arm1.shape
    assert np.array_equal(arm2[:, P:], arm1[:, P:])
    assert up.suffix_equal(arm1, arm2).all()
    for g, r in enumerate(rows):
        block = arm2[g * n:(g + 1) * n, :P].astype(np.int64)
        code = block @ (V ** np.arange(P - 1, -1, -1))
        counts = np.bincount(code, minlength=V ** P)
        for p in PREFIXES:
            pr = float(COND[tuple(r[P:])][p])
            c = int(np.dot(p, V ** np.arange(P - 1, -1, -1)))
            se = (pr * (1 - pr) / n) ** 0.5
            assert abs(counts[c] / n - pr) <= 4 * se, (g, p)
        assert not np.array_equal(block, np.tile(np.array(r[:P]), (n, 1)))


# ---- (f) the frozen draw order --------------------------------------------------------------
def _replay(T, E, pi, arm1, rng):
    """API §2.2, step by step, with test-side float kernels."""
    n = arm1.shape[0]
    beta = np.ones((n, NS))
    for t in range(L - 1, P - 1, -1):
        beta = (E[:, arm1[:, t].astype(np.int64)].T * beta) @ T.T
    w = pi[None, :] * beta
    B = w / w.sum(axis=1, keepdims=True)
    Tr = (pi[None, :] * T.T) / pi[:, None]
    cumE, cumR = tsampler._cumulative_rows(E), tsampler._cumulative_rows(Tr)
    z = tsampler._draw(tsampler._cumulative_rows(B), np.arange(n), rng.random(n))
    out = arm1.copy()
    for t in range(P, 0, -1):
        out[:, t - 1] = tsampler._draw(cumE, z, rng.random(n))
        if t > 1:
            z = tsampler._draw(cumR, z, rng.random(n))
    return out


def test_draw_order_and_uniform_count():
    n = 257
    g0 = np.random.Generator(np.random.PCG64(7))
    arm1 = g0.integers(0, V, size=(n, L)).astype(np.uint8)
    rng = np.random.Generator(np.random.PCG64(4242))
    arm2 = up.sample_prefix(flt(TF), flt(EF), flt(PF), arm1, rng)
    ref = np.random.Generator(np.random.PCG64(4242))
    ref.random(n * (1 + P + (P - 1)))
    assert rng.bit_generator.state == ref.bit_generator.state
    again = _replay(flt(TF), flt(EF), flt(PF), arm1, np.random.Generator(np.random.PCG64(4242)))
    assert np.array_equal(arm2, again)
    assert uc.CONTRACT["sizes"]["uniforms_per_arm2_row"] == 1 + 28 + 27


def test_rows_are_paired_by_index_not_sorted():
    g0 = np.random.Generator(np.random.PCG64(8))
    arm1 = g0.integers(0, V, size=(64, L)).astype(np.uint8)
    rng = np.random.Generator(np.random.PCG64(9))
    arm2 = up.sample_prefix(flt(TF), flt(EF), flt(PF), arm1, rng)
    assert np.array_equal(arm2[:, P:], arm1[:, P:])  # row i pairs with row i


# ---- (g) zero-probability columns, (h) impossible suffixes ------------------------------------
E_ZERO = [[0.75, 0.0, 0.25], [0.25, 0.0, 0.75], [0.2, 0.0, 0.8]]


def test_zero_probability_column_never_drawn():
    E = np.array(E_ZERO)
    g0 = np.random.Generator(np.random.PCG64(10))
    arm1 = (2 * g0.integers(0, 2, size=(20_000, L))).astype(np.uint8)  # symbols 0 and 2 only
    arm2 = up.sample_prefix(flt(TF), E, flt(PF), arm1, np.random.Generator(np.random.PCG64(11)))
    assert not np.any(arm2 == 1)
    assert set(np.unique(arm2[:, :P])) == {0, 2}


def test_bridge_refuses_impossible_suffix():
    beta = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
    assert status_of_raise(up.bridge, flt(PF), beta) == SAMPLER
    arm1 = np.array([[0, 0, 0, 0, 0, 1, 0, 2]], dtype=np.uint8)  # symbol 1 has probability 0
    st = status_of_raise(up.sample_prefix, flt(TF), np.array(E_ZERO), flt(PF), arm1,
                         np.random.Generator(np.random.PCG64(1)))
    assert st == SAMPLER


def test_suffix_equal_flags_a_changed_suffix_cell():
    a1 = np.zeros((5, L), dtype=np.uint8)
    a2 = a1.copy()
    a2[:, 0] = 1  # prefix changes are allowed
    a2[3, L - 1] = 1
    assert up.suffix_equal(a1, a2).tolist() == [True, True, True, False, True]


def test_float_kernels_match_exact_kernels():
    for s in SUFFIXES[::5]:
        kf = up.prefix_kernels(flt(TF), flt(EF), flt(PF), list(s), P)
        ko = up.prefix_kernels(obj(TF), obj(EF), obj(PF), list(s), P)
        for key in ("beta", "bridge", "T_rev"):
            exact = np.array(ko[key].tolist(), dtype=np.float64)
            assert np.allclose(np.asarray(kf[key], dtype=np.float64), exact, rtol=1e-14, atol=0)
