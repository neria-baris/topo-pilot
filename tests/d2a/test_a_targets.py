"""Independent tests of tools/d2a/d2a_targets.py (job 0028, author A): T-FIX, T-SUPP, T-PRIOR and
the G0-NUM identities at small sampled batches. Written from D2A-FROZEN-v1 sections 3 and 5.2
and tools/d2a/API.md section 2.2 only, before the module existed.

References: d1_seam.exact_history / exact_model (Fractions), an independent Fraction J3 and
path enumeration written here, and the production BayesFilter run from explicit priors.
Batches are tiny (a few hundred episodes) and drawn from a test-only SeedTree master.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.oracle import BayesFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "d2a"), ("tools", "d1_seam"), ("tools", "x4_oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

import d1_seam  # noqa: E402
import d2a_targets as TG  # noqa: E402
import d2a_world as W  # noqa: E402

pytestmark = pytest.mark.oracle

S0, S2, S3, A, B = 0, 1, 2, 3, 4
FM = d1_seam.float_model()
EXACT = d1_seam.exact_model()
NAMED = {"h_star": d1_seam.H_STAR, "h_a": d1_seam.H_A, "h_b": d1_seam.H_B,
         "h_edge": d1_seam.H_EDGE, "h_max": d1_seam.H_MAX}
T_CC = np.block([[FM["T_C"], np.zeros((12, 12))], [np.zeros((12, 12)), FM["T_C"]]])


def _f(x):
    return np.array([float(v) for v in x], dtype=np.float64)


def _flat(J):
    return [v for row in J for v in row]


def _tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


def _at(h, proc="CM"):
    out = TG.oracle_at(np.array([h], dtype=np.uint8), len(h), proc)
    return {k: np.asarray(v, dtype=np.float64)[0] for k, v in out.items()}


def _exact_J3(b, T, E):
    """Independent Fraction J3[25 s1 + 5 s2 + s3] = b T diag(E s1) T diag(E s2) T E s3."""
    def step(v, s):
        return [sum((v[i] * T[i][j] for i in range(12)), Q(0)) * E[j][s] for j in range(12)]
    out = [Q(0)] * 125
    for s1 in range(5):
        v1 = step(b, s1)
        if not any(v1):
            continue
        for s2 in range(5):
            v2 = step(v1, s2)
            if any(v2):
                for s3 in range(5):
                    out[25 * s1 + 5 * s2 + s3] = sum(step(v2, s3), Q(0))
    return out


def _sample(n, T, name):
    sampler = HMMSampler(T, FM["E_mix"], FM["mu"], SequenceLayout())
    return sampler.sample(n, SeedTree(4242).generator("author_a", name))[0]


@pytest.fixture(scope="module")
def cm_tokens():
    return _sample(400, FM["T"], "cm")


# ---- T-FIX ---------------------------------------------------------------------------------
@pytest.mark.parametrize("name", list(NAMED))
def test_T_FIX_named_histories_match_exact(name):
    h = NAMED[name]
    e, o = d1_seam.exact_history(h), _at(h)
    for key in ("b_C", "b_M", "b_mix", "Q1", "Q1_C", "Q1_M"):
        assert np.max(np.abs(o[key] - _f(e[key]))) <= 1e-12, key
    assert np.max(np.abs(o["Q1_filter"] - _f(e["Q1"]))) <= 1e-12
    for key, ref in (("J2", "J"), ("J2_C", "J_C"), ("J2_M", "J_M")):
        assert o[key].shape == (25,)
        assert np.max(np.abs(o[key] - _f(_flat(e[ref])))) <= 1e-12, key
    assert abs(float(o["pi"]) - float(e["pi"])) <= 1e-11
    half = [(x + y) / 2 for x, y in zip(e["Q1_C"], e["Q1_M"])]
    assert np.max(np.abs(o["Q1_half"] - _f(half))) <= 1e-12
    j_half = [(x + y) / 2 for x, y in zip(_flat(e["J_C"]), _flat(e["J_M"]))]
    assert np.max(np.abs(o["J2_half"] - _f(j_half))) <= 1e-12
    t2 = [(e["pi"] - Q(1, 2)) * (y - x) for x, y in zip(_flat(e["J_C"]), _flat(e["J_M"]))]
    assert np.max(np.abs(o["T2"] - _f(t2))) <= 1e-12


@pytest.mark.parametrize("name", list(NAMED))
def test_T_FIX_three_step_laws_match_independent_fractions(name):
    h = NAMED[name]
    e, o = d1_seam.exact_history(h), _at(h)
    jc = _exact_J3(e["b_C"], EXACT["T_C"], EXACT["E_C"])
    jm = _exact_J3(e["b_M"], EXACT["T_M"], EXACT["E_M"])
    pi = e["pi"]
    assert np.max(np.abs(o["J3_C"] - _f(jc))) <= 1e-12
    assert np.max(np.abs(o["J3_M"] - _f(jm))) <= 1e-12
    j3 = _f([(1 - pi) * x + pi * y for x, y in zip(jc, jm)])
    t3 = _f([(pi - Q(1, 2)) * (y - x) for x, y in zip(jc, jm)])
    assert np.max(np.abs(o["J3"] - j3)) <= 1e-12 and np.max(np.abs(o["T3"] - t3)) <= 1e-12
    marg = [sum(jc[25 * i + 5 * j + k] for k in range(5)) for i in range(5) for j in range(5)]
    assert marg == _flat(e["J_C"])  # the reference itself is consistent with exact_history


def test_T_FIX_tv_values_of_g0_fix():
    hs, ha, hb = _at(d1_seam.H_STAR), _at(d1_seam.H_A), _at(d1_seam.H_B)
    he, hm = _at(d1_seam.H_EDGE), _at(d1_seam.H_MAX)

    def dist(j):
        return np.asarray(j).reshape(5, 5).sum(0)  # distant (second-symbol) marginal

    assert abs(_tv(hs["J2_C"], hs["J2_M"]) - 1 / 50) <= 1e-12
    assert abs(_tv(dist(hs["J2_C"]), dist(hs["J2_M"])) - 1 / 50) <= 1e-12
    assert abs(_tv(ha["J2"], hb["J2"]) - 1 / 100) <= 1e-12
    assert abs(_tv(he["Q1_C"], he["Q1_M"]) - 1 / 10) <= 1e-12
    assert abs(_tv(hm["J2_C"], hm["J2_M"]) - 3 / 200) <= 1e-12
    assert abs(_tv(dist(hm["J2_C"]), dist(hm["J2_M"])) - 1 / 100) <= 1e-12
    e = {k: d1_seam.exact_history(h) for k, h in NAMED.items()}
    assert d1_seam.tv(e["h_star"]["J_C"], e["h_star"]["J_M"]) == Q(1, 50)
    assert d1_seam.tv(e["h_a"]["J"], e["h_b"]["J"]) == Q(1, 100)
    assert d1_seam.tv(e["h_edge"]["Q1_C"], e["h_edge"]["Q1_M"]) == Q(1, 10)
    assert d1_seam.tv(e["h_max"]["J_C"], e["h_max"]["J_M"]) == Q(3, 200)
    assert d1_seam.tv(e["h_max"]["Q2dist_C"], e["h_max"]["Q2dist_M"]) == Q(1, 100)


def test_g0_fix_gate_passes():
    gate = TG.g0_fix()
    assert gate["status"] == "PASS"
    assert gate["checks"] and all(bool(v) for v in gate["checks"].values())


# ---- T-SUPP --------------------------------------------------------------------------------
def _read_strings(k):
    """Indices of k-symbol strings with a read (A/B), reachable with positive probability from
    some column-3 state (3, y) in either exact world (independent enumeration)."""
    found = set()
    for f in "CM":
        T, E = EXACT["T_" + f], EXACT["E_" + f]

        def rec(v, prefix, T=T, E=E):
            if len(prefix) == k:
                found.add(prefix)
                return
            for s in range(5):
                nxt = [sum((v[i] * T[i][j] for i in range(12)), Q(0)) * E[j][s]
                       for j in range(12)]
                if any(nxt):
                    rec(nxt, prefix + (s,))

        for y in range(3):
            rec([Q(int(i == 3 * 3 + y)) for i in range(12)], ())
    return sorted(sum(s * 5 ** (k - 1 - i) for i, s in enumerate(x)) for x in found
                  if A in x or B in x)


def test_T_SUPP_support_lists_equal_independent_enumeration():
    assert tuple(W.S2) == tuple(_read_strings(2)) == (3, 4, 8, 9)
    s3 = _read_strings(3)
    assert len(s3) == 24 and tuple(W.S3) == tuple(s3)


@pytest.mark.parametrize("t", [5, 16, 28, 31])
def test_T_SUPP_targets_vanish_off_support(t, cm_tokens):
    rows = np.flatnonzero(cm_tokens[:, t - 1] == S3)
    assert rows.size > 0
    o = TG.oracle_at(cm_tokens[rows], t)
    off2 = np.setdiff1d(np.arange(25), np.asarray(W.S2))
    off3 = np.setdiff1d(np.arange(125), np.asarray(W.S3))
    assert np.max(np.abs(np.asarray(o["T2"])[:, off2])) <= 1e-12
    assert np.max(np.abs(np.asarray(o["T3"])[:, off3])) <= 1e-12


# ---- G0-NUM identities on a small batch ----------------------------------------------------
@pytest.mark.parametrize("t", [3, 16, 28, 32])
def test_oracle_identities(t, cm_tokens):
    o = {k: np.asarray(v, dtype=np.float64) for k, v in TG.oracle_at(cm_tokens, t).items()}
    pi = o["pi"]
    assert np.max(np.abs(o["b_mix"] - np.hstack([(1 - pi)[:, None] * o["b_C"],
                                                  pi[:, None] * o["b_M"]]))) <= 1e-12
    assert np.max(np.abs(pi - o["b_mix"][:, 12:].sum(1))) <= 1e-12
    assert np.max(np.abs(pi - 1 / (1 + np.exp(o["logev_C"] - o["logev_M"])))) <= 1e-10
    assert np.max(np.abs(o["Q1"] - o["Q1_filter"])) <= 1e-12
    for key in ("J2", "J3"):
        assert np.max(np.abs(o[key].sum(1) - 1)) <= 1e-12
    assert np.max(np.abs(o["J3"].reshape(-1, 5, 5, 5).sum(3).reshape(-1, 25) - o["J2"])) <= 1e-12
    assert np.max(np.abs(o["T2"] - (o["J2"] - o["J2_half"]))) <= 1e-12
    assert np.max(np.abs(o["T3"] - (o["J3"] - (o["J3_C"] + o["J3_M"]) / 2))) <= 1e-12
    assert np.max(np.abs(o["G2"] - 0.5 * np.abs(o["J2"] - o["J2_half"]).sum(1))) <= 1e-12
    dec = cm_tokens[:, t - 1] == S3
    if dec.any():  # Theorem A at decision positions
        assert np.max(np.abs(o["Q1"][dec] - [0.2, 0.2, 0.6, 0, 0])) <= 1e-12
    edge = np.isin(cm_tokens[:, t - 1], (S0, S2))
    if edge.any():  # band-edge identity, section 3.3
        def delta(b):
            rho = b.reshape(-1, 4, 3).sum(1)
            return rho[:, 0] - rho[:, 2]
        want = 0.2 / 4 * (pi - 0.5) * (delta(o["b_M"]) - delta(o["b_C"]))
        assert np.max(np.abs((o["Q1"][:, A] - o["Q1_half"][:, A] - want)[edge])) <= 1e-12


def test_cc_oracle_null():
    tok = _sample(200, T_CC, "cc")
    for t in (3, 16, 28, 32):
        o = TG.oracle_at(tok, t, "CC")
        assert np.max(np.abs(np.asarray(o["pi"]) - 0.5)) <= 1e-11
        for key in ("Q1", "J2", "J3"):  # world-conditional TVs
            c, m = np.asarray(o[key + "_C"]), np.asarray(o[key + "_M"])
            assert np.max(0.5 * np.abs(c - m).sum(1)) <= 1e-12, key


# ---- T-PRIOR -------------------------------------------------------------------------------
def _exact_priors(model):
    v, out = list(model["mu"]), []
    for _ in range(32):
        out.append(_f(v))
        v = [sum((v[i] * model["T"][i][j] for i in range(24)), Q(0)) for j in range(24)]
    return out  # out[k] = mu T^k


PRIORS = {"CM": _exact_priors(EXACT), "CC": _exact_priors(d1_seam.exact_model("N1"))}


@pytest.mark.parametrize("proc", ["CM", "CC"])
def test_T_PRIOR_window_prior_is_mu_T_power(proc):
    for t in range(1, 33):
        for m in (1, 4, 8, t):
            got = np.asarray(TG.window_prior(t, m, proc), dtype=np.float64)
            k = t - min(m, t)
            assert got.shape == (24,)
            assert np.max(np.abs(got - PRIORS[proc][k])) <= 1e-12, (t, m)
            assert abs(got.sum() - 1) <= 1e-12


def _filter(tokens, prior, t, m):
    return BayesFilter(FM["T"], FM["E_mix"], prior).run(tokens[:, t - m:t])


@pytest.mark.parametrize("t", [1, 5, 16, 28, 32])
def test_T_PRIOR_whole_window_equals_full_filter(t, cm_tokens):
    full = _filter(cm_tokens, FM["mu"], t, t)
    post = np.asarray(TG.window_posterior(cm_tokens, t, t, "CM"))
    assert post.shape == (cm_tokens.shape[0], 24)
    assert np.max(np.abs(post - full.b[:, t - 1])) <= 1e-11
    assert np.max(np.abs(post[:, 12:].sum(1) - full.b[:, t - 1, 12:].sum(1))) <= 1e-11


@pytest.mark.parametrize("t", range(1, 9))
def test_T_PRIOR_window8_equals_full_oracle_up_to_t8(t, cm_tokens):
    full = _filter(cm_tokens, FM["mu"], t, t)
    post = np.asarray(TG.window_posterior(cm_tokens, t, 8, "CM"))
    assert np.max(np.abs(post - full.b[:, t - 1])) <= 1e-11
    assert np.max(np.abs(post @ FM["T"] @ FM["E_mix"] - full.q[:, t])) <= 1e-11
    o = TG.oracle_at(cm_tokens, t)
    pi = np.asarray(o["pi"])
    assert np.max(np.abs(np.asarray(o["pi8"]) - pi)) <= 1e-11
    assert np.max(np.abs(np.asarray(o["Q1_w8"]) - np.asarray(o["Q1"]))) <= 1e-11
    if t <= 4:
        assert np.max(np.abs(np.asarray(o["pi4"]) - pi)) <= 1e-11
    if t == 1:
        assert np.max(np.abs(np.asarray(o["pi1"]) - pi)) <= 1e-11


@pytest.mark.parametrize("t", [16, 28])
def test_T_PRIOR_windows_use_the_true_time_marginal(t, cm_tokens):
    o = TG.oracle_at(cm_tokens, t)
    for m, key in ((1, "pi1"), (4, "pi4"), (8, "pi8")):
        ref = _filter(cm_tokens, PRIORS["CM"][t - m], t, m).b[:, -1]
        post = np.asarray(TG.window_posterior(cm_tokens, t, m, "CM"))
        assert np.max(np.abs(post - ref)) <= 1e-11, m
        assert np.max(np.abs(np.asarray(o[key]) - ref[:, 12:].sum(1))) <= 1e-11, m
        if m == 8:
            q8 = ref @ FM["T"] @ FM["E_mix"]
            assert np.max(np.abs(np.asarray(o["Q1_w8"]) - q8)) <= 1e-11
