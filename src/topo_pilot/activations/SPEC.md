# SPEC: `activations` (wave W3)

## Purpose

Deterministic, gradient-free extraction of the hook activations and logits for the fixed analysis histories, from a saved checkpoint.

## Public API

```python
class ActivationExtractor:
    def __init__(self, hooks: Sequence[str], batch_size: int = 256, device: str = "auto"): ...
    def extract(self, model: TransformerLM, obs_test: ObservationSet, index: HistoryIndex,
                panels: Sequence[int] | None = None) -> tuple[np.ndarray, np.ndarray, list[str]]:
        """Returns A [M, K, d] float32 at position index.end (=32), logits [M, V] float32,
           history_ids in index order."""

class ActivationStage:   # I/O, consumer "activations"
    def run(self, checkpoint_id: str, obs_test_id: str, history_index_id: str,
            hooks: Sequence[str], panels: Sequence[int] | None, store) -> str: ...  # ActivationSet id
```

## Logic requirements

- Use `eval()` and `torch.no_grad()`.
- Build inputs with `SequenceLayout.model_inputs` and take position `end` (= 32), whose history is w₁..w₃₂. The logits at that position predict w₃₃.
- Row order must equal `HistoryIndex` order, whatever the batching. Re-sort explicitly by an index map.
- Never average, pool, or join with latent information. Joins with beliefs happen later in `analysis`, by `history_id`.
- **Storage:** checkpoint 0 and checkpoint 5000 are extracted for all 8 panels, and the other checkpoints for panel 1 only. The stage config decides this, not this module.

## Invariants and errors

| Condition | Error |
|---|---|
| unknown hook | `UNKNOWN_HOOK` |
| the input digest of a row disagrees with `HistoryIndex.tokens_hash` | `ALIGNMENT_ERROR` |
| logits from extraction differ from a plain forward pass (> 1e-5) | `NUMERICAL_FAILURE` |
| any privileged artifact access | `LEAKAGE` |

## Dependencies and forbidden information

`contracts`, torch, and `learner.load_model` / `learner.TransformerLM` (public). **Must not import** `world`, `process`, `oracle`, `analysis`, or `prediction`. Must not load the sidecar.

## Done when

The TEST_PLAN passes. The README states the position convention with a worked example.
