# Preregistration X4: representation geometry vs readout geometry (secondary; no training)

Status: SECONDARY analyses. F1, H2, H3, and H4 and their rules in PREREGISTRATION.md are unchanged and remain primary.
Blinding: Blind to owner and to the planning conductor; a prior conductor session that ended before this plan may have seen S4 console output; no repo changes after the S4 analysis (last commit a4f7844, 11:50).
Data: the stored ActivationSets of every S4 run (and, later, S5 runs) at checkpoints 0 and 5000, all 8 panels (512 histories at p = 32), plus each run's checkpoint-5000 and checkpoint-0 weights (final LN γ, β and W_U only). No new training, no new extraction.

## Views (each is a point cloud over the same history_ids)
- V0: resid_post_3, raw Euclidean (= the primary metric; reference, recomputed only if not stored).
- V1: LN-gauge-free u = (z − mean(z)·1)/sqrt(var(z)+1e-5), Euclidean.
- V2: ln_final_out, Euclidean (includes γ, β). If S6's layer sweep has already computed the F1 contrast for this hook on 8 panels at 0/5000, reuse those numbers instead of recomputing.
- V3: readout-visible part of V1: P_A u, where P_A is the orthogonal projector onto range(A), A = diag(γ) W_U^T, using the weights of the same checkpoint as the activations.
- V4: readout-null part of V1: u − P_A u.
- V5: predictive geometry: Hellinger distance between softmax(logits) rows.
At checkpoint 0 the projector uses the checkpoint-0 weights, so the F1 contrast "final − init" compares each view with itself.

## Measures (identical definitions to PREREGISTRATION.md)
S (max finite H1 persistence / q95 of positive distances); per replicate r and panel i, D_{r,i} = (S^cyl_final − S^cyl_init) − (S^sq_final − S^sq_init); u_r as in §7.4; the F1 rule applied per view gives a per-view verdict (SUPPORTED / REJECTED / INCONCLUSIVE), reported as "F1-rule under view Vk" and never replacing F1.
Δgeom per view (vs b32 and b1, as in §7.5).
Positive control: ρ_s(d_V5, d_future1) on all pairs per panel (oracle q at p = 32).

## Pre-registered expectations and interpretation
X4-a (gauge robustness): the verdict under V1 equals the verdict under V0. If V0 is supported but V1 is not, the primary signal lives in readout-invisible gauge directions: report it as a caveat on F1, not as a refutation.
X4-b (functional geometry): under O, the verdict under V5 is SUPPORTED (expected because oracle future1 separates the worlds 8/8 and the models pass the learning gate). Positive control: median over panels of ρ_s(d_V5, d_future1) ≥ 0.9 in every replicate; if the control fails, X4-b is INCONCLUSIVE (pipeline or model issue).
X4-c (where the structure lives): two-sided, descriptive. Report median_i D under V3 and under V4, and their ratio, per replicate. Interpretation fixed in advance:
  V3 supported, V4 not → the cylinder signal sits in the readout-visible subspace (structure used by the output map);
  V4 supported, V3 not → structure is present but invisible to next-token prediction (representation ≠ computation);
  both / neither → reported as such.
X4-d (same-last-symbol H2 baseline): within pairs with equal w32, compare ρ_s(d_A, d_B32) for the model (V0 and V1) against R2 and R3 (R1 is constant on these pairs and excluded). Supported iff the model value exceeds max(R2, R3) in all 3 replicates and ≥ 7/8 panels.
H3′ (requires owner approval at checkpoint H3; until approved, report only as descriptive): under P, at checkpoint 5000, ρ_s(d_A, d_B32) on all pairs (A = V0 and, separately, V1) exceeds both its checkpoint-0 value and max(R2, R3) in all 3 replicates and ≥ 7/8 panels. Under O the same measure is reported for comparison. H3 as registered stays one-sided.

## Units and statistics
The replicate (training run) is the unit; panels are within-run resampling; pairs are never tests. No p-values over pairs or tokens. Statuses (collapsed/censored/inconclusive) propagate; null never means 0.

## Cost
Pure re-analysis: about (5 views × 7 runs × 2 checkpoints × 8 panels) Ripser calls of 512 points for S4, the same again for S5. Minutes to an hour on CPU.

## Approval

Owner approval: PREREGISTRATION_X4.md approved by the repository owner, 2026-10-13; H3′ approved at checkpoint H3 (2026-10-13), so it is a decision rule, not descriptive only. Approved while still blind (no S4 analysis numbers seen).
