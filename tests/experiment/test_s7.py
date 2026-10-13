"""Stage S7 (TEST_PLAN X17-X21), from SPEC.md "Stage S7" only; stub stores, no training."""
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import (
    ActivationSet,
    ErrorCode,
    GateReport,
    MetricRecords,
    MetricRow,
    ObservationSet,
    StageFailure,
)
from topo_pilot.contracts.testing import memory_store, tiny_observations
from topo_pilot.experiment import STAGE_REGISTRY, load_config, s7_probes
from topo_pilot.experiment.s3 import on_test_split
from topo_pilot.experiment.s7 import S7Runs, gate_gg
from topo_pilot.experiment.s7_circular import CircularJob
from topo_pilot.experiment.s7_dev import ProbeData
from topo_pilot.experiment.s7_probes import ProbesJob

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]
CONS = "experiment"
JOBS = ("dev_extract", "controls", "probes", "circular", "sensitivity")


@pytest.fixture(scope="module")
def cfg():
    return load_config(REPO / "configs" / "stages.yaml", repo_root=REPO)


def _save_rec(store, config, rows=()):
    return store.save(MetricRecords(rows=tuple(rows)), config=config, parents=[], seed_map={},
                      consumer=CONS)


def _runs(cfg):
    return [dict(r) for r in cfg.stage("S7")["runs_ordered"]]


def _run_key(r):
    return [r["world"], r["condition"], int(r["seed"])]


def _fill_store(cfg, store, skip_run=None, failed_run=None, jobs=JOBS):
    for r in _runs(cfg):
        key = _run_key(r)
        if key == skip_run:
            continue
        conf = {"stage": "S7", "kind": "run", "run_key": key}
        if key == failed_run:
            conf["outcome"] = "failed"
        _save_rec(store, conf)
    for j in jobs:
        _save_rec(store, {"stage": "S7", "kind": j})


# ----------------------------------------------------------------------------------- X17
def test_X17_registry_requires_and_gates():
    cls = STAGE_REGISTRY["S7"]
    assert tuple(cls.requires) == ("S4", "S5")
    assert tuple(cls.gates) == ("G-G",)


def test_X17_plan_missing_s6_raises_missing_parent(cfg):
    store = memory_store()
    with pytest.raises(StageFailure) as ei:
        STAGE_REGISTRY["S7"]().plan(cfg, store)
    assert ei.value.code == ErrorCode.MISSING_PARENT
    # only O present: still missing P
    _save_rec(store, {"stage": "S6", "kind": "dynamics", "condition": "O"})
    with pytest.raises(StageFailure) as ei:
        STAGE_REGISTRY["S7"]().plan(cfg, store)
    assert ei.value.code == ErrorCode.MISSING_PARENT


def test_X17_plan_order_with_s6_records(cfg):
    store = memory_store()
    for c in ("O", "P"):
        _save_rec(store, {"stage": "S6", "kind": "dynamics", "condition": c})
    plan = STAGE_REGISTRY["S7"]().plan(cfg, store)
    runs = _runs(cfg)
    assert len(runs) == 4
    assert [dict(p) for p in plan[:4]] == runs
    assert [p["job"] for p in plan[4:]] == [*JOBS, "gate"]
    assert len(plan) == 10


# ----------------------------------------------------------------------------------- X18
def test_X18_gate_gg_passes_when_all_documented(cfg):
    store = memory_store()
    _fill_store(cfg, store)
    rep = store.load(GateReport, gate_gg(cfg, store), consumer=CONS)
    assert rep.gate_id == "G-G" and rep.verdict == "pass"
    names = {c.name for c in rep.checks}
    assert len(rep.checks) == 4 + 5
    assert "run_documented_cylinder-U-1729" in names
    assert "run_documented_any-N-3141" in names
    assert "analysis_documented_probes" in names
    assert all(c.passed for c in rep.checks)


def test_X18_gate_gg_fails_for_undocumented_run(cfg):
    store = memory_store()
    _fill_store(cfg, store, skip_run=["any", "N", 2718])
    rep = store.load(GateReport, gate_gg(cfg, store), consumer=CONS)
    assert rep.verdict == "fail"
    failing = [c.name for c in rep.checks if not c.passed]
    assert failing == ["run_documented_any-N-2718"]


def test_X18_gate_gg_failed_run_record_counts_as_documented(cfg):
    store = memory_store()
    _fill_store(cfg, store, failed_run=["square", "U", 1729])
    rep = store.load(GateReport, gate_gg(cfg, store), consumer=CONS)
    assert rep.verdict == "pass"


def test_X18_gate_gg_fails_for_missing_job_record(cfg):
    store = memory_store()
    _fill_store(cfg, store, jobs=("dev_extract", "controls", "probes", "circular"))
    rep = store.load(GateReport, gate_gg(cfg, store), consumer=CONS)
    assert rep.verdict == "fail"
    assert [c.name for c in rep.checks if not c.passed] == ["analysis_documented_sensitivity"]


# ----------------------------------------------------------------------------------- X19
def test_X19_failed_run_is_recorded_not_raised(cfg, monkeypatch):
    store = memory_store()

    def boom(self, job):
        raise StageFailure(ErrorCode.NONFINITE_LOSS, "experiment.test", "loss", "planted")

    monkeypatch.setattr(S7Runs, "_train", boom)
    job = {"world": "cylinder", "condition": "U", "seed": 1729}
    ids = S7Runs(cfg, store).execute(job)
    assert len(ids) == 1
    meta = store.meta(ids[0])
    assert meta.config["stage"] == "S7" and meta.config["kind"] == "run"
    assert meta.config["outcome"] == "failed"
    assert meta.config["run_key"] == ["cylinder", "U", 1729]
    rec = store.load(MetricRecords, ids[0], consumer=CONS)
    assert len(rec.rows) == 1
    row = rec.rows[0]
    assert row.metric_id == "run_available" and row.status == "not_run"
    assert row.value is None
    assert ErrorCode.NONFINITE_LOSS.value in row.uncertainty_kind
    assert (row.world, row.condition, row.replicate) == ("cylinder", "U", 1729)


def test_X19_non_stagefailure_exception_uses_type_name(cfg, monkeypatch):
    store = memory_store()

    def boom(self, job):
        raise ValueError("x")

    monkeypatch.setattr(S7Runs, "_train", boom)
    ids = S7Runs(cfg, store).execute({"world": "any", "condition": "N", "seed": 2718})
    row = store.load(MetricRecords, ids[0], consumer=CONS).rows[0]
    assert row.status == "not_run" and row.uncertainty_kind == "ValueError"


# ----------------------------------------------------------------------------------- X20
def _row(metric, value, panel, **kw):
    return MetricRow(run_id="r", space="privileged_eval:circular", metric_id=metric,
                     value=value, status="ok" if value is not None else "inconclusive",
                     panel=panel, **kw)


def test_X20_circular_summary_known_answer():
    # panel: (agreement_x, null_q95, control, oracle)
    spec = {1: (0.9, 0.5, 0.1, 0.95), 2: (0.3, 0.4, 0.2, 0.85), 3: (None, None, None, 0.75)}
    rows = []
    for p, (a, q, c, o) in spec.items():
        rows += [_row("agreement_x", a, p), _row("agreement_x_null_q95", q, p),
                 _row("agreement_control", c, p), _row("agreement_oracle_x", o, p)]
    out = CircularJob.summary(rows, {"world": "cylinder", "condition": "O", "replicate": 1729,
                                     "checkpoint": 5000})
    got = {r.metric_id: r.value for r in out}
    assert got["agreement_x_median"] == pytest.approx(0.6)       # median(0.9, 0.3)
    assert got["n_panels_above_null_q95"] == 1.0                 # panel 1 only
    assert got["n_panels_with_h1_class"] == 2.0                  # panel 3 undefined
    assert got["agreement_control_median"] == pytest.approx(0.15)
    assert got["agreement_oracle_x_median"] == pytest.approx(0.85)
    assert all(r.checkpoint == 5000 and r.world == "cylinder" for r in out)


def _planted(rng, W, noise, n_per=16, d=6):
    n = 8 * n_per
    X = rng.normal(size=(n, d))
    Y = X @ W + noise * rng.normal(size=(n, W.shape[1]))
    panel = np.repeat(np.arange(1, 9), n_per)
    pd = ProbeData(ids=[f"h{i}" for i in range(n)], panel=panel, b32=Y, b1=Y,
                   q=np.zeros((n, 2)), w32=np.zeros(n, dtype=int))
    return X, Y, pd


def _job():
    job = ProbesJob.__new__(ProbesJob)
    job.lambdas = [0.0, 0.01, 1.0, 100.0]
    job.fit_panels = [1, 2, 3, 4, 5]
    job.val_panels = [6, 7]
    return job


def test_X20_probe_recovers_planted_map_and_lambda_uses_val_rows_only(monkeypatch):
    rng = np.random.default_rng(7)
    W = rng.normal(size=(6, 3))
    Xd, Yd, dev = _planted(rng, W, 0.01)
    Xt, Yt, test = _planted(rng, W, 0.01)

    calls = []
    orig = s7_probes.RidgeProbe.fit

    def spy(self, X_fit, Y_fit, X_val, Y_val, *a, **k):
        calls.append((np.array(X_fit), np.array(Y_fit), np.array(X_val), np.array(Y_val)))
        return orig(self, X_fit, Y_fit, X_val, Y_val, *a, **k)

    monkeypatch.setattr(s7_probes.RidgeProbe, "fit", spy)
    _, pooled, per_panel = _job().probe(Xd, Yd, Xt, Yt, dev, test)
    assert pooled["r2"] > 0.99
    assert len(per_panel) == 8 and min(per_panel) > 0.99
    assert len(calls) == 1
    Xf, Yf, Xv, Yv = calls[0]
    fit_rows = np.isin(dev.panel, [1, 2, 3, 4, 5])
    val_rows = np.isin(dev.panel, [6, 7])
    np.testing.assert_array_equal(Xv, Xd[val_rows])
    np.testing.assert_array_equal(Yv, Yd[val_rows])
    np.testing.assert_array_equal(Xf, Xd[fit_rows])
    np.testing.assert_array_equal(Yf, Yd[fit_rows])
    # no panel-8 rows (neither fit nor val panel) in what the fit saw
    p8 = Xd[dev.panel == 8]
    for blk in (Xf, Xv):
        assert not any((blk == r).all(axis=1).any() for r in p8)


def test_X20_probe_shuffled_labels_give_low_r2():
    rng = np.random.default_rng(11)
    W = rng.normal(size=(6, 3))
    Xd, Yd, dev = _planted(rng, W, 0.01)
    Xt, Yt, test = _planted(rng, W, 0.01)
    _, pooled, _ = _job().probe(Xd, Yd, Xt, Yt, dev, test,
                                shuffle_rng=np.random.default_rng(3))
    assert pooled["r2"] < 0.1


# ----------------------------------------------------------------------------------- X21
def _obs(store, split, seed):
    o = tiny_observations(R=4, seed=seed)
    o = ObservationSet(split=split, V=o.V, sequence_id=o.sequence_id, tokens=o.tokens)
    return store.save(o, config={"split": split, "seed": seed}, parents=[], seed_map={},
                      consumer=CONS)


def _acts(store, obs_id):
    a = ActivationSet(hooks=("resid_post_3",), source="baseline:R2",
                      history_id=np.array(["a", "b"]),
                      A=np.zeros((2, 1, 3), dtype=np.float32))
    return store.save(a, config={"parent": obs_id}, parents=[obs_id], seed_map={},
                      consumer=CONS)


def test_X21_on_test_split_distinguishes_dev_and_test():
    store = memory_store()
    dev_obs, test_obs = _obs(store, "dev", 1), _obs(store, "test", 2)
    dev_act, test_act = _acts(store, dev_obs), _acts(store, test_obs)
    assert on_test_split(store, test_act) is True
    assert on_test_split(store, dev_act) is False
