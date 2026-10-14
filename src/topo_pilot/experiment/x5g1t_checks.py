"""X5 G1 study integrity checks (x5g1-train-v4 §11; API v4 §5): full-hash verification of used
artifacts and checkpoint identity against the model, arm, master and pools."""

from __future__ import annotations

import dataclasses

from topo_pilot.contracts import ArtifactStore, Checkpoint
from topo_pilot.learner import ModelConfig

from .x5g1_safety import verify_sources_full
from .x5g1t_train import study_run_key, study_train_config


class IntegrityFailed(RuntimeError):
    """A used artifact failed full-hash verification or checkpoint identity checks."""


def verify_full(store: ArtifactStore, expected: dict, when: str) -> None:
    bad = verify_sources_full(store, expected)
    if bad:
        raise IntegrityFailed(f"integrity {when}: " + "; ".join(bad))


def validate_checkpoints(store: ArtifactStore, outcome: dict, cfg, arm: str, master,
                         train_pool_id: str, dev_pool_id: str) -> dict:
    """``{checkpoint_id: (Checkpoint, sha)}`` after checking every identity field."""
    ckpts = outcome.get("checkpoints") or []
    if outcome.get("arm") != arm or outcome.get("master") != master:
        raise IntegrityFailed(f"outcome is for {outcome.get('arm')}/{outcome.get('master')}, "
                              f"not {arm}/{master}")
    steps = [c.get("step") for c in ckpts]
    if steps != list(cfg.grid):
        raise IntegrityFailed(f"{arm}/{master}: checkpoint steps {steps} != grid")
    run_key = study_run_key(master)
    want_cfg = {"run_key": list(run_key),
                "model_config": dataclasses.asdict(ModelConfig(**cfg.model_config)),
                "train_config": dataclasses.asdict(study_train_config(cfg.steps, cfg.grid))}
    want_parents = tuple(sorted({train_pool_id, dev_pool_id}))
    run_id = "-".join(map(str, run_key))
    out = {}
    for c in ckpts:
        cid, sha = c.get("checkpoint_id"), c.get("payload_sha256")
        try:
            meta = store.meta(cid)
        except Exception as exc:  # noqa: BLE001 - any failure is an integrity failure
            raise IntegrityFailed(f"{cid}: {type(exc).__name__}: {exc}") from exc
        expect = {**want_cfg, "step": c["step"]}
        if meta.artifact_type != "Checkpoint" or meta.payload_sha256 != sha:
            raise IntegrityFailed(f"{cid}: type/payload mismatch")
        if dict(meta.config) != expect:
            raise IntegrityFailed(f"{cid}: config differs from the study identity")
        if tuple(meta.parent_ids) != want_parents:
            raise IntegrityFailed(f"{cid}: parents {meta.parent_ids} != {want_parents}")
        verify_full(store, {cid: (Checkpoint, sha)}, f"checkpoint {cid}")
        ck = store.load(Checkpoint, cid, consumer="experiment")
        if ck.observation_id != train_pool_id or ck.run_id != run_id or ck.step != c["step"]:
            raise IntegrityFailed(f"{cid}: observation/run/step identity mismatch")
        out[cid] = (Checkpoint, sha)
    return out
