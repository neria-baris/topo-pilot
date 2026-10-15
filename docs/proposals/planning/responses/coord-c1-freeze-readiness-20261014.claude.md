STATUS: FREEZE_READY

# C1 freeze-readiness: crossed counterfactual state forcing (Claude planning track L)

Planning only. Responds to `planning/requests/coord-c1-freeze-readiness-20261014.md`. Binding authority: `archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md` part B3 item C, and the owner research charter in `NEXT_RESEARCH_AND_WORKFLOW.md`. Shared input: the Codex draft `fc2c107:docs/proposals/CAUSAL_CIRCLE_STATE_FORCING_PROTOCOL_DRAFT.md`. I ran no Python, sampling, inference or training, opened no `payload.npz` or `state.pt`, and made no git writes. This is the only file I wrote. No commit or sha exists for it, because the hard rules for this track forbid git writes.

FREEZE_READY means every parameter, tolerance, seed, split, gate order and decision boundary below is fixed, and no step needs a choice that could be made after seeing data. It does not replace the independent clean-context review that the request announces. Section 15 lists the defaults that the reviewer should challenge first.

## Summary (≤ 300 words)

The test asks whether the final readout of each E4 cylinder-O model (seeds 1729/2718/3141, step 5000, `resid_post_3`, index 32) uses the learned circular phase in the direction the exact oracle prescribes.

**Donors.** Each new history H gets two deterministic donors H^±: canonical x-centre of w1..w31 shifted by ±1 (±2 cells), w32 kept. Oracle predictives q^± are recomputed from the full donor prefixes.

**Forced state.** Only the chart phase moves: a^± = a + B[f(φ^±) − f(φ)].
- φ: the frozen K4 PH chart; φ^±: its reading of the model's own donor activation; f(φ) = (cos φ, sin φ).
- B: first-harmonic block of a symbol- and nuisance-adjusted Frisch–Waugh regression fitted on calibration.

**Statistic.** The crossed regret contrast A = ½⟨q⁺−q⁻, log p⁺ − log p⁻⟩ (mismatched minus matched KL). It cancels exactly every target-independent effect of the moves: damage, flattening, LayerNorm scale.

**Controls.** 32 frozen Haar-random frames carry the same whitened displacement coordinates into random planes of the within-class whitened space. Per-row norm and displacement spectrum match exactly by construction. Damage and support are gated on calibration (early stop) and again on validation.

**Endpoint.** θ = E[A_T − mean_r A_{C_r}] / E[G], with G = ½ Jeffreys(q⁺, q⁻). The decision uses the Fieller-equivalent score Z = Y − 0.10·G: joint whole-row bootstrap, Bonferroni 0.05/3. PASS needs the lower bound above 0 in all three models.

**Gates before the fresh test:** oracle headroom; donor eligibility; chart availability and registration; manipulation; decoder adequacy; damage and support matching; positive control (full donor). Validation precision then sets N_test ∈ {4096, 8192, 16384}.

**PASS licenses one claim:** this phase component is used by the final readout, in the oracle's direction, for this counterfactual family. Not necessity, topological necessity, long memory, upstream mechanism or predictive repair.

---

## Request-1 item map

| Item | Where |
|---|---|
| 1 Exact nonlinear probe family | §7.1 |
| 2 Matching of information damage; intended changes vs damage; early stop | §6, §7.2–7.3, §10 |
| 3 Support and counterfactual alignment; eligibility; how the forced state is built | §4, §5, §8 |
| 4 Single endpoint, precision, decision rule, what each outcome licenses | §9 |
| 5 Seed maps, chart identity, ID binding, fresh test | §2, §3, §11 |
| 6 Six-field reuse assessment | §13 |
| 7 Staged plan with CPU | §12 |

---

## 1. Question, estimand and competing explanations

**Question (charter Priority 2).** In the three original E4 cylinder-O models, does the final readout functionally use the learned circular phase at `resid_post_3`/p32 for next-symbol prediction, in the direction an exact counterfactual oracle prescribes? The alternative is that the circle is only decodable there (R² ≈ 0.997 for m32 is already known).

**Why this site, and what that limits.** `resid_post_3` is the last block. At index 32 the only downstream computation is `ln_final` followed by `unembed`, so the test concerns use by the trained readout. That question is not trivial:
- the readout of a 128-dimensional residual into 36 symbols has effective rank ≤ 35 after removing the softmax shift, so at least 93 directions are invisible to the readout;
- a perfectly decodable circle can therefore lie entirely in directions the readout ignores.

The test says nothing about how earlier blocks compute the phase.

**Competing explanations, and what separates them.**

| | Explanation | Prediction for A_T | Prediction for the controls |
|---|---|---|---|
| E1 | Directional use: the readout maps changes of chart phase to predictive changes aligned with the oracle | A_T ≫ 0 | mean A_C ≈ 0 |
| E0 | Detectable only: the phase lies in directions the readout ignores | A_T ≈ 0 | ≈ 0 |
| E2 | Generic displacement or damage: moves change predictions without regard to direction (flattening, LN scale, off-support distortion, nuisance damage) | Removed exactly by the crossed contrast (§9.1); any residual interaction is estimated by the matched family | same |
| E3 | Nuisance channel: the move also shifts y-related nuisance in the counterfactual direction, and the readout uses that | Bounded by the leakage gate (§7.3) | |
| E4 | Short-context channel: within-symbol phase mostly carries w31 information | **Not separated.** This is a stated limit (§9.4) and a question for Priority 1 / K4 | |

**Estimand.** For model j, over rows that are naturally sampled and oracle-eligible:

θ_j = E[Y_j] / E[G]

with Y and G defined in §9. A value θ_j = 1 means the phase-only move reproduces, beyond the controls, as much counterfactual discrimination as the oracle itself has. Everything is conditional on:
- the frozen chart;
- the calibration fits;
- the 32 frozen frames.

The study tests *causal efficacy* (setting the variable moves the output correctly). It does not test necessity: nothing is removed.

## 2. Fixed objects and identities

**Models.** All IDs are taken from the K4 `CONTRACT.json` and must be re-verified at the start of stage S4.

| Seed | Checkpoint (step 5000) | EmissionSpec |
|---|---|---|
| 1729 | c3358e3cb9c352fb | 3633ac27dab50cf4 |
| 2718 | 98b0e703a337d513 | 97838b9e13a26f74 |
| 3141 | 036b670743ffbbaf | 8c29c329c197c79e |

- Shared objects: WorldSpec 21feee1d8ee5422e (12×12 cylinder; axis 0 periodic) and TransitionSpec e4dafc7b9785c172 (max-degree lazy walk, p_stay 0.2, uniform π).
- Read-only artifact root: `X:/Downloads/projects/topo-pilot/topo-pilot/artifacts`.
- The float32 state-dict sha256 is recorded before and after every stage, and must be unchanged.

**Numerics.** Every C1 forward pass uses an exact float64 cast of the frozen float32 weights:
- the model is in eval mode, with no_grad;
- the cast is exact because every float32 value is representable in float64;
- the float32–float64 logit discrepancy on validation is reported (expected ≤ 1e-4);
- an identity patch must reproduce the unpatched index-32 logits **bitwise**.

All oracle and endpoint arithmetic is float64.

**Chart identity, with fixed precedence:**
- **(a) Reuse K4.** If K4 job 0016 has produced certified chart and gauge artifacts (`chart_to_arrays` NPZ) for all three models, and their K4 chart gates (support, fidelity, bins, resultant) are PASS, C1 binds:
  - per model, the chart NPZ sha256;
  - the K4 CONTRACT sha256 and producer commit;
  - the K4 GATES.jsonl record.

  C1 loads them with `chart_from_arrays` and never refits them. The K4 landmarks are the 512 E4 test panel-1 rows. Those rows have been exposed, which is acceptable because they serve only as the coordinate system and never as C1 data.
- **(b) Stop.** If any K4 chart gate is FAIL or INCONCLUSIVE, C1 stops as CHART_UNAVAILABLE. The same method at the same site has already failed, and refitting until it passes is not allowed.
- **(c) Fallback.** If K4 never reached chart construction, C1 builds the chart once per model using:
  - the identical frozen `chart.py` and `cochain.py`;
  - the identical K4 chart parameters (field 47; largest strictly positive finite H1 bar; midpoint scale; certified integer lift with bounds [1, 2, 4, 8, 16]; 8-NN Gaussian extension; support |z| ≥ 0.2 and 8th-NN ≤ R);
  - landmarks = the 512 lowest-`sequence_id` natural rows of C1 calibration block 0, with the gauge fitted on their m32;
  - K4's validation gates, applied on the C1 validation block. The direct fidelity chart uses its 512 lowest-ID rows.

  At most six constructions are allowed. Failure means CHART_UNAVAILABLE. No other chart family, field, scale or site is permitted.

The gauge does not enter the endpoint: any rotation or reflection of φ is absorbed into B. The gauge is used only by the registration gate (§8.2).

## 3. Data splits and histories (all new; nothing exposed before)

All histories are sampled with the existing `HMMSampler` (canonical E, T, π) and converted to each model's named tokens with `named = symbol_perm[canonical]`. One set of canonical histories is shared by all three models. Rows are paired across models by `sequence_id`, and canonical 32-token digests must be identical across models.

Latent states are discarded immediately. Token column 33 (w33) is never read. No EvalSidecar is created or read.

| Split | Size | Blocks (4096 rows each) | Panels | Use |
|---|---|---|---|---|
| Calibration | 8192 | cal b0, b1 | 8 × 1024 | All fitting: Frisch–Waugh map, Σ_W, decoders, eligibility threshold, support q99. Early-stop matching gates. No logits are computed on calibration. |
| Validation | 4096 | val b0 | 4 × 1024 | All feasibility gates; positive control; precision projection. Validation endpoint means are written to a sealed file (§9.3). |
| Fresh test | N_test ∈ {4096, 8192, 16384} | test b0..b(k−1), k = N_test/4096 | — | The single endpoint evaluation. Sampled only after coordinator ACCEPT of the validation gate report. |

Fresh-test blocks are sampled in fixed 4096-row streams. The ladder therefore never changes which rows a block contains. This is needed because `HMMSampler` interleaves draws across rows: a sample of size n is not a prefix of a sample of size 2n.

**Separation checks** (pattern of X4-B2; identity-only access to old stores):
- sequence IDs are disjoint from every stored ObservationSet;
- there are 0 identical 32-symbol canonical windows shared with any E4 train, dev or test data, any X4/X4-B2/job-0014 pool, or between C1 blocks;
- the first-token χ² sampler check passes.

Any collision is a seed or lineage defect, and the study stops.

## 4. Counterfactual donors, oracle targets and eligibility

**Donor transform.** Canonical symbol j = 6a + b, where a is the x-centre index (centre x = 0.5 + 2a) and b the y-centre index. Then:

τ_k(j) = 6·((a + k) mod 6) + b, for k ∈ {+1, −1}

H^± = (τ_±(w1), …, τ_±(w31), w32).

The donor tokens are a pure deterministic function of the source tokens. Their per-row sha256 digests are recorded, and they are not stored as ObservationSets.

**Exact symmetry, verified at stage S3.** Let ρ_k(x, y) = ((x + 2k) mod 12, y). The checks are:
- T[ρz, ρz′] = T[z, z′];
- E_canon[ρz, τ_k(j)] = E_canon[z, j];
- π is uniform.

The maximum absolute deviation must be ≤ 1e-15. Consequences:
- b_t(τH_{1:t}) = ρ b_t(H_{1:t}) holds exactly for t ≤ 31;
- because w32 is kept, b32(H^±) ∝ (ρ_± b31(H) T) ⊙ E_canon[:, w32]. This is **not** a rotation of b32(H).

The donor posterior is computed directly with `BayesFilter` and checked against this closed form to ≤ 1e-12.

**Oracle targets** (canonical order; mapped to each model's named order by q_named[perm[j]] = q_canon[j]; cross-checked against direct named-space filtering to ≤ 1e-12):

| Symbol | Definition |
|---|---|
| q_i⁰ | b32(H_i) T E_canon |
| q_i^± | b32(H_i^±) T E_canon |
| G_i | ½ Σ_v (q_i⁺ − q_i⁻)(v) · (log q_i⁺ − log q_i⁻)(v) ≥ 0, i.e. half the Jeffreys divergence |

Exactly one transition follows the posterior, then one emission. Every entry is strictly positive because the emissions are softmaxes; nothing is floored or clipped.

**Support of the counterfactual prefix (oracle-only eligibility).** The only implausible step in H^± is the last one. Under the symmetry, p(τ w1..w31) = p(w1..w31) exactly. The plausibility of the donor is therefore measured exactly by its last-symbol surprisal:

s_i^± = −log q_31(H_i^±)[w32] = `BayesFilter.run(...).ce[:, 31]`

- **Threshold.** s_max is the 0.999 `inverted_cdf` quantile of the natural surprisal s_i = −log q_31(H_i)[w32] over the calibration rows. It is computed at S3, frozen, and depends only on the oracle.
- **Eligibility.** A row is eligible iff s_i⁺ ≤ s_max and s_i⁻ ≤ s_max. The rule uses no model outputs and is applied identically to every split. The estimand is defined on eligible rows.
- **No other exclusion.** Model-side support (§8) is gated as a fraction and never used to remove rows.

## 5. Constructing the forced state (symbol- and nuisance-adjusted first-harmonic map)

Notation, per model and per row:

| Symbol | Meaning |
|---|---|
| a_i | natural activation at `resid_post_3`, input index 32 (history position p32) |
| a_i^± | the model's activation on the donor H_i^± |
| φ_i^S = φ(a_i), φ_i^± = φ(a_i^±) | phases from the frozen chart extension (§2) |
| f(φ) | (cos φ, sin φ) |

**Fit, on calibration natural rows only, by ordinary least squares.**

a_i = Σ_w α_w·1[w32(i) = w] + Γ z̃_i + B f(φ_i^S) + ε_i

- The design matrix is 41 columns × 8192 rows: 36 symbol indicators (no global intercept), 3 nuisance covariates and 2 phase columns.
- z = (ȳ, Var y, ‖m32‖) from b32. These are oracle features of the public prefix, standardised with calibration means and SDs.
- Solve with `numpy.linalg.lstsq`. Require full column rank 41, condition number ≤ 1e8, and σ_min(B)/σ_max(B) ≥ 1e-6. Otherwise the status is PATCH_MODEL_DEGENERATE and the study stops.

**Why this regression.** Because of Frisch–Waugh–Lovell, B is identified only from *within-symbol*, nuisance-adjusted covariation of the activation with the chart phase. That is exactly the variation the w32-preserving donors change. The 6 x-centre columns give 6 distinct tangent directions in R², so B is identified.

**Within-class covariance.**
- r_i = a_i − α̂_{w32(i)} − Γ̂ z̃_i. This keeps the phase term and ε.
- Σ_W = the Ledoit–Wolf covariance of r on calibration, from the existing `x4f_scores.ledoit_wolf`.
- W = Σ_W^{−1/2}, the symmetric inverse square root via `eigh`. Ledoit–Wolf guarantees positive definiteness; λ_min ≤ 1e-12·λ_max gives SUPPORT_DEGENERATE.

**Primary forced states.**
- Δ_i^± = B [f(φ_i^±) − f(φ_i^S)]
- a_{T,i}^± = a_i + Δ_i^±
- Every other position and every weight is unchanged.

The move is a nonlinear function of the activations, through the chart. It is state forcing, not erasure.

**Patched pass.** The reference path is `learner.forward_with_patch(model64, [BOS, named w1..w32], "resid_post_3", 32, a_forced)`, reading logits[:, 32]. It is used for every row for S, D± and T±. Two path checks:
- **Identity patch:** must equal the unpatched logits bitwise.
- **Zero patch:** Δ = 0 gives A = 0 exactly.

A tail path, `model.unembed(model.ln_final(a))` using the model's own modules, may be used only for the control frames. Before that, it must equal `forward_with_patch` within 1e-12 on every validation and test row for T±. This is exact in principle, because no block follows `resid_post_3`.

**Positive control.** p^{D±} = the model's own prediction on H^±. At this final site, this is the full donor-state replacement.

## 6. Random control family: isometric random-frame transplant (matched by construction)

**Construction.**
- Q̃ = an orthonormal basis of span(W B), from QR (128×2).
- Primary whitened coordinates: c_i^± = Q̃ᵀ W Δ_i^± ∈ R². These are exact, since WΔ ∈ span(WB).
- For r = 0..31: draw G_r ∈ R^{128×2} with i.i.d. N(0,1) entries from the frame stream (§11). Take the QR decomposition G_r = U_r R_r and set Q̃_r = U_r·diag(sign diag R_r). This is a Haar 2-frame. No draw is rejected or regenerated, and none is selected.
- Control displacement: Δ_{r,i}^± = W^{−1} Q̃_r c_i^±; control state: a_{C_r,i}^± = a_i + Δ_{r,i}^±.

**Identities, which hold exactly and are checked to 1e-10 relative:**
1. **Norm, per row:** ‖WΔ_{r,i}^±‖ = ‖c_i^±‖ = ‖WΔ_i^±‖.
2. **Variance:** the whitened displacement second-moment matrix, centred or not, is Q̃_r S Q̃_rᵀ with S = Σ c cᵀ. It has the same eigenvalues as the primary's Q̃ S Q̃ᵀ, so trace and spectrum match exactly.
3. **Pair structure:** the ± arms of a row are mapped by the same frame.
4. **Symmetry:** the expectation of Δ_{r,i} over Haar frames is 0.

Information damage and support are not identities; they are measured and gated (§7, §8).

**Metric choice (a deliberate default; see §15).** "Norm" means the within-class Mahalanobis norm.
- This metric makes the norm requirement and the support requirement coincide, and it is invariant to the anisotropic scale of the residual stream.
- Matching raw L2 norm with random directions would push controls far off-support along low-variance directions. That is the mirror image of the X4-F family mismatch.
- The raw-norm ratio mean‖Δ_C‖/mean‖Δ_T‖ is reported per frame. It is not gated, because under the crossed contrast it affects variance, not bias (§9.1).

**What the family adds.** Because the crossed contrast cancels effects that do not depend on the target, the family is an empirical *placebo*:
- under E0, E1 and E2 its mean A is expected to be ≈ 0;
- any systematic alignment that generic matched moves do produce, for example through LayerNorm interactions or a frame overlapping readout structure, is subtracted.

## 7. Nonlinear probes, information damage, intended changes

### 7.1 Probe family (all fixed in advance)

**Class.** Random Fourier features (an approximate Gaussian kernel) followed by affine ridge regression.

**Inputs.** Activations a ∈ R^128, standardised with calibration mean and SD (`x4f_scores.standardizer`).

**Features.**
- ψ(a) = sqrt(2/2048)·cos(ãΩ + β), with 2048 features, Ω ~ N(0, ℓ⁻²I) and β ~ U[0, 2π).
- Built with `rbf_bandwidth`, `rbf_map` and `rbf_features` (from `x4f_scores`, unchanged).
- ℓ = the median pairwise distance among 1024 calibration rows drawn by the bandwidth stream. ℓ ≤ 1e-12 gives RBF_DEGENERATE and the study stops.

**Ridge and selection.** λ ∈ {1e-3, 1e-2, 1e-1, 1, 10}.
- λ is selected by leave-one-panel-out over the 8 calibration panels, using `x4f_probe.nested_ridge` unchanged; ties go to the larger λ.
- The refit on all calibration rows uses `standardizer` on the features plus `prediction.ridge.RidgeProbe([λ*])` (public; same affine semantics), so that the frozen predictor can be applied to many patched sets.
- Equivalence to `nested_ridge`'s own validation predictions is required to within 1e-10.

**Fit split.** Calibration natural source activations only. No donors, no patched states, no validation rows.

**Targets, one decoder each:**

| Decoder | Target | Decoded quantity |
|---|---|---|
| (i) | w32 one-hot (36 columns) | ŵ = argmax; ties go to the lowest index |
| (ii) | the full 12-state y-marginal of b32 (12 columns) | ŷ |
| (iii) | m32 (2 columns) | target diagnostic only; never part of a gate on damage |

**Adequacy gate M4 (validation, unpatched).** Accuracy of ŵ ≥ 0.95, and `r2_pooled`(ŷ) ≥ 0.50. Otherwise DECODER_INADEQUATE: damage cannot be measured, so the study is INCONCLUSIVE.

### 7.2 Damage metric (fixed decoders reading the patched state)

**Why fixed decoders.** State forcing is a known, nearly invertible shift. Whether a *refitted* decoder could still recover a variable is therefore not the relevant notion of damage. What matters for a frozen downstream is how fixed decoders *read* the forced state. Refit recoverability is not used.

For an intervention X ∈ {T, C_0, …, C_31}, on a split with n rows:

- D_w(X) = (1/2n) Σ_{i,±} 1[ŵ(a_{X,i}^±) ≠ ŵ(a_i)] (fraction of rows whose decoded last symbol changes)
- D_y(X) = (1/2n) Σ_{i,±} ‖ŷ(a_{X,i}^±) − ŷ(a_i)‖² / tr Cov_cal(y-marginal) (normalised shift of decoded y-nuisance)
- Family value: D(C̄) = mean over r of D(C_r).

**Gate M2.** It runs on calibration first, which is the early stop: no logits exist at that point. It then runs again on validation, per model.

| Requirement | Bound |
|---|---|
| Ceilings for the primary and the family mean | D_w(T) ≤ 0.02, D_y(T) ≤ 0.05; D_w(C̄) ≤ 0.02, D_y(C̄) ≤ 0.05 |
| Matching | \|D_w(T) − D_w(C̄)\| ≤ 0.01 and \|D_y(T) − D_y(C̄)\| ≤ 0.02 |
| Dispersion | ≥ 28 of 32 frames individually within the ceilings. No frame is dropped; this only checks that outliers do not dominate the family. |

Failure gives FAMILY_UNMATCHED and the study stops, with no redraw and no retuning.

### 7.3 Intended changes versus damage

| Kind of change | Classification |
|---|---|
| Chart phase; m32 direction; circle radius ‖m32‖; 2nd and 3rd x-harmonics | **Intended or allowed**: they belong to the circular variable being moved. Radius and harmonic changes are reported as "circle-state fidelity" and are not gated. |
| Last symbol w32 | **No change intended** (the counterfactual keeps it). Any decoded change is damage. |
| y-marginal | **No change intended by the intervention.** Any decoded shift counts as damage in D_y. This is conservative. |

**Counterfactual-implied nuisance change** (oracle side):
- ν^± = the y-marginal of b32(H^±);
- κ_ν = mean‖ν⁺ − ν⁻‖² / tr Cov_cal(ν).

This is the part of the counterfactual that a phase-only intervention cannot, and should not, reproduce. It caps θ below 1 and is reported.

**Leakage (explanation E3):**

L(X) = Σ_i ⟨ŷ(a_{X,i}⁺) − ŷ(a_{X,i}⁻), ν_i⁺ − ν_i⁻⟩ / Σ_i ‖ν_i⁺ − ν_i⁻‖²

- If κ_ν ≥ 0.01, gate M2 also requires L(T) ≤ 0.25 on validation. Otherwise NUISANCE_CONFOUNDED: the primary could succeed through a y-channel.
- If κ_ν < 0.01, L is reported only.

## 8. Support and counterfactual alignment

### 8.1 Gate M3: support of the forced states (calibration early stop, then validation)

**Within-class Mahalanobis distance:**

D_M(a; w, z̃) = ‖W(a − α̂_w − Γ̂ z̃ − r̄_cal)‖

- It uses the source row's w32 and z̃; for natural donor states, the donor's own z̃.
- q99 = the 0.99 `inverted_cdf` quantile over calibration natural rows.
- The existing `ledoit_wolf`/`support_report` machinery is applied to the residualised arrays.

**Fractions beyond q99:** F(S), F(D) (pooled over ±), F(T), and F(C̄) (mean over frames).

**Requirements, all of which must hold:**
- F(T) ≤ max(0.05, F(D) + 0.02). The forced state must be no less supported than the model's own state on the counterfactual prefix, which is itself an unusual history.
- F(C̄) ≤ max(0.05, F(D) + 0.02).
- |F(T) − F(C̄)| ≤ 0.02.
- K4 chart support (|z| ≥ 0.2 and 8th-NN distance ≤ R) holds for ≥ 0.98 of the T and C̄ states, and for ≥ 0.99 of the S states and ≥ 0.98 of the D± states on validation.

No row is ever removed. Unsupported rows keep their phase arg z and stay in the endpoint.

### 8.2 Gate V1 (validation): the chart registers the counterfactual

- δ_i = wrap(φ_i⁺ − φ_i⁻) ∈ (−π, π].
- δ*_i = wrap(arg m32(H_i⁺) − arg m32(H_i⁻)), from the oracle, in the gauge orientation.
- Among rows with |δ*_i| ≥ median|δ*|, the fraction with sign(δ_i) = sign(δ*_i) must be ≥ 0.75. sign(0) counts as disagreement.

Otherwise CHART_NOT_REGISTERING. The primary moves would then be uninformative, and a FAIL could not be read.

### 8.3 Gate V2 (validation): manipulation, i.e. the intervention implements the phase change

- d_i^± = wrap(φ_i^± − φ_i^S); e_i^± = wrap(φ(a_{T,i}^±) − φ_i^S).
- Progress ratio κ = Σ_{i,±} e_i^± sign(d_i^±) / Σ_{i,±} |d_i^±|. Require 0.5 ≤ κ ≤ 1.5.
- Among arms with |d| ≥ median|d|, the fraction with sign(e) = sign(d) must be ≥ 0.80.
- κ for the controls is reported (expected ≈ 0).

Absolute angle thresholds such as π/12 are not used, because the shifts within a symbol are small.

### 8.4 Gate V3 (validation): positive control

- A_full,i = ½⟨q_i⁺ − q_i⁻, log p_i^{D+} − log p_i^{D−}⟩.
- θ_full = E[A_full]/E[G].
- Require the lower bound of Z_full = A_full − 0.30·G to be > 0 at 0.05/3 (bootstrap seed 520504).

Otherwise MODEL_HEADROOM: the model itself does not discriminate the two counterfactuals, so no phase test can be read.

## 9. Endpoint, precision and decision

### 9.1 Per-row statistic (crossed regret contrast)

For a pair of interventions X = (X⁺, X⁻), with p from the patched pass in canonical order:

A_i(X) = ½ Σ_v (q_i⁺ − q_i⁻)(v) · [log p_{X⁺,i}(v) − log p_{X⁻,i}(v)]
       = ½[KL(q⁺‖p_{X⁻}) + KL(q⁻‖p_{X⁺})] − ½[KL(q⁺‖p_{X⁺}) + KL(q⁻‖p_{X⁻})]

That is, mismatched regret minus matched regret against the exact oracle. Its properties:
- If p_{X^±} = q^±, then A = G. The oracle's own discrimination is the margin.
- If a move changes log p by a term that does not depend on the target, the term appears identically in both brackets. Damage, flattening and global scale effects therefore cancel **exactly**.
- If p_{X⁺} = p_{X⁻}, then A = 0.

**Endpoint quantities:**
- Y_i = A_i(T) − (1/32) Σ_r A_i(C_r)
- θ_j = E[Y]/E[G]
- Z_i = Y_i − c·G_i, with c = 0.10

### 9.2 Precision method (Fieller-equivalent; ratio problem removed)

**Equivalence.** The headroom gates guarantee E[G] > 0, so θ_j > c ⇔ E[Z_j] > 0 and θ_j < c ⇔ E[Z_j] < 0. The decision is made on a *mean*. Inverting this test at the margin is exactly Fieller's test, so no delta-method approximation is needed for the decision.

**Fresh-test bootstrap.**
- 5000 draws, PCG64 seed 520503.
- Per draw: one call `idx = rng.integers(0, n, size=n)`, shared by every model and every array (K4 convention).
- Per model: Z̄*.
- L_j = quantile_{0.05/3}, U_j = quantile_{1−0.05/3}, both `inverted_cdf`.
- θ̂ = Ȳ/Ḡ is reported with intervals from the same draws (ratio of resampled means). These intervals are descriptive only.
- The randomness of frames and calibration is held fixed: inference is conditional on them.

**Validation precision (gate P1)** reuses `tools/x4_circle_history/precision.py` unchanged:
- `sd_b4_draws(X = {j: Z_val}, r4n = {j: G_val}, models, seed = 520501, draws = 5000, size = n_val)`;
- `centered_draws(X, models, seed = 520502, draws = 5000, size = N)`;
- `precision_summary` with cfg = {alpha: 0.05/3, power: 0.80, delta: 0.0, alternative: (0.20 − 0.10)·Ḡ_val, projected_N: N}.

N_test = the smallest N in {4096, 8192, 16384} with status PASS. If none passes: UNDERPOWERED, and the study stops. Only SDs and centred errors drive this choice, never the validation mean.

### 9.3 Decision rule (strict) and what it licenses

**Per model:** PASS_j ⇔ L_j > 0; FAIL_j ⇔ U_j < 0; otherwise INC_j.

**Overall:**
- **PASS** iff PASS_j for all three models. This is an intersection–union rule, so it is valid at the stated level. Bonferroni is kept for consistency with K4.
- **FAIL** iff FAIL_j for all three.
- **MIXED/INCONCLUSIVE** otherwise. Per-model statuses are reported, and no winner is selected.

**Numerical certificate.** Each row gets a float64 error bound, |err A_i| ≤ ‖q⁺ − q⁻‖₁·max|err log p| from max|logit|. Any |L_j| or |U_j| within 1e-9 of 0 gives INCONCLUSIVE_NUMERICAL.

**Sealed validation means.** The point estimates of θ and θ_full on validation go to a sealed file, opened only after the fresh result is recorded.

**Secondary quantities** (reported; never part of the decision):
- θ_full;
- the phase share ψ = θ/θ_full;
- repair R = ½Σ_± [KL(q^±‖p_S) − KL(q^±‖p_{T^±})];
- the per-frame A_C;
- κ_ν and L;
- radius and harmonic fidelity;
- the raw-norm ratio;
- Y against |d| (descriptive).

**PASS licenses.** In each of the three E4 cylinder-O models at `resid_post_3`/p32, forcing the learned PH-chart phase toward the phase the model assigns to a ±2-cell x-translated prefix (w32 kept) moves the next-symbol distribution in the oracle's counterfactual direction. It does so by at least 10% of the oracle's own discrimination, beyond matched random-frame moves. In other words, the final readout functionally uses this phase component in an oracle-consistent way, for this counterfactual family, conditional on the declared gates.

**FAIL licenses.** At this site and with this operationalisation, phase-only moves along the fitted map do not reach 10% of oracle-aligned discrimination beyond the controls in any model. That is a scoped lack of *practical* support.

**Neither licenses:**
- H1 or topological necessity, or any claim about square worlds;
- that the circle is the only carrier, or that it is necessary;
- the upstream mechanism;
- long memory, or separation from w31 or short-context information (E4 explanation);
- predictive repair (that is the secondary R);
- generalisation to other counterfactuals, sites, checkpoints or natural language;
- a literal internal circular variable.

A FAIL does not show that the circle is epiphenomenal: other sites, harmonics or nonlinear operationalisations remain open.

**INCONCLUSIVE and gate failures license only "assay infeasible as specified".** X4-F stays INCONCLUSIVE/FAMILY_UNMATCHED, and the E4 G-H FAIL and other frozen verdicts are untouched.

## 10. Gate order (first failure stops; early stop before any regret)

| Order | Stage | Gate | Pass condition | Status on failure |
|---|---|---|---|---|
| 1 | S3 (oracle only) | H0 | All of: symmetry ≤ 1e-15; BayesFilter vs 60-digit decimal reference on the 4 lowest-ID rows per split for H, H⁺, H⁻ (posterior ≤ 1e-12; predictive computed in Decimal ≤ 1e-12); separation clean; eligible fraction ≥ 0.90 on calibration and on validation; one-sided 0.05 lower bound of Ḡ_val > 0.01 nat (`oracle_profile.bootstrap_profile`, seed 520505) | HEADROOM / ELIGIBILITY / IDENTITY |
| 2 | S4 (cal) | Identities, C0, M1 | Checkpoint and EmissionSpec identities; chart available (§2); M1 holds (norm and spectrum identities, frame orthonormality, identity/zero patch on a 1024-row cal subset); FWL non-degenerate | as named |
| 3 | S4 (cal) | M2, M3 | §7.2, §8.1 — **early stop; no logits computed** | FAMILY_UNMATCHED / SUPPORT |
| 4 | S5 (val) | C0 support, M4, M2, M3 | as above | as named |
| 5 | S5 (val) | V1, V2 | §8.2, §8.3 | CHART_NOT_REGISTERING / MANIPULATION_FAILED |
| 6 | S5 (val) | V3 | §8.4 (donor logits only) | MODEL_HEADROOM |
| 7 | S5 (val) | P1 | §9.2 (primary and control logits computed here for the first time) | UNDERPOWERED |
| 8 | S7 (fresh) | Pre-scoring T-gates | All computed before Z: identities and separation; eligible fraction within ±0.02 of validation; one-sided 0.05 lower bound of Ḡ_test > 0.01 (seed 520506); C0 support, M1–M3, V1–V3 with the same tolerances | INCONCLUSIVE_TEST_GATE: endpoint not scored; arrays sealed and kept |
| 9 | S7 | Endpoint | §9.3 | — |

## 11. Seed map and identity binding (frozen at contract freeze)

| Purpose | Stream or seed |
|---|---|
| Histories | `SeedTree(0).generator("data", "c1-sf-v1", split, block, "cylinder", "overlap", "1.25")`. split ∈ {cal, val, test}; cal blocks 0–1, val block 0, test blocks 0–3 (only 0..k−1 sampled) |
| Sequence IDs | `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c1-sf-v1/{split}/b{block}"), "test", 4096)`. Split label `test`, as in the X4-B2 pools; distinct process codes |
| Control frames | `SeedTree(0).generator("c1-sf-v1", "frame", model_seed, r)`, r = 0..31 |
| Random Fourier features | `SeedTree(0).generator("c1-sf-v1", "rbf", model_seed, target)`; bandwidth subsample `(... "rbf_bandwidth", model_seed, target)` |
| Bootstrap (PCG64 integers) | 520501 val SD; 520502 val centred; 520503 fresh endpoint; 520504 val V3; 520505 S3 headroom; 520506 fresh pre-scoring |

The issued seed maps are saved with every artifact (`SeedTree.issued`).

**Binding record** (C1 `CONTRACT.json`):
- protocol sha256;
- producer commit and environment identity (`env_identity.py`);
- model, checkpoint, EmissionSpec, WorldSpec and TransitionSpec IDs, plus the float32 state-dict sha256;
- `symbol_perm` digests;
- K4 chart NPZ sha256 values plus the K4 CONTRACT/commit/gate record, or for fallback (c) the C1 chart sha256 values;
- C1 ObservationSet and HistoryIndex IDs per (split, block): panels of 1024 rows, `end` = 32;
- per-row canonical digests of H, H⁺ and H⁻;
- s_max, the FWL coefficients, Σ_W, W, the decoder weights and every q99, each with sha256 after its stage;
- the release IDs.

**Store.** An independent store at `X:/Downloads/projects/topo-pilot/c1-state-forcing-store/`. The main store listing hash must be unchanged before and after.

## 12. Staged plan and rough CPU

Resources follow the owner override: no CPU-time cap, measured through the meter and a single ledger; ≤ 4 threads (torch and BLAS); ≤ 12 GiB; one scientific job at a time; outputs on X: only; safe STOP if C: < 2 GB or X: < 30 GB free. Real usage limits, STOP and existing latches always win.

**Cost basis:** about 54 MFLOP per full forward row; 1024-row batches; peak RAM < 4 GiB.

| Stage | Content | Rough CPU |
|---|---|---|
| S0 Written contract | Coordinator merges the two tracks into PROTOCOL + CONTRACT.json + API.md + TEST_PLAN.md → independent clean-context review → freeze (sha in the decision log) | documents only |
| S1 Independent tests | Two authors work from API.md alone, before any implementation. **A:** donor transform and symmetry on a tiny periodic HMM; closed-form donor posterior; crossed-contrast identities (A = G at p = q; exact cancellation of target-independent logit terms; A = 0 for equal arms); Fieller equivalence and decision boundaries; bootstrap index order; ladder logic; numerical certificate. **B:** FWL recovery of a known B in a noiseless synthetic case, plus a trap showing that sequential residualisation is wrong; Haar frame sign convention, isometry and isospectral identities, pair mapping; damage, leakage and support formulas with q99 `inverted_cdf`; manipulation and registration wrap at ±π, sign(0), median ties; gate order (no logits before M2/M3 pass; fresh Z not computed if a pre-scoring gate fails). Synthetic fixtures only. | ≤ 15 min technical (not scientific) |
| S2 Implementation | A separate builder in a new worktree from the accepted K4 head. Reuse per §13. At most 2 correction jobs per defect. | tests ≤ 15 min |
| S3 Oracle only (release R1) | Sample cal and val (12,288 rows); separation; symmetry; decimal reference; s_max; eligibility; G; gate H0 | ≤ 10 CPU-min |
| S4 Calibration (R2) | Extract S and D± (8192 × 3 passes × 3 models); chart (reuse, or fallback ≤ 30 min); FWL; Σ_W; decoders (LOPO, 2 targets plus the m32 diagnostic × 3 models); frames; M1–M3 on activations only | 30–60 CPU-min (+ ≤ 30 fallback) |
| S5 Validation (R2 continued) | Gates in §10 order. Full forward passes for S, D±, T± (4096 × 5 × 3 models); tail path for 64 control states per row; decoding and chart extension of ~270k states per model; bootstrap; P1; gate report; sealed means | 30–60 CPU-min |
| S6 Coordinator ACCEPT | Independent review of the validation gate report; release R3 names N_test | — |
| S7 Fresh test (R3) | Sample k blocks; separation; pre-scoring gates; endpoint; decision; immutable exports | 20–90 CPU-min (N_test 4096 → 16384) |
| S8 Report | Report, review, decision record, morning report | — |

Expected total scientific CPU: about 1.5–4.5 h.

## 13. Six-field reuse assessment (charter)

| Field | C1 |
|---|---|
| **Existing functions and artifacts (reused unchanged)** | **Process and data:** E4 WorldSpec, TransitionSpec, EmissionSpecs and checkpoints; `dataset.sampler.HMMSampler`; `dataset.checks.{process_code, make_sequence_ids, check_first_token, check_disjoint}`; `dataset.public.assert_public`; `contracts` (ObservationSet, HistoryIndex, SeedTree, SequenceLayout, ArtifactStore, tokens_hash). **Oracle:** `oracle.BayesFilter`; `tools/x4_oracle_profile/oracle_profile.py` (validate_process, canonical_emission, posterior_means, bootstrap_profile, percentile_interval); the independent decimal reference in `tests/oracle_profile/independent_reference.py`. **Model:** `activations.ActivationExtractor`; `learner.forward_with_patch` and its independent tests. **Chart:** `tools/x4_circle_history/chart.py` (chart_from_arrays, extend, chart_gates, agreement, phase_bin_counts; plus fit_chart/fit_gauge with `cochain.py` for fallback (c) only). **Statistics:** `tools/x4_circle_history/precision.py` (sd_b4_draws, centered_draws, precision_summary); `analysis.x4f_scores` (standardizer, r2_pooled, rbf_bandwidth, rbf_map, rbf_features, ledoit_wolf, support_report); `experiment.x4f_probe.nested_ridge`; `prediction.ridge.RidgeProbe`. **Runtime:** meter, ledger and guards in `tools/x4_oracle_profile/{meter, winjob, controls, runtime, freeze}` and `tools/x4_circle_history/{meter_bind, op_guard, env_identity, live_context, release, stage_records, run_tests_bind}`. **Separation-check pattern:** X4-B2. X4-F's `random_family`, its exports and its gate orchestration are **not** reused (they carry the dormant defects listed in the X4-F addendum §3). |
| **Missing capability** | (1) The deterministic donor transform with retained last symbol, and the symmetry check. (2) The symbol- and nuisance-adjusted FWL phase map and the forced-state construction. (3) The isometric random-frame family. (4) Damage, leakage, support, manipulation and registration gate kernels for forced states. (5) The crossed-contrast endpoint, Fieller score and decision. (6) A C1 history adapter (new streams → ObservationSet and HistoryIndex). (7) The C1 stage driver plus thin bindings for runtime modules that read their own job's CONTRACT. |
| **Smallest change** | One new package, `tools/c1_state_forcing/`, of pure kernels (arrays, config and injected guard/timer in; no hidden I/O or randomness), about 700–900 lines plus tests. Runtime modules are reused through module-level rebinding, the pattern `meter_bind` already uses for job 0014: rebind `CONTRACT`, the stage names and a "no CPU cap" stage allocation. If `meter_bind` cannot express "uncapped" by rebinding, the smallest change is an explicit `uncapped` value handled in a separately versioned C1 copy, with a regression test. The frozen K4 files are never edited (no retrofit). Nothing new is added to `src/`. |
| **Stable interfaces and invariants** | One site, model set and next-symbol endpoint. Donors keep w32. Fits and the gauge use calibration only. Canonical/named joins are exact, and rows are paired by sequence_id across models. No w33 and no sidecar. Weights frozen; identity patch bitwise. Maps, frames, seeds and artifacts are immutable. Gates run in a fixed order, and the first failure stops. Every row stays in the endpoint (no trimming). Stages cannot be retried (`stage_records`). |
| **Regression checks** | The full existing suite for learner, analysis and oracle-profile, plus the K4 chart/precision tests, must pass unchanged. The independent S1 tests come first. The equivalence of the tail path and `forward_with_patch`, and of the RidgeProbe refit and `nested_ridge`, is checked on real validation rows. Guard fault tests apply to any rebinding. |
| **Next plausible extension** | The same kernels can serve one separately reviewed follow-up without new abstractions. Examples: an earlier site, if a certified chart exists there, or a w31-retaining donor (H^± shifting w1..w30) to separate short from long history. No generic causal or topology framework. |

## 14. Risks and stop rules

**Risks (each ends INCONCLUSIVE with exact values preserved; none is rescued):**

| | Risk | Mitigation or consequence |
|---|---|---|
| R1 | The K4 chart is unavailable or failed | §2 (b): stop |
| R2 | The chart does not resolve shifts within a symbol (V1 or V2 fail): an 8-NN extension over 512 landmarks may be locally flat | Stop |
| R3 | Damage mismatch: random whitened frames hit nuisance directions that the FWL-adjusted primary avoids | M2 stops on calibration before any logit is computed |
| R4 | Low donor eligibility | Known at S3 for minutes of CPU |
| R5 | Model headroom (V3). Unlikely given R² 0.997 | Stop |
| R6 | Precision fails even at 16,384 rows | Stop |
| R7 | **Interpretation:** the phase within a symbol mostly carries w31 information (E4 explanation); the effect is confined to the readout at the final site | Stated limits, not gates |
| R8 | The single-ellipse map is misspecified | Judged by V2. The FWL within-class partial R² is reported against a per-x-column slope model, descriptively |

**Stop rules:**
- The first failed gate ends the stage. Outputs and negative findings are kept.
- No redraw, regeneration or selection of frames.
- No change of threshold, tolerance, chart, site, harmonic count or metric after any data are seen.
- At most 2 correction jobs per technical defect; then reformulate or stop and move to queue item D.
- Fresh rows are never added after the fresh test is seen.
- Any identity, lineage or numerical-integrity mismatch stops the study before classification.
- Usage limits, STOP, the disk thresholds and latches always win.
- Under B6 nothing here can change a published E4 claim. If a result appeared to, the coordinator would stop and wait for the owner.

## 15. Defaults the independent reviewer should challenge (non-blocking; all fixed)

1. **Within-class Mahalanobis isometry** as the matched "norm", with raw L2 reported. The alternative is raw-metric isometry with frames shaped by Σ_W. It matches raw norm exactly but leaves support to the gate.
2. **The crossed ± design** satisfies the owner's random-family requirement through a placebo whose mean is near zero (§6). The reviewer should confirm this reading of B3-C.
3. The margin c = 0.10, the planning alternative 0.20, the positive-control threshold 0.30, and the eligibility threshold (natural q0.999).
4. Including ‖m32‖ among the FWL nuisance covariates, which keeps the radius fixed in B.
5. The damage and support tolerances: 0.02 / 0.05 / 0.01 / 0.02 / 28-of-32 / 0.98.

---

## 16. Critique of the fc2c107 draft: kept, changed, why

**Kept:**
- the site, models and checkpoint;
- the same-last-symbol x-translation donor, in canonical space and converted per model;
- the oracle recomputed from the full donor prefix rather than assumed to be a rotation (the draft's correct observation that keeping w32 breaks equivariance);
- an exact expectation under q with no sampled w33, and no flooring;
- state forcing through a nonlinear chart rather than linear erasure;
- calibration-only fitting and gauge;
- identity and zero patches;
- full donor replacement as an engineering positive control;
- no trimming, a joint whole-row bootstrap, Bonferroni 0.05/3;
- validation precision before the fresh test;
- the rule against substituting an oracle angle for the PH chart;
- the staged path and the narrow claim language;
- X4-F left closed.

**Changed:**

1. **Single donor with a random-sign family → crossed ± donors.**
   - In the draft, the 32 sign fields have only two destinations, and about half reproduce the primary, so Y estimates ½[R(reflection) − R(T)] with added noise.
   - Y also mixes primary damage with control damage: the baseline cancels, and Y > 0 is possible while the primary worsens regret.
   - The crossed contrast A = ½⟨q⁺ − q⁻, log p⁺ − log p⁻⟩ applies both interventions against both targets. Effects that do not depend on the target therefore cancel *exactly*, and A = G for an oracle-perfect predictor gives a natural normalisation.
2. **Sequential residualisation and 12-bin centroids on raw φ → a joint FWL regression.**
   - At p32 the chart phase is largely determined by w32. Residuals with the symbol means removed, binned by *absolute* phase, average to roughly zero within each bin.
   - The draft's curve would therefore be attenuated and aliased with a six-fold period: the centroid of a bin mixes symbols whose centres lie on either side of it.
   - FWL identifies the within-symbol phase slope, which is what the w32-preserving donor changes.
3. **φ_D made explicit** as the chart reading of the model's own donor activation (an interchange of one scalar variable). A registration gate V1 was added, so that an insensitive chart cannot pass as a negative result.
4. **Controls: norm rescaling → an isometric Haar-frame transplant.**
   - The draft rescaled each control to the primary's Euclidean norm, which distorts the requested phase. It also required raw and whitened norms within 5% together, which cannot hold in general.
   - Isometric transplant matches the per-row norm and the full displacement spectrum exactly, with no rejection sampling. This addresses the X4-F G4 failure mode by construction rather than by luck.
5. **Damage: refit recoverability of the source target → fixed nonlinear decoders reading nuisance.**
   - The draft's refit notion comes from erasure. For an invertible state shift it is uninformative, and it also counted the intended phase change as damage.
   - The probe family is now fully specified and reuses the independently tested X4-F random-feature and ridge code.
   - Radius and harmonics are reclassified as part of the circular target, not as nuisance.
6. **The ratio-precision blocker** is resolved by Fieller equivalence (Z = Y − 0.10G). The K4 mean-only precision functions then become reusable unchanged, and the decision is exact at the margin.
7. **Headroom:** KL(q_D‖q_S) → half-Jeffreys between the ± donors. A **model-side** positive-control gate was added; without it, a FAIL could reflect a model that does not discriminate the counterfactual at all.
8. **Donor support:** "every donor ≤ 10 nats" was fragile, since one row anywhere stopped the test. It is replaced by an oracle-only eligibility rule referenced to the natural surprisal distribution, applied identically to every split, with fraction gates. This is legitimate because it uses no model output.
9. **Manipulation thresholds:** the absolute π/12 and π/6 are meaningless for small within-symbol shifts; a relative progress ratio replaces them.
10. **Sample size:** a fixed 4096 → a ladder projected from validation, with the fresh test sampled in fixed 4096-row blocks (prefix stability).
11. **Numerics:** float64 evaluation of the exact weights removes the open numerical-envelope item.
12. **Decision symmetry:** the draft's "upper < 0.10 in ANY model → FAIL" became per-model statuses, with FAIL only if all three fail and MIXED otherwise. This is consistent with K4.
13. **Chart reuse:** "reuse if accepted, else fit in this study" was made a three-way rule. A failed K4 chart stops C1 rather than inviting a refit until it passes.

**Kept as limits:** the claim stays at the level of the readout at the final site, with no necessity claim. The w31/short-context limit (E4 explanation) is added; the draft did not name it.

---

## 17. Request 2: D sketch (oracle only; B2 not reopened)

**Aim.** Construct a process in which a topological distinction is provably irrelevant to next-symbol prediction but relevant at horizon k > 1. Both constructions use one idea: the lazy walk moves at most one cell per step (a light cone), and the topological quantity is a **Z₂ holonomy**, the parity of seam crossings of the path. Neither touches the original cylinder-O process, horizon or screen that B2 closed.

### D-1: cylinder vs Möbius with a y-blind seam band (closest to existing machinery)

**Worlds.** 12×12 with axis 0 glued periodically (C, the existing cylinder) or with a flip, (11, y) ~ (0, 11 − y) (M). `QuotientLatticeBuilder` already supports `flipped`; only a three-line registered subclass is needed. Transitions: the existing max-degree lazy walk, D_max = 4, so every x-neighbour has probability (1 − p)/4 whatever y is.

**Emission.**
- Band S = {x ∈ {10, 11, 0, 1}}. For z ∈ S, emit the deterministic symbol β_x: x is exact, and nothing about y is revealed.
- Outside S, the existing overlap emission (σ = 1.25) over 36 symbols. Alphabet V = 40.

**Facts:**
- (F1) R(x, y) = (x, 11 − y) is an automorphism of both C and M, and preserves T and E (with the symbol relabelling b → 5 − b).
- (F2) In M, crossing the seam composes the y-coordinate with R.
- (F3) Inside S, the x-marginal is a lazy walk that does not depend on y, in both worlds, and x is observed exactly.

**Claim.** Let H be any positive-probability history that ends with β_x, x ∈ {11, 0} (the band interior, 2 steps from the nearest column outside the band). Then:
- (i) Q₁^C(H) = Q₁^M(H) exactly.
- (ii) Take H with no earlier band visit, a y-belief at band entry that is not R-symmetric, and an odd number of seam crossings inside the band. Then Q₂^C(H) ≠ Q₂^M(H).

**Proof sketch.**
- (i) w_{t+1} is emitted from S with probability 1 (F3 plus the light cone). Its law depends only on the x-belief, which is identical in both worlds.
- (ii) Exit to x = 9 or x = 2 at step 2 has probability ((1 − p)/4)² > 0. There, the emission depends on y. In M the y-belief is R applied to the C belief (F2); within the band, a path between the two sides crosses the seam an odd number of times. The total-variation gap is at least ((1 − p)/4)² · TV(E_out(·|ρ), E_out(·|Rρ)) > 0 for a non-symmetric ρ.

The orientability of the world (a topological invariant) is therefore invisible at horizon 1 throughout the band interior and visible at horizon 2.

**Oracle-only check.**
1. Build T and E for both worlds; `validate_process`; verify F1 exactly (≤ 1e-15).
2. Construct three explicit witness histories (a prefix fixing y, band entry from x = 9, then β10, β11, β0).
3. Compute Q₁, Q₂ and Q₃ with `BayesFilter`/`FutureOperator`. Horizon 2 has 40² = 1,600 entries.
4. Report max|ΔQ₁| (≤ 1e-15) and the gap at horizon 2, against the closed-form lower bound.
5. Sample 16,384 histories with `HMMSampler` and report the fraction that end in the band interior together with the empirical gap distribution.

Cost: seconds to a few CPU-minutes. No model, no training.

### D-2: double cover with delayed kick (exact for *every* belief, within one world)

**State.** s = (x̃ ∈ Z₂₄, y, κ ∈ {−1, 0, +1}). p(x̃) = x̃ mod 12 projects onto the base cylinder, and σ = ⌊x̃/12⌋ is the sheet. The sheet flips at each seam crossing, so it is the winding parity of the path.

**Emission.** The existing base overlap emission of (p(x̃), y), blind to both σ and κ.

**Transition.**
- The base position moves by the lifted lazy walk plus the pending kick κ (a y-step clipped at the boundary).
- Then κ′ = (−1)^{σ′} if the new base position lies in a marked region M_b, and 0 otherwise.

**Claim.**
- (i) For every belief b, Q₁(b) depends only on the (base, κ)-marginal of b. With ι the sheet swap, (I − ι)·T̃Ẽ = 0 as a matrix identity, because the law of base_{t+1} is a function of (base_t, κ_t) only.
- (ii) (I − ι)·T̃ diag(Ẽ_w) T̃Ẽ ≠ 0 whenever P(base_{t+1} ∈ M_b) > 0. The sheet sets the sign of κ_{t+1}, which moves base_{t+2} in opposite directions, and the overlap emission at t + 2 distinguishes them.

So the observability matrix O₁ annihilates the sheet-antisymmetric subspace and O₂ does not. This is the "ambient algebra" of B2, but here the gap is guaranteed by construction.

**Topology.** On the cylinder base, σ depends on the path's homotopy class (Z₂ holonomy). On a square base, the double cover is trivial and σ becomes a constant label fixed at time 0. The same construction there yields a static latent class, not a topological one. That is the natural contrast.

**Oracle-only check.**
1. Build T̃ and Ẽ (864 states); compute the stationary law.
2. Verify (I − ι)T̃Ẽ = 0 to ≤ 1e-15.
3. Compute σ_min of O₂ restricted to the antisymmetric subspace (a 1,296 × 432 block).
4. Sample reachable histories and report the distribution of the antisymmetric belief component together with the induced Q₂ gap. This is an exact witness: the oracle beliefs of two reachable histories that differ only in an earlier observed kick direction.

Cost: under a CPU-minute for the algebra; a few CPU-minutes for the sampling.

**Recommendation for D.** Draft D-1 first. It reuses the existing world builder, lazy walk and overlap emission, compares two genuinely different topologies (orientable and non-orientable), and has a one-line proof. D-2 is the stronger "every belief" result, but it needs a new state space. Either goes through the C path (review → freeze → oracle-only gate) before any training.
