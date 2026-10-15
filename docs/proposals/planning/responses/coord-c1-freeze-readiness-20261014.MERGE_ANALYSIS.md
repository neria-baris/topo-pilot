# C1 freeze-readiness: merge analysis of track X (Codex) and track L (Claude)

Clean-context comparison for the coordinator. Read-only analysis; no Python run, no data opened.
Inputs:
- the request `planning/requests/coord-c1-freeze-readiness-20261014.md`;
- `OWNER_MESSAGE.md` B3-C/D;
- X = `coord-c1-freeze-readiness-20261014.codex.md` (cited as X§n);
- L = `coord-c1-freeze-readiness-20261014.claude.md` (cited as L§n).

Code checked at `topo-pilot-circle-history-k4` HEAD 4f219d6, in `tools/x4_circle_history/{chart,precision,CONTRACT.json}`, `tools/x4_oracle_profile/oracle_profile.py`, `src/topo_pilot/{learner/patch.py, activations/_extractor.py, analysis/x4f_scores.py, experiment/x4f_probe.py, prediction/ridge.py, process/{emission,centers,_geometry}.py, dataset/sampler.py, contracts/ids.py}`.

Bottom line: L's core design is better identified on four points: the crossed ± contrast, the FWL tangent map, the positive control and the Fieller score. X's binding discipline is better on two points: donor novelty and the uncapped-meter binding. X's control family and centroid curve are defective as specified. Several of X's every-row gates make an INCONCLUSIVE result near-certain. Neither plan is wholly freeze-ready as written. The merged design in §6 is.

---

## 1. Synopses

**X (phase-associated centroid forcing).**
- **Intervention.** One donor per row: H' shifts the x-centre of w1..w31 by +1 symbol column (2 cells) and keeps w32. Its posterior b_D is recomputed from the full prefix.
- **Forced state.** a_T = a_S + μ(φ_D) − μ(φ_S). Here μ is a 12-bin periodic centroid curve of nuisance-adjusted activations, binned by K4 chart phase. The adjustment is an affine ridge on 36 symbol indicators plus oracle y-moments, fitted on CAL-FIT (X§4).
- **Controls.** 32 hash-seeded sign fields request φ_S ± |d| through the same curve. Each is rescaled to the primary's raw L2 norm (X§6).
- **Matching gates:**
  - geometry: raw norm 1e-8, whitened norm per row 5%, trace 5%;
  - recoverability damage: probes refit on each patched condition to recover the source targets, tolerance 0.02 per block and per field;
  - semantic movement through a frozen probe P_0, with angle errors ≤ π/12 or π/6 per row.
- **Endpoint (X§8).** Y = mean_r KL(q_D‖p_{C_r}) − KL(q_D‖p_T), and θ = E[Y]/E[KL(q_D‖q_S)].
- **Inference.** Ratio-of-means bootstrap with 5000 draws at α = 0.05/6.
- **Decision.** PASS if L_j > 0.10 in all three models. FAIL if U_j < 0.10 in any model.
- **Population.** Nine oracle-only eligibility rules, including TV-to-transport ≤ 0.10, y-TV ≤ 0.02 and |δ_O| ≥ π/12. Coverage must be ≥ 50%.
- **Splits.** Cal 8192 → 4096 eligible (CAL-FIT 3072 / CAL-AUDIT 1024); val 4096 → 2048; fresh 8192 → 4096 fixed.
- **Support (X§7).** Every state must lie within τ = 1.25 × the CAL-FIT maximum Mahalanobis distance and pass K4 extension support. One miss stops the cohort.
- **Numerics.** 80-digit Decimal enclosures on all rows.
- **Precision.** Projected joint power with a Clopper–Pearson bound, plus an influence-SD check.
- **CPU.** 9–87 CPU-h.
- **D.** Two constructions (D1 clock/seam gadget; D2 a circular phase visible only in a future pair) and a sufficiency lemma (X§15–18).

**L (crossed counterfactual state forcing).**
- **Intervention.** Two donors per row, H^± = x-centre shifts of ±1 column with w32 kept, and oracle targets q^±.
- **Forced state.** a^± = a + B[f(φ^±) − f(φ_S)], with f = (cos, sin). φ^± is the K4 chart reading of the model's own donor activation. B is the phase block of a joint OLS (FWL) regression of a on 36 symbol dummies, 3 oracle nuisance covariates and f(φ_S), fitted on calibration (L§5).
- **Controls.** 32 Haar 2-frames in within-class-whitened space carry the primary's whitened coordinates. Norm per row and spectrum match exactly (L§6).
- **Damage.** Fixed RFF decoders read the w32 and y-marginal changes. LOPO λ is chosen on calibration. Gates M2 and M3 run first on calibration with no logits, then on validation (L§7–8).
- **Other gates:**
  - registration V1 (the chart sees the ± counterfactual);
  - manipulation V2 (progress ratio);
  - positive control V3 (the model's own donor predictions discriminate q^±).
- **Endpoint (L§9).** A = ½⟨q⁺−q⁻, log p⁺ − log p⁻⟩ and Y = A_T − mean_r A_{C_r}. θ = E[Y]/E[G], with G = ½·Jeffreys(q⁺, q⁻).
- **Decision.** Made on Z = Y − 0.10·G, using a joint bootstrap at 0.05/3. PASS if all three lower bounds are > 0. FAIL if all three upper bounds are < 0. MIXED otherwise.
- **Eligibility.** Donor last-symbol surprisal ≤ the calibration q0.999 of the natural surprisal. The eligible fraction must be ≥ 0.90.
- **Splits.** Cal 8192 (2 blocks), val 4096. Fresh N ∈ {4096, 8192, 16384} is chosen from validation SD alone, using the reused `precision.py`.
- **CPU.** 1.5–4.5 CPU-h.
- **D.** D-1 (cylinder vs Möbius with a y-blind band) and D-2 (a double cover with a delayed kick) (L§17).

## 2. Agreements (strong merge candidates)

1. **Fixed objects.** Both use:
   - the three E4 cylinder-O models 1729/2718/3141, step 5000;
   - `resid_post_3` at index 32;
   - the same checkpoint and EmissionSpec IDs and the shared World/Transition IDs (X§10 = L§2);
   - no training and no site search.
2. **Donor transform.** Both use the canonical τ(6a+b) = 6((a±1) mod 6)+b on w1..w31 with w32 kept. The donor posterior is recomputed from the full prefix and is never a rotated b_S.
   - Verified in code: centres are (0.5+2a, 0.5+2b) with j = 6a+b (`centers.GridCenters`), and the x-distance is wrapped on a periodic axis (`_geometry.point_distances`). The 2-cell shift is therefore an exact symmetry, as L§4 claims.
3. **Oracle target.** Exactly one transition and then emission: q = b32·T·E. The expectation is exact under q. Nothing reads w33 or a sidecar, and nothing is floored or clipped.
4. **Eligibility.** Oracle-only and fixed before calibration. No model output, regret or chart value enters it. No row is trimmed after the model stage.
5. **Patching.** Through `learner.forward_with_patch`. Identity and zero patches are checked. At this site, full donor replacement equals the model's own donor prediction.
6. **Baseline cancellation.** In both endpoints the unpatched regret cancels. Both state that θ > 0 does not mean improvement over the unpatched prediction, and both report repair only as a secondary quantity.
7. **Probe class.** 2048-feature Gaussian RFF plus affine ridge, reusing `x4f_scores.{standardizer, rbf_map, rbf_features}` and `RidgeProbe`, fitted on calibration only.
8. **Endpoint scaffold.** One ratio endpoint normalised by an oracle margin. Practical margin 0.10, design alternative 0.20, power 0.80. Joint whole-row bootstrap shared across models with 5000 draws and `inverted_cdf` quantiles. Validation-only precision before the fresh test.
9. **Fresh histories.** New histories never exposed. One sampler call per fixed cohort or block, with no replenishment. First failed gate stops. No relaxation after values are seen.
10. **Chart.** The K4 chart method, unchanged. Neither plan lets an oracle-angle decoder replace a failed chart.
11. **Licenses.** No H1 or topological necessity, upstream mechanism, long memory, repair, generalisation or literal circle variable. X4-F INCONCLUSIVE and the other frozen verdicts are untouched.
12. **Resources.** No CPU cap, ≤ 4 threads, ≤ 12 GiB, one job at a time, outputs on X:, and STOP at C: < 2 GB or X: < 30 GB. Meter, ledger and guards are reused through a new C1 binding, without editing frozen K4 files.

## 3. Conflicts

| Topic | X | L | Better, and why | Risk if the wrong one is chosen |
|---|---|---|---|---|
| Intervention and forced-state construction | 12-bin centroid curve μ of the symbol- and nuisance-adjusted residual, binned by **absolute** chart phase; a_T = a_S + μ(φ_D) − μ(φ_S) | Joint FWL: B = within-symbol, nuisance-adjusted linear map from f(φ) to a; a^± = a + B Δf | **L.** After symbol means are removed, the residual is a within-symbol deviation. Binning it by absolute phase mixes deviations of opposite sign. The K4 gauge aligns φ to the oracle m32 (`fit_gauge`), whose x-centres sit at 15° + 60°a, so each centre lies **inside** a 30° bin (e.g. [0°, 30°) contains 15°). Those bin means are ≈ 0 and the neighbouring bins alias between adjacent symbols. FWL identifies the tangent directly: 6 centre phases give 6 tangent directions, which span R². | X: an attenuated or aliased 6-fold displacement. The primary is weak or misdirected, so the result is likely INCONCLUSIVE or a spurious FAIL. |
| Counterfactual definition | One donor (+1 column). Target q_D. Margin g = KL(q_D‖q_S) | Two donors (±1). Targets q^±. Margin G = ½·Jeffreys(q⁺, q⁻) | **L.** Both arms have an oracle target, and a perfect predictor gives A = G, so θ = 1 is a natural anchor. X's reflection arm has no oracle target. | X: θ has no "perfect = 1" scale; see the normalisation row. |
| Baseline cancellation | R^S cancels; the reflection contrast survives (Y ≈ (n_refl/32)(R^refl − R^T)) | p_S is unused; A compares the ± patched arms; arm-common additive log-p terms and v-constant terms cancel exactly | **L**, with corrected wording. Both cancel the baseline. L's cancellation is symmetric and needs no oracle entropy terms. L's claim that it cancels "flattening and LN scale" is too strong: see §4 L-1. | Small. The wording overclaims identification. |
| Control family and overlap with the primary | 32 sign fields with only **two** destinations. ≈ 50% coincide exactly with the primary and contribute 0. The family mean is ½·reflection with Binomial(32, ½) weight noise. The "random family" is a disguised mirror arm. | 32 Haar 2-frames in whitened space. Expected squared overlap with span(WB) is ≈ 2/128 per direction. Norm and spectrum match exactly by construction. By Haar symmetry the mean A_C ≈ 0, so the family is a near-placebo that absorbs second-order generic effects. | **L.** It meets the owner's "random family matched in norm and variance" literally, with zero rejection sampling. X's family overlaps the primary by construction, halves the signal and adds noise. | X: dilution by ½, vacuous matching gates (half the fields are the primary), and the owner's requirement not truly met. |
| Norm, spectrum and damage matching; information-damage metric | Raw norm 1e-8, **and** whitened norm 5% per row, trace 5%, harmonic moments. Damage = loss of recoverability of the source targets by probes **refit** on each patched condition, tolerance 0.02 per block × field | Whitened (within-class LW) isometry, exact. Raw-norm ratio reported only. Damage = how **fixed** decoders read w32 and y after the move: ceilings 0.02/0.05 and matching 0.01/0.02, ≥ 28/32 frames. A y-leakage gate L(T) ≤ 0.25 applies when κ_ν ≥ 0.01 | **L.** The forced state is an additive, nearly invertible shift, so refit recoverability is ≈ 0 for every condition: X's gate passes trivially and measures nothing. Equal raw **and** whitened norms per row within 5% is not generally attainable for different directions. L's fixed decoders measure what a frozen downstream reads, which is the relevant collateral damage. | X: a meaningless "matched" verdict, or an arbitrary failure on the per-row whitened-norm rule. L: M2 may fail because random whitened frames hit w32 directions (L-R3). That is an honest early stop. |
| Nonlinear probes | ℓ = √128 fixed and λ = 1 singleton: no selection at all. Adequacy normalised MSE ≤ 0.20 and accuracy ≥ 0.90 | ℓ = median pairwise distance (`rbf_bandwidth`), λ ∈ {1e-3..10} by LOPO on 8 calibration panels (`nested_ridge`), then a `RidgeProbe` refit. Adequacy accuracy ≥ 0.95 and pooled R² ≥ 0.50 | **L.** Selection is calibration-only, so there is no leakage, and it is fixed in advance. X's untuned λ = 1 risks PROBE_INADEQUATE with no recourse. X's "zero selection" is not more rigorous than calibration-internal selection. | X: avoidable INCONCLUSIVE. L: none beyond the 1e-10 equivalence check (cho_solve vs lstsq). |
| Eligibility and support | 9 rules, including TV(b_D, R_δ b_S) ≤ 0.10, y-TV ≤ 0.02, \|δ_O\| ≥ π/12 and \|Δlog P\| ≤ 5, with coverage ≥ 50%. Support: **every** state within 1.25 × the CAL-FIT max Mahalanobis **and** passing K4 extension support; one miss stops | Single rule: donor w32 surprisal ≤ calibration q0.999 of the natural surprisal, which is exact because p(τw1..31) = p(w1..31). Fraction ≥ 0.90. Support is gated as fractions beyond the calibration q99: F(T), F(C̄) ≤ max(0.05, F(D)+0.02), \|F(T)−F(C̄)\| ≤ 0.02, K4 support ≥ 0.98 or 0.99 | **L.** With w32 kept, b_D is pulled toward w32's centre, so \|δ_O\| ≥ π/12 and the TV-to-transport rule select rows where w32 is weakly informative. That is an atypical population with real coverage risk. X's all-row extreme-value support rule covers ≈ 4096 × 34 states × 3 models against 1.25 × max(6144). Its failure probability is high whatever the science. | X: near-certain INCONCLUSIVE/SUPPORT_FAILED or COUNTERFACTUAL_UNSUPPORTED. L: the population is broader. Nuisance compatibility moves from eligibility to the leakage gate. |
| Endpoint formula and normalisation | θ = E[mean_r R^{C_r} − R^T] / E[KL(q_D‖q_S)] | θ = E[A_T − mean_r A_{C_r}] / E[½·J(q⁺, q⁻)] | **L.** A perfect predictor gives θ = 1. In X, under a local quadratic approximation, an ideal phase-reading readout gives θ ≈ ½·(2d)²/d² ≈ 2, so X's 0.10 is ≈ 5% of ideal and is not "10% of the oracle margin". | X: the margin's meaning is miscalibrated by a factor of about 2. |
| Precision method and test size | Ratio-of-means percentile bootstrap. Projected joint power with Clopper–Pearson ≥ 0.80 over bootstrap successes, plus an influence-SD check. Fresh N = 4096 fixed | Fieller-equivalent: θ > c ⇔ E[Y − cG] > 0, given E[G] > 0, so the decision is on a mean. `precision.py` is reused unchanged (`sd_b4_draws`, `centered_draws`, `precision_summary` with alternative = 0.10·Ḡ_val, delta 0). Ladder N ∈ {4096, 8192, 16384} in fixed 4096-row streams | **L.** The test is exact at the margin, reuses tested code (verified signatures and semantics), and is simpler. The ladder uses only validation SD and centred errors, not the validation mean. The fixed-stream design is correct: `HMMSampler.sample` draws `rng.random(n)` per step, so a sample of size n is not a prefix of one of size 2n. | X: a bespoke double gate and an INCONCLUSIVE at fixed 4096 that a larger N would avoid. |
| Positive control | Full donor replacement is "engineering only, calibration", excluded from the science | V3 on validation: lower bound of A_full − 0.30·G > 0, else MODEL_HEADROOM | **L.** Without it, a FAIL cannot separate "the readout ignores the phase" from "the model does not discriminate the counterfactual prefixes". | X: an uninterpretable FAIL. |
| Chart reuse from K4 | Reuse accepted K4 artifacts, else construct on the first 512 CAL-FIT rows. Branch fixed at freeze | (a) reuse if all K4 chart gates PASS; (b) **stop** if a K4 chart gate is FAIL or INCONCLUSIVE; (c) construct once only if K4 never reached the chart stage. "Six constructions" = K4's `max_chart_constructions` (3 production + 3 fidelity) | **L.** X's "construct if absent" leaves the case "exists but failed" unspecified. That case would fall into a refit on new data of a method that already failed at the same site: run-to-pass. | X: a forbidden-in-spirit refit loop. |
| Threshold values | margin 0.10; α 0.05/6; headroom E[g] LB > 0.005 nat; damage 0.02; angles π/12 and π/6 per row; adequacy 0.20 / 0.90; support 1.25 × max | margin 0.10; α 0.05/3; headroom Ḡ LB > 0.01; damage 0.02/0.05/0.01/0.02; κ ∈ [0.5, 1.5] with sign ≥ 0.80; V1 ≥ 0.75; V3 0.30; adequacy 0.95 / 0.50; support q99 fractions | **L** mostly. Absolute angle thresholds are meaningless for within-symbol shifts, which are small. X's α/6 treats a one-sided intersection test as two-sided. For an intersection-union PASS, 0.05/3 is already conservative. | X: INCONCLUSIVE by construction. |
| Decision symmetry | FAIL if **any** model has U_j < 0.10, the exact complement of the all-three claim | FAIL only if **all three** have U_j < c; otherwise MIXED with per-model statuses | **L**, plus X's sentence. MIXED should state explicitly that the all-three claim is not supported. Each FAIL definition is consistent with its own license text. | Mislabelling a one-model miss as a scientific FAIL of "readout use". |
| Stop rules | First failing gate; no replenishment; technical fixes need coordinator review; the fresh test cannot change method | The same, plus ≤ 2 correction jobs per defect (owner B5), sealed validation means, and arrays kept on a fresh pre-scoring failure | **L ∪ X.** They are compatible. Add X's "no selective-coverage claim conditional on passing fresh gates". | Minor. |
| Numerics | 80-digit Decimal enclosures on all rows; CPU 9–87 h | float64 model (an exact cast), a per-row error bound, and a 60-digit Decimal reference on 4 rows per split | **L**, with an implementation fix (§4 L-3). All-row Decimal is out of proportion to a 0.10 relative margin. | X: tens of CPU-hours with no gain in validity. |

## 4. Defects

### X

- **X-1 (§6, mis-specified family).** Controls have two destinations, and ≈ half reproduce Δ_T exactly. Y_i = (n_refl,i/32)(R^refl − R^T), so E[Y] ≈ ½·E[R^refl − R^T] with Binomial(32, ½) noise. The "family" is not random, overlaps the primary by about 50%, and makes half the per-field matching gates vacuous. X acknowledges the coincidences (X§6, lines 283–285) but does not recognise the consequence.
- **X-2 (§4, aliasing and attenuation).** The centroid curve bins the symbol-residualised activations by absolute gauged phase. The gauge aligns φ to the oracle m32 (`chart.fit_gauge`), and the symbol x-centres are at phases 15° + 60°a (`GridCenters` 0.5+2a). So each centre falls inside a bin and the deviations of opposite sign cancel. μ(φ_D) − μ(φ_S) is not the within-symbol tangent the w32-preserving donor moves along.
- **X-3 (§6, rescaling distorts the request).** Rescaling a control to the raw ‖Δ_T‖ changes its requested phase. Requiring raw norm (1e-8) **and** whitened norm (5% per row, every row and every field) is not generally satisfiable for two different directions.
- **X-4 (§6, uninformative damage metric).** Refit recoverability of the source targets after an additive shift is ≈ 0 for every condition, so equality of damage holds trivially. It also costs 33 refits per model per split.
- **X-5 (§7 and §4, extreme-value gates).** The following must hold on every row or state, or the cohort stops: Mahalanobis ≤ 1.25 × the CAL-FIT max; K4 extension support for every state; chart-vs-δ_O agreement within π/12 per row (line 363). Each is a maximum over 10⁴ to 10⁵ objects. Failure is close to guaranteed and is unrelated to the science.
- **X-6 (§3, population drift and coverage).** |δ_O| ≥ π/12 and TV(b_D, R_δ b_S) ≤ 0.10 keep only rows where w32 barely constrains x. With σ = 1.25 and centres 2 cells apart, w32 is usually informative, so the ≥ 50% coverage gate is at risk. If it passes, the estimand refers to an atypical subpopulation.
- **X-7 (§8, normalisation).** g = KL(q_D‖q_S) does not correspond to anything the forced arms can attain, and the reflection arm has no oracle target. Under a local quadratic approximation an ideal readout gives θ ≈ 2. The margin 0.10 is therefore not "10% of the oracle margin" as the request asks.
- **X-8 (no positive control).** Full donor replacement is excluded (line 188), so a FAIL is not interpretable.
- **X-9 (§4, chart branch gap).** A K4 chart that exists but failed is unaddressed, and the construction branch then permits a refit of a failed method.
- **X-10 (§9, bootstrap power bound).** The Clopper–Pearson bound over bootstrap "successes" bounds Monte Carlo error only, not sampling uncertainty. It is harmless but adds complexity without validity.
- **Not defects.** No leakage found: every fit is on CAL-FIT, precision is on validation, and the fresh test chooses nothing. The seed map is valid: `SeedTree(master).generator(name, *scope)` accepts strings.

### L

- **L-1 (§9.1 and Summary, overclaim).** "Cancels exactly every target-independent effect: damage, flattening, LayerNorm scale" is too strong. A cancels exactly only:
  - additive log-p perturbations common to both arms; and
  - terms constant in v (Σ(q⁺−q⁻) = 0).

  Multiplicative flattening or temperature scales A, attenuating it conservatively. Arm-asymmetric damage does not cancel, and arms do differ because |d⁺| ≠ |d⁻| when w32 is kept. The matched family handles the residual. The text must say "approximately; the residual is estimated by the controls".
- **L-2 (§6, family is a placebo).** By the Haar symmetry Q → −Q, E[A_C] ≈ 0 to first order. The family subtracts only second-order generic effects, so the endpoint ≈ A_T. This is defensible, and L flags it at L§15.2, but the reviewer must accept that "beyond matched random moves" adds little discrimination beyond A_T > 0.10·G.
- **L-3 (§2 vs §13, reuse inconsistency).** L requires float64 evaluation with a bitwise identity patch, and its §13 reuse list names `ActivationExtractor` as reused unchanged. But `ActivationExtractor.extract` returns float32 activations and logits (`_extractor.py` lines 124–135) and needs an ObservationSet and a HistoryIndex. L does not store donors as ObservationSets (L§4). So donor activations and a float64 bitwise identity cannot come from the extractor. Activations must come from the float64 model's own `return_hooks` (`forward_with_patch` casts the replacement to `x.dtype`, so that path works). Fix this in the contract.
- **L-4 (§8.1, quantile method).** L says q99 is `inverted_cdf` but reuses `support_report`, which uses the default linear `np.quantile` and its own LW fit on its inputs. Pick one: implement D_M explicitly with `inverted_cdf` and do not reuse `support_report`.
- **L-5 (§2(c) vs §8.1, chart support).** The fallback applies K4 chart gates, where support must hold for **every** validation row (CONTRACT `support_rule`). M3 instead uses fractions of ≥ 0.98 or 0.99. Under fallback (c), the all-row K4 rule on 4096 rows recreates X-5. Specify that the K4 gates are applied to a 512-row panel, as K4 does.
- **L-6 (§9.2 and §3, effective N).** The ladder counts sampled rows, but the endpoint uses eligible rows. The projection must use the expected eligible count, or the ladder must be defined on eligible rows.
- **L-7 (§5 and §8.3, weak manipulation check).** B is fitted from φ(a) itself, so V2 (does the chart read the forced state as moved) is partly guaranteed by construction. It is a weak manipulation check. This is not wrong, but V1 (registration against the oracle δ*) is the substantive gate and should be described as such.
- **L-8 (§5, lax degeneracy bound).** The bound σ_min(B)/σ_max(B) ≥ 1e-6 is almost vacuous. Consider reporting the within-class partial R² of f(φ) as a gate, or keep the bound and accept it.
- **L-9 (§3, donor freshness).** Separation checks cover the C1 source histories only. The donor prefixes H^± are not checked against old exposures; X§10 does check them.
- **Not defects.** No leakage found: s_max, FWL, Σ_W, decoders and q99 come from calibration, and the ladder from validation SD. The `precision.py` call is semantically correct for Z = Y − 0.10G, because `alternative + e + q_α > delta` with delta = 0. `bootstrap_profile` can serve the Ḡ headroom with norm = sq = {1: G}.

## 5. Unique catches

**Only X:**
1. Donor and source novelty against a hash-based exposure registry, including planning-feasibility histories (X§10).
2. A sufficiency lemma for D. A recursively updatable statistic sufficient for horizon 1 is sufficient at every horizon, so any gap must be stated at a reachable decision phase (X§15).
3. The distinction between the operational oracle and the ideal process, following K4 (X§2).
4. Verifying, not assuming, that the margin is identical across models (X§8).
5. No claim of selective coverage conditional on passing fresh gates (X§9).
6. The uncapped policy written as JSON `null`, a default of one thread, a 16 GiB output envelope, and rebinding of the meter's hardcoded CPU ceilings (X§12).
7. The distinction between a frozen semantic probe and a recoverability refit (conceptually correct, even though refit damage is the wrong gate here).

**Only L:**
1. X-1: the degenerate sign family.
2. X-2: the aliased absolute-phase binning, and the FWL fix.
3. X-3: raw plus whitened norm matching is infeasible.
4. X-4: refit damage is uninformative for invertible shifts.
5. A positive-control gate (V3).
6. A registration gate (V1).
7. Fieller equivalence, which removes the ratio-precision blocker.
8. Prefix stability of the sampler for the ladder.
9. "Stop if the K4 chart failed".
10. The w31 short-context limit (E4 explanation).
11. Readout rank ≤ 35, so the test is not trivial.
12. Absolute π/12 thresholds are meaningless for within-symbol shifts.
13. The exact x-translation symmetry check, with a closed-form donor posterior.

## 6. Recommended merged design

Each item gives the source and a one-line reason.

1. **Site, models, IDs and resources.** Shared (§2, item 1). Thread default 1, uncapped JSON `null` and an output envelope (X§12). *Uncontested.*
2. **Donors.** L's crossed H^± (±1 column, w32 kept). The donor posterior is recomputed directly with BayesFilter and checked against L's closed form and symmetry ≤ 1e-12. *Two oracle-targeted arms anchor θ = 1 and cancel arm-common effects.*
3. **Oracle and margin.** q^± = b32(H^±)TE and G = ½·Jeffreys(q⁺, q⁻), plus X's cross-model identity check on G. *Calibrated normalisation.*
4. **Eligibility.** L's single surprisal rule (calibration q0.999, fraction ≥ 0.90) and positive likelihood. Drop X's TV, |δ_O| and y-TV rules. *Broad, oracle-only, exact, no coverage trap.* Y-nuisance compatibility moves to L's κ_ν / leakage gate.
5. **Forced state.** L's FWL map, with φ^± = the chart reading of the model's own donor activation. *Identifies the within-symbol tangent; X's curve aliases.*
6. **Controls.** L's 32 Haar whitened 2-frames applied to the primary's whitened coordinates, with the same frame for both arms. Report the raw-norm ratio. *Exact matching of norm and spectrum, negligible overlap with the primary.* Document L-2 (placebo character) in the claim text.
7. **Probes.** L's RFF-2048 with the median bandwidth and calibration LOPO λ through `nested_ridge`, then a `RidgeProbe` refit. Targets: w32 and the y-marginal, with m32 as a diagnostic. *Calibration-only selection, tested code.*
8. **Damage.** L's fixed-decoder collateral metric (M2), run on calibration first with no logits, then on validation. Add the leakage gate. Optionally report X's refit recoverability descriptively, without a gate. *The relevant notion for a frozen readout.*
9. **Support.** L's fraction-based within-class Mahalanobis gate, implemented explicitly with `inverted_cdf` (fixes L-4). K4 extension support is gated as fractions, and K4's all-row chart gate applies only to a 512-row chart panel (fixes L-5). *Avoids X-5.*
10. **Manipulation and registration.** L's V1 (≥ 0.75 sign agreement with the oracle δ*) and V2 (κ ∈ [0.5, 1.5], ≥ 0.80). Do not use absolute angles. *Within-symbol shifts are small.*
11. **Positive control.** L's V3 (Z_full = A_full − 0.30·G, lower bound > 0). *Makes FAIL interpretable.*
12. **Endpoint.** Y = A_T − mean_r A_{C_r}, θ = E[Y]/E[G], decision on Z = Y − 0.10·G. Correct L-1's wording. *Exact at the margin, simplest.*
13. **Inference.** Joint whole-row bootstrap, 5000 draws, PCG64, one index per draw shared by all models and arrays, α = 0.05/3 per tail. *IUT for PASS; consistent with K4.*
14. **Precision and test size.** `precision.py` unchanged. Ladder N ∈ {4096, 8192, 16384} on **eligible** rows (fixes L-6), in fixed 4096-row sampler streams. *Reuse plus a power guarantee without X's double gate.*
15. **Decision.**
    - PASS if all three lower bounds are > 0.
    - FAIL if all three upper bounds are < 0.
    - MIXED otherwise. Per-model statuses are reported, with the explicit sentence that "the all-three claim is not supported" (X's license).
    - Validity failures take precedence.
16. **Chart.** L's three-way rule: reuse accepted K4; stop if K4's chart failed; construct once only if K4 never reached the chart stage. Bind the NPZ sha. *No run-to-pass.*
17. **Freshness.** L's separation checks plus X's exposure registry covering **sources and donors** (fixes L-9). Fresh histories are sampled only after the validation acceptance.
18. **Numerics.** float64 cast of the frozen weights. Activations come from the float64 model's `return_hooks`, not from `ActivationExtractor` (fixes L-3). K4-style Decimal reference on the lowest-ID rows per split, plus L's per-row float64 bound. *Proportionate.*
19. **Splits.** Cal 8192 (FWL, Σ_W, decoders, s_max, q99, M2 and M3 early stop), val 4096 (all gates, V3, P1, sealed means), fresh by ladder. Seed map as in L§11, plus X's registry seed scope.
20. **Licenses.** The union of both "neither licenses" lists, plus L's E4/w31 limit and X's "no selective coverage" sentence.
21. **Stop rules.** First failure stops. No redraw of frames. Arrays are sealed and kept. ≤ 2 correction jobs per defect. No change after exposure.
22. **CPU.** Expected about 2–6 CPU-h, using L's estimate plus margin for float64 forward passes on ~270k control states per model. This is a forecast, not a cap.

**Parameters a result-blind reviewer must scrutinise:**
- margin c = 0.10, alternative 0.20, positive-control threshold 0.30, power 0.80, α = 0.05/3;
- donor step ±1 column (2 cells) and eligibility q0.999 / ≥ 0.90;
- FWL covariates (ȳ, Var y, ‖m32‖): including ‖m32‖ fixes the radius out of B;
- metric choice: whitened (within-class LW, phase term retained) versus raw;
- 32 frames and ≥ 28/32 dispersion;
- damage tolerances 0.02 / 0.05 / 0.01 / 0.02, leakage 0.25 with κ_ν trigger 0.01;
- support fractions q99, max(0.05, F(D)+0.02), 0.02, and 0.98 / 0.99;
- V1 0.75 (rows above the median |δ*|), V2 κ ∈ [0.5, 1.5] and 0.80;
- decoder adequacy 0.95 / 0.50;
- headroom Ḡ lower bound > 0.01 nat;
- ladder grid and its eligible-row basis;
- the FAIL-all versus FAIL-any asymmetry;
- whether a near-placebo random family satisfies owner B3-C (L-2).

## 7. D sketches

**X D1 (three-phase clock with a seam gadget).**
- Correct: Q1 = `!` deterministically, and Q2 = A (cylinder) vs B (square).
- Imprecise: "prefixes ending A,# and B,# identify the components" fails in the first cycle, where the initial x = 0 emits A in both worlds. It needs "after at least one full cycle".
- Scientifically thin: the distinction is a single bit readable from the second-to-last symbol, and the gadget is far from the lazy walk. X states this limit honestly.

**X D2 (circular phase visible only in a future pair).**
- The algebra checks out: q_d > 0 for ε = 1/4 because |cos + sin| ≤ √2; both single marginals equal 1/3; the joint identifies (cos θ, sin θ).
- The topology statement is properly scoped: a continuous injective image of S¹ is homeomorphic to S¹, with no claim about ambient H1.
- It departs from the pilot's alphabet, and the twelve-phase finite version proves only twelve distinctions.

**X§15 lemma.** Correct and important. It should be adopted as the framing for any D contract.

**L D-1 (cylinder vs Möbius with a y-blind band).** Closest to the existing machinery: `QuotientLatticeBuilder` supports `flipped`, and the lazy walk and grid centres are reused. Claim (i) holds at the band interior: x is exact, the next symbol is in the band with probability 1, and the x-law does not depend on y. Claim (ii) is plausible. Three defects need fixing:
- (a) Outside the band, the "existing overlap emission" in M would use **unwrapped** x-distances, because `point_distances` wraps only when `is_x_periodic` holds and a flipped glue is not periodic. E then differs between C and M near x = 2 and 9. That contaminates both the pre-band beliefs and the Q2 gap. The **same** E rows must be fixed for both worlds.
- (b) It must be framed as a single mixture process with a hidden world bit F (as X's D1 is) to be a prediction statement.
- (c) Q1 equality holds only at the band interior, a reachable decision phase, consistent with X§15.

**L D-2 (double cover with a delayed kick).** Claim (i), (I−ι)T̃Ẽ = 0, is correct as a matrix identity if ι is defined as the sheet swap only, with κ unchanged. This needs to be stated. Claim (ii) needs M_b to lie away from the y-boundaries, where clipping can make ±κ coincide. Reachable sheet-asymmetric beliefs require an earlier observed kick, and witness histories should be exhibited. It is the strongest "every belief" statement of the four. It needs a new 864-state space, and on a square base it collapses to a static label: a good built-in contrast.

**Which first.** L D-1, with fixes (a)–(c) and X§15's framing. It is the closest to the cylinder/square machinery, compares two genuinely different topologies, and its oracle check costs CPU-minutes. Keep X D2 as the companion if the owner means "a continuous circular family of predictive states" rather than a world-topology distinction. That is the owner choice X raises in its open questions. Do not pursue X D1 or L D-2 first: X D1 is too trivial, and L D-2 costs more to build.
