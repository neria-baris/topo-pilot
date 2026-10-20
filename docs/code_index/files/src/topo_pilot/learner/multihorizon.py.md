# `src/topo_pilot/learner/multihorizon.py`

- Source: [src/topo_pilot/learner/multihorizon.py](../../../../../../src/topo_pilot/learner/multihorizon.py)
- Kind: python
- Lines: 139

## Module docstring

> Direct joint heads for the next k symbols and the multi-horizon loss (D2A-FROZEN-v1 §4.3-4.5).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 18, via package root)
- `from .config import ModelConfig` -> [src/topo_pilot/learner/config.py](config.py.md) (line 20, via relative)
- `from .model import ModelOutput, TransformerLM` -> [src/topo_pilot/learner/model.py](model.py.md) (line 21, via relative)
- `from .trainer import lm_loss` -> [src/topo_pilot/learner/trainer.py](trainer.py.md) (line 22, via relative)

### External (third-party)

- `torch` (lines 15, 16)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 13)
- `io` (lines 11)
- `pickle` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/d2a/test_a_pad.py](../../../tests/d2a/test_a_pad.py.md) (line 18, import)
- [tests/learner/test_multihorizon.py](../../../tests/learner/test_multihorizon.py.md) (line 38, import)
- [tools/d2a/d2a_eval.py](../../../tools/d2a/d2a_eval.py.md) (line 18, import)
- [tools/d2a/d2a_train.py](../../../tools/d2a/d2a_train.py.md) (line 73, import)

## Top-level constants

- `_HORIZONS`

## Classes and functions

- **class `MultiHorizonOutput(ModelOutput)`** [L28-31] decorators: @dataclass(frozen=True) - ``ModelOutput`` plus ``joint_logits``: k -> ``[B, n_ctx, vocab_out**k]``.
- **class `MultiHorizonLM(TransformerLM)`** [L34-72] - ``TransformerLM`` trunk (same parameter creation, init and causality check) + joint heads.
- **method `MultiHorizonLM.__init__`** [L47-61]: `def __init__(self, cfg: ModelConfig, horizon: int, aux_seed: int)`
- **method `MultiHorizonLM.forward`** [L63-72]: `def forward(self, inputs: torch.Tensor, *, return_hooks=()) -> ModelOutput`
- **function `check_causal_joint`** [L76-94]: `def check_causal_joint(model: MultiHorizonLM, tol: float = 1e-06) -> None` decorators: @torch.no_grad() - Perturb one input position j (local generator, seed 0); joint logits at positions < j
- **function `joint_index`** [L97-103]: `def joint_index(y: torch.Tensor, k: int, V: int = 5) -> torch.Tensor` - ``u_k[:, p] = sum_{j<k} y[:, p+j] V^(k-1-j)`` for ``p = 0..n-k`` -> ``[B, n+1-k]``.
- **function `multi_horizon_loss`** [L106-115]: `def multi_horizon_loss(out: ModelOutput, y: torch.Tensor, horizon: int) -> torch.Tensor` - ``(1/H) sum_{k=1..H} (1/k) CE_k`` (§4.4); ``H = 1`` is exactly ``lm_loss``.
- **function `load_multi_horizon`** [L118-135]: `def load_multi_horizon(checkpoint, horizon: int) -> MultiHorizonLM` - Rebuild ``MultiHorizonLM`` (CPU, eval) from ``checkpoint.model_config`` and its weights,

