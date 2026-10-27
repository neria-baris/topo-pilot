"""Author A (job 0121): T-N1, T-LNSCALE, T-LEAK and T-DOSE.

Protocol C2ND-DESIGN-v1 §2.3 (Lemma N1), §2.8 (leak), §2.9 (LN-scale split), Lemma DC3, §4.1;
names and signatures from tools/c2_nd/API.md §7, §8.1, §6.2. Written from the protocol copy,
API.md, CONTRACT.json, TEST_PLAN.md and the job 0116 review only. Synthetic fixtures; every
expected value comes from the protocol or from an independent computation in this file.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_nd") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first: API.md §1 test imports)

# isort: split
import c2_code as ck  # noqa: E402
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_decoy as ndy  # noqa: E402

P, NOUT, DM = 31, 8, 32  # readout coordinates, outputs, d_model (tiny; API.md ND-C33)
VARIANT_NAMES = ("R_E", "R_K1", "R_K2")


def _centre(v):
    return v - v.mean(axis=1, keepdims=True)


def _frame(seed, n=256):
    """Random readout M (8 x 31), oblique GLS projectors with a random SPD Sigma, two arms."""
    rng = np.random.default_rng(seed)
    Gamma, B = rng.normal(size=(P, 5)), rng.normal(size=(P, 6))
    A = rng.normal(size=(P, P))
    Sigma = A @ A.T / P + 0.5 * np.eye(P)
    g = ck.gls(Gamma, B, Sigma)
    M = rng.normal(size=(NOUT, P))
    y2 = rng.normal(size=(n, P))
    y1 = y2 + rng.normal(size=(n, P))
    dz = _centre((y1 - y2) @ M.T)
    d = dz / np.abs(dz).max() + 0.05 * _centre(rng.normal(size=(n, NOUT)))  # sum_v d_v = 0
    return dict(rng=rng, Gamma=Gamma, B=B, Sigma=Sigma, P_S=g["P_S"], P_G=g["P_G"],
                L_B=g["L_B"], M=M, y1=y1, y2=y2, d=d)


def _half_dot(d, v):
    return 0.5 * np.sum(d * v, axis=1)


def _row_ok(got, want, tol, scale):
    return bool(np.all(np.abs(np.asarray(got) - np.asarray(want)) <= tol * scale))


# ---- T-N1 (Lemma N1) ---------------------------------------------------------------------
def test_n1_subtraction_direct_arm_and_energies():
    f = _frame(101)
    d, M, y1, y2, P_S = f["d"], f["M"], f["y1"], f["y2"], f["P_S"]
    q = nat.nr_quantities(d, M, y1, y2, P_S)
    assert np.array_equal(q["A_comp"], q["A_full"] - q["A_S"])  # by subtraction, exact
    dy = y1 - y2
    A_full = _half_dot(d, dy @ M.T)
    A_S = _half_dot(d, (dy @ P_S.T) @ M.T)
    scale = np.maximum(1.0, np.abs(A_full))
    assert _row_ok(q["A_full"], A_full, 1e-12, scale)
    assert _row_ok(q["A_S"], A_S, 1e-12, scale)
    # the complement arm, computed directly through closed-form logits z = c0 + y @ M.T
    yC = nat.comp_arm(y1, y2, P_S)
    c0 = f["rng"].normal(size=NOUT) * 3.0
    direct = nat.a_comp_direct(d, c0 + yC @ M.T, c0 + y2 @ M.T)
    assert _row_ok(direct, q["A_comp"], 1e-12, scale)
    # Lemma N1 (ii): A_comp = 1/2 d' M (I - P_S) dy for an oblique P_S
    I = np.eye(P)  # noqa: E741
    assert _row_ok(q["A_comp"], _half_dot(d, (dy @ (I - P_S).T) @ M.T), 1e-12, scale)
    # energies: e_comp = ||C M (I - P_S) dy||^2, cross = e_full - e_S - e_comp (not additive)
    CM = M - M.mean(axis=0)
    vS, vC = (dy @ P_S.T) @ CM.T, (dy @ (I - P_S).T) @ CM.T
    e_full, e_S, e_comp = (np.sum(v * v, axis=1) for v in (dy @ CM.T, vS, vC))
    escale = np.maximum(1.0, e_full)
    assert _row_ok(q["e_full"], e_full, 1e-12, escale)
    assert _row_ok(q["e_S"], e_S, 1e-12, escale)
    assert _row_ok(q["e_comp"], e_comp, 1e-12, escale)
    assert np.array_equal(q["cross"], q["e_full"] - q["e_S"] - q["e_comp"])
    assert _row_ok(q["cross"], 2.0 * np.sum(vS * vC, axis=1), 1e-11, escale)
    assert np.max(np.abs(q["cross"])) > 1e-3  # the cross term is not zero in general


def test_n1_comp_arm_is_reverse_interchange():
    f = _frame(102)
    y1, y2, P_S = f["y1"], f["y2"], f["P_S"]
    yC = nat.comp_arm(y1, y2, P_S)
    scale = np.maximum(1.0, np.maximum(np.abs(y1).max(1), np.abs(y2).max(1)))[:, None]
    assert _row_ok(yC, y1 - (y1 - y2) @ P_S.T, 1e-13, scale)  # Lemma N1 (i)
    assert _row_ok(yC, y2 + (y1 - y2) @ (np.eye(P) - P_S).T, 1e-13, scale)
    assert _row_ok(yC, ck.interchange(y1, y2, P_S)[1], 1e-13, scale)  # y_S^{1<-2}


def test_n1_shares_sum_to_one():
    f = _frame(103, n=512)
    q = nat.nr_quantities(f["d"], f["M"], f["y1"], f["y2"], f["P_S"])
    mf = float(np.mean(q["A_full"]))
    assert abs(mf) > 1e-3
    psi_comp, psi = float(np.mean(q["A_comp"])) / mf, float(np.mean(q["A_S"])) / mf
    assert abs(psi_comp + psi - 1.0) <= 1e-12  # Lemma N1 (iii)


def test_n1_stream_arrays_and_sign_flips():
    f = _frame(104, n=300)
    rng, d, M, y1, y2, P_S = f["rng"], f["d"], f["M"], f["y1"], f["y2"], f["P_S"]
    n = len(d)
    E_x, E_y = rng.random(n) < 0.8, rng.random(n) < 0.7
    G_x = np.abs(rng.normal(size=n)) + 0.1
    yY2 = rng.normal(size=(n, P))
    yY1 = yY2 + 0.5 * rng.normal(size=(n, P))
    dY = _centre(rng.normal(size=(n, NOUT))) * 0.2
    q, qy = nat.nr_quantities(d, M, y1, y2, P_S), nat.nr_quantities(dY, M, yY1, yY2, P_S)
    Pv = {"R_E": ck.gls(f["Gamma"], f["B"])["P_S"],
          "R_K1": ck.gls(f["Gamma"], f["B"][:, :2], f["Sigma"])["P_S"],
          "R_K2": ck.gls(f["Gamma"], f["B"][:, :4], f["Sigma"])["P_S"]}
    variants = {v: nat.nr_quantities(d, M, y1, y2, Pv[v]) for v in VARIANT_NAMES}
    s = nat.nr_stream(q, qy, G_x, E_x, E_y, variants=variants)
    names = ["V3x", "Y1", "Zc010", "Zc050", "Wc", "Vc", "NEGc", "Zc090", "Zc100", "Z090"]
    names += [f"{v}:{z}" for v in VARIANT_NAMES for z in ("Zc010", "Zc050")]
    assert set(s) == set(names) and len(s) == 16  # API.md §7.1, keys exactly
    dy = y1 - y2
    A_full, A_S = _half_dot(d, dy @ M.T), _half_dot(d, (dy @ P_S.T) @ M.T)
    A_comp = A_full - A_S
    CM = M - M.mean(axis=0)
    e_full = np.sum((dy @ CM.T) ** 2, axis=1)
    e_comp = np.sum(((dy @ (np.eye(P) - P_S).T) @ CM.T) ** 2, axis=1)
    dyY = yY1 - yY2
    AY_full, AY_S = _half_dot(dY, dyY @ M.T), _half_dot(dY, (dyY @ P_S.T) @ M.T)
    want = {"V3x": (A_full - 0.3 * G_x, E_x), "Y1": (AY_S - 0.1 * AY_full, E_y),
            "Zc010": (A_comp - 0.1 * A_full, E_x), "Zc050": (A_comp - 0.5 * A_full, E_x),
            "Wc": (A_comp + 0.1 * A_full, E_x), "Vc": (e_comp - 0.1 * e_full, E_x),
            "NEGc": (A_comp, E_x), "Zc090": (A_comp - 0.9 * A_full, E_x),
            "Zc100": (A_comp - A_full, E_x), "Z090": (A_S - 0.9 * A_full, E_x)}
    for v in VARIANT_NAMES:
        A_Sv = _half_dot(d, (dy @ Pv[v].T) @ M.T)
        for c, z in ((0.1, "Zc010"), (0.5, "Zc050")):
            want[f"{v}:{z}"] = (A_full - A_Sv - c * A_full, E_x)
    big = np.maximum.reduce([np.ones(n), np.abs(A_full), np.abs(G_x), e_full, np.abs(AY_full)])
    for name, (w, E) in want.items():
        got = np.asarray(s[name], dtype=np.float64)
        assert got.shape == (n,)
        assert np.all(got[~E] == 0.0), name  # indicator form s 1_E
        assert _row_ok(got[E], w[E], 1e-12, big[E]), name
    # Lemma N1 (iii): Zc^c = -Z^(1-c) per row; Zc010 = -Z090
    sc = np.maximum(1.0, np.abs(A_full))
    assert _row_ok(s["Zc010"], -s["Z090"], 1e-12, sc)
    cs = ((Fraction(1, 10), "Zc010"), (Fraction(1, 2), "Zc050"), (Fraction(9, 10), "Zc090"))
    for c, z in cs:
        assert _row_ok(s[z], -np.where(E_x, A_S - float(1 - c) * A_full, 0.0), 1e-12, sc)
    assert _row_ok(s["Zc100"], -np.where(E_x, A_S, 0.0), 1e-12, sc)


def test_n1_mirrored_bounds_on_a_shared_stream():
    rng = np.random.default_rng(105)
    X = rng.normal(size=64) + 0.2
    for alpha, ranks in ((nc.ALPHA["N-R"], (67, 19934)), (nc.ALPHA["N-M"], (56, 19945))):
        res = ndc.stream_bounds({"X|1729": X, "N|1729": -X}, nc.seed("test_NR"), alpha,
                                nc.TEST_DRAWS)
        bx, bn = res["X|1729"], res["N|1729"]
        assert bn["L"] == -bx["U"] and bn["U"] == -bx["L"]  # Lemma N1 (iv), exact
        assert bn["mean"] == -bx["mean"]
        assert (bx["rank_L"], bx["rank_U"]) == ranks == (bn["rank_L"], bn["rank_U"])
        assert ranks[0] + ranks[1] == nc.TEST_DRAWS + 1
    assert nc.ALPHA["N-R"] == Fraction(1, 300) and nc.ALPHA["N-M"] == Fraction(1, 360)


# ---- T-LNSCALE (§2.9) --------------------------------------------------------------------
def test_lnscale_split_is_exact():
    rng = np.random.default_rng(201)
    n = 96
    y1, y2 = rng.uniform(-3, 3, size=(n, 16)), rng.uniform(-3, 3, size=(n, 16))
    s1, s2 = rng.uniform(0.8, 1.25, n), rng.uniform(0.8, 1.25, n)
    scale = np.maximum(1.0, np.maximum(np.abs(y1).max(1), np.abs(y2).max(1)))[:, None]
    dy_dir, dy_sig = nat.ln_split(y1, y2, s1, s2)
    assert _row_ok(dy_dir + dy_sig, y1 - y2, 1e-15, scale)
    r = (s1 / s2)[:, None]
    assert _row_ok(dy_sig, (1.0 - r) * y1, 1e-15, scale)
    assert _row_ok(dy_dir, r * y1 - y2, 1e-15, scale)
    # a pure-rescaling pair puts the whole response in the sigma part
    y2p = (s1 / s2)[:, None] * y1
    dir_p, sig_p = nat.ln_split(y1, y2p, s1, s2)
    assert _row_ok(dir_p, 0.0, 1e-15, scale)
    assert _row_ok(sig_p, y1 - y2p, 1e-15, scale)
    # symmetric version: 1/2 (sigma part of arm order 1,2 minus that of order 2,1)
    sym = 0.5 * (dy_sig - nat.ln_split(y2, y1, s2, s1)[1])
    ref = 0.5 * ((1.0 - s1 / s2)[:, None] * y1 - (1.0 - s2 / s1)[:, None] * y2)
    assert _row_ok(sym, ref, 1e-14, scale)


def test_lnscale_sigma_formula():
    # API-AMBIGUITY: API.md §7.3 gives sigma(a3, eps) = sqrt(np.var(a3, axis=1) + eps) "on
    # resid_post_3[:, 32]"; this test passes the [n, d_model] position-32 rows (2-d input).
    rng = np.random.default_rng(202)
    a3, eps = rng.normal(size=(40, DM)) * 2.0 + 0.3, 1e-5
    want = np.sqrt(np.var(a3, axis=1) + eps)
    assert np.all(np.abs(nat.sigma(a3, eps) - want) <= 1e-14 * want)


# ---- T-LEAK (§2.8) -----------------------------------------------------------------------
def test_leak_equals_refit_code_share_of_dnull():
    f = _frame(301, n=400)
    rng, d, M, P_S = f["rng"], f["d"], f["M"], f["P_S"]
    dy = f["y1"] - f["y2"]
    Mp = float(nc.G_D) * (M @ (np.eye(P) - P_S))  # D-NULL head M' = g M (I - P_S)
    Gh = f["Gamma"] + 0.02 * rng.normal(size=f["Gamma"].shape)
    Bh = f["B"] + 0.02 * rng.normal(size=f["B"].shape)
    A2 = rng.normal(size=(P, P))
    P_hat = ck.gls(Gh, Bh, A2 @ A2.T / P + 0.5 * np.eye(P))["P_S"]  # an independent refit
    leak = nat.leak(d, Mp, dy, P_hat, P_S)
    AS_refit = _half_dot(d, (dy @ P_hat.T) @ Mp.T)
    assert _row_ok(leak, AS_refit, 1e-12, np.maximum(1.0, np.abs(AS_refit)))
    by_diff = _half_dot(d, (dy @ (P_hat - P_S).T) @ Mp.T)
    assert _row_ok(leak, by_diff, 1e-13, np.maximum(1.0, np.abs(by_diff)))
    assert np.max(np.abs(leak)) > 1e-6  # a non-trivial leak
    zero = nat.leak(d, Mp, dy, P_S, P_S)
    scale = max(1.0, float(np.max(np.abs(_half_dot(d, dy @ Mp.T)))))
    assert np.max(np.abs(zero)) <= 1e-13 * scale


def test_kappa_leak_and_canonical_angles():
    f = _frame(302)
    rng, M, P_S, B = f["rng"], f["M"], f["P_S"], f["B"]
    assert abs(nat.kappa_leak(M, P_S, B)) <= 1e-12
    Bh = B + 0.05 * rng.normal(size=B.shape)
    CM = M - M.mean(axis=0)
    want = np.linalg.norm(CM @ (np.eye(P) - P_S) @ Bh, 2) / np.linalg.norm(CM @ Bh, 2)
    assert want > 1e-6 and abs(nat.kappa_leak(M, P_S, Bh) - want) <= 1e-12 * want
    ang = np.asarray(nat.canonical_angles(B, B))
    assert ang.shape == (6,) and np.all(np.abs(ang) <= 1e-7)
    # B-hat = B rotated by a known angle theta in one plane (any basis of the same span)
    Q = np.linalg.qr(B)[0]
    w = rng.normal(size=P)
    w -= Q @ (Q.T @ w)
    w /= np.linalg.norm(w)
    theta = 0.3
    Bt = Q.copy()
    Bt[:, 0] = np.cos(theta) * Q[:, 0] + np.sin(theta) * w
    Bt = Bt @ (rng.normal(size=(6, 6)) + 3.0 * np.eye(6))
    ang = np.asarray(nat.canonical_angles(Bt, B))
    assert np.all(np.diff(ang) >= 0.0)  # ascending
    assert abs(ang[-1] - theta) <= 1e-10 and np.all(np.abs(ang[:-1]) <= 1e-7)


# ---- T-DOSE (Lemma DC3) ------------------------------------------------------------------
def _psi_dose(psi, rho):
    return (1 - rho) * psi / (1 - rho * psi)


def test_dose_exact_fractions():
    rho = Fraction(23, 25)
    assert nc.RHO == rho and nc.G_D == 6
    assert _psi_dose(Fraction(4, 5), rho) == Fraction(8, 33)
    assert _psi_dose(Fraction(9, 10), rho) == Fraction(18, 43)
    grid = [Fraction(4, 5) + Fraction(k, 100) for k in range(11)]
    vals = [_psi_dose(p, rho) for p in grid]
    assert all(a < b for a, b in zip(vals, vals[1:]))  # increasing on [4/5, 9/10]
    assert all(Fraction(1, 10) < v < Fraction(1, 2) for v in vals)  # PARTIAL range
    comp = [1 - v for v in vals]
    assert min(comp) == Fraction(25, 43) and max(comp) == Fraction(25, 33)
    assert Fraction(1, 2) < Fraction(25, 43) and Fraction(25, 33) < 1


def test_dose_head_edit_on_a_synthetic_readout():
    f = _frame(401, n=512)
    rng, P_S = f["rng"], f["P_S"]
    Q0 = np.linalg.qr(np.column_stack([np.ones(DM), rng.normal(size=(DM, P))]))[0][:, 1:]
    WU = rng.normal(size=(NOUT, DM))
    M = WU @ Q0
    dz = _centre((f["y1"] - f["y2"]) @ M.T)
    d = dz / np.abs(dz).max()  # oracle-like contrast aligned with this readout (sum zero)
    W = np.asarray(ndy.head_edit("DDOSE", WU, Q0, P_S), dtype=np.float64)
    assert W.shape == (NOUT, DM)
    g, rho = float(nc.G_D), float(nc.RHO)
    Mp = W @ Q0
    want = g * (M @ (np.eye(P) - rho * P_S))
    assert np.max(np.abs(Mp - want)) <= 1e-12 * max(1.0, np.max(np.abs(want)))
    dy = f["y1"] - f["y2"]
    A_S, A_full = _half_dot(d, (dy @ P_S.T) @ M.T), _half_dot(d, dy @ M.T)
    Ap_S, Ap_full = _half_dot(d, (dy @ P_S.T) @ Mp.T), _half_dot(d, dy @ Mp.T)
    psi = float(np.mean(A_S)) / float(np.mean(A_full))
    got = float(np.mean(Ap_S)) / float(np.mean(Ap_full))
    assert abs(got - (1 - rho) * psi / (1 - rho * psi)) <= 1e-12
    assert _row_ok(Ap_S, g * (1 - rho) * A_S, 1e-12, np.maximum(1.0, np.abs(Ap_S)))
