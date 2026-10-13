"""Training loop: AdamW + warmup/cosine, deterministic batch order, dev CE at checkpoints."""

from __future__ import annotations

import logging
import math
import time
from collections.abc import Callable
from dataclasses import dataclass, field

import torch
import torch.nn.functional as F

from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure
from topo_pilot.dataset import PublicTokenDataset

from .config import ModelConfig, TrainConfig
from .model import TransformerLM

log = logging.getLogger(__name__)
_NO_DECAY_PARENTS = ("tok_emb", "pos_emb")
_DEV_BATCH = 512


@dataclass(frozen=True)
class TrainSummary:
    """Outcome of ``Trainer.fit``.

    ``tokens_per_second`` = target tokens processed / wall time, excluding the step-0 dev
    evaluation and step-0 callback. ``dev_ce_by_step`` maps checkpoint step -> mean dev CE
    (nats per position). ``checkpoint_ids`` is filled by ``LearnerStage``.
    """

    steps_done: int
    final_train_loss: float
    dev_ce_by_step: dict[int, float]
    tokens_per_second: float
    wall_time_s: float
    device: str
    torch_version: str
    checkpoint_ids: tuple[str, ...] = field(default=())


@dataclass
class WarmupCosine:
    """LR multiplier after ``s`` finished updates (picklable, so scheduler state is plain data)."""

    warmup: int
    steps: int

    def __call__(self, s: int) -> float:
        if s < self.warmup:
            return (s + 1) / self.warmup
        frac = (s - self.warmup) / max(1, self.steps - self.warmup)
        return 0.5 * (1.0 + math.cos(math.pi * frac))


def resolve_device(name: str) -> torch.device:
    """``"auto"`` -> CUDA if available else CPU; otherwise ``torch.device(name)``."""
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


def _materialise(ds: PublicTokenDataset) -> tuple[torch.Tensor, torch.Tensor]:
    items = [ds[i] for i in range(len(ds))]
    return torch.stack([a for a, _ in items]), torch.stack([b for _, b in items])


def lm_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """Mean cross-entropy over every position: ``-mean log softmax(logits)[target]``."""
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))


class Trainer:
    """Trains a ``TransformerLM`` on public tokens only.

    Math: loss = mean over batch and all 33 positions of CE; AdamW (betas 0.9/0.999, eps 1e-8),
    decay on weight matrices only (all ``nn.Linear`` weights incl. unembedding; biases, LayerNorm
    and both embeddings excluded), global-norm clipping, ``WarmupCosine`` multiplier.
    Batch ``k`` = ``batch_size`` indices drawn with replacement from
    ``seeds.generator("batch_order", *run_key)``; init under ``seeds.seed("init", *run_key)``.

    Raises
    ------
    StageFailure
        ``LEAKAGE`` (non-PublicTokenDataset), ``NONFINITE_LOSS``, ``INVALID_CONFIG``
        (steps < 1, checkpoint step outside ``0..steps``, bad warmup/batch size).
    """

    def __init__(self, model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree,
                 run_key: tuple):
        self.model_cfg, self.train_cfg = model_cfg, train_cfg
        self.seeds, self.run_key = seeds, tuple(run_key)
        self.model: TransformerLM | None = None

    def _check_config(self) -> None:
        c = self.train_cfg
        bad = [s for s in c.checkpoint_steps if not 0 <= s <= c.steps]
        if c.steps < 1 or c.batch_size < 1 or c.warmup < 1 or bad or c.schedule != "cosine":
            raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.Trainer", "train_config",
                               f"steps={c.steps} batch={c.batch_size} warmup={c.warmup} "
                               f"checkpoint steps outside 0..steps: {bad}")

    def _optimizer(self, model: TransformerLM) -> torch.optim.AdamW:
        decay, plain = [], []
        for name, p in model.named_parameters():
            is_matrix = p.ndim == 2 and not name.startswith(_NO_DECAY_PARENTS)
            (decay if is_matrix else plain).append(p)
        groups = [{"params": decay, "weight_decay": self.train_cfg.weight_decay},
                  {"params": plain, "weight_decay": 0.0}]
        return torch.optim.AdamW(groups, lr=self.train_cfg.lr)

    @torch.no_grad()
    def dev_ce(self, model: TransformerLM, x: torch.Tensor, y: torch.Tensor) -> float:
        """Mean CE (nats per position) over the whole dev set, batched, no grad, eval mode."""
        model.eval()
        total, count = 0.0, 0
        for i in range(0, x.shape[0], _DEV_BATCH):
            xb, yb = x[i:i + _DEV_BATCH], y[i:i + _DEV_BATCH]
            loss = lm_loss(model(xb).logits, yb)
            _require_finite(loss, "dev")
            total += float(loss) * yb.numel()
            count += yb.numel()
        model.train()
        return total / count

    def fit(self, train: PublicTokenDataset, dev: PublicTokenDataset,
            on_checkpoint: Callable[[int, TransformerLM, dict], None]) -> TrainSummary:
        """Run training; ``on_checkpoint(step, model, info)`` is called at every checkpoint step.

        ``info`` has ``dev_ce``, ``train_loss`` (None at step 0), ``is_final`` and, at the final
        step only, ``optimizer_state`` and ``scheduler_state`` (live state dicts: serialise now).
        """
        for name, ds in (("train", train), ("dev", dev)):
            if not isinstance(ds, PublicTokenDataset):
                raise StageFailure(ErrorCode.LEAKAGE, "learner.Trainer", f"{name}_dataset",
                                   f"expected PublicTokenDataset, got {type(ds).__name__}")
        self._check_config()
        previous = torch.are_deterministic_algorithms_enabled()
        torch.use_deterministic_algorithms(True, warn_only=True)
        try:
            return self._fit(train, dev, on_checkpoint)
        finally:
            torch.use_deterministic_algorithms(previous, warn_only=True)

    def _fit(self, train, dev, on_checkpoint) -> TrainSummary:
        cfg, device = self.train_cfg, resolve_device(self.train_cfg.device)
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(self.seeds.seed("init", *self.run_key))
            model = TransformerLM(self.model_cfg)
        model.to(device).train()
        self.model = model
        x_tr, y_tr = (t.to(device) for t in _materialise(train))
        x_dev, y_dev = (t.to(device) for t in _materialise(dev))
        opt = self._optimizer(model)
        sched = torch.optim.lr_scheduler.LambdaLR(opt, WarmupCosine(cfg.warmup, cfg.steps))
        rng = self.seeds.generator("batch_order", *self.run_key)
        marks = set(cfg.checkpoint_steps)
        dev_by_step: dict[int, float] = {}

        def checkpoint(step: int, train_loss: float | None) -> None:
            ce = self.dev_ce(model, x_dev, y_dev)
            dev_by_step[step] = ce
            info = {"dev_ce": ce, "train_loss": train_loss, "is_final": step == cfg.steps}
            if step == cfg.steps:
                info["optimizer_state"] = opt.state_dict()
                info["scheduler_state"] = sched.state_dict()
            on_checkpoint(step, model, info)
            log.info("learner checkpoint step=%d dev_ce=%.4f", step, ce)

        if 0 in marks:
            checkpoint(0, None)
        start, loss_val = time.perf_counter(), float("nan")
        for step in range(1, cfg.steps + 1):
            idx = torch.from_numpy(rng.integers(0, x_tr.shape[0], size=cfg.batch_size)).to(device)
            loss = lm_loss(model(x_tr[idx]).logits, y_tr[idx])
            _require_finite(loss, f"train step {step}")
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            opt.step()
            sched.step()
            loss_val = float(loss.detach())
            if step in marks:
                checkpoint(step, loss_val)
        wall = time.perf_counter() - start
        tokens = cfg.steps * cfg.batch_size * y_tr.shape[1]
        return TrainSummary(steps_done=cfg.steps, final_train_loss=loss_val,
                            dev_ce_by_step=dev_by_step, tokens_per_second=tokens / wall,
                            wall_time_s=wall, device=str(device), torch_version=torch.__version__)


def _require_finite(loss: torch.Tensor, where: str) -> None:
    if not bool(torch.isfinite(loss)):
        raise StageFailure(ErrorCode.NONFINITE_LOSS, "learner.Trainer", "loss",
                           f"non-finite loss at {where}", recoverable=False)


__all__ = ["TrainSummary", "Trainer", "WarmupCosine", "lm_loss", "resolve_device"]
