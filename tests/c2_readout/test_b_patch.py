"""Author B (job 0101): T-PATCH and T-X1 (C2-FROZEN-v2 §13.3; §2.1, §2.7, §7 rows 9 and 17).

Written from PROTOCOL_C2_v2.md, API.md §7 and CONTRACT.json only; tools/c2_readout/*.py never
read. Synthetic fixtures: a tiny float64 TransformerLM (4 blocks, d_model 128, n_ctx 33) with a
random final LayerNorm; random token inputs; no checkpoint, no store.
"""

from __future__ import annotations

import inspect
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn.functional as F

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402  (first: the sys.path convention)
import c2_driver as cdr  # noqa: E402
import c2_model as cm  # noqa: E402

from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch  # noqa: E402

N_ROWS, IDX, TAU = 16, 32, 1e-9
SITES = ("resid_post_2", "resid_post_3", "ln_final_out")


class _Policy(cdr.LogitPolicy):
    """Permissive policy stub built from cdr.LogitPolicy: records kinds, refuses nothing."""

    def __init__(self):
        super().__init__(done=())
        self.kinds = []

    def require(self, kind):
        self.kinds.append(kind)

    def require_write(self, kind):
        self.kinds.append("write:" + str(kind))


def _tiny_model():
    cfg = ModelConfig(vocab_in=37, vocab_out=36, n_ctx=33, n_layers=4, d_model=128,
                      n_heads=4, d_mlp=64)
    with torch.random.fork_rng():
        torch.manual_seed(101101)
        model = TransformerLM(cfg)
        with torch.no_grad():
            model.ln_final.weight.copy_(1.0 + 0.3 * torch.randn(128))
            model.ln_final.bias.copy_(0.5 * torch.randn(128))
            model.unembed.weight.mul_(25.0)
            model.blocks[3].attn.qkv.weight.mul_(20.0)
            model.blocks[3].attn.proj.weight.mul_(10.0)
    return model.to(torch.float64).eval()


def _inputs(seed, n=N_ROWS):
    named = np.random.default_rng(seed).integers(0, 36, size=(n, 32))
    bos = np.full((n, 1), 36, dtype=np.int64)
    return torch.from_numpy(np.hstack((bos, named)).astype(np.int64))


@pytest.fixture(scope="module")
def tiny():
    model = _tiny_model()
    inputs, inputs_b = _inputs(1), _inputs(2)
    with torch.no_grad():
        nat = model(inputs, return_hooks=SITES)
        nat_b = model(inputs_b, return_hooks=SITES)
    return {"model": model, "inputs": inputs, "inputs_b": inputs_b,
            "logits": nat.logits.numpy().copy(), "logits_b": nat_b.logits.numpy().copy(),
            "hooks": {s: nat.hooks[s][:, IDX, :].numpy().copy() for s in SITES},
            "hooks_b": {s: nat_b.hooks[s][:, IDX, :].numpy().copy() for s in SITES},
            "ids": np.arange(1000, 1000 + N_ROWS, dtype=np.int64)}


def _scale(z):
    return max(1.0, float(np.max(np.abs(z))))


def _fwp(model, inputs, site, rep):
    with torch.no_grad():
        out = forward_with_patch(model, inputs, site, IDX, torch.as_tensor(rep))
    return out.logits.numpy().copy()


def _no_arrays(obj) -> bool:
    if isinstance(obj, (np.ndarray, torch.Tensor)):
        return False
    if isinstance(obj, dict):
        return all(_no_arrays(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(_no_arrays(v) for v in obj)
    return True


# ---- T-PATCH ----
def test_activations3_are_the_three_hooks_at_position_32(tiny):
    acts = cm.activations3(tiny["model"], tiny["inputs"])
    assert set(acts) == set(SITES)
    for s in SITES:
        assert acts[s].dtype == np.float64 and acts[s].shape == (N_ROWS, 128)
        assert np.array_equal(acts[s], tiny["hooks"][s]), s


def test_identity_patch_bitwise_at_three_sites(tiny):
    pol, model = _Policy(), tiny["model"]
    acts = cm.activations3(model, tiny["inputs"])
    assert cm.identity_patch(model, tiny["inputs"], acts, pol) == {s: True for s in SITES}
    for s in SITES:
        full = _fwp(model, tiny["inputs"], s, tiny["hooks"][s])
        assert np.array_equal(full, tiny["logits"]), s  # every position, bitwise
        z = cm.patched_logits(model, tiny["inputs"], s, tiny["hooks"][s], pol, "m0")
        assert z.dtype == np.float64 and z.shape == (N_ROWS, 36)
        assert np.array_equal(z, tiny["logits"][:, IDX]), s
    assert "m0" in pol.kinds  # patched_logits calls policy.require(kind)


def test_identity_patch_detects_a_one_entry_change(tiny):
    acts = {s: v.copy() for s, v in tiny["hooks"].items()}
    acts["resid_post_2"][3, 5] += 1e-6
    res = cm.identity_patch(tiny["model"], tiny["inputs"], acts, _Policy())
    assert res == {"resid_post_2": False, "resid_post_3": True, "ln_final_out": True}


def test_ln_final_out_patch_is_linear_and_input_independent(tiny):
    model, pol = tiny["model"], _Policy()
    rng = np.random.default_rng(31)
    r1, r2 = rng.standard_normal((N_ROWS, 128)), rng.standard_normal((N_ROWS, 128))
    def pl(inp, r):
        return cm.patched_logits(model, inp, "ln_final_out", r, pol, "m0")

    inp = tiny["inputs"]
    z1, z2, z12 = pl(inp, r1), pl(inp, r2), pl(inp, 2.0 * r1 - 0.5 * r2)
    tol = 1e-12 * _scale(z12)
    assert np.max(np.abs(z12 - (2.0 * z1 - 0.5 * z2))) <= tol
    WU = model.unembed.weight.detach().numpy()
    assert np.max(np.abs(z1 - r1 @ WU.T)) <= 1e-12 * _scale(z1)  # bias-free head, no 2nd LN
    zb = pl(tiny["inputs_b"], r1)  # other histories, same replacement
    assert np.max(np.abs(zb - z1)) <= 1e-13 * _scale(z1)
    assert np.max(np.abs(tiny["logits"][:, IDX] - tiny["logits_b"][:, IDX])) > 1e-3


def _attend(q, k, v, n_heads):
    b, L, w = q.shape
    q, k, v = (t.view(b, L, n_heads, -1).transpose(1, 2) for t in (q, k, v))
    s = q @ k.transpose(-1, -2) / math.sqrt(w // n_heads)
    mask = torch.ones(L, L, dtype=torch.bool).tril()
    p = torch.softmax(s.masked_fill(~mask, float("-inf")), dim=-1)
    return (p @ v).transpose(1, 2).reshape(b, L, w)


def _block3_manual(model, x, kv_from):
    """Block 3 by hand: queries from x; keys/values from kv_from at position 32 only."""
    blk = model.blocks[3]
    q, k, v = blk.attn.qkv(blk.ln1(x)).split(128, dim=2)
    _, k2, v2 = blk.attn.qkv(blk.ln1(kv_from)).split(128, dim=2)
    k, v = k.clone(), v.clone()
    k[:, IDX], v[:, IDX] = k2[:, IDX], v2[:, IDX]
    h = x + blk.attn.proj(_attend(q, k, v, blk.attn.n_heads))
    h = h + blk.fc_out(F.gelu(blk.fc_in(blk.ln2(h))))
    return model.unembed(model.ln_final(h))[:, IDX].numpy().copy()


def test_resid_post_2_prefix_unchanged_and_own_patched_key_value(tiny):
    model, inp = tiny["model"], tiny["inputs"]
    rep = tiny["hooks"]["resid_post_2"] + np.random.default_rng(41).standard_normal((N_ROWS,
                                                                                    128))
    full = _fwp(model, inp, "resid_post_2", rep)
    assert np.array_equal(full[:, :IDX], tiny["logits"][:, :IDX])  # positions < 32, bitwise
    z = cm.patched_logits(model, inp, "resid_post_2", rep, _Policy(), "m0")
    assert np.max(np.abs(z - full[:, IDX])) <= 1e-12 * _scale(z)
    with torch.no_grad():
        x_nat = model(inp, return_hooks=("resid_post_2",)).hooks["resid_post_2"].clone()
        x_pat = x_nat.clone()
        x_pat[:, IDX] = torch.as_tensor(rep)
        own = _block3_manual(model, x_pat, x_pat)
        foreign = _block3_manual(model, x_pat, x_nat)
    assert np.max(np.abs(own - z)) <= 1e-10 * _scale(z)  # attends to its own patched K/V
    assert np.max(np.abs(foreign - z)) > 1e-6  # the natural K/V at 32 would differ


# ---- T-X1 ----
@pytest.fixture(scope="module")
def readout(tiny):
    basis = cm.readout_basis(tiny["model"])
    u, ub = tiny["hooks"]["ln_final_out"], tiny["hooks_b"]["ln_final_out"]
    y, yb = cm.readout_coords(u, basis), cm.readout_coords(ub, basis)
    Q = np.linalg.qr(np.random.default_rng(51).standard_normal((127, 6)))[0]
    y_int = yb + (y - yb) @ (Q @ Q.T).T  # an interchange-like coordinate vector
    return {"basis": basis, "u": u, "y": y, "y_int": y_int, "z": tiny["logits"][:, IDX]}


def _closed(basis, y):
    return np.asarray(basis["WU"]) @ np.asarray(basis["beta"]) + y @ np.asarray(basis["M"]).T


def _arms(tiny, ro, z_nat=None, y_int=None):
    z_nat = ro["z"] if z_nat is None else z_nat
    y_int = ro["y_int"] if y_int is None else y_int
    return {"nat_H": (tiny["inputs"], ro["y"], z_nat, tiny["ids"]),
            "R_x_21": (tiny["inputs_b"], y_int, None, tiny["ids"])}


def test_x1_signature_has_no_store_access():
    assert list(inspect.signature(cm.x1).parameters) == ["model64", "arms", "basis", "policy"]


def test_x1_closed_form_equals_patch_path_and_returns_diagnostics_only(tiny, readout):
    b = readout["basis"]
    placed = np.asarray(b["beta"]) + readout["y_int"] @ np.asarray(b["Q0"]).T
    z_fwp = _fwp(tiny["model"], tiny["inputs_b"], "ln_final_out", placed)[:, IDX]
    dev = np.max(np.abs(z_fwp - _closed(b, readout["y_int"])), axis=1)
    assert np.all(dev <= TAU * np.maximum(1.0, np.max(np.abs(z_fwp), axis=1)))
    pol = _Policy()
    res = cm.x1(tiny["model"], _arms(tiny, readout), b, pol)
    assert res["status"] == "PASS" and list(res["ids_over"]) == []
    assert set(res) <= {"arms", "ids_over", "status"} and set(res["arms"]) == {"nat_H",
                                                                                "R_x_21"}
    scale = max(_scale(readout["z"]), _scale(z_fwp))
    for arm in res["arms"].values():
        assert set(arm) <= {"max_dev", "n_over"} and arm["n_over"] == 0
        assert float(arm["max_dev"]) <= TAU * scale
    assert _no_arrays(res)  # no logits, coordinates or endpoint arrays retained
    assert "x1" in pol.kinds


def _defect(kind, tiny, ro):
    b = dict(ro["basis"])
    if kind == "beta":
        b["beta"] = np.asarray(b["beta"]) + 0.5
        return b, _arms(tiny, ro), "R_x_21"
    if kind == "Q0":
        q = np.asarray(b["Q0"]).copy()
        q[:, [0, 1]] = q[:, [1, 0]]
        b["Q0"] = q
        return b, _arms(tiny, ro), "R_x_21"
    return b, _arms(tiny, ro, z_nat=np.roll(ro["z"], 1, axis=0)), "nat_H"  # row index


@pytest.mark.parametrize("kind", ["beta", "Q0", "index"])
def test_x1_injected_defect_fails_by_1e6_tau(tiny, readout, kind):
    basis, arms, arm = _defect(kind, tiny, readout)
    res = cm.x1(tiny["model"], arms, basis, _Policy())
    assert res["status"] == "FAIL_TECHNICAL/X1"
    z_ref = readout["z"]
    if kind != "index":
        placed = np.asarray(basis["beta"]) + readout["y_int"] @ np.asarray(basis["Q0"]).T
        z_ref = _fwp(tiny["model"], tiny["inputs_b"], "ln_final_out", placed)[:, IDX]
    assert float(res["arms"][arm]["max_dev"]) >= 1e6 * TAU * _scale(z_ref)
    assert res["arms"][arm]["n_over"] == N_ROWS
    assert sorted({int(i) for i in res["ids_over"]}) == tiny["ids"].tolist()


def test_x1_fail_closed_on_one_row_and_tolerance_is_relative(tiny, readout):
    z = readout["z"].copy()
    z[5, 7] += 1e-6 * max(1.0, float(np.max(np.abs(z[5]))))
    res = cm.x1(tiny["model"], _arms(tiny, readout, z_nat=z), readout["basis"], _Policy())
    assert res["status"] == "FAIL_TECHNICAL/X1" and res["arms"]["nat_H"]["n_over"] == 1
    assert [int(i) for i in res["ids_over"]] == [int(tiny["ids"][5])]
    z_ok = readout["z"].copy()
    z_ok[5, 7] += 1e-12 * max(1.0, float(np.max(np.abs(z_ok[5]))))
    ok = cm.x1(tiny["model"], _arms(tiny, readout, z_nat=z_ok), readout["basis"], _Policy())
    assert ok["status"] == "PASS"


def test_x1_non_finite_replacement_is_fail_closed(tiny, readout):
    y_bad = readout["y_int"].copy()
    y_bad[2, 0] = np.nan
    try:
        res = cm.x1(tiny["model"], _arms(tiny, readout, y_int=y_bad), readout["basis"],
                    _Policy())
    except Exception:  # noqa: BLE001  a raised refusal is fail-closed as well
        return
    assert res["status"] == "FAIL_TECHNICAL/X1"


def test_readout_identity_rule(tiny, readout):
    b, y, z = readout["basis"], readout["y"], readout["z"]
    ok = cm.readout_identity(z, y, b)
    assert bool(ok["ok"]) and ok["n_over"] == 0 and float(ok["max_dev"]) <= TAU * _scale(z)
    z2 = z.copy()
    z2[3] += 1e-3
    bad = cm.readout_identity(z2, y, b)
    assert not bad["ok"] and bad["n_over"] == 1


def test_kappa_x1_matches_the_written_formula(readout):
    b, u, y, z = readout["basis"], readout["u"], readout["y"], readout["z"]
    WU, beta, Q0 = (np.abs(np.asarray(b[k])) for k in ("WU", "beta", "Q0"))
    S = (np.abs(u) + beta[None, :]) @ WU.T + np.abs(y) @ (WU @ Q0).T  # S_iv
    kappa = float(np.max(S / np.maximum(1.0, np.max(np.abs(z), axis=1))[:, None]))
    got = float(cm.kappa_x1(u, y, b, z))
    assert abs(got - kappa) <= 1e-12 * kappa


def test_x1_attainability_product_form_exact():
    crit = Fraction(1, 10**10) / (4 * 128 * Fraction(1, 2**53))  # 2**44 / 1e10 = 1759.2186...
    k_f = float(crit)
    assert cm.x1_attainable(k_f) == (Fraction(k_f) <= crit)
    up, down = np.nextafter(k_f, np.inf), np.nextafter(k_f, -np.inf)
    assert cm.x1_attainable(float(down)) and not cm.x1_attainable(float(up))
    assert cm.x1_attainable(1759.0) and not cm.x1_attainable(1760.0)  # "1.76e3" is rounded
    assert cm.x1_attainable(50.0)
    assert cc.CONTRACT["tolerances"]["x1_attainability"] == "1e-10"
