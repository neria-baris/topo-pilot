"""Author B (job 0119), TEST_PLAN §3 `test_b_oracle.py`: stream scopes (§6.6), one
`HMMSampler.sample` call per world-look returning contiguous uint8 tokens without w_last or
states (§4.7, RC-5), `row_arrays` keys/shapes/dtypes and formulas, the DR8 formula bridge at
W = 12, the DR11 alignment traps against an independent reference filter written here, the DR3
forced unanchored world (m_K = 0), `prefix_permuted`, `p4_rows` and the marginal conventions.

Synthetic only: the tiny DR1 world (layout n_obs = 9) and fixed token arrays; at W = 12 only
deterministic token rows are filtered, nothing is sampled. Written without reading
tools/hws/*.py."""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hws") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hws"))

import hws_worlds as hw  # noqa: E402
import hws_oracle as ho  # noqa: E402

import k4b_scores  # noqa: E402
import oracle_profile  # noqa: E402
import scores  # noqa: E402
from topo_pilot.contracts import SeedTree, SequenceLayout  # noqa: E402
from topo_pilot.dataset.sampler import HMMSampler  # noqa: E402

TINY = SequenceLayout(n_obs=9, context=8, analysis_position=8)
STAGES = ("S0", "S1", "X1", "S2", "S3", "DRY")


@pytest.fixture(scope="module")
def tiny():
    return hw.build_tiny()


@pytest.fixture(scope="module")
def w0():
    return hw.build_process(hw.W0)


def _tok(n, L, V, a=7, b=1):
    return ((np.arange(n * L).reshape(n, L) * a + b) % V).astype(np.uint8)


def _kl(p, q):
    return np.sum(p * (np.log(p) - np.log(q)), axis=1)


def _H(p):
    return -np.sum(p * np.log(p), axis=1)


def _spy(monkeypatch):
    calls, outs = [], []
    orig = HMMSampler.sample

    def spy(self, n, rng):
        calls.append(n)
        out = orig(self, n, rng)
        outs.append(out)
        return out

    monkeypatch.setattr(HMMSampler, "sample", spy)
    return calls, outs, orig


# ---------------------------------------------------------------------------- streams

def test_history_streams_match_the_seedtree_scopes():
    key = "W12-q2-s1.5-p0.75"
    draws = {}
    for st in STAGES:
        got = ho.history_generator(st, key).random(4)
        assert np.array_equal(got, SeedTree(0).generator("data", "hws-v1", st, key).random(4))
        draws[st] = tuple(got)
    nc = ho.history_generator("NULLCHK", key, origin="S1").random(4)
    ref = SeedTree(0).generator("data", "hws-v1", "NULLCHK", "S1", key).random(4)
    assert np.array_equal(nc, ref)
    draws["NULLCHK/S1"] = tuple(nc)
    draws["perm"] = tuple(ho.perm_generator(key).random(4))
    assert np.array_equal(draws["perm"],
                          SeedTree(0).generator("hws-v1", "prefix_perm", key).random(4))
    assert len(set(draws.values())) == len(draws)  # stages never share a stream


def test_stream_refusals():
    with pytest.raises((ValueError, TypeError, hw.HwsStop)):
        ho.history_generator("NULLCHK", "W12-q1-s1.25-p0.2")
    for bad in ("S4", "nullchk", "", "FINAL", "s1"):
        with pytest.raises(ValueError):
            ho.history_generator(bad, "W12-q1-s1.25-p0.2")


# --------------------------------------------------------------------------- sampling

def test_sample_calls_the_sampler_once_and_drops_the_last_symbol(tiny, monkeypatch):
    calls, outs, orig = _spy(monkeypatch)
    tok = ho.sample(tiny, 50, np.random.default_rng(5), TINY)
    assert calls == [50]
    assert isinstance(tok, np.ndarray) and tok.dtype == np.uint8
    assert tok.shape == (50, 8) and tok.flags.c_contiguous
    assert np.array_equal(tok, outs[0][0][:, :8])
    replay, _ = orig(HMMSampler(tiny["T"], tiny["E"], tiny["pi"], TINY), 50,
                     np.random.default_rng(5))
    assert np.array_equal(tok, replay[:, :8])


def test_world_look_streams_and_bit_identical_regeneration(tiny, monkeypatch):
    calls, _, _ = _spy(monkeypatch)
    look = ho.world_look(tiny, "DRY", 64, (1, 2, 4), layout=TINY)
    assert calls == [64]
    assert list(look["stream"]) == ["data", "hws-v1", "DRY", tiny["key"]]
    ref = ho.sample(tiny, 64, SeedTree(0).generator("data", "hws-v1", "DRY", tiny["key"]), TINY)
    assert np.array_equal(look["tok"], ref)
    again = ho.world_look(tiny, "DRY", 64, (1, 2, 4), layout=TINY)  # resume: same stream
    assert np.array_equal(again["tok"], look["tok"])
    for K in (1, 2, 4, 8):
        assert np.array_equal(again["rows"]["m"][K], look["rows"]["m"][K])
    assert np.array_equal(again["rows"]["D"][4], look["rows"]["D"][4])
    nc = ho.world_look(tiny, "NULLCHK", 64, (1, 2, 4), origin="DRY", layout=TINY)
    assert list(nc["stream"]) == ["data", "hws-v1", "NULLCHK", "DRY", tiny["key"]]
    assert not np.array_equal(nc["tok"], look["tok"])
    assert calls == [64, 64, 64, 64]


# ------------------------------------------------------------------------- row arrays

def test_row_arrays_keys_shapes_dtypes_and_formulas(tiny):
    n, Ks = 40, (1, 2, 4)
    tok = _tok(n, 8, 3, 5, 2)
    rows = ho.row_arrays(tiny, tok, Ks)
    # API-AMBIGUITY: API §3 writes `m[K]`, `D[K]`, `Hq[K]`; read as rows["m"][K] (int K)
    T, E, pi, c = tiny["T"], tiny["E"], tiny["pi"], tiny["features"]
    b = {K: oracle_profile.suffix_posterior(T, E, pi, tok, K) for K in (1, 2, 4, 8)}
    q = {K: (b[K] @ T) @ E for K in b}
    m = {K: b[K] @ c for K in b}
    for K in Ks + (8,):
        assert rows["m"][K].shape == (n, 2) and rows["m"][K].dtype == np.float64
        np.testing.assert_allclose(rows["m"][K], m[K], rtol=0, atol=1e-15)
    for K in Ks:
        for name in ("D", "rn", "G"):
            assert rows[name][K].shape == (n,) and rows[name][K].dtype == np.float64
        np.testing.assert_allclose(rows["G"][K], _kl(q[8], q[K]), rtol=0, atol=1e-12)
        np.testing.assert_allclose(rows["rn"][K], np.linalg.norm(m[8] - m[K], axis=1),
                                   rtol=0, atol=1e-15)
    for name in ("G0", "G4A", "IZ4", "IX4", "Hb1", "m_norm", "phase", "pinsker_slack",
                 "gain_ind", "weak_ind", "m_sq"):
        assert rows[name].shape == (n,) and rows[name].dtype == np.float64, name
    for name in ("Hq", "HqA", "Hb", "Hbx"):
        assert set(rows[name]) >= {4, 8}, name
    bx = {K: b[K].reshape(n, 6, 2).sum(axis=2) for K in (4, 8)}
    q0 = np.broadcast_to(pi @ T @ E, q[8].shape)
    np.testing.assert_allclose(rows["G0"], _kl(q[8], q0), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["G4A"], _kl(q[8], q[4]), rtol=0, atol=1e-12)  # n_axial 1
    np.testing.assert_allclose(rows["IZ4"], _kl(b[8], b[4]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["IX4"], _kl(bx[8], bx[4]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["Hq"][8], _H(q[8]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["Hb"][4], _H(b[4]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["Hbx"][4], _H(bx[4]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["Hb1"], _H(b[1]), rtol=0, atol=1e-12)
    np.testing.assert_allclose(rows["m_norm"], np.linalg.norm(m[8], axis=1), rtol=0,
                               atol=1e-15)
    np.testing.assert_allclose(rows["m_sq"], rows["m_norm"] ** 2, rtol=1e-14, atol=0)
    np.testing.assert_allclose(rows["pinsker_slack"], 2 * rows["IX4"] - rows["rn"][4] ** 2,
                               rtol=0, atol=1e-15)
    assert np.all(rows["pinsker_slack"] >= -1e-12)  # §2.3: holds on every row
    assert np.array_equal(rows["gain_ind"], (rows["G4A"] >= 0.005).astype(np.float64))
    assert np.array_equal(rows["weak_ind"], (rows["m_norm"] < 0.1).astype(np.float64))
    assert set(rows["nulls"]) == {"m4_phase", "orth_1", "orth_2", "orth_4"}  # no sha at L = 8
    assert float(rows["norm_err"]) <= 1e-12


def test_dr8_formula_bridge_at_w12(w0):
    tok = _tok(64, 32, 36, 11, 5)
    Ks = (1, 2, 4, 8, 16)
    rows = ho.row_arrays(w0, tok, Ks)
    feats = oracle_profile.circle_features(w0["coords"])
    pm = oracle_profile.posterior_means(w0["T"], w0["E"], w0["pi"], tok, Ks + (32,), feats)
    m32, m4 = pm[32], pm[4]
    phi = k4b_scores.oracle_phase(m32)
    for K in Ks + (32,):
        assert np.array_equal(rows["m"][K], pm[K]), K
    for K in Ks:
        assert np.array_equal(rows["D"][K], k4b_scores.phase_scores(phi, m32, pm[K])), K
        assert np.array_equal(rows["rn"][K], scores.r4_norms(m32, pm[K])), K
        orth = np.sum(pm[K] * (m32 - pm[K]), axis=1)
        np.testing.assert_allclose(rows["nulls"][f"orth_{K}"], orth, rtol=0, atol=1e-15)
    assert np.array_equal(rows["phase"], phi)
    nulls = rows["nulls"]
    assert set(nulls) == set(ho.NULL_NAMES)
    assert np.array_equal(nulls["m4_phase"],
                          k4b_scores.phase_scores(k4b_scores.m4_phase(m4), m32, m4))
    assert np.array_equal(nulls["sha_suffix"],
                          k4b_scores.phase_scores(k4b_scores.sha_phase(tok), m32, m4))
    b32 = oracle_profile.suffix_posterior(w0["T"], w0["E"], w0["pi"], tok, 32)
    b4 = oracle_profile.suffix_posterior(w0["T"], w0["E"], w0["pi"], tok, 4)
    qa = {K: ((b @ w0["T"]) @ w0["E"]).reshape(64, 6, 6).sum(axis=2)
          for K, b in ((32, b32), (4, b4))}
    np.testing.assert_allclose(rows["G4A"], _kl(qa[32], qa[4]), rtol=0, atol=1e-12)


# ----------------------------------------------------------------- DR11 alignment traps

def _ref_belief(T, E, pi, tok, K, transpose=False, symmap=None, prefix=False,
                inherit=False, trailing=False):
    """Independent suffix filter: restart from pi, emit first, transition between emissions."""
    TT = T.T if transpose else T
    EE = E[:, symmap] if symmap is not None else E
    n, L = tok.shape
    out = np.empty((n, len(pi)))
    for r in range(n):
        seq = tok[r] if inherit else (tok[r, :K] if prefix else tok[r, L - K:])
        b = pi.copy()
        for t, w in enumerate(seq):
            if t:
                b = b @ TT
            b = b * EE[:, int(w)]
            b = b / b.sum()
        out[r] = b @ TT if trailing else b
    return out


def test_dr11_alignment_traps_are_detected(tiny):
    rng = np.random.default_rng(3)
    T = rng.random((12, 12)) + 0.05
    T /= T.sum(axis=1, keepdims=True)  # not symmetric, so a transposed T is visible
    pi = np.full(12, 1.0 / 12)
    for _ in range(500):
        pi = pi @ T
    proc = dict(tiny, T=T, pi=pi)
    tok = rng.integers(0, 3, (200, 8)).astype(np.uint8)
    rows = ho.row_arrays(proc, tok, (1, 2, 4))
    c, E, K = tiny["features"], tiny["E"], 2
    np.testing.assert_allclose(rows["m"][K], _ref_belief(T, E, pi, tok, K) @ c, rtol=0,
                               atol=1e-12)
    np.testing.assert_allclose(rows["m"][8], _ref_belief(T, E, pi, tok, 8) @ c, rtol=0,
                               atol=1e-12)
    traps = {"transposed_T": {"transpose": True}, "wrong_symbol_map": {"symmap": [1, 2, 0]},
             "prefix_not_suffix": {"prefix": True}, "inherited_belief": {"inherit": True},
             "trailing_transition": {"trailing": True}}
    for name, kw in traps.items():
        bad = _ref_belief(T, E, pi, tok, K, **kw) @ c
        assert np.max(np.abs(bad - rows["m"][K])) > 1e-6, name


# ------------------------------------------------------------ DR3, known zero, P4, marginals

def test_dr3_forced_unanchored_world_has_zero_moments():
    proc = hw.build_process(hw.World(12, 2, F(5, 4), F(1, 5)), alias="unanchored")
    rows = ho.row_arrays(proc, _tok(16, 32, proc["V"]), (1, 2, 4))
    for K in (1, 2, 4, 32):
        assert np.max(np.abs(rows["m"][K])) <= 1e-12, K
    for K in (1, 2, 4):
        assert np.max(np.abs(rows["D"][K])) <= 1e-12, K


def test_identical_emission_has_no_beyond_k_information():
    N = hw.build_known_zero("N")
    rows = ho.row_arrays(N, _tok(8, 32, 36), (1, 2, 4))
    for K in (1, 2, 4):
        for name in ("D", "rn", "G"):
            assert np.max(np.abs(rows[name][K])) <= 1e-12, (name, K)
    for name in ("G4A", "IZ4", "IX4"):
        assert np.max(np.abs(rows[name])) <= 1e-12, name


def test_prefix_permuted_and_p4_rows(tiny):
    tok = np.random.default_rng(8).integers(0, 36, (20, 32)).astype(np.uint8)
    keep = tok.copy()
    out = ho.prefix_permuted(tok, np.random.default_rng(4))
    assert np.array_equal(tok, keep) and out.dtype == np.uint8 and out.shape == tok.shape
    assert np.array_equal(out[:, 28:], tok[:, 28:])
    assert all(sorted(out[r, :28]) == sorted(tok[r, :28]) for r in range(20))
    ref = tok.copy()
    ref[:, :28] = np.random.default_rng(4).permuted(tok[:, :28], axis=1)
    assert np.array_equal(out, ref) and not np.array_equal(out, tok)
    t8 = _tok(30, 8, 3, 5, 1)
    T, E, pi, c = tiny["T"], tiny["E"], tiny["pi"], tiny["features"]
    mL = oracle_profile.suffix_posterior(T, E, pi, t8, 8) @ c
    perm = ho.prefix_permuted(t8, np.random.default_rng(6))
    assert np.array_equal(perm[:, 4:], t8[:, 4:])
    mP = oracle_profile.suffix_posterior(T, E, pi, perm, 8) @ c
    got = ho.p4_rows(tiny, t8, mL, np.random.default_rng(6))
    np.testing.assert_allclose(got, np.sum((mL - mP) ** 2, axis=1), rtol=0, atol=1e-15)


def test_marginal_index_conventions():
    rng = np.random.default_rng(9)
    b = rng.random((3, 96))
    ref = np.zeros((3, 8))
    for z in range(96):  # state id x*12 + y
        ref[:, z // 12] += b[:, z]
    np.testing.assert_allclose(ho.x_marginal(b, 8, 12), ref, rtol=1e-15, atol=0)
    qv = rng.random((3, 18))
    refq = np.zeros((3, 3))
    for v in range(18):  # v = 6g + b
        refq[:, v // 6] += qv[:, v]
    np.testing.assert_allclose(ho.circ_marginal(qv, 6), refq, rtol=1e-15, atol=0)
