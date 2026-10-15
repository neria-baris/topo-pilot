# Chart redesign: merged proposal for the owner's decision (no execution authorised)

**Coordinator:** Claude c351b245. **Date:** 2026-10-15, ~04:40Z. Tracks: X (Codex, 610 lines) and L (Claude). Both are STATUS: PROPOSAL.

## Agreed by both tracks independently (strong)
1. **What failed.** K4 failed in its frozen chart construction, not on circular structure or history dependence. The 1-skeleton at scale r is connected iff r ≥ ℓ_max, the longest MST edge, which equals the largest finite H0 death. Nothing in "the longest H1 bar, midpoint scale" guarantees r ≥ ℓ_max.
2. **E4's circular coordinates met the same issue and handled it silently** (verified by the coordinator in `src/topo_pilot/topology/circular.py`).
   - The construction is the same: ripser, F47, the selected bar, the midpoint scale.
   - It then uses a minimum-norm `lstsq`, so each off-giant component gets an independent constant offset; isolated points get phase 0.
   - The docstring documents this (line 33), so it is a **documented design choice, not a bug**. There is no integer-closure certificate and no primitive normalisation.
   - E4's agreement of 0.88–0.89 is a descriptive statistic over all points, including those constant-phase points. It does not overturn the published E4 claim, which was descriptive and representational. **Proposed:** a one-line methodological caveat in the README's "after E4" section, an owner decision because it touches published text.
3. **Diagnostic first.** It covers geometry only, with no phases, labels, lift, oracle or endpoint:
   - the selected bar (b, d) and the midpoint r;
   - ℓ_max (the H0 deaths);
   - component sizes and the giant fraction;
   - nearest-neighbour distances of the excluded points.

   It costs about 1 CPU-minute and adds almost no exposure, since E4 S7 already ran the same persistent homology.
4. **K4 stays closed INCONCLUSIVE** (no rescue, B3-A). Any redesigned result on E4 histories is exploratory. Confirmation needs fresh histories with the chart and the evaluation rule frozen beforehand.
5. **C1 needs an explicit successor protocol.** Its current freeze is blocked by §14.

## Conflict: which redesign rule
| | X (Codex) | L (Claude) |
|---|---|---|
| Rule | Keep all landmarks. Choose one deterministic scale inside [ℓ_max, d), the intersection of the bar's lifetime and the connected regime. Stop if it is empty. | Largest connected component at the frozen scale, gated at ≥ 95% of landmarks. Identical to the frozen rule when the graph is connected. |
| Against the other | Rejects automatic component trimming as fitting the method to the failure. | One outlier sets the scale for the whole chart, and the rule fails outright when ℓ_max ≥ d. Larger r can make the edge/triangle counts exceed the CPU/wall limits. |

**Coordinator recommendation:** **L's rule (a), with the 95% gate, as primary, with X's rule reported descriptively.**
- (a) changes nothing when the graph is connected, so it is the minimal deviation from the reviewed method.
- It is robust to a handful of outliers.
- It needs only one new number, 0.95, which reuses C1's existing 5% allowance.
- X's objection is answered by fixing the rule and gate **before** the diagnostic. Trimming is then not adaptive: the rule and the 95% threshold are pre-declared.
- X's interval rule [ℓ_max, d) is computed and reported by the diagnostic as a comparison only.

## Decision tree for the owner
1. **Approve diagnostics only.** The coordinator then dispatches the geometry-only diagnostic job, for all three models on panels 1–2, with a mechanical reading rule frozen before it runs.
2. **Diagnostic outcome.** GO if, in all six model × panel cases, the giant component holds ≥ 95% of landmarks and the selected bar is the one E4 used. Otherwise STOP the chart route. In that case priorities 1 and 2 need a different approach, and the coordinator plans alternatives.
3. **On GO, approve a C1 successor ("C1′").**
   - A protocol delta: the chart is the 95% largest component, built once on **C1's own fresh calibration/validation histories**, not on E4 panels.
   - It goes through a Codex review and freeze, then implementation and the C1 stages.
   - **Expected chance of reaching a C1 verdict** (L's planning estimate, not a measurement): 15–25%.
4. **K4.** Stays closed. A K4b on fresh histories is optional and runs only if the owner opts in. L judges it not worth it for priority 1, and suggests a later fresh-history profile instead.

## Owner questions
- (i) Approve the diagnostic? (Recommended: yes. It is cheap, adds no exposure and decides GO/STOP.)
- (ii) Approve L's rule (a), with the 95% gate, as the pre-declared redesign rule?
- (iii) Pursue C1′ on GO, given a 15–25% expected chance of a verdict? Or stop priority 2 on this route?
- (iv) Add the methodological caveat on E4's circular coordinates to the README's "after E4" section?
