"""Independent tests, author A (job 0026): C0-val criteria and the construction ledger
(TEST_PLAN A-1 items 7 and 8; protocol section 14 'Validation chart gates' and 'Construction
limit').

The production chart here is a hand-built chart.Chart: 120 landmarks on the unit circle at
angles (k + 1/2) * 3 degrees with phi equal to that angle, sigma 0.05 and support radius 0.5.
A query placed exactly on landmark k takes the exact-duplicate branch of the frozen extend, so
its phase is that landmark's angle, its resultant is 1 and its 8th-NN distance is 2 sin(6 deg)
~ 0.209 (supported). Bin j (30 degrees wide) holds landmarks 10j..10j+9. Far queries (~50 away)
are unsupported. Expected values are recomputed with the frozen chart kernels.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_chart  # noqa: E402
import c1_config  # noqa: E402
import c1_records  # noqa: E402
import chart  # noqa: E402

L = 120
ANGLES = 2.0 * np.pi * (np.arange(L) + 0.5) / L
RING = np.column_stack([np.cos(ANGLES), np.sin(ANGLES)])
GAUGE = chart.Gauge(sign=1, shift=0.0, alignment=1.0)
NAMES = ("support", "fidelity", "bins", "resultant")


def synthetic_chart(landmarks, phi, info=None):
    n = len(phi)
    zero = np.zeros(0, dtype=np.int64)
    return chart.Chart(np.array([f"{k:020d}" for k in range(n)]), np.asarray(landmarks),
                       np.asarray(phi, dtype=np.float64), 0.05, 0.5, np.full(n, 0.2),
                       np.zeros((0, 2), dtype=np.int64), zero, zero, zero, zero,
                       np.zeros(n, dtype=np.int64), 1, dict(info or {}))


PROD = synthetic_chart(RING, ANGLES)


def queries(bin_counts, n_far):
    rows = [RING[10 * j + i % 10] for j, c in enumerate(bin_counts) for i in range(c)]
    rows += [(30.0 + 2.5 * i, -40.0 + 1.5 * i) for i in range(n_far)]
    Q = np.array(rows, dtype=np.float64)
    assert len(Q) == 512
    return Q


def direct_for(ext_phase, cstar, phi=None):
    phi = ext_phase[cstar] if phi is None else phi
    return synthetic_chart(np.zeros((len(cstar), 2)), phi, {"cstar": np.asarray(cstar)})


def criteria(result):
    c = result["criteria"]
    if isinstance(c, dict):
        out = {}
        for name in NAMES:
            keys = [k for k in c if name in str(k)]
            assert len(keys) == 1, (name, list(c))
            out[name] = bool(c[keys[0]])
        return out
    assert len(c) == 4
    return dict(zip(NAMES, (bool(x) for x in c)))


@pytest.fixture(autouse=True)
def no_chart_gates(monkeypatch):
    """chart.chart_gates must never be called (its support criterion is every-row)."""

    def forbidden(*args, **kwargs):
        raise AssertionError("chart.chart_gates called")

    monkeypatch.setattr(chart, "chart_gates", forbidden)


def evaluate(bin_counts, n_far, cstar=None, direct_phi=None):
    cfg = c1_config.chart_cfg()
    Q = queries(bin_counts, n_far)
    ext = chart.extend(PROD, GAUGE, Q, cfg)
    cstar = np.setdiff1d(np.arange(512), [3, 100]) if cstar is None else np.asarray(cstar)
    direct = direct_for(ext.phase, cstar, direct_phi)
    result = c1_chart.c0_val(PROD, GAUGE, Q, direct, cfg)
    want = {
        "n_supported": int(ext.supported.sum()),
        "fidelity": chart.agreement(ext.phase[cstar], direct.phi),
        "bins": chart.phase_bin_counts(ext.phase, 12),
        "resultant": chart.overall_resultant(ext.phase),
    }
    assert int(result["n_supported"]) == want["n_supported"]
    assert result["fidelity"] == want["fidelity"]
    assert np.asarray(result["bins"]).tolist() == want["bins"].tolist()
    assert result["resultant"] == want["resultant"]
    expect = {
        "support": 100 * want["n_supported"] >= 99 * 512,
        "fidelity": want["fidelity"] >= 0.80,
        "bins": bool(np.all(want["bins"] >= 8)),
        "resultant": want["resultant"] <= 0.30,
    }
    assert criteria(result) == expect
    status = "PASS" if all(expect.values()) else "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert result["status"] == status
    return result, want, ext


BALANCED_507 = [43, 43, 43] + [42] * 9


def test_support_507_of_512_passes():
    result, want, _ = evaluate(BALANCED_507, n_far=5)
    assert want["n_supported"] == 507 and result["status"] == "PASS"


def test_support_506_of_512_fails():
    result, want, _ = evaluate([43, 43, 42] + [42] * 9, n_far=6)
    assert want["n_supported"] == 506
    assert criteria(result) == {"support": False, "fidelity": True, "bins": True,
                                "resultant": True}
    assert result["status"] == "INCONCLUSIVE/CHART_UNAVAILABLE"


def test_bins_and_resultant_use_all_512_queries_including_unsupported():
    """Bins and resultant count every production-extension query, supported or not."""
    result, want, ext = evaluate(BALANCED_507, n_far=5)
    assert int(np.sum(want["bins"])) == 512
    assert not np.all(ext.supported)
    masked = chart.phase_bin_counts(ext.phase[ext.supported], 12)
    assert int(masked.sum()) == 507 and masked.tolist() != want["bins"].tolist()


def test_resultant_fails_while_bins_pass():
    result, want, _ = evaluate([424] + [8] * 11, n_far=0)
    assert want["resultant"] > 0.30 and int(want["bins"].min()) == 8
    assert criteria(result)["resultant"] is False and criteria(result)["bins"] is True


def test_bins_fail_while_resultant_passes():
    result, want, _ = evaluate([7] + [46] * 10 + [45], n_far=0)
    assert int(want["bins"].min()) == 7 and want["resultant"] <= 0.30
    assert criteria(result)["bins"] is False and criteria(result)["resultant"] is True


def test_fidelity_uses_the_complete_direct_component_unmasked_by_support():
    cfg = c1_config.chart_cfg()
    ext = chart.extend(PROD, GAUGE, queries(BALANCED_507, 5), cfg)
    cstar = np.arange(512)  # the direct component retains the unsupported rows too
    phi = ext.phase.copy()
    far = np.flatnonzero(~ext.supported)
    phi[far] = (phi[far] + 2.0) % (2.0 * np.pi)
    result, want, _ = evaluate(BALANCED_507, 5, cstar=cstar, direct_phi=phi)
    masked = chart.agreement(ext.phase[ext.supported], phi[ext.supported])
    assert masked == 1.0 and want["fidelity"] < 1.0
    assert result["fidelity"] == want["fidelity"]


def test_fidelity_below_080_fails():
    rng = np.random.default_rng(20261015)
    cstar = np.setdiff1d(np.arange(512), [3, 100])
    phi = rng.uniform(0.0, 2.0 * np.pi, len(cstar))
    result, want, _ = evaluate(BALANCED_507, 5, cstar=cstar, direct_phi=phi)
    assert want["fidelity"] < 0.80
    assert criteria(result)["fidelity"] is False
    assert result["status"] == "INCONCLUSIVE/CHART_UNAVAILABLE"


def test_extend_phase_is_the_frozen_extend():
    cfg = c1_config.chart_cfg()
    Q = queries(BALANCED_507, 5)
    got, want = c1_chart.extend_phase(PROD, GAUGE, Q, cfg), chart.extend(PROD, GAUGE, Q, cfg)
    for name in ("phase", "resultant", "eighth_distance", "supported", "duplicate"):
        assert np.asarray(getattr(got, name)).tobytes() == np.asarray(
            getattr(want, name)).tobytes(), name


def ledger_path(tmp_path):
    return tmp_path / "CHART_CONSTRUCTIONS.json"


def test_six_constructions_then_refusal(tmp_path):
    ledger = c1_chart.ConstructionLedger(ledger_path(tmp_path))
    for model in (1729, 2718, 3141):
        for role in ("production", "direct"):
            ledger.claim(model, role)
    assert ledger_path(tmp_path).exists()
    with pytest.raises(c1_records.C1GateFailure) as caught:
        ledger.claim(4242, "production")  # a seventh construction
    assert str(caught.value.status).startswith("FAIL_TECHNICAL")


def test_no_second_claim_of_the_same_model_and_role(tmp_path):
    ledger = c1_chart.ConstructionLedger(ledger_path(tmp_path))
    ledger.claim(1729, "production")
    assert ledger_path(tmp_path).exists()  # durable before construction starts
    with pytest.raises(c1_records.C1GateFailure) as caught:
        ledger.claim(1729, "production")
    assert str(caught.value.status).startswith("FAIL_TECHNICAL")
    ledger.claim(1729, "direct")  # the other role is still free


def test_claims_survive_a_new_ledger_object(tmp_path):
    c1_chart.ConstructionLedger(ledger_path(tmp_path)).claim(2718, "direct")
    reopened = c1_chart.ConstructionLedger(ledger_path(tmp_path))
    with pytest.raises(c1_records.C1GateFailure):
        reopened.claim(2718, "direct")
    for model, role in ((1729, "production"), (1729, "direct"), (2718, "production"),
                        (3141, "production"), (3141, "direct")):
        reopened.claim(model, role)
    with pytest.raises(c1_records.C1GateFailure):
        c1_chart.ConstructionLedger(ledger_path(tmp_path)).claim(9999, "direct")
