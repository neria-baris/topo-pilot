"""Author A (job 0197): the learning measures and onsets' inputs (§2.4 a, §5.2 k_L/k_P; KD5; DRD7).

`hwsb_eval.model_predictive` is monkeypatched to planted predictives (rows of Dirichlet
q1, q4, q32 with full support); the reused `hwsb_eval.b1`/`forcing` are the documented
formulas (tools/hwsb/API.md) and serve as the reference for the pass-through values.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_known as dk  # noqa: E402
import hwsd_score as ds  # noqa: E402
import hwsb_config  # noqa: E402
import hwsb_eval  # noqa: E402
import hwsc_records  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402


def planted_q(n=96, seed=21):
    rng = np.random.default_rng(seed)
    return {K: rng.dirichlet(np.ones(36), size=n) for K in (1, 4, 32)}


def run(monkeypatch, q, p, **kw):
    seen = {}

    def fake(checkpoint, canon32, perm, *a, **k):
        seen.update(ckpt=checkpoint, canon32=canon32, perm=perm)
        return p

    monkeypatch.setattr(hwsb_eval, "model_predictive", fake)
    canon = np.zeros((len(p), 32), dtype=np.uint8)
    res = ds.learning_one("CKPT", canon, "PERM", q, **kw)
    assert seen["ckpt"] == "CKPT" and seen["perm"] == "PERM" and seen["canon32"] is canon
    return res


def test_z_constants():
    assert dc.Z == NormalDist().inv_cdf(1 - 0.05 / 4) == hwsb_config.Z_B23
    assert dc.Z_S == NormalDist().inv_cdf(1 - 1 / 720)
    assert abs(dc.Z_S - 2.99132) < 1e-5 and abs(dc.Z - 2.2414) < 1e-4
    assert dc.LEARN == Fraction(4, 5)


def test_p_equals_q32_captured_one(monkeypatch):
    q = planted_q()
    r = run(monkeypatch, q, q[32].copy())
    assert abs(r["captured"] - 1.0) <= 1e-12 and r["learn_pass"] is True
    assert r["status"] == "PASS" and abs(r["regret"]) <= 1e-12
    assert r["B2_zS"]["L"] > 0 and r["B2_L_zS"] == r["B2_zS"]["L"]


def test_p_equals_q1_captured_zero(monkeypatch):
    q = planted_q()
    r = run(monkeypatch, q, q[1].copy())
    assert abs(r["captured"]) <= 1e-12 and r["learn_pass"] is False and r["status"] == "FAIL"


def test_p_equals_q4_no_beyond_four_gain(monkeypatch):
    q = planted_q()
    r = run(monkeypatch, q, q[4].copy())
    assert r["B2_z"]["d_mean"] == 0 and r["B2_zS"]["d_mean"] == 0
    assert r["B2_zS"]["L"] <= 0 and not r["B2_L_zS"] > 0  # no predictive onset (strict)


def test_pass_through_of_b1_and_forcing(monkeypatch):
    q = planted_q()
    p = 0.6 * q[32] + 0.4 * q[4]
    r = run(monkeypatch, q, p)
    b1 = hwsb_eval.b1(q, p)
    for key in ("captured", "regret", "G_C", "status", "regret_sd", "regret_se", "G_C_sd", "n"):
        assert r[key] == b1[key], key
    assert r["B2_z"] == hwsb_eval.forcing(q[32], q[4], p, dc.Z)
    assert r["B2_zS"] == hwsb_eval.forcing(q[32], q[4], p, dc.Z_S)
    assert r["z"] == dc.Z and r["z_S"] == dc.Z_S
    assert r["B2_zS"]["L"] < r["B2_z"]["L"]  # z_S > z with the same d_mean and se
    assert r["B2_L_zS"] == r["B2_zS"]["L"]
    assert set(dc.CONTRACT["records"]["LEARN"]) <= set(r)


def test_explicit_z_arguments(monkeypatch):
    q = planted_q()
    p = 0.5 * q[32] + 0.5 * q[4]
    r = run(monkeypatch, q, p, z=1.0, z_s=3.0)
    assert r["B2_z"] == hwsb_eval.forcing(q[32], q[4], p, 1.0)
    assert r["B2_zS"] == hwsb_eval.forcing(q[32], q[4], p, 3.0)


def test_captured_exactly_four_fifths_passes(monkeypatch):
    from topo_pilot.prediction.metrics import LearningGate

    check, _ = LearningGate(0.8).evaluate_with_status(0.8)
    assert check.passed  # equality passes (the stage-C gate value)
    rng = np.random.default_rng(2)
    a, b = rng.dirichlet(np.ones(36)), rng.dirichlet(np.ones(36))
    for n, k in ((5, 1), (10, 2), (15, 3), (20, 4), (40, 8)):
        q = {32: np.tile(a, (n, 1)), 4: np.tile(a, (n, 1)), 1: np.tile(b, (n, 1))}
        p = q[32].copy()
        p[:k] = b
        if hwsb_eval.b1(q, p)["captured"] == 0.8:
            r = run(monkeypatch, q, p)
            assert r["captured"] == 0.8 and r["learn_pass"] is True
            return
    pytest.skip("API-AMBIGUITY: no planted float reaches captured == 0.8 exactly")


def test_learn_pass_reads_status_only(monkeypatch):
    q = planted_q()
    p = q[32].copy()
    real = hwsb_eval.b1

    def b1_fail(qq, pp):
        return dict(real(qq, pp), status="FAIL")

    monkeypatch.setattr(hwsb_eval, "b1", b1_fail)
    r = run(monkeypatch, q, p)
    assert r["learn_pass"] is False


def test_no_context_gain_is_numerical(monkeypatch):
    q = planted_q()
    q[1] = q[32].copy()  # G_C = 0 <= 1e-6: captured NaN, b1 status INCONCLUSIVE
    with pytest.raises(C1GateFailure) as e:
        run(monkeypatch, q, q[4].copy())
    assert e.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_nan_predictive_is_numerical(monkeypatch):
    q = planted_q()
    p = q[32].copy()
    p[3] = np.nan
    # the reused kl_rows may stop first (hws_worlds.HwsStop); any exception counts through the
    # reused status mapping (API.md §0: hwsc_records.status_of)
    with pytest.raises(Exception) as e:
        run(monkeypatch, q, p)
    assert hwsc_records.status_of(e.value) == "FAIL_TECHNICAL/NUMERICAL"


@pytest.mark.slow
def test_kd5_passes_on_w0():
    r = dk.kd5()
    assert r["status"] == "PASS"
