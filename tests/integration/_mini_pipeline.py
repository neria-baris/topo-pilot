"""Shared mini S1 -> S2 -> S3 pipeline for the I04 / I06 integration tests (CPU, minutes)."""

import shutil
import sys
from pathlib import Path

import numpy as np
import torch
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore,
    ErrorCode,
    GateCheck,
    GateReport,
    LocalFSBackend,
    StageFailure,
)
from topo_pilot.experiment import load_config, run_stage  # noqa: E402
from topo_pilot.experiment.stages import STAGE_REGISTRY, latest_gate_verdicts  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
THREADS = 2
_CACHE: dict[str, ArtifactStore] = {}


def _mini_configs(tmp: Path) -> Path:
    cfg_dir = tmp / "configs"
    shutil.copytree(REPO / "configs", cfg_dir, ignore=shutil.ignore_patterns("local.yaml"))
    base = yaml.safe_load((cfg_dir / "base.yaml").read_text(encoding="utf-8"))
    base["worlds"]["dims"] = [4, 4]
    base["emissions"]["V"] = 4
    base["seeds"]["masters"] = [1729, 2718]
    base["data"].update(n_train=2000, n_dev=256, n_test=256, n_panels=2, panel_size=64)
    base["model"].update(n_layers=2, d_model=16, n_heads=2, d_mlp=32,
                         hooks=["embed", "resid_post_0", "resid_post_1", "ln_final_out"],
                         primary_hook="resid_post_1")
    base["training"].update(steps=200, warmup=20, checkpoints=[0, 100, 200],
                            primary_checkpoint=200)
    (cfg_dir / "base.yaml").write_text(yaml.safe_dump(base), encoding="utf-8")
    stages = yaml.safe_load((cfg_dir / "stages.yaml").read_text(encoding="utf-8"))
    stages["S4"]["extract"]["all_panels_at"] = [0, 200]
    (cfg_dir / "stages.yaml").write_text(yaml.safe_dump(stages), encoding="utf-8")
    return cfg_dir / "stages.yaml"


def _waive_failures(store: ArtifactStore, stage: str) -> None:
    verdicts = latest_gate_verdicts(store, stage)
    for gid in STAGE_REGISTRY[stage].gates:
        if not any(v in ("pass", "waived") for v in verdicts.get(gid, ())):
            store.save(GateReport(stage=stage, gate_id=gid, verdict="waived",
                                  checks=(GateCheck("mini_world", False),),
                                  waiver_reason="integration mini config"),
                       config={"stage": stage, "gate": gid, "waiver": "mini"}, parents=[],
                       seed_map={}, consumer="experiment")


def build_store(tmp: Path, scramble_z: bool = False) -> ArtifactStore:
    """Run S1, S2, S3 of the mini config into a fresh store under ``tmp``.

    With ``scramble_z`` the dataset stage's ``EvalSidecar`` is built with row-reversed ``z``.
    """
    torch.set_num_threads(THREADS)
    cfg = load_config(_mini_configs(tmp), repo_root=REPO)
    cfg.stage("S3")["device_policy"]["torch_threads"] = THREADS
    store = ArtifactStore(LocalFSBackend(tmp / "artifacts"))
    store.save(GateReport(stage="S0", gate_id="G-S0", verdict="pass",
                          checks=(GateCheck("stub_for_integration", True),)),
               config={"stage": "S0", "gate": "G-S0"}, parents=[], seed_map={},
               consumer="experiment")
    import topo_pilot.dataset.stage as ds
    orig = ds.EvalSidecar
    if scramble_z:
        def scrambled(**kw):
            kw["z"] = np.ascontiguousarray(kw["z"][::-1])
            return orig(**kw)
        ds.EvalSidecar = scrambled
    try:
        for stage in ("S1", "S2", "S3"):
            try:
                run_stage(stage, cfg, store)
            except StageFailure as exc:
                if exc.code != ErrorCode.GATE_FAILED:
                    raise
                _waive_failures(store, stage)
    finally:
        ds.EvalSidecar = orig
    return store


def get_store(tmp_factory, name: str) -> ArtifactStore:
    """Session-cached store: ``plain`` or ``scrambled``."""
    if name not in _CACHE:
        _CACHE[name] = build_store(tmp_factory.mktemp(name), scramble_z=(name == "scrambled"))
    return _CACHE[name]


def ids_and_hashes(store: ArtifactStore, artifact_type) -> dict[str, str]:
    return {i: store.meta(i).payload_sha256 for i in store.find(artifact_type)}


def all_artifacts(store: ArtifactStore) -> dict[str, dict[str, str]]:
    """{artifact_type: {artifact_id: payload_sha256}} of every complete artifact."""
    import json

    from topo_pilot.contracts import ArtifactMeta
    out: dict[str, dict[str, str]] = {}
    for key in store.backend.list(""):
        if key.endswith("/meta.json"):
            meta = ArtifactMeta.from_json_dict(json.loads(store.backend.get(key)))
            if meta.status == "complete":
                digest = meta.payload_sha256
                if meta.artifact_type == "MetricRecords" and (
                        meta.config.get("kind") == "run_timing"
                        or meta.config.get("stage") == "S3"):
                    digest = _untimed_digest(store, meta.artifact_id)
                out.setdefault(meta.artifact_type, {})[meta.artifact_id] = digest
    return out


TIMING_METRICS = ("wall_time_s", "tokens_per_second", "projected_hours_S4", "projected_hours_S5")


def _untimed_digest(store: ArtifactStore, artifact_id: str) -> str:
    """Digest of a MetricRecords without its measured timing rows (wall time, throughput and the
    projections derived from them), which differ between identical reruns; every other row
    (regret, captured, dev CE, ...) must reproduce exactly."""
    import hashlib

    from topo_pilot.contracts import MetricRecords, canonical_json
    rows = [r for r in store.load(MetricRecords, artifact_id, consumer="experiment").rows
            if r.metric_id not in TIMING_METRICS]
    return "untimed:" + hashlib.sha256(canonical_json(rows).encode("utf-8")).hexdigest()
