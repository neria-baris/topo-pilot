# X4-F: coordinate-associated causal use — protocol draft (x4f-draft-1)

14 October 2026. Branch `x4f-planning`, from 698e9b1.

**DRAFT FOR OWNER REVIEW.** It authorises nothing. Nothing in this document has been implemented, sampled, fitted, extracted or run. Every proposed numeric criterion is marked **[P]** and needs explicit approval before execution. The base design is [X4_CAUSAL.md](X4_CAUSAL.md), "Short experiment F". Where this draft adds to it, the addition is labelled; nothing in it is replaced silently.

## 0. Standing results this draft builds on (unchanged)

| Item | Status | Record |
|---|---|---|
| E4 circular coordinate vs symbol-only and mixing explanations | In all 3 cylinder-O models, the resid_post_3 coordinate exceeds the in-sample optimistic last-symbol bound and R1/R2/R3/b1 in 24/24 run-panels. This is **descriptive only**: no independent confirmation and no causal evidence. | D-057 |
| Practical Q2-gap branch | Closed: Phase B INCONCLUSIVE, B2 NO-GO, H4C-I NOT RUN, strict sufficiency UNRESOLVED. Phase C is not reopened. | D-052, D-054, D-055 |

The open questions for X4-F:

* **Short-context origin.** Does the information beyond the last symbol come from w31/w32 or from longer history?
* **Intermediate recoverability.** Is the coordinate recoverable at resid_post_1? The resid_post_3 result does not transfer automatically.
* **Causal use.** Does the frozen model's next prediction use this information?

## 1. Hypothesis (unchanged from X4_CAUSAL)

**H4C-F.** At resid_post_1, position 32, linearly erasing the calibrated belief-expectation circle target m32 raises oracle-relative one-step regret in each of the three frozen cylinder-O models. The rise must exceed that of rank- and displacement-matched random erasure by **≥ 0.01 nat**.

The claim is **coordinate-associated information use** in this frozen computation. It is not H1 necessity, a topology-specific effect or long-history integration. Information erasure is not a topology change.

## 2. Objects

### Models

The three frozen step-5000 cylinder-O checkpoints, seeds 1729, 2718 and 3141 (σ 1.25, original T/E/π). Step-0 checkpoints are used for descriptive initialisation references only.

### Site

`resid_post_1` at position 32: the input token is w32, the history is w1..w32, and the prediction is for w33.

The intervention replaces only the position-32 vector at that site. The token sequence, attention mask, positions 0–31 at every layer, and all weights stay frozen. Blocks 2–3, the final LayerNorm and the unembedding are recomputed. Because attention is causal, the patch can affect only position 32's output; this is verified as a test.

### Targets (oracle-computed, never given to the model)

* x angle of each state: θ_z = 2π·x_z/12.
* **Primary:** m32 = Σ_z b32_z (cos θ_z, sin θ_z), with b32 the exact belief over all 32 symbols. Expectations are used instead of an angle, which is undefined when the resultant is small.
* **Short-context control (added):**
  - b2 = P(z32 | w31, w32) under the stationary prior π, computed with the existing `BayesFilter(T, E, π)` on the two-token history (w31, w32);
  - m2 = Σ_z b2_z (cos θ_z, sin θ_z);
  - b1 = r_{w32} (the existing last-symbol posterior), and m1 = Σ_z b1_z (cos θ_z, sin θ_z).
* **Secondary target (added):** r2 = m32 − m2, the expected-angle information beyond the last two symbols. **r2 does not replace the primary hypothesis.** An effect attributed to r2 would still not show long memory; it shows information beyond (w31, w32).
* **The PH angle is not a target.** The persistent-homology angle is not an intervention target because no out-of-sample map for it is validated.

### Effect measure (unchanged)

Per model r, with p the frozen model's next-symbol distribution and p_I the distribution after intervention I:

  ΔR_r(I) = E_h[ KL(Q1(h) ‖ p_I(h)) − KL(Q1(h) ‖ p(h)) ]  (nats; Q1 is the oracle's next-symbol law)

## 3. Data splits, frozen in order

| Role | Source | Use | Never used for |
|---|---|---|---|
| Calibration | Existing dev pool of each model, panels 1–6 (3,072 histories) | fit probes, erasers, controls, standardisation and support statistics | evaluation of any gate |
| Validation | Same dev pool, panels 7–8 (1,024 histories) | feasibility gates G1–G5; dose and support checks | fitting |
| Fresh causal test | **New** 4,096 trajectories per process, from a new named stream and sequence-ID namespace (x4f-v1). Canonical trajectories are shared across the 3 models, each mapped through its own symbol_perm. | the single H4C-F evaluation | any selection of site, transform, dose, control or threshold |

* **Not usable.** The old test pool and the B2 pools are not used as the causal test. The old test pool is unblinded. The B2 pools were drawn for a different question; reusing them is listed as an owner decision.
* **Mappings.** Per-model dev histories keep their own history IDs. Fresh-test canonical keys are mapped to each model's history IDs, and no join uses token-hash IDs alone.

## 4. Feasibility gates (validation only; all must pass before any fresh-test run)

### G1 — recoverability at resid_post_1

* **Method:** affine ridge with an unpenalised intercept, fit-only standardisation and λ ∈ {1e-3, …, 10}, chosen on validation MSE. This is the existing RidgeProbe protocol.
* **Fit and score:** fit on calibration, score on validation.
* **Primary [P]:** validation R² of m32 (both coordinates pooled, variance-weighted) **≥ 0.50** in every model, and above the q95 of 20 shuffled-label refits.
* **Beyond two symbols [P]:** validation R² of r2 **≥ 0.10** and above the shuffled q95, in every model.
  - Also reported: R²(resid_post_1 → m32) − R²(m2 → m32), with m2 as a fit-free affine baseline.
  - If this sub-gate fails, the secondary r2 analysis is dropped and reported as such. The primary analysis may continue.
* **Descriptive only:** the same probes at resid_post_3 and embed, and at step 0.

### G2 — identity reconstruction of the frozen suffix

* Replacing the position-32 resid_post_1 vector by itself must reproduce the model's position-32 logits within **1e-5** absolute in float32, on every validation history.
* Positions < 32 must be unchanged.
* At ln_final_out, the final effective-null projection must leave the centred logits unchanged within **1e-8** in float64.
* Any failure stops the run.

### G3 — erasure success, with remaining information reported

* **Eraser:** a continuous-target linear concept eraser (oblique LEACE form) fitted on calibration (h, m32): x′ = x − W⁺ P W (x − μ). The lost rank is ≤ 2 and is recorded together with ‖·‖.
* **Linear success [P]:** a ridge refit on erased calibration features scores validation R²(m32) **≤ 0.05** in every model.
* **Nonlinear residual (fixed probe, reported).** A predeclared nonlinear probe is applied to erased features: an RBF random-feature ridge with 2,048 features, bandwidth set by the calibration median heuristic and λ grid as above. If its validation R²(m32) is **≥ 0.25 [P]**, any positive result is limited to the "linearly accessible component", and no claim of erased circle information is made.
* **Downstream (descriptive).** Recoverability of m32 at resid_post_3 after the patch, which shows whether the information is recomputed downstream.

### G4 — matching of controls

* **Random erasers.** 20 random rank-matched oblique projections, fit-free, drawn in the calibration-whitened space. They are accepted only if their mean per-history L2 displacement on calibration is within **5%** of the primary eraser's, with at most 10,000 draws per model.
* **Predictive-damage profile, reported for every eraser:**
  - validation drop in ridge decodability of oracle Q1 from the erased h;
  - centred-logit displacement;
  - next-symbol entropy change.
* **Specificity failure.** If the m32 eraser's Q1-decodability loss exceeds the generic-predictive control's by more than its own effect margin, specificity is withheld.
* **Unmatched controls.** If no family can be matched, that comparison is INCONCLUSIVE and the raw damage curves are kept.

### G5 — support

* Ledoit–Wolf Mahalanobis distance of patched vectors relative to the calibration distribution.
* **Pass [P]:** the fraction of patched validation vectors beyond the calibration q99 is **≤ 5%** for the primary eraser, and **≤ 2×** the median random-control rate.
* Also reported: kNN distance ratios and the pre-LN norm at resid_post_3.
* **Failure:** off-support patching makes the mechanistic result INCONCLUSIVE.

### Gate outcome

**FEASIBLE** requires G1-primary, G2, G3-linear, G4-random and G5 to pass in all three models. Otherwise the outcome is **NOT FEASIBLE** or **INCONCLUSIVE**, with the gate named.

After the gates: STOP for owner review, and freeze every transform, control, dose and threshold before any fresh-test sampling.

## 5. Interventions and controls on the fresh test (fixed after G1–G5)

| Intervention | Role |
|---|---|
| Identity / resume | reconstruction control (G2 on the test set; it must also pass) |
| **m32 linear eraser** | **primary** |
| 20 matched random erasers | primary comparison: mean ΔR |
| Shuffled-target eraser | specificity control: same fitter on permuted calibration targets |
| R1 last-symbol eraser | 2 leading calibration principal components of one-hot w32 |
| **Short-context eraser** (added) | m2 target, rank 2 |
| **r2 eraser** (added, secondary) | information beyond (w31, w32); only if the G1 r2 sub-gate passed |
| y control | non-periodic E_b[y]/11, rank 1. Compared against a rank-1 dose of the primary, never directly against rank 2. |
| Local-position eraser | rank-2 calibration principal components of b·(radius-1 neighbourhood incidence) |
| Generic predictive eraser | rank-2 calibration principal oracle-Q1 directions |
| Final effective-null projection | exact no-effect control at ln_final_out |
| Natural donor patch (secondary) | donor from calibration with the same w32 and nearest oracle belief; hybrid context may be off-manifold |
| Frozen vs refitted readout (secondary) | an affine head refit on intervened calibration features, scored on test. A rescue indicates decoder mismatch or surviving information; failure is not proof of loss. |
| Dose curve (secondary) | partial erasure at α ∈ {0.25, 0.5, 0.75, 1.0} for the primary and its matched randoms |

**PH manipulation check (separate, descriptive).** Leading-cocycle circular coordinates of resid_post_3 on two validation panels, before and after the primary eraser, using the frozen S7 estimator. This is a check that the manipulation changed the circle, never an outcome or a gate. Erasure is information removal, labelled B under X4_CAUSAL's manipulation types. A topology claim would need a separate, calibrated type-C manipulation, which is not planned.

## 6. Decision rule (unchanged H4C-F)

Per model r, define:

  D_r = ΔR_r(m32 eraser) − mean_k ΔR_r(random_k)

Its uncertainty comes from a 2,000-draw paired bootstrap over fresh-test trajectories. Canonical keys are resampled jointly across models and mapped to each model's history IDs.

* **SUPPORTED:** every model has D_r ≥ 0.01 nat and a bootstrap lower bound > 0, and all gates and the test identity check pass.
* **REJECTED:** some model's D_r upper bound is < 0.01 nat, with valid gates.
* **INCONCLUSIVE:** anything else, including failed alignment, reconstruction, decodability, matching or support.

The model is the replication unit, and three all-positive signs give only p = 0.125. There is no population claim.

The short-context, R1, y, local-position and generic-predictive results are reported as specificity evidence for the primary, but **they do not change the primary rule**.

**Reading the specificity evidence:**

* **Specificity claim allowed:** the primary exceeds both the short-context (m2) and R1 erasers' ΔR, with lower bound > 0, in every model.
* **Short-context explanation not excluded:** the m2 eraser matches or exceeds the primary.
* **Information beyond two symbols:** may be stated only if the r2 eraser is itself SUPPORTED by the same rule against its own matched randoms. It is still not long memory.

## 7. Stop conditions

1. **Any G1–G5 failure:** stop after the gate report. No test sampling and no retuning.
2. **G2 on the fresh test fails:** INCONCLUSIVE; stop.
3. **CPU cap reached:** the cap is 3 CPU hours for the whole execution [P], with 8 GB RAM. Report censoring; no automatic extension.
4. **After the single fresh-test evaluation:** STOP for owner review, whatever the outcome. No re-run, no new site, no new dose and no extra seeds.
5. **Any result:** no intervention outcome is promoted to a topology, H1-necessity or long-memory claim.

## 8. Owner decisions required before execution

1. **Gate thresholds:** approve or modify every **[P]** value (G1 0.50/0.10, G3 0.05/0.25, G4 5% and 10,000 draws, G5 5%/2×, budget 3 CPU h).
2. **Eraser:** approve the continuous-target oblique-LEACE form and the RBF random-feature residual probe (2,048 features, median bandwidth).
3. **New extraction:** approve extracting resid_post_1 (plus embed and resid_post_3 for descriptive checks) on the existing dev pools of the 3 step-5000 checkpoints. The step-0 checkpoints are optional and descriptive.
4. **Fresh test lineage:** approve 4,096 new trajectories per process under stream x4f-v1 with namespace code 6, or prefer another option (e.g., reusing a B2 pool, not recommended).
5. **Frozen-forward adapter:** approve a minimal learner-side function (see the implementation plan, §2). It is a module change subject to review and independent tests.
6. **Secondary analyses:** whether to keep the r2 eraser, the natural-donor patch, the refitted readout and the dose curves, or drop some to save cost.
7. **y control:** confirm the rank-1 comparison rule rather than forcing rank 2.
8. **Sequencing:** confirm that execution is split into (a) gates on calibration/validation followed by a stop, and (b) a separately approved fresh-test run.
