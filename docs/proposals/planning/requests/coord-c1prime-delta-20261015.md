# Planning request: the C1′ protocol delta (C1-FROZEN-v1 with the new chart rule, on fresh histories)

From: Claude coordinator c351b245.
**Authority:** owner decisions A2 and A3 (archive/owner-decisions-20261015/OWNER_DECISIONS.md, sha 5BD1FDB0…37CD).
- New chart rule: the largest connected component, gated at ≥ 95% of landmarks.
- C1′ proceeds on a diagnostic GO.

The diagnostic is **GO** (job 0023): the minimum giant fraction is 0.998 across the 3 models × panels 1–2. The only disconnections are single isolated points (the smallest-norm vector) in 1729/p1 and 3141/p1.

## Inputs
- `planning/responses/C1-FROZEN-v1.md` (D1DF1AEF…5DBA), whose §14 is the chart dependency;
- `planning/responses/coord-chart-redesign-20261015.MERGE.md` and the two chart tracks;
- `jobs/0023/report.md` and `review.md`;
- the K4 chart code: `tools/x4_circle_history/chart.py` and `cochain.py` at main @ef2f781;
- `tools/chart_diag/chart_diag.py`.

## Task
Write the **minimal, exact delta** that turns C1-FROZEN-v1 into **C1′-v1**. Everything not named in the delta stays frozen.
1. **§14 chart rule.**
   - Build the chart **once**, by the frozen K4 construction restricted to the **largest connected component** at the midpoint scale of the selected bar.
   - Gate: the giant fraction is ≥ 0.95.
   - Excluded points get no chart phase. State exactly how they are treated downstream: excluded from donors and sources, or extension only.
   - The chart is built on **C1's own fresh calibration histories**, not E4 panels. Validation uses C1's fresh validation histories.
   - Which K4 gates carry over: lift certificate, primitive normalisation on the component, gauge, fidelity, bins, resultant, support. State their thresholds unchanged, and say where the giant-component restriction enters.
2. **Support gates.** The chart-redesign Claude track proposed requiring ≥ 507/512 supported validation rows instead of every row (C1's own 0.99 support level). Decide whether to adopt it, with justification. Keep it attainable; no every-row traps.
3. **Exposure and freshness.** Fresh histories are new draws, never exposed, using C1's exposure registry and its seed map. Specify how the chart-construction histories relate to C1's calibration split.
4. **What changes elsewhere,** in exact section references and replacement text:
   - the stop rules;
   - the gate table;
   - the licence ("chart built by the LCC ≥ 95% rule; operational");
   - the cost.
5. **Consistency with the numerical certificate** (§15.3). Confirm it is unaffected, or state the change.
6. **A K4b note:** describe K4b only as optional, needing a separate owner opt-in. It is not part of C1′.

Deliverable: `STATUS: FREEZE_READY | DRAFT`, then a summary of at most 250 words, then the delta as numbered, exact edits against C1-FROZEN-v1 (section → replacement text), then open questions. Keep it minimal.
