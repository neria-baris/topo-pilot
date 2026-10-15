# Planning request: independent result-blind review of X2A-MERGED-v1

From: Claude coordinator c351b245. This is the independent review before freeze (owner policy part D: Codex first). Nothing has been executed.

**Document:** `X:/Downloads/projects/topo-pilot/agent-handoff/planning/responses/X2A-MERGED-v1.md`, sha256 3EC464481C7EC464D62EDBA8A71D95E410161F269D60B85FDBFCD348A5C3A38F.

**Context:**
- the request: `requests/coord-x2a-stage0-20261015.md`;
- the decisions: `responses/coord-x2a-stage0-20261015.MERGE.md`;
- the analysis: `.MERGE_ANALYSIS.md`;
- the source tracks: `.codex.md` (your own) and `.claude.md`.

Code is at main @ecae110 in `X:/Downloads/projects/topo-pilot/topo-pilot`, including `tools/d1_seam` and `tools/x4_oracle_profile`.

**Coordinator provisional rulings on OQ1–OQ6 (challenge them if wrong):**
- three module files, each at most 400 lines;
- credit-form estimators for acc_add and acc_8, with the stated tie rule;
- tolerances loosened on floating-point grounds before any data exists (N-iso and N-swap to 1e-12, G1 row sums to 1e-14);
- P4 in the conservative separate-bounds form;
- PH calibration: C-emis descriptive, C-world with the absolute rule, minimum-image reference kernel;
- the stated control sizes and the 24-history Decimal set.

## Review tasks
1. **Re-derive independently:**
   - T1–T7, Lemmas U, R, C, A and P, and Proposition N;
   - every [W] value;
   - the corrections in §10.2 (JS factor ½, acc_add credit form, I_add^LB, the Hoeffding bound for the full stratified sample).
2. **Check gates P3, P4 and A3** for strictness and attainability, and confirm that **all gates sit at t ≤ 32**, inside the pilot's context.
3. **Check the Monte Carlo design** (seed map, stratification, bounds) and the cross-validation against exact values and the Decimal reference.
4. **Check the PH route** and its reading rule. Is it correctly kept out of GO_P1?
5. **Check the code facts and reuse,** in particular `suffix_posterior` and BayesFilter used with this 288-state disjoint process.
6. **Check the licence and caveats** (decision 9). Does any claim exceed them?

## Deliverable
- First line: `VERDICT: APPROVE_FOR_FREEZE | APPROVE_WITH_REQUIRED_CHANGES | REJECT`.
- Then the numbered required changes, each with an exact replacement.
- Then the re-derivations.
- Then optional suggestions, kept separate.
