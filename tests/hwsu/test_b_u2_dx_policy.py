"""Author B (job 0223, phase 2): the logit policy and the M0 mirror (API_U2 1.3-1.4; protocol 2.10,
6 rows 11-12). Synthetic: a float64 TransformerLM (4 layers, d_model 128, random init, a few
rows), no checkpoint, no store. x1_gate's input layout is not fixed by API_U2 (see AUTHORSHIP)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

BIND = "FAIL_TECHNICAL/BINDING"
MODEL = "FAIL_TECHNICAL/MODEL"
J = 620301


def _m():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_model")


def _fail(fn, *a, **k):
    with pytest.raises(C1GateFailure) as e:
        fn(*a, **k)
    return e.value.status


# ------------------------------------------------------------------ constants
def test_gate_order_and_allowed_kinds():
    m = _m()
    assert tuple(m.GATE_ORDER_U) == ("BASIS", "M0", "X1", "P1", "T-PRE", "NUM", "ENDPOINT")
    assert {k: set(v) for k, v in m.ALLOWED_U.items()} == {
        "basis": {"BASIS"}, "m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"},
        "test_endpoint": {"NUM", "ENDPOINT"}}


# ------------------------------------------------------------------ UPolicy
def test_policy_refuses_unknown_gate():
    p = _m().UPolicy()
    assert _fail(p.begin, "NOT-A-GATE") == BIND


def test_policy_refuses_out_of_order_gate_and_nested_begin():
    p = _m().UPolicy()
    p.begin("X1")
    p.end("X1")
    assert _fail(p.begin, "M0") == BIND  # earlier than one already begun
    p.begin("T-PRE")
    assert _fail(p.begin, "NUM") == BIND  # another gate is current
    p.end("T-PRE")
    p.begin("NUM")
    p.end("NUM")


@pytest.mark.parametrize("kind,ok,bad", [
    ("basis", ["BASIS"], ["M0", "X1", "T-PRE"]),
    ("m0", ["M0", "T-PRE"], ["BASIS", "X1", "NUM"]),
    ("x1", ["X1", "T-PRE"], ["BASIS", "M0", "NUM"])])
def test_require_allows_only_the_listed_gates(kind, ok, bad):
    m = _m()
    for g in ok:
        p = m.UPolicy()
        p.begin(g)
        p.require(kind)
    for g in bad:
        p = m.UPolicy()
        p.begin(g)
        assert _fail(p.require, kind) == BIND


def test_require_without_a_current_gate_refused():
    p = _m().UPolicy()
    assert _fail(p.require, "x1") == BIND
    p.begin("X1")
    p.end("X1")
    assert _fail(p.require, "x1") == BIND


def test_test_endpoint_needs_t_pre_pass():
    m = _m()
    p = m.UPolicy()
    p.begin("NUM")
    assert _fail(p.require, "test_endpoint") == BIND  # T-PRE not PASS: no endpoint array
    p2 = m.UPolicy()
    p2.begin("T-PRE")
    p2.end("T-PRE")
    p2.mark_pass("T-PRE")
    p2.begin("NUM")
    p2.require("test_endpoint")
    p2.end("NUM")
    p2.begin("ENDPOINT")
    p2.require("test_endpoint")


def test_test_endpoint_refused_at_other_gates_even_after_t_pre():
    p = _m().UPolicy(done=())
    p.begin("T-PRE")
    p.mark_pass("T-PRE")
    assert _fail(p.require, "test_endpoint") == BIND  # current gate is T-PRE, not NUM/ENDPOINT


def test_policy_done_argument_does_not_grant_pass_by_itself():
    p = _m().UPolicy(done=())
    p.begin("NUM")
    assert _fail(p.require, "test_endpoint") == BIND


# ------------------------------------------------------------------ m0_u
@pytest.fixture(scope="module")
def tiny():
    torch = pytest.importorskip("torch")
    from topo_pilot.learner import ModelConfig, TransformerLM

    cfg = ModelConfig(vocab_in=37, vocab_out=36, n_ctx=33, n_layers=4, d_model=128,
                      n_heads=4, d_mlp=64)
    with torch.random.fork_rng():
        torch.manual_seed(223001)
        model = TransformerLM(cfg)
        with torch.no_grad():
            model.ln_final.weight.copy_(1.0 + 0.3 * torch.randn(128))
            model.ln_final.bias.copy_(0.5 * torch.randn(128))
    model = model.to(torch.float64).eval()
    rng = np.random.default_rng(223)
    n = 16
    perm = rng.permutation(36)
    canon32 = rng.integers(0, 36, size=(n, 32)).astype(np.uint8)
    d_canon = rng.standard_normal((n, 36))
    d_canon -= d_canon.mean(axis=1, keepdims=True)
    return {"model": model, "perm": perm, "canon32": canon32, "d": d_canon}


def _run_m0(tiny, sha="sha-A", ck=None, state="sha-A"):
    m = _m()
    import c2_model

    pol = m.UPolicy()
    inputs = m.named_inputs(tiny["canon32"], tiny["perm"])
    pol.begin("M0")
    acts, z = c2_model.natural_pass(tiny["model"], inputs, pol, "m0")
    basis = m.basis_u(tiny["model"])
    ck = ck or uc.CONTRACT["stage_c_u2"]["checkpoint_ids"].get(J) or \
        uc.CONTRACT["stage_c_u2"]["checkpoint_ids"][str(J)]
    ident = {"checkpoint_id": ck, "state_sha": state, "canon32": tiny["canon32"],
             "master": J, "j": J}
    return m.m0_u(tiny["model"], sha, ident, inputs, acts, z, basis, tiny["d"], tiny["perm"], pol)


def test_m0_u_true_identity_passes_when_attainable(tiny, monkeypatch):
    import c2_model

    monkeypatch.setattr(c2_model, "x1_attainable", lambda k: True)
    monkeypatch.setattr(c2_model, "m0", lambda *a, **k: pytest.fail("c2_model.m0 must never be called"))  # noqa: E501
    r = _run_m0(tiny)
    assert r["status"] == "PASS", r
    assert r["checks"]["ids"] and r["checks"]["state_sha"] and r["checks"]["roundtrip"]
    assert r["checks"]["rank"] and r["checks"]["readout"] and r["checks"]["two_route"]


def test_m0_u_wrong_state_sha_is_model_failure(tiny, monkeypatch):
    import c2_model

    monkeypatch.setattr(c2_model, "x1_attainable", lambda k: True)
    r = _run_m0(tiny, sha="sha-OTHER")
    assert r["status"] == MODEL and not r["checks"]["state_sha"]


def test_m0_u_wrong_checkpoint_id_is_model_failure(tiny, monkeypatch):
    import c2_model

    monkeypatch.setattr(c2_model, "x1_attainable", lambda k: True)
    r = _run_m0(tiny, ck="not-the-registered-id")
    assert r["status"] == MODEL and not r["checks"]["ids"]


def test_m0_u_only_attainability_failing_is_inconclusive_numerical(tiny, monkeypatch):
    import c2_model

    monkeypatch.setattr(c2_model, "x1_attainable", lambda k: False)
    r = _run_m0(tiny)
    assert r["status"] == "INCONCLUSIVE/NUMERICAL", r
    assert not r["checks"]["attainable"]
    assert all(v for k, v in r["checks"].items() if k != "attainable")


def test_m0_u_refused_outside_m0_or_t_pre(tiny):
    m = _m()
    import c2_model

    pol = m.UPolicy()
    inputs = m.named_inputs(tiny["canon32"], tiny["perm"])
    pol.begin("M0")
    acts, z = c2_model.natural_pass(tiny["model"], inputs, pol, "m0")
    pol.end("M0")
    pol2 = m.UPolicy()
    pol2.begin("BASIS")  # identity patches need kind "m0": not allowed at BASIS
    ident = {"checkpoint_id": "x", "state_sha": "s", "canon32": tiny["canon32"], "master": J, "j": J}  # noqa: E501
    with pytest.raises(C1GateFailure):
        m.m0_u(tiny["model"], "s", ident, inputs, acts, z, m.basis_u(tiny["model"]), tiny["d"],
               tiny["perm"], pol2)
