# `src/topo_pilot/learner/trainer.py`

- Source: [src/topo_pilot/learner/trainer.py](../../../../../../src/topo_pilot/learner/trainer.py)
- Kind: python
- Lines: 203

## Module docstring

> Training loop: AdamW + warmup/cosine, deterministic batch order, dev CE at checkpoints.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 15, via package root)
- `from .config import ModelConfig, TrainConfig` -> [src/topo_pilot/learner/config.py](config.py.md) (line 17, via relative)
- `from .model import TransformerLM` -> [src/topo_pilot/learner/model.py](model.py.md) (line 18, via relative)

### External (third-party)

- `torch` (lines 11, 12)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 8)
- `dataclasses` (lines 9)
- `logging` (lines 5)
- `math` (lines 6)
- `time` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/learner/__init__.py](__init__.py.md) (line 7, import)
- [src/topo_pilot/learner/multihorizon.py](multihorizon.py.md) (line 22, import)
- [src/topo_pilot/learner/stage.py](stage.py.md) (line 24, import)
- [tests/learner/test_multihorizon.py](../../../tests/learner/test_multihorizon.py.md) (line 46, import)
- [tests/learner/test_training.py](../../../tests/learner/test_training.py.md) (line 115, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 35, import)
- [tests/x6_stage1/test_b_train_chain.py](../../../tests/x6_stage1/test_b_train_chain.py.md) (line 33, import)
- [tools/x6_stage1/x6s1_cloud.py](../../../tools/x6_stage1/x6s1_cloud.py.md) (line 30, import)
- [tools/x6_stage1/x6s1_ingest.py](../../../tools/x6_stage1/x6s1_ingest.py.md) (line 29, import)

## Top-level constants

- `_DEV_BATCH`
- `_NO_DECAY_PARENTS`

## Classes and functions

- **class `TrainSummary`** [L26-41] decorators: @dataclass(frozen=True) - Outcome of ``Trainer.fit``.
- **class `WarmupCosine`** [L45-55] decorators: @dataclass - LR multiplier after ``s`` finished updates (picklable, so scheduler state is plain data).
- **method `WarmupCosine.__call__`** [L51-55]: `def __call__(self, s: int) -> float`
- **function `resolve_device`** [L58-62]: `def resolve_device(name: str) -> torch.device` - ``"auto"`` -> CUDA if available else CPU; otherwise ``torch.device(name)``.
- **function `_materialise`** [L65-67]: `def _materialise(ds: PublicTokenDataset) -> tuple[torch.Tensor, torch.Tensor]`
- **function `lm_loss`** [L70-72]: `def lm_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor` - Mean cross-entropy over every position: ``-mean log softmax(logits)[target]``.
- **class `Trainer`** [L75-194] - Trains a ``TransformerLM`` on public tokens only.
- **method `Trainer.__init__`** [L91-96]: `def __init__(self, model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree, run_key: tuple, *, model_factory=None, loss_fn=None)`
- **method `Trainer._check_config`** [L98-104]: `def _check_config(self) -> None`
- **method `Trainer._optimizer`** [L106-113]: `def _optimizer(self, model: TransformerLM) -> torch.optim.AdamW`
- **method `Trainer.dev_ce`** [L116-127]: `def dev_ce(self, model: TransformerLM, x: torch.Tensor, y: torch.Tensor) -> float` decorators: @torch.no_grad() - Mean CE (nats per position) over the whole dev set, batched, no grad, eval mode.
- **method `Trainer.fit`** [L129-146]: `def fit(self, train: PublicTokenDataset, dev: PublicTokenDataset, on_checkpoint: Callable[[int, TransformerLM, dict], None]) -> TrainSummary` - Run training; ``on_checkpoint(step, model, info)`` is called at every checkpoint step.
- **method `Trainer._fit`** [L148-194]: `def _fit(self, train, dev, on_checkpoint) -> TrainSummary`
- **function `_require_finite`** [L197-200]: `def _require_finite(loss: torch.Tensor, where: str) -> None`

