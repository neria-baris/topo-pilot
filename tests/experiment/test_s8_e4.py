"""Stage S8 and the E4 report (TEST_PLAN X22-X25): stub memory stores, hand-computed values."""
import pytest

from topo_pilot.contracts import (
    ErrorCode,
    GateCheck,
    GateReport,
    MetricRecords,
    MetricRow,
    StageFailure,
)
from topo_pilot.contracts.testing import memory_store
from topo_pilot.experiment import STAGE_REGISTRY
from topo_pilot.experiment.report_e4 import build_e4
from topo_pilot.experiment.report_e4_s7 import (
    CIRC,
    circular_table,
    control_runs,
    control_table,
    probe_table,
    sensitivity_table,
)
from topo_pilot.experiment.s8 import TIMING_METRICS, RerunJob, compare_stores, integrity

pytestmark = pytest.mark.experiment

CONS = "experiment"


def _r(metric, value, space="x", **kw):
    return MetricRow(run_id="t", space=space, metric_id=metric, value=value, **kw)


def _rec(store, rows, parents=(), **config):
    return store.save(MetricRecords(rows=tuple(rows)), config=config, parents=list(parents),
                      seed_map={}, consumer=CONS)


def _gate(store, stage, gate_id, verdict="pass", value=1.0):
    checks = (GateCheck("c", verdict == "pass", value, 0.5),)
    return store.save(GateReport(stage=stage, gate_id=gate_id, verdict=verdict, checks=checks),
                      config={"stage": stage, "gate": gate_id}, parents=[], seed_map={},
                      consumer=CONS)


def _row_value(rows, space, metric):
    return next(r.value for r in rows if r.space == space and r.metric_id == metric)


def _mismatch_text(rows):
    return next(r.uncertainty_kind or "" for r in rows if r.metric_id == "mismatches")


def _pair():
    return memory_store(), memory_store()


# ---- X22 ---------------------------------------------------------------------------------

def test_X22_identical_stores_ok_and_every_type_counted():
    main, rerun = _pair()
    for s in (main, rerun):
        _rec(s, [_r("a", 1.0)], stage="S1", kind="k1")
        _rec(s, [_r("a", 2.0)], stage="S1", kind="k2")
        _gate(s, "S1", "G-A")
    rows, ok = compare_stores(main, rerun)
    assert ok
    assert _row_value(rows, "rerun:MetricRecords", "n") == 2
    assert _row_value(rows, "rerun:MetricRecords", "id_found") == 2
    assert _row_value(rows, "rerun:MetricRecords", "checksum_equal") == 2
    assert _row_value(rows, "rerun:GateReport", "n") == 1
    assert _row_value(rows, "rerun:GateReport", "verdict_match") == 1
    assert _row_value(rows, "rerun", "mismatches") == 0


def test_X22_same_id_different_payload_is_checksum_mismatch():
    main, rerun = _pair()
    _rec(main, [_r("a", 1.0)], stage="S1", kind="k")
    _rec(rerun, [_r("a", 1.5)], stage="S1", kind="k")
    rows, ok = compare_stores(main, rerun)
    assert not ok
    assert _row_value(rows, "rerun", "mismatches") == 1
    assert _row_value(rows, "rerun:MetricRecords", "checksum_equal") == 0
    assert "checksum" in _mismatch_text(rows)


def test_X22_artifact_absent_from_main_is_missing():
    main, rerun = _pair()
    _rec(main, [_r("a", 1.0)], stage="S1", kind="k")
    _rec(rerun, [_r("a", 1.0)], stage="S1", kind="k")
    _rec(rerun, [_r("b", 2.0)], stage="S1", kind="only_in_rerun")
    rows, ok = compare_stores(main, rerun)
    assert not ok
    assert _row_value(rows, "rerun", "mismatches") == 1
    assert "missing" in _mismatch_text(rows)
    assert _row_value(rows, "rerun:MetricRecords", "n") == 2
    assert _row_value(rows, "rerun:MetricRecords", "id_found") == 1


def test_X22_run_timing_differs_only_in_timing_rows_is_equal():
    assert set(TIMING_METRICS) >= {"wall_time_s", "tokens_per_second"}
    main, rerun = _pair()

    def rows(wall, tps):
        return [_r("regret", 0.25), _r("captured", 0.5), _r("wall_time_s", wall),
                _r("tokens_per_second", tps)]
    cfg = {"kind": "run_timing", "run_key": ["cylinder", "O", 1729]}
    _rec(main, rows(10.0, 100.0), **cfg)
    _rec(rerun, rows(12.5, 80.0), **cfg)
    out, ok = compare_stores(main, rerun)
    assert ok
    assert _row_value(out, "rerun:MetricRecords", "checksum_equal") == 1


def test_X22_run_timing_with_other_row_differing_is_mismatch():
    main, rerun = _pair()
    cfg = {"kind": "run_timing", "run_key": ["cylinder", "O", 1729]}
    _rec(main, [_r("regret", 0.25), _r("wall_time_s", 10.0)], **cfg)
    _rec(rerun, [_r("regret", 0.26), _r("wall_time_s", 10.0)], **cfg)
    rows, ok = compare_stores(main, rerun)
    assert not ok
    assert "checksum" in _mismatch_text(rows)


def test_X22_untimed_kind_differing_in_wall_time_is_mismatch():
    main, rerun = _pair()
    _rec(main, [_r("wall_time_s", 10.0)], stage="S4", kind="run")
    _rec(rerun, [_r("wall_time_s", 11.0)], stage="S4", kind="run")
    assert not compare_stores(main, rerun)[1]


def test_X22_gate_reports_compared_by_gate_and_verdict_only():
    main, rerun = _pair()
    _gate(main, "S1", "G-A", "pass", value=1.0)
    _gate(rerun, "S1", "G-A", "pass", value=0.7)  # different payload, same (gate, verdict)
    rows, ok = compare_stores(main, rerun)
    assert ok
    assert _row_value(rows, "rerun:GateReport", "verdict_match") == 1
    m2, r2 = _pair()
    _gate(m2, "S1", "G-A", "pass")
    _gate(r2, "S1", "G-A", "fail")
    rows, ok = compare_stores(m2, r2)
    assert not ok
    assert _row_value(rows, "rerun:GateReport", "verdict_match") == 0


# ---- X23 ---------------------------------------------------------------------------------

def test_X23_intact_store_ok_with_n_equal_n_verified():
    store = memory_store()
    parent = _rec(store, [_r("a", 1.0)], stage="S1", kind="p")
    _rec(store, [_r("b", 2.0)], parents=[parent], stage="S2", kind="c")
    _gate(store, "S2", "G-B")
    rows, ok = integrity(store)
    assert ok
    assert _row_value(rows, "integrity", "n_artifacts") == 3
    assert _row_value(rows, "integrity", "n_verified") == 3
    assert _row_value(rows, "integrity", "n_problems") == 0


def test_X23_missing_parent_is_reported():
    store = memory_store()
    parent = _rec(store, [_r("a", 1.0)], stage="S1", kind="p")
    child = _rec(store, [_r("b", 2.0)], parents=[parent], stage="S2", kind="c")
    # The store refuses to save a child whose parent is absent (MISSING_PARENT), so the
    # condition is built afterwards: delete every backend key of the parent
    # ("MetricRecords/<parent id>/...") from the in-memory dictionary.
    backend = store.backend
    for key in backend.list(f"MetricRecords/{parent}/"):
        del backend._data[key]
    assert backend.list(f"MetricRecords/{child}/")
    rows, ok = integrity(store)
    assert not ok
    assert _row_value(rows, "integrity", "n_problems") >= 1
    problems = next(r.uncertainty_kind for r in rows if r.metric_id == "n_problems")
    assert f"{child}:missing_parent" in problems


# ---- X24 ---------------------------------------------------------------------------------

def test_X24_s8_registered_with_requires_and_gate():
    stage = STAGE_REGISTRY["S8"]
    assert tuple(stage.requires) == ("S7",)
    assert tuple(stage.gates) == ("G-H",)


class _Cfg:
    repo_root = None

    def __init__(self, s3_runs, identity):
        self._s = {"S3": {"runs": s3_runs},
                   "S8": {"rerun_stages": ["S0", "S1", "S2", "S3"],
                          "rerun_identity_check": identity}}

    def stage(self, sid):
        return self._s[sid]


def test_X24_rerun_job_rejects_s3_runs_differing_from_identity_check():
    registered = {"world": "cylinder", "condition": "O", "seed": 1729}
    other = {"world": "square", "condition": "O", "seed": 1729}
    for runs in ([other], [registered, other], []):
        job = RerunJob(_Cfg(runs, registered), memory_store())
        with pytest.raises(StageFailure) as exc:
            job.run_job()
        assert exc.value.code == ErrorCode.INVALID_CONFIG


# ---- X25 ---------------------------------------------------------------------------------

def test_X25_empty_store_prints_not_run_and_invents_nothing(tmp_path):
    out_dir = tmp_path / "E4"
    path = build_e4(memory_store(), out_dir)
    assert path == out_dir / "summary.md"
    text = path.read_text(encoding="utf-8")
    assert "Gate G-G: not run" in text
    assert "Gate G-H: not run" in text
    assert "S8 rerun: not run" in text
    assert "X4-causal" in text and "X5, X6" in text and "X1–X3" in text
    assert "**Not run:**" in text
    assert "nan" not in text.lower()
    assert "| any-N-1729 (S4)" not in text
    assert not (out_dir / "fig_probes.png").exists()
    assert not (out_dir / "fig_circular.png").exists()
    for line in text.splitlines():
        if line.startswith("| activations") or line.startswith("| exact next-symbol") \
                or line.startswith("| one-hot last symbol"):
            assert line.count("not run") == 2


def test_X25_probe_table_hand_computed():
    rows = [_r("r2_test", v, space="probe:A5000->b32", condition="O")
            for v in (0.2, 0.9, 0.4)]
    rows += [_r("lambda", 0.1, space="probe:A5000->b32", condition="O")]
    lines = probe_table(rows)
    main = next(ln for ln in lines if ln.startswith("| activations, step 5000 → b³² (main)"))
    cells = [c.strip() for c in main.strip("|").split("|")]
    assert cells[1] == "0.400 (0.200–0.900)"
    assert cells[2] == "not run"
    other = next(ln for ln in lines if "step 0 →" in ln)
    assert other.count("not run") == 2


def test_X25_circular_table_hand_computed():
    rows = []
    for rep, agree, above, h1 in ((1, 0.5, 3, 8), (2, 0.7, 4, 6)):
        kw = dict(space=CIRC, condition="O", world="cylinder", checkpoint=5000, replicate=rep)
        rows += [_r("agreement_x_median", agree, **kw),
                 _r("n_panels_above_null_q95", above, **kw),
                 _r("n_panels_with_h1_class", h1, **kw),
                 _r("agreement_control_median", 0.1, **kw),
                 _r("agreement_oracle_x_median", 0.9, **kw)]
    body = circular_table(rows, 5000)[2:]
    assert len(body) == 1  # only the (O, cylinder, 5000) combination has data
    cells = [c.strip() for c in body[0].strip("|").split("|")]
    assert cells[:3] == ["O", "cylinder", "5000"]
    assert cells[3] == "0.600 (0.500, 0.700)"   # median of 0.5, 0.7
    assert cells[4] == "7/16"                    # 3 + 4 over 2 runs x 8 panels
    assert cells[5] == "14/16"                   # 8 + 6
    assert cells[6] == "0.100" and cells[7] == "0.900"


def test_X25_sensitivity_table_hand_computed():
    primary = {"O": ("f1-O", "h3p-O", "0.50"), "P": ("f1-P", "h3p-P", "0.40")}
    sp = "sens:chord"
    rows = [_r("F1rule_verdict_SUPPORTED", 1.0, space=sp, condition="O"),
            _r("median_D", 0.02, space=sp, condition="O", replicate=1),
            _r("u", 0.01, space=sp, condition="O", replicate=1),
            _r("H3prime_verdict_REJECTED", 0.0, space=sp, condition="O"),
            _r("delta_geom_all_fraction_positive", 0.75, space=sp, condition="O")]
    lines = sensitivity_table(rows, primary)
    assert "| primary (S4/S5, X4) | O | f1-O | h3p-O | 0.50 |" in lines
    assert "| primary (S4/S5, X4) | P | f1-P | h3p-P | 0.40 |" in lines
    assert "| chord | O | SUPPORTED (0.020/0.010) | REJECTED | 0.75 |" in lines
    p_line = next(ln for ln in lines if ln.startswith("| chord | P |"))
    assert p_line.endswith("| not run | not run |")


def test_X25_failed_control_run_prints_failed_reason():
    store = memory_store()
    _rec(store, [_r("run_available", None, status="not_run", uncertainty_kind="boom: OOM")],
         stage="S7", kind="run", run_key=["cylinder", "N", 2718])
    _rec(store, [_r("run_available", 1.0), _r("V", 144.0), _r("regret", 0.1234)],
         stage="S7", kind="run", run_key=["cylinder", "U", 1729])
    lines = control_table(control_runs(store), [])
    failed = next(ln for ln in lines if ln.startswith("| cylinder-N-2718"))
    assert "failed: boom: OOM" in failed
    ok_line = next(ln for ln in lines if ln.startswith("| cylinder-U-1729"))
    assert "failed" not in ok_line and "144" in ok_line and "0.1234" in ok_line
