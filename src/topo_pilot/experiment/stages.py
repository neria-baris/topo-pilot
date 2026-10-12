"""Stage registry and the W0 stage S0 (environment and contract sanity).

W0 skeleton: stages run inline in this process via :func:`run_stage`. In W4 the runner plans
``JobSpec``s and executes them through an ``Executor`` (see SPEC.md).
"""

from __future__ import annotations

import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, ClassVar

from topo_pilot.contracts import ArtifactStore, ErrorCode, GateCheck, GateReport, StageFailure

from .config import ResolvedConfig


class Stage(ABC):
    """A run stage. ``plan`` lists job descriptors; ``execute`` runs one and returns artifact ids."""

    stage_id: ClassVar[str]
    requires: ClassVar[tuple[str, ...]] = ()
    gates: ClassVar[tuple[str, ...]] = ()

    @abstractmethod
    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        """Job descriptors for this stage, in priority order."""

    @abstractmethod
    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        """Run one job; return the ids of the artifacts it wrote."""


STAGE_REGISTRY: dict[str, type[Stage]] = {}


def register_stage(cls: type[Stage]) -> type[Stage]:
    """Class decorator adding a stage to :data:`STAGE_REGISTRY` under its ``stage_id``."""
    STAGE_REGISTRY[cls.stage_id] = cls
    return cls


def _run(cmd: list[str], cfg: ResolvedConfig) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=cfg.repo_root, capture_output=True, text=True, timeout=600)
    lines = (proc.stdout + proc.stderr).strip().splitlines()
    return proc.returncode == 0, lines[-1] if lines else ""


@register_stage
class S0Stage(Stage):
    """S0: the store is initialised, the environment lock exists, the contracts suite passes,
    and ``tools/check_imports.py`` is clean. Writes ``GateReport(stage="S0", gate_id="G-S0")``."""

    stage_id = "S0"

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "S0", "job": "sanity"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        lock = cfg.repo_root / "requirements.lock"
        tests_ok, tests_line = _run([sys.executable, "-m", "pytest", "tests/contracts", "-q"], cfg)
        imports_ok, imports_line = _run([sys.executable, "tools/check_imports.py"], cfg)
        checks = (
            GateCheck("env_lock_present", lock.is_file(), lock.name, "exists"),
            GateCheck("contracts_tests", tests_ok, tests_line, "all pass"),
            GateCheck("check_imports", imports_ok, imports_line, "clean"),
        )
        verdict = "pass" if all(c.passed for c in checks) else "fail"
        report = GateReport(stage="S0", gate_id="G-S0", verdict=verdict, checks=checks)
        rid = store.save(report, config={"stage": "S0", "gate": "G-S0",
                                         "config_hash": cfg.config_hash,
                                         "producer": store.producer_version},
                         parents=[], seed_map={}, consumer="experiment")
        return [rid]


def run_stage(stage_id: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[str]:
    """Run every planned job of ``stage_id`` inline; raises ``INVALID_CONFIG`` for an unknown
    stage and ``GATE_FAILED`` when a written GateReport has verdict ``fail``."""
    if stage_id not in STAGE_REGISTRY:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.run_stage", "stage_id",
                           f"stage {stage_id!r} is not implemented yet "
                           f"(available: {sorted(STAGE_REGISTRY)})")
    stage = STAGE_REGISTRY[stage_id]()
    for required in stage.requires:
        verdicts = [store.load(GateReport, gid, consumer="experiment").verdict
                    for gid in store.find(GateReport, stage=required)]
        if not any(v in ("pass", "waived") for v in verdicts):
            raise StageFailure(ErrorCode.GATE_FAILED, f"experiment.{stage_id}", "requires",
                               f"required stage {required} has no passed gate")
    written: list[str] = []
    for job in stage.plan(cfg, store):
        written.extend(stage.execute(job, cfg, store))
    for aid in written:
        meta = store.meta(aid)
        if meta.artifact_type == "GateReport":
            report = store.load(GateReport, aid, consumer="experiment")
            if report.verdict == "fail":
                failed = [c.name for c in report.checks if not c.passed]
                raise StageFailure(ErrorCode.GATE_FAILED, f"experiment.{stage_id}",
                                   report.gate_id, f"failed checks: {failed}", aid)
    return written
