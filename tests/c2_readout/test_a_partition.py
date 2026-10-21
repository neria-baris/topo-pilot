"""Independent tests, author A (job 0101): T-PARTITION, T-RANDOM, T-ENERGY, T-HEADKERNEL and the
c2_attrib part of T-BOOT (the C2-M descriptive stream, NEW-5; the indicator form) (C2-FROZEN-v1
2.6, 2.8-2.10, 2.12, 6.1, 13.3). The rest of T-BOOT is in test_a_inference.py.

Targets (API.md 10, 11): ca.partition, ca.half_dot, ca.null_projector, ca.decomposition,
ca.nu_S, ca.random_ref, ca.energies, ca.cs_bound, ca.abs_mean, ca.desc_intervals,
cdc.stream_bounds, cdc.guard, cdc.r_model, cdc.licence, ck.gls, ck.interchange,
ck.code_phase, ck.r1.
Synthetic geometry only (random readout matrices and displacements; explicit centred-logit
fixtures). Expected values come from the protocol formulas evaluated in this file.

API-ASSUMPTION (API.md 11.2 leaves the format of `b` open): r_model receives, per statistic
name of 11.1 without the model suffix, the stream_bounds entry plus its guard "g" (the layout
of report.json per_model.bounds, API.md 15.2).
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402
import c1_endpoint  # noqa: E402
import c1_means  # noqa: E402
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_decide as cdc  # noqa: E402

QCODE = ("These outcomes concern the frozen, nuisance-excluding linear code defined by this "
         "fit and projector.")
VALUES = {"k": 2, "list": [1729, 2718], "other": "INC", "psi_hat": 0.05, "lower": 0.01,
          "upper": 0.08, "tau_hat": 0.05, "psi_M_hat": 0.05, "gate": "L1", "values": "-",
          "statuses": "-", "models": [1729, 2718], "registration": 0.9, "R2_code_0": 0.8,
          "rho_inc": 0.95, "intervals": "-", "theta_rot": 0.5, "interval": (0.4, 0.6),
          "s_rot": 0.9, "m": 1}


def _C(v):
    return v - v.mean(axis=1, keepdims=True)


def _half(d, v):
    return 0.5 * np.sum(d * v, axis=1)


def _geometry(n=40, p=12, seed=1):
    rng = np.random.default_rng(seed)
    M = rng.normal(size=(36, p))
    d = rng.dirichlet(np.ones(36), n) - rng.dirichlet(np.ones(36), n)
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    Sigma = (U * rng.uniform(0.5, 2.0, p)) @ U.T
    g = ck.gls(rng.normal(size=(p, 5)), rng.normal(size=(p, 2)), (Sigma + Sigma.T) / 2)
    return M, d, rng.normal(size=(n, p)), g, (Sigma + Sigma.T) / 2


def _stats(d, M, dy, P_S, P_G, G, Sigma):
    part, en = ca.partition(d, M, dy, P_S, P_G), ca.energies(M, dy, P_S)
    r = ca.random_ref(M, Sigma, dy, en["e_full"])["r"]
    return {"V3x": part["A_full"] - 0.3 * G, "Y1": -np.ones(len(d)),
            "Z010": part["A_S"] - 0.1 * part["A_full"],
            "Z050": part["A_S"] - 0.5 * part["A_full"],
            "Vabs": en["e_S"] - 0.1 * en["e_full"], "Vrand": en["e_S"] - (127 / 60) * r,
            "NEG": part["A_S"]}, part, en


def _b(stats, model=1729, draws=2000):
    keyed = {f"{s}|{model}": np.asarray(v, dtype=np.float64) for s, v in stats.items()}
    res = cdc.stream_bounds(keyed, cc.seed("test_R"), cc.ALPHA["R"], draws=draws)
    return {s: dict(res[f"{s}|{model}"], g=cdc.guard(stats[s])) for s in stats}


# ---- T-PARTITION -----------------------------------------------------------------------------
def test_partition_sums_exactly_and_matches_closed_forms():
    M, d, dy, g, _ = _geometry()
    out = ca.partition(d, M, dy, g["P_S"], g["P_G"])
    assert np.array_equal(out["A_rest"], out["A_full"] - out["A_S"] - out["A_G"])
    assert np.max(np.abs(out["A_S"] + out["A_G"] + out["A_rest"] - out["A_full"])) <= 1e-12
    for key, P in (("A_full", np.eye(12)), ("A_S", g["P_S"]), ("A_G", g["P_G"]),
                   ("A_rest", g["P_rest"])):
        assert np.max(np.abs(out[key] - _half(d, (dy @ P.T) @ M.T))) <= 1e-11
    v = dy @ M.T
    assert np.array_equal(ca.half_dot(d, v), c1_endpoint.A_hat(d, v, np.zeros_like(v)))


def test_lemma_d1_interventional_identity_and_source_independence():
    M, d, dy, g, _ = _geometry(seed=2)
    rng = np.random.default_rng(2)
    y2 = rng.normal(size=dy.shape)
    y1 = y2 + dy
    WUb = rng.normal(size=36)
    z = lambda y: WUb + y @ M.T  # noqa: E731  (Lemma R iii)
    A_S = ca.partition(d, M, y1 - y2, g["P_S"], g["P_G"])["A_S"]
    y21, y12 = ck.interchange(y1, y2, g["P_S"])
    assert np.max(np.abs(ca.half_dot(d, z(y21) - z(y2)) - A_S)) <= 1e-11
    assert np.max(np.abs(ca.half_dot(d, z(y1) - z(y12)) - A_S)) <= 1e-11
    shift = rng.normal(size=(36, 12))[rng.integers(0, 36, len(d))] + rng.normal(size=dy.shape)
    moved = ca.partition(d, M, (y1 + shift) - (y2 + shift), g["P_S"], g["P_G"])
    base = ca.partition(d, M, y1 - y2, g["P_S"], g["P_G"])
    for key in ("A_full", "A_S", "A_G", "A_rest"):  # alpha_w and the source state cancel
        assert np.max(np.abs(moved[key] - base[key])) <= 1e-11


def test_lemma_d2_logit_and_log_softmax_forms_agree_when_sum_d_is_zero():
    rng = np.random.default_rng(3)
    q1, q2 = rng.dirichlet(np.ones(36), 30), rng.dirichlet(np.ones(36), 30)
    d = q1 / q1.sum(1, keepdims=True) - q2 / q2.sum(1, keepdims=True)
    z1, z2 = rng.normal(0.0, 4.0, (30, 36)), rng.normal(0.0, 4.0, (30, 36))
    lse = lambda z: z - np.log(np.sum(np.exp(z), axis=1, keepdims=True))  # noqa: E731
    assert np.max(np.abs(ca.half_dot(d, lse(z1) - lse(z2)) - ca.half_dot(d, z1 - z2))) <= 1e-12


def _null_fixture():
    rng = np.random.default_rng(4)
    M = rng.normal(size=(36, 12))
    M[:, 10] = 0.5  # a constant logit column: C M e10 = 0
    M[:, 11] = M[:, 0] + M[:, 1]  # C M (e0 + e1 - e11) = 0
    return M


def test_null_projector_is_the_orthogonal_projector_onto_ker_CM():
    M = _null_fixture()
    J = ca.null_projector(M)
    CM = M - M.mean(axis=0)
    assert J.shape == (12, 12)
    assert np.max(np.abs(J - J.T)) <= 1e-12 and np.max(np.abs(J @ J - J)) <= 1e-12
    assert np.max(np.abs(CM @ J)) <= 1e-12 and abs(np.trace(J) - 2.0) <= 1e-12
    e10 = np.eye(12)[10]
    assert np.max(np.abs(J @ e10 - e10)) <= 1e-12


def test_operator_decomposition_sums_and_converts_null_source_variation():
    M = _null_fixture()
    J = ca.null_projector(M)
    _, d, dy, g, _ = _geometry(seed=5)
    dec = ca.decomposition(d, M, dy, g["P_S"], J)
    A_S = ca.partition(d, M, dy, g["P_S"], g["P_G"])["A_S"]
    assert np.max(np.abs(dec["A_vis"] + dec["A_null"] - A_S)) <= 1e-11
    I = np.eye(12)
    assert np.max(np.abs(dec["e_vis"] - np.sum(_C((dy @ (I - J).T @ g["P_S"].T) @ M.T) ** 2,
                                                1))) <= 1e-9
    assert np.max(np.abs(dec["e_null"] - np.sum(_C((dy @ J.T @ g["P_S"].T) @ M.T) ** 2, 1))) \
        <= 1e-9
    P = np.outer(np.eye(12)[0], np.eye(12)[0] + np.eye(12)[10])  # oblique: maps e10 to e0
    assert np.max(np.abs(P @ P - P)) == 0.0
    t = np.linspace(0.5, 1.5, 20)[:, None]
    dyn = t * np.eye(12)[10]  # a readout-null source displacement
    dn = np.tile(_C((M @ np.eye(12)[0])[None, :]) / 10.0, (20, 1))
    assert np.max(np.abs(_C((dyn @ J.T) @ M.T))) <= 1e-12  # C M J dy = 0
    out = ca.decomposition(dn, M, dyn, P, J)
    assert np.min(np.abs(out["A_null"])) > 1e-3 and np.min(out["e_null"]) > 1e-3
    assert np.max(np.abs(out["A_vis"])) <= 1e-12
    nu = ca.nu_S(J, g["P_S"], dy)
    ref = np.mean(np.sum((dy @ g["P_S"].T @ J.T) ** 2, 1)) / np.mean(
        np.sum((dy @ g["P_S"].T) ** 2, 1))
    assert abs(nu - ref) <= 1e-12 * max(1.0, ref)


# ---- T-RANDOM --------------------------------------------------------------------------------
def test_random_subspace_constants_exact():
    k, n = 6, 127
    a = Fraction(k * (n * (k + 1) - 2), n * (n + 2) * (n - 1))
    b = Fraction(k * (n - k), n * (n + 2) * (n - 1))
    assert (a, b) == (Fraction(887, 344043), Fraction(121, 344043))
    assert a + n * b == Fraction(6, 127)
    assert Fraction(cc.RS_A) == a and Fraction(cc.RS_B) == b and int(cc.RS_K) == 6
    assert Fraction(cc.E_RAND) == Fraction(127, 60) == Fraction(1, 10) / Fraction(6, 127)
    assert Fraction(cc.E_RAND) * (a + n * b) == Fraction(1, 10)  # isotropic: both 0.10


def test_rs1_rs2_monte_carlo_against_random_ref():
    rng = np.random.default_rng(6)
    p, draws = 127, 6000
    M = rng.normal(size=(36, p))
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    lam = rng.uniform(0.5, 2.0, p)
    Sigma = (U * lam) @ U.T
    S_half, S_ihalf = (U * np.sqrt(lam)) @ U.T, (U / np.sqrt(lam)) @ U.T
    dy = rng.normal(size=(2, p)) @ S_half
    d = rng.dirichlet(np.ones(36), 2) - rng.dirichlet(np.ones(36), 2)
    e_full = np.sum(_C(dy @ M.T) ** 2, axis=1)
    ref = ca.random_ref(M, Sigma, dy, e_full)
    CM = M - M.mean(axis=0)
    assert abs(ref["tau_K"] - np.trace(CM @ Sigma @ CM.T)) <= 1e-9 * ref["tau_K"]
    assert np.max(np.abs(ref["wtw"] - np.sum((dy @ np.linalg.inv(Sigma)) * dy, 1))) <= 1e-9
    r_expect = float(cc.RS_A) * e_full + float(cc.RS_B) * ref["tau_K"] * ref["wtw"]
    assert np.max(np.abs(ref["r"] - r_expect) / r_expect) <= 1e-12
    w = dy @ S_ihalf
    al, en = np.empty((draws, 2)), np.empty((draws, 2))
    for i in range(draws):
        Q = np.linalg.qr(rng.normal(size=(p, 6)))[0]
        v = ((w @ Q) @ Q.T) @ S_half  # P_R dy = Sigma^(1/2) Pi Sigma^(-1/2) dy
        al[i], en[i] = _half(d, v @ M.T), np.sum(_C(v @ M.T) ** 2, axis=1)
    A_full = _half(d, dy @ M.T)
    for est, target in ((al, 6 / 127 * A_full), (en, ref["r"])):
        se = est.std(axis=0) / math.sqrt(draws)
        assert np.all(np.abs(est.mean(axis=0) - target) <= 5 * se)


# ---- T-ENERGY --------------------------------------------------------------------------------
def test_energies_match_definitions_and_isotropic_ratio_is_one_tenth():
    M, d, dy, g, Sigma = _geometry(seed=7)
    en = ca.energies(M, dy, g["P_S"])
    assert np.max(np.abs(en["e_full"] - np.sum(_C(dy @ M.T) ** 2, 1))) <= 1e-9
    assert np.max(np.abs(en["e_S"] - np.sum(_C(dy @ g["P_S"].T @ M.T) ** 2, 1))) <= 1e-9
    rng = np.random.default_rng(7)
    Mi, dyi = rng.normal(size=(36, 127)), rng.normal(size=(6000, 127))
    e_full = np.sum(_C(dyi @ Mi.T) ** 2, 1)
    r = ca.random_ref(Mi, np.eye(127), dyi, e_full)["r"]
    assert abs((127 / 60) * r.mean() / e_full.mean() - 0.10) <= 0.002


def _cfix(n=2000, s=1.0, oblique=True):
    """Centred-logit fixture: d = (e0 - e1)/2, M columns e0-e1, e2-e3, e4-e5, e6-e7 (p = 4)."""
    E = np.eye(36)
    M = np.column_stack((E[0] - E[1], E[2] - E[3], E[4] - E[5], E[6] - E[7]))
    d = np.tile(0.5 * (E[0] - E[1]), (n, 1))
    sgn = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
    dy = np.column_stack((2 * np.ones(n), np.zeros(n), 3 * np.ones(n), sgn * s))
    P = np.outer([1.0, 0, 0, 1.0], [0, 0, 0, 1.0]) if oblique else np.diag([0, 0, 0, 1.0])
    return d, M, dy, P


def test_cancellation_fixture_energy_blocks_not_used():
    d, M, dy, P = _cfix()
    st, part, en = _stats(d, M, dy, P, np.zeros((4, 4)), 2 * np.ones(len(d)), np.eye(4))
    assert abs(part["A_S"].mean()) <= 1e-12 and np.min(np.abs(part["A_S"])) == 0.5
    out = cdc.r_model(_b(st), False)
    assert out["status"] == "LOW_ALIGNED"


def test_orthogonal_movement_fixture_gives_zero_share_low_aligned():
    d, M, dy, P = _cfix(s=2.0, oblique=False)
    st, part, en = _stats(d, M, dy, P, np.zeros((4, 4)), 2 * np.ones(len(d)), np.eye(4))
    assert np.all(part["A_S"] == 0.0) and np.min(en["e_S"]) > 1.0
    assert cdc.r_model(_b(st), False)["status"] == "LOW_ALIGNED"


def test_cauchy_schwarz_bound_holds_and_matches_its_formula():
    M, d, dy, g, _ = _geometry(n=200, seed=8)
    A_S = ca.partition(d, M, dy, g["P_S"], g["P_G"])["A_S"]
    e_S = ca.energies(M, dy, g["P_S"])["e_S"]
    E = np.arange(200) % 5 != 0
    bound = ca.cs_bound(d, e_S, E)
    ref = 0.5 * math.sqrt(np.mean(np.sum(d[E] ** 2, 1))) * math.sqrt(np.mean(e_S[E]))
    assert abs(bound - ref) <= 1e-12 * ref
    assert abs(ca.abs_mean(A_S, E) - np.mean(np.abs(A_S[E]))) <= 1e-12
    assert ca.abs_mean(A_S, E) <= bound


def test_opposition_fixture_rc4_not_used_with_negative_qualifier_and_licence():
    n = 400
    E = np.eye(36)
    u1, u2 = (E[0] - E[1]) / math.sqrt(2), (E[2] - E[3]) / math.sqrt(2)
    M = np.column_stack((u1, u2))  # orthonormal centred-logit coordinates
    dy = np.tile([1.0, 100.0], (n, 1)) * (1 + 0.01 * np.sin(np.arange(n)))[:, None]
    P = np.array([[1.0, -0.02], [0.0, 0.0]])  # P (1, 100) = (-1, 0): the code opposes
    d = np.tile(E[0] - E[1], (n, 1))  # the oracle contrast along the first coordinate
    st, part, en = _stats(d, M, dy, P, np.zeros((2, 2)), np.ones(n), np.eye(2))
    assert np.max(np.abs(part["A_S"] / part["A_full"] + 1.0)) <= 1e-12  # psi = -1
    share = en["e_S"].mean() / en["e_full"].mean()
    assert abs(share - 1 / 10001) <= 1e-9
    out = cdc.r_model(_b(st), False)
    assert out["status"] == "NOT_USED" and bool(out["negative"])
    text = cdc.licence("R", "NOT_USED", VALUES)
    assert "negative" in text and "opposing" in text and QCODE in text
    assert "below 10% in magnitude" not in text


# ---- T-HEADKERNEL (X 11 item 5) --------------------------------------------------------------
def test_circle_code_in_the_head_kernel_is_a_valid_not_used():
    n, p = 600, 12
    rng = np.random.default_rng(9)
    I = np.eye(p)
    Gamma = np.vstack((rng.normal(size=(8, 5)), np.zeros((4, 5))))
    B = I[:, 8:12]  # the K = 2 code lives in coordinates 8..11
    g = ck.gls(Gamma, B, np.eye(p))
    M = np.hstack((rng.normal(size=(36, 8)), np.zeros((36, 4))))  # code coordinates in ker(M)
    M -= M.mean(axis=0)
    phi = rng.uniform(-np.pi, np.pi, n)
    f = lambda ph: np.column_stack((np.cos(ph), np.sin(ph), np.cos(2 * ph),  # noqa: E731
                                    np.sin(2 * ph)))
    other = rng.normal(size=(n, 8))
    y_p = np.hstack((other + 0.5 * np.cos(phi + 1)[:, None], f(phi + 1.0)))
    y_m = np.hstack((other - 0.5 * np.cos(phi + 1)[:, None], f(phi - 1.0)))
    alpha, w32 = np.zeros((36, p)), np.zeros(n, dtype=np.int64)
    ph_p, mod_p = ck.code_phase(y_p, alpha, w32, g["L_B"])
    ph_m, mod_m = ck.code_phase(y_m, alpha, w32, g["L_B"])
    m32 = lambda ph: 0.8 * np.column_stack((np.cos(ph), np.sin(ph)))  # noqa: E731
    r1 = ck.r1(ph_p, ph_m, mod_p, mod_m, m32(phi + 1.0), m32(phi - 1.0),
               ck.zero_code_threshold(mod_p))
    assert r1["status"] == "PASS"  # the code moves with the counterfactual
    dy = y_p - y_m
    d = _C(dy @ M.T) / np.max(np.abs(_C(dy @ M.T)))
    st, part, en = _stats(d, M, dy, g["P_S"], g["P_G"], _half(d, dy @ M.T), np.eye(p))
    assert np.all(part["A_S"] == 0.0) and np.all(en["e_S"] == 0.0)  # exact zeros
    out = cdc.r_model(_b(st), False)
    assert out["resp"] and out["status"] == "NOT_USED"


# ---- T-BOOT: the C2-M descriptive stream (NEW-5) and the indicator form ---------------------
def test_cm_descriptive_stream_24_arrays_shared_indices_and_undefined():
    rng = np.random.default_rng(4)
    n, models = 48, (1729, 2718, 3141)
    names = ("A_MS", "A_MC", "I_M", "e_MS", "e_MC", "e_MF")
    nums = {f"{a}|{j}": rng.normal(0.3, 1, n) for j in models for a in names}
    dens = {f"{a}|{j}": rng.normal(1.0, 0.3, n) for j in models for a in ("A_full", "e_full")}
    dens["A_full|2718"] = np.zeros(n)  # zero original denominator
    one = np.zeros(n)
    one[7] = 1.0
    dens["e_full|3141"] = one  # some resampled denominators are zero
    nums["I_M|1729"][3] = np.nan  # a non-finite value
    pairs = [(f"{a}|{j}", f"{'A_full' if a[0] != 'e' else 'e_full'}|{j}")
             for j in models for a in names]
    assert len(nums) + len(dens) == 24
    res = ca.desc_intervals(nums, dens, pairs)
    allm = c1_means.bootstrap_means({**nums, **dens}, cc.seed("test_M_desc"), 5000)
    for num, den in pairs:
        got = res.get((num, den), res.get(f"{num}/{den}", res.get(num)))
        r = allm[num] / np.where(allm[den] == 0, np.nan, allm[den])
        undefined = (np.mean(dens[den]) == 0 or np.any(allm[den] == 0)
                     or not np.all(np.isfinite(nums[num])) or not np.all(np.isfinite(r)))
        if undefined:
            assert got == "UNDEFINED" or (isinstance(got, dict) and "UNDEFINED" in got.values())
        else:
            lo = c1_means.quantile_with_rank(r, Fraction(1, 40))[0]
            hi = c1_means.quantile_with_rank(r, Fraction(39, 40))[0]
            assert abs(got["L"] - lo) <= 1e-14 * abs(lo) and abs(got["U"] - hi) <= 1e-14 * abs(hi)
    assert sum(1 for p in pairs if p[1] in ("A_full|2718", "e_full|3141")) == 6


def test_indicator_form_sign_and_eligible_row_ratio():
    rng = np.random.default_rng(5)
    for _ in range(50):
        s, a = rng.normal(rng.normal(), 1, 40), rng.normal(1, 1, 40)
        E = rng.random(40) < 0.7
        ind = np.where(E, s, 0.0)
        assert np.sign(ind.mean()) == np.sign(s[E].mean())
        assert abs(ind.mean() / np.where(E, a, 0.0).mean() - s[E].mean() / a[E].mean()) <= \
            1e-9 * (1 + abs(s[E].mean() / a[E].mean()))
