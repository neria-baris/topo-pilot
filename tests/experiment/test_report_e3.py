"""E3 report (X14–X16): records only, fixed status readings, P wording, S6 plan."""
import pytest

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow
from topo_pilot.experiment.report_e3 import H3_READING, build_e3, h4_table
from topo_pilot.experiment.report_x4 import P_X4B_NOTE, x4_section
from topo_pilot.experiment.s6 import S6Stage

pytestmark = pytest.mark.experiment

PREREG = """| H3 | Under P the rule holds (test row) |
| H4 | S rises after history use (test row) |
**Which hypotheses are decidable (conductor note):** one-sided (test sentence).
H3′ (test line): rule text.
X4-b (test line): expectation.
"""
DECISIONS = "2026-10-13 | D-034 | H4 rule (test line) | reason | ref\n"


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "PREREGISTRATION.md").write_text(PREREG, encoding="utf-8")
    (tmp_path / "PREREGISTRATION_X4.md").write_text(PREREG, encoding="utf-8")
    (tmp_path / "state").mkdir()
    (tmp_path / "state" / "DECISIONS.md").write_text(DECISIONS, encoding="utf-8")
    return tmp_path


@pytest.fixture
def store(tmp_path):
    return ArtifactStore(LocalFSBackend(tmp_path / "artifacts"), producer_version="test")


def _r(space, metric, value, **kw):
    return MetricRow(run_id="analysis", space=space, metric_id=metric, value=value, **kw)


def _save(store, rows, **config):
    store.save(MetricRecords(rows=tuple(rows)), config=config, parents=[], seed_map={},
               consumer="experiment")


def _dyn_rows(cond="O", seed=1729):
    rows = []
    for world in ("cylinder", "square"):
        kw = {"world": world, "condition": cond, "replicate": seed}
        rows += [_r("dyn:S", "S_H1", 0.1 + 0.01 * i, checkpoint=t, panel=1, **kw)
                 for i, t in enumerate((0, 50, 100))]
        rows += [_r("dyn:regret", "regret", 1.0 / (i + 1), checkpoint=t, panel=1, **kw)
                 for i, t in enumerate((0, 50, 100))]
        rows += [_r("dyn", "G_C", 0.26, **kw), _r("dyn", "u_r", 0.01, **kw),
                 _r("dyn", "t_history", 50.0, **kw), _r("dyn", "t_rise", 100.0, **kw),
                 _r("dyn", "h4_consistent", 1.0, uncertainty_kind="consistent", **kw),
                 _r("dyn", "order_null_first_third_share", 0.3, **kw),
                 _r("dyn", "order_null_p", 0.5, **kw)]
    rows.append(_r("H4", f"H4_verdict_{'SUPPORTED'}", 1.0, condition=cond))
    return rows


def test_X14_empty_store_says_not_run(store, repo, tmp_path):
    out = build_e3(store, tmp_path / "E3", repo)
    text = out.read_text(encoding="utf-8")
    assert "**F1 rule under P: not run**" in text
    assert "**H4 under O: not run**" in text
    assert H3_READING["not run"] in text
    assert "| H3 | Under P the rule holds (test row) |" in text
    assert "2026-10-13 | D-034 | H4 rule (test line) | reason | ref" in text
    assert (tmp_path / "E3" / "condition_P.md").is_file()


def test_X14_rejected_h3_is_read_one_sided(store, repo, tmp_path):
    _save(store, [_r("F1", "F1_verdict_REJECTED", 0.0, condition="P")],
          stage="S5", kind="analysis")
    text = build_e3(store, tmp_path / "E3", repo).read_text(encoding="utf-8")
    assert "**F1 rule under P: REJECTED**" in text
    assert "is NOT read as evidence that the structure comes from emission geometry" in text


def test_X15_dynamics_table_and_figures(store, repo, tmp_path):
    rows = _dyn_rows()
    _save(store, rows, stage="S6", kind="dynamics", condition="O")
    text = build_e3(store, tmp_path / "E3", repo).read_text(encoding="utf-8")
    assert "**H4 under O: SUPPORTED**" in text
    assert (tmp_path / "E3" / "fig_dynamics.png").is_file()
    table = h4_table(rows, [])
    assert table[2] == ("| cylinder-1729 | 0.2600 | 0.0100 | 50 | 100 | consistent | not run "
                        "| not run | 0.300 | 0.500 |")


def test_X16_x4_section_p_wording(store, tmp_path):
    (tmp_path / "p.md").write_text(PREREG, encoding="utf-8")
    _save(store, [_r("x4:c", "X4c_both", 1.0, condition="P")], stage="X4", kind="analysis")
    p_text = "\n".join(x4_section(store, tmp_path / "p.md", "P"))
    o_text = "\n".join(x4_section(store, tmp_path / "p.md", "O"))
    assert P_X4B_NOTE in p_text and P_X4B_NOTE not in o_text
    assert "Condition P: decision rule (approved at H3, D-037" in p_text
    assert "Condition O: comparison only (descriptive)" in o_text


class _Cfg:
    def __init__(self, s6):
        self.s6 = s6

    def stage(self, stage_id):
        return self.s6


def test_X16_s6_plan_includes_x4curves_and_p_after_s5(store):
    plan = S6Stage().plan(_Cfg({"layer_sweep": True, "x4_curves": ["V1", "V5"]}), store)
    assert [(j["condition"], j["job"]) for j in plan] == [
        ("O", "dynamics"), ("O", "layers"), ("O", "x4curves")]
    _save(store, [_r("F1", "u", 0.1, condition="P", replicate=1729)],
          stage="S5", kind="analysis")
    plan = S6Stage().plan(_Cfg({}), store)
    assert [(j["condition"], j["job"]) for j in plan] == [("O", "dynamics"), ("P", "dynamics")]
