import itertools

import numpy as np
import pytest

from topo_pilot import oracle
from topo_pilot.contracts import EvalSidecar, StageFailure
from topo_pilot.contracts.testing import memory_store, tiny_hmm, tiny_observations
from topo_pilot.oracle import BayesFilter, FutureOperator, LastSymbolPosterior, context_gain

pytestmark = pytest.mark.oracle


# ---------------------------------------------------------------- brute-force helpers
def joint_over_paths(T, E, pi, seq):
    """Array [N]*len(seq) of P(w_1..w_P, z_1..z_P) under the generation model."""
    N = T.shape[0]
    P = len(seq)
    out = np.zeros((N,) * P)
    for path in itertools.product(range(N), repeat=P):
        p = pi[path[0]] * E[path[0], seq[0]]
        for t in range(1, P):
            p *= T[path[t - 1], path[t]] * E[path[t], seq[t]]
        out[path] = p
    return out


def brute_marginal(T, E, pi, seq):
    """(evidence, posterior of last state) for a sequence."""
    J = joint_over_paths(T, E, pi, list(seq))
    ev = J.sum()
    last = J.sum(axis=tuple(range(len(seq) - 1)))
    return ev, last / ev


def code_name(exc):
    c = exc.value.code
    return getattr(c, "name", str(c))


@pytest.fixture(scope="module")
def hmm():
    return tiny_hmm()


# ---------------------------------------------------------------- O01
def test_O01_bruteforce_all_length4_sequences(hmm):
    T, E, pi = hmm
    seqs = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int64)
    assert seqs.shape == (81, 4)
    res = BayesFilter(T, E, pi).run(seqs)
    assert res.b.shape == (81, 4, 4)
    assert res.q.shape == (81, 5, 3)
    assert res.log_evidence.shape == (81,)
    assert res.ce.shape == (81, 4)
    cache = {}

    def ev_post(seq):
        key = tuple(seq)
        if key not in cache:
            cache[key] = brute_marginal(T, E, pi, key)
        return cache[key]

    for r, seq in enumerate(seqs.tolist()):
        assert res.log_evidence[r] == pytest.approx(np.log(ev_post(seq)[0]), abs=1e-10)
        for t in range(1, 5):
            np.testing.assert_allclose(res.b[r, t - 1], ev_post(seq[:t])[1], atol=1e-10)
        for t in range(0, 5):
            for w in range(3):
                if t == 0:
                    pred = float(pi @ E[:, w])
                else:
                    pred = ev_post(seq[:t] + [w])[0] / ev_post(seq[:t])[0]
                assert res.q[r, t, w] == pytest.approx(pred, abs=1e-10)
        for t in range(1, 5):
            assert res.ce[r, t - 1] == pytest.approx(-np.log(res.q[r, t - 1, seq[t - 1]]),
                                                     abs=1e-10)
    assert np.allclose(res.b.sum(-1), 1.0, atol=1e-10)
    assert np.allclose(res.q.sum(-1), 1.0, atol=1e-10)


def test_O01_belief_at_matches_run(hmm):
    T, E, pi = hmm
    tok = np.array([[0, 1, 2, 2, 1], [2, 2, 0, 1, 0]], dtype=np.int64)
    f = BayesFilter(T, E, pi)
    res = f.run(tok)
    for p in range(1, 6):
        np.testing.assert_allclose(f.belief_at(tok, p), res.b[:, p - 1], atol=1e-12)
        np.testing.assert_allclose(f.run(tok[:, :p]).b[:, p - 1], res.b[:, p - 1], atol=1e-12)


def test_O01_evidence_is_sum_of_ce(hmm):
    T, E, pi = hmm
    tok = np.random.default_rng(3).integers(0, 3, size=(6, 20))
    res = BayesFilter(T, E, pi).run(tok)
    np.testing.assert_allclose(res.log_evidence, -res.ce.sum(1), atol=1e-10)


def test_filter_inputs_untouched_and_rows_independent(hmm):
    T, E, pi = hmm
    T0, E0, pi0 = T.copy(), E.copy(), pi.copy()
    tok = tiny_observations(R=8).tokens.astype(np.int64)
    f = BayesFilter(T, E, pi)
    full = f.run(tok)
    single = f.run(tok[3:4])
    np.testing.assert_allclose(full.b[3], single.b[0], atol=1e-12)
    np.testing.assert_array_equal(T, T0)
    np.testing.assert_array_equal(E, E0)
    np.testing.assert_array_equal(pi, pi0)
    np.testing.assert_allclose(f.run(tok.astype(np.uint8)).b, full.b, atol=1e-12)


# ---------------------------------------------------------------- O02
def test_O02_q0_is_pi_E(hmm):
    T, E, pi = hmm
    tok = np.random.default_rng(0).integers(0, 3, size=(5, 7))
    q = BayesFilter(T, E, pi).run(tok).q
    for r in range(5):
        np.testing.assert_allclose(q[r, 0], pi @ E, atol=1e-14)
    T2 = np.array([[0.9, 0.1], [0.4, 0.6]])
    E2 = np.array([[0.8, 0.2], [0.3, 0.7]])
    pi2 = np.array([0.2, 0.8])
    q2 = BayesFilter(T2, E2, pi2).run(np.array([[0, 1]])).q
    np.testing.assert_allclose(q2[0, 0], pi2 @ E2, atol=1e-14)


# ---------------------------------------------------------------- O03
def test_O03_unique_emission_belief_is_delta():
    T, _, pi = tiny_hmm()
    E = np.eye(4)
    rng = np.random.default_rng(1)
    tok = np.zeros((6, 10), dtype=np.int64)
    for r in range(6):
        z = rng.choice(4, p=pi)
        for t in range(10):
            tok[r, t] = z
            z = rng.choice(4, p=T[z])
    with pytest.raises(StageFailure) as exc:
        BayesFilter(T, E, pi).run(np.array([[0, 2]], dtype=np.int64))
    assert code_name(exc) == "IMPOSSIBLE_HISTORY"
    res = BayesFilter(T, E, pi).run(tok)
    for r in range(6):
        for t in range(10):
            np.testing.assert_allclose(res.b[r, t], np.eye(4)[tok[r, t]], atol=1e-12)
            np.testing.assert_allclose(res.q[r, t + 1], (T @ E)[tok[r, t]], atol=1e-12)


# ---------------------------------------------------------------- O04
def test_O04_uniform_emission_beliefs_stay_pi():
    T, _, pi = tiny_hmm()
    E = np.full((4, 3), 1 / 3)
    tok = np.random.default_rng(2).integers(0, 3, size=(6, 12))
    res = BayesFilter(T, E, pi).run(tok)
    np.testing.assert_allclose(res.b, np.broadcast_to(pi, res.b.shape), atol=1e-12)
    np.testing.assert_allclose(res.q, 1 / 3, atol=1e-12)
    np.testing.assert_allclose(res.log_evidence, 12 * np.log(1 / 3), atol=1e-10)


# ---------------------------------------------------------------- O05
def test_O05_F1_F2(hmm):
    T, E, pi = hmm
    tok = np.array([[0, 1], [2, 2], [1, 0], [0, 0]], dtype=np.int64)
    res = BayesFilter(T, E, pi).run(tok)
    b = res.b[:, 1]
    fo = FutureOperator(T, E)
    F1, F2 = fo.F1(b), fo.F2(b)
    assert F1.shape == (4, 3) and F2.shape == (4, 3, 3)
    np.testing.assert_allclose(F1, res.q[:, 2], atol=1e-12)
    np.testing.assert_allclose(F2.sum(axis=2), F1, atol=1e-12)
    np.testing.assert_allclose(F2.sum(axis=(1, 2)), 1.0, atol=1e-12)
    for r in range(4):
        ev = brute_marginal(T, E, pi, tok[r].tolist())[0]
        for i in range(3):
            for j in range(3):
                bf = brute_marginal(T, E, pi, tok[r].tolist() + [i, j])[0] / ev
                assert F2[r, i, j] == pytest.approx(bf, abs=1e-10)


def test_O05_F2_from_prior_matches_brute_force(hmm):
    T, E, pi = hmm
    F2 = FutureOperator(T, E).F2(pi[None, :])
    for i in range(3):
        for j in range(3):
            assert F2[0, i, j] == pytest.approx(brute_marginal(T, E, pi, [i, j])[0], abs=1e-12)


# ---------------------------------------------------------------- O06
def test_O06_last_symbol_posterior(hmm):
    T, E, pi = hmm
    lsp = LastSymbolPosterior(T, E, pi)
    w = np.array([0, 1, 2, 2, 0], dtype=np.int64)
    r = lsp.r(w)
    assert r.shape == (5, 4)
    f = BayesFilter(T, E, pi)
    ql = lsp.q_last(w)
    assert ql.shape == (5, 3)
    np.testing.assert_allclose(ql, r @ T @ E, atol=1e-12)
    np.testing.assert_allclose(ql.sum(1), 1.0, atol=1e-12)
    for k, wk in enumerate(w):
        one = f.run(np.array([[wk]]))
        np.testing.assert_allclose(r[k], one.b[0, 0], atol=1e-12)
        np.testing.assert_allclose(r[k], pi * E[:, wk] / (pi @ E[:, wk]), atol=1e-14)
        np.testing.assert_allclose(ql[k], one.q[0, 1], atol=1e-12)


# ---------------------------------------------------------------- O07
def test_O07_context_gain_nonneg_and_zero(hmm):
    rng = np.random.default_rng(4)
    for _ in range(50):
        qc = rng.dirichlet(np.ones(5), size=7)
        ql = rng.dirichlet(np.ones(5), size=7)
        assert context_gain(qc, ql) >= -1e-15
        assert context_gain(qc, qc) == pytest.approx(0.0, abs=1e-12)
    qc = np.array([[0.5, 0.5]])
    ql = np.array([[0.25, 0.75]])
    expect = 0.5 * np.log(0.5 / 0.25) + 0.5 * np.log(0.5 / 0.75)
    assert context_gain(qc, ql) == pytest.approx(expect, abs=1e-12)
    both = context_gain(np.vstack([qc, [[0.1, 0.9]]]), np.vstack([ql, [[0.1, 0.9]]]))
    assert both == pytest.approx(expect / 2, abs=1e-12)
    T, E, pi = hmm
    tok = tiny_observations(R=8).tokens.astype(np.int64)
    qC = BayesFilter(T, E, pi).run(tok).q[:, 32]
    qL = LastSymbolPosterior(T, E, pi).q_last(tok[:, 31])
    assert context_gain(qC, qL) >= -1e-12


# ---------------------------------------------------------------- O08
def test_O08_impossible_history_raises():
    T, _, pi = tiny_hmm()
    E0 = np.array([[0.5, 0.5, 0.0]] * 4)
    with pytest.raises(StageFailure) as exc:
        BayesFilter(T, E0, pi).run(np.array([[0, 1, 2]], dtype=np.int64))
    assert code_name(exc) == "IMPOSSIBLE_HISTORY"
    T2 = np.eye(2)
    E2 = np.array([[1.0, 0.0], [0.0, 1.0]])
    pi2 = np.array([1.0, 0.0])
    f = BayesFilter(T2, E2, pi2)
    f.run(np.array([[0, 0, 0]], dtype=np.int64))
    with pytest.raises(StageFailure) as exc:
        f.run(np.array([[0, 0, 1]], dtype=np.int64))
    assert code_name(exc) == "IMPOSSIBLE_HISTORY"
    with pytest.raises(StageFailure) as exc:
        f.run(np.array([[0, 0, 0], [0, 1, 0]], dtype=np.int64))
    assert code_name(exc) == "IMPOSSIBLE_HISTORY"
    with pytest.raises(StageFailure) as exc:
        LastSymbolPosterior(T2, E2, pi2).r(np.array([1], dtype=np.int64))
    assert code_name(exc) == "IMPOSSIBLE_HISTORY"


def test_alignment_errors(hmm):
    T, E, pi = hmm
    f = BayesFilter(T, E, pi)
    with pytest.raises(StageFailure) as exc:
        f.run(np.zeros((2, 34), dtype=np.int64))
    assert code_name(exc) == "ALIGNMENT_ERROR"
    with pytest.raises(StageFailure) as exc:
        f.run(np.array([[0, 1, 3]], dtype=np.int64))
    assert code_name(exc) == "ALIGNMENT_ERROR"
    f.run(np.zeros((2, 33), dtype=np.int64))  # P = 33 is allowed


# ---------------------------------------------------------------- O09
def test_O09_long_near_deterministic_no_underflow():
    N = 4
    eps = 1e-3
    E = (1 - eps) * np.eye(N) + eps / N * np.ones((N, N))
    pi = np.full(N, 1 / N)
    T = (1 - eps) * np.roll(np.eye(N), 1, axis=1) + eps / N * np.ones((N, N))
    tok = np.array([[(t + 1) % N for t in range(33)], [(3 * t) % N for t in range(33)]],
                   dtype=np.int64)
    res = BayesFilter(T, E, pi).run(tok)
    for a in (res.log_evidence, res.ce, res.b, res.q):
        assert np.all(np.isfinite(a))
    assert np.all(res.ce >= 0)
    np.testing.assert_allclose(res.b.sum(-1), 1.0, atol=1e-10)
    np.testing.assert_allclose(res.q.sum(-1), 1.0, atol=1e-10)
    assert res.log_evidence[0] > 33 * np.log(1 / N)
    eps2 = 1e-12
    T3 = (1 - eps2) * np.roll(np.eye(N), 1, axis=1) + eps2 / N
    res3 = BayesFilter(T3, E, pi).run(tok[:1])
    assert np.isfinite(res3.log_evidence[0])
    np.testing.assert_allclose(res3.b.sum(-1), 1.0, atol=1e-10)


# ---------------------------------------------------------------- O10
def test_O10_observability_ranks():
    N = 4
    T = 0.6 * np.eye(N) + 0.1 * np.ones((N, N))
    assert abs(np.linalg.det(T)) > 1e-3

    def rank(s):
        return int(np.sum(np.asarray(s) > 1e-10))

    sv = FutureOperator(T, np.eye(N)).observability_singular_values(3)
    assert len(sv) == 3
    assert all(rank(s) == N for s in sv)
    svu = FutureOperator(T, np.full((N, 3), 1 / 3)).observability_singular_values(3)
    assert len(svu) == 3
    assert all(rank(s) == 1 for s in svu)
    assert len(FutureOperator(T, np.eye(N)).observability_singular_values(2)) == 2


# ---------------------------------------------------------------- O11
def test_O11_policy_refuses_sidecar_for_oracle():
    store = memory_store()
    obs = tiny_observations(R=4)
    side = EvalSidecar(split="test", N=4, sequence_id=obs.sequence_id,
                       z=np.zeros((4, 33), dtype=np.int16))
    sid = store.save(side, config={"k": "sidecar"}, parents=[], seed_map={}, consumer="analysis")
    assert store.load(EvalSidecar, sid, consumer="analysis").N == 4
    with pytest.raises(StageFailure) as exc:
        store.load(EvalSidecar, sid, consumer="oracle")
    assert code_name(exc) == "LEAKAGE"


def test_public_api_exports():
    for name in ("BayesFilter", "LastSymbolPosterior", "FutureOperator", "context_gain",
                 "OracleStage"):
        assert hasattr(oracle, name)
