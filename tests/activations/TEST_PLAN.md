# TEST_PLAN: activations

Marker: `pytest.mark.activations`. Tiny model on CPU. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| A01 | Row order equals `HistoryIndex` order for batch sizes 1, 7, and 256 (identical arrays) | contract |
| A02 | Extracted logits equal the plain forward logits at position 32 (1e-5) | known answer |
| A03 | Changing token w₃₃ (not visible at position 32) leaves the activations unchanged; changing w₃₂ changes them | contract |
| A04 | An unknown hook raises `UNKNOWN_HOOK`; a corrupted `tokens_hash` raises `ALIGNMENT_ERROR` | error path |
| A05 | Panels filter: requesting panel 1 returns exactly its 512 ids | contract |
| A06 | Static: no forbidden imports; loading a sidecar via the stage raises `LEAKAGE` | contract |
