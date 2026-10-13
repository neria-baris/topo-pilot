"""X4 report section (TEST_PLAN X13): verbatim prereg lines, "not run" when missing."""
import pytest

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow
from topo_pilot.experiment.report_x4 import x4_section

pytestmark = pytest.mark.experiment

PREREG = """# Prereg
Blinding: blind to everyone (test sentence).
X4-c (where the structure lives): two-sided.
  V3 supported, V4 not → visible sentence;
  V4 supported, V3 not → null sentence;
  both / neither → reported as such.

## Addendum: caveats

1. Caveat one.
"""


@pytest.fixture
def store(tmp_path):
    return ArtifactStore(LocalFSBackend(tmp_path / "artifacts"), producer_version="test")


def _save(store, rows):
    store.save(MetricRecords(rows=tuple(rows)), config={"stage": "X4", "kind": "analysis"},
               parents=[], seed_map={}, consumer="experiment")


def test_X13_missing_record_says_not_run(store, tmp_path):
    (tmp_path / "p.md").write_text(PREREG, encoding="utf-8")
    lines = x4_section(store, tmp_path / "p.md")
    assert "X4: not run" in lines
    assert "Blinding: blind to everyone (test sentence)." in lines


@pytest.mark.parametrize("cat, expected", [("V4_only", "V4 supported, V3 not → null sentence;"),
                                           ("neither", "both / neither → reported as such.")])
def test_X13_quotes_prereg_interpretation_and_addendum(store, tmp_path, cat, expected):
    (tmp_path / "p.md").write_text(PREREG, encoding="utf-8")
    _save(store, [MetricRow(run_id="X4", space="x4:c", metric_id=f"X4c_{cat}", value=1.0,
                            condition="O")])
    text = "\n".join(x4_section(store, tmp_path / "p.md"))
    assert f"Category: {cat}. Pre-registered interpretation: {expected}" in text
    assert "1. Caveat one." in text
    assert "SECONDARY" in text
