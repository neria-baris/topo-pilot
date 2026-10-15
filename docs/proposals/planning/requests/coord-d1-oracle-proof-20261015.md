# Planning request: D-1, an oracle-only proof and check of a horizon-dependent topological distinction

From: Claude coordinator c351b245. Authority: archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md, part B3 item D ("mathematical/oracle-only: does a process exist in which a topological distinction is unnecessary for the next symbol but necessary for a longer horizon, with the gap proven by construction"; do not reopen B2 / D-055).
Charter: NEXT_RESEARCH_AND_WORKFLOW.md, "Owner research charter", priority 3.
Prior round: planning/responses/coord-c1-freeze-readiness-20261014.MERGE.md, section "D decision". Both D sketches in round 1 (`.codex.md` and `.claude.md` §17) and the analyst's assessment (`.MERGE_ANALYSIS.md` §7) are shared inputs.

## Task

Produce a complete, checkable protocol for **D-1: cylinder versus Möbius with a seam band**.
- Inside the band, emissions reveal x exactly and say nothing about y.
- Because the lazy walk moves at most one cell per step, the next-symbol predictive distributions are provably identical in both worlds for histories ending in the band.
- The two-step (or k-step) prediction differs.

Required:
1. **Exact construction.**
   - Lattice size, band width, emission rows inside and outside the band, and the alphabet.
   - Emission rows outside the band must be **identical in both worlds by construction**. Supply them as an explicit array, not from `point_distances`, which ignores the flipped gluing.
   - Formulate it as **one process with a hidden world bit**, so the "topological distinction" is the posterior over that bit.
2. **Theorem and proof.**
   - For the stated history class, P(w_{t+1} | h, world) is independent of the world bit; that is, horizon-1 insufficiency of the distinction.
   - The horizon-k distribution depends on it for some reachable h, with an explicit lower bound on the difference (TV or KL).
   - State the reachable decision phase precisely, using X's sufficiency lemma from round 1.
   - Address the edge cases: band entry, the lazy stay probability, and boundary rows of the non-glued y axis.
3. **Oracle-only verification plan.**
   - Exact Bayesian computations with the existing oracle kernels (`src/topo_pilot/oracle`, BayesFilter / FutureOperator). Reuse unchanged where possible, state the minimal new code, and give a six-field reuse assessment.
   - Numerical tolerances, an exact or Decimal cross-check, the cost estimate, and the PASS/FAIL criteria of the check itself.
   - No training and no model.
4. **What a PASS licenses for the downstream programme** (a later trained-model test). What would have to be added there (not now)? Also state honestly what this construction does **not** say about the original cylinder/square pilot.
5. **Risks:** identifiability, the reachability probability of band histories, and any degeneracy (for example, the world bit becomes identifiable from outside-band statistics, which would trivialise the horizon gap). Give a mitigation for each.

Be rigorous. Prefer the simplest construction that makes the theorem exact.

Deliverable format: `STATUS: FREEZE_READY | DRAFT | BLOCKED`, then a summary of at most 300 words, then the full protocol, then open questions.
