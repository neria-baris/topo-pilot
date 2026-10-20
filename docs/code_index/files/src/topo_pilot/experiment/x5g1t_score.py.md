# `src/topo_pilot/experiment/x5g1t_score.py`

- Source: [src/topo_pilot/experiment/x5g1t_score.py](../../../../../../src/topo_pilot/experiment/x5g1t_score.py)
- Kind: python
- Lines: 78

## Module docstring

> X5 G1 training-study scoring at p32 (x5g1-train contract §4): batched, float64, stable.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 15, via package root)

### External (third-party)

- `numpy` (lines 11, 13)
- `torch` (lines 12)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1_scorebench.py](x5g1_scorebench.py.md) (line 39, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 60, import)
- [tests/experiment/test_x5g1_scorebench_smoke.py](../../../tests/experiment/test_x5g1_scorebench_smoke.py.md) (line 9, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 28, import)

## Top-level constants

- `POSITION`
- `SCORE_BATCH`

## Classes and functions

- **function `p32_log_probs`** [L22-45]: `def p32_log_probs(model: torch.nn.Module, inputs: torch.Tensor, batch: int = SCORE_BATCH, guard: Callable[[str], None] | None = None) -> NDArray[np.float64]` decorators: @torch.no_grad() - ``log softmax(logits[:, 32, :])`` in float64, ``[R, V]``, computed ``batch`` rows at a time.
- **function `kl_from_log_probs`** [L48-71]: `def kl_from_log_probs(q: NDArray, logp: NDArray) -> NDArray[np.float64]` - Per-row ``KL(q || p) = sum_v q_v (log q_v - log p_v)`` with ``0 log 0 = 0`` (nats).
- **function `regret_rows`** [L74-78]: `def regret_rows(model: torch.nn.Module, inputs: torch.Tensor, q: NDArray, batch: int = SCORE_BATCH, guard: Callable[[str], None] | None = None) -> NDArray[np.float64]` - Per-history regret ``KL(q_C(h) || p_model(h))`` at p32, nats, ``[R]`` (guarded batches).

