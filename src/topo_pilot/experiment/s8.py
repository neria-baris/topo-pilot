"""Stage S8: final reproducibility and integration checks (D-047, D-048); gate G-H.

Jobs, each writing one MetricRecords (``stage = S8``, ``kind`` = job name):

- ``rerun``: clone HEAD into a fresh temporary directory, run ``S8.rerun_stages`` (S0→S3; S3
  trains exactly ``rerun_identity_check``) with the same interpreter, the clone's sources first
  on ``PYTHONPATH`` and an empty artifact store; then compare every rerun artifact with the main
  store: same id present, same ``payload_sha256``. MetricRecords that embed measured timing
  (``kind = run_timing`` and the S3 stage record) are compared without their timing rows.
  GateReports embed tool output and the config hash, so they are compared by (stage, gate,
  verdict) only. The clone is deleted afterwards; wall times per stage are recorded.
- ``integrity``: every artifact of the main store is complete, its parents exist, and it loads
  with its payload checksum verified (``ArtifactStore.load``).
- ``reports``: E0/E2/E3 regenerated from MetricRecords into a temporary directory and compared
  byte for byte with the committed ``reports/`` files.
- ``tests``: module suites (default selection), ``slow`` tests and ``integration`` tests.

G-H passes iff the rerun reproduces every non-gate artifact (ids and checksums, timing rows
excepted), the store is intact, the reports reproduce, and every test command passes.
"""

from __future__ import annotations

import filecmp
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from topo_pilot.contracts import (
    ARTIFACT_CLASSES,
    ArtifactMeta,
    ArtifactStore,
    ErrorCode,
    GateCheck,
    GateReport,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    StageFailure,
    canonical_json,
)

from .config import ResolvedConfig
from .stages import Stage, register_stage, run_tool, save_tool_gate

log = logging.getLogger(__name__)
CONS = "experiment"
TIMING_METRICS = ("wall_time_s", "tokens_per_second", "projected_hours_S4", "projected_hours_S5")
REPORT_LEVELS = ("E0", "E2", "E3")
REPORT_INPUTS = ("PREREGISTRATION.md", "PREREGISTRATION_X4.md", "state/DECISIONS.md")
HAND_WRITTEN = ("exploratory.md",)  # conductor notes, not generated from MetricRecords


def _row(metric: str, value: float | None, space: str, **kw: Any) -> MetricRow:
    status = kw.pop("status", "ok" if value is not None else "inconclusive")
    return MetricRow(run_id="S8", space=space, metric_id=metric,
                     value=None if value is None else float(value), status=status, **kw)


def metas(store: ArtifactStore) -> list[ArtifactMeta]:
    """Every artifact meta of a local store."""
    out = []
    for key in store.backend.list(""):
        if key.endswith("/meta.json"):
            out.append(ArtifactMeta.from_json_dict(json.loads(store.backend.get(key))))
    return out


def timed(meta: ArtifactMeta) -> bool:
    """MetricRecords whose rows include measured wall time or throughput."""
    return meta.artifact_type == "MetricRecords" and (
        meta.config.get("kind") == "run_timing" or meta.config.get("stage") == "S3")


def untimed_digest(store: ArtifactStore, artifact_id: str) -> str:
    rows = [r for r in store.load(MetricRecords, artifact_id, consumer=CONS).rows
            if r.metric_id not in TIMING_METRICS]
    return hashlib.sha256(canonical_json(rows).encode("utf-8")).hexdigest()


def compare_stores(main: ArtifactStore, rerun: ArtifactStore) -> tuple[list[MetricRow], bool]:
    """Rows per artifact type (n, ids found, checksums equal) and the overall match flag."""
    counts: dict[str, Counter] = {}
    bad: list[str] = []
    gates_ok = True
    for meta in metas(rerun):
        t = meta.artifact_type
        c = counts.setdefault(t, Counter())
        c["n"] += 1
        if t == "GateReport":
            report = rerun.load(GateReport, meta.artifact_id, consumer=CONS)
            ref = {(main.load(GateReport, g, consumer=CONS).gate_id,
                    main.load(GateReport, g, consumer=CONS).verdict)
                   for g in main.find(GateReport, stage=meta.config.get("stage"))}
            same = (report.gate_id, report.verdict) in ref
            c["verdict_match"] += int(same)
            gates_ok &= same
            continue
        try:
            ref_meta = main.meta(meta.artifact_id)
        except StageFailure:
            bad.append(f"{t}:{meta.artifact_id}:missing")
            continue
        c["id_found"] += 1
        if timed(meta):
            equal = untimed_digest(main, meta.artifact_id) == untimed_digest(rerun,
                                                                             meta.artifact_id)
        else:
            equal = ref_meta.payload_sha256 == meta.payload_sha256
        c["checksum_equal"] += int(equal)
        if not equal:
            bad.append(f"{t}:{meta.artifact_id}:checksum")
    rows = []
    for t, c in sorted(counts.items()):
        for k in ("n", "id_found", "checksum_equal", "verdict_match"):
            if k in c or (k == "verdict_match") == (t == "GateReport"):
                rows.append(_row(k, c[k], f"rerun:{t}"))
    ok = not bad and gates_ok and all(c["n"] for c in counts.values())
    rows.append(_row("mismatches", len(bad), "rerun", uncertainty_kind="; ".join(bad[:20]) or None))
    return rows, ok


class RerunJob:
    """Fresh clone of HEAD + empty store; S0→S3; comparison with the main store."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        s8 = cfg.stage("S8")
        self.stages = list(s8["rerun_stages"])
        self.run = dict(s8["rerun_identity_check"])

    def git(self, *args: str, cwd: Path | None = None) -> str:
        return subprocess.run(["git", *args], cwd=cwd or self.cfg.repo_root, check=True,
                              capture_output=True, text=True, timeout=600).stdout.strip()

    def run_job(self) -> tuple[list[MetricRow], bool]:
        s3_runs = [dict(r) for r in self.cfg.stage("S3")["runs"]]
        if s3_runs != [self.run]:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.S8", "rerun_run",
                               f"S3 trains {s3_runs}, not the registered {self.run}")
        sha = self.git("rev-parse", "--short=12", "HEAD")
        tmp = Path(tempfile.mkdtemp(prefix="topo-pilot-rerun-"))
        rows = [_row("cpu_count", os.cpu_count(), "rerun",
                     uncertainty_kind=f"HEAD {sha} | {platform.platform()} | "
                                      f"python {platform.python_version()}")]
        try:
            clone = tmp / "repo"
            self.git("clone", "--quiet", "--no-hardlinks", str(self.cfg.repo_root), str(clone))
            env = {**os.environ, "PYTHONPATH": str(clone / "src")}
            for sid in self.stages:
                t0 = time.time()
                proc = subprocess.run([sys.executable, "-m", "topo_pilot.experiment.cli", "stage",
                                       sid, "--config", "configs/stages.yaml"], cwd=clone,
                                      env=env, capture_output=True, text=True, timeout=4 * 3600)
                rows.append(_row("rerun_wall_time_s", time.time() - t0, f"rerun:{sid}",
                                 uncertainty_kind=None if proc.returncode == 0
                                 else proc.stderr.strip().splitlines()[-1][:200]))
                if proc.returncode != 0:
                    log.error("S8 rerun: %s failed: %s", sid, proc.stderr[-2000:])
                    return rows + [_row("rerun_completed", 0, "rerun")], False
            rerun = ArtifactStore(LocalFSBackend(clone / "artifacts"))
            cmp_rows, ok = compare_stores(self.store, rerun)
            return rows + [_row("rerun_completed", 1, "rerun")] + cmp_rows, ok
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def integrity(store: ArtifactStore) -> tuple[list[MetricRow], bool]:
    """Every artifact complete, parents present, payload checksum verified on load."""
    counts: Counter = Counter()
    bad: list[str] = []
    all_metas = metas(store)
    ids = {m.artifact_id for m in all_metas}
    for meta in all_metas:
        counts["n"] += 1
        if meta.status != "complete":
            bad.append(f"{meta.artifact_id}:incomplete")
            continue
        missing = [p for p in meta.parent_ids if p not in ids]
        if missing:
            bad.append(f"{meta.artifact_id}:missing_parent")
        try:
            store.load(ARTIFACT_CLASSES[meta.artifact_type], meta.artifact_id, consumer=CONS)
            counts["verified"] += 1
        except StageFailure as exc:
            bad.append(f"{meta.artifact_id}:{exc.code.value}")
    rows = [_row("n_artifacts", counts["n"], "integrity"),
            _row("n_verified", counts["verified"], "integrity"),
            _row("n_problems", len(bad), "integrity", uncertainty_kind="; ".join(bad[:20]) or None)]
    return rows, not bad and counts["n"] == counts["verified"]


def reproduce_reports(cfg: ResolvedConfig, store: ArtifactStore) -> tuple[list[MetricRow], bool]:
    """Regenerate E0/E2/E3 into a temporary directory; compare with the committed files."""
    from .cli import build_reports

    tmp = Path(tempfile.mkdtemp(prefix="topo-pilot-reports-"))
    rows, ok = [], True
    try:
        shadow = cfg.__class__(repo_root=tmp, base=cfg.base, stages=cfg.stages, local=cfg.local)
        for name in REPORT_INPUTS:  # the text the builders quote verbatim
            (tmp / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cfg.repo_root / name, tmp / name)
        for level in REPORT_LEVELS:
            build_reports(level, shadow, store)
            committed = sorted(f for f in (cfg.repo_root / "reports" / level).iterdir()
                               if f.name not in HAND_WRITTEN)
            for f in committed:
                new = tmp / "reports" / level / f.name
                same = new.is_file() and filecmp.cmp(f, new, shallow=False)
                ok &= same
                rows.append(_row("identical", int(same), f"reports:{level}/{f.name}"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return rows, ok


def test_rows(cfg: ResolvedConfig) -> list[GateCheck]:
    py = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    cmds = {"module_suites": [*py, "tests"], "slow_tests": [*py, "tests", "-m", "slow"],
            "integration_tests": [*py, "tests/integration", "-m", "integration"]}
    out = []
    for name, cmd in cmds.items():
        passed, line = run_tool(cmd, cfg, timeout=3 * 3600)
        out.append(GateCheck(name, passed, line, "all pass"))
    return out


@register_stage
class S8Stage(Stage):
    """S8: clean rerun, store integrity, report reproduction, test suites; gate G-H."""

    stage_id = "S8"
    requires = ("S7",)
    gates = ("G-H",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"job": "all"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        written, checks = [], []
        for kind, fn in (("rerun", lambda: RerunJob(cfg, store).run_job()),
                         ("integrity", lambda: integrity(store)),
                         ("reports", lambda: reproduce_reports(cfg, store))):
            log.info("S8: %s", kind)
            rows, ok = fn()
            digest = hashlib.sha256(canonical_json(rows).encode("utf-8")).hexdigest()[:16]
            written.append(store.save(MetricRecords(rows=tuple(rows)),
                                      config={"stage": "S8", "kind": kind,
                                              "producer": store.producer_version,
                                              "rows_digest": digest},
                                      parents=[], seed_map={}, consumer=CONS))
            checks.append(GateCheck(f"{kind}_ok", ok, ok, True))
        checks += test_rows(cfg)
        written.append(save_tool_gate(store, cfg, "S8", "G-H", checks, written))
        return written
