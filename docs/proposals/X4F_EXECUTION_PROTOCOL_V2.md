# X4-F execution protocol (x4f-exec-v2)

14 October 2026. Branch `x4f-execution-contract`, from 2270fb0. Handoff job 0002 (correction round after the review of job 0001).

**Status: prepared for coordinator review.** This contract freezes only when the coordinator records ACCEPT. Nothing real-data runs before that.

**Governing documents.**

* It supersedes [x4f-exec-v1](X4F_EXECUTION_PROTOCOL.md), which is kept unchanged as a record. Changes v1 → v2 are listed in §13; changes draft-1 → v1 remain in v1 §12.
* [x4f-draft-1](X4F_COORDINATE_CAUSAL_PROTOCOL_DRAFT.md) and all historical results are unchanged.
* Base design: [X4_CAUSAL.md](X4_CAUSAL.md), Short experiment F.

**No scientific computation was performed** in preparing this contract.

**Choices accepted in the job 0001 review, adopted unchanged:**

* G1-primary stays at 0.50, as a prospective practical gate, not a calibrated guarantee;
* no new step-0 extraction;
* six-panel inner selection, with outer panels 7–8 used for gates only;
* mean-displacement matching within 5%, with per-history diagnostics and no median gate;
* the first gate task is capped at 1 CPU h, within a cumulative 3 CPU h / 8 GB for X4-F.

## 1. Fixed scientific frame

* **Hypothesis H4C-F.** In each of the three frozen step-5000 cylinder-O models (seeds 1729, 2718, 3141; σ 1.25; original T/E/π), erasing the m32 target at `resid_post_1`, input index 32, raises oracle-relative one-step regret by **≥ 0.01 nat** more than the mean over its matched random erasers.
  - Uncertainty comes from a paired bootstrap over canonical trajectories, resampled jointly across models.
  - A positive result is coordinate-associated information use. It is not H1 necessity, a topology effect or long memory.
* **Recorded results that stay as they are:**
  - the practical Q2-gap branch stays closed;
  - Phase B INCONCLUSIVE, B2 NO-GO, H4C-I NOT RUN, strict sufficiency UNRESOLVED;
  - E4 accepted with G-H FAIL.
* **Units.** The model is the replication unit; trajectories carry the uncertainty.

## 2. Definitions and array conventions

**Array conventions.** Rows are histories; columns are features or target coordinates.

* X ∈ R^{n×d} (d = 128); targets Z ∈ R^{n×q}.
* Means: μ = mean over the rows of X; ζ = mean over the rows of Z.
* Covariances use the population normalisation 1/n (erasure is invariant to this factor):
  Σ_xx = (X − μ)ᵀ(X − μ)/n and Σ_xz = (X − μ)ᵀ(Z − ζ)/n.
* A linear map is written M for its column action on a single vector x. Applied to a batch it is X′ = (X − μ)Mᵀ + μ.

**Inputs and site.**

* Inputs are `SequenceLayout.model_inputs`: [BOS = V, w1..w32], indices 0–32.
* History position p32 is input index 32.
* h is the output of `blocks[1]` at index 32.
* z3 is the output of `blocks[3]`.
* u = (z3 − mean(z3)) / sqrt(var(z3) + 1e-5), using the population variance.
* y = u·diag(γ) + β, and logits = y·W_Uᵀ.

**Targets (oracle-computed).**

* θ_z = 2π·x_z/12, and m(b) = Σ_z b_z (cos θ_z, sin θ_z).
* **m32 = m(b32) — primary.** b32 is the posterior from `BayesFilter(T, E, π)` on w1..w32.
* **m2 = m(b2).** b2 is the last step of `BayesFilter(T, E, π)` run on (w31, w32), with π as the stationary and initial law.
* **m1 = m(r_{w32}).**
* **r2 = m32 − m2 — secondary.**
* **y-target** = E_{b32}[y_z]/11.
* **Local-position target** = the 2 leading calibration principal components of b32·N, where N is the radius-1 cylinder incidence with self.
* **R1 target** = the 2 leading calibration principal components of one-hot(w32).
* **Generic predictive target** = the 2 leading calibration principal components of Q1 = b32·T·E.
* **circle-PC1 target** = m32·v1, where v1 is the leading eigenvector of Cov_cal(m32).

**Effect measure.**

ΔR(I) = mean_h [ KL(Q1 ‖ p_I) − KL(Q1 ‖ p) ], in nats, over full distributions.

## 3. Data roles (unchanged from v1)

| Role | Panels | Use |
|---|---|---|
| Calibration | dev 1–6 (3,072) | inner leave-one-panel-out tuning; final refit of every probe, eraser, control, standardisation and support statistic |
| Outer validation | dev 7–8 (1,024) | gates only; never selection |
| Fresh causal test | later job | single H4C-F evaluation |

## 4. Recoverability (G1)

**Probe and standardisation.**

* Affine ridge with an unpenalised intercept, using `RidgeProbe` semantics: it centres on the fitting rows, with W = (XcᵀXc + λI)⁻¹XcᵀYc.
* Features are standardised before the probe, using statistics of the fitting rows only. A column with fitting-row standard deviation ≤ 1e-12 is centred and left unscaled (factor 1).

**Pipeline.**

1. **Inner selection.** Leave-one-panel-out over calibration panels 1–6. For each λ ∈ {1e-3, 1e-2, 1e-1, 1, 10} and each fold, fit with `RidgeProbe([λ])` on 5 panels and compute the MSE on the held-out panel.
2. **Choose λ.** Take the λ with the minimal mean fold MSE. Ties go to the larger λ.
3. **Refit** on all of calibration.
4. **Score once** on validation.

**R² and its zero case.**

* R²_val = 1 − SSE_val / SST_val, where SST_val = Σ_{i, coordinates} (Z_val − ζ_cal)², i.e. pooled around the calibration mean.
* If SST_val ≤ 1e-12 · n_val · q, the status is **R2_UNDEFINED_ZERO_VARIANCE** and no R² value is reported.
  - For m32 this makes **G1 INCONCLUSIVE**.
  - For a secondary target, it drops that analysis.

**Shuffled controls.**

* 20 per (model, target), with stream ("x4f-v1", "shuffle", target, seed, k).
* Calibration target rows are permuted jointly, and the identical pipeline (inner selection plus refit) is run on them.
* Scoring uses the unpermuted validation targets. The q95 is taken over the shuffles that have a defined R².
* If fewer than 20 shuffles have a defined R², the status is **SHUFFLE_UNDEFINED**, which makes the gate INCONCLUSIVE.

**RBF residual probe (for G3).**

* Features: 2,048 random Fourier features of the calibration-standardised x, φ(x) = sqrt(2/2048)·cos(x̃Ω + b).
* Draws: Ω ~ N(0, ℓ⁻²) and b ~ U[0, 2π), from stream ("x4f-v1", "rbf", seed).
* Bandwidth: ℓ is the median of the pairwise distances among 1,024 calibration rows drawn with stream ("x4f-v1", "rbf_bandwidth", seed).
* If ℓ ≤ 1e-12, the status is **RBF_DEGENERATE**: no RBF value is reported, and the G3 label is not attached.
* For erased features, the standardisation and ℓ are recomputed on the erased calibration rows.

**G1, per model, for all three models.**

* **G1-primary:** R²_val(h → m32) ≥ 0.50, and above the shuffled q95.
* **G1-r2** (governs only whether r2 is measured and reported):
  1. If trace Var_cal(m32) ≤ 1e-12, the status is M32_ZERO_VARIANCE and G1 is INCONCLUSIVE.
  2. Otherwise, if trace Var_cal(r2) < 0.01 × trace Var_cal(m32), or trace Var_cal(r2) ≤ 1e-6, the status is **R2_DROPPED_LOW_VARIANCE**.
  3. Otherwise the criterion is R²_val(h → r2) ≥ 0.10 and above the q95. Failure gives **R2_NOT_RECOVERABLE**.
* **What r2 is used for.** r2 is measured only. Causal support for r2 is not tested in this contract (see §6, F-r2).

**Short-context comparators (descriptive).** Each uses the same SST_val and the same zero-variance rule.

* **(a) Fit-free direct:** m2 used directly as the prediction of m32.
* **(b) Fitted affine:** m2 → m32.
* **(c) Fitted affine:** [m2, h] → m32.

The m1 analogues of (a) and (b) are also reported.

## 5. Whitening and erasers (calibration only)

**Whitening with a retained range.**

* Eigendecomposition: Σ_xx = U Λ Uᵀ.
* Retain the eigenvectors with λ_i > 1e-10 · λ_max, giving U_keep (d×k) and Λ_k.
* W = Λ_k^{−1/2} U_keepᵀ (k×d, mapping a centred x to whitened coordinates in R^k); W⁺ = U_keep Λ_k^{1/2} (d×k).
* Then W W⁺ = I_k, and W⁺ W = U_keep U_keepᵀ.
* If λ_max ≤ 1e-12, or k = 0, the status is **FEATURES_DEGENERATE** and no eraser can be built. For the primary, this makes **G3 INCONCLUSIVE**.

**Target cross-covariance (primary and every control).**

* G = W Σ_xz (k×q), the whitened cross-covariance.
* Degenerate targets:
  - If trace Cov_cal(Z) ≤ 1e-12, the status is **TARGET_ZERO_VARIANCE**.
  - Otherwise, if ρ_max = σ_max(G) / sqrt(trace Cov_cal(Z)) ≤ 1e-8, the status is **TARGET_UNCORRELATED**. ρ_max is a dimensionless canonical-correlation bound in [0, 1].
  - For the primary, either status makes **G3 INCONCLUSIVE**. For a control, it withholds that comparison.
* Rank: r = the number of singular values of G with σ > 1e-8 · σ_max(G). It is **reported as found, not assumed to be 2**, and it always satisfies 1 ≤ r ≤ min(q, k). A rank is never inferred from singular values below this tolerance.
* P_s = Q_r Q_rᵀ (k×k), where Q_r holds the r leading left singular vectors of G.

**Eraser map.**

* E = W⁺ P_s W (d×d, the removed component), and M = I − E.
* Batch form: X′ = (X − μ)Mᵀ + μ.
* **Equivalent d-dimensional form:** with W_d = U_keep Λ_k^{−1/2} U_keepᵀ, W_d⁺ = U_keep Λ_k^{1/2} U_keepᵀ and P = U_keep P_s U_keepᵀ, the same E equals W_d⁺ P W_d. This matches the review's notation "Q = U_keep Q_small, P = QQᵀ".

**Required properties.** Each check is computed and reported; a failure gives **ERASER_INVALID**, which for the primary is a G3 failure:

* **Idempotence:** ‖M M − M‖_max ≤ 1e-10 · max(1, ‖M‖_max). This holds analytically, because W W⁺ = I_k.
* **Rank loss:** the number of singular values of E above 1e-8 · σ_max(E) equals r.
* **Exactness:** ‖Cov_cal(X′, Z)‖_max ≤ 1e-8 · ‖Σ_xz‖_max. Σ_xz is non-zero here, because degenerate targets were already handled.
  - The residual (I − U_keep U_keepᵀ)Σ_xz lies in the discarded eigen-directions.
  - By Cauchy–Schwarz it is bounded by sqrt(1e-10 · λ_max · trace Cov(Z)).
  - Its value is reported.

**Fitted erasers.**

* Primary: m32.
* Mandatory test-time controls, fitted and profiled in the first gate task: shuffled-target m32 (stream ("x4f-v1", "shuffle_eraser", seed)), R1, m2, local position, and generic predictive.
* Optional: the circle-PC1 and y erasers, only if S4 is retained (§8).
* Not fitted in this contract: the r2 eraser.

**Final effective-null (unchanged from v1).**

* C = I − 11ᵀ/V, and P_eff = `readout_projector(γ, C·W_U)`, the projector onto range(A·C) with A = diag(γ)·W_Uᵀ.
* u′ = u·P_eff; then y′ = u′·diag(γ) + β replaces `ln_final_out` at index 32 and goes directly to W_U.
* No projector is applied to y, and there is no second LayerNorm.
* If P_eff = 0 (A·C = 0), the status is **READOUT_DEGENERATE**, and **G2 is INCONCLUSIVE**.

**Dose.** α = 1.0 only; M is then idempotent. Partial doses M_α = I − αE (deferred) are **not** idempotent for 0 < α < 1, and are never called erasures. α = 0 is never used.

## 6. Random matched families (by target)

**Family list.**

| Family | Matched to | Rank | Status in the first gate task |
|---|---|---|---|
| F-primary | m32 eraser | r_primary (§5) | **mandatory; gates G4** |
| F-circlePC1 | circle-PC1 eraser | its own r (1 if non-degenerate) | optional: built only if S4 is retained; never gates the primary |
| F-y | y eraser | its own r | optional: same rule |
| F-r2 | r2 eraser | — | **not built here**; needs a later reviewed test task with its own frozen rule before any fresh sampling |

In the first gate task only F-primary is constructed. The optional families are not built just to exercise the architecture.

**Draws (for a family matched to target eraser t with rank r_t).**

* Require r_t ≤ k; otherwise the status is **RANK_EXCEEDS_RETAINED**.
* Draw j uses stream ("x4f-v1", "random_eraser", family, seed, j). Draw G_j ∈ R^{k×r_t} with i.i.d. N(0, 1) entries.
* Take the QR factorisation Q_s = qr(G_j). If |diag(R)|_min ≤ 1e-12 · |diag(R)|_max, the draw is rejected as **DRAW_DEGENERATE** and counted.
* Set P_s = Q_s Q_sᵀ, and E_j = W⁺ P_s W with the **same** μ, W and W⁺ as the target eraser, so the random erasers live in the retained range. Each accepted draw passes the same idempotence and rank-loss checks.

**Displacement and matching.**

* d_i = ‖x′_i − x_i‖₂ in raw resid_post_1 units. D = mean_i d_i on calibration.
* Target displacement zero case: if D_t ≤ 1e-12 · mean_i ‖x_i − μ‖₂, the status is **ZERO_DISPLACEMENT**. Matching is then undefined: G4 is INCONCLUSIVE for F-primary, and the comparison is withheld for an optional family.
* Acceptance: |D_j − D_t| ≤ 0.05 · D_t.
* Drawing continues until 20 draws are accepted or 10,000 draws are reached. Accepted indices are frozen.
* Fewer than 20 accepted: **FAMILY_UNMATCHED**. This is a G4 failure for F-primary, and withholds S4 for an optional family.
* Per-history mismatch: |d_i(rand) − d_i(t)| / d_i(t), over the histories with d_i(t) > 1e-12 · mean_i ‖x_i − μ‖₂. The number of excluded histories is reported.
* **Deviation from X4_CAUSAL (kept from v1).** X4_CAUSAL asks for per-history matching; this contract matches the mean. q10, q50 and q90 of d_i and the per-history mismatch (median, q90) are reported.
* **Interpretation.** Equal rank and matched mean displacement do not imply equal predictive damage.

## 7. Frozen-forward adapter (unchanged from v1 §7, restated)

```python
forward_with_patch(model, inputs[R, 33], site, index, replacement[R, d])
```

* Returns full logits [R, 33, V] and the requested hooks.
* `site` ∈ {resid_post_k, ln_final_out}. At resid_post_k, x[:, index] is replaced after `blocks[k]` and the forward pass continues. At ln_final_out, the normed vector is replaced and W_U is applied directly.
* Runs in eval mode with no_grad and no parameter writes. The learner receives no target or oracle object.

**G2 (validation, per model):**

* identity replacement → index-32 logits within 1e-5 (float32), and indices < 32 within 1e-7;
* primary eraser replacement → indices < 32 within 1e-7;
* final effective-null → centred logits within 1e-8 (float64);
* state-dict sha256 unchanged.

The independent fixture tests are as in v1.

**Probability zero case.** Model probabilities are a softmax of finite logits, so they are strictly positive. If a KL term meets p_I(v) = 0 where the other law is positive, after float64 conversion, the status is **KL_UNDEFINED** for that history set. Nothing is clipped or smoothed.

## 8. Damage profile, units, eligibility and specificity

**Damage profile on validation.** Computed for the primary, every accepted random in F-primary and every fitted control:

| Quantity | Unit |
|---|---|
| lost rank r | integer |
| displacement quantiles; mismatch | resid_post_1 L2 units; dimensionless ratio |
| linear Q1-decodability loss ΔR²_Q1 = R²_val(h → Q1) − R²_val(h′ → Q1) | dimensionless R² (§4 pipeline; erased refit on erased calibration) |
| linear and RBF R²_val(h′ → m32) | dimensionless R² |
| output displacement mean KL(p ‖ p_I) | nats |
| support fraction | fraction (§9) |

Validation regret ΔR is **not** computed before the fresh test.

**Specificity rules (prospective).** The primary 0.01-nat rule is unchanged by all of these. Units are never mixed.

* **S1 — eligibility only (validation, R² vs R²).**
  - The primary is *eligible* for a later claim against generic predictive damage only if ΔR²_Q1(m32 eraser) ≤ ΔR²_Q1(generic eraser).
  - S1 alone never establishes specificity.
  - If S1 fails, the generic specificity claim is withheld in advance.
* **S1-test — claim beyond generic predictive damage (fresh test, nats vs nats).** All of the following are required:
  1. S1 eligibility.
  2. Matched controls: the generic eraser's rank equals r_primary, and its calibration mean displacement is within 5% of the primary's.
  3. Valid controls: the generic eraser has no degeneracy status and passes G5's primary-level support rule.
  4. In every model, the paired bootstrap 95% lower bound of ΔR(m32) − ΔR(generic) is > 0.

  If any one fails, the claim is withheld.
* **S2 (short context, m2) and S3 (R1, last symbol).** The same four test-time requirements as S1-test, with the m2 or R1 eraser in place of the generic one. There is no S1-style validation eligibility step for these.
* **S4 (rank-1 circle-PC1 vs y; optional).**
  - Only if retained before the fresh test. Each eraser is compared against its own matched rank-1 family.
  - The reported quantity is [ΔR(circle-PC1) − mean ΔR(F-circlePC1)] − [ΔR(y) − mean ΔR(F-y)], in nats, with a paired lower bound.
  - If either family is FAMILY_UNMATCHED or degenerate, S4 is withheld.
  - A rank-1 result is never compared with a rank-2 or partial-dose result.
* **Unmatched or degenerate controls** keep descriptive damage profiles only; no claim rests on them.

## 9. Support (G5)

* **Reference.** The mean and Ledoit–Wolf covariance of calibration h. If the Ledoit–Wolf covariance is not positive definite (minimum eigenvalue ≤ 1e-12 · maximum), the status is **SUPPORT_DEGENERATE** and **G5 is INCONCLUSIVE**.
* **Statistic.** D(x) is the Mahalanobis distance; q99_cal is computed over the calibration rows.
* **Pass, per model.**
  - frac_primary = the fraction of patched validation vectors with D > q99_cal; it must be ≤ 0.05;
  - and frac_primary ≤ 2 × median_j frac_j over the 20 accepted F-primary draws.
  - **Zero case, stated literally:** if that median is 0, the clause requires frac_primary = 0. No floor is added.
* **Reported, not gates:**
  - the unpatched-validation fraction beyond q99_cal, as the reference;
  - the 10-NN ratio. Its denominator is the median 10-NN distance of unpatched validation rows to calibration; if that is 0, the status is RATIO_UNDEFINED;
  - the change in the resid_post_3 pre-LN norm.

## 10. Gates and the first execution task

| Gate | Pass condition (all three models) | Statuses giving INCONCLUSIVE |
|---|---|---|
| G1 | G1-primary | R2_UNDEFINED_ZERO_VARIANCE (m32), M32_ZERO_VARIANCE, SHUFFLE_UNDEFINED |
| G2 | §7 acceptance | READOUT_DEGENERATE, KL_UNDEFINED |
| G3 | primary linear R²_val(h′ → m32) ≤ 0.05, ERASER valid. The label LINEAR_COMPONENT_ONLY is attached if RBF R² ≥ 0.25. | FEATURES_DEGENERATE, TARGET_ZERO_VARIANCE, TARGET_UNCORRELATED, ERASER_INVALID, R2_UNDEFINED_ZERO_VARIANCE |
| G4 | F-primary reaches 20 accepted draws; damage profiles computed for the primary, F-primary and the mandatory controls (a control's own degeneracy withholds only that control) | ZERO_DISPLACEMENT, RANK_EXCEEDS_RETAINED, FAMILY_UNMATCHED |
| G5 | §9 | SUPPORT_DEGENERATE |

**Overall.**

* FEASIBLE iff G1–G5 all pass.
* NOT_FEASIBLE iff G1-primary fails with defined values in some model.
* INCONCLUSIVE otherwise, with the gate and status named.

**First execution task.** It is to be issued separately, after ACCEPT:

1. Implement the adapter, the analysis functions and the gate orchestration, with independent tests (including the fixtures of the addendum).
2. Extract dev activations at step 5000 for `embed`, `resid_post_1`, `resid_post_3` and `ln_final_out`, plus logits, into an independent store.
3. Run G1–G5 on calibration and validation, write the gate report, and STOP.

**Excluded from the first execution task:**

* fresh sampling and test-time ΔR;
* the optional families F-circlePC1 and F-y, and F-r2;
* the r2 eraser;
* new step-0 extraction.

**Deferred, listed and not dropped:**

* the natural-donor patch;
* the frozen-vs-refitted readout comparison;
* the dose curve;
* the PH manipulation check;
* the S4 retention decision;
* an r2 causal-support rule.

**No change in response to data.** No threshold or tolerance in this contract may change in response to dev results.

## 11. Zero and near-zero cases (consolidated)

| Quantity | Condition | Status | Effect |
|---|---|---|---|
| SST_val (any target) | ≤ 1e-12 · n_val · q | R2_UNDEFINED_ZERO_VARIANCE | primary → G1 or G3 INCONCLUSIVE; secondary → dropped |
| trace Var_cal(m32) | ≤ 1e-12 | M32_ZERO_VARIANCE | G1 INCONCLUSIVE |
| trace Var_cal(r2) | < 0.01 × trace Var_cal(m32), or ≤ 1e-6 | R2_DROPPED_LOW_VARIANCE | r2 not measured |
| Shuffle R² | fewer than 20 defined | SHUFFLE_UNDEFINED | gate INCONCLUSIVE |
| Feature standard deviation | ≤ 1e-12 | (column unscaled) | — |
| RBF bandwidth ℓ | ≤ 1e-12 | RBF_DEGENERATE | no RBF label |
| λ_max(Σ_xx), or k | ≤ 1e-12, or k = 0 | FEATURES_DEGENERATE | eraser impossible |
| trace Cov(Z) | ≤ 1e-12 | TARGET_ZERO_VARIANCE | eraser not built |
| ρ_max | ≤ 1e-8 | TARGET_UNCORRELATED | eraser not built |
| Singular values of G | ≤ 1e-8 · σ_max | (excluded from the rank) | no rank from noise |
| Idempotence, rank, exactness | outside the §5 tolerances | ERASER_INVALID | primary → G3 failure |
| r_t vs k | r_t > k | RANK_EXCEEDS_RETAINED | family impossible |
| QR diagonal | min ≤ 1e-12 · max | DRAW_DEGENERATE (draw rejected, counted) | — |
| D_t | ≤ 1e-12 · mean ‖x − μ‖ | ZERO_DISPLACEMENT | matching undefined |
| d_i(t) per history | ≤ 1e-12 · mean ‖x − μ‖ | (excluded from the mismatch ratio, counted) | — |
| Accepted draws | < 20 within 10,000 | FAMILY_UNMATCHED | primary → G4 failure; optional → withheld |
| A·C (readout) | P_eff = 0 | READOUT_DEGENERATE | G2 INCONCLUSIVE |
| Probability in KL | 0 where the other law is positive | KL_UNDEFINED | no clipping |
| Ledoit–Wolf covariance | λ_min ≤ 1e-12 · λ_max | SUPPORT_DEGENERATE | G5 INCONCLUSIVE |
| Median random support fraction | = 0 | (literal: primary must be 0) | — |
| 10-NN denominator | = 0 | RATIO_UNDEFINED | reported only |
| Dose α | α ≠ 1 | — | not used now; never called erasure if < 1 |

Each tolerance has its own source:

* 1e-12 is a float64 zero floor.
* 1e-8 is the rank tolerance, or the relative exactness tolerance.
* 1e-10 is the whitening floor.
* 0.01 and 1e-6 are the r2 low-variance rule, carried from v1.

None is new in response to data, and none has been evaluated on data.

## 12. Frozen parameters

| Parameter | Value |
|---|---|
| Models / site / index | seeds 1729, 2718, 3141 at step 5000 / resid_post_1 / input index 32 |
| Calibration / validation | dev panels 1–6 (3,072) / 7–8 (1,024) |
| Inner selection | leave-one-panel-out over panels 1–6; λ ∈ {1e-3, 1e-2, 1e-1, 1, 10}; ties → larger λ |
| R² | 1 − SSE/SST around the calibration mean, pooled; zero rule §11 |
| Shuffles | 20, q95, identical pipeline |
| RBF | 2,048 features; median bandwidth on 1,024 calibration rows; seeded |
| G1 | 0.50 and > shuffled q95; r2 0.10 and > q95; low-variance rule |
| Whitening | retained λ > 1e-10 · λ_max (k recorded) |
| Rank tolerance | 1e-8 · σ_max; rank reported as found |
| Eraser checks | idempotence 1e-10; rank loss = r; exactness 1e-8 relative |
| G2 | 1e-5 / 1e-7 / 1e-8; weights hash |
| G3 | linear ≤ 0.05; RBF label ≥ 0.25 |
| F-primary | rank r_primary in the retained range; 20 accepted within 5% mean displacement; ≤ 10,000 draws; stream ("x4f-v1", "random_eraser", family, seed, j) |
| G5 | Ledoit–Wolf; q99_cal; ≤ 0.05 and ≤ 2 × median F-primary |
| Dose | α = 1.0 |
| Future test (recorded only) | 4,096 canonical trajectories; stream ("x4f-v1", "test", "cylinder", "overlap", "1.25"); namespace 6; 2,000 joint bootstrap draws, stream ("x4f-v1", "bootstrap") |
| Budget | X4-F scientific ≤ 3 CPU h cumulative, 8 GB; first gate task ≤ 1 CPU h; technical time reported separately |

## 13. Change log v1 → v2 (before any data)

| # | v1 | v2 | Review item |
|---|---|---|---|
| 1 | random Q drawn in full d | drawn in R^k (retained whitening range), embedded via U_keep; same μ/W/W⁺ as the target; idempotence and rank-loss checks; actual r_primary used, not 2; degeneracy statuses; batch convention X′ = (X − μ)Mᵀ + μ | 1 |
| 2 | S1 read as a specificity rule | S1 = validation eligibility only; a generic claim needs S1, matched rank and displacement, valid controls, and a paired test ΔR lower bound > 0 in every model; S2/S3 use the same test requirements; units separate | 2 |
| 3 | two families by rank, both required by G4 | families by target; only F-primary is mandatory and gates G4; F-circlePC1 and F-y are optional, built only if S4 is retained, and withhold S4 on failure, never failing the primary; F-r2 deferred to a later reviewed task; **explicit change: v1's mandatory rank-1 family is removed from G4** | 3 |
| 4 | zero cases partly implicit | §11 table: covariance exactness with a non-zero baseline guaranteed, R² zero variance, displacement denominators, KL zeros, support zero median, readout degeneracy, dose | 4 |
| 5 | erasers for every control fitted at the gate | mandatory test-time controls fitted and profiled; optional y/circle-PC1 only with S4; r2 eraser not fitted | 3 |

## 14. Coordinator review choices still open

None are required for ACCEPT. One is optional: whether to retain S4 (and so build F-circlePC1 and F-y) can be decided before the fresh-test task. Until then it remains deferred.
