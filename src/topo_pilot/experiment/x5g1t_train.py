"""X5 G1 training-study composition (x5g1-train-v3 §2, §8): the public ``Trainer`` with an
experiment-side checkpoint callback that mirrors the ``LearnerStage`` identity, controls before
and after every checkpoint write, one model per lock, and an outcome recorded on every exit."""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from pathlib import Path

from topo_pilot.analysis import X5_GRID
from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    ObservationSet,
    SeedTree,
    SequenceLayout,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import ModelConfig, TrainConfig, Trainer, serialise_state

from .x5g1t_runtime import (
    EST,
    RunLock,
    assert_can_start,
    interval_estimate,
    record_outcome,
)

LOCK_NAME = "RUN.lock"


def study_train_config(steps: int = 5000, grid=X5_GRID) -> TrainConfig:
    """Stored E3 values except ``checkpoint_steps`` = the grid and ``device = "cpu"``."""
    return TrainConfig(steps=steps, checkpoint_steps=tuple(int(t) for t in grid), device="cpu")


def study_run_key(master) -> tuple:
    """The same for both arms of a pair: identical init and batch order."""
    return ("x5g1", "cylinder", master)


def checkpoint_callback(store: ArtifactStore, obs_train_id: str, obs_dev_id: str,
                        model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree,
                        run_key: tuple, before: Callable[[int], None],
                        after: Callable[[int], None], record: list) -> Callable:
    """``on_checkpoint(step, model, info)``: ``before`` -> LearnerStage-identical save ->
    record ``{step, checkpoint_id, payload_sha256}`` -> ``after``."""
    model_dict, train_dict = dataclasses.asdict(model_cfg), dataclasses.asdict(train_cfg)
    run_id = "-".join(map(str, run_key))

    def on_checkpoint(step: int, model, info: dict) -> None:
        before(step)
        ckpt = Checkpoint(run_id=run_id, step=step, observation_id=obs_train_id,
                          state=serialise_state(model, info), model_config=model_dict,
                          train_config=train_dict,
                          has_optimizer_state="optimizer_state" in info)
        config = {"run_key": list(run_key), "step": step, "model_config": model_dict,
                  "train_config": train_dict}
        cid = store.save(ckpt, config=config, parents=[obs_train_id, obs_dev_id],
                         seed_map=dict(seeds.issued), consumer="experiment")
        record.append({"step": step, "checkpoint_id": cid,
                       "payload_sha256": store.meta(cid).payload_sha256})
        after(step)

    return on_checkpoint


def _next_updates(grid: tuple[int, ...], step: int) -> int:
    later = [t for t in grid if t > step]
    return later[0] - step if later else 0


def train_one(store: ArtifactStore, obs_train_id: str, obs_dev_id: str, model_cfg: ModelConfig,
              train_cfg: TrainConfig, master, arm: str, root: Path, controls,
              reserve_s: float = 0.0, est: dict = EST) -> dict:
    """Train one model under a run lock; always record COMPLETE or INCOMPLETE, then re-raise.

    ``controls.boundary(what, next_estimate, reserve, audit)`` runs before the model, before
    each checkpoint write and after it (STOP/hold/budget/resources).
    """
    root = Path(root)
    lock = root / LOCK_NAME
    assert_can_start(root, arm, master, lock)
    run_key = study_run_key(master)
    identity = {"arm": arm, "master": master, "run_key": list(run_key),
                "obs_train": obs_train_id, "obs_dev": obs_dev_id}
    record: list = []
    grid = tuple(train_cfg.checkpoint_steps)
    tag = f"{arm}/{master}"

    def audit() -> dict:
        return {"run": identity, "completed_checkpoints": list(record)}

    def before(step: int) -> None:
        controls.boundary(f"{tag} ckpt {step}", est["save"], reserve_s, audit)

    def after(step: int) -> None:
        controls.boundary(f"{tag} ckpt {step} done",
                          interval_estimate(_next_updates(grid, step), est)
                          if step < train_cfg.steps else 0.0, reserve_s, audit)

    outcome: dict = {"status": "INCOMPLETE", "arm": arm, "master": master, "run": identity,
                     "checkpoints": record, "cause": None}
    with RunLock(lock, identity):
        try:
            full = train_cfg.steps * est["update"] + len(grid) * (est["dev_ce"] + est["save"])
            controls.boundary(f"{tag} start", full, reserve_s, audit)
            layout = SequenceLayout()
            train = PublicTokenDataset(store.load(ObservationSet, obs_train_id,
                                                  consumer="learner"), layout)
            dev = PublicTokenDataset(store.load(ObservationSet, obs_dev_id, consumer="learner"),
                                     layout)
            seeds = SeedTree(master)
            cb = checkpoint_callback(store, obs_train_id, obs_dev_id, model_cfg, train_cfg,
                                     seeds, run_key, before, after, record)
            summary = Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, cb)
            outcome.update(status="COMPLETE" if len(record) == len(grid) else "INCOMPLETE",
                           dev_ce_by_step={str(k): v for k, v in
                                           summary.dev_ce_by_step.items()},
                           final_train_loss=summary.final_train_loss)
        except BaseException as exc:
            outcome["cause"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            record_outcome(root, arm, master, outcome)
    return outcome
