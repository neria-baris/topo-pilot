"""E2 report: built from MetricRecords/GateReport only; missing data prints "not run"."""
import pytest

from topo_pilot.contracts import (
    ArtifactStore,
    GateCheck,
    GateReport,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
)
from topo_pilot.experiment.report_e2 import build_e2, f1_table, verdict

pytestmark = pytest.mark.experiment


@pytest.fixture
def store(tmp_path):
    return ArtifactStore(LocalFSBackend(tmp_path / "artifacts"), producer_version="test")


def _r(space, metric, value, **kw):
    return MetricRow(run_id="analysis", space=space, metric_id=metric, value=value, **kw)


def _analysis_rows(seed=1729):
    rows = []
    for world, init, final in (("cylinder", 0.2, 0.5), ("square", 0.2, 0.25)):
        for p in range(1, 9):
            for ck, s in ((0, init), (5000, final)):
                rows.append(_r("act:resid_post_last", "S_H1", s + 0.002 * p, world=world,
                               condition="O", replicate=seed, panel=p, checkpoint=ck))
    rows += [_r("F1", "D", 0.25 if p < 8 else -0.01, condition="O", replicate=seed, panel=p)
             for p in range(1, 9)]
    rows += [_r("F1", "u", 0.05, condition="O", replicate=seed),
             _r("F1", "median_D", 0.25, condition="O", replicate=seed),
             _r("F1:base:R2", "median_D", 0.02, condition="O", replicate=seed),
             _r("geometry", "delta_geom_same_last_symbol", None, world="cylinder",
                condition="O", replicate=seed, panel=1, status="inconclusive"),
             _r("F1", "F1_verdict_INCONCLUSIVE", None, condition="O", status="inconclusive",
                uncertainty_kind="replicates: 1 < 3")]
    return rows


def test_f1_table_reports_four_medians_and_positive_count():
    lines = f1_table(_analysis_rows(), 5000)
    assert lines[2].startswith("| 1729 | 0.209 | 0.509 | 0.209 | 0.259 | 7/8 | 0.2500")
    assert lines[2].endswith("| yes |")


def test_verdict_reads_status_and_reasons():
    assert verdict(_analysis_rows()) == ("INCONCLUSIVE", "replicates: 1 < 3")
    assert verdict([]) == ("not run", "")


def test_build_e2_from_records_only(store, tmp_path):
    mid = store.save(MetricRecords(rows=tuple(_analysis_rows())),
                     config={"stage": "S4", "kind": "analysis", "condition": "O"}, parents=[],
                     seed_map={}, consumer="experiment")
    store.save(GateReport(stage="S4", gate_id="G-F", verdict="pass",
                          checks=(GateCheck("learning_gate_replicate_0", True, True, True),)),
               config={"stage": "S4", "gate": "G-F"}, parents=[mid], seed_map={},
               consumer="experiment")
    out = build_e2(store, tmp_path / "E2")
    text = out.read_text(encoding="utf-8")
    assert "**F1 verdict: INCONCLUSIVE** (replicates: 1 < 3)" in text
    assert "Gate G-F: **pass**" in text
    assert "not run" in text  # H0 rows are absent
    assert (tmp_path / "E2" / "fig_f1_contrasts.png").stat().st_size > 0


def test_build_e2_without_analysis_says_not_run(store, tmp_path):
    text = build_e2(store, tmp_path / "E2").read_text(encoding="utf-8")
    assert "**F1 verdict: not run**" in text
