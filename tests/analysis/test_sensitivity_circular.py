"""Independent tests N13, N20-N25 for SPEC part (c): sensitivity variants, circular correspondence.

Expected values are computed by hand or by brute force with numpy/scipy inside the tests.
"""
import numpy as np
import pytest
from scipy.spatial.distance import cdist

from topo_pilot.analysis import (
    CircularCorrespondence,
    Sensitivity,
    belief_angle,
    circular_agreement,
    lattice_angle,
)
from topo_pilot.contracts import (
    ActivationSet,
    ErrorCode,
    EvalSidecar,
    HistoryIndex,
    ObservationSet,
    OracleOutputs,
    StageFailure,
    make_history_id,
    tokens_hash,
)
from topo_pilot.contracts.testing import memory_store, tiny_world_spec

pytestmark = pytest.mark.analysis

S = Sensitivity()


def expect_code(code, fn, *args, **kwargs):
    with pytest.raises(StageFailure) as ei:
        fn(*args, **kwargs)
    assert ei.value.code == code


def wrap(a):
    """Wrap angles to (-pi, pi]."""
    return np.angle(np.exp(1j * np.asarray(a)))


# ---------------------------------------------------------------- N20


def test_N20_euclidean_equals_cdist():
    X = np.random.default_rng(0).normal(size=(15, 5))
    D = S.activation_D(X, "euclidean")
    assert np.allclose(D, cdist(X, X), atol=1e-10)
    assert np.allclose(D, D.T) and np.all(np.diag(D) == 0)


def test_N20_chord_equals_normalised_cdist_and_scale_invariant():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(12, 4))
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    D = S.activation_D(X, "chord")
    assert np.allclose(D, cdist(Xn, Xn), atol=1e-10)
    scale = rng.uniform(0.2, 9.0, size=(12, 1))
    assert np.allclose(S.activation_D(X * scale, "chord"), D, atol=1e-9)


def test_N20_pca_full_dims_equals_euclidean():
    rng = np.random.default_rng(2)
    X_fit = rng.normal(size=(40, 4))
    X = rng.normal(size=(10, 4))
    D = S.activation_D(X, "pca", X_fit=X_fit, pca_dims=4)
    assert np.allclose(D, cdist(X, X), atol=1e-8)


def test_N20_pca_one_dim_matches_hand_singular_vector():
    # 2-D example: fit cloud stretched along (1, 1); X is a different cloud.
    X_fit = np.array([[-3.0, -2.5], [-1.0, -1.2], [0.5, 0.4], [2.0, 2.2], [1.5, 1.1]])
    X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 2.0], [3.0, -1.0]])
    Xc = X_fit - X_fit.mean(axis=0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    v1 = Vt[0]
    proj = X @ v1
    expected = np.abs(proj[:, None] - proj[None, :])
    D = S.activation_D(X, "pca", X_fit=X_fit, pca_dims=1)
    assert np.allclose(D, expected, atol=1e-9)


def test_N20_pca_fit_set_defines_projection():
    X = np.array([[0.0, 0.0], [1.0, 5.0], [2.0, -3.0]])
    fit_x = np.array([[-4.0, 0.1], [4.0, -0.1], [-2.0, 0.0], [2.0, 0.0]])  # variance along axis 0
    fit_y = fit_x[:, ::-1].copy()                                           # variance along axis 1
    Dx = S.activation_D(X, "pca", X_fit=fit_x, pca_dims=1)
    Dy = S.activation_D(X, "pca", X_fit=fit_y, pca_dims=1)
    for D, fit in ((Dx, fit_x), (Dy, fit_y)):
        v1 = np.linalg.svd(fit - fit.mean(axis=0), full_matrices=False)[2][0]
        proj = X @ v1
        assert np.allclose(D, np.abs(proj[:, None] - proj[None, :]), atol=1e-9)
    assert not np.allclose(Dx, Dy)


# ---------------------------------------------------------------- N21


def hand_hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / np.sqrt(2.0)


def hand_sqrt_js(p, q):
    m = 0.5 * (p + q)

    def kl(a, b):
        return sum(x * np.log(x / y) for x, y in zip(a, b) if x > 0)

    return np.sqrt(0.5 * kl(p, m) + 0.5 * kl(q, m))


def test_N21_hand_values_two_point_distributions():
    p, q = np.array([1.0, 0.0]), np.array([0.5, 0.5])
    P = np.vstack([p, q])
    H = S.distribution_D(P, "hellinger")
    J = S.distribution_D(P, "sqrt_js")
    assert H[0, 1] == pytest.approx(hand_hellinger(p, q), abs=1e-12)
    assert H[0, 1] == pytest.approx(np.sqrt((1 - np.sqrt(0.5)) ** 2 / 2 + 0.25), abs=1e-12)
    assert J[0, 1] == pytest.approx(hand_sqrt_js(p, q), abs=1e-12)
    # JSD = 0.5*ln(4/3) + 0.5*(0.5*ln(2/3) + 0.5*ln 2)
    jsd = 0.5 * np.log(4 / 3) + 0.25 * np.log(2 / 3) + 0.25 * np.log(2.0)
    assert J[0, 1] == pytest.approx(np.sqrt(jsd), abs=1e-12)
    for D in (H, J):
        assert np.allclose(D, D.T) and np.all(np.diag(D) == 0)


def test_N21_bounds_and_disjoint_supports():
    rng = np.random.default_rng(3)
    P = rng.dirichlet(np.ones(6) * 0.3, size=20)
    H = S.distribution_D(P, "hellinger")
    J = S.distribution_D(P, "sqrt_js")
    assert H.min() >= 0 and H.max() <= 1 + 1e-12
    assert J.min() >= 0 and J.max() <= np.sqrt(np.log(2)) + 1e-12
    disj = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert S.distribution_D(disj, "hellinger")[0, 1] == pytest.approx(1.0, abs=1e-12)
    assert S.distribution_D(disj, "sqrt_js")[0, 1] == pytest.approx(np.sqrt(np.log(2)), abs=1e-12)


def test_N21_head():
    h = Sensitivity.head(5, 3)
    assert h.tolist() == [0, 1, 2]
    assert h.dtype == np.int64


# ---------------------------------------------------------------- N22


def test_N22_agreement_identity():
    rng = np.random.default_rng(4)
    th = rng.uniform(-np.pi, np.pi, size=50)
    assert circular_agreement(th, th) == pytest.approx(1.0, abs=1e-12)


def test_N22_agreement_rotation_invariant():
    rng = np.random.default_rng(5)
    th = rng.uniform(-np.pi, np.pi, size=50)
    for c in (0.3, 2.0, -4.1):
        assert circular_agreement(th + c, th) == pytest.approx(1.0, abs=1e-12)


def test_N22_agreement_reflection_invariant():
    rng = np.random.default_rng(6)
    th = rng.uniform(-np.pi, np.pi, size=50)
    assert circular_agreement(-th, th) == pytest.approx(1.0, abs=1e-12)
    assert circular_agreement(-th + 1.1, th) == pytest.approx(1.0, abs=1e-12)


def test_N22_agreement_hand_four_points():
    phi = np.array([0.0, 0.0, 0.0, np.pi / 2])
    theta = np.zeros(4)
    # |mean e^{i phi}| = |(3 + i)/4| = sqrt(10)/4 for both signs
    assert circular_agreement(phi, theta) == pytest.approx(np.sqrt(10) / 4, abs=1e-12)
    phi2 = np.array([0.0, 0.0, np.pi / 2, np.pi / 2])
    assert circular_agreement(phi2, theta) == pytest.approx(np.sqrt(2) / 2, abs=1e-12)


def test_N22_agreement_independent_uniform_small():
    rng = np.random.default_rng(7)
    phi = rng.uniform(0, 2 * np.pi, size=4000)
    theta = rng.uniform(0, 2 * np.pi, size=4000)
    assert circular_agreement(phi, theta) < 0.1


# ---------------------------------------------------------------- N23


def grid_3x2():
    # vertex id x*2 + y, x in 0..2, y in 0..1
    return np.array([[x, y] for x in range(3) for y in range(2)], dtype=np.float64)


def test_N23_lattice_angle_hand_values():
    coords = grid_3x2()
    states = np.arange(6)
    a0 = lattice_angle(coords, states, 0, 3.0)
    assert np.allclose(a0, 2 * np.pi * np.array([0, 0, 1, 1, 2, 2]) / 3.0)
    a1 = lattice_angle(coords, states, 1, 2.0)
    assert np.allclose(a1, np.pi * np.array([0, 1, 0, 1, 0, 1]))
    assert np.allclose(lattice_angle(coords, [5, 2], 0, 3.0), [4 * np.pi / 3, 2 * np.pi / 3])


def test_N23_belief_delta_returns_state_angle():
    coords = grid_3x2()
    b = np.eye(6)
    got = belief_angle(b, coords, 0, 3.0)
    want = lattice_angle(coords, np.arange(6), 0, 3.0)
    assert np.allclose(wrap(got - want), 0.0, atol=1e-12)
    assert np.all(got > -np.pi - 1e-12) and np.all(got <= np.pi + 1e-12)


def test_N23_belief_split_returns_midpoint():
    coords = np.array([[0.0, 0.0], [1.0, 0.0]])
    b = np.array([[0.5, 0.5]])
    assert belief_angle(b, coords, 0, 4.0)[0] == pytest.approx(np.pi / 4, abs=1e-12)
    # zero resultant (angles 0 and pi) gives 0 by the spec
    assert belief_angle(b, coords, 0, 2.0)[0] == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------- N24


def noisy_circle(M=120, d=8, noise=0.05, seed=0):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, size=M)
    X = np.zeros((M, d))
    X[:, 0], X[:, 1] = np.cos(th), np.sin(th)
    X += rng.normal(scale=noise, size=X.shape)
    return th, cdist(X, X)


def test_N24_compare_recovers_true_angle():
    th, D = noisy_circle()
    out = CircularCorrespondence(n_perm=50).compare(D, th, np.random.default_rng(10))
    assert out["status"] == "ok"
    assert out["agreement"] > 0.9
    assert out["p_value"] <= 0.02
    assert out["null_q95"] is not None and out["null_q95"] < out["agreement"]
    assert np.asarray(out["phi"]).shape == (120,)


def test_N24_compare_independent_angle_not_significant():
    _, D = noisy_circle()
    cc = CircularCorrespondence(n_perm=50)
    n_big = 0
    for s in range(5):
        rng = np.random.default_rng(100 + s)
        theta = rng.uniform(0, 2 * np.pi, size=120)
        out = cc.compare(D, theta, rng)
        assert out["status"] == "ok"
        n_big += out["p_value"] > 0.02
    assert n_big >= 4


def test_N24_collinear_points_no_h1_class():
    X = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
    out = CircularCorrespondence(n_perm=10).compare(cdist(X, X), np.array([0.0, 1.0, 2.0]),
                                                    np.random.default_rng(0))
    assert out["status"] == "no_h1_class"
    for k in ("agreement", "null_q95", "p_value", "phi"):
        assert out[k] is None


# ---------------------------------------------------------------- N25


def test_N25_errors():
    X = np.random.default_rng(0).normal(size=(6, 3))
    expect_code(ErrorCode.INVALID_CONFIG, S.activation_D, X, "cosine")
    expect_code(ErrorCode.INVALID_CONFIG, S.activation_D, X, "pca")
    expect_code(ErrorCode.INVALID_CONFIG, S.activation_D, X, "pca", X_fit=X, pca_dims=0)
    expect_code(ErrorCode.ALIGNMENT_ERROR, S.activation_D, X, "pca", X_fit=X[:, :2], pca_dims=1)
    Xz = X.copy()
    Xz[2] = 0.0
    expect_code(ErrorCode.NUMERICAL_FAILURE, S.activation_D, Xz, "chord")
    P = np.full((4, 3), 1 / 3)
    expect_code(ErrorCode.INVALID_CONFIG, S.distribution_D, P, "kl")
    for variant in Sensitivity.DISTRIBUTION_VARIANTS:
        expect_code(ErrorCode.NUMERICAL_FAILURE, S.distribution_D, P * 1.5, variant)
        Pn = P.copy()
        Pn[0] = [1.5, -0.5, 0.0]
        expect_code(ErrorCode.NUMERICAL_FAILURE, S.distribution_D, Pn, variant)
    expect_code(ErrorCode.INVALID_CONFIG, Sensitivity.head, 5, 0)
    expect_code(ErrorCode.INVALID_CONFIG, Sensitivity.head, 5, 6)
    expect_code(ErrorCode.ALIGNMENT_ERROR, circular_agreement, np.zeros(3), np.zeros(4))
    expect_code(ErrorCode.ALIGNMENT_ERROR, circular_agreement, np.zeros(0), np.zeros(0))
    coords = grid_3x2()
    expect_code(ErrorCode.ALIGNMENT_ERROR, lattice_angle, coords, [6], 0, 3.0)
    expect_code(ErrorCode.ALIGNMENT_ERROR, lattice_angle, coords, [0], 2, 3.0)
    expect_code(ErrorCode.INVALID_CONFIG, lattice_angle, coords, [0], 0, 0.0)
    expect_code(ErrorCode.ALIGNMENT_ERROR, belief_angle, np.ones((2, 5)) / 5, coords, 0, 3.0)


def test_N25_compare_errors():
    th, D = noisy_circle(M=30)
    rng = np.random.default_rng(0)
    expect_code(ErrorCode.ALIGNMENT_ERROR, CircularCorrespondence(n_perm=5).compare, D,
                th[:-1], rng)

    def zero_perm():
        return CircularCorrespondence(n_perm=0).compare(D, th, rng)

    expect_code(ErrorCode.INVALID_CONFIG, zero_perm)


# ---------------------------------------------------------------- N13


def build_store(n=6, reverse_oracle=False):
    store = memory_store()
    ws = tiny_world_spec("cylinder", n=n)
    N = n * n
    M = 36
    rng = np.random.default_rng(0)
    tokens = rng.integers(0, 3, size=(M, 33)).astype(np.uint8)
    seq = np.arange(M, dtype=np.int64)
    kw = dict(seed_map={}, consumer="experiment")
    world_id = store.save(ws, config={"w": "cyl"}, parents=[], **kw)
    obs_id = store.save(ObservationSet(split="test", V=3, sequence_id=seq, tokens=tokens),
                        config={"o": 1}, parents=[], **kw)
    xs = np.arange(M) % n
    ys = rng.integers(0, n, size=M)
    state32 = (xs * n + ys).astype(np.int16)
    z = rng.integers(0, N, size=(M, 33)).astype(np.int16)
    z[:, 31] = state32
    side_id = store.save(EvalSidecar(split="test", N=N, sequence_id=seq, z=z),
                         config={"s": 1}, parents=[], **kw)
    hashes = [tokens_hash(tokens[r, :32]) for r in range(M)]
    hids = [make_history_id("ds", int(seq[r]), 32, hashes[r]) for r in range(M)]
    hidx = HistoryIndex(dataset_id="ds", history_id=np.array(hids), sequence_id=seq,
                        end=np.full(M, 32, dtype=np.int64), panel=np.ones(M, dtype=np.int64),
                        tokens_hash=np.array(hashes), panel_size=M, n_panels=1)
    hidx_id = store.save(hidx, config={"h": 1}, parents=[obs_id], **kw)
    ang = 2 * np.pi * xs / n + rng.uniform(-0.15, 0.15, size=M)
    A = np.zeros((M, 1, 8))
    A[:, 0, 0], A[:, 0, 1] = np.cos(ang), np.sin(ang)
    A += rng.normal(scale=0.03, size=A.shape)
    logits = rng.normal(size=(M, 3)).astype(np.float32)
    act = ActivationSet(hooks=("resid_post_3",), source="model", history_id=np.array(hids),
                        A=A.astype(np.float32), logits=logits, checkpoint_id="ckpt0")
    act_id = store.save(act, config={"a": 1}, parents=[hidx_id], **kw)
    b32 = np.zeros((M, N))
    b32[np.arange(M), state32] = 1.0
    oh = np.array(hids)
    if reverse_oracle:
        oh, b32 = oh[::-1].copy(), b32[::-1].copy()
    q = np.full((M, 3), 1 / 3)
    ora = OracleOutputs(history_id=oh, b32=b32, b1=b32.copy(), q=q, q_last=q.copy(),
                        belief_entropy=np.zeros(M), log_evidence=np.zeros(M))
    ora_id = store.save(ora, config={"or": 1}, parents=[hidx_id], **kw)
    return store, act_id, side_id, world_id, ora_id


METRICS = {"agreement_x", "agreement_x_null_q95", "agreement_x_p", "agreement_control",
           "agreement_oracle_x"}


def test_N13_circular_rows_are_privileged_eval():
    store, act_id, side_id, world_id, ora_id = build_store()
    rows = CircularCorrespondence(n_perm=20).run(
        store, act_id, side_id, world_id, ora_id, "resid_post_3", 1, np.random.default_rng(0),
        world="cylinder", condition="O", replicate=1, checkpoint=0)
    assert rows
    assert METRICS <= {r.metric_id for r in rows}
    for r in rows:
        assert r.space == "privileged_eval:circular"
        assert r.run_id == act_id
        assert r.world == "cylinder" and r.condition == "O" and r.replicate == 1
        assert r.panel == 1 and r.hook == "resid_post_3"
        assert r.checkpoint is not None and r.checkpoint == 0
    by = {r.metric_id: r for r in rows}
    # delta beliefs at the true state reproduce the lattice angle exactly
    assert by["agreement_oracle_x"].value == pytest.approx(1.0, abs=1e-9)
    if by["agreement_x"].status == "ok":
        assert by["agreement_x"].value > 0.8


def test_N13_oracle_id_mismatch_raises():
    store, act_id, side_id, world_id, ora_id = build_store(reverse_oracle=True)
    expect_code(ErrorCode.SAMPLE_ID_MISMATCH, CircularCorrespondence(n_perm=5).run,
                store, act_id, side_id, world_id, ora_id, "resid_post_3", 1,
                np.random.default_rng(0), world="cylinder", condition="O", replicate=1,
                checkpoint=0)
