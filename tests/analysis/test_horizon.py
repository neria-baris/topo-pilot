"""Part (e) horizon feasibility: known answers and properties (X4 Phase B, protocol x4b-v1 §8)."""
import numpy as np
import pytest

from topo_pilot.analysis import (
    hellinger,
    helmert_basis,
    joint_marginals,
    nearest_partners,
    overall_verdict,
    pair_d2,
    practical_verdict,
    screen_pool,
    select_anchors,
    strict_verdict,
    tangent_audit,
)
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.analysis


def _maps(T, E):
    """Hand-written G1 = T E and lexicographic joint G2 (block i = T diag(E[:, i]) T E)."""
    G1 = T @ E
    G2 = np.hstack([T @ np.diag(E[:, i]) @ G1 for i in range(E.shape[1])])
    return G1, G2


def _stochastic(rng, n, m):
    a = rng.random((n, m)) + 0.05
    return a / a.sum(1, keepdims=True)


def _path():
    T = np.array([[.6, .4, 0, 0], [.4, .2, .4, 0], [0, .4, .2, .4], [0, 0, .4, .6]])
    E = np.array([[1., 0], [1, 0], [1, 0], [0, 1]])  # A at 0/1/2, B at 3
    return T, E


def test_helmert_basis_orthonormal_sum_zero():
    B = helmert_basis(144)
    assert B.shape == (144, 143)
    assert np.max(np.abs(B.T @ B - np.eye(143))) < 1e-13
    assert np.max(np.abs(B.sum(0))) < 1e-13
    with pytest.raises(StageFailure):
        helmert_basis(1)


def test_constant_emissions_factorize_and_have_no_gap():
    rng = np.random.default_rng(0)
    T = _stochastic(rng, 6, 6)
    E = np.tile(_stochastic(rng, 1, 3), (6, 1))
    G1, G2 = _maps(T, E)
    audit = tangent_audit(G1, G2)
    assert audit.verdict == "FACTORIZES" and audit.factor_conditioned
    b = _stochastic(rng, 2, 6)
    assert hellinger(b[:1] @ G2, b[1:] @ G2)[0] < 1e-7


def test_four_state_path_known_answer():
    G1, G2 = _maps(*_path())
    d0, d1 = np.eye(4)[0], np.eye(4)[1]
    np.testing.assert_allclose(d0 @ G1, [1, 0], atol=1e-15)
    np.testing.assert_allclose(d1 @ G1, [1, 0], atol=1e-15)
    assert (d0 @ G2)[0 * 2 + 0] == pytest.approx(1.0)      # AA
    assert (d1 @ G2)[0 * 2 + 1] == pytest.approx(0.16)     # AB
    assert tangent_audit(G1, G2).verdict == "ALLOWS_STABLE"


def test_constructed_factorization_is_detected():
    rng = np.random.default_rng(1)
    G1 = _stochastic(rng, 10, 4)
    L = _stochastic(rng, 4, 16)
    audit = tangent_audit(G1, G1 @ L)
    assert audit.verdict == "FACTORIZES"
    assert all(r.rho <= 1e-10 for r in audit.rows)
    assert not audit.certificate


def test_generic_hmm_has_certificate_and_tolerance_rows():
    rng = np.random.default_rng(2)
    G1, G2 = _maps(_stochastic(rng, 9, 9), _stochastic(rng, 9, 3))
    audit = tangent_audit(G1, G2)
    assert audit.verdict == "ALLOWS_STABLE" and audit.certificate
    assert [r.tau for r in audit.rows] == [1e-8, 1e-10, 1e-12]
    for r in audit.rows:
        assert r.rank_H <= 2 and r.null_dim == 8 - r.rank_H and r.null_residual < 1e-12


def test_symbol_permutation_invariance():
    rng = np.random.default_rng(3)
    T, E = _stochastic(rng, 9, 9), _stochastic(rng, 9, 3)
    perm = np.array([2, 0, 1])
    a, b = tangent_audit(*_maps(T, E)), tangent_audit(*_maps(T, E[:, perm]))
    np.testing.assert_allclose(a.H_singular_values, b.H_singular_values, atol=1e-14)
    np.testing.assert_allclose([r.rho for r in a.rows], [r.rho for r in b.rows], rtol=1e-9)
    beliefs = _stochastic(rng, 40, 9)
    q_a, q_b = beliefs @ (T @ E), beliefs @ (T @ E[:, perm])
    np.testing.assert_allclose(hellinger(q_a[:20], q_a[20:]), hellinger(q_b[:20], q_b[20:]),
                               atol=1e-15)


def test_joint_order_and_marginals_catch_bT2E_and_transposed_order():
    rng = np.random.default_rng(4)
    T, E = _stochastic(rng, 7, 7), _stochastic(rng, 7, 3)
    G1, G2 = _maps(T, E)
    first, second = joint_marginals(G2, 3)
    np.testing.assert_allclose(first, G1, atol=1e-14)
    np.testing.assert_allclose(second, T @ G1, atol=1e-14)
    assert np.max(np.abs(second - G1)) > 1e-3       # bT²E is not Q1
    transposed = G2.reshape(7, 3, 3).transpose(0, 2, 1).reshape(7, 9)
    assert np.max(np.abs(joint_marginals(transposed, 3)[0] - G1)) > 1e-3
    with pytest.raises(StageFailure) as exc:
        joint_marginals(T @ G1, 3)                  # a [N, V] marginal is not a joint
    assert exc.value.code == ErrorCode.ALIGNMENT_ERROR


def test_hellinger_bounds_and_negative_error():
    p = np.array([[1.0, 0.0], [0.5, 0.5]])
    q = np.array([[0.0, 1.0], [0.5, 0.5]])
    np.testing.assert_allclose(hellinger(p, q), [1.0, 0.0])
    with pytest.raises(StageFailure) as exc:
        hellinger(np.array([[1.1, -0.1]]), q[:1])
    assert exc.value.code == ErrorCode.NUMERICAL_FAILURE


def test_select_anchors_is_deterministic_and_order_free():
    ids = [f"test|{i}|h" for i in range(40)]
    a = select_anchors(ids, n=8)
    b = select_anchors(list(reversed(ids)), n=8)
    assert [ids[i] for i in a] == [list(reversed(ids))[i] for i in b]
    with pytest.raises(StageFailure):
        select_anchors(ids[:5], n=8)
    with pytest.raises(StageFailure):
        select_anchors(ids + ids[:1], n=8)


def test_nearest_partners_excludes_self_duplicates_and_other_symbols():
    Q1 = np.array([[.5, .5], [.5, .5], [.51, .49], [.6, .4], [.5, .5]])
    keys = ["k0", "k0", "k2", "k3", "k4"]          # row 1 repeats row 0's history
    last = np.array([0, 0, 0, 0, 1])
    ids = [f"id{i}" for i in range(5)]
    p = nearest_partners(Q1, keys, np.array([0]), last, ids, k=5)
    assert p.idx[0].tolist() == [2, 3, -1, -1, -1]
    assert p.n_duplicate[0] == 1 and p.group_size[0] == 2
    u = nearest_partners(Q1, keys, np.array([0]), None, ids, k=2)
    assert u.idx[0].tolist() == [4, 2]              # distance 0 to a distinct history first


def test_screen_pool_and_pair_d2():
    d1 = np.array([[0.005, 0.02], [0.02, 0.03], [0.001, np.nan]])
    d2 = np.array([[0.06, 0.2], [0.5, 0.5], [0.01, np.nan]])
    s = screen_pool(d1, d2, min_eligible=2, min_fraction=0.5)
    assert s.eligible.tolist() == [True, False, True]
    assert s.witness.tolist() == [True, False, False]
    assert (s.n_eligible, s.n_witness, s.fraction, s.status) == (2, 1, 0.5, "WITNESS")
    assert screen_pool(d1, d2, min_eligible=3).status == "UNDERCOVERED"
    assert screen_pool(d1, d2, min_eligible=2, min_fraction=0.6).status == "NO_MATERIAL_GAP"
    Q2 = np.array([[1.0, 0.0], [0.0, 1.0]])
    from topo_pilot.analysis import Partners
    part = Partners(np.array([[1, -1]]), np.array([[0.0, np.nan]]), np.array([1]),
                    np.array([0]))
    out = pair_d2(Q2, np.array([0]), part)
    assert out[0, 0] == pytest.approx(1.0) and np.isnan(out[0, 1])


@pytest.mark.parametrize("statuses,expected", [
    ({"test": "WITNESS", "a": "WITNESS", "b": "WITNESS", "c": "UNDERCOVERED"}, "GAP"),
    ({"test": "WITNESS", "a": "WITNESS", "b": "NO_MATERIAL_GAP", "c": "NO_MATERIAL_GAP"},
     "INCONCLUSIVE"),
    ({"test": "NO_MATERIAL_GAP", "a": "NO_MATERIAL_GAP", "b": "NO_MATERIAL_GAP",
      "c": "UNDERCOVERED"}, "NO_GAP"),
    ({"test": "NO_MATERIAL_GAP", "a": "NO_MATERIAL_GAP", "b": "NO_MATERIAL_GAP",
      "c": "WITNESS"}, "INCONCLUSIVE"),
    ({"test": "UNDERCOVERED", "a": "WITNESS", "b": "WITNESS", "c": "WITNESS"}, "INCONCLUSIVE"),
])
def test_practical_verdict_two_of_three_rule(statuses, expected):
    assert practical_verdict(statuses)[0] == expected


def test_overall_and_strict_verdicts():
    assert overall_verdict("ALLOWS_STABLE", False, "GAP", True)[0] == "GO"
    assert overall_verdict("ALLOWS_STABLE", False, "GAP", False)[0] == "INCONCLUSIVE"
    assert overall_verdict("ALLOWS_STABLE", False, "NO_GAP", True)[0] == "NO-GO"
    assert overall_verdict("FACTORIZES", True, "GAP", True)[0] == "NO-GO"
    assert overall_verdict("FACTORIZES", False, "GAP", True)[0] == "INCONCLUSIVE"
    assert overall_verdict("TOLERANCE_DEPENDENT", False, "GAP", True)[0] == "INCONCLUSIVE"
    assert overall_verdict("ALLOWS_STABLE", False, "INCONCLUSIVE", True)[0] == "INCONCLUSIVE"
    assert strict_verdict("ALLOWS_STABLE") == "UNRESOLVED"
    assert strict_verdict("FACTORIZES") == "SUFFICIENT_AMBIENT"
