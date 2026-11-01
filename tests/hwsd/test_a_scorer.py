"""Author A (job 0197): the per-checkpoint scorer and its registered statuses (§2.4, §2.6, §7 rows
9-10; API.md §6 and §16; DRD6).

Chart kernels are replaced by spies (k4b_charts.build_chart/extend, k4b_decoder.fit/to_arrays,
c1_chart.c0_val) so that the order, the ledger claims, the freeze and the status mapping are
observed without any chart construction. The real c1_chart.ConstructionLedger is used.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import namedtuple
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_score as ds  # noqa: E402
import c1_chart  # noqa: E402
import k4b_charts  # noqa: E402
import k4b_decoder  # noqa: E402
import k4b_scores  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

Gauge = namedtuple("Gauge", "sign shift alignment")
Ext = namedtuple("Ext", "phase supported")
WALL = "native operation fit_chart_lcc ran 612.0 s, past the 600 s wall"
CRIT_FAIL = {"support": True, "fidelity": True, "bins": False, "resultant": False}
CRIT_PASS = {"support": True, "fidelity": True, "bins": True, "resultant": True}


class FakeChart:
    support_radius = 1.0


def tabs(n=24, n_land=8, seed=0):
    rng = np.random.default_rng(seed)
    out = {}
    for split in ("cal", "val", "test"):
        land = np.zeros(n, dtype=bool)
        land[:n_land] = True
        out[split] = {"seq_ids": np.arange(n, dtype=np.int64) + 1000 * len(split),
                      "canon32": rng.integers(0, 36, size=(n, 32)).astype(np.uint8),
                      "landmark": land}
    return out


def install(monkeypatch, log, prod=("PASS", ""), direct=("PASS", ""), c0=("PASS", CRIT_PASS)):
    def build_chart(X, ids, m32, ledger, model, role, cfg, guard=None, timed=None, persist=None):
        log.append(("build", role))
        ledger.claim(model, role)
        st, rs = prod if role == "production" else direct
        good = st == "PASS"
        return {"status": st, "reason": rs, "chart": FakeChart() if good else None,
                "gauge": Gauge(1, 0.0, 0.5) if good else None,
                "serial": {"phi": np.arange(3.0), "sigma": np.ones(3)} if good else None,
                "diagnostics": {"role": role}}

    def extend(chart, gauge, Q, cfg, timed=None):
        log.append(("extend",))
        return Ext(np.linspace(0.0, 6.0, len(Q)), np.ones(len(Q), dtype=bool))

    def fit(canon32, ids, phi, model):
        log.append(("fit",))
        return {"status": "AVAILABLE", "reason": ""}

    def c0_val(p, gauge, val_X, d, cfg):
        log.append(("c0_val",))
        return {"status": c0[0], "n": 512, "n_supported": 512, "fidelity": 0.9,
                "bins": [43] * 12, "resultant": 0.1, "criteria": dict(c0[1])}

    monkeypatch.setattr(k4b_charts, "build_chart", build_chart)
    monkeypatch.setattr(k4b_charts, "extend", extend)
    monkeypatch.setattr(k4b_decoder, "fit", fit)
    monkeypatch.setattr(k4b_decoder, "to_arrays", lambda dec: {"W": np.ones(2)})
    monkeypatch.setattr(c1_chart, "c0_val", c0_val)


def acts_spy(log, out_dir, t):
    def acts(split):
        log.append(("acts", split, (out_dir / "FROZEN.json").exists()))
        return np.random.default_rng(len(split)).normal(size=(len(t[split]["seq_ids"]), 128))
    return acts


def run_chart(monkeypatch, tmp_path, j=620301, step=100, skip_direct=False, ledger=None, **kw):
    log = []
    install(monkeypatch, log, **kw)
    t = tabs()
    out_dir = ds.checkpoint_dir(tmp_path, j, step)
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger = ledger or ds.ledger_for(tmp_path, j, step)
    m32 = np.ones((24, 2)) * 0.1
    res = ds.chart_one(j, acts_spy(log, out_dir, t), t, m32, ledger, {"cfg": "fake"}, out_dir,
                       timed=None, skip_direct=skip_direct)
    return res, log, out_dir, ledger


def kinds(log):
    return [e[0] if e[0] != "build" else "build:" + e[1] for e in log]


# ---- layout ----
def test_checkpoint_dir_and_one_ledger_per_checkpoint(tmp_path):
    want = tmp_path / "stages" / "SCORE" / "620302" / "s700"
    assert ds.checkpoint_dir(tmp_path, 620302, 700) == want
    for step in (0, 50):
        ds.checkpoint_dir(tmp_path, 620301, step).mkdir(parents=True, exist_ok=True)
        ds.ledger_for(tmp_path, 620301, step).claim(620301, "production")
    files = sorted(tmp_path.rglob("CHART_CONSTRUCTIONS.json"))
    assert files == [ds.checkpoint_dir(tmp_path, 620301, s) / "CHART_CONSTRUCTIONS.json"
                     for s in (0, 50)]


# ---- chart_one order, freeze, ledger ----
def test_chart_one_pass_order_and_freeze(monkeypatch, tmp_path):
    res, log, out_dir, _ = run_chart(monkeypatch, tmp_path)
    k = kinds(log)
    assert k.index("acts") < k.index("build:production") < k.index("fit")
    val = [e for e in log if e[0] == "acts" and e[1] == "val"]
    assert val and all(e[2] for e in val)  # val activations only after FROZEN.json exists
    assert k.index("fit") < k.index("build:direct") < k.index("c0_val")
    assert [e for e in log if e[0] == "acts" and e[1] == "test"] == []
    fz = json.loads((out_dir / "FROZEN.json").read_text(encoding="utf-8"))
    for name in ("CHART.npz", "DECODER.npz", "ACTS_cal.npz"):
        assert fz["files"][name] == hashlib.sha256((out_dir / name).read_bytes()).hexdigest()
    assert fz["c0_cal"] == "PASS" and fz["decoder_status"] == "AVAILABLE"
    assert fz["gauge"] == [1, 0.0, 0.5]
    with np.load(out_dir / "ACTS_cal.npz", allow_pickle=False) as z:
        assert np.array_equal(z["acts"], res["acts_cal"])
    assert res["c0_cal"]["status"] == "PASS" and res["c0_val"]["status"] == "PASS"
    assert isinstance(res["prod"]["chart"], FakeChart) and res["frozen"] is not None
    assert res["decoder"]["status"] == "AVAILABLE"
    assert ds.status_of_checkpoint(res, {"status": "PASS", "certified": {}}) == ("SCORED", "SCORED")


def test_second_construction_of_a_role_is_refused(monkeypatch, tmp_path):
    _, _, _, ledger = run_chart(monkeypatch, tmp_path)
    with pytest.raises(C1GateFailure) as e:
        run_chart(monkeypatch, tmp_path / "again", ledger=ledger)
    assert e.value.status.startswith("FAIL_TECHNICAL")


def test_c0_cal_failure_no_direct_no_decoder_no_freeze(monkeypatch, tmp_path):
    res, log, out_dir, _ = run_chart(
        monkeypatch, tmp_path, prod=("INCONCLUSIVE/CHART_UNAVAILABLE", "GIANT_BELOW_0.95"))
    assert kinds(log).count("build:production") == 1 and "build:direct" not in kinds(log)
    assert "fit" not in kinds(log) and "c0_val" not in kinds(log)
    assert not (out_dir / "FROZEN.json").exists()
    assert [e for e in log if e[0] == "acts" and e[1] != "cal"] == []
    assert res["prod"] is None and res["decoder"] is None and res["frozen"] is None
    assert res["c0_val"] is None
    assert res["c0_cal"]["status"] == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert ds.status_of_checkpoint(res, None) == (
        "CHART_UNAVAILABLE", "CHART_UNAVAILABLE/INCONCLUSIVE/CHART_UNAVAILABLE: GIANT_BELOW_0.95")


def test_c0_cal_fail_technical_stops(monkeypatch, tmp_path):
    with pytest.raises(C1GateFailure) as e:
        run_chart(monkeypatch, tmp_path, prod=("FAIL_TECHNICAL/NUMERICAL", "non-finite phase"))
    assert e.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_skip_direct(monkeypatch, tmp_path):
    res, log, out_dir, _ = run_chart(monkeypatch, tmp_path, skip_direct=True)
    assert "build:direct" not in kinds(log) and "c0_val" not in kinds(log)
    assert [e for e in log if e[0] == "acts" and e[1] == "val"] == []
    assert (out_dir / "FROZEN.json").exists() and res["c0_val"] is None


@pytest.mark.parametrize("st,reason,label", [
    ("INCONCLUSIVE", "NO_H1_BAR", "SCORED_UNVALIDATED/INCONCLUSIVE: NO_H1_BAR"),
    ("INCONCLUSIVE/CHART_UNAVAILABLE", "GIANT_BELOW_0.95",
     "SCORED_UNVALIDATED/INCONCLUSIVE/CHART_UNAVAILABLE: GIANT_BELOW_0.95"),
    ("INCONCLUSIVE/RESOURCE", "memory", "SCORED_UNVALIDATED/INCONCLUSIVE/RESOURCE: memory"),
    ("INCONCLUSIVE", WALL, "SCORED_UNVALIDATED/NATIVE_WALL: " + WALL),
])
def test_direct_chart_not_pass_labels(monkeypatch, tmp_path, st, reason, label):
    res, log, _, _ = run_chart(monkeypatch, tmp_path, direct=(st, reason))
    assert "c0_val" not in kinds(log)
    assert res["c0_val"]["status"] != "PASS" and res["c0_val"]["direct_status"] == st
    assert ds.status_of_checkpoint(res, {"status": "PASS", "certified": {}}) == (
        "SCORED_UNVALIDATED", label)


def test_direct_fail_technical_stops(monkeypatch, tmp_path):
    with pytest.raises(C1GateFailure) as e:
        run_chart(monkeypatch, tmp_path, direct=("FAIL_TECHNICAL/BLINDNESS", "x"))
    assert e.value.status == "FAIL_TECHNICAL/BLINDNESS"


def test_c0_val_criteria_label(monkeypatch, tmp_path):
    # API-AMBIGUITY: c0_val "criteria" (four booleans) read as {criterion: passed}.
    res, _, _, _ = run_chart(monkeypatch, tmp_path,
                             c0=("INCONCLUSIVE/CHART_UNAVAILABLE", CRIT_FAIL))
    assert res["c0_val"]["status"] == "INCONCLUSIVE/CHART_UNAVAILABLE"
    assert ds.status_of_checkpoint(res, {"status": "PASS", "certified": {}}) == (
        "SCORED_UNVALIDATED", "SCORED_UNVALIDATED/CRITERIA: bins,resultant")


def test_native_wall_at_c0_cal(monkeypatch, tmp_path):
    res, _, _, _ = run_chart(monkeypatch, tmp_path, prod=("INCONCLUSIVE", WALL))
    assert ds.status_of_checkpoint(res, None) == (
        "CHART_UNAVAILABLE", "CHART_UNAVAILABLE/NATIVE_WALL: " + WALL)


def test_archived_wall_label_protocol_reading():
    # SPEC-QUESTION: API.md §6 score_checkpoint records an archived (X-3) killed production
    # construction as C0-CAL {"status": "INCONCLUSIVE", "reason": "NATIVE_WALL: <label>
    # (archived)"}; read through map_build that would label "CHART_UNAVAILABLE/INCONCLUSIVE:
    # NATIVE_WALL: ...". The protocol (§2.6 RC-8, DRD6) and CONTRACT statuses.label_formats
    # say CHART_UNAVAILABLE/NATIVE_WALL: <reason>; this test asserts the protocol's form.
    ch = {"c0_cal": {"status": "INCONCLUSIVE", "reason": "NATIVE_WALL: op-17 (archived)",
                     "diagnostics": None},
          "c0_val": None, "prod": None, "decoder": None, "frozen": None}
    status, label = ds.status_of_checkpoint(ch, None)
    assert status == "CHART_UNAVAILABLE"
    assert label.startswith("CHART_UNAVAILABLE/NATIVE_WALL: ") and "op-17 (archived)" in label


def test_uncertified_precedes_validation(monkeypatch, tmp_path):
    res, _, _, _ = run_chart(monkeypatch, tmp_path,
                             c0=("INCONCLUSIVE/CHART_UNAVAILABLE", CRIT_FAIL))
    cert = {"status": "INCONCLUSIVE/NUMERICAL",
            "certified": {"X_minus": False, "X_plus": True, "n_hat": False}}
    assert ds.status_of_checkpoint(res, cert) == (
        "UNCERTIFIED", "UNCERTIFIED/INCONCLUSIVE/NUMERICAL: X_minus,n_hat")


def test_36_checkpoints_at_most_72_claims(monkeypatch, tmp_path):
    n_build = 0
    for j in dc.MASTERS:
        for step in dc.STEPS:
            _, log, _, _ = run_chart(monkeypatch, tmp_path, j=j, step=step)
            n_build += kinds(log).count("build:production") + kinds(log).count("build:direct")
    files = list(tmp_path.rglob("CHART_CONSTRUCTIONS.json"))
    assert n_build == 72 and len(files) == 36
    for f in files:
        assert len(c1_chart.ConstructionLedger(f).claims()) == 2


# ---- map_build (§7 row 9) ----
def test_map_build_rules():
    with pytest.raises(C1GateFailure) as e:
        ds.map_build({"status": "FAIL_TECHNICAL/NUMERICAL", "reason": "r"}, "C0-CAL")
    assert e.value.status == "FAIL_TECHNICAL/NUMERICAL"
    assert ds.map_build({"status": "INCONCLUSIVE", "reason": WALL}, "w") == {
        "kind": "NATIVE_WALL", "text": "NATIVE_WALL: " + WALL}
    assert ds.map_build({"status": "INCONCLUSIVE", "reason": "NO_H1_BAR"}, "w") == {
        "kind": "INCONCLUSIVE", "text": "INCONCLUSIVE: NO_H1_BAR"}
    for st in ("INCONCLUSIVE/CHART_UNAVAILABLE", "INCONCLUSIVE/RESOURCE"):
        assert ds.map_build({"status": st, "reason": "x"}, "w") == {"kind": st, "text": st + ": x"}
    # the wall rule needs the bare INCONCLUSIVE status of op_guard's Unresolved
    assert ds.map_build({"status": "INCONCLUSIVE/RESOURCE", "reason": WALL}, "w")["kind"] == (
        "INCONCLUSIVE/RESOURCE")


# ---- arrays_one (planted) and controls_one ----
def moments(n, seed=3):
    rng = np.random.default_rng(seed)
    return {K: rng.normal(scale=0.3, size=(n, 2)) for K in (1, 2, 4, 32)}


def test_arrays_one_planted(monkeypatch):
    n = 40
    m = moments(n)
    phase = np.random.default_rng(4).uniform(0, 2 * np.pi, n)
    sup = np.arange(n) % 3 != 0
    monkeypatch.setattr(k4b_charts, "extend", lambda c, g, Q, cfg, timed=None: Ext(phase, sup))
    r = ds.arrays_one({"chart": FakeChart(), "gauge": Gauge(1, 0.0, 0.5)}, np.zeros((n, 128)), m,
                      None, None, {"cfg": "fake"}, planted=True)
    c = r["certificate"]
    assert c["status"] == "PASS" and c["planted"] is True and r["bounds"] is None
    assert c["max_B"] == {"X_minus": Fraction(0), "X_plus": Fraction(0), "n_hat": Fraction(0)}
    a = r["arrays"]
    r4 = m[32] - m[4]
    norm = np.sqrt(np.sum(r4 ** 2, axis=1))
    dot = np.cos(phase) * r4[:, 0] + np.sin(phase) * r4[:, 1]
    np.testing.assert_allclose(a["X_minus"][sup], dot[sup], rtol=0, atol=1e-15)
    np.testing.assert_allclose(a["X_plus"][sup], dot[sup], rtol=0, atol=1e-15)
    np.testing.assert_allclose(a["X_minus"][~sup], -norm[~sup], rtol=0, atol=1e-15)
    np.testing.assert_allclose(a["X_plus"][~sup], norm[~sup], rtol=0, atol=1e-15)
    assert np.all(a["X_minus"] <= a["X_plus"])
    ref = k4b_scores.endpoint_arrays(phase, sup, m[32], m[4])
    for key in ("X_minus", "X_plus", "r4n"):
        assert np.array_equal(a[key], ref[key])
    assert r["max_abs"] == {"X_minus": float(np.max(np.abs(a["X_minus"]))),
                            "X_plus": float(np.max(np.abs(a["X_plus"])))}


def test_controls_one_against_control_arrays(monkeypatch):
    n = 30
    m = moments(n, seed=5)
    rng = np.random.default_rng(6)
    canon = rng.integers(0, 36, size=(n, 32)).astype(np.uint8)
    psi = rng.uniform(0, 2 * np.pi, n)
    monkeypatch.setattr(k4b_decoder, "predict_phase", lambda dec, c32: psi.copy())
    ext = {j: Ext(rng.uniform(0, 2 * np.pi, n), rng.random(n) < 0.8) for j in (1729, 2718, 3141)}
    decs = {1729: {"status": "AVAILABLE", "reason": ""},
            2718: {"status": "UNAVAILABLE", "reason": "equivalence"},
            3141: {"status": "AVAILABLE", "reason": ""}}
    full = k4b_scores.control_arrays(m, canon, ext, {j: {"unavailable": "n/a"} for j in ext}, decs)
    for j in (1729, 3141):
        c = ds.controls_one(m, canon, ext[j], decs[j])
        assert set(c) == {"decoder", "delta1", "delta2", "naive"}
        for name in c:
            for key, v in full[name][j].items():
                assert np.array_equal(np.asarray(c[name][key]), np.asarray(v)), (name, key)
        np.testing.assert_array_equal(c["decoder"]["phi"], psi)
        naive = k4b_scores.naive_scores(ext[j].phase, m[32], m[4])
        np.testing.assert_array_equal(c["naive"]["X"], naive)
    c = ds.controls_one(m, canon, ext[2718], decs[2718])
    assert c["decoder"] == {"unavailable": "equivalence"}
