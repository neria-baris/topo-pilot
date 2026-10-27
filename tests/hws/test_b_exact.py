"""Author B (job 0119), TEST_PLAN §3 `test_b_exact.py`: p_D2a against brute force (tiny world,
tiny rational HMM by Fractions), the E4 boundary, symbol law, A_eff, mean last-symbol entropy,
the K <= 3 suffix enumeration, the Decimal and BayesFilter spot checks (pass on the correct world,
fail when one side sees a perturbed E), the tier-0 law report (RC-3, DR13) and `exact_world`.
Protocol §2.4, §2.6, §5.1 E4, §8; DR6, DR13; KC9, KC10.

Written without reading tools/hws/*.py. Every expected value is computed independently here."""

from __future__ import annotations

import decimal
import itertools
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hws") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hws"))

import hws_worlds as hw  # noqa: E402
import hws_exact as he  # noqa: E402

import error_bound  # noqa: E402
import process_law  # noqa: E402
from topo_pilot.contracts import ErrorCode, StageFailure  # noqa: E402
from topo_pilot.oracle import BayesFilter  # noqa: E402
from topo_pilot.process import TransitionBuilder  # noqa: E402

TAU = F(1, 2000000)
# tiny rational HMM: dyadic entries, so the float arrays are the exact law
T_Q = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
E_Q = [[F(1, 2), F(1, 4), F(1, 4)], [F(1, 8), F(1, 8), F(3, 4)]]
PI_Q = [F(1, 2), F(1, 2)]


def _f(m):
    return np.array([[float(v) for v in row] for row in m]) if isinstance(m[0], list) \
        else np.array([float(v) for v in m])


def _forward(T, E, pi, hist):
    a = pi * E[:, hist[0]]
    for w in hist[1:]:
        a = (a @ T) * E[:, w]
    return a


def _forward_q(hist):
    a = [PI_Q[z] * E_Q[z][hist[0]] for z in range(2)]
    for w in hist[1:]:
        a = [sum(a[s] * T_Q[s][t] for s in range(2)) * E_Q[t][w] for t in range(2)]
    return sum(a)


def _perturbed(E):
    Ep = np.array(E, dtype=np.float64, copy=True)
    Ep[:, 0] *= 1.5
    return Ep / Ep.sum(axis=1, keepdims=True)


@pytest.fixture(scope="module")
def tiny():
    return hw.build_tiny()


@pytest.fixture(scope="module")
def w0():
    return hw.build_process(hw.W0)


# --------------------------------------------------------------------------- p_D2a, E4

@pytest.mark.parametrize("alphabet", [(0,), (0, 1), (1, 2)])
def test_p_d2a_equals_brute_force_on_the_tiny_world(tiny, alphabet):
    T, E, pi = tiny["T"], tiny["E"], tiny["pi"]
    brute = sum(_forward(T, E, pi, h).sum() for h in itertools.product(alphabet, repeat=8))
    got = he.p_d2a(T, E, pi, alphabet=alphabet, Lh=8)
    assert isinstance(got, float) and abs(got - brute) <= 1e-15


def test_p_d2a_full_alphabet_and_symbols_beyond_v(tiny):
    T, E, pi = tiny["T"], tiny["E"], tiny["pi"]
    full = he.p_d2a(T, E, pi, alphabet=(0, 1, 2), Lh=8)
    assert abs(full - 1.0) <= 1e-13
    assert abs(he.p_d2a(T, E, pi, alphabet=(0, 1, 2, 3, 4), Lh=8) - full) <= 1e-15
    assert abs(he.p_d2a(T, E, pi, alphabet=(0, 3, 4), Lh=8)
               - he.p_d2a(T, E, pi, alphabet=(0,), Lh=8)) <= 1e-15


@pytest.mark.parametrize("alphabet, Lh", [((0, 1), 6), ((2,), 5), ((0,), 7)])
def test_p_d2a_equals_exact_fractions_on_a_rational_hmm(alphabet, Lh):
    exact = sum(_forward_q(h) for h in itertools.product(alphabet, repeat=Lh))
    got = he.p_d2a(_f(T_Q), _f(E_Q), _f(PI_Q), alphabet=alphabet, Lh=Lh)
    assert abs(F(got) - exact) <= F(1, 10**15) * max(exact, F(1, 10**3))


def test_e4_boundary():
    assert he.e4_check(TAU)["status"] == "PASS"  # DR6 planted value Fraction(1, 2000000)
    x = float(TAU)
    assert F(x) <= TAU  # 1/2000000 = 1.048576 * 2**-21 rounds down (mantissa remainder .21)
    up = float(np.nextafter(x, 1.0))
    assert F(up) > TAU
    assert he.e4_check(x)["status"] == "PASS"
    assert he.e4_check(up)["status"] == "INELIGIBLE/E4"
    assert he.e4_check(x)["p_D2a"] == x
    t2 = F(1, 2**21)  # an exactly representable threshold: equality passes
    assert he.e4_check(2.0**-21, tau=t2)["status"] == "PASS"
    assert he.e4_check(float(np.nextafter(2.0**-21, 1.0)), tau=t2)["status"] == "INELIGIBLE/E4"
    assert he.e4_check(0.0)["status"] == "PASS"


# ------------------------------------------------------- symbol law, A_eff, entropy, KC9

def _direct_entropy(T, E, pi):
    p = np.array([sum(pi[z] * E[z, w] for z in range(len(pi))) for w in range(E.shape[1])])
    H = 0.0
    for w in range(E.shape[1]):
        r = [pi[z] * E[z, w] / p[w] for z in range(len(pi))]
        H += p[w] * -sum(v * math.log(v) for v in r if v > 0)
    return p, H


def test_symbol_law_aeff_and_last_entropy_direct(tiny):
    T, E, pi = tiny["T"], tiny["E"], tiny["pi"]
    p, H = _direct_entropy(T, E, pi)
    np.testing.assert_allclose(he.symbol_law(tiny), p, rtol=0, atol=1e-15)
    assert abs(he.mean_last_entropy(tiny) - H) <= 1e-12
    assert abs(he.a_eff(tiny) - math.exp(H)) <= 1e-12
    post = he.last_symbol_posteriors(tiny)
    assert post.shape == (E.shape[1], len(pi))
    for w in range(E.shape[1]):
        np.testing.assert_allclose(post[w], pi * E[:, w] / p[w], rtol=0, atol=1e-15)


def test_aeff_on_known_zero_worlds():
    U, N = hw.build_known_zero("U"), hw.build_known_zero("N")
    assert abs(he.a_eff(U) - 1.0) <= 1e-12 and abs(he.mean_last_entropy(U)) <= 1e-12
    assert abs(he.mean_last_entropy(N) - math.log(144)) <= 1e-12
    assert abs(he.a_eff(N) - 144.0) <= 1e-9


def test_suffix_enumeration_against_brute_force(tiny):
    T, E, pi, c = tiny["T"], tiny["E"], tiny["pi"], tiny["features"]
    out = he.suffix_enumeration(tiny, Ks=(1, 2, 3))
    V = E.shape[1]
    for K in (1, 2, 3):
        Em = EH = tot = 0.0
        for s in itertools.product(range(V), repeat=K):
            a = _forward(T, E, pi, s)
            P = a.sum()
            b = a / P
            m = b @ c
            q = (b @ T) @ E
            Em += P * float(m @ m)
            EH += P * float(-np.sum(q * np.log(q)))
            tot += P
        assert abs(tot - 1.0) <= 1e-12
        assert out[K]["n_suffixes"] == V**K
        assert abs(out[K]["E_m_sq"] - Em) <= 1e-12
        assert abs(out[K]["E_Hq"] - EH) <= 1e-12


# ------------------------------------------------------------------- KC10 / S3 spot checks

def test_decimal_spot_check_passes_and_detects_a_perturbed_e(w0, monkeypatch):
    tok = ((np.arange(32) * 5 + 3) % 36).astype(np.uint8).reshape(1, 32)
    ok = he.decimal_spot_check(w0, tok, (4,))
    assert bool(ok["pass"]) and F(ok["max_gap"]) <= error_bound.MOMENT_TOL_EXACT
    orig = error_bound._reference_posterior
    Ep = _perturbed(w0["E"])
    monkeypatch.setattr(error_bound, "_reference_posterior",
                        lambda T, E, pi, suffix: orig(T, Ep, pi, suffix))
    bad = he.decimal_spot_check(w0, tok, (4,))
    assert not bool(bad["pass"]) and F(bad["max_gap"]) > error_bound.MOMENT_TOL_EXACT


def test_decimal_spot_check_is_w12_only(tiny):
    with pytest.raises(ValueError):
        he.decimal_spot_check(tiny, np.zeros((1, 32), dtype=np.uint8), (4,))


def test_bayes_cross_check_passes_and_detects_a_perturbed_e(tiny, monkeypatch):
    tok = ((np.arange(40 * 8).reshape(40, 8) * 7 + 1) % 3).astype(np.uint8)
    ok = he.bayes_cross_check(tiny, tok)
    assert bool(ok["pass"]) and ok["max_abs"] <= 1e-12
    orig = BayesFilter.__init__

    def init(self, T, E, pi):
        orig(self, T, _perturbed(E), pi)

    monkeypatch.setattr(BayesFilter, "__init__", init)
    bad = he.bayes_cross_check(tiny, tok)
    assert not bool(bad["pass"]) and bad["max_abs"] > 1e-12


# ------------------------------------------------------------------ tier-0 law report

@pytest.mark.parametrize("sigma", [F(3, 2), F(11, 8)])
def test_law_bound_report_nonterminating_logit(sigma):
    logit = F(1, 2) / (2 * sigma**2)  # squared distance 1/2 to the nearest centre
    den = logit.denominator
    for prime in (2, 5):
        while den % prime == 0:
            den //= prime
    assert den > 1  # the Decimal division cannot terminate (1/9 at 3/2, 16/121 at 11/8)
    before = dict(process_law.LAW)
    proc = hw.build_process(hw.World(12, 1, sigma, F(1, 5)))
    rep = he.law_bound_report(proc)
    assert rep["status"] == "UNAVAILABLE/NONTERMINATING_LOGIT"
    assert process_law.LAW == before


def test_law_bound_report_with_injected_enclosures():
    proc = hw.build_process(hw.World(12, 1, F(3, 2), F(1, 2)))
    before = dict(process_law.LAW)
    seen = {}

    def bounded(T, E, pi, coords):
        seen.update(sigma=process_law.LAW["sigma"], nb=process_law.LAW["neighbour"],
                    E=np.array_equal(E, proc["E"]), coords=np.array_equal(coords, proc["coords"]))
        return {"status": "BOUNDED", "Z_bound": "1/1000"}

    assert he.law_bound_report(proc, enclosure=bounded)["status"] == "BOUNDED"
    assert seen == {"sigma": F(3, 2), "nb": F(1, 8), "E": True, "coords": True}
    assert process_law.LAW == before

    def other(*args):
        raise RuntimeError("planted technical failure")

    with pytest.raises(RuntimeError):
        he.law_bound_report(proc, enclosure=other)
    assert process_law.LAW == before

    def inexact(*args):
        raise decimal.Inexact("planted")

    rep = he.law_bound_report(proc, enclosure=inexact)
    assert rep["status"] == "UNAVAILABLE/NONTERMINATING_LOGIT"
    assert process_law.LAW == before


# --------------------------------------------------------------------------- exact_world

EXACT_KEYS = {"p_v", "min_p", "A_eff", "mean_last_entropy", "p_D2a", "V", "n_A", "symmetry",
              "e1", "e2", "e3", "e4", "status", "tier", "changed", "distance"}


def test_exact_world_on_a_symmetric_cell():
    proc = hw.build_process(hw.World(8, 2, F(5, 4), F(1, 5)))
    ex = he.exact_world(proc)
    assert EXACT_KEYS <= set(ex)
    first = next((ex[k]["status"] for k in ("e1", "e2", "e3", "e4")
                  if ex[k]["status"] != "PASS"), "PASS")
    assert ex["e3"]["status"] == "INELIGIBLE/E3" and ex["status"] == first != "PASS"
    np.testing.assert_allclose(ex["p_v"], proc["pi"] @ proc["E"], rtol=0, atol=1e-15)
    assert ex["min_p"] == min(ex["p_v"])
    assert ex["V"] == 18 and ex["n_A"] == 3 and ex["tier"] == 2
    assert ex["changed"] == 2 and ex["distance"] == "2"
    assert ex["p_D2a"] == he.p_d2a(proc["T"], proc["E"], proc["pi"])
    assert abs(ex["A_eff"] - he.a_eff(proc)) <= 1e-12


def test_exact_world_identity_fields_at_w0(w0):
    ex = he.exact_world(w0)
    assert ex["tier"] == 0 and ex["changed"] == 0 and ex["distance"] == "0"
    assert ex["V"] == 36 and ex["n_A"] == 6 and ex["e3"]["status"] == "PASS"
    want = "PASS" if F(float(ex["p_D2a"])) <= TAU else "INELIGIBLE/E4"
    assert ex["e4"]["status"] == want


def test_exact_world_e1_carries_only_e1(monkeypatch):
    def boom(self, world, cfg):
        raise StageFailure(ErrorCode.INVALID_CONFIG, "test", "planted", "planted failure")

    monkeypatch.setattr(TransitionBuilder, "build", boom)
    ex = he.exact_world(hw.build_process(hw.World(16, 3, F(2), F(7, 8))))
    assert ex["status"] == "INELIGIBLE/E1" and ex["e1"]["status"] == "INELIGIBLE/E1"
    assert ex.get("e2") is None and ex.get("e4") is None
