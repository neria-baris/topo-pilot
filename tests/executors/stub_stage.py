"""Stub stage for the executors tests, imported in subprocesses via ``import_modules``.

Job config keys: ``value`` (float written), ``input_id`` (optional MetricRecords input, whose
value is added), ``fail`` (raise a StageFailure), ``emit`` (``"metrics"`` or ``"gate"``).
"""

from collections.abc import Mapping
from typing import Any

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    GateCheck,
    GateReport,
    MetricRecords,
    MetricRow,
    StageFailure,
)
from topo_pilot.experiment import ResolvedConfig, Stage, register_stage


@register_stage
class StubStage(Stage):
    """Writes one tiny artifact so executors can be tested without science code."""

    stage_id = "STUB"

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "STUB"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        if job.get("fail"):
            raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "stub", "forced", "forced failure")
        value = float(job.get("value", 1.0))
        parents = []
        if job.get("input_id"):
            parents = [job["input_id"]]
            value += store.load(MetricRecords, job["input_id"], consumer="experiment").rows[0].value
        if job.get("emit") == "gate":
            art = GateReport(stage="STUB", gate_id="G-STUB", verdict="pass",
                             checks=(GateCheck("c", True, value, "any"),))
        else:
            art = MetricRecords(rows=(MetricRow("r", "world", "stub_value", value),))
        return [store.save(art, config={"stage": "STUB", "value": value}, parents=parents,
                           seed_map={}, consumer="experiment")]
