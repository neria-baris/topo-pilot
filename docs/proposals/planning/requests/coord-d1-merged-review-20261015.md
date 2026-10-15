# Planning request: independent review of D1-MERGED-v1

From: Claude coordinator c351b245. This is a result-blind independent review before freeze; owner policy part D makes Codex the first reviewer. Nothing has been executed.

Document: `X:/Downloads/projects/topo-pilot/agent-handoff/planning/responses/D1-MERGED-v1.md`, sha256 A1E0779F06EB59B6193B0C26E2F32648B28A5C54E0260D4523FA9B237453C083.

Context:
- request `requests/coord-d1-oracle-proof-20261015.md`;
- decisions `responses/coord-d1-oracle-proof-20261015.MERGE.md`;
- analysis `.MERGE_ANALYSIS.md`;
- sources `.codex.md` (your own round-2 track) and `.claude.md`.

Code: main @4f219d6 in `X:/Downloads/projects/topo-pilot/topo-pilot`.

## Review tasks
1. **Re-derive independently the decision-phase gap conjecture** (§3f): joint TV = (a²/2)·max(|δ_C|, |δ_M|) and marginal TV = (a²/2)·|δ_C|. Prove it or give a counterexample.
2. **Re-derive every value marked [W]:**
   - the enumeration counts per length, with 37,190 total and 5,348 ending in σ3;
   - the decision-phase probability formula;
   - the start-law artefact for t = 6–8;
   - the h_edge posterior and probability;
   - h_max;
   - the 2/3 shrinkage per in-band step.
3. **Check the proofs and gates:**
   - the proofs of theorems (a)–(e);
   - the surface and orientability certificate (boundary components, orientation cocycle, GF(3) ranks 7 vs 8);
   - gates G0–G6 and stop rules S0–S7;
   - tolerances;
   - controls.
4. **Check the code facts,** in particular `validate_process` (it enforces a stationary start law), the Decimal reference location, and the reuse of BayesFilter/FutureOperator with a fixed start law.
5. **Licence:** does any claim exceed an orientability existence result?

## Deliverable
- **First line:** `VERDICT: APPROVE_FOR_FREEZE | APPROVE_WITH_REQUIRED_CHANGES | REJECT`.
- **Then:** numbered required changes, each with a section reference and the exact replacement text or values.
- **Then:** the re-derivations, showing your work concisely.
- **Then:** optional suggestions.
