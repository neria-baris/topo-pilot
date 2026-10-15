# CHART-DIAG-FROZEN-v1: geometry-only chart diagnostic, with its reading rule fixed before execution

**Coordinator:** c351b245. **Date:** 2026-10-15, ~06:25Z.
**Authority:** owner decision A1 (archive/owner-decisions-20261015/OWNER_DECISIONS.md, sha 5BD1FDB0…37CD) and the merged proposal coord-chart-redesign-20261015.MERGE.md.

## Scope
- **Cases:** the three E4 cylinder-O models 1729, 2718 and 3141 at step 5000, hook resid_post_3, position p32. Panels **1 (calibration) and 2 (validation)**: 512 histories each, so 6 cases.
- **Allowed:** geometry only.
- **Not allowed:** phases, cocycle lift, primitive normalisation, gauge, oracle, latent labels, endpoints, any alternative chart, and any access to panels 3–8 beyond the identity-only joins already permitted in K4.

## Computation (identical to the frozen K4 chart up to bar selection; reuse its functions unchanged)
For each case:
1. Order the 512 raw 128-d vectors by history ID, as K4 does.
2. Compute Euclidean distances and ripser with maxdim 1 over F47, exactly as `tools/x4_circle_history/chart.py` does.
3. Select the largest finite positive H1 bar (b, d) by K4's tie rule, and take the midpoint r = (b+d)/2.

Report:
- (b, d, r) and the number of finite H1 bars;
- ℓ_max, the largest finite H0 death (the longest MST edge);
- the components of the 1-skeleton at scale r: count and sorted sizes;
- the **giant fraction** f = |largest component| / 512;
- for points outside the giant component: their nearest-neighbour distance, their rank by vector norm (1 = largest), and their history IDs;
- **X's interval** [ℓ_max, d): whether it is empty, and its length. **This is descriptive only.**

## Reading rule (mechanical; fixed now)
- **GO** if f ≥ 0.95 in **all 6** cases. **STOP** otherwise.
- **INVALID** on any computational or integrity failure. ripser output must match K4's code path exactly for case (1729, panel 1): the selected (b, d) must reproduce the job-0018 computation, if it is recoverable from the frozen operations log; otherwise this is reported as not checkable.
- **On GO:** the C1′ protocol delta proceeds (owner A3). The chart is built once, by the LCC ≥ 95% rule, on **C1's own fresh** calibration and validation histories, not on E4 panels.
- **On STOP:** the chart route ends for K4 and C1. The coordinator plans alternatives.
- **K4 stays closed INCONCLUSIVE in every case** (no rescue).

## Exposure
Same activations and the same PH as E4 S7 and K4 job 0018. This adds no new label exposure and no fitting.
