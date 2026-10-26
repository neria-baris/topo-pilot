# `src/topo_pilot/learner/model.py`

- Source: [src/topo_pilot/learner/model.py](../../../../../../src/topo_pilot/learner/model.py)
- Kind: python
- Lines: 169

## Module docstring

> Decoder-only pre-LN transformer with named residual-stream hooks.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 13, via package root)
- `from .config import ModelConfig` -> [src/topo_pilot/learner/config.py](config.py.md) (line 15, via relative)

### External (third-party)

- `torch` (lines 9, 10, 11)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 6)
- `dataclasses` (lines 7)
- `math` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/learner/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/learner/multihorizon.py](multihorizon.py.md) (line 21, import)
- [src/topo_pilot/learner/patch.py](patch.py.md) (line 16, import)
- [src/topo_pilot/learner/stage.py](stage.py.md) (line 23, import)
- [src/topo_pilot/learner/trainer.py](trainer.py.md) (line 18, import)
- [tests/c2_readout/test_a_readout.py](../../../tests/c2_readout/test_a_readout.py.md) (line 35, import)

## Top-level constants

- `HOOK_NAMES`

## Classes and functions

- **function `hook_names`** [L21-23]: `def hook_names(n_layers: int) -> tuple[str, ...]` - Hook names for a model with ``n_layers`` blocks (equals ``HOOK_NAMES`` for 4).
- **class `ModelOutput`** [L27-32] decorators: @dataclass(frozen=True) - Forward result: ``logits [B, n_ctx, vocab_out]`` and requested ``hooks`` (each
- **class `CausalSelfAttention(nn.Module)`** [L35-49] - Multi-head causal self-attention: softmax(Q K^T / sqrt(d_head) + causal mask) V.
- **method `CausalSelfAttention.__init__`** [L38-42]: `def __init__(self, cfg: ModelConfig)`
- **method `CausalSelfAttention.forward`** [L44-49]: `def forward(self, x: torch.Tensor) -> torch.Tensor`
- **class `Block(nn.Module)`** [L52-66] - Pre-LN block: ``x = x + Attn(LN(x)); x = x + MLP(LN(x))``.
- **method `Block.__init__`** [L55-62]: `def __init__(self, cfg: ModelConfig)`
- **method `Block.forward`** [L64-66]: `def forward(self, x: torch.Tensor) -> torch.Tensor`
- **class `TransformerLM(nn.Module)`** [L69-126] - Decoder-only, pre-LN, learned positional embeddings, final LN, untied unembedding.
- **method `TransformerLM.__init__`** [L84-95]: `def __init__(self, cfg: ModelConfig)`
- **method `TransformerLM._init_weights`** [L97-106]: `def _init_weights(self) -> None` - N(0, 0.02) for embeddings and matrices; residual output projections scaled by
- **method `TransformerLM.forward`** [L108-126]: `def forward(self, inputs: torch.Tensor, *, return_hooks: Sequence[str] = ()) -> ModelOutput`
- **function `_validate`** [L129-141]: `def _validate(cfg: ModelConfig) -> None`
- **function `check_causal`** [L145-169]: `def check_causal(model: TransformerLM, tol: float = 1e-06) -> None` decorators: @torch.no_grad() - Perturb one input position j of a random batch; logits at positions < j must not move.

