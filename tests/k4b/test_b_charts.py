"""Author B, K4b TEST_PLAN B4-B8, B12: K4b cfg reaches c1_chart; ledgers (6 trained, 3 step-0,
'direct' refused on step-0); INIT_UNAVAILABLE non-gating, shared-code FAIL_TECHNICAL stops;
freeze before validation, no gauge/refit on validation; GIANT 487/486, support 507/506;
bitwise determinism. Kernels monkeypatched (fit_chart_lcc, chart.extend); no PH, no checkpoint."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import c1_chart  # noqa: E402
import c1_config  # noqa: E402
import chart  # noqa: E402
import errors  # noqa: E402
import k4b_charts  # noqa: E402
import k4b_config  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

MODELS = (1729, 2718, 3141)
N = 512
UNAVAILABLE = "INCONCLUSIVE/CHART_UNAVAILABLE"
GIANT_FAIL = C1GateFailure(UNAVAILABLE, "GIANT_BELOW_0.95")


def outcome(fn, *args, **kwargs):
    try:
        result = fn(*args, **kwargs)
    except C1GateFailure as exc:
        return exc.status, None
    return result["status"], result


def grid_phi(n=N):
    return np.arange(n) * (2 * np.pi / n)


def fake_chart(n=N, d=4, seed=0):
    phi = grid_phi(n)
    info = {"cstar": list(range(n)), "m": n, "n": n, "lift_kind": "centered_exact",
            "excluded_ids": [], "n_components": 1, "component_sizes": [n]}
    rng = np.random.default_rng(seed)
    e = np.zeros(0, dtype=np.int64)
    return chart.Chart(c1_chart.landmark_ids(np.arange(n) + 10**6), rng.normal(size=(n, d)),
                       phi, 1.0, 2.0, np.ones(n), np.zeros((0, 2), dtype=np.int64), e, e, e, e,
                       np.zeros(n, dtype=np.int64), 1, info)


M32 = 0.5 * np.column_stack((np.cos(grid_phi()), np.sin(grid_phi())))


class Kernel:
    """Fake fit_chart_lcc: records each call and the ledger claims present at call time."""

    def __init__(self, out, plan=()):
        self.out, self.plan, self.calls = Path(out), list(plan), []

    def __call__(self, X, ids, cfg, guard=None, timed=None, persist=None):
        claims = [c1_chart.ConstructionLedger(self.out / name).claims()
                  for name in (k4b_charts.TRAINED_LEDGER, k4b_charts.INIT_LEDGER)]
        self.calls.append({"cfg": dict(cfg), "claims": claims})
        action = self.plan.pop(0) if self.plan else None
        if isinstance(action, BaseException):
            raise action
        return fake_chart()


def patch(monkeypatch, name, fn, module=c1_chart):
    monkeypatch.setattr(module, name, fn)
    if hasattr(k4b_charts, name):
        monkeypatch.setattr(k4b_charts, name, fn)


def inputs(seed=1):
    rng = np.random.default_rng(seed)
    X = {j: rng.normal(size=(N, 4)) for j in MODELS}
    ids = c1_chart.landmark_ids(np.arange(N, dtype=np.int64) + 10**6)
    return X, ids


def ledger_claims(out, name):
    return c1_chart.ConstructionLedger(Path(out) / name).claims()


# ------------------------------------------------------------------------ cfg equality (B4)

def test_chart_cfg_equals_c1prime_cfg():
    cfg = k4b_config.chart_cfg()
    assert cfg == c1_config.chart_cfg(c1_config.CONTRACT)
    assert set(cfg) == set(c1_config.CHART_KERNEL_KEYS) | {"lift_cpu_cap_s",
                                                          "native_operation_wall_s"}
    assert cfg["lift_cpu_cap_s"] == float("inf")
    assert cfg["native_operation_wall_s"] == 600.0


def test_check_chart_equality_default_is_equal():
    r = k4b_config.check_chart_equality()
    assert r["equal"] is True and r["cfg_diff"] == []
    assert r["giant_equal"] is True and r["val_support_equal"] is True


def test_check_chart_equality_detects_each_difference():
    k = copy.deepcopy(k4b_config.CONTRACT)
    k["chart"]["field"] = 2
    r = k4b_config.check_chart_equality(k)
    assert r["equal"] is False and r["cfg_diff"] == ["field"]
    g = copy.deepcopy(k4b_config.CONTRACT)
    g["chart"]["giant"]["min_m"] = 486
    assert k4b_config.check_chart_equality(g)["giant_equal"] is False
    s = copy.deepcopy(k4b_config.CONTRACT)
    s["chart"]["val_support"]["min_supported"] = 506
    assert k4b_config.check_chart_equality(s)["val_support_equal"] is False


def test_build_chart_claims_first_and_passes_k4b_cfg(tmp_path, monkeypatch):
    kernel = Kernel(tmp_path)
    patch(monkeypatch, "fit_chart_lcc", kernel)
    trained, _ = k4b_charts.open_ledgers(tmp_path)
    X, ids = inputs()
    cfg = k4b_config.chart_cfg()
    res = k4b_charts.build_chart(X[1729], ids, M32, trained, 1729, "production", cfg)
    assert res["status"] == "PASS"
    assert kernel.calls[0]["cfg"] == cfg
    assert [1729, "production"] in kernel.calls[0]["claims"][0]  # claimed before fitting
    assert res["gauge"] == chart.fit_gauge(fake_chart(), M32)
    assert str(res["serial"]["info_json"]).count('"role": "production"') == 1
    direct = k4b_charts.build_chart(X[1729], ids, M32, trained, 1729, "direct", cfg)
    assert direct["gauge"] == c1_chart.IDENTITY_CARRIER
    assert '"role": "validation_only"' in str(direct["serial"]["info_json"])


def test_failed_construction_keeps_its_claim_and_is_never_retried(tmp_path, monkeypatch):
    patch(monkeypatch, "fit_chart_lcc", Kernel(tmp_path, [GIANT_FAIL]))
    trained, _ = k4b_charts.open_ledgers(tmp_path)
    X, ids = inputs()
    cfg = k4b_config.chart_cfg()
    status, _ = outcome(k4b_charts.build_chart, X[2718], ids, M32, trained, 2718,
                        "production", cfg)
    assert status == UNAVAILABLE
    assert [2718, "production"] in ledger_claims(tmp_path, k4b_charts.TRAINED_LEDGER)
    again, _ = outcome(k4b_charts.build_chart, X[2718], ids, M32, trained, 2718,
                       "production", cfg)
    assert again.startswith("FAIL_TECHNICAL")


# ----------------------------------------------------------------------------- ledgers (B5)

def test_open_ledgers_two_files(tmp_path):
    assert k4b_charts.TRAINED_LEDGER == "CHART_CONSTRUCTIONS_trained.json"
    assert k4b_charts.INIT_LEDGER == "CHART_CONSTRUCTIONS_init.json"
    trained, init = k4b_charts.open_ledgers(tmp_path)
    assert isinstance(trained, c1_chart.ConstructionLedger)
    assert isinstance(init, k4b_charts.InitLedger)
    assert Path(trained.path) == tmp_path / k4b_charts.TRAINED_LEDGER


def test_trained_ledger_holds_six(tmp_path):
    trained, _ = k4b_charts.open_ledgers(tmp_path)
    for j in MODELS:
        for role in ("production", "direct"):
            trained.claim(j, role)
    assert len(trained.claims()) == 6
    with pytest.raises(C1GateFailure) as exc:
        trained.claim(9999, "production")
    assert exc.value.status.startswith("FAIL_TECHNICAL")


@pytest.mark.parametrize("role", ["direct", "validation_only"])
def test_init_ledger_refuses_any_role_but_production(tmp_path, role):
    _, init = k4b_charts.open_ledgers(tmp_path)
    with pytest.raises(C1GateFailure) as exc:
        init.claim(1729, role)
    assert exc.value.status == "FAIL_TECHNICAL"
    if role == "direct":
        assert exc.value.reason == "role 'direct' refused on the step-0 ledger"
    assert init.claims() == []


def test_init_ledger_three_production_claims(tmp_path):
    trained, init = k4b_charts.open_ledgers(tmp_path)
    for j in MODELS:
        init.claim(j, "production")
    assert len(init.claims()) == 3
    assert len(ledger_claims(tmp_path, k4b_charts.INIT_LEDGER)) == 3
    with pytest.raises(C1GateFailure):
        init.claim(1729, "production")
    assert trained.claims() == []


# ------------------------------------------------------------------- step-0 charts (B6)

def test_init_unavailable_is_non_gating(tmp_path, monkeypatch):
    kernel = Kernel(tmp_path, [None, GIANT_FAIL, None])
    patch(monkeypatch, "fit_chart_lcc", kernel)
    X, ids = inputs(2)
    res = k4b_charts.init_charts(MODELS, X, ids, M32, tmp_path, k4b_config.chart_cfg())
    per = res.get("per_model", res)
    assert per[2718]["status"] == "INIT_UNAVAILABLE" and per[2718]["reason"]
    assert per[1729]["status"] == "PASS" and per[3141]["status"] == "PASS"
    assert len(kernel.calls) == 3
    assert len(ledger_claims(tmp_path, k4b_charts.INIT_LEDGER)) == 3
    assert ledger_claims(tmp_path, k4b_charts.TRAINED_LEDGER) == []


@pytest.mark.parametrize("plan,n_calls", [
    ([errors.Invalid("exact duplicate landmarks carry conflicting phases")], 1),
    ([None, errors.Invalid("queries must be finite")], 2),
])
def test_init_shared_code_fail_technical_stops_immediately(tmp_path, monkeypatch, plan, n_calls):
    kernel = Kernel(tmp_path, plan)
    patch(monkeypatch, "fit_chart_lcc", kernel)
    X, ids = inputs(3)
    with pytest.raises(C1GateFailure) as exc:
        k4b_charts.init_charts(MODELS, X, ids, M32, tmp_path, k4b_config.chart_cfg())
    assert exc.value.status.startswith("FAIL_TECHNICAL")
    assert len(kernel.calls) == n_calls


def test_init_gauge_integrity_defect_stops(tmp_path, monkeypatch):
    patch(monkeypatch, "fit_chart_lcc", Kernel(tmp_path))
    X, ids = inputs(4)
    bad = M32.copy()
    bad[3, 0] = np.nan
    with pytest.raises(C1GateFailure) as exc:
        k4b_charts.init_charts(MODELS, X, ids, bad, tmp_path, k4b_config.chart_cfg())
    assert exc.value.status.startswith("FAIL_TECHNICAL")


# --------------------------------------------- freeze, no gauge/refit on validation (B7, B8)

def fake_extend(n_sup):
    def ext(ch, gauge, Q, cfg, timed=None):
        m = len(Q)
        return chart.Extension(grid_phi(m), np.ones(m), np.zeros(m), np.arange(m) < n_sup,
                               np.zeros(m, dtype=bool))
    return ext


def frozen_store(out, monkeypatch, kernel):
    patch(monkeypatch, "fit_chart_lcc", kernel)
    X, ids = inputs(5)
    cfg = k4b_config.chart_cfg()
    cal = k4b_charts.c0_cal(MODELS, X, ids, M32, out, cfg, None, None, None)
    assert cal["status"] == "PASS"
    init = k4b_charts.init_charts(MODELS, X, ids, M32, out, cfg)
    decoders = {j: {"status": "UNAVAILABLE", "reason": "degenerate bandwidth"} for j in MODELS}
    record = k4b_charts.freeze_production(out, cal["per_model"], init, decoders)
    assert (Path(out) / "stages" / "S4a" / "PRODUCTION_FROZEN.json").exists()
    assert record
    return cal


def test_require_frozen_refuses_without_record(tmp_path):
    with pytest.raises(C1GateFailure) as exc:
        k4b_charts.require_frozen(tmp_path)
    assert exc.value.status == "FAIL_TECHNICAL/LINEAGE"


def test_c0_val_gate_refused_before_freeze_spends_no_construction(tmp_path, monkeypatch):
    kernel = Kernel(tmp_path)
    patch(monkeypatch, "fit_chart_lcc", kernel)
    X, ids = inputs(6)
    prod = {j: {"chart": fake_chart(), "gauge": chart.fit_gauge(fake_chart(), M32)}
            for j in MODELS}
    status, _ = outcome(k4b_charts.c0_val_gate, MODELS, prod, X, ids, tmp_path,
                        k4b_config.chart_cfg())
    assert status == "FAIL_TECHNICAL/LINEAGE"
    assert kernel.calls == []
    assert ledger_claims(tmp_path, k4b_charts.TRAINED_LEDGER) == []


def test_tampered_frozen_artefact_refused(tmp_path, monkeypatch):
    frozen_store(tmp_path, monkeypatch, Kernel(tmp_path))
    k4b_charts.require_frozen(tmp_path)
    files = [p for p in (tmp_path / "stages").rglob("*")
             if p.is_file() and p.name != "PRODUCTION_FROZEN.json"]
    assert files
    for p in files:
        with p.open("ab") as handle:
            handle.write(b"\0")
    with pytest.raises(C1GateFailure) as exc:
        k4b_charts.require_frozen(tmp_path)
    assert exc.value.status == "FAIL_TECHNICAL/LINEAGE"


def run_val_gate(out, monkeypatch, n_sup, direct_plan=()):
    kernel = Kernel(out)
    cal = frozen_store(out, monkeypatch, kernel)
    kernel.plan = list(direct_plan)
    n_before = len(kernel.calls)

    def no_gauge(*args, **kwargs):
        raise AssertionError("no gauge is fitted on validation data")

    seen = []
    real_c0_val = c1_chart.c0_val

    def spy_c0_val(prod, gauge, val_X, direct, cfg):
        seen.append((prod, gauge))
        return real_c0_val(prod, gauge, val_X, direct, cfg)

    patch(monkeypatch, "fit_production_gauge", no_gauge)
    monkeypatch.setattr(chart, "fit_gauge", no_gauge)
    patch(monkeypatch, "c0_val", spy_c0_val)
    monkeypatch.setattr(chart, "extend", fake_extend(n_sup))
    rng = np.random.default_rng(7)
    val_X = {j: rng.normal(size=(N, 4)) for j in MODELS}
    ids_val = c1_chart.landmark_ids(np.arange(N, dtype=np.int64) + 2 * 10**6)
    status, res = outcome(k4b_charts.c0_val_gate, MODELS, cal["per_model"], val_X, ids_val,
                          out, k4b_config.chart_cfg())
    return status, res, cal, kernel, n_before, seen


def test_c0_val_support_507_passes_without_gauge_or_refit(tmp_path, monkeypatch):
    status, _, cal, kernel, n_before, seen = run_val_gate(tmp_path, monkeypatch, 507)
    assert status == "PASS"
    assert len(kernel.calls) - n_before == 3  # one direct chart per model, nothing else
    claims = ledger_claims(tmp_path, k4b_charts.TRAINED_LEDGER)
    assert sorted(map(tuple, claims)) == sorted((j, r) for j in MODELS
                                                for r in ("production", "direct"))
    assert len(seen) == 3
    for (prod, gauge), j in zip(seen, MODELS):
        ref = cal["per_model"][j]
        assert np.array_equal(prod.phi, ref["chart"].phi)
        assert gauge == ref["gauge"]


def test_c0_val_support_506_is_chart_unavailable(tmp_path, monkeypatch):
    assert run_val_gate(tmp_path, monkeypatch, 506)[0] == UNAVAILABLE


def test_c0_val_direct_giant_failure_is_chart_unavailable(tmp_path, monkeypatch):
    assert run_val_gate(tmp_path, monkeypatch, 512, [GIANT_FAIL])[0] == UNAVAILABLE


# --------------------------------------------------------------- frozen thresholds (B8)

def test_giant_487_passes_486_fails():
    assert k4b_config.CONTRACT["chart"]["giant"]["min_m"] == 487
    assert c1_chart.giant_pass(487, 512) is True
    assert c1_chart.giant_pass(486, 512) is False


@pytest.mark.parametrize("n_sup,ok", [(507, True), (506, False)])
def test_c0_val_support_threshold_with_k4b_cfg(monkeypatch, n_sup, ok):
    assert k4b_config.CONTRACT["chart"]["val_support"]["min_supported"] == 507
    monkeypatch.setattr(chart, "extend", fake_extend(n_sup))
    prod = fake_chart()
    r = c1_chart.c0_val(prod, chart.fit_gauge(prod, M32), np.zeros((N, 4)), fake_chart(),
                        k4b_config.chart_cfg())
    assert r["criteria"]["support"] is ok
    assert r["status"] == ("PASS" if ok else UNAVAILABLE)


# ------------------------------------------------------------------- determinism (B12)

LABELS = [f"{j}/{step}" for j in MODELS for step in ("step5000", "step0")]


def activations():
    rng = np.random.default_rng(8)
    return {k: rng.normal(size=(3072, 128)) for k in LABELS}


def test_determinism_identical_passes():
    stored = activations()
    again = {k: v.copy() for k, v in stored.items()}
    r = k4b_charts.determinism_check(stored, again)
    assert r["status"] == "PASS" and list(r["mismatch"]) == []


@pytest.mark.parametrize("change", ["bit", "dtype", "shape", "negzero"])
def test_determinism_any_bitwise_difference_fails(change):
    stored = activations()
    again = {k: v.copy() for k, v in stored.items()}
    key = LABELS[3]
    if change == "bit":
        again[key][5, 7] = np.nextafter(again[key][5, 7], np.inf)
    elif change == "dtype":
        again[key] = again[key].astype(np.float32).astype(np.float64)
        stored[key] = stored[key].astype(np.float32)
    elif change == "shape":
        again[key] = again[key][:3071]
    else:
        stored[key][0, 0] = 0.0
        again[key][0, 0] = -0.0  # equal by value, different bytes
    r = k4b_charts.determinism_check(stored, again)
    assert r["status"] == "FAIL_TECHNICAL/DETERMINISM"
    assert list(r["mismatch"]) == [key]
