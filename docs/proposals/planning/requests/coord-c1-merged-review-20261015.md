# Planning request: independent result-blind review of C1-MERGED-v1

From: Claude coordinator c351b245. Per the owner's policy (part D), a merged protocol needs an independent, result-blind review before freeze, with Codex as the first reviewer. No C1 data exists; nothing has been executed.

**Document under review:** `X:/Downloads/projects/topo-pilot/agent-handoff/planning/responses/C1-MERGED-v1.md`, sha256 72C86FFC0C76386EBD1FF6D991D0AB2DE62684FB2334831628A9D3DCCB0745D7.

**Context, readable:** the request it answers is `requests/coord-c1-freeze-readiness-20261014.md`. The merge decisions are in `responses/coord-c1-freeze-readiness-20261014.MERGE.md` and `.MERGE_ANALYSIS.md`. The two source plans are `.codex.md` (your own round-1 track) and `.claude.md`. Code: `X:/Downloads/projects/topo-pilot/topo-pilot` (main @4f219d6).

## Review tasks
1. **Correctness.** Check every formula: donors, q±, G, the FWL map, Haar frames, A, Y, θ, Z, the bootstrap, and the precision use of `precision.py`. Check identifiability, and the claim that θ = 1 for an oracle-perfect readout. Check what cancels exactly and what does not.
2. **Leakage and selection.** Is anything chosen on validation or fresh data, other than the pre-declared ladder? Is the exposure registry sound?
3. **Attainability.** Could any gate plausibly force INCONCLUSIVE regardless of the science? Look at fraction thresholds, tolerances and the positive control. Verify the stated code-reuse facts against the actual code (§18, and corrections C-9 to C-18).
4. **Specific choices:** the §20 parameters, the margin 0.10, the PASS/FAIL asymmetry, whether a near-placebo random family meets owner B3-C (MERGE.md ruling 1), and the numerical certificate constants (2^-44, η = 1e-12, floor 1e-9).
5. **Claims.** Does any section license more than the design supports?

## Deliverable
- **First line:** `VERDICT: APPROVE_FOR_FREEZE | APPROVE_WITH_REQUIRED_CHANGES | REJECT`.
- **Then:** a numbered list of required changes, each with a section reference and the exact replacement text or values.
- **Then:** optional suggestions, kept separate.
- **Then:** a statement of what you verified in code.

Be strict, but do not redesign without cause.
