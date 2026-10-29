"""Author A (job 0176): the learning gate L1 on planted predictives.

Protocol HWSC §5 gate 4 (C5), §6.3; DRC7. API.md §6 `l1`, §11.2 gate 4,
choice 14; hwsb API `b1`, `model_predictive`, `oracle_predictives`.
`model_predictive` and `oracle_predictives` are monkeypatched to return
planted Dirichlet predictives; `hwsb_eval.b1` runs unchanged.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_gates as cg  # noqa: E402
import hwsb_eval  # noqa: E402

J1, J2, J3 = 620301, 620302, 620303
MODELS = (J1, J2, J3)
N, V = 64, 6


def base(seed=5):
    rng = np.random.default_rng(seed)
    q32 = rng.dirichlet(np.ones(V), size=N)
    q1 = rng.dirichlet(np.ones(V), size=N)
    q4 = 0.5 * (q1 + q32)
    return {1: q1, 4: q4, 32: q32}


def mix(q, lam):
    return lam * q[32] + (1.0 - lam) * q[1]


def captured(q, p):
    return hwsb_eval.b1(q, p)["captured"]


def find_08():
    """(q, p_at, p_below): captured(p_at) == 0.8 exactly, captured(p_below) < 0.8."""
    for seed in range(5, 45):
        q = base(seed)
        lo, hi = 0.0, 1.0
        while math.nextafter(lo, 1.0) < hi:
            mid = 0.5 * (lo + hi)
            if mid in (lo, hi):
                break
            if captured(q, mix(q, mid)) >= 0.8:
                hi = mid
            else:
                lo = mid
        lam = hi
        for _ in range(64):
            c = captured(q, mix(q, lam))
            if c == 0.8:
                below = math.nextafter(lam, 0.0)
                while captured(q, mix(q, below)) >= 0.8:
                    below = math.nextafter(below, 0.0)
                return q, mix(q, lam), mix(q, below)
            if c < 0.8:
                break
            lam = math.nextafter(lam, 0.0)
    return None


@pytest.fixture(scope="module")
def exact08():
    found = find_08()
    if found is None:
        # API-AMBIGUITY: no planted mixture hit captured == 0.8 exactly in float.
        pytest.skip("captured == 0.8 not reachable exactly by bisection")
    return found


class Spy:
    def __init__(self, q, preds):
        self.q, self.preds, self.calls, self.oracle_calls = q, preds, [], 0

    def oracle(self, proc, canon32, *a, **kw):
        self.oracle_calls += 1
        return dict(self.q)

    def model(self, checkpoint, canon32, perm, *a, **kw):
        self.calls.append(checkpoint)
        return self.preds[checkpoint]


def ctx_for():
    lg = np.zeros((N, 32), dtype=np.uint8)
    return {"ckpts": {**{(j, 5000): f"ckpt5000-{j}" for j in MODELS},
                      **{(j, 0): f"ckpt0-{j}" for j in MODELS}},
            "proc": {"perm": {j: np.arange(V) for j in MODELS}},
            "tables": {"lgate": {"canon32": lg}}}


def install(monkeypatch, q, by_model):
    spy = Spy(q, {f"ckpt5000-{j}": by_model[j] for j in MODELS})
    monkeypatch.setattr(hwsb_eval, "oracle_predictives", spy.oracle)
    monkeypatch.setattr(hwsb_eval, "model_predictive", spy.model)
    return spy


def l1_json(out):
    return json.loads((out / "stages" / "E1" / "L1.json").read_text(encoding="utf-8"))


def per_model(rec, j):
    pm = rec["per_model"]
    return pm[j] if j in pm else pm[str(j)]


def test_reference_points():
    q = base()
    r32, r1 = hwsb_eval.b1(q, q[32]), hwsb_eval.b1(q, q[1])
    assert abs(r32["captured"] - 1.0) <= 1e-12 and r32["status"] == "PASS"
    assert r1["captured"] == 0.0 and r1["status"] == "FAIL"


def test_all_pass_records_every_model(tmp_path, monkeypatch, exact08):
    q, p08, _ = exact08
    preds = {J1: q[32], J2: p08, J3: mix(q, 0.97)}
    spy = install(monkeypatch, q, preds)
    out = cg.l1(tmp_path, ctx_for())
    assert sorted(spy.calls) == sorted(f"ckpt5000-{j}" for j in MODELS)
    rec = l1_json(tmp_path)
    assert list(rec["failing"]) == [] and rec["k"] == 0
    for j in MODELS:
        ref = hwsb_eval.b1(q, preds[j])
        assert per_model(rec, j)["captured"] == ref["captured"]
        assert per_model(rec, j)["status"] == "PASS"
    assert per_model(rec, J2)["captured"] == 0.8  # equality passes
    assert abs(per_model(rec, J1)["captured"] - 1.0) <= 1e-12
    # API-AMBIGUITY: the return value is "per-model records"; accept either the
    # L1 record shape or a dict keyed by model.
    pm = out.get("per_model", out) if isinstance(out, dict) else None
    assert pm is not None
    assert {int(k) for k in pm if str(k).isdigit()} >= set(MODELS)


def failing_case(tmp_path, monkeypatch, q, preds, k, failing):
    spy = install(monkeypatch, q, preds)
    with pytest.raises(Exception) as ei:
        cg.l1(tmp_path, ctx_for())
    exc = ei.value
    assert getattr(exc, "status", None) == "INCONCLUSIVE/NOT_LEARNED"
    assert str(getattr(exc, "reason", "")).startswith(f"{k}/3")
    assert len(spy.calls) == 3  # all three computed before the decision
    rec = l1_json(tmp_path)
    assert rec["k"] == k
    assert sorted(int(j) for j in rec["failing"]) == sorted(failing)
    for j in MODELS:
        assert per_model(rec, j)["captured"] == hwsb_eval.b1(q, preds[j])["captured"]


def test_first_model_failing_k1(tmp_path, monkeypatch):
    q = base()
    preds = {J1: q[1], J2: q[32], J3: mix(q, 0.95)}
    assert hwsb_eval.b1(q, q[1])["captured"] == 0.0
    failing_case(tmp_path, monkeypatch, q, preds, 1, [J1])


def test_two_failing_k2(tmp_path, monkeypatch):
    q = base()
    preds = {J1: mix(q, 0.2), J2: q[32], J3: q[1]}
    failing_case(tmp_path, monkeypatch, q, preds, 2, [J1, J3])


def test_just_below_08_fails(tmp_path, monkeypatch, exact08):
    q, p08, below = exact08
    assert hwsb_eval.b1(q, below)["captured"] < 0.8
    preds = {J1: q[32], J2: q[32], J3: below}
    failing_case(tmp_path, monkeypatch, q, preds, 1, [J3])


def test_gc_floor_is_numerical(tmp_path, monkeypatch):
    q = base()
    q = {1: q[32].copy(), 4: q[32].copy(), 32: q[32]}  # G_C = 0 <= 1e-6
    assert hwsb_eval.b1(q, q[32])["status"] == "INCONCLUSIVE"
    install(monkeypatch, q, {j: q[32] for j in MODELS})
    with pytest.raises(Exception) as ei:
        cg.l1(tmp_path, ctx_for())
    assert getattr(ei.value, "status", None) == "FAIL_TECHNICAL/NUMERICAL"


def test_nan_row_is_numerical(tmp_path, monkeypatch):
    q = base()
    bad = q[32].copy()
    bad[3, 2] = np.nan
    install(monkeypatch, q, {J1: q[32], J2: bad, J3: q[32]})
    # API-AMBIGUITY: the NaN may surface as C1GateFailure or as the reused
    # hws_worlds.HwsStop from kl_rows; both carry status FAIL_TECHNICAL/NUMERICAL.
    with pytest.raises(Exception) as ei:
        cg.l1(tmp_path, ctx_for())
    assert getattr(ei.value, "status", None) == "FAIL_TECHNICAL/NUMERICAL"


def test_learning_constant():
    assert cc.LEARN == Fraction(4, 5)
