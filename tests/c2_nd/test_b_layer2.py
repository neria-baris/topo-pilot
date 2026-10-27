"""Author B, KM1-KM4 (protocol §2.4, §5.1) and T-RESP with ORACLE-FEAS (i) (§2.5, §3 rows 9,
21, 23, §5.1; API.md §7.2, §7.4, §8.2).

Layer-2 fixtures: tiny float64 TransformerLMs whose block 3 has zero attention output (KM1-KM3
also zero MLP output, KM4 a GELU MLP gate); the head reads a 6-d "code" subspace S of the
centred residual (or its complement). Patched states are formed by c2_attrib.cm_replacements
and run through forward_with_patch at resid_post_2/32; synthetic a2(H) and donors keep the
per-row mean and norm of a2(H) (reflections inside S and inside its complement).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import c2_attrib as ca  # noqa: E402
import c2_decide as cdc  # noqa: E402
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
import torch  # noqa: E402

from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch  # noqa: E402

N, D = 64, 32
NM_KEYS = {"V3x", "Ztau", "ZMc010", "ZMc050", "WMc", "VMc", "NEGMc"}


def spaces(seed):
    """P2: orthogonal projector onto a 6-d S inside 1-perp; PC: onto 1-perp minus S."""
    Cn = np.eye(D) - 1.0 / D
    Q = np.linalg.qr(Cn @ np.random.default_rng(seed).normal(size=(D, 6)))[0]
    P2 = Q @ Q.T
    return P2, Cn - P2


def km_model(seed, W, mlp=False):
    torch.manual_seed(seed)
    cfg = ModelConfig(vocab_in=9, vocab_out=8, d_model=D, n_heads=4, d_mlp=64)
    m = TransformerLM(cfg).double().eval()
    with torch.no_grad():
        blk = m.blocks[3]
        blk.attn.proj.weight.zero_()
        blk.attn.proj.bias.zero_()
        if mlp:  # KM4: a GELU gate whose hidden units mix code and complement coordinates
            blk.fc_in.weight.copy_(2.0 * torch.randn(64, D, dtype=torch.float64))
            blk.fc_in.bias.zero_()
            blk.fc_out.weight.copy_(torch.randn(D, 64, dtype=torch.float64))
        else:
            blk.fc_out.weight.zero_()
        blk.fc_out.bias.zero_()
        m.ln_final.weight.fill_(1.0)
        m.ln_final.bias.zero_()
        m.unembed.weight.copy_(torch.from_numpy(W))
    return m


def reflect(h, P, rng):
    e = rng.normal(size=h.shape) @ P.T
    e /= np.linalg.norm(e, axis=1, keepdims=True)
    return -2.0 * np.sum(h * e, axis=1, keepdims=True) * e


def donors(seed, P2, PC, norm_only=False):
    rng = np.random.default_rng(seed)
    h = rng.normal(size=(N, D)) + rng.normal(size=(N, 1))
    if norm_only:  # KM3: the code is unchanged, the complement is only rescaled
        hC = (h - h.mean(axis=1, keepdims=True)) @ PC.T
        return h, h + 0.6 * hC, h - 0.4 * hC
    dp = reflect(h, P2, rng) + reflect(h, PC, rng)
    dm = reflect(h, P2, rng) + reflect(h, PC, rng)
    return h, h + dp, h + dm


def zpatch(model, X, rep):
    with torch.no_grad():
        out = forward_with_patch(model, X, "resid_post_2", 32, torch.from_numpy(rep))
    return out.logits[:, 32].numpy().copy()


def run_km(model, P2, h, Dp, Dm):
    x = np.random.default_rng(4).integers(0, 8, size=(N, 33))
    x[:, 0] = 8
    X = torch.as_tensor(x, dtype=torch.int64)
    rp, rm = ca.cm_replacements(h, Dp, P2), ca.cm_replacements(h, Dm, P2)
    z = {k: (zpatch(model, X, rp[k]), zpatch(model, X, rm[k])) for k in ("F", "S", "C")}
    dzF = z["F"][0] - z["F"][1]
    d = dzF / np.linalg.norm(dzF, axis=1, keepdims=True)  # A_F > 0 on every row
    A_full = ca.half_dot(d, dzF)
    return ca.cm_quantities(d, z, A_full), A_full, rp, rm


def shares(cm_):
    mF = float(np.mean(cm_["A_F"]))
    return (float(np.mean(cm_["A_S"])) / mF, float(np.mean(cm_["A_C"])) / mF,
            float(np.mean(cm_["I_M"])) / mF)


def bounds(arrays, seed=630505, alpha=Fraction(1, 360), draws=2000):
    res = cdc.stream_bounds(arrays, seed, alpha, draws)
    return {k: dict(v, g=cdc.guard(arrays[k], 0.0)) for k, v in res.items()}


def nm_status(cm_, A_full):
    E = np.ones(N, dtype=bool)
    arrays = nat.nm_stream(cm_, A_full, A_full, E)  # G_x = A_full: theta = 1, V3x passes
    assert set(arrays) == NM_KEYS
    return ndc.nm_model(bounds(arrays))["status"], arrays


def test_km1_code_only_head_is_necessary_m():
    P2, PC = spaces(1)
    W = np.random.default_rng(2).normal(size=(8, D)) @ P2
    h, Dp, Dm = donors(3, P2, PC)
    cm_, A_full, rp, rm = run_km(km_model(21, W), P2, h, Dp, Dm)
    psi, psi_c, _ = shares(cm_)
    scale = max(1.0, float(np.mean(np.abs(cm_["A_F"]))))
    assert abs(psi - 1.0) <= 1e-12 and abs(psi_c) <= 1e-12
    assert float(np.max(np.abs(cm_["I_M"]))) <= 1e-12 * scale
    for r in (rp, rm):  # every patched state keeps the LayerNorm scale of a2(H)
        for k in ("F", "S", "C"):
            ratio = ca.ln_scale_ratio(r[k], h, 1e-5)
            assert float(np.max(np.abs(ratio - 1.0))) <= 1e-12
    assert nm_status(cm_, A_full)[0] == "NECESSARY_M"


def test_km2_complement_only_head_is_not_necessary_m():
    P2, PC = spaces(1)
    W = np.random.default_rng(2).normal(size=(8, D)) @ PC
    cm_, A_full, _, _ = run_km(km_model(21, W), P2, *donors(3, P2, PC))
    psi, psi_c, _ = shares(cm_)
    assert abs(psi) <= 1e-12 and abs(psi_c - 1.0) <= 1e-12
    assert nm_status(cm_, A_full)[0] == "NOT_NECESSARY_M"


def test_km3_layernorm_scale_loophole():
    """The head reads only S and the code is the same in both donors; the complement changes
    the row norm only, yet psi_M,comp is far from 0: the code is not shown necessary."""
    P2, PC = spaces(1)
    W = np.random.default_rng(2).normal(size=(8, D)) @ P2
    model = km_model(21, W)
    assert float(np.max(np.abs(W @ PC))) <= 1e-12  # the code is the sole readout input
    h, Dp, Dm = donors(5, P2, PC, norm_only=True)
    cm_, A_full, rp, rm = run_km(model, P2, h, Dp, Dm)
    psi, psi_c, _ = shares(cm_)
    assert abs(psi_c) > 1e-3
    assert abs(psi) <= 1e-12  # the S state carries no response
    eps = float(model.blocks[3].ln1.eps)
    for r in (rp, rm):
        assert float(np.max(np.abs(ca.ln_scale_ratio(r["C"], h, eps) - 1.0))) > 1e-3
        assert float(np.max(np.abs(ca.ln_scale_ratio(r["S"], h, eps) - 1.0))) <= 1e-12
    assert nm_status(cm_, A_full)[0] != "NECESSARY_M"


def test_km4_mlp_gate_interaction():
    P2, PC = spaces(1)
    W = np.random.default_rng(2).normal(size=(8, D)) @ P2
    cm_, A_full, _, _ = run_km(km_model(23, W, mlp=True), P2, *donors(3, P2, PC))
    assert float(np.max(np.abs(cm_["I_M"]))) > 1e-6
    assert np.allclose(cm_["I_M"], cm_["A_F"] - cm_["A_S"] - cm_["A_C"], rtol=0, atol=1e-15)
    psi, psi_c, iota = shares(cm_)
    assert abs(iota - (1.0 - psi - psi_c)) <= 1e-12 * max(1.0, abs(iota), abs(psi), abs(psi_c))
    status, arrays = nm_status(cm_, A_full)
    want = cm_["A_C"] - 0.1 * cm_["A_F"]  # categories on psi_M,comp: A_C against A_F only
    assert float(np.max(np.abs(arrays["ZMc010"] - want))) <= 1e-15 * max(
        1.0, float(np.max(np.abs(want))))
    moved = dict(cm_, A_S=cm_["A_S"] + 1.0, I_M=cm_["I_M"] - 1.0)  # A_S and I_M do not enter
    status2, arrays2 = nm_status(moved, A_full)
    assert all(np.array_equal(arrays[k], arrays2[k]) for k in NM_KEYS)
    assert status2 == status


# ---- T-RESP -----------------------------------------------------------------------------------
def bd(sgn, g=1e-9):
    lo, hi = (0.5, 0.7) if sgn > 0 else (-0.7, -0.5)
    return {"mean": (lo + hi) / 2, "L": lo, "U": hi, "rank_L": 84, "rank_U": 4917, "g": g}


NR = {"V3x": -1, "Y1": -1, "Zc010": 1, "Zc050": 1, "Wc": 1, "Vc": 1, "NEGc": 1, "Zc090": -1,
      "Zc100": -1, "Z090": -1}
DD = {"V3x": -1, "Y1": -1, "Z010": -1, "Z050": -1, "Vabs": -1, "Vrand": -1, "NEG": -1}
NM = {"V3x": -1, "Ztau": 1, "ZMc010": 1, "ZMc050": 1, "WMc": 1, "VMc": 1, "NEGMc": 1}
NEGATIVE_CLAIMS = ("NOT_NECESSARY", "NOT_USED", "DECOY_NOT_USED", "NOT_NECESSARY_M")


@pytest.mark.parametrize("y_active", (False, True))
def test_no_full_response_is_model_headroom(y_active):
    nr = {k: bd(s) for k, s in NR.items()}
    dd = {k: bd(s) for k, s in DD.items()}
    nm = {k: bd(s) for k, s in NM.items()}
    got = (ndc.nr_model(nr, y_active)["status"], ndc.d_model(dd, y_active)["status"],
           ndc.nm_model(nm)["status"])
    assert got == ("EXCLUDED/MODEL_HEADROOM",) * 3
    assert not set(got) & set(NEGATIVE_CLAIMS)
    for res in (ndc.nr_model(nr, y_active), ndc.d_model(dd, y_active), ndc.nm_model(nm)):
        assert not res["resp"] and not res["endpoint_formed"]
    up = {"V3x": bd(1)}  # the same fixtures with a full response would claim non-use
    assert ndc.nr_model(dict(nr, **up), False)["status"] == "NOT_NECESSARY"
    assert ndc.d_model(dict(dd, **up), False)["status"] == "DECOY_NOT_USED"
    assert ndc.nm_model(dict(nm, **up))["status"] == "NOT_NECESSARY_M"


def test_unamplified_decoy_fails_and_gain_six_passes():
    psi, theta = Fraction(85, 100), Fraction(95, 100)
    assert (1 - psi) * theta == Fraction(1425, 10000) < Fraction(3, 10)
    assert 6 * (1 - psi) * theta == Fraction(855, 1000) > Fraction(3, 10)
    rng = np.random.default_rng(8)
    n = 256
    G = 1.0 + 0.1 * rng.random(n)
    A_full = float(theta) * G
    A_rest = A_full - float(psi) * A_full  # the decoy's remaining readout (code removed)
    E = np.ones(n, dtype=bool)
    qy = {"A_full": G, "A_S": np.zeros(n)}
    out = {}
    for name, g, seed in (("V3x'-g1", 1, nc.seed("val_V3xD_g1")),
                          ("V3x'", 6, nc.seed("val_V3xD"))):
        Ap = g * A_rest
        qx = {"A_full": Ap, "A_S": np.zeros(n), "e_full": Ap**2, "e_S": np.zeros(n),
              "r": Ap**2}
        arr = nat.d_stream(qx, qy, G, E, E, refit={"problem": "RD"})
        assert set(arr) == {"V3x", "Y1", "Z010", "Z050", "Vabs", "Vrand", "NEG"}
        assert np.max(np.abs(arr["V3x"] - (Ap - 0.3 * G))) <= 1e-15
        b = cdc.stream_bounds({"V3x": arr["V3x"]}, seed, Fraction(1, 60), 5000)["V3x"]
        gs = cdc.guard(arr["V3x"], 0.0)
        assert (b["rank_L"], b["rank_U"]) == (84, 4917)
        out[name] = "PASS" if b["L"] > gs else "FAIL"
    assert out == {"V3x'-g1": "FAIL", "V3x'": "PASS"}
    assert (nc.seed("val_V3xD_g1"), nc.seed("val_V3xD")) == (630519, 630514)


def oracle_fixture(n=32):
    rng = np.random.default_rng(9)
    qp, qm = rng.dirichlet(np.ones(36), size=n), rng.dirichlet(np.ones(36), size=n)
    perm = np.roll(np.arange(36), 1)  # a 36-cycle: not an involution
    assert not np.array_equal(perm[perm], np.arange(36))
    d_named = np.empty_like(qp)
    d_named[:, perm] = qp - qm  # canonical column c goes to named column perm[c]
    G = 0.5 * np.sum((qp - qm) * (np.log(qp) - np.log(qm)), axis=1)
    return qp, qm, d_named, perm, G


def test_oracle_feas_identity():
    qp, qm, d_named, perm, G = oracle_fixture()
    res = nat.oracle_identity(qp, qm, d_named, perm, G)
    assert bool(res["ok"]) and res["n_over"] == 0
    assert res["max_dev"] <= 1e-12 * max(1.0, float(np.max(np.abs(G))))
    bad = nat.oracle_identity(qp, qm, d_named, np.argsort(perm), G)  # the inverse conversion
    assert not bool(bad["ok"]) and bad["n_over"] > 0
    G_nan = G.copy()
    G_nan[0] = np.nan
    assert nat.oracle_identity(qp, qm, d_named, perm, G_nan)["n_over"] >= 1
