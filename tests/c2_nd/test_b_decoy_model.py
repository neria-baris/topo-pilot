"""Author B, T-DECOY-EXACT (protocol §2.6, §2.7, §3 rows 11 and 20, §5.1; API.md §6).

Tiny float64 TransformerLM (d_model 32, 8 outputs, so ker(M) has dimension 23 >= 6; ND-C33),
a synthetic oblique P_S = B L_B from a GLS fit with Sigma != I, and the head edits, the
coordinate wrapper, M0-D, DX and decoy_sha64. Expected values are computed inside the test.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import c2_attrib as ca  # noqa: E402
import c2_model as cm  # noqa: E402
import nd_attrib as nat  # noqa: E402
import nd_decoy as ndy  # noqa: E402
import nd_driver as ndr  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
import torch  # noqa: E402

from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch  # noqa: E402

G_D, RHO = 6, Fraction(23, 25)
HEAD = ("DNULL", "DNULL1", "DONLY", "DDOSE")
COORD = ("DNULLR", "DID")
N = 16


def tiny_model(seed):
    torch.manual_seed(seed)
    cfg = ModelConfig(vocab_in=9, vocab_out=8, d_model=32, n_heads=4, d_mlp=64)
    m = TransformerLM(cfg).double().eval()
    with torch.no_grad():  # a non-uniform final LayerNorm, so Q0 is not the plain Helmert basis
        m.ln_final.weight.copy_(1.0 + 0.5 * torch.rand(32, dtype=torch.float64))
        m.ln_final.bias.copy_(0.2 * torch.randn(32, dtype=torch.float64))
        m.unembed.weight.copy_(torch.randn(8, 32, dtype=torch.float64))
    return m


def tokens(seed, n=N):
    x = np.random.default_rng(seed).integers(0, 8, size=(n, 33))
    x[:, 0] = 8  # BOS
    return torch.as_tensor(x, dtype=torch.int64)


def projector(seed, r=31):
    """Oblique GLS projectors: L (11 x r) with rows 0..4 for Gamma, 5..10 for B; P_S = B L_B."""
    rng = np.random.default_rng(seed)
    B, G = rng.normal(size=(r, 6)), rng.normal(size=(r, 5))
    A = rng.normal(size=(r, r))
    Sig = A @ A.T + r * np.eye(r)
    X, Si = np.hstack([G, B]), np.linalg.inv(Sig)
    L = np.linalg.solve(X.T @ Si @ X, X.T @ Si)
    return {"B": B, "Gamma": G, "L": L, "L_B": L[5:], "P_S": B @ L[5:], "Sigma": Sig}


def hooks(model, X):
    with torch.no_grad():
        out = model(X, return_hooks=model.hook_names)
    return {k: v.clone() for k, v in out.hooks.items()}, out.logits[:, 32].numpy().copy()


def at_gate(gate):
    pol = ndr.LogitPolicy(done=ndr.GATE_ORDER[: ndr.GATE_ORDER.index(gate)])
    pol.begin(gate)
    return pol


def rel_rows(a, b, tol):
    """Per row max|a - b| <= tol * max(1, max|b|)."""
    a, b = np.atleast_2d(a), np.atleast_2d(b)
    dev = np.max(np.abs(a - b), axis=1)
    return bool(np.all(dev <= tol * np.maximum(1.0, np.max(np.abs(b), axis=1))))


@pytest.fixture(scope="module")
def base():
    model = tiny_model(11)
    basis = cm.readout_basis(model)
    pr = projector(5)
    X1, X2 = tokens(1), tokens(2)
    h1, z1 = hooks(model, X1)
    h2, z2 = hooks(model, X2)
    u1, u2 = (h["ln_final_out"][:, 32].numpy() for h in (h1, h2))
    y1, y2 = cm.readout_coords(u1, basis), cm.readout_coords(u2, basis)
    d = np.random.default_rng(3).normal(size=(N, 8))
    return dict(model=model, basis=basis, pr=pr, X1=X1, X2=X2, h1=h1, z1=z1, z2=z2, u1=u1,
                y1=y1, y2=y2, d=d)


def expected_head(kind, WU, Q0, P_S, g=G_D):
    Pi, eye = Q0 @ P_S @ Q0.T, np.eye(Q0.shape[0])
    return {"DNULL": g * (WU @ (eye - Pi)), "DNULL1": WU @ (eye - Pi), "DONLY": WU @ Pi,
            "DDOSE": g * (WU @ (eye - float(RHO) * Pi))}[kind]


def head(b, kind, P=None, g=G_D):
    P = b["pr"]["P_S"] if P is None else P
    return ndy.head_edit(kind, b["basis"]["WU"], b["basis"]["Q0"], P, g=g)


def coord_decoys(b):
    bs, pr = b["basis"], b["pr"]
    mm = ndy.move_map(pr["B"], pr["L_B"], bs["M"])
    assert mm["ok"]
    return {k: ndy.make_coord_decoy(b["model"], k, bs["Q0"], bs["beta"], mm["T"], mm["Tinv"],
                                    bs["WU"]) for k in COORD}, mm


def test_shapes_and_pi_s(base):
    bs = base["basis"]
    assert bs["Q0"].shape == (32, 31) and bs["M"].shape == (8, 31)
    Pi = ndy.pi_S(bs["Q0"], base["pr"]["P_S"])
    assert Pi.shape == (32, 32)
    ref = bs["Q0"] @ base["pr"]["P_S"] @ bs["Q0"].T
    assert np.max(np.abs(Pi - ref)) <= 1e-13 * max(1.0, np.max(np.abs(ref)))


@pytest.mark.parametrize("kind", HEAD)
def test_head_edit_formula(base, kind):
    bs = base["basis"]
    W = head(base, kind)
    ref = expected_head(kind, bs["WU"], bs["Q0"], base["pr"]["P_S"])
    assert W.shape == bs["WU"].shape and W.dtype == np.float64
    assert np.max(np.abs(W - ref)) <= 1e-13 * max(1.0, np.max(np.abs(ref)))


@pytest.mark.parametrize("kind", ("DNULL", "DNULL1"))
def test_null_heads_annihilate_code(base, kind):
    Mp = head(base, kind) @ base["basis"]["Q0"]
    CMp, B = Mp - Mp.mean(axis=0), base["pr"]["B"]
    bound = 1e-12 * np.max(np.abs(CMp)) * np.max(np.abs(B))
    assert np.max(np.abs(CMp @ B)) <= bound


def test_donly_and_ddose_identities(base):
    bs, P, d = base["basis"], base["pr"]["P_S"], base["d"]
    dy = base["y1"] - base["y2"]
    Mp = head(base, "DONLY") @ bs["Q0"]
    A_full = ca.half_dot(d, dy @ Mp.T)
    A_comp = A_full - ca.half_dot(d, (dy @ P.T) @ Mp.T)
    assert np.all(np.abs(A_comp) <= 1e-12 * np.maximum(1.0, np.abs(A_full)))
    Md = head(base, "DDOSE") @ bs["Q0"]
    A_Sp = ca.half_dot(d, (dy @ P.T) @ Md.T)
    A_S = ca.half_dot(d, (dy @ P.T) @ bs["M"].T)
    want = G_D * float(1 - RHO) * A_S
    assert np.all(np.abs(A_Sp - want) <= 1e-12 * np.maximum(1.0, np.abs(A_Sp)))


@pytest.mark.parametrize("kind", HEAD)
def test_head_decoy_is_the_base_with_a_new_head(base, kind):
    model, W = base["model"], head(base, kind)
    before = copy.deepcopy(model.state_dict())
    dec = ndy.make_head_decoy(model, W)
    assert isinstance(dec, TransformerLM) and not dec.training
    assert torch.equal(dec.unembed.weight, torch.from_numpy(W))
    sd = dec.state_dict()
    for k, v in model.state_dict().items():
        assert torch.equal(v, before[k])  # the base is not modified
        if k != "unembed.weight":
            assert torch.equal(sd[k], v), k
    h, z1p = hooks(dec, base["X1"])
    for name in model.hook_names:  # every upstream hook and ln_final_out bitwise
        assert torch.equal(h[name], base["h1"][name]), name
    z2p = hooks(dec, base["X2"])[1]
    Mp = W @ base["basis"]["Q0"]  # W'_U beta cancels in every difference (Lemma DC1)
    assert rel_rows(z1p - z2p, (base["y1"] - base["y2"]) @ Mp.T, 1e-12)


@pytest.mark.parametrize("kind", HEAD)
def test_patch_and_basis_unchanged_on_head_decoy(base, kind):
    W = head(base, kind)
    dec = ndy.make_head_decoy(base["model"], W)
    X = base["X1"]
    h, _ = hooks(dec, X)
    with torch.no_grad():
        nat_logits = dec(X).logits
        pat = forward_with_patch(dec, X, "ln_final_out", 32, h["ln_final_out"][:, 32]).logits
    assert torch.equal(pat, nat_logits)
    rb = cm.readout_basis(dec)
    assert np.array_equal(rb["M"], W @ base["basis"]["Q0"])
    assert np.array_equal(rb["Q0"], base["basis"]["Q0"])
    acts = cm.activations3(dec, X)
    assert all(cm.identity_patch(dec, X, acts, at_gate("M0-D")).values())


def test_coordinate_wrapper(base):
    decs, mm = coord_decoys(base)
    bs, X, model = base["basis"], base["X1"], base["model"]
    T, Q0, beta = mm["T"], bs["Q0"], bs["beta"]
    for kind, dec in decs.items():
        assert isinstance(dec, TransformerLM)
        assert isinstance(dec.ln_final[1], ndy.CoordMap)
        h, z = hooks(dec, X)
        for name in model.hook_names[:-1]:
            assert torch.equal(h[name], base["h1"][name]), (kind, name)
        u = base["u1"]
        want = beta + ((u - beta) @ Q0) @ T.T @ Q0.T
        assert rel_rows(h["ln_final_out"][:, 32].numpy(), want, 1e-12)
        with torch.no_grad():
            pat = forward_with_patch(dec, X, "ln_final_out", 32, h["ln_final_out"][:, 32])
            assert torch.equal(pat.logits, dec(X).logits)
        Wd = dec.unembed.weight.detach().numpy()
        cb = ndy.coord_basis(dec, bs)
        assert np.array_equal(cb["M"], Wd @ Q0) and np.array_equal(cb["Q0"], Q0)
        assert np.array_equal(cb["WUbeta"], Wd @ beta)
        y_prime = cm.readout_coords(h["ln_final_out"][:, 32].numpy(), cb)
        assert rel_rows(y_prime, base["y1"] @ T.T, 1e-12)
    W = decs["DNULLR"].unembed.weight.detach().numpy()
    assert np.max(np.abs(W - G_D * bs["WU"])) <= 1e-14 * np.max(np.abs(W))
    Wid = decs["DID"].unembed.weight.detach().numpy()
    ref = bs["WU"] @ Q0 @ mm["Tinv"] @ Q0.T
    assert np.max(np.abs(Wid - ref)) <= 1e-12 * max(1.0, np.max(np.abs(ref)))


def test_coordinate_decoys_predict_like_their_partners(base):
    decs, _ = coord_decoys(base)
    dnull = ndy.make_head_decoy(base["model"], head(base, "DNULL"))

    def dz(m):
        return hooks(m, base["X1"])[1] - hooks(m, base["X2"])[1]

    assert rel_rows(dz(decs["DNULLR"]), dz(dnull), 1e-10)  # D-NULL-R == D-NULL
    assert rel_rows(dz(decs["DID"]), base["z1"] - base["z2"], 1e-10)  # D-ID == base


def m0d_inputs(b, P=None, g=G_D):
    bs, pr = b["basis"], b["pr"]
    decoys = {k: ndy.make_head_decoy(b["model"], head(b, k, P, g)) for k in HEAD}
    decoys.update(coord_decoys(b)[0])
    c2_fit = {k: bs[k] for k in ("Q0", "M", "beta", "WU", "WUbeta", "gamma")}
    c2_fit.update(R_P_S=pr["P_S"], R_B=pr["B"], R_L=pr["L"], R_Gamma=pr["Gamma"],
                  R_Sigma=pr["Sigma"])
    X = b["X1"]
    return decoys, c2_fit, X, cm.activations3(b["model"], X), b["z1"]


# API-AMBIGUITY: m0d's `inputs`, `acts` and `z_base` are taken as the token rows [n, 33], the
# base model's activations3 dict and its natural logits at position 32 on those rows; API.md
# §6.5 does not spell out their structure (nor the source of the H+/H- pairs used by the
# prediction identities of item (vii)).
def test_m0d_passes_on_correct_decoys(base):
    decoys, c2_fit, X, acts, z = m0d_inputs(base)
    res = ndy.m0d(1729, base["model"], decoys, base["basis"], c2_fit, X, acts, z,
                  at_gate("M0-D"))
    assert res["status"] == "PASS", res.get("checks")
    assert set(HEAD) <= set(res["per_decoy"])


@pytest.mark.parametrize("bad", ("g5", "transposed", "other_model"))
def test_m0d_fails_on_misbuilt_head_decoys(base, bad):
    P = {"g5": None, "transposed": base["pr"]["P_S"].T, "other_model": projector(77)["P_S"]}
    decoys, c2_fit, X, acts, z = m0d_inputs(base, P[bad], 5 if bad == "g5" else G_D)
    res = ndy.m0d(1729, base["model"], decoys, base["basis"], c2_fit, X, acts, z,
                  at_gate("M0-D"))
    assert res["status"] == "FAIL_TECHNICAL/DECOY"


def test_m0d_refused_outside_its_gates(base):
    decoys, c2_fit, X, acts, z = m0d_inputs(base)
    with pytest.raises(Exception):
        ndy.m0d(1729, base["model"], decoys, base["basis"], c2_fit, X, acts, z, at_gate("C0c"))


# API-AMBIGUITY: the per-decoy array dict passed to dx is not named in API.md §6.5; it is taken
# here as nat.nr_quantities(d, M', y1, y2, P_S) with the construction projector (keys A_full,
# A_S, A_comp, e_full, e_S), for DNULL, DNULL1 and DONLY only (the DDOSE and DID inputs, the
# base A_S and z'' - z, have no named key).
def dx_arrays(b, P_build):
    Q0, P = b["basis"]["Q0"], b["pr"]["P_S"]
    return {k: nat.nr_quantities(b["d"], head(b, k, P_build) @ Q0, b["y1"], b["y2"], P)
            for k in ("DNULL", "DNULL1", "DONLY")}


def test_dx_passes_on_correct_decoys(base):
    res = ndy.dx(dx_arrays(base, base["pr"]["P_S"]), at_gate("DX"))
    assert res["status"] == "PASS"
    assert all(res["per_decoy"][k]["n_over"] == 0 for k in ("DNULL", "DNULL1", "DONLY"))


@pytest.mark.parametrize("bad", ("transposed", "other_model"))
def test_dx_fails_on_misbuilt_decoys(base, bad):
    P = base["pr"]["P_S"].T if bad == "transposed" else projector(77)["P_S"]
    res = ndy.dx(dx_arrays(base, P), at_gate("DX"))
    assert res["status"] == "FAIL_TECHNICAL/DECOY"
    assert res["per_decoy"]["DNULL"]["n_over"] > 0
    assert res["per_decoy"]["DONLY"]["n_over"] > 0


def ref_sha64(module, record):
    h = hashlib.sha256()
    sd = module.state_dict()
    for k in sorted(sd):
        t = sd[k].detach().to(torch.float64).contiguous().cpu().numpy()
        h.update(k.encode("utf-8") + b"\0" + str(tuple(t.shape)).encode("ascii") + b"\0")
        h.update(np.ascontiguousarray(t).tobytes())
    h.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return h.hexdigest()


def record_of(kind, j=1729):
    return {"version": "c2nd-decoy-v1", "kind": kind, "model": j,
            "base_state_sha": nc.CONTRACT["models"][str(j)]["state_sha_f32"],
            "c2_fit_sha256": nc.CONTRACT["c2_store"]["files"][f"fits/FIT_{j}.npz"],
            "g_D": "6", "rho": "23/25"}


class _Buf(torch.nn.Module):
    def __init__(self, t):
        super().__init__()
        self.register_buffer("w", t)


def test_decoy_sha64(base):
    dec = ndy.make_head_decoy(base["model"], head(base, "DNULL"))
    rec = record_of("DNULL")
    s = ndy.decoy_sha64(dec, rec)
    assert s == ndy.decoy_sha64(copy.deepcopy(dec), dict(rec)) == ref_sha64(dec, rec)
    assert ndy.decoy_sha64(dec, dict(rec, kind="DONLY")) != s
    assert ndy.decoy_sha64(dec, dict(rec, rho="9/10")) != s
    flipped = copy.deepcopy(dec)
    with torch.no_grad():
        flipped.unembed.weight.data.view(-1).view(torch.int64)[0] ^= 1  # one weight bit
    assert ndy.decoy_sha64(flipped, rec) != s
    coord = coord_decoys(base)[0]["DNULLR"]
    assert ndy.decoy_sha64(coord, record_of("DNULLR")) == ref_sha64(coord, record_of("DNULLR"))
    a = torch.arange(6, dtype=torch.float64)  # the same bytes in another shape
    one, two = _Buf(a.reshape(2, 3).clone()), _Buf(a.reshape(3, 2).clone())
    assert ndy.decoy_sha64(one, rec) != ndy.decoy_sha64(two, rec)
    assert ndy.decoy_sha64(one, rec) == ref_sha64(one, rec)
