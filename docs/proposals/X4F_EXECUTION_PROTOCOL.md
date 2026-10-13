# X4-F execution protocol (x4f-exec-v1)

14 October 2026. Branch `x4f-execution-contract`, from `x4f-planning` at 6eccd59. Handoff job 0001.

**Status: prepared for coordinator review.** This contract becomes frozen only when the coordinator records ACCEPT for job 0001. Until then nothing real-data is executed. After ACCEPT, any change needs a new job, a version bump and a DECISIONS line before any real-data use.

This document supersedes [x4f-draft-1](X4F_COORDINATE_CAUSAL_PROTOCOL_DRAFT.md) for execution purposes. The draft itself stays unchanged. The base is [X4_CAUSAL.md](X4_CAUSAL.md), Short experiment F. Section 11 lists every change from draft-1.

**No scientific computation was performed** in preparing this contract: no sampling, fitting, extraction, PH, intervention or training.

## 1. Fixed scientific frame (not open for revision here)

* **Hypothesis H4C-F.** In each of the three frozen step-5000 cylinder-O models (seeds 1729, 2718, 3141; σ 1.25; original T/E/π), erasing the m32 target at `resid_post_1`, position 32, raises oracle-relative one-step regret. The rise must exceed the mean rise from matched random erasure by **≥ 0.01 nat**. Uncertainty comes from a paired bootstrap over canonical trajectories, resampled jointly across models.
* **What a positive result would mean.** It would show coordinate-associated information use. It would not show H1 necessity, a topology-specific effect or long memory. Erasure is information removal (X4_CAUSAL manipulation type B).
* **Branches that stay as recorded:**
  - the practical Q2-gap branch stays closed (D-055);
  - Phase B INCONCLUSIVE, B2 NO-GO, H4C-I NOT RUN, strict sufficiency UNRESOLVED;
  - E4 accepted with G-H FAIL.
* **Units.** The model is the replication unit and the trajectory the uncertainty unit. Panels and pairs are never replicates.

## 2. Definitions

**Inputs and site.**

* Model inputs follow `SequenceLayout.model_inputs`: `[BOS = V, w1, …, w32]`, 33 positions, indices 0–32.
* History position p = 32 is input index 32 (input token w32). Its logits predict w33.

**Representations** (h at index 32):

* h is the output of `blocks[1]`, i.e. `resid_post_1`.
* z3 is the output of `blocks[3]`, i.e. `resid_post_3`.
* u = (z3 − mean(z3)) / sqrt(var(z3) + 1e-5), using the population variance (ddof 0), as in `torch.nn.LayerNorm`.
* y = u·diag(γ) + β is `ln_final_out`.
* logits = y·W_Uᵀ.

**Targets** (oracle-computed in experiment/analysis, never given to the learner):

* x angle of state z: θ_z = 2π·x_z/12.
* m(b) = Σ_z b_z (cos θ_z, sin θ_z), a vector in R².
* **m32** = m(b32), where b32 is the exact `BayesFilter(T, E, π)` posterior after w1..w32. **Primary.**
* **m2** = m(b2), where b2 = `BayesFilter(T, E, π).run(w31, w32)` at its last step, i.e. the posterior given only (w31, w32) with initial law π, the stationary and initial law of this process.
* **m1** = m(r_{w32}), using the existing `LastSymbolPosterior`.
* **r2** = m32 − m2. **Secondary only.**
* **y-target** = E_{b32}[y_z]/11, rank 1.
* **Local position** = b32·N, with N the fixed radius-1 neighbourhood-incidence matrix of the 12×12 cylinder (self included). The target is its 2 leading calibration principal components.
* **R1 target** = the 2 leading calibration principal components of one-hot(w32).
* **Generic predictive target** = the 2 leading calibration principal components of oracle Q1 = b32·T·E.

**Effect measure.**

ΔR(I) = mean_h [ KL(Q1(h) ‖ p_I(h)) − KL(Q1(h) ‖ p(h)) ], in **nats**, computed over full softmax distributions.

## 3. Data roles

Every model has its own existing dev pool (S7 dev HistoryIndex: 4,096 histories, panels 1–8).

| Role | Panels | Use |
|---|---|---|
| Calibration | 1–6 (3,072) | inner tuning (leave-one-panel-out over panels 1–6); final refit of every probe, eraser, control, standardisation and support statistic |
| Outer validation | 7–8 (1,024) | gates G1–G5 only; **never** used to choose λ, bandwidth, rank, eraser or random seeds |
| Fresh causal test | new lineage, later job | single H4C-F evaluation; not part of the first execution task |

## 4. Recoverability (G1) — nested selection

**Probe.** Affine ridge with an unpenalised intercept, using the existing `RidgeProbe` semantics. Features are standardised with statistics of the fitting rows only; constant columns pass unscaled.

**Pipeline** (identical for every target, feature set and control):

1. **Inner selection.** Leave-one-panel-out over calibration panels 1–6: 6 folds, each fitting on 5 panels and scoring the held-out panel. λ is chosen from {1e-3, 1e-2, 1e-1, 1, 10} by mean inner-fold MSE. Ties go to the larger λ.
2. **Refit.** Refit on all 3,072 calibration rows with the chosen λ.
3. **Score.** Score once on outer validation (panels 7–8).

**Score.**

* Out-of-sample R² = 1 − SSE_val / SST_val.
* SST is taken around the **calibration** target mean. Both are pooled over the target's coordinates; for 2-D targets this is equivalent to variance weighting.
* Values can be negative. They are reported as computed.

**Shuffled controls.** 20 per (model, target).

* Calibration target rows are permuted jointly across coordinates, with stream `SeedTree(0).generator("x4f-v1", "shuffle", target, seed, k)`.
* The **same** inner selection and refit pipeline runs on the permuted calibration targets.
* Scoring uses the unpermuted validation targets.
* The control value is the q95 of the 20 scores.

**RBF residual probe (used in G3).**

* 2,048 random Fourier features: φ(x) = sqrt(2/2048)·cos(x̃Ω + b).
* x̃ is x standardised on calibration.
* Ω ~ N(0, 1/ℓ²), b ~ U[0, 2π), stream `("x4f-v1", "rbf", seed)`.
* ℓ = the median pairwise Euclidean distance among 1,024 calibration rows, drawn with stream `("x4f-v1", "rbf_bandwidth", seed)`.
* Then the same ridge pipeline; λ is chosen on inner folds only.
* For erased features, ℓ and the standardisation are recomputed on the erased calibration rows.

**G1 criteria** (frozen, per model; all three models must pass):

* **G1-primary.** R²_val(h → m32) ≥ **0.50**, and above the shuffled q95.
* **G1-r2.** This sub-gate decides only whether the secondary r2 analysis runs.
  1. **Low-variance check first.** If trace Var_cal(r2) < **0.01** × trace Var_cal(m32), or trace Var_cal(r2) < **1e-6**, the status is `R2_DROPPED_LOW_VARIANCE`. The r2 analyses are not run, and this is not a failure of G1-primary.
  2. **Otherwise.** R²_val(h → r2) ≥ **0.10**, and above the shuffled q95.
  3. **If either part fails,** the status is `R2_NOT_RECOVERABLE`. The r2 eraser is dropped and reported, and the primary continues.

**Short-context comparators** (descriptive, kept distinct):

* **(a) Fit-free direct.** m2 used directly as the prediction of m32: R²_val = 1 − Σ‖m32 − m2‖² / SST_val. No fitting.
* **(b) Fitted affine.** Ridge m2 → m32 through the same pipeline.
* **(c) Fitted affine with h.** Ridge [m2, h] → m32 through the same pipeline.
* **Reported.** R²(h → m32) minus (a), and minus (b); and (c) minus (b). None of these is a gate; r2 recoverability is the gate.

**Also reported, descriptive:**

* the same G1 probes at `embed` and `resid_post_3`, and on step-0 dev activations when available — the step-0 checkpoints must be in the approved extraction;
* the m1 comparators analogous to (a) and (b).

## 5. Erasers (fitted on calibration only)

**Continuous-target oblique LEACE.** For features X (rows x) and target Z on calibration:

1. **Centre.** μ = mean(X); Σ_xx = Cov(X); Σ_xz = Cov(X, Z).
2. **Whiten.** W = Σ_xx^{−1/2} via eigendecomposition. Eigenvalues ≤ **1e-10** × λ_max are dropped from both W and W⁺ (the pseudo-inverse square root). The number kept is recorded.
3. **Project.** P = the orthogonal projector onto the column space of W·Σ_xz. Its rank is the number of singular values > **1e-8** × σ_max.
4. **Erase.** x′ = x − W⁺·P·W·(x − μ).
5. **Exactness check.** The calibration cross-covariance Cov(X′, Z) must have max |·| ≤ **1e-8** × max |Σ_xz|. A failure is a G3 failure.

**Erasers fitted per model.** Each is rank ≤ the target dimension, with the rank recorded:

* **Primary:** m32.
* **Controls:** shuffled-target m32 (permuted calibration rows, stream `("x4f-v1", "shuffle_eraser", seed)`); R1 target; m2 (short context); r2 (only if G1-r2 passed); local position; generic predictive.
* **Rank-1 pair:**
  - **circle-PC1** — target m32·v1, where v1 is the leading eigenvector of Cov_cal(m32);
  - **y** — the y-target.

**Final effective-null (exact control).**

* Computed from the same checkpoint's γ, β and W_U (V×d).
* C = I − 11ᵀ/V. P_eff = `analysis.readout_projector(γ, C·W_U)`, the projector onto range(A·C) with A = diag(γ)·W_Uᵀ.
* Using u from z3: u′ = u·P_eff, then y′ = u′·diag(γ) + β. y′ replaces `ln_final_out` at index 32 and goes directly to W_U.
* The u-space projector is **never** applied to y, and **no** second LayerNorm is applied.

**Rules.** Dose α = 1.0 only in this execution: full erasure. Doses are partial erasures x′ = x − α·W⁺PW(x − μ). No eraser is renormalised.

## 6. Random matched erasers

**Families.** Per model and per rank r ∈ {2 (matched to the m32 eraser), 1 (matched to circle-PC1)}.

**Draw.** Each candidate uses stream `SeedTree(0).generator("x4f-v1", "random_eraser", r, seed, draw_index)`:

1. Draw a d×r Gaussian matrix in the whitened space and orthonormalise it by QR, giving Q.
2. Set P = Q·Qᵀ.
3. Erase with the same formula x′ = x − W⁺·P·W·(x − μ).

**Acceptance.**

* Displacement is measured in raw resid_post_1 units on calibration: d_i = ‖x′_i − x_i‖₂.
* A candidate is accepted iff |mean_i d_i(random) − mean_i d_i(target)| ≤ **0.05** × mean_i d_i(target).
* Drawing continues until **20** are accepted or **10,000** draws are reached. The accepted draw indices are frozen.

**Deviation from X4_CAUSAL, stated explicitly.** X4_CAUSAL specifies per-history L2 displacement within 5%. A fixed linear eraser cannot match another fixed linear eraser history by history; that would require history-dependent rescaling, which would change the control into a nonlinear, target-dependent map. This contract therefore matches the **calibration mean** (within 5%) and does not assume per-history equality. Reported on validation, per family:

* the q10, q50 and q90 of d_i;
* the per-history mismatch |d_i(rand) − d_i(target)| / d_i(target), at its median and q90.

**Interpretation.** Equal rank and matched mean displacement do **not** imply equal damage to predictive information. Damage is measured separately (§8).

## 7. Frozen-forward adapter semantics (learner; module change subject to review)

```python
def forward_with_patch(model, inputs, site, index, replacement) -> PatchedOutput
```

**Arguments.**

* `inputs`: int64 [R, 33], from `SequenceLayout.model_inputs`, with BOS at index 0.
* `site` ∈ {"resid_post_k" for 0 ≤ k < n_layers, "ln_final_out"}.
* `index`: an input index in 0..32.
* `replacement`: float [R, d].

**Returns.** Full logits [R, 33, V] for **all** positions, plus requested hooks. Tests can therefore check every position.

**Semantics.**

* **At resid_post_k:** compute embed → blocks[0..k]; set x[:, index, :] = replacement; continue blocks[k+1..], then ln_final and unembed.
* **At ln_final_out:** compute normally up to `ln_final`; set the normed vector at `index` to the replacement; apply W_U directly.
* **Always:** eval mode, `torch.no_grad()`, no parameter writes. The learner receives no target, oracle or analysis object.

**Real-data acceptance (G2, validation, per model):**

* identity replacement → logits at index 32 within **1e-5** absolute (float32) of plain `forward`, and at every index < 32 within **1e-7**;
* the primary eraser replacement → logits at every index < 32 within **1e-7** of plain `forward` (causality on real inputs);
* the final effective-null replacement leaves the centred logits at index 32 unchanged within **1e-8**, recomputed in float64 from y′ with the same W_U;
* the parameter state-dict sha256 is unchanged.

**Fixture tests (independent test writer):**

* identity reproduces every position;
* a non-identity patch at index p leaves indices < p unchanged and changes index p;
* the final-null patch leaves the centred logits unchanged;
* invalid site, index or shape raises the documented code;
* weights are bitwise identical before and after;
* learner imports no world, process, oracle, analysis or prediction code.

## 8. Damage profile, units and specificity rules

**Measured on outer validation** for every fitted eraser and every accepted random. Each quantity keeps its own unit:

| Quantity | Unit | Definition |
|---|---|---|
| lost rank | integer | rank(P) |
| displacement | resid_post_1 L2 units | d_i quantiles; mismatch vs the matched target (§6) |
| linear Q1 decodability loss | dimensionless R² | R²_val(h → Q1) − R²_val(h′ → Q1), both through the §4 pipeline, with the erased model refit on erased calibration features |
| circle decodability after erasure | dimensionless R² | linear and RBF R²_val(h′ → m32) |
| output displacement | nats | mean_h KL(p(h) ‖ p_I(h)) over full softmax |
| support | fraction | §9 |

**Validation regret is not computed** in this execution. ΔR is the test outcome and is reserved for the fresh causal test.

**Prospective specificity rules** (applied later to the test; written now):

* **S1 (generic predictive information).** Specificity of the primary against generic predictive damage is claimed only if, on validation, the m32 eraser's linear Q1 decodability loss is ≤ the generic-predictive eraser's (R² vs R²). Otherwise specificity against generic predictive damage is **withheld**, and the primary verdict is reported unchanged.
* **S2 (short context).** Specificity against short context is claimed only if, on test, ΔR(m32) − ΔR(m2) has a bootstrap lower bound > 0 in every model (nats vs nats). Otherwise it is withheld.
* **S3 (R1).** Likewise with the R1 eraser, under the same rule as S2.
* **S4 (rank-1 y comparison).** The circle-PC1 and y erasers are each compared with their own rank-1 matched randoms (§6). The excess circle-PC1 − y is reported in nats. A rank-1 result is never compared with a rank-2 or partial-dose result.

**Unmatched controls.** A control whose mean displacement is not within 5% of the primary is labelled `unmatched`. Its comparison with the primary is descriptive, and no specificity claim rests on it. Random families that cannot reach 20 accepted draws fail G4.

## 9. Support (G5)

* **Reference distribution.** Ledoit–Wolf covariance and the mean of calibration h. The Mahalanobis distance D(x) has its reference threshold q99_cal on calibration rows.
* **Pass, per model.** The fraction of patched validation vectors with D > q99_cal is **≤ 0.05** for the primary eraser, and **≤ 2 ×** the median fraction over its 20 matched randoms.
* **Reported, not gates:** the same quantities for every control; the 10-NN distance ratio, i.e. the median distance from patched vectors to their 10 nearest calibration rows over the same quantity for unpatched validation rows; and the change in the resid_post_3 pre-LN norm.

## 10. Gates and the first execution task

**Gate statuses.** Each gate passes in all three models, or fails with a named reason.

| Gate | Pass condition |
|---|---|
| G1 | G1-primary (§4) |
| G2 | adapter acceptance (§7) |
| G3 | linear R²_val(h′ → m32) ≤ **0.05** for the primary, and the eraser exactness check passes. If RBF R²_val(h′ → m32) ≥ **0.25**, the label `LINEAR_COMPONENT_ONLY` is attached; this is a label, not a failure. |
| G4 | both random families (rank 2 and rank 1) reach 20 accepted draws; the damage profiles of §8 are computed |
| G5 | §9 |

**Overall.**

* `FEASIBLE` iff G1–G5 all pass.
* `NOT_FEASIBLE` iff G1-primary fails cleanly in some model.
* `INCONCLUSIVE` otherwise, with the gate named.

**First execution task scope** (a later job; nothing more):

* implement the adapter, the analysis functions and the orchestration, with independent tests;
* extract dev activations: `embed`, `resid_post_1`, `resid_post_3` and `ln_final_out` plus logits, for the three step-5000 checkpoints, with step-0 optional. These go to an independent store.
* run G1–G5 on calibration and validation; write the gate report; **STOP**.

**Excluded from the first execution task:**

* any fresh-test sampling or test-time ΔR;
* any change to the primary;
* the PH manipulation check.

**Deferred, not removed** (each needs its own future task):

* the natural-donor patch;
* the frozen-vs-refitted readout comparison;
* the dose curve (α ∈ {0.25, 0.5, 0.75}, still listed);
* the PH manipulation check on validation clouds.

## 11. Frozen parameters

| Parameter | Value |
|---|---|
| Models / site / index | seeds 1729, 2718, 3141 at step 5000 / resid_post_1 / input index 32 |
| Calibration / validation | dev panels 1–6 (3,072) / 7–8 (1,024) per model |
| Inner selection | leave-one-panel-out over panels 1–6; λ ∈ {1e-3, 1e-2, 1e-1, 1, 10}; ties → larger λ |
| R² definition | 1 − SSE_val / SST_val around the calibration mean, pooled over coordinates |
| Shuffled controls | 20 per (model, target); stream ("x4f-v1", "shuffle", target, seed, k); q95 |
| RBF probe | 2,048 features; median bandwidth on 1,024 calibration rows; streams ("x4f-v1", "rbf" / "rbf_bandwidth", seed) |
| G1 | m32 R² ≥ 0.50 and > shuffled q95; r2 R² ≥ 0.10 and > q95; r2 low-variance rule 0.01 × / 1e-6 |
| Whitening / rank tolerances | eigenvalue floor 1e-10 × λ_max; projector rank tolerance 1e-8 × σ_max; exactness 1e-8 relative |
| G2 | index-32 logits ≤ 1e-5 abs (float32); indices < 32 ≤ 1e-7; final-null centred logits ≤ 1e-8 (float64); weights hash equal |
| G3 | linear R² ≤ 0.05; RBF label at ≥ 0.25 |
| Random erasers | ranks 2 and 1; 20 accepted; mean-displacement tolerance 5%; ≤ 10,000 draws; stream ("x4f-v1", "random_eraser", r, seed, i) |
| G5 | Ledoit–Wolf Mahalanobis; q99_cal; primary ≤ 0.05 and ≤ 2 × median random |
| Dose | α = 1.0 only in the first execution; {0.25, 0.5, 0.75} deferred |
| Future test (recorded, not executed) | 4,096 canonical trajectories per process; stream ("x4f-v1", "test", "cylinder", "overlap", "1.25"); namespace code 6; 2,000 joint canonical bootstrap draws, stream ("x4f-v1", "bootstrap"); primary rule as in §1 |
| Budget | cumulative X4-F scientific execution ≤ **3 CPU h**, 8 GB RAM peak working set (measured with the corrected query); first gate task ≤ 1 CPU h of it. Technical implementation and test time are reported separately. |

## 12. Changes from x4f-draft-1 (all before any real-data execution)

| # | Draft-1 | x4f-exec-v1 | Reason |
|---|---|---|---|
| 1 | Primary frame | unchanged | coordinator item 1 |
| 2 | λ "chosen on validation MSE" | nested leave-one-panel-out inside calibration; validation reserved for gates; shuffles run the same pipeline | gate scores must not be selection-biased (item 2) |
| 3 | G4 compared "Q1-decodability loss" with "its own effect margin" (R² vs nats) | the undefined comparison is removed; a unit table is added; specificity rules S1–S4 compare like with like; the primary rule is untouched | unit consistency (item 3) |
| 4 | y rank 1 "against a rank-1 dose of the primary" | a separate rank-1 circle-PC1 eraser fitted on calibration, with its own rank-1 random family | a partial rank-2 dose does not lose rank 1 (item 4) |
| 5 | mean displacement matching, deviation unstated | deviation from per-history matching stated, justified and quantified | item 5 |
| 6 | final-null "at ln_final_out" | u-space P_eff from A·C, then y′ = u′·diag(γ) + β; no projector on y; no second LayerNorm | item 6 |
| 7 | adapter returned logits at p only | full logits for all positions; index semantics; tolerances for < p; weights hash | item 7 |
| 8 | "m2 fit-free affine baseline" (ambiguous) | (a) direct, (b) fitted affine and (c) fitted [m2, h], kept distinct; low-variance drop for r2 | item 8 |
| 9 | thresholds marked [P] | frozen values and seeds in §11; RBF bandwidth/λ selection defined; rank tolerances added; random draw limit unchanged (10,000) | item 9 |
| 10 | gates plus secondary expansions | first execution = implementation + G1–G5 only; natural donor, refitted head, dose curve and PH check deferred | item 10 |
| 11 | G2 tolerance for positions < p not stated | ≤ 1e-7 | added for item 7 |
| 12 | G3 had no eraser-exactness check | ≤ 1e-8 relative | numerical validity |

## 13. Review choices left to the coordinator

1. **G1-primary threshold.** Keep 0.50 or change it. It has no empirical basis at resid_post_1; resid_post_3 decodes b32 well, but that does not transfer.
2. **Step-0 extraction.** Whether to include the step-0 dev extraction. It is descriptive only and adds 3 forward passes of 4,096 histories.
3. **Inner-selection design.** Whether leave-one-panel-out with 6 folds is preferred to 5-fold random CV. Panels are disjoint trajectory sets, which favours panels.
4. **Mean-only matching.** Whether mean-only displacement matching is acceptable, or whether an additional median within 10% should be required. The latter is stricter and may fail G4 more often.
5. **First gate task budget.** Whether 1 CPU h is the right share of the 3 CPU h total.
