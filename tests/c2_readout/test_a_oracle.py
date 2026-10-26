"""Independent tests, author A (job 0101; v2 update, job 0105): T-ORACLE with the y-translation
donor H^Y (D-0104-1) and T-ROT (RC-14) (C2-FROZEN-v2 2.2, 2.3, 2.11, 5.4, 5.5, 13.3), and
T-LADDER (RC-15; 6.7; targets cs.p1, cs.n_test), moved here from test_a_gls.py (400 lines).

Targets (API.md 4.2, 6.2, 6.4, 10 and erratum 19.3): cd.OFF, cd.k_y, cd.y_donor, cd.donors4,
cd.role_arrays, cd.REASONS, cd.coverage_tally, cd.rho_m_index, co2.oracle_role,
co2.oracle_split, co2.eligibility, co2.reason_flags, co2.x_leakage, co2.rotation_oracle,
ca.rotation_block, ca.y_rot, ca.rotation_arm, ck.gls.

Tiny cylinder HMM with exact rational (dyadic) weights and 36 symbols c = 6a + b: 12 periodic
x-cells (c1_oracle.m32 and the rotation index maps need x in 0..11; API.md erratum E-1) by the
two cell rows y = 5, 6, so the posterior mean row ybar(b31) falls on both sides of 5.5 and both
signs of k_Y occur. Max-degree-4 lazy walk (3/16 per neighbour), factorised emission
E = Ex(x, a) Ey(y, b). The H^Y oracle quantities are checked against an exact Fraction filter
written here; no closed form or symmetry report is used for H^Y (v2 2.2, C-4).
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
import c2_stats as cs  # noqa: E402
import precision  # noqa: E402

EX = [Fraction(1, 2), Fraction(1, 8), Fraction(1, 32), Fraction(1, 32), Fraction(1, 16),
      Fraction(1, 4)]  # by circular offset (a - x // 2) mod 6
EY5 = [Fraction(1, 16), Fraction(1, 4), Fraction(1, 2), Fraction(1, 8), Fraction(1, 32),
       Fraction(1, 32)]  # row y = 5 by symbol row b; row y = 6 uses Ey(6, b) = Ey(5, 5 - b)


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


def _canon(n=6, seed=0, rows=(1, 4)):
    """Canonical histories whose prefix symbols lie in symbol rows rows[0]..rows[1]."""
    rng = np.random.default_rng(seed)
    a, b = rng.integers(0, 6, (n, 32)), rng.integers(rows[0], rows[1] + 1, (n, 32))
    b[:, 31] = rng.integers(0, 6, n)  # w32 anywhere (it is never shifted)
    return (6 * a + b).astype(np.uint8)


def _hy_ref(H, k):
    """Independent H^Y (v2 2.2): b -> b + k on w1..w31, a and w32 kept; Y_def per row."""
    H = np.asarray(H, dtype=np.int64)
    a, b = H[:, :31] // 6, H[:, :31] % 6
    nb = b + np.asarray(k)[:, None]
    ok = np.all((nb >= 0) & (nb <= 5), axis=1)
    D = H.copy()
    D[:, :31] = 6 * a + nb
    return D, ok


def _split(T, E, pi, coords, H):
    oH = co2.oracle_role(T, E, pi, H, coords)
    k = cd.k_y(oH["b31"], coords)
    return co2.oracle_split(T, E, pi, coords, H, k), oH, k


# ---- T-ORACLE: the y-translation donor H^Y (D-0104-1) ----------------------------------------
def test_k_y_sign_rule_with_the_tie_going_to_minus_one():
    coords = _hmm()[0]
    lo, hi = np.flatnonzero(coords[:, 1] == 5), np.flatnonzero(coords[:, 1] == 6)
    b = np.zeros((4, 24))
    b[0, lo] = 1.0 / len(lo)  # ybar = 5
    b[1, hi[3]] = 1.0  # ybar = 6
    b[2, lo[0]], b[2, hi[0]] = 0.5, 0.5  # ybar = 5.5 exactly: -1
    b[3, lo[0]], b[3, hi[0]] = 0.5 + 2.0 ** -20, 0.5 - 2.0 ** -20  # ybar just below 5.5: +1
    assert (b[2] @ coords[:, 1]) == 5.5
    k = cd.k_y(b, coords)
    assert k.dtype == np.int64 and list(k) == [1, -1, -1, 1]
    full = np.array([(x, y) for x in range(12) for y in range(12)], dtype=np.float64)
    assert list(cd.k_y(np.eye(144)[[0, 11, 5, 6]], full)) == [1, -1, 1, -1]  # y = 0, 11, 5, 6


def test_y_donor_shifts_the_symbol_row_and_keeps_column_and_w32():
    H = _canon(n=40, seed=1)  # prefix rows 1..4: defined under both signs
    k = np.where(np.arange(40) % 2 == 0, 1, -1)
    HY, ydef = cd.y_donor(H, k)
    ref, ok = _hy_ref(H, k)
    assert HY.dtype == np.int64 and HY.shape == (40, 32) and bool(np.all(ydef)) and np.all(ok)
    assert np.array_equal(HY, ref)
    assert np.array_equal(HY[:, :31] // 6, H[:, :31].astype(np.int64) // 6)  # column a kept
    shift = HY[:, :31] % 6 - H[:, :31].astype(np.int64) % 6
    assert np.array_equal(shift, np.broadcast_to(k[:, None], (40, 31)))
    assert np.array_equal(HY[:, 31], H[:, 31].astype(np.int64))  # w32 kept
    four = cd.donors4(H, k)
    assert all(np.array_equal(x, y) for x, y in zip(four[:3], c1_oracle.donors(H)))
    assert np.array_equal(four[3], HY)


def test_off_grid_rule_never_clamps_or_wraps_and_forms_no_HY():
    H = _canon(n=6, seed=2).astype(np.int64)
    k = np.array([1, -1, 1, -1, 1, -1])
    H[0, 4] = 6 * 2 + 5  # row 5 under k = +1: off grid
    H[1, 9] = 6 * 3 + 0  # row 0 under k = -1: off grid
    H[2, 31] = 6 * 1 + 5  # only w32 in row 5: defined (w32 is never shifted)
    H[3, 7] = 6 * 4 + 5  # row 5 under k = -1: defined
    H[4, 7] = 6 * 0 + 0  # row 0 under k = +1: defined
    H = H.astype(np.uint8)
    HY, ydef = cd.y_donor(H, k)
    assert list(ydef) == [False, False, True, True, True, True]
    assert cd.OFF == 255 and np.all(HY[~ydef] == cd.OFF)  # never a clamped or wrapped symbol
    ref, ok = _hy_ref(H, k)
    assert np.array_equal(ok, ydef) and np.array_equal(HY[ydef], ref[ydef])
    roles = cd.role_arrays(H, k)
    for role in ("H", "Hp", "Hm"):
        assert np.array_equal(roles[role][1], np.arange(6))
    assert np.array_equal(roles["HY"][1], np.flatnonzero(ydef))
    assert np.array_equal(roles["HY"][0], ref[ydef]) and not np.any(roles["HY"][0] == cd.OFF)
    assert {"S_Y", "LIK_Y", "OFF_GRID_Y"} <= set(cd.REASONS)
    assert not {"S_REFL", "LIK_REFL"} & set(cd.REASONS)
    tally = cd.coverage_tally({r: (~ydef if r == "OFF_GRID_Y" else np.zeros(6, bool))
                               for r in cd.REASONS})
    assert tally["OFF_GRID_Y"] == 2 and sum(tally.values()) == 2


def test_oracle_split_HY_by_exact_forward_eligibility_f_y_and_x_leakage():
    coords, _, (Tq, Eq, piq), (T, E, pi) = _hmm()
    H = _canon(n=4, seed=3).astype(np.int64)
    H[2, 5], H[2, 6] = 6 * 1 + 5, 6 * 2 + 0  # rows 5 and 0 in one prefix: off grid either way
    H = H.astype(np.uint8)
    o, oH, k = _split(T, E, pi, coords, H)
    assert np.array_equal(k, np.where(oH["b31"] @ coords[:, 1] < 5.5, 1, -1))
    HY, ydef = _hy_ref(H, k)
    assert list(ydef) == [True, True, False, True]
    assert np.array_equal(o["Y_def"], ydef) and np.array_equal(o["k_Y"], k)
    TE = [[sum(Tq[i][j] * Eq[j][v] for j in range(24)) for v in range(36)] for i in range(24)]
    toks = dict(zip(("H", "Hp", "Hm"), c1_oracle.donors(H)), HY=HY)
    for role, tk in toks.items():
        for i in range(4):
            if role == "HY" and not ydef[i]:
                for key in ("b31", "b32", "q", "qbar", "s", "le"):
                    assert np.all(np.isnan(o["HY"][key][i]))  # no H^Y formed here
                continue
            b31, b32 = _filter(Tq, Eq, piq, [int(v) for v in tk[i]])
            q = [sum(b32[j] * TE[j][v] for j in range(24)) for v in range(36)]
            for key, ref in (("b31", b31), ("b32", b32), ("q", q)):
                got = np.asarray(o[role][key][i])
                assert np.max(np.abs(got / np.array([float(x) for x in ref]) - 1)) <= 1e-12
            assert abs(o[role]["qbar"][i].sum() - 1) <= 1e-15
    G, d = c1_oracle.G_hat(o["H"]["qbar"][ydef], o["HY"]["qbar"][ydef])[:2]
    assert np.array_equal(o["d_y"][ydef], d) and np.allclose(o["G_y"][ydef], G, 0, 1e-15)
    assert np.all(np.isnan(o["d_y"][~ydef])) and np.all(np.isnan(o["G_y"][~ydef]))
    G, d = c1_oracle.G_hat(o["Hp"]["qbar"], o["Hm"]["qbar"])[:2]
    assert np.array_equal(o["d_x"], d) and np.allclose(o["G_x"], G, 0, 1e-15)
    cached = co2.oracle_split(T, E, pi, coords, H, k, o_H=oH)
    for role in ("H", "HY"):
        assert np.array_equal(cached[role]["b32"], o[role]["b32"], equal_nan=True)
    el = co2.eligibility(o, 1e9)
    le_y = np.where(ydef, o["HY"]["le"], np.nan)
    assert np.array_equal(el["E_y"], ydef & np.isfinite(o["H"]["le"]) & np.isfinite(le_y))
    assert float(np.mean(el["E_y"])) == 0.75  # f_y = |E_y| / N: the OFF_GRID_Y row counts
    small = co2.eligibility(o, -1.0)
    assert not np.any(small["E_y"]) and not np.any(small["E_x"])
    fl = co2.reason_flags(o, -1.0)
    assert np.array_equal(fl["OFF_GRID_Y"], ~ydef)
    assert np.array_equal(fl["S_Y"], ydef) and not np.any(fl["LIK_Y"])  # not evaluated off grid
    lam = co2.x_leakage(o, el["E_x"], el["E_y"], coords)
    for key in ("b31", "b32"):
        mm = lambda r: c1_oracle.m32(o[r][key], coords)  # noqa: E731
        num = np.linalg.norm(mm("HY")[ydef] - mm("H")[ydef], axis=1).mean()
        den = np.linalg.norm(mm("Hp") - mm("Hm"), axis=1).mean()
        assert abs(lam[key] - num / den) <= 1e-12 * max(1.0, num / den)


def test_rho_m_index_maps_on_the_full_grid():
    rng = np.random.default_rng(1)
    coords = np.array([(x, y) for x in range(12) for y in range(12)], float)[rng.permutation(144)]
    pos = {(int(x), int(y)): i for i, (x, y) in enumerate(coords)}
    for m in (-2, -1, 1, 2):
        idx = cd.rho_m_index(coords, m)
        assert all(idx[i] == pos[((int(x) + m) % 12, int(y))] for i, (x, y) in enumerate(coords))
        assert np.array_equal(idx[cd.rho_m_index(coords, -m)], np.arange(144))
    for k in (-1, 1):
        assert np.array_equal(cd.rho_m_index(coords, 2 * k), c1_oracle.rho_index(coords, k))


@pytest.mark.parametrize("m", [1, 2])
def test_rotation_oracle_rolls_b31_and_reapplies_w32(m):
    coords, idx, _, (T, E, pi) = _hmm()
    H = _canon(n=5, seed=4)
    o = _split(T, E, pi, coords, H)[0]
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


# ---- T-LADDER (RC-15) ------------------------------------------------------------------------
MODELS = [1729, 2718, 3141]
SEEDS = {"R": (620501, 620502), "M": (620511, 620507), "S*": (620512, 620514)}


def _ladder(monkeypatch, family, pass_at):
    """Stub the kernels: record their arguments; per-model pass/fail by (array, N)."""
    rec = {"sd": [], "c": [], "cfg": [], "names": []}
    gated = ("Ztau",) if family == "M" else ("Z010", "Z050")
    arrays = {name: {j: np.full(4096, 10.0 + i) for j in MODELS}
              for i, name in enumerate(gated + ("ZM010", "VM", "Vabs"))}
    afull = {j: np.full(4096, 1.0 + 0.5 * k) for k, j in enumerate(MODELS)}

    def sd_b4(X, r4n, models, seed, draws, size):
        rec["sd"].append((seed, draws, size))
        return np.zeros((draws, len(models))), np.zeros((draws, len(models)))

    def centered(X, models, seed, draws, size):
        rec["c"].append((seed, draws, size))
        rec["names"].append(int(round(float(X[models[0]][0]) - 10.0)))
        return np.zeros((draws, len(models)))

    def summary(sd, e, models, cfg):
        rec["cfg"].append(dict(cfg))
        name = (gated + ("ZM010", "VM", "Vabs"))[rec["names"][-1]]
        per = {j: {"mde_upper": 0.0 if pass_at[name][j] and cfg["projected_N"] >=
                   pass_at[name][j] else 1e9, "power": 1.0, "sd_lower": 0.0, "sd_upper": 0.0,
                   "mde_lower": 0.0, "q_alpha": 0.0} for j in models}
        met = all(v["mde_upper"] <= cfg["alternative"] for v in per.values())
        return {"models": per, "status": "PASS" if met else "INCONCLUSIVE", "criterion_met": met}

    for name, fn in (("sd_b4_draws", sd_b4), ("centered_draws", centered),
                     ("precision_summary", summary)):
        monkeypatch.setattr(precision, name, fn)
        if hasattr(cs, name):
            monkeypatch.setattr(cs, name, fn)
    return cs.p1(family, arrays, afull, MODELS, cc.ALPHA[family]), rec, gated


@pytest.mark.parametrize("family", ["R", "M", "S*"])
def test_p1_calls_kernels_with_the_registered_cfg_and_seeds(monkeypatch, family):
    every = {n: {j: 4096 for j in MODELS} for n in ("Z010", "Z050", "Ztau", "ZM010", "VM",
                                                     "Vabs")}
    out, rec, gated = _ladder(monkeypatch, family, every)
    sd_seed, c_seed = SEEDS[family]
    assert {s for s, _, _ in rec["sd"]} == {sd_seed} and {s for s, _, _ in rec["c"]} == {c_seed}
    assert all(d == 5000 and size == 4096 for _, d, size in rec["sd"])
    assert sorted({size for _, _, size in rec["c"]}) == [4096, 8192, 16384]
    assert {(gated + ("ZM010", "VM", "Vabs"))[i] for i in rec["names"]} == set(gated)
    for cfg in rec["cfg"]:
        assert cfg["alpha"] == float(cc.ALPHA[family]) and cfg["power"] == 0.80
        assert cfg["delta"] == 0.0 and cfg["projected_N"] in (4096, 8192, 16384)
        assert abs(cfg["alternative"] - 0.10 * 1.0) <= 1e-12
    assert out["N_F"] == 4096 and out["status"] == "PASS" and list(out["precision_limited"]) == []


def _pa(**kw):
    base = {n: {j: 4096 for j in MODELS} for n in ("Z010", "Z050", "Ztau", "ZM010", "VM",
                                                    "Vabs")}
    for name, row in kw.items():
        base[name] = {**base[name], **row}  # int model keys (0102 review correction)
    return base


@pytest.mark.parametrize("pass_at, n_f, limited, status", [
    (_pa(Z010={1729: 8192}), 8192, [], "PASS"),
    (_pa(Z050={3141: None}), 4096, [3141], "PASS"),
    (_pa(Z010={2718: 16384}, Z050={3141: 8192}), 16384, [], "PASS"),
    (_pa(Z010={2718: 16384}, Z050={3141: None}), 16384, [3141], "PASS"),
    (_pa(Z010={1729: None, 2718: None}), None, None, "INCONCLUSIVE/UNDERPOWERED"),
])
def test_p1_n_f_rules_and_precision_limited(monkeypatch, pass_at, n_f, limited, status):
    out, _, _ = _ladder(monkeypatch, "R", pass_at)
    assert out["status"] == status and out["N_F"] == n_f
    if limited is not None:
        assert sorted(out["precision_limited"]) == limited


def test_n_test_is_the_max_over_alive_families():
    assert tuple(cs.n_test({"R": 8192, "M": 4096, "S*": 16384})) == (16384, 4)
    assert tuple(cs.n_test({"R": 4096, "S*": 8192})) == (8192, 2)
    assert tuple(cs.n_test({"R": 4096})) == (4096, 1)
