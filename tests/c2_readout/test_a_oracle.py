"""Independent tests, author A (job 0101): T-ORACLE and T-ROT (RC-14) (C2-FROZEN-v1 2.2, 2.3,
2.11, 13.3).

Targets (API.md 4.2, 6.2, 6.4, 10): cd.sigma, cd.reflect_donor, cd.donors4, cd.rho_R_index,
cd.rho_m_index, cd.symmetry_report_R, co2.oracle_role, co2.oracle_split, co2.rotation_oracle,
ca.rotation_block, ca.y_rot, ca.rotation_arm, ck.gls.

Tiny cylinder HMM with exact rational (dyadic) weights. API-AMBIGUITY: protocol 13.3 asks for
a 4 x 4 cylinder, but the index maps fixed by protocol 2.2/2.11 and API.md 4.2 are the 12-grid
maps (x, 11 - y) and ((x + m) mod 12, y), and c1_oracle.m32 needs x in 0..11. The fixture is
therefore the smallest cylinder on which those maps act: 12 x-cells (periodic) by the two
mirror rows y = 5, 6 (24 states), with a max-degree-4 lazy walk (3/16 per neighbour) and a
factorised emission E = Ex(x, a) Ey(y, b) invariant under (rho_R, sigma) and (tau shifts).
Reference posteriors are computed in exact Fractions in this file.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402,F401
import c1_oracle  # noqa: E402
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_data as cd  # noqa: E402
import c2_oracle as co2  # noqa: E402

EX = [Fraction(1, 2), Fraction(1, 8), Fraction(1, 32), Fraction(1, 32), Fraction(1, 16),
      Fraction(1, 4)]  # by circular offset (a - x // 2) mod 6
EY5 = [Fraction(1, 16), Fraction(1, 4), Fraction(1, 2), Fraction(1, 8), Fraction(1, 32),
       Fraction(1, 32)]  # row y = 5; row y = 6 is its mirror: Ey(6, b) = Ey(5, 5 - b)


def _hmm():
    coords = np.array([(x, y) for x in range(12) for y in (5, 6)], dtype=np.float64)
    idx = {(int(x), int(y)): i for i, (x, y) in enumerate(coords)}
    T = [[Fraction(0)] * 24 for _ in range(24)]
    E = [[Fraction(0)] * 36 for _ in range(24)]
    for (x, y), i in idx.items():
        for nb in (((x + 1) % 12, y), ((x - 1) % 12, y), (x, 11 - y)):
            T[i][idx[nb]] += Fraction(3, 16)
        T[i][i] += Fraction(7, 16)
        for a in range(6):
            for b in range(6):
                ey = EY5[b] if y == 5 else EY5[5 - b]
                E[i][6 * a + b] = EX[(a - x // 2) % 6] * ey
    pi = [Fraction(1, 24)] * 24
    f = lambda M: np.array([[float(v) for v in r] for r in M])  # noqa: E731
    return coords, idx, (T, E, pi), (f(T), f(E), np.full(24, 1 / 24))


def _filter(T, E, pi, tokens):
    """Exact forward filter: b_t = a_t * E[:, w_t] / norm, a_{t+1} = b_t T; returns b31, b32."""
    a, bs = list(pi), []
    for w in tokens:
        post = [a[i] * E[i][w] for i in range(24)]
        s = sum(post)
        post = [p / s for p in post]
        bs.append(post)
        a = [sum(post[i] * T[i][j] for i in range(24)) for j in range(24)]
    return bs[30], bs[31]


def _canon(n=6, seed=0):
    return np.random.default_rng(seed).integers(0, 36, (n, 32)).astype(np.uint8)


# ---- T-ORACLE --------------------------------------------------------------------------------
def test_sigma_and_reflect_donor():
    c = np.arange(36)
    assert np.array_equal(cd.sigma(c), 6 * (c // 6) + 5 - c % 6)
    assert np.array_equal(cd.sigma(cd.sigma(c)), c)
    H = _canon()
    R = cd.reflect_donor(H)
    assert R.shape == (6, 32) and R.dtype == np.int64
    assert np.array_equal(R[:, :31], cd.sigma(H[:, :31].astype(np.int64)))
    assert np.array_equal(R[:, 31], H[:, 31].astype(np.int64))
    four = cd.donors4(H)
    ref = c1_oracle.donors(H)
    assert len(four) == 4 and all(np.array_equal(a, b) for a, b in zip(four[:3], ref))
    assert np.array_equal(four[3], R)


def test_rho_R_and_rho_m_index_maps_on_the_full_grid():
    rng = np.random.default_rng(1)
    coords = np.array([(x, y) for x in range(12) for y in range(12)], float)[rng.permutation(144)]
    pos = {(int(x), int(y)): i for i, (x, y) in enumerate(coords)}
    R = cd.rho_R_index(coords)
    assert R.dtype == np.int64
    assert all(R[i] == pos[(int(x), 11 - int(y))] for i, (x, y) in enumerate(coords))
    assert np.array_equal(R[R], np.arange(144))
    for m in (-2, -1, 1, 2):
        idx = cd.rho_m_index(coords, m)
        assert all(idx[i] == pos[((int(x) + m) % 12, int(y))] for i, (x, y) in enumerate(coords))
        assert np.array_equal(idx[cd.rho_m_index(coords, -m)], np.arange(144))
    for k in (-1, 1):
        assert np.array_equal(cd.rho_m_index(coords, 2 * k), c1_oracle.rho_index(coords, k))


def test_symmetry_report_R_exact_and_perturbed():
    coords, _, _, (T, E, pi) = _hmm()
    rep = cd.symmetry_report_R(T, E, pi, coords)
    assert bool(rep["exact_invariance"]) and bool(rep["symmetry_ok"])
    assert rep["max_dev"] <= 1e-14 and rep["r_E"] == 0 and rep["eps_sym"] == 0
    h = 2.0 ** -30
    E2 = E.copy()
    E2[0, 0] += h
    E2[0, 1] -= h  # dyadic, exact, rows still sum to one
    R = cd.rho_R_index(coords)
    s = cd.sigma(np.arange(36))
    r_E = max(abs(Fraction(E2[R[z], s[v]]) / Fraction(E2[z, v]) - 1)
              for z in range(24) for v in range(36))
    rep2 = cd.symmetry_report_R(T, E2, pi, coords)
    assert rep2["r_E"] == r_E and rep2["eps_sym"] == r_E / (1 - r_E)
    assert not bool(rep2["symmetry_ok"]) and bool(rep2["exact_invariance"])
    T2 = T.copy()
    T2[0, 2] += h
    T2[0, 0] -= h
    assert not bool(cd.symmetry_report_R(T2, E, pi, coords)["exact_invariance"])


def test_exact_reflection_identity_and_closed_form_b32_of_HR():
    coords, idx, (Tq, Eq, piq), (T, E, pi) = _hmm()
    H = _canon(n=3, seed=2)
    HR = cd.reflect_donor(H)
    R = cd.rho_R_index(coords)
    for i in range(3):
        b31, _ = _filter(Tq, Eq, piq, [int(v) for v in H[i]])
        b31R, b32R = _filter(Tq, Eq, piq, [int(v) for v in HR[i]])
        assert all(b31R[R[z]] == b31[z] for z in range(24))  # b31(sigma H) = rho_R b31(H)
        u = [sum(b31R[k] * Tq[k][j] for k in range(24)) * Eq[j][int(H[i, 31])]
             for j in range(24)]
        assert b32R == [x / sum(u) for x in u]  # b32(H^R) closed form, exactly
    o = co2.oracle_split(T, E, pi, coords, H)
    cf = c1_oracle.closed_form_b32(o["H"]["b31"], T, E, H[:, 31].astype(np.int64), R)
    assert np.max(np.abs(o["HR"]["b32"] / cf - 1)) <= 1e-12


def test_oracle_split_roles_match_exact_filter_and_normalised_predictive():
    coords, _, (Tq, Eq, piq), (T, E, pi) = _hmm()
    n = 2
    H = _canon(n=n, seed=3)
    o = co2.oracle_split(T, E, pi, coords, H)
    TE = [[sum(Tq[k][j] * Eq[j][v] for j in range(24)) for v in range(36)] for k in range(24)]
    roles = dict(zip(("H", "Hp", "Hm", "HR"), cd.donors4(H)))
    for role, toks in roles.items():
        for key in ("b31", "b32", "q", "qbar", "s", "le"):
            assert key in o[role]
        for i in range(n):
            b31, b32 = _filter(Tq, Eq, piq, [int(v) for v in toks[i]])
            q = [sum(b32[k] * TE[k][v] for k in range(24)) for v in range(36)]
            for got, ref in ((o[role]["b31"][i], b31), (o[role]["b32"][i], b32),
                             (o[role]["q"][i], q)):
                assert np.max(np.abs(np.asarray(got) / np.array([float(x) for x in ref]) - 1)) \
                    <= 1e-12
        qb = o[role]["qbar"]
        assert np.max(np.abs(qb.sum(axis=1) - 1)) <= 1e-15
        assert np.max(np.abs(qb - o[role]["q"] / o[role]["q"].sum(1, keepdims=True))) <= 1e-16
    for pair, (a, b) in (("x", ("Hp", "Hm")), ("y", ("H", "HR"))):
        G, d = c1_oracle.G_hat(o[a]["qbar"], o[b]["qbar"])[:2]
        assert np.array_equal(o["d_" + pair], d) and np.allclose(o["G_" + pair], G, 0, 1e-15)
        assert np.all(o["G_" + pair] >= 0)
    assert o["nuis"].shape == (n, 5)
    single = co2.oracle_role(T, E, pi, H)  # API.md 6.2 signature (no coords): m32 not asserted
    assert np.array_equal(single["qbar"], o["H"]["qbar"])


@pytest.mark.parametrize("m", [1, 2])
def test_rotation_oracle_rolls_b31_and_reapplies_w32(m):
    coords, idx, _, (T, E, pi) = _hmm()
    H = _canon(n=5, seed=4)
    o = co2.oracle_split(T, E, pi, coords, H)
    w32 = H[:, 31].astype(np.int64)
    rot = co2.rotation_oracle(o["H"]["b31"], T, E, w32, coords, m)
    for sgn, key in ((1, "b_plus"), (-1, "b_minus")):
        roll = np.array([idx[((int(x) + sgn * m) % 12, int(y))] for x, y in coords])
        t = np.zeros_like(o["H"]["b31"])
        t[:, roll] = o["H"]["b31"]  # mass at x moves to x + sgn m
        u = (t @ T) * E[:, w32].T
        assert np.max(np.abs(rot[key] / (u / u.sum(1, keepdims=True)) - 1)) <= 1e-13
    for key, b in (("q_plus", rot["b_plus"]), ("q_minus", rot["b_minus"])):
        q = (b @ T) @ E
        assert np.max(np.abs(rot[key] - q / q.sum(1, keepdims=True))) <= 1e-15
    assert np.max(np.abs(rot["d"] - (rot["q_plus"] - rot["q_minus"]))) == 0.0
    assert np.allclose(rot["G"], c1_oracle.G_hat(rot["q_plus"], rot["q_minus"])[0], 0, 1e-15)
    if m == 2:  # the oracle side equals the natural-donor closed form b32(H+-)
        for key, role in (("b_plus", "Hp"), ("b_minus", "Hm")):
            assert np.max(np.abs(rot[key] / o[role]["b32"] - 1)) <= 1e-12


# ---- T-ROT (RC-14) ---------------------------------------------------------------------------
def _f(phi, K):
    return np.array([g(k * phi) for k in range(1, K + 1) for g in (np.cos, np.sin)])


@pytest.mark.parametrize("theta", [np.pi / 6, np.pi / 3])
def test_frozen_orientation_rotates_every_harmonic_by_k_theta(theta):
    for K in (1, 2, 3):
        R = ca.rotation_block(K, theta)
        assert R.shape == (2 * K, 2 * K)
        assert np.max(np.abs(R @ _f(0.3, K) - _f(0.3 + theta, K))) <= 1e-15
        for k in range(1, K + 1):
            blk = R[2 * k - 2:2 * k, 2 * k - 2:2 * k]
            ref = np.array([[np.cos(k * theta), -np.sin(k * theta)],
                            [np.sin(k * theta), np.cos(k * theta)]])
            assert np.max(np.abs(blk - ref)) <= 1e-15
        assert np.count_nonzero(R - np.kron(np.eye(K), np.ones((2, 2))) * R) == 0


def _rot_world(n=300, seed=5):
    rng = np.random.default_rng(seed)
    p = 12
    Gamma, B = rng.normal(size=(p, 5)), rng.normal(size=(p, 6))
    g = ck.gls(Gamma, B, np.eye(p))
    phi = rng.uniform(-np.pi, np.pi, n)
    alpha, w32 = rng.normal(size=(36, p)), rng.integers(0, 36, n)
    Y = alpha[w32] + rng.normal(size=(n, 5)) @ Gamma.T + np.array([_f(x, 3) for x in phi]) @ B.T
    return g, B, alpha, w32, Y, phi


def test_y_rot_rotates_the_code_and_holds_every_other_coordinate():
    g, B, alpha, w32, Y, _ = _rot_world()
    th = np.pi / 6
    yr = ca.y_rot(Y, alpha, w32, B, g["L_B"], th)
    code = (Y - alpha[w32]) @ g["L_B"].T
    assert np.max(np.abs((yr - alpha[w32]) @ g["L_B"].T - code @ ca.rotation_block(3, th).T)) \
        <= 1e-10
    assert np.max(np.abs(yr @ g["L_G"].T - Y @ g["L_G"].T)) <= 1e-10
    assert np.max(np.abs(yr @ g["P_rest"].T - Y @ g["P_rest"].T)) <= 1e-10


@pytest.mark.parametrize("m, theta", [(1, np.pi / 6), (2, np.pi / 3)])
def test_exact_sign_fixture_plus_theta_moves_toward_the_plus_rolled_belief(m, theta):
    g, B, alpha, w32, Y, phi = _rot_world(seed=6)
    ang = np.array([2 * np.pi * (2 * (v // 6) + 0.5) / 12 for v in range(36)])  # column a
    # a toy head reading the first-harmonic code pair: z_v = 3 (cos a_v, sin a_v) . L_B[:2] y
    head = 3.0 * np.column_stack((np.cos(ang), np.sin(ang))) @ g["L_B"][:2]
    # the toy oracle: the pre-observation belief phase rolled by +-m cells (= +-theta); 2 theta
    # is a multiple of the 6-column period, so both normalisers agree and sign d_v = sign
    # sin(a_v - phi) = sign of the head's logit change
    pre = lambda s: np.exp(4 * np.cos(ang[None, :] - phi[:, None] - s * theta))  # noqa: E731
    qp, qm = pre(1) / pre(1).sum(1, keepdims=True), pre(-1) / pre(-1).sum(1, keepdims=True)
    d_rot = qp - qm
    G_rot = c1_oracle.G_hat(qp, qm)[0]
    E = np.ones(len(phi), dtype=bool)
    y_p = ca.y_rot(Y, alpha, w32, B, g["L_B"], theta)
    y_m = ca.y_rot(Y, alpha, w32, B, g["L_B"], -theta)
    good = ca.rotation_arm(d_rot, head, y_p, y_m, G_rot, E)
    assert np.all(good["A_rot"] > 0) and good["s_rot"] == 1.0
    ref = 0.5 * np.sum(d_rot * ((y_p - y_m) @ head.T), axis=1)
    assert np.max(np.abs(good["A_rot"] - ref)) <= 1e-12
    assert abs(good["theta_rot"] - ref.mean() / G_rot.mean()) <= 1e-12
    flipped = ca.rotation_arm(d_rot, head, y_m, y_p, G_rot, E)  # sign-flipped orientation
    assert np.all(flipped["A_rot"] < 0) and flipped["s_rot"] == 0.0
    y_z = y_p.copy()
    y_z[::3] = y_m[::3]  # A_rot,i = 0 exactly on every third row: counted as disagreement
    zero = ca.rotation_arm(d_rot, head, y_z, y_m, G_rot, E)
    assert np.all(zero["A_rot"][::3] == 0.0)
    assert zero["s_rot"] == np.count_nonzero(np.arange(len(phi)) % 3 != 0) / len(phi)
    Eh = np.arange(len(phi)) % 2 == 0
    half = ca.rotation_arm(d_rot, head, y_z, y_m, G_rot, Eh)
    sel = zero["A_rot"][Eh]
    assert half["s_rot"] == np.count_nonzero(sel > 0) / np.count_nonzero(Eh)
    assert m in (1, 2)
