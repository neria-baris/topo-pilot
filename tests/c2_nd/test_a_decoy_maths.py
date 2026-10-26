"""Author A (job 0121): T-MOVE (Lemma DC4), T-GAIN (Lemma DG) and T-ILLUSION (MD-9).

Protocol C2ND-DESIGN-v1 §2.6-§2.8, §3 rows 11 and 20, §5.1; names from API.md §6, §7.3, §8.
Written from the protocol copy, API.md, CONTRACT.json, TEST_PLAN.md and the 0116 review only.
Synthetic fixtures; expected values from the protocol and independent computations here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_nd") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first: API.md §1 test imports)

# isort: split
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_decoy as ndy  # noqa: E402
import nd_driver as ndr  # noqa: E402

P, NOUT, DM = 31, 8, 32
K0 = P - NOUT  # dim ker(M) = 23 for a rank-8 readout (API.md ND-C33)
D_KEYS = {"V3x", "Y1", "Z010", "Z050", "Vabs", "Vrand", "NEG"}


def _mx(x):
    return float(np.max(np.abs(x)))


def _centre(v):
    return v - v.mean(axis=1, keepdims=True)


def _base(seed):
    rng = np.random.default_rng(seed)
    M = rng.normal(size=(NOUT, P))
    Gamma, B = rng.normal(size=(P, 5)), rng.normal(size=(P, 6))
    A = rng.normal(size=(P, P))
    Sigma = A @ A.T / P + 0.5 * np.eye(P)  # Sigma != I: an oblique P_S
    g = ck.gls(Gamma, B, Sigma)
    return dict(rng=rng, M=M, Gamma=Gamma, B=B, Sigma=Sigma, L_B=g["L_B"], P_S=g["P_S"],
                P_G=g["P_G"])


def _dx_policy():
    pol = ndr.LogitPolicy(done=ndr.GATE_ORDER[: ndr.GATE_ORDER.index("DX")])
    pol.begin("DX")
    return pol


def _bounds(arrays, seed, alpha, j=1729, draws=2000):
    res = ndc.stream_bounds({f"{s}|{j}": a for s, a in arrays.items()}, seed, alpha, draws)
    return ndc.model_bounds(res, {s: ndc.guard(a) for s, a in arrays.items()}, j)


# ---- T-MOVE (Lemma DC4) -----------------------------------------------------------------
def test_move_null_basis_and_move_map():
    f = _base(801)
    rng, M, B, L_B, Gamma = f["rng"], f["M"], f["B"], f["L_B"], f["Gamma"]
    I = np.eye(P)  # noqa: E741
    V0 = np.asarray(ndy.null_basis(M))
    assert V0.shape == (P, K0)
    assert _mx(V0.T @ V0 - np.eye(K0)) <= 1e-12 and _mx(M @ V0) <= 1e-12 * _mx(M)
    mm = ndy.move_map(B, L_B, M)
    assert mm["ok"] and mm["rank"] == 6 and not str(mm["status"]).startswith("EXCLUDED")
    U, T, Tinv = (np.asarray(mm[k]) for k in ("U", "T", "Tinv"))
    assert U.shape == (P, 6) and T.shape == (P, P) == Tinv.shape
    assert _mx(L_B @ U - np.eye(6)) <= 1e-12
    assert _mx(M @ U) <= 1e-12 * _mx(M) * _mx(U)
    # U does not depend on the orthonormal basis of ker(M): V0 -> V0 Q (own basis here)
    Q = np.linalg.qr(rng.normal(size=(K0, K0)))[0]
    W = np.linalg.svd(M)[2][NOUT:].T @ Q
    assert _mx(W @ np.linalg.pinv(L_B @ W) - U) <= 1e-12 * max(1.0, _mx(U))
    assert _mx(T - (I + (U - B) @ L_B)) <= 1e-12 * max(1.0, _mx(T))
    assert _mx(Tinv - (I + (B - U) @ L_B)) <= 1e-12 * max(1.0, _mx(Tinv))
    assert _mx(T @ Tinv - I) <= 1e-12
    assert _mx(T @ B - U) <= 1e-12 * _mx(U)
    assert _mx(T @ Gamma - Gamma) <= 1e-12 * _mx(Gamma)
    assert _mx(L_B @ T - L_B) <= 1e-12 * _mx(L_B)
    sv = np.asarray(mm["sv"])
    assert sv.shape == (6,) and sv[-1] / sv[0] >= 1e-6
    cond = float(np.linalg.cond(T, 2))
    assert abs(mm["cond_T"] - cond) <= 1e-6 * cond and cond <= 1e8


def test_move_rank_deficient_is_construction():
    f = _base(802)
    rng, M, L_B = f["rng"], f["M"], f["L_B"]
    L5 = L_B.copy()
    L5[5] = rng.normal(size=NOUT) @ M  # a code row inside row(M): rank(L_B V0) = 5
    B5 = np.linalg.pinv(L5)
    assert _mx(L5 @ B5 - np.eye(6)) <= 1e-10
    sv = np.linalg.svd(L5 @ np.linalg.svd(M)[2][NOUT:].T, compute_uv=False)
    assert sv[-1] / sv[0] < 1e-6  # fixture: the construction gate must fail
    mm = ndy.move_map(B5, L5, M)
    assert not mm["ok"] and mm["status"] == "EXCLUDED/CONSTRUCTION"


def test_move_prediction_identities_and_adapter():
    f = _base(803)
    rng, M, B, L_B, P_S, Gamma = (f[k] for k in ("rng", "M", "B", "L_B", "P_S", "Gamma"))
    I, g = np.eye(P), float(nc.G_D)  # noqa: E741
    assert _mx(P_S - B @ L_B) <= 1e-12 * _mx(P_S)
    mm = ndy.move_map(B, L_B, M)
    T, Tinv = np.asarray(mm["T"]), np.asarray(mm["Tinv"])
    Q0 = np.linalg.qr(np.column_stack([np.ones(DM), rng.normal(size=(DM, P))]))[0][:, 1:]
    WU = M @ Q0.T  # so that WU @ Q0 = M
    assert _mx(WU @ Q0 - M) <= 1e-12 * _mx(M)
    dy = rng.normal(size=(64, P))
    du, du_T = dy @ Q0.T, (dy @ T.T) @ Q0.T  # u - beta = Q0 y; decoy u' - beta = Q0 T y
    dz_null = du @ (g * WU @ (np.eye(DM) - Q0 @ P_S @ Q0.T)).T  # D-NULL head on the base
    dz_r = du_T @ (g * WU).T  # D-NULL-R: code moved by T, head g W_U
    assert _mx(dz_r - dz_null) <= 1e-12 * _mx(dz_null)
    dz_id = du_T @ (WU @ Q0 @ Tinv @ Q0.T).T  # D-ID: the move compensated
    assert _mx(dz_id - dy @ M.T) <= 1e-12 * _mx(dy @ M.T)
    # M0-D (vii) on the correct construction (heads given as readout matrices M' = W' Q0)
    # API-AMBIGUITY: API.md §6.5 adapter_identities(..., heads) does not fix the form of
    # `heads` nor the inputs of "pred_DNULLR"/"pred_DID"; heads = {kind: M'} assumed here.
    heads = {"DNULL": g * M @ (I - P_S), "DNULL1": M @ (I - P_S)}
    ai = ndy.adapter_identities(mm["V0"], mm["U"], T, Tinv, B, Gamma, L_B, M, heads)
    for k in ("V0tV0", "LBU", "MU", "TTinv", "TB", "TG", "LBT", "null_DNULL", "null_DNULL1"):
        assert ai[k] <= 1e-10, k


def test_move_ols_gls_equivariance():
    f = _base(804)
    rng, M, B, L_B, Gamma, Sigma = (f[k] for k in ("rng", "M", "B", "L_B", "Gamma", "Sigma"))
    mm = ndy.move_map(B, L_B, M)
    T, Tinv = np.asarray(mm["T"]), np.asarray(mm["Tinv"])
    n = 600
    w32, zt = np.arange(n) % 36, rng.normal(size=(n, 5))
    fh = ck.harmonics(rng.uniform(0.0, 2.0 * np.pi, n), 3)
    Y = rng.normal(size=(36, P))[w32] + zt @ Gamma.T + fh @ B.T + 0.3 * rng.normal(size=(n, P))
    f1, f2 = ck.fwl(Y, w32, zt, fh), ck.fwl(Y @ T.T, w32, zt, fh)
    for key, want in (("B", T @ f1["B"]), ("Gamma", T @ f1["Gamma"]),
                      ("resid", f1["resid"] @ T.T)):
        assert _mx(f2[key] - want) <= 1e-10 * _mx(want), key
    g1 = ck.gls(f1["Gamma"], f1["B"], Sigma)
    g2 = ck.gls(T @ f1["Gamma"], T @ f1["B"], T @ Sigma @ T.T)
    assert _mx(g2["L"] - g1["L"] @ Tinv) <= 1e-10 * _mx(g1["L"] @ Tinv)
    PT = T @ g1["P_S"] @ Tinv
    assert _mx(g2["P_S"] - PT) <= 1e-10 * max(1.0, _mx(PT))


def test_move_ledoit_wolf_equivariance():
    f = _base(805)
    rng = f["rng"]
    T = np.asarray(ndy.move_map(f["B"], f["L_B"], f["M"])["T"])
    R = rng.normal(size=(60, P)) @ (np.eye(P) + 0.3 * rng.normal(size=(P, P)))
    O = np.linalg.qr(rng.normal(size=(P, P)))[0]
    S1 = ck.ledoit_wolf(R)
    assert _mx(ck.ledoit_wolf(R @ O.T) - O @ S1 @ O.T) <= 1e-12 * _mx(S1)
    ST = T @ S1 @ T.T
    assert _mx(T @ T.T - np.eye(P)) > 1e-3  # fixture: T is not orthogonal
    assert _mx(ck.ledoit_wolf(R @ T.T) - ST) > 1e-6 * _mx(ST)


# ---- T-GAIN (Lemma DG) ------------------------------------------------------------------
GAINS = (1, 2, 6, 20)
A_TYPE, E_TYPE = ("Z010", "Z050", "NEG", "Y1"), ("Vabs", "Vrand")


def _gain_world(seed=811, n=512):
    f = _base(seed)
    rng, M, P_S = f["rng"], f["M"], f["P_S"]
    I = np.eye(P)  # noqa: E741
    y2, dy = rng.normal(size=(n, P)), rng.normal(size=(n, P))
    yY2, dyY = rng.normal(size=(n, P)), 0.7 * rng.normal(size=(n, P))
    vC, vS = (dy @ (I - P_S).T) @ M.T, (dy @ P_S.T) @ M.T
    d = _centre(vC) / _mx(vC) + 0.3 * _centre(vS) / _mx(vS)  # sum_v d_v = 0
    vY = (dyY @ (I - P_S).T) @ M.T
    dY = _centre(vY) / _mx(vY)
    A2 = rng.normal(size=(P, P))
    S2 = A2 @ A2.T / P + 0.5 * np.eye(P)
    ref = ck.gls(f["Gamma"] + 0.01 * rng.normal(size=(P, 5)),
                 f["B"] + 0.01 * rng.normal(size=(P, 6)), S2)  # the R@D refit stand-in
    refit = {"problem": "RD", "P_S": ref["P_S"], "P_G": ref["P_G"], "Sigma": S2}
    q = {}
    for g in GAINS:
        Mp = float(g) * (M @ (I - P_S))  # D-NULL head at gain g
        q[g] = (ca.pair(d, Mp, y2 + dy, y2, ref["P_S"], ref["P_G"], S2),
                ca.pair(dY, Mp, yY2 + dyY, yY2, ref["P_S"], ref["P_G"], S2))
    E_x, E_y = rng.random(n) < 0.9, rng.random(n) < 0.9
    return dict(q=q, refit=refit, E_x=E_x, E_y=E_y)


def _gain_run(w, Gx_mult, Gy_mult):
    """D arrays, bounds and d_model at every gain; Y1' active iff V3y' passes (C2 y_active)."""
    qx1, qy1 = w["q"][1]
    G_x, G_y = Gx_mult * np.asarray(qx1["A_full"]), Gy_mult * np.asarray(qy1["A_full"])
    out = {}
    for g in GAINS:
        qx, qy = w["q"][g]
        arr = nat.d_stream(qx, qy, G_x, w["E_x"], w["E_y"], refit=w["refit"])
        b = _bounds(arr, nc.seed("test_D"), nc.ALPHA["D"])
        v3y = np.where(w["E_y"], np.asarray(qy["A_full"]) - 0.3 * G_y, 0.0)
        by = _bounds({"V3y": v3y}, nc.seed("val_V3xD"), nc.VAL_ALPHA)
        y_on = by["V3y"]["L"] > by["V3y"]["g"]
        out[g] = dict(arr=arr, b=b, y_on=y_on, res=ndc.d_model(b, y_on))
    return out


def test_gain_scaling_of_arrays_and_bounds():
    # API-AMBIGUITY: API.md §7.3 d_stream(..., refit) fixes only refit["problem"]; the R@D
    # projector dict is passed with the keys "P_S", "P_G", "Sigma" in addition.
    out = _gain_run(_gain_world(), 1.0, 1.0)
    a1, b1 = out[1]["arr"], out[1]["b"]
    assert set(a1) == D_KEYS  # API.md §7.3: the seven DNULL keys when qx_r is None
    for g in GAINS:
        a, b = out[g]["arr"], out[g]["b"]
        for keys, p in ((A_TYPE, 1), (E_TYPE, 2)):
            for k in keys:
                s = float(g) ** p
                tol = 1e-12 * s * max(_mx(a1[k]), 1e-300)
                assert abs(float(np.mean(a[k])) - s * float(np.mean(a1[k]))) <= tol, (g, k)
                for side in ("L", "U"):
                    assert abs(b[k][side] - s * b1[k][side]) <= tol, (g, k, side)


def test_gain_decisions_do_not_depend_on_g():
    out = _gain_run(_gain_world(), 1.0, 1.0)  # theta' = g: V3x' and V3y' pass for all g
    first = out[1]["res"]
    assert not str(first["status"]).startswith("EXCLUDED")
    for g in GAINS:
        r = out[g]["res"]
        assert out[g]["y_on"]
        assert (r["status"], bool(r["rule6b"]), bool(r["negative"])) == (
            first["status"], bool(first["rule6b"]), bool(first["negative"])), g
    # V3x' fails at g = 1 only (theta' = g / 5 against 0.30): EXCLUDED/MODEL_HEADROOM there
    out2 = _gain_run(_gain_world(), 5.0, 1.0)
    assert out2[1]["res"]["status"] == "EXCLUDED/MODEL_HEADROOM"
    for g in GAINS[1:]:
        assert out2[g]["res"]["status"] == first["status"], g
    # Y1' activity changes only through V3y' (theta'_y = g / 5)
    out3 = _gain_run(_gain_world(), 1.0, 5.0)
    assert not out3[1]["y_on"] and all(out3[g]["y_on"] for g in GAINS[1:])
    assert not out3[1]["res"]["spec"] and all(out3[g]["res"]["spec"] for g in GAINS[1:])
    assert all(out3[g]["res"]["status"] == first["status"] for g in GAINS)


# ---- T-ILLUSION (§5.1, MD-9) ------------------------------------------------------------
def _illusion(seed=901, n=256):
    f = _base(seed)
    rng, M, P_S = f["rng"], f["M"], f["P_S"]
    J = ca.null_projector(M)  # Euclidean projector onto K = ker(CM)
    y2 = rng.normal(size=(n, P))
    dy = 2.0 * rng.normal(size=(n, P)) @ J.T + 0.5 * rng.normal(size=(n, P))
    v = ((dy @ J.T) @ P_S.T) @ M.T
    d = _centre(v) / _mx(v)
    return dict(f, J=J, d=d, y1=y2 + dy, y2=y2, dy=dy)


def test_illusion_operator_decomposition_is_report_only_arithmetic():
    w = _illusion()
    M, P_S, J, d, dy = w["M"], w["P_S"], w["J"], w["d"], w["dy"]
    assert _mx(P_S @ J - J @ P_S) > 1e-6  # the oblique P_S does not commute with J
    CM = M - M.mean(axis=0)
    assert _mx((dy @ J.T) @ CM.T) <= 1e-12 * max(1.0, _mx(dy))  # ||C M J dy|| = 0
    dec = ca.decomposition(d, M, dy, P_S, J)
    assert float(np.mean(np.abs(dec["A_null"]))) > 1e-6  # A_S^null != 0 although CMJdy = 0
    A_S = 0.5 * np.sum(d * ((dy @ P_S.T) @ M.T), axis=1)
    sc = np.maximum(1.0, np.abs(A_S))
    assert np.all(np.abs(dec["A_vis"] + dec["A_null"] - A_S) <= 1e-12 * sc)


def test_illusion_decoy_built_with_J_fails_m0d_and_dx():
    # API-AMBIGUITY: API.md §6.5 dx(arrays, policy) does not fix the per-decoy array keys;
    # the c2_attrib.pair keys under the construction projector P_S are passed for DNULL only.
    w = _illusion(902)
    M, P_S, J, B, L_B = w["M"], w["P_S"], w["J"], w["B"], w["L_B"]
    I, g = np.eye(P), float(nc.G_D)  # noqa: E741
    mm = ndy.move_map(B, L_B, M)
    heads = {"DNULL": g * M @ (I - J), "DNULL1": M @ (I - J)}
    assert _mx(heads["DNULL"] @ P_S) > 1e-6  # M' P_S != 0
    ai = ndy.adapter_identities(mm["V0"], mm["U"], mm["T"], mm["Tinv"], B, w["Gamma"], L_B,
                                M, heads)
    assert ai["null_DNULL"] > 1e-10 and ai["null_DNULL1"] > 1e-10  # M0-D (vii) fails
    qd = ca.pair(w["d"], heads["DNULL"], w["y1"], w["y2"], P_S, w["P_G"], w["Sigma"])
    res = ndy.dx({"DNULL": qd}, _dx_policy())
    assert res["per_decoy"]["DNULL"]["n_over"] > 0
    assert res["status"] == "FAIL_TECHNICAL/DECOY"


def test_illusion_euclidean_projector_decoy_still_has_null_code_readout():
    # PLAN-DEFECT (reported to the coordinator): TEST_PLAN T-ILLUSION (ii) and protocol §5.1
    # expect a decoy built with the Euclidean projector P_E = B (B'B)^-1 B' to fail M0-D (vii)
    # and DX. But (I - P_E) B = 0 exactly, so C M' B = 0 and M' P_S = M' B L_B = 0: the code
    # readout is still exactly null and both checks must pass. This test asserts the algebra.
    w = _illusion(903)
    M, P_S, B, L_B = w["M"], w["P_S"], w["B"], w["L_B"]
    I, g = np.eye(P), float(nc.G_D)  # noqa: E741
    PE = B @ np.linalg.solve(B.T @ B, B.T)
    heads = {"DNULL": g * M @ (I - PE), "DNULL1": M @ (I - PE)}
    assert _mx(heads["DNULL"] @ P_S) <= 1e-12 * _mx(heads["DNULL"]) * _mx(P_S)
    mm = ndy.move_map(B, L_B, M)
    ai = ndy.adapter_identities(mm["V0"], mm["U"], mm["T"], mm["Tinv"], B, w["Gamma"], L_B,
                                M, heads)
    assert ai["null_DNULL"] <= 1e-10 and ai["null_DNULL1"] <= 1e-10
    qd = ca.pair(w["d"], heads["DNULL"], w["y1"], w["y2"], P_S, w["P_G"], w["Sigma"])
    res = ndy.dx({"DNULL": qd}, _dx_policy())
    assert res["per_decoy"]["DNULL"]["n_over"] == 0
    assert res["status"] != "FAIL_TECHNICAL/DECOY"
