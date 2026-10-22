"""Independent tests, author A (job 0101): T-READOUT, T-ORDER and T-GLS part 1 (Lemmas G1-G3,
the whitened-design fixtures, "B in the nuisance span"; G1 in the v2 whitened form, D-0104-2)
(C2-FROZEN-v2 2.1, 2.3, 2.5, 13.3).
T-GLS part 2 (GLS-REF) is in test_a_gls.py.

Targets (API.md 6.2, 7.2, 7.3, 8.1, 8.2): cm.helmert, cm.readout_basis, cm.readout_coords,
cm.closed_logits, cm.placed, cm.symbol_order_a/b/c, cm.two_route, co2.d_named, ck.gls,
ck.gls_identities, ck.interchange, ck.fwl, ck.f1_fwl.
Synthetic fixtures only: a one-block float64 TransformerLM (d_model 128) whose final LayerNorm
and unembedding are randomised in the test; permutations built and checked here; random GLS
problems. Expected values come from protocol 2.1, 2.3, 2.5, 7 row 9 and 9.3 T18, and from
computations in this file.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402,F401  (first: sys.path convention, API.md 1)
import c1_oracle  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_model as cm  # noqa: E402
import c2_oracle as co2  # noqa: E402
import torch  # noqa: E402

from topo_pilot.learner.config import ModelConfig  # noqa: E402
from topo_pilot.learner.model import TransformerLM  # noqa: E402

BOS = 36
DEG = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"


def _helmert_ref(n):
    out = np.zeros((n, n - 1))
    for k in range(1, n):
        s = np.sqrt(k * (k + 1.0))
        out[:k, k - 1] = 1.0 / s
        out[k, k - 1] = -k / s
    return out


def _model(gamma=None, seed=0):
    torch.manual_seed(seed)
    cfg = ModelConfig(vocab_in=37, vocab_out=36, n_layers=1, d_model=128, n_heads=4, d_mlp=64)
    model = TransformerLM(cfg).to(torch.float64).eval()
    rng = np.random.default_rng(seed)
    g = rng.uniform(0.75, 1.25, 128) if gamma is None else np.asarray(gamma, dtype=np.float64)
    with torch.no_grad():
        model.ln_final.weight.copy_(torch.from_numpy(g))
        model.ln_final.bias.copy_(torch.from_numpy(rng.normal(0.0, 0.3, 128)))
        model.unembed.weight.copy_(torch.from_numpy(rng.normal(0.0, 0.5, (36, 128))))
    return model


def _ln(model, x):
    with torch.no_grad():
        u = model.ln_final(torch.from_numpy(np.asarray(x, dtype=np.float64)))
        z = model.unembed(u)
    return u.numpy(), z.numpy()


# ---- T-READOUT -------------------------------------------------------------------------------
def test_helmert_formula_orthonormal_and_orthogonal_to_ones():
    N1 = cm.helmert(128)
    assert N1.shape == (128, 127) and N1.dtype == np.float64
    assert np.max(np.abs(N1 - _helmert_ref(128))) <= 4e-16
    assert np.max(np.abs(N1.T @ N1 - np.eye(127))) <= 1e-14
    assert np.max(np.abs(np.ones(128) @ N1)) <= 1e-13
    assert cm.helmert(4).shape == (4, 3)


def test_readout_basis_is_positive_diagonal_qr_of_diag_gamma_helmert():
    model = _model(seed=1)
    basis = cm.readout_basis(model)
    gamma = model.ln_final.weight.detach().numpy()
    beta = model.ln_final.bias.detach().numpy()
    WU = model.unembed.weight.detach().numpy()
    A = np.diag(gamma) @ _helmert_ref(128)
    Q0 = basis["Q0"]
    assert Q0.shape == (128, 127)
    assert np.max(np.abs(Q0.T @ Q0 - np.eye(127))) <= 1e-13
    R = Q0.T @ A  # Q0 R = A with R upper triangular, positive diagonal (the unique qr_pos)
    assert np.max(np.abs(np.tril(R, -1))) <= 1e-13
    assert np.all(np.diag(R) > 0)
    assert np.max(np.abs(Q0 @ R - A)) <= 1e-13
    assert np.array_equal(basis["gamma"], gamma) and np.array_equal(basis["beta"], beta)
    assert np.max(np.abs(basis["M"] - WU @ Q0)) <= 1e-13
    assert np.max(np.abs(basis["WUbeta"] - WU @ beta)) <= 1e-13
    assert basis["rank_ok"] is True or basis["rank_ok"] == np.True_
    assert float(basis["ln_eps"]) == 1e-5


def test_lemma_R_reconstruction_and_closed_logits():
    model = _model(seed=2)
    basis = cm.readout_basis(model)
    rng = np.random.default_rng(2)
    x = rng.normal(0.0, 2.0, (64, 128)) + rng.normal(0.0, 1.0, (64, 1))
    u, z = _ln(model, x)
    y = cm.readout_coords(u, basis)
    assert y.shape == (64, 127)
    beta, Q0 = basis["beta"], basis["Q0"]
    assert np.max(np.abs(y - (u - beta) @ Q0)) <= 1e-13
    resid = (u - beta) - ((u - beta) @ Q0) @ Q0.T  # u - beta lies in U0 = col(Q0)
    assert np.max(np.abs(resid)) <= 1e-12 * max(1.0, np.max(np.abs(u - beta)))
    assert np.max(np.abs(cm.placed(y, basis) - u)) <= 1e-12 * max(1.0, np.max(np.abs(u)))
    zc = cm.closed_logits(y, basis)
    assert zc.shape == (64, 36)
    assert np.max(np.abs(zc - z)) <= 1e-11 * max(1.0, np.max(np.abs(z)))
    y_hat = rng.normal(0.0, 3.0, (8, 127))  # Lemma R (iv): any y_hat, through the linear head
    with torch.no_grad():
        z_head = model.unembed(torch.from_numpy(cm.placed(y_hat, basis))).numpy()
    assert np.max(np.abs(cm.closed_logits(y_hat, basis) - z_head)) <= 1e-11 * np.max(
        np.abs(z_head))


@pytest.mark.parametrize("zeros, rank, ok", [((17,), 127, True), ((17, 90), 126, False)])
def test_rank_rule_one_zero_gamma_keeps_rank_two_zeros_do_not(zeros, rank, ok):
    gamma = np.random.default_rng(3).uniform(0.75, 1.25, 128)
    gamma[list(zeros)] = 0.0
    A = np.diag(gamma) @ _helmert_ref(128)
    assert np.linalg.matrix_rank(A) == rank
    basis = cm.readout_basis(_model(gamma=gamma, seed=3))
    assert bool(basis["rank_ok"]) is ok


def test_layernorm_eps_scale_not_removed_but_u_minus_beta_in_U0():
    model = _model(seed=4)
    basis = cm.readout_basis(model)
    gamma, beta, Q0 = basis["gamma"], basis["beta"], basis["Q0"]
    v = np.random.default_rng(4).normal(size=128)
    v -= v.mean()
    outs = {}
    for c in (1e-3, 1.0, 1e3):
        u, _ = _ln(model, (c * v)[None, :])
        cv = c * v
        expect = gamma * cv / np.sqrt(np.mean(cv * cv) + 1e-5) + beta  # epsilon = 1e-5 kept
        assert np.max(np.abs(u[0] - expect)) <= 1e-12
        d = u[0] - beta
        assert np.max(np.abs(d - Q0 @ (Q0.T @ d))) <= 1e-12 * max(1.0, np.max(np.abs(d)))
        outs[c] = u[0]
    assert np.max(np.abs(outs[1e-3] - outs[1.0])) > 1e-2  # scale is not removed (RC-16)
    y_small = cm.readout_coords(outs[1e-3][None, :], basis)
    y_one = cm.readout_coords(outs[1.0][None, :], basis)
    assert np.max(np.abs(y_small - y_one)) > 1e-2


# ---- T-ORDER (RC-1, NEW-7) -------------------------------------------------------------------
def _perm():
    cycle = (np.arange(36) + 1) % 36
    swap = np.arange(36)
    swap[[0, 5]] = [5, 0]
    return cycle[swap]  # a 36-cycle composed with a transposition


def _perm_involutive():
    p = np.arange(36)
    p[0::2], p[1::2] = np.arange(1, 36, 2), np.arange(0, 36, 2)
    return p


def _scatter(x, perm):  # independent named_from_canonical: named column perm[c] <- canonical c
    out = np.zeros_like(x)
    for c in range(36):
        out[:, perm[c]] = x[:, c]
    return out


def _patch_inverse(monkeypatch):
    wrong = lambda x, perm: np.asarray(x)[..., np.asarray(perm)]  # noqa: E731
    for mod in (c1_oracle, cm, co2):
        if hasattr(mod, "named_from_canonical"):
            monkeypatch.setattr(mod, "named_from_canonical", wrong)


def test_permutation_fixture_is_non_involutive():
    perm, inv = _perm(), _perm_involutive()
    assert sorted(perm.tolist()) == list(range(36))
    assert not np.array_equal(perm[perm], np.arange(36))
    assert not np.array_equal(perm, np.argsort(perm))
    assert np.array_equal(inv[inv], np.arange(36))


def test_d_named_scatters_canonical_into_named_order():
    rng = np.random.default_rng(5)
    d = rng.normal(size=(6, 36))
    assert np.array_equal(co2.d_named(d, _perm()), _scatter(d, _perm()))


def test_contraction_identity_and_the_wrong_conversion_differs():
    perm = _perm()
    rng = np.random.default_rng(6)
    d, zc = rng.normal(size=(8, 36)), rng.normal(0.0, 3.0, (8, 36))
    zn = _scatter(zc, perm)
    right = np.sum(co2.d_named(d, perm) * zn, axis=1)
    assert np.max(np.abs(right - np.sum(d * zc, axis=1))) <= 1e-12
    wrong = np.sum(c1_oracle.canonical_from_named_cols(d, perm) * zn, axis=1)
    assert np.min(np.abs(wrong - right)) > 1e-3


def test_an_involutive_permutation_hides_the_direction_error():
    perm = _perm_involutive()
    d = np.random.default_rng(7).normal(size=(5, 36))
    assert np.array_equal(c1_oracle.named_from_canonical(d, perm),
                          c1_oracle.canonical_from_named_cols(d, perm))


def test_symbol_order_b_accepts_correct_map_rejects_inverse(monkeypatch):
    assert bool(cm.symbol_order_b(_perm())) and bool(cm.symbol_order_b(_perm_involutive()))
    _patch_inverse(monkeypatch)
    assert not bool(cm.symbol_order_b(_perm()))


def test_symbol_order_a_accepts_correct_map_rejects_inverse():
    perm = _perm()
    canon = np.random.default_rng(8).integers(0, 36, (40, 32)).astype(np.uint8)
    bos = np.full((40, 1), BOS, dtype=np.int64)
    named = np.hstack((bos, perm[canon.astype(np.int64)]))
    assert bool(cm.symbol_order_a(named, canon, perm))
    wrong = np.hstack((bos, np.argsort(perm)[canon.astype(np.int64)]))
    assert not bool(cm.symbol_order_a(wrong, canon, perm))


def test_symbol_order_c_accepts_correct_map_rejects_inverse(monkeypatch):
    d = np.random.default_rng(9).normal(size=(12, 36))
    assert bool(cm.symbol_order_c(d, _perm()))
    _patch_inverse(monkeypatch)
    assert not bool(cm.symbol_order_c(d, _perm()))
    assert bool(cm.symbol_order_c(d, _perm_involutive()))  # the inverse is hidden here


def test_two_route_accepts_correct_map_rejects_inverse():
    perm = _perm()
    rng = np.random.default_rng(10)
    qa, qb = rng.dirichlet(np.ones(36), 16), rng.dirichlet(np.ones(36), 16)
    d = qa - qb
    zn = rng.normal(0.0, 10.0, (16, 36))
    assert bool(cm.two_route(d, co2.d_named(d, perm), zn, perm)["ok"])
    wrong = c1_oracle.canonical_from_named_cols(d, perm)
    assert not bool(cm.two_route(d, wrong, zn, perm)["ok"])


def _seq(values):
    acc = 0.0
    for v in values:
        acc = acc + v
    return acc


def test_two_route_cancellation_and_zero_rows_new7():
    perm = _perm()
    rng = np.random.default_rng(11)
    d = np.zeros((3, 36))
    zc = rng.normal(0.0, 3.0, (3, 36))
    d[0, 3], d[0, 7] = 0.5, -0.5  # 1/2 d'z is exactly 0, sum |d z| = 1
    zc[0, [3, 7]] = 1.0
    d[1, 2], d[1, 9], d[1, 35] = 0.1, 0.2, -0.3  # cancels below 1e-15, sum |d z| = 0.6
    zc[1, [2, 9, 35]] = 1.0
    d[2] = rng.normal(size=36)  # a generic row
    zn = _scatter(zc, perm)
    dn = co2.d_named(d, perm)
    s_c = [_seq(d[1] * zc[1]), _seq(dn[1] * zn[1])]  # canonical order; named order
    assert s_c[0] == 0.30000000000000004 - 0.3 and abs(s_c[0]) < 1e-15 and abs(s_c[1]) < 1e-15
    assert s_c[0] != s_c[1]  # summation order alone separates the two routes ...
    assert abs(s_c[0] - s_c[1]) > 1e-12 * abs(s_c[0])  # ... so a purely relative rule fails
    assert _seq(d[0] * zc[0]) == 0.0
    out = cm.two_route(d, dn, zn, perm)
    assert bool(out["ok"])  # the T18 rule 1e-12 * max(1, sum |d z|) passes every row
    wrong = c1_oracle.canonical_from_named_cols(d, perm)
    assert np.min(np.abs(np.sum(wrong * zn, axis=1) - np.sum(dn * zn, axis=1))[:2]) > 1e-3
    for row in range(3):
        assert not bool(cm.two_route(d[row:row + 1], wrong[row:row + 1], zn[row:row + 1],
                                     perm)["ok"])


def _problem(p=12, K=1, seed=0, spread=1.0):
    rng = np.random.default_rng(seed)
    Gamma, B = rng.normal(size=(p, 5)), rng.normal(size=(p, 2 * K))
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    Sigma = (U * np.exp(rng.uniform(-spread, spread, p))) @ U.T
    return Gamma, B, (Sigma + Sigma.T) / 2


# ---- Lemmas G1-G3 ----------------------------------------------------------------------------
@pytest.mark.parametrize("K", [1, 2, 3])
def test_g1_identities_and_closed_form(K):
    Gamma, B, Sigma = _problem(p=15, K=K, seed=K)
    g = ck.gls(Gamma, B, Sigma)
    assert g["status"] == "PASS" and g["rank_Xt"] == 5 + 2 * K and g["cond_Xt"] <= 1e8
    assert bool(ck.gls_identities(g, Gamma, B, Sigma)["ok"])
    Xn, W = np.hstack((Gamma, B)), np.linalg.inv(Sigma)
    L_ref = np.linalg.solve(Xn.T @ W @ Xn, Xn.T @ W)
    assert np.max(np.abs(g["L"] - L_ref)) <= 1e-10
    PS, PG, I = g["P_S"], g["P_G"], np.eye(15)
    assert np.max(np.abs(g["L"] @ Xn - np.eye(5 + 2 * K))) <= 1e-10
    assert np.max(np.abs(PS - B @ g["L_B"])) <= 1e-12
    assert np.max(np.abs(PG - Gamma @ g["L_G"])) <= 1e-12
    for lhs, rhs in ((PS @ PS, PS), (PG @ PG, PG), (PS @ PG, 0 * I), (PG @ PS, 0 * I)):
        assert np.max(np.abs(lhs - rhs)) <= 1e-10  # dimensionless: absolute 1e-10 (v2 2.5)
    assert np.max(np.abs(PS @ Gamma)) <= 1e-10 * np.max(np.abs(Gamma))  # relative bounds
    assert np.max(np.abs(PG @ B)) <= 1e-10 * np.max(np.abs(B))
    R = np.linalg.cholesky(Sigma).T  # Sigma = R'R (protocol factor convention)
    Pt = np.linalg.solve(R.T, (PS + PG) @ R.T)  # whitened P~ = R^-T P R'
    assert np.max(np.abs(Pt - Pt.T)) <= 1e-10
    assert np.max(np.abs(g["P_rest"] - (I - PS - PG))) <= 1e-12


def test_euclidean_variant_still_excludes_gamma():
    Gamma, B, Sigma = _problem(p=12, K=2, seed=4, spread=2.0)
    e, w = ck.gls(Gamma, B), ck.gls(Gamma, B, Sigma)
    assert e["status"] == "PASS"
    assert np.max(np.abs(e["P_S"] @ Gamma)) <= 1e-10
    assert np.max(np.abs(e["L"] @ np.hstack((Gamma, B)) - np.eye(9))) <= 1e-10
    P = e["P_S"] + e["P_G"]
    assert np.max(np.abs(P - P.T)) <= 1e-10  # W = I
    assert np.max(np.abs(e["P_S"] - w["P_S"])) > 1e-3  # only the complement metric changed
    assert bool(ck.gls_identities(e, Gamma, B)["ok"])


def test_g2_interchange_takes_code_from_arm1_and_the_rest_from_arm2():
    Gamma, B, Sigma = _problem(p=12, K=3, seed=5)
    g = ck.gls(Gamma, B, Sigma)
    rng = np.random.default_rng(5)
    y1, y2 = rng.normal(size=(20, 12)), rng.normal(size=(20, 12))
    y21, y12 = ck.interchange(y1, y2, g["P_S"])
    for a, b in ((y21 @ g["L_B"].T, y1 @ g["L_B"].T), (y21 @ g["L_G"].T, y2 @ g["L_G"].T),
                 (y21 @ g["P_rest"].T, y2 @ g["P_rest"].T), (y12 @ g["L_B"].T, y2 @ g["L_B"].T),
                 (y12 @ g["L_G"].T, y1 @ g["L_G"].T), (y12 @ g["P_rest"].T, y1 @ g["P_rest"].T)):
        assert np.max(np.abs(a - b)) <= 1e-10
    t = rng.normal(size=(20, 5))  # P_S (Delta + Gamma t) = P_S Delta
    dy = y1 - y2
    assert np.max(np.abs((dy + t @ Gamma.T) @ g["P_S"].T - dy @ g["P_S"].T)) <= 1e-10


def test_g3_monte_carlo_within_state_covariance_vanishes():
    Gamma, B, Sigma = _problem(p=10, K=1, seed=6, spread=2.0)
    n = 40000
    rng = np.random.default_rng(66)
    eps = rng.normal(size=(n, 10)) @ np.linalg.cholesky(Sigma).T
    y = eps + rng.normal(size=10)  # fixed (w, z, phi): a constant mean plus Sigma noise

    def zscores(g):
        a, b = y @ g["L"].T, y @ g["P_rest"].T
        a, b = a - a.mean(0), b - b.mean(0)
        cov = a.T @ b / n
        return np.abs(cov) / (np.outer(a.std(0), b.std(0)) / np.sqrt(n) + 1e-300)

    zg = zscores(ck.gls(Gamma, B, Sigma))
    assert np.max(zg[np.isfinite(zg)]) <= 5.0  # tolerance 5 SD of the n-row cross-covariance
    ze = zscores(ck.gls(Gamma, B))
    assert np.max(ze[np.isfinite(ze)]) > 10.0  # the Euclidean operator does not decorrelate


# ---- whitened-design fixtures (RC-10, RC-12) -------------------------------------------------
def test_rank_deficient_nuisance_plus_code_block_is_degenerate():
    Gamma, B, Sigma = _problem(p=30, K=1, seed=7)
    B1 = B.copy()
    B1[:, 0] = Gamma[:, 0]  # [Gamma, B] of rank 6 < 7
    g = ck.gls(Gamma, B1, Sigma)
    assert g["rank_Xt"] < 7 and g["status"] == DEG


def test_b_in_the_nuisance_span_is_degenerate():
    Gamma, _, Sigma = _problem(p=30, K=2, seed=8)
    C = np.random.default_rng(8).normal(size=(5, 4))
    g = ck.gls(Gamma, Gamma @ C, Sigma)  # col(B) inside col(Gamma)
    assert g["rank_Xt"] < 9 and g["status"] == DEG


def test_conditioning_above_1e8_with_a_well_conditioned_fwl_design():
    rng = np.random.default_rng(9)
    n, p = 720, 12
    w32 = np.arange(n) % 36
    phi = rng.uniform(-np.pi, np.pi, n)
    zt = rng.normal(size=(n, 5))
    f = np.column_stack((np.cos(phi), np.sin(phi)))
    Gam = rng.normal(size=(p, 5))
    Bt = Gam[:, :2] + 1e-10 * rng.normal(size=(p, 2))  # code columns almost in the nuisance span
    Y = rng.normal(size=(36, p))[w32] + zt @ Gam.T + f @ Bt.T + 1e-14 * rng.normal(size=(n, p))
    fit = ck.fwl(Y, w32, zt, f)
    assert fit["rank"] == 43 and fit["cond"] <= 1e3 and ck.f1_fwl(fit) == "PASS"
    g = ck.gls(fit["Gamma"], fit["B"], np.eye(p))
    assert g["rank_Xt"] == 7 and g["cond_Xt"] > 1e8 and g["status"] == DEG
