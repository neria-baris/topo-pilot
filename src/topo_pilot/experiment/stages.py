"""Stage registry and the W0 stage S0 (environment and contract sanity).

W0 skeleton: stages run inline in this process via :func:`run_stage`. In W4 the runner plans
``JobSpec``s and executes them through an ``Executor`` (see SPEC.md).
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, ClassVar

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    GateCheck,
    GateReport,
    StageFailure,
    canonical_json,
)

from .config import ResolvedConfig

_PYTEST_TIMING = re.compile(r"\s+in\s+[\d.]+s(\s+\([\d:]+\))?")


class Stage(ABC):
    """A run stage: ``plan`` lists job descriptors; ``execute`` runs one, returns artifact ids.

    ``gates`` lists every gate the stage writes; a later stage that ``requires`` this one runs
    only if the latest report of each of these gates is ``pass`` or ``waived``.
    """

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


def tool_line(output: str) -> str:
    """Last output line of a tool run, with pytest's wall time removed (``95 passed in 3.7s``
    becomes ``95 passed``) so that gate contents do not change between identical runs."""
    lines = output.strip().splitlines()
    return _PYTEST_TIMING.sub("", lines[-1]).strip("= ") if lines else ""


def run_tool(cmd: list[str], cfg: ResolvedConfig, timeout: int = 600) -> tuple[bool, str]:
    """Run ``cmd`` in the repository; returns (exit code 0, :func:`tool_line`)."""
    proc = subprocess.run(cmd, cwd=cfg.repo_root, capture_output=True, text=True,
                          timeout=timeout)
    return proc.returncode == 0, tool_line(proc.stdout + proc.stderr)


def save_tool_gate(store: ArtifactStore, cfg: ResolvedConfig, stage: str, gate_id: str,
                   checks: Sequence[GateCheck], parents: Sequence[str]) -> str:
    """Save a GateReport whose checks embed tool output (test counts, file counts).

    The config holds the producer version and a digest of the checks, so a re-evaluation with
    different tool output gets a new id instead of ``CHECKSUM_MISMATCH``; identical
    re-evaluations keep the same id.
    """
    checks = tuple(checks)
    verdict = "pass" if checks and all(c.passed for c in checks) else "fail"
    digest = hashlib.sha256(canonical_json(checks).encode("utf-8")).hexdigest()[:16]
    return store.save(GateReport(stage=stage, gate_id=gate_id, verdict=verdict, checks=checks),
                      config={"stage": stage, "gate": gate_id, "config_hash": cfg.config_hash,
                              "producer": store.producer_version, "checks_digest": digest},
                      parents=list(parents), seed_map={}, consumer="experiment")


@register_stage
class S0Stage(Stage):
    """S0: the store is initialised, the environment lock exists, the contracts suite passes,
    and ``tools/check_imports.py`` is clean. Writes ``GateReport(stage="S0", gate_id="G-S0")``."""

    stage_id = "S0"
    gates = ("G-S0",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "S0", "job": "sanity"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        lock = cfg.repo_root / "requirements.lock"
        tests_ok, tests_line = run_tool([sys.executable, "-m", "pytest", "tests/contracts", "-q",
                                         "-p", "no:cacheprovider"], cfg)
        imports_ok, imports_line = run_tool([sys.executable, "tools/check_imports.py"], cfg)
        checks = (
            GateCheck("env_lock_present", lock.is_file(), lock.name, "exists"),
            GateCheck("contracts_tests", tests_ok, tests_line, "all pass"),
            GateCheck("check_imports", imports_ok, imports_line, "clean"),
        )
        return [save_tool_gate(store, cfg, "S0", "G-S0", checks, [])]


def latest_gate_verdicts(store: ArtifactStore, stage_id: str) -> dict[str, tuple[str, ...]]:
    """Per gate id of ``stage_id``: the verdicts of its most recent report(s).

    Reports are ordered by ``created_utc`` (second resolution); several reports written in the
    same second are all returned, so a waiver recorded right after a failure is not lost.
    """
    latest: dict[str, tuple[str, list[str]]] = {}
    for aid in store.find(GateReport, stage=stage_id):
        created = store.meta(aid).created_utc
        report = store.load(GateReport, aid, consumer="experiment")
        prev = latest.get(report.gate_id)
        if prev is None or created > prev[0]:
            latest[report.gate_id] = (created, [report.verdict])
        elif created == prev[0]:
            prev[1].append(report.verdict)
    return {gid: tuple(verdicts) for gid, (_, verdicts) in latest.items()}


def _check_requirements(stage: Stage, store: ArtifactStore) -> None:
    """Raise ``GATE_FAILED`` unless every gate of every required stage passed (or was waived)."""
    for required in stage.requires:
        verdicts = latest_gate_verdicts(store, required)
        cls = STAGE_REGISTRY.get(required)
        expected = (cls.gates if cls is not None and cls.gates else tuple(verdicts)) or ("<any>",)
        bad = [gid for gid in expected
               if not any(v in ("pass", "waived") for v in verdicts.get(gid, ()))]
        if bad:
            raise StageFailure(ErrorCode.GATE_FAILED, f"experiment.{stage.stage_id}", "requires",
                               f"required stage {required}: gates not passed {bad}")


def run_stage(stage_id: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[str]:
    """Run every planned job of ``stage_id`` inline; raises ``INVALID_CONFIG`` for an unknown
    stage and ``GATE_FAILED`` when a required stage's gate has not passed or a written
    GateReport has verdict ``fail``."""
    if stage_id not in STAGE_REGISTRY:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.run_stage", "stage_id",
                           f"stage {stage_id!r} is not implemented yet "
                           f"(available: {sorted(STAGE_REGISTRY)})")
    stage = STAGE_REGISTRY[stage_id]()
    _check_requirements(stage, store)
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
