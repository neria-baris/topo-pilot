VERDICT: APPROVE_WITH_REQUIRED_CHANGES

The crossed endpoint, FWL construction, paired Haar frames, and eligible-row ladder are coherent. I would retain the scientific design and declared margin. Freeze is blocked by the numerical certificate, several incorrect claims, and incomplete reuse bindings.

## Required changes

1. **§3.5 and §16 H5 — correct the bootstrap API.**

   `bootstrap_profile` returns a dictionary, and its `rng` argument requires a `Generator`, not a bare `PCG64`.

   Replace the call and extraction with:

   ```python
   seed = 520505  # validation; 520506 for fresh
   result = oracle_profile.bootstrap_profile(
       norm={1: G},
       sq={1: G},
       Ks=(1,),
       rng=np.random.Generator(np.random.PCG64(seed)),
       draws=5000,
   )
   lower = float(
       oracle_profile.percentile_interval(result["B"][:, 0], [0.05])[0]
   )
   ```

   Retain the requirement `lower > 0.01`.

2. **§1.3, §8.3, §12.1, and MERGE ruling 4 — correct the oracle-perfect anchor and remove the ceiling claim.**

   The identity \(A_T=G\) is correct. It does **not** imply \(\theta=1\), because the endpoint subtracts the frozen control family.

   Replace the oracle-perfect interpretation with:

   > If the primary arms reproduce \(q^+\) and \(q^-\), then \(A_T=G\) pointwise. Consequently,
   > \[
   > \theta=1-\frac{E[\overline A_C]}{E[G]}.
   > \]
   > The primary oracle-perfect anchor is \(\theta_T=E[A_T]/E[G]=1\). The control-adjusted endpoint equals 1 only when \(E[\overline A_C]=0\). An oracle-perfect full-donor readout gives \(\theta_{\rm full}=1\). These ratios are discrimination indices, not proportions constrained to \([0,1]\).

   Replace “it caps θ below 1” in §8.3 with:

   > Donor nuisance changes can affect the achievable discrimination of this intervention. They impose no general mathematical upper bound on θ.

   This correction must also appear in the merge ruling and associated explanatory text.

3. **§1.2 E2, §1.3 specificity statement, §6 raw-norm paragraph, §12.1, and C-1 — restrict what the controls establish.**

   The cancellation identities are correct, but “the residual is estimated by the controls” suggests an identification guarantee that matching does not provide. Raw-norm differences can affect nonlinear bias through LayerNorm, not just variance.

   Replace those assertions with:

   > In exact arithmetic, arm-common additive log-probability perturbations cancel, and terms constant across symbols cancel. A common inverse-temperature multiplier β scales A by β. This is attenuation only for \(0<β<1\); it does not establish general conservatism for Y when primary and control effects differ.
   >
   > Averaging over Haar frames eliminates the linear Taylor term of the control contrast. Higher-order terms and the finite, frozen 32-frame mean need not be zero. Matching whitened displacement norms and covariance spectra, together with the damage gates, does not establish equality of orientation-dependent nonlinear effects. The family provides an operational random-direction comparison, not an unbiased subtraction of every generic or nuisance effect.
   >
   > Raw-norm ratios are reported because raw-scale differences can affect both the mean contrast and its variance.

   Replace “it subtracts only second-order generic effects” with:

   > Its leading nonzero frame-averaged Taylor contribution is second order; higher-order contributions remain possible.

   **Owner B3-C:** I accept ruling 1 under this explicit operational interpretation: displacement norm and variance are matched in the declared whitened metric, and information damage is matched through the declared decoder metrics. A near-placebo family does not itself violate B3-C.

4. **§1.1, §1.2 E3, §1.4, §5.2, §7, and §8.3 — narrow the phase-isolation claims.**

   FWL removes specified linear associations. Fixed-decoder damage and leakage constrain measured decoder responses. Neither establishes preservation of every nuisance channel.

   Apply the following replacements:

   - Replace **“phase-only move”** throughout the scientific claims with **“chart-phase-directed move along the fitted B map.”**
   - Replace the final PASS conclusion with:

     > PASS supports causal efficacy of the prespecified chart-phase-directed state changes at the trained final readout, relative to the frozen random-direction family. It does not uniquely attribute the predictive change to phase independently of every collateral feature.

   - Replace E3’s “bounded” characterization with:

     > Decoded y-alignment is constrained by the leakage gate. The gate does not bound the fraction of the predictive endpoint attributable to y or exclude every nuisance-mediated explanation.

   - Replace “Including ‖m32‖ … keeps the circle radius out of B” with:

     > Including ‖m32‖ adjusts the fitted phase coefficient for its linear association with the oracle radius. It does not guarantee radius preservation by the intervention.

   - Replace the invertibility rationale in §7 with:

     > Fixed decoders measure changes in the responses of prespecified readers. Refit recoverability answers a different question. Because the displacement depends on the activation through the chart, invertibility of the intervention is not assumed.

   Also replace §1.1’s global null-direction argument with:

   > After removing the softmax shift, the unembedding has rank at most 35. The Jacobian of the complete residual-to-distribution map therefore has a kernel of dimension at least 93 at each activation. LayerNorm makes this map nonlinear, so these local null directions are not automatically globally invisible finite displacements.

5. **§5.2 and §14 — make identifiability and gauge dependence exact.**

   Replace the final identifiability justification with:

   > Let C contain the 36 symbol indicators and three standardized nuisance columns, F contain the two phase columns, and A contain the activation rows. With \(M_C=I-CC^+\),
   > \[
   > \widehat B^{\,T}=(F^TM_CF)^{-1}F^TM_CA.
   > \]
   > F1 establishes identification through full rank of \([C,F]\). Distinct symbol-column tangent directions alone do not guarantee identification after nuisance adjustment. Constant nuisance columns use scale 1 and are handled by the rank gate. F1 additionally requires \(\sigma_{\max}(B)>0\) before evaluating the singular-value ratio.

   Replace “The gauge does not enter the endpoint” with:

   > A rotation or reflection is absorbed into B for the primary displacement in exact arithmetic. The complete frozen-family endpoint remains conditional on the gauge and QR basis: changing that basis can change the controls generated by fixed frame draws. No gauge or basis is selected using intervention outcomes.

   Specify the primary QR sign convention as positive diagonal, matching the control convention. A rank-deficient QR input causes the appropriate degeneracy failure; it is never redrawn.

6. **§15.3, §13 step 2, §20 item 14, and C-19 — replace the unsupported numerical certificate before freeze.**

   This is the principal blocker.

   - Four reference rows cannot establish an all-row oracle L1 error bound.
   - The reference checks use maximum absolute error, which does not imply L1 error ≤ `1e-12`.
   - `2^-44` lacks a derivation for the actual post-logit implementation.
   - The displayed bounds omit arithmetic rounding and some product-error terms.
   - The G bound uses `η/min(q)` without ensuring that the true probabilities remain above the required lower bound.
   - Tiny predictive probabilities can make the proposed absolute-error G bound enormous, forcing numerical INCONCLUSIVE despite ordinary scientific headroom.

   Replace §15.3 with:

   > **Numerical certification: NOT_READY until the following proof is attached and independently reviewed before freeze.**
   >
   > Recorded float64 logits remain the operational model output. The certificate must bound post-logit evaluation, oracle predictive errors, construction of A/G/Y/Z, and bootstrap-mean arithmetic for every eligible fresh row. Reference-row comparisons are implementation checks, not universal error bounds.
   >
   > Oracle uncertainty must be established analytically for the permitted filtering computation or by validated per-row enclosures. Componentwise or relative bounds should be used where an absolute L1 bound becomes uninformative for tiny probabilities. All assumptions about elementary functions, BLAS reductions, underflow, and normalization must be stated.
   >
   > Neither η = `1e-12` nor the log-softmax constant `2^-44` is accepted solely because it passes sampled reference checks. Their retention requires a source-specific derivation. Certificate evaluation must round bounds outward.
   >
   > Let \(b^Z_{j,i}\) be the proved row bound and \(r^{\rm mean}_j\) the proved bootstrap-mean arithmetic bound. Define
   > \[
   > B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j.
   > \]
   > The endpoint rule uses `max(B_num,j, 1e-9)` for model j. Corresponding signed numerical guards apply to the headroom and V3 thresholds. The `1e-9` floor is an additional conservative guard, not a proof of accuracy.

   For checking a proposed revision, under a genuinely established per-arm L1 bound η, a valid **input-perturbation portion** of the A bound is:

   \[
   \tfrac12\left[
   (\|\widehat q^+-\widehat q^-\|_1+2\eta)(\epsilon_++\epsilon_-)
   +2\eta\|\widehat\ell_+-\widehat\ell_-\|_\infty
   \right].
   \]

   Arithmetic-rounding terms must still be added. For oracle logarithms, an absolute-error approach requires \(m_\pm=\min\widehat q^\pm>\eta\), and uses \(-\log(1-\eta/m_\pm)\), plus logarithm-evaluation error—not simply `η/m±`.

   **Do not freeze with this item unresolved.** This does not require all-row Decimal posterior calculations; a proved analytic envelope or validated enclosure is sufficient.

7. **§6 M1 and §16 row 9 — define relative errors at zero and specify centered spectra.**

   Replace the M1 comparison definitions with:

   > For each norm identity, divide absolute error by the primary norm when it is positive. If the primary norm is zero, require the primary coordinates and control displacement to be exactly zero.
   >
   > For the uncentered second moment, \(S=\sum cc^T\). For the centered version, \(S=\sum(c-\bar c)(c-\bar c)^T\), with the mean taken over the pooled eligible rows and both arms.
   >
   > Compare sorted spectra using their maximum absolute difference divided by the primary spectrum’s maximum absolute eigenvalue. If that denominator is zero, require both moment matrices to be zero. Retain the `1e-10` relative threshold and `1e-12` frame-orthonormality threshold.
   >
   > These identities concern displacement covariance in whitened coordinates. They do not assert equality of the covariance of complete patched activations.

   Otherwise, componentwise relative comparisons encounter the 126 zero eigenvalues of these rank-two matrices.

8. **§18, C-10, C-12, C-13, and §17 S2 — complete the reuse bindings.**

   Add this exact binding requirement:

   > `c1_meter_bind` additionally binds `meter.WORKER_SESSION` to the authorized executing worker session. The same identity must own RUN.lock; `--lock-owner` alone does not override the run-mode identity check.
   >
   > C1 does not import `meter_bind` as an allegedly side-effect-free helper module. That import reads the K4 CONTRACT, changes import paths, imports the K4 release module, and captures `_LEGACY_LIMIT`. The small disk/limiter helpers are extracted into the C1 binding, with provenance and regression checks, while frozen K4 files remain unchanged.
   >
   > Rebind `env_identity.SCIENTIFIC_IMPORTS`, call `env_identity.import_scientific()`, then call `record()`. `record()` itself does not consult SCIENTIFIC_IMPORTS.
   >
   > Use `stage_records.PREREQUISITE = {"oracle": None, "calibration": "oracle", "validation": "calibration", "fresh": "validation"}`. The C1 driver separately verifies the expected PASS-gate set for each prerequisite stage: the reused helper checks evidence and absence of recorded failures, but does not know C1’s required gate names.
   >
   > The C1 boundary adapts `StageFailure`, `ProfileError`, and reference-input/Decimal exceptions into recorded C1 failures. `stage_records.run_gate` does not catch those exception classes unchanged. Every failure receives a gate or resource-stop record before termination.

9. **§14, §17–18 resource statements — remove the inherited lift CPU cap and close the incomplete-chart branch.**

   `cochain.integer_lift` independently enforces `cfg["lift_cpu_cap_s"]`, currently 30 seconds. Rebinding the meter does not remove it.

   Add:

   > C1 retains K4’s scientific chart choices and exact lift checks, with the owner’s resource override applied explicitly. In the C1 contract, `lift_cpu_cap_s` is JSON `null`, decoded to positive infinity; `native_operation_wall_s` is 600. The external operation guard remains 600 seconds. The finite lift bounds, node limit, rounding tolerance, and construction-count limit remain unchanged. Frozen K4 files are not edited.

   Amend Branch B to include:

   > If K4 attempted charts but lacks a complete, accepted PASS record for all required chart gates and models, C1 stops as INCONCLUSIVE/CHART_UNAVAILABLE. Branch C applies only when K4 never attempted chart construction.

   Branch A must bind the coordinator acceptance record as well as the chart artifact and gate records. Describe the configuration as identical **apart from the explicit owner resource override**.

10. **§2.4 and §16 H2 — make freshness checks unambiguous.**

    Replace the registry requirement with:

    > Define \(U_s=\bigcup_i\{H_i,H_i^+,H_i^-\}\) for split s. Calibration and validation require \(U_{\rm cal}\cap R_1=\varnothing\), \(U_{\rm val}\cap R_1=\varnothing\), and \(U_{\rm cal}\cap U_{\rm val}=\varnothing\), where \(R_1\) is registry version 1. Fresh requires \(U_{\rm test}\cap R_2=\varnothing\), where registry version 2 contains version 1 and both complete C1 earlier split unions. Cross-split disjointness includes every source/donor role combination.
    >
    > Registry manifests bind scanned inputs by content hashes, including canonicalization metadata and identity material. A filename listing alone is insufficient. Collision detection stops as a lineage alarm; it does not logically prove that a seed defect caused the collision.

    The proposed coverage is otherwise sound. Applying version 2’s absence requirement retrospectively to calibration/validation would contradict its inclusion of those histories.

11. **§12.2, §13, and §1.4 — distinguish exact algebra from approximate inference.**

    Replace §12.2 with:

    > For the eligible population, when \(E[G]>0\),
    > \[
    > \theta>c\iff E[Y-cG]>0,
    > \]
    > and likewise for `<`. This algebraic reduction avoids a delta-method ratio decision. C1 uses a percentile-bootstrap test of the resulting mean. It is not the classical Fieller confidence-set construction. H5 supplies empirical evidence of denominator headroom, not a deterministic guarantee about the population expectation.

    Add to §13:

    > Bootstrap tail levels and coverage are nominal approximations, conditional on the frozen calibration objects and family. The joint resampling preserves cross-model dependence but does not make percentile-bootstrap coverage exact.
    >
    > At α = 0.05/3 per tail, the union bound is 0.05 separately for erroneous above-margin declarations and erroneous below-margin declarations across models. It is not a simultaneous 0.05 guarantee covering both directions together.

    Retain the all-PASS/all-FAIL/MIXED rule. The asymmetry relative to a FAIL-any rule is defensible because the stated overall FAIL claim concerns all three models.

12. **§2.2, §6, §12.5, §16–18 — reconcile computation order with unavoidable logits and seal reconstructible means.**

    Replace all “no logits exist/computed” claims and associated tests with:

    > Required activation forwards and model-construction checks may generate logits internally. Those logits are discarded unread, except for declared identity/zero-patch checks. Donor logits are first retained for scientific use at V3; primary and control logits are first retained for endpoint/precision use at P1. Fresh A/Y/Z are not evaluated before T-PRE passes, apart from the declared target-free identity checks.

    Add:

    > Every validation endpoint-bearing secondary statistic is sealed until the fresh outcome is recorded, including primary/control contrast means, per-frame contrast means, repair, phase share, and summaries from which the primary endpoint mean can be reconstructed. Validation gate records and centered precision summaries remain available as declared.
    >
    > All production fits use calibration. The direct validation chart is a fixed-rule fidelity comparator only and is never used to construct interventions. Explicit exceptions to eligible-only evaluation include the declared all-row fits, M0 calibration panel, registry checks, sampler diagnostics, and branch-C chart panels.

13. **§11 V3 failure interpretation — remove an unsupported negative conclusion.**

    Replace:

    > “the model itself does not discriminate the two counterfactuals”

    with:

    > V3 did not establish that the model exceeds the prespecified 0.30 normalized discrimination threshold with the required lower bound. This can reflect insufficient discrimination, uncertainty, or a numerical/technical problem. It does not establish zero discrimination. The phase assay stops as specified.

## Optional suggestions

- **Retain the §20 scientific values.** I found no result-blind reason to change `c = 0.10`, alternative `0.20`, V3 threshold `0.30`, 32 frames, or the damage tolerances. The margin denotes a practical fraction of oracle discrimination, not predictive information or repair.
- The eligibility, support, decoder, V1, and V2 thresholds have no demonstrated structural impossibility. They can nevertheless stop a scientifically interesting cohort; that is an assay-feasibility outcome. The fraction-based rules substantially improve attainability over every-row support rules.
- Consider a scaled `1e-8` calibration-prediction tolerance for the RidgeProbe/Cholesky equivalence check, supported by synthetic ill-conditioned fixtures. Both implementations solve normal equations through different solvers; universal `1e-10` agreement is not established merely by estimator equivalence.
- Define `Sup(T)` and `Sup(C̄)` explicitly as pooled over arms, and clarify whether `Sup(D±)` is required separately for each donor arm.
- Retain the `1e-9` endpoint floor after fixing certification. It is small relative to the declared headroom and practical alternative.
- Replace §16’s unconditional “binomial SD ≈ 0.004” with the conditional expression
  \[
  \sqrt{f(1-f)(1/4096+1/n_{\rm sampled,test})}.
  \]
  The `0.02` fraction tolerance remains plausibly attainable.

## What I verified in code

I confirmed the document SHA256 matches the supplied value. Main and the accepted K4 worktree both resolve to `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`. Verification was source/document reading only; I ran no experiments or tests and opened no scientific payloads.

- **Donors and oracle:** grid symbol ordering, periodic overlap-emission construction, emit-first sampler/filter conventions, `b[:,31]`, `q[:,32]`, and `ce[:,31]`. The donor transform and closed-form posterior are mathematically correct under exact symmetry; stored-float symmetry is checked approximately. The crossed KL identity, \(A=G\) for oracle-matching arms, and \(G\ge0\) are correct in exact probability arithmetic.
- **Model:** `load_model` builds an eval-mode CPU model; ordinary forward lacks an internal `no_grad`; `forward_with_patch` replaces the declared residual site and casts replacements. Only LayerNorm and unembedding follow this site. The tail-path mathematical equivalence is correct.
- **Precision:** all three specified `precision.py` functions, their signatures, quantile conventions, MDE formula, power formula, and PASS conditions. The proposed Z inputs and alternative are correct. The k formula guarantees sufficient eligible rows when its fresh fraction condition holds; \(k\le5\) follows from \(f_{\rm val}\ge0.90\).
- **Decoders/support:** RFF draw order, bandwidth, standardization, pooled R², Ledoit–Wolf implementation, nested-ridge selection/refit, and RidgeProbe behavior. The C-14 refit recipe represents the same estimator. `support_report` indeed uses a default linear quantile and its own covariance fit.
- **Chart/reference:** chart/gauge serialization, string landmark ordering, extension/support definitions, chart gates, Decimal posterior-only return, and inheritance of trapping-context settings. C-15 and C-18 are correct. C-16’s normalization-rounding rationale matches the source; I did not empirically validate its tolerance.
- **Bindings:** exclusive artifact creation, stage prerequisites, release-specific bindings, meter defaults, worker-session lock check, memory cap, helper-import side effects, environment-import behavior, and the hidden lift CPU cap.

C-9, C-11, C-14, C-15, C-17, and C-18 are substantively supported by the code. C-10, C-12, and C-13 require the additions above. The existing code does not substantiate C-19’s claimed numerical certificate.