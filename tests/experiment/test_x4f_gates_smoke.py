"""Builder-authored smoke test (not the independent X4-F tests): G1-G5 orchestration end to end
on a tiny synthetic model and planted targets; checks plumbing, statuses and isolation only."""
import numpy as np
import pytest
import torch

from topo_pilot.analysis import fit_oblique_eraser, gate_verdict, whiten
from topo_pilot.experiment import x4f_gates
from topo_pilot.experiment.x4f_damage import g3, g4, g5
from topo_pilot.experiment.x4f_data import ModelData
from topo_pilot.experiment.x4f_gates import ValForward, control_targets, g1, g2
from topo_pilot.learner import ModelConfig, TransformerLM

pytestmark = pytest.mark.experiment


@pytest.fixture(scope="module")
def tiny():
    torch.manual_seed(0)
    model = TransformerLM(ModelConfig(vocab_in=4, vocab_out=3, n_layers=4, d_model=16,
                                      n_heads=2, d_mlp=32)).eval()
    rng = np.random.default_rng(0)
    R = 512
    inputs = np.concatenate([np.full((R, 1), 3), rng.integers(0, 3, (R, 32))], axis=1)
    with torch.no_grad():
        out = model(torch.as_tensor(inputs), return_hooks=["embed", "resid_post_1",
                                                           "resid_post_3", "ln_final_out"])
    acts = {k: v[:, 32, :].double().numpy() for k, v in out.hooks.items()}
    # isotropic synthetic features keep the matched random family feasible (plumbing only)
    acts["resid_post_1"] = rng.standard_normal((R, 16))
    h = acts["resid_post_1"]
    ang = h[:, 0] / (h[:, 0].std() + 1e-9)
    m32 = np.column_stack([np.cos(ang), np.sin(ang)])
    m2 = m32 + 0.3 * rng.standard_normal(m32.shape)
    b = rng.dirichlet(np.ones(9), R)
    q1 = rng.dirichlet(np.ones(3), R)
    targets = {"m32": m32, "m2": m2, "m1": m2 + 0.1, "r2": m32 - m2, "Q1": q1,
               "onehot_w32": np.eye(3)[inputs[:, -1]], "local": b}
    panel = np.repeat(np.arange(1, 9), R // 8)
    d = ModelData(1729, tuple(str(i) for i in range(R)), panel, inputs, acts, targets,
                  panel <= 6, panel >= 7)
    return model, d


def test_gates_end_to_end(tiny, monkeypatch):
    monkeypatch.setattr(x4f_gates, "N_RBF", 32)
    monkeypatch.setattr(x4f_gates, "N_SHUFFLE", 20)
    model, d = tiny
    r1 = g1(d)
    assert r1["status"] in ("PASS", "FAIL") and r1["m32"]["r2"] is not None
    assert len(r1["m32_shuffle"]["values"]) == 20
    wh = whiten(d.acts["resid_post_1"][d.cal])
    primary = fit_oblique_eraser(d.acts["resid_post_1"][d.cal], d.targets["m32"][d.cal], wh)
    vf = ValForward(model, d)
    r2 = g2(d, model, vf, primary)
    assert r2["identity_index32"] <= 1e-5 and r2["identity_before32"] <= 1e-7
    assert r2["weights_unchanged"] and r2["final_null"]["centred_diff_f64"] <= 1e-8
    assert r2["primary_before32"] <= 1e-7
    r3 = g3(d, wh, primary)
    assert r3["rank"] in (1, 2) and r3["status"].split(":")[0] in ("PASS", "FAIL")
    r4, clouds = g4(d, vf, wh, primary, control_targets(d))
    assert r4["family_status"] == "ok" and len(r4["accepted"]) == 20
    assert set(r4["profiles"]) >= {"primary", "R1", "m2", "local", "generic", "shuffled_m32"}
    r5 = g5(d, clouds)
    assert r5["status"].split(":")[0] in ("PASS", "FAIL")
    assert gate_verdict({1729: {"G1": "PASS", "G2": "PASS", "G3": "PASS", "G4": "PASS",
                                "G5": "PASS"}})[0] == "FEASIBLE"


def test_g1_ignores_validation_targets_for_selection(tiny, monkeypatch):
    monkeypatch.setattr(x4f_gates, "N_SHUFFLE", 20)
    _, d = tiny
    poisoned = dict(d.targets)
    m = poisoned["m32"].copy()
    m[d.val] = 1e6
    poisoned["m32"] = m
    d2 = ModelData(d.seed, d.history_id, d.panel, d.inputs, d.acts, poisoned, d.cal, d.val)
    assert g1(d2)["m32"]["lam"] == g1(d)["m32"]["lam"]
