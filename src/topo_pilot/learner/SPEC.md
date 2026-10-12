# SPEC: `learner` (wave W3)

## Purpose

- The model definition;
- the training loop;
- checkpoint save and restore.

It sees **only** public tokens.

## Public API

```python
@dataclass(frozen=True)
class ModelConfig:
    vocab_in: int; vocab_out: int; n_ctx: int = 33
    n_layers: int = 4; d_model: int = 128; n_heads: int = 4; d_mlp: int = 512
    activation: Literal["gelu"] = "gelu"; dropout: float = 0.0; tie_embeddings: bool = False

HOOK_NAMES: tuple[str, ...]   # ("embed", "resid_post_0", ..., f"resid_post_{L-1}", "ln_final_out")

class TransformerLM(torch.nn.Module):
    """Decoder-only, pre-LN, learned positional embeddings, final LN, untied unembedding."""
    def __init__(self, cfg: ModelConfig): ...
    def forward(self, inputs: torch.LongTensor, *, return_hooks: Sequence[str] = ()) -> ModelOutput: ...
    # ModelOutput(logits [B, n_ctx, vocab_out], hooks: dict[name, Tensor[B, n_ctx, d_model]])

@dataclass(frozen=True)
class TrainConfig:
    steps: int = 5000; batch_size: int = 128; lr: float = 1e-3; warmup: int = 200
    schedule: Literal["cosine"] = "cosine"; weight_decay: float = 0.1; grad_clip: float = 1.0
    checkpoint_steps: tuple[int, ...] = (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000)
    device: str = "auto"

class Trainer:
    def __init__(self, model_cfg: ModelConfig, train_cfg: TrainConfig, seeds: SeedTree, run_key: tuple): ...
    def fit(self, train: PublicTokenDataset, dev: PublicTokenDataset,
            on_checkpoint: Callable[[int, TransformerLM, dict], None]) -> TrainSummary: ...
    # loss: mean cross-entropy over all 33 positions; dev CE logged at every checkpoint

class LearnerStage:   # I/O, consumer "learner"
    def run(self, obs_train_id: str, obs_dev_id: str, model_cfg, train_cfg,
            seeds: SeedTree, run_key: tuple, store: ArtifactStore) -> list[str]: ...  # checkpoint ids
def load_model(checkpoint: Checkpoint) -> TransformerLM: ...   # used by `activations`
```

## Logic requirements

- **Hook semantics.** `resid_post_k` is the residual stream after block k, before any final LayerNorm. `embed` is the token embedding plus the positional embedding.
- **Randomness.** Initialisation uses `seeds.seed("init", *run_key)`. Batch order uses `seeds.generator("batch_order", *run_key)`. Sampling is with replacement over training trajectories: each step draws `batch_size` trajectory indices.
- **Checkpoints.** Step 0 is saved **before** any update. Optimizer and scheduler state are stored only at the final step.
- **Device.** "auto" means CUDA if available, otherwise CPU. Record the device and the torch version in the metadata. Determinism flags are set where available. GPU nondeterminism is documented, not hidden.
- **Throughput report.** `TrainSummary` includes tokens per second, used by S3 to project compute.

## Invariants and errors

| Condition | Error |
|---|---|
| changing input position j changes logits at positions < j | `CAUSAL_MASK_FAILED` (checked once at construction on a random batch) |
| NaN or Inf loss | `NONFINITE_LOSS` (the run is marked failed, never retried silently) |
| a dataset that is not a `PublicTokenDataset`, or an artifact access outside the policy | `LEAKAGE` |

## Dependencies and forbidden information

`contracts`, torch, and `dataset.PublicTokenDataset` (public API). **Must not import** `world`, `process`, `oracle`, `analysis`, or `prediction`. **Must not load** `EvalSidecar`, `TransitionSpec`, or `EmissionSpec`. `tools/check_imports.py` enforces this.

## Done when

The TEST_PLAN passes on CPU. The README documents the hook semantics with a diagram of one block.
