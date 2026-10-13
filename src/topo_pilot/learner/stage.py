"""Checkpoint serialisation and the single I/O class of the learner."""

from __future__ import annotations

import dataclasses
import io
from typing import Any

import torch

from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.dataset import PublicTokenDataset

from .config import ModelConfig, TrainConfig
from .model import TransformerLM
from .trainer import Trainer, TrainSummary

CONSUMER = "learner"


def serialise_state(model: TransformerLM, info: dict[str, Any]) -> bytes:
    """``torch.save({"model": ...[, "optimizer", "scheduler"]})`` into bytes.

    torch's zip writer uses fixed timestamps and key order, so equal tensors give identical
    bytes (verified by test L06b). Optimizer / scheduler entries exist only if ``info`` has them
    (final step).
    """
    weights = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    payload: dict[str, Any] = {"model": weights}
    if "optimizer_state" in info:
        payload["optimizer"] = info["optimizer_state"]
        payload["scheduler"] = info["scheduler_state"]
    buffer = io.BytesIO()
    torch.save(payload, buffer)
    return buffer.getvalue()


def load_model(checkpoint: Checkpoint) -> TransformerLM:
    """Rebuild a ``TransformerLM`` (eval mode, CPU) from ``checkpoint.model_config`` + weights.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` if the config or the stored weights do not fit the architecture.
    """
    try:
        model = TransformerLM(ModelConfig(**dict(checkpoint.model_config)))
        state = torch.load(io.BytesIO(checkpoint.state), map_location="cpu", weights_only=True)
        model.load_state_dict(state["model"])
    except (TypeError, KeyError, RuntimeError) as exc:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.load_model", "checkpoint",
                           f"{type(exc).__name__}: {exc}") from exc
    return model.eval()


class LearnerStage:
    """Loads the two ObservationSets (consumer ``learner``), trains, saves one Checkpoint per step.

    Identity: each checkpoint's config is ``{run_key, step, model_config, train_config}`` with
    parents ``[obs_train_id, obs_dev_id]``, so ids are content-addressed by what generates them.
    After ``run``, ``last_summary`` holds the ``TrainSummary`` (with ``checkpoint_ids``).
    """

    def __init__(self) -> None:
        self.last_summary: TrainSummary | None = None

    def run(self, obs_train_id: str, obs_dev_id: str, model_cfg: ModelConfig,
            train_cfg: TrainConfig, seeds: SeedTree, run_key: tuple,
            store: ArtifactStore) -> list[str]:
        """Train and store checkpoints; returns their ids in step order.

        Raises
        ------
        StageFailure
            ``LEAKAGE`` (store policy), ``NONFINITE_LOSS``, ``INVALID_CONFIG`` and store errors.
        """
        layout = SequenceLayout()
        train_obs = store.load(ObservationSet, obs_train_id, consumer=CONSUMER)
        dev_obs = store.load(ObservationSet, obs_dev_id, consumer=CONSUMER)
        train, dev = PublicTokenDataset(train_obs, layout), PublicTokenDataset(dev_obs, layout)
        model_dict = dataclasses.asdict(model_cfg)
        train_dict = dataclasses.asdict(train_cfg)
        run_id = "-".join(map(str, run_key))
        ids: list[str] = []

        def save(step: int, model: TransformerLM, info: dict) -> None:
            ckpt = Checkpoint(run_id=run_id, step=step, observation_id=obs_train_id,
                              state=serialise_state(model, info), model_config=model_dict,
                              train_config=train_dict,
                              has_optimizer_state="optimizer_state" in info)
            config = {"run_key": list(run_key), "step": step, "model_config": model_dict,
                      "train_config": train_dict}
            ids.append(store.save(ckpt, config=config, parents=[obs_train_id, obs_dev_id],
                                  seed_map=dict(seeds.issued), consumer=CONSUMER))

        summary = Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, save)
        self.last_summary = dataclasses.replace(summary, checkpoint_ids=tuple(ids))
        return ids
