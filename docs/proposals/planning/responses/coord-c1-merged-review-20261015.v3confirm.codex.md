NOT_CONFIRMED

1. **§15.3.5 L5 — the outward-evaluation lemma is false as stated.**

   Six multiplications on a root-to-leaf path do not mean that an underflow error encounters only five further factors bounded by \(2^{21}\). Those factors can themselves be products.

   Counterexample: a balanced product of 64 leaves, one \(2^{-1074}\) and 63 equal to \(2^{21}\). It satisfies the stated depth and leaf limits. Under FTZ/DAZ, its computed value can be zero, with every intermediate finite, whereas its exact value is \(2^{249}\). `OUT(0)` does not enclose it.

   **Exact fix:** retain the displayed bound formulas and `OUT`, but replace L5’s premises and proof with:

   > L5 applies specifically to the expanded C1 bound expressions. Each expression has nonnegative leaves bounded by \(2^{23}\), total polynomial degree at most 7, at most \(2^{16}\) expanded monomials, and at most \(2^{17}\) arithmetic nodes after shared subexpressions are replicated. These counts include the evaluation \(\bar\rho=\rho+\rho^2\).
   >
   > P2 checks the \(2^{23}\) bound on every data leaf used in bound evaluation. Constants are replaced by `up(c)`.
   >
   > Normal-range rounding contributes a factor at most
   > \[
   > (1-u)^{-2^{17}}\le1+2^{-35}.
   > \]
   > Expanding the nonnegative contexts through which an additive underflow error propagates gives at most \(2^{16}\) monomials of degree at most 7. Including all \(2^{17}\) possible events and subsequent relative rounding, their total contribution is bounded by
   > \[
   > 2^{-1000}\,2^{17}\,2^{16}\,(2^{23})^7\,2
   > =2^{-805}<\zeta.
   > \]
   > Thus \(E\le(1+2^{-35})\widehat E+\zeta\le OUT(\widehat E)\). Intermediate values are bounded by \(2^{178}\), excluding overflow.

   Include an expression-count table establishing these limits for \(b^G,b^A,b^Y,b^Z,b^{Zf}\). Remove the incorrect “fewer than 7,000 leaves” assertion. Restrict S1’s L5 fixtures to the revised premises.

   **Also correct lemma U:** P2 bounds final scores, not every intermediate operand. Use an operand bound of \(2^{64}\) for the prescribed score/mean kernels and propagation factors at most \(2^{23}\). The corresponding allowance is
   \[
   2^{16}2^{-936}2^{47}=2^{-873}<\zeta.
   \]
   Update §23.4’s verification claims accordingly. The main score formulas need no redesign.

2. **§3.2–3.4, §15.3.12, §16 H3, and ruling 5 — two independently rounded evaluations need a combined bound; the closed form also has a stored-symmetry defect.**

   The single-evaluation `2e-12` justification does not establish a `2e-12` comparison between two evaluations. Moreover, emission symmetry is presently approximate, so the exact stored-weight closed form need not equal the direct donor posterior.

   **Exact fix:** replace ruling 5 and its restatements with:

   > Named/canonical comparisons on the normal fast path use componentwise relative tolerance \(4\cdot10^{-12}\), accounting for both evaluations. This remains an operational integrity check, outside Theorem 6.
   >
   > For the closed-form comparison, verify exact permutation invariance of T and π. Measure
   > \[
   > r_E=\max_{k,z,v}
   > \left|\frac{E[\rho_kz,\tau_kv]}{E[z,v]}-1\right|
   > \]
   > in exact rationals. For \(r_E<1\), put \(\epsilon_E=r_E/(1-r_E)\). The exact normalized donor and closed-form posteriors have componentwise log-ratio discrepancy at most \(62\epsilon_E\), accounting for the 31 transformed emissions.
   >
   > With \(\delta=2\cdot10^{-12}\), set
   > \[
   > t=\frac{2\delta}{1-\delta}+62\epsilon_E.
   > \]
   > When the normal-range comparison assumptions hold and \(t\le3/2\), require componentwise relative agreement within \(t+t^2\). Otherwise use validated enclosures for both computations, including the stored-symmetry discrepancy; do not apply the single-evaluation tolerance.

   The factor 62 follows from 31 emission log-errors and normalization: the unnormalized log-ratio range has width at most \(62\epsilon_E\). Common transition, emission and normalization operations do not increase that oscillation.

   Apply this rule to every normative occurrence. The supplied v3 still contains the superseded absolute `1e-12` rules.

3. **Ruling 6, §3.4, and §15.3.12 — distinguish reference-enclosure width from operational error.**

   A 60-digit enclosure has width around \(10^{-55}\). Requiring a float64 result to lie within that reference-only width would reject ordinary float64 rounding. Ruling 6 needs an explicit acceptance rule.

   **Exact fix:** replace it with:

   > For a P1-failing H3 reference history, construct the exact-rational reference interval
   > \[
   > I_v=\left[
   > \frac{\tilde x_v}{1+\beta_x},
   > \frac{\tilde x_v}{1-\beta_x}
   > \right],
   > \]
   > using the posterior envelope for a posterior and \(\beta_q\) for a predictive. The enclosure width represents reference uncertainty, not an allowed float64 error.
   >
   > Retain the absolute H3 implementation tolerance \(a=2\cdot10^{-12}\). Define
   > \[
   > D_{\rm low}=\max_v\operatorname{dist}(\hat x_v,I_v),\qquad
   > D_{\rm high}=\max_v\max_{y\in\partial I_v}|\hat x_v-y|.
   > \]
   > PASS if \(D_{\rm high}\le a\); FAIL_TECHNICAL/ORACLE if \(D_{\rm low}>a\); otherwise INCONCLUSIVE/NUMERICAL.
   >
   > Predictive certification separately uses route F’s measured discrepancy and P4. Zero operational posterior entries caused by underflow do not themselves fail P4, which concerns predictives.

   This preserves the existing absolute implementation tolerance while using the reference’s proved width correctly.

4. **§1.2–1.3, §12.1, the MERGE erratum, and associated tests — the exact cancellation and perfect-readout claims contradict v3’s literal, potentially unnormalized predictive target.**

   The \(\omega_{TE}\) correction in Theorem 3 correctly recognizes this issue. The surrounding exact identities have not been updated.

   **Exact fix:** insert the following qualification and replace conflicting unconditional identities:

   > Exact probability-normalization identities below apply when the two oracle predictives have equal mass. For the literal stored-weight target, let
   > \[
   > m_\pm=\sum_v q^{*\pm}(v),\qquad
   > \delta_m=m_+-m_-.
   > \]
   > Then \(|\delta_m|\le\omega_{TE}\). A symbol-constant arm difference k contributes \(\tfrac12k\delta_m\); it does not cancel identically unless \(\delta_m=0\).
   >
   > Under a common inverse-temperature β,
   > \[
   > A_\beta=\beta A-\tfrac12\delta_m
   > \bigl(\log Z_\beta^+-\log Z_\beta^-\bigr).
   > \]
   > Arm-common additive log-probability perturbations still cancel exactly.
   >
   > For an oracle-perfect probability readout
   > \(p^\pm=q^{*\pm}/m_\pm\),
   > \[
   > A_{\rm oracle}
   > =G^*-\tfrac12\delta_m\log(m_+/m_-).
   > \]
   > Thus the exact unit anchor holds when \(m_+=m_-\); otherwise it has this explicit mass correction. Control adjustment additionally subtracts \(E[\overline A_C]/E[G^*]\).

   Keep the certified target and numerical method unchanged. Qualify the “KL/regret” terminology as literal stored-weight sums where the inputs are not normalized probability vectors. Update the corresponding exact-identity tests and the merge addendum.

5. **§16, §18, and §22 F6 — exception adaptation remains underspecified.**

   RC8’s bindings are otherwise correctly applied, but F6 still leaves outcome classification to implementation.

   **Exact fix:** add:

   > `ProfileError` and reference-input `ValueError` produce FAIL_TECHNICAL/ORACLE. Decimal exceptions and watched certificate flags produce FAIL_TECHNICAL/NUMERICAL. Other `StageFailure` instances produce FAIL_TECHNICAL at the offending gate, preserving their original code and message, except `PH_RESOURCE_LIMIT`, which produces INCONCLUSIVE/RESOURCE, and `GATE_FAILED` representing an explicitly declared unmet criterion, which produces that criterion’s specified INCONCLUSIVE status. Existing `Unresolved`, STOP, usage and resource handling retain their declared classifications.

   Mark F6 resolved with this mapping.

6. **§11 and computation-order restatements — finish the consequential consistency edits.**

   **Exact fixes:**

   - Replace §11’s “Otherwise INCONCLUSIVE/MODEL_HEADROOM” with:

     > V3’s outcome follows exactly the three-way signed rule of §15.3.11(V): PASS, INCONCLUSIVE/MODEL_HEADROOM, or INCONCLUSIVE/NUMERICAL; technical failures retain their specified precedence.

   - Replace unqualified “Fresh A/Y/Z … before T-PRE” statements in §2.2 and the test list with:

     > Fresh primary/control A, Y, Z and their bounds are not evaluated before T-PRE passes. A_full, Z_full and their bounds are evaluated inside T-PRE for V3.

   - Replace §18’s invariant “every fit and the gauge use calibration only” with:

     > Every production fit and production gauge use calibration only; the declared direct validation chart is a fidelity comparator.

   - Incorporate rulings 5–6 into the protocol itself rather than leaving conflicting normative rules alongside them.

7. **§15.3.13 — the numerical-inconclusiveness probability projection reverses the implication of the power gate.**

   P1 does not imply a lower bound on standard error. A power requirement generally constrains it from above. The stated density assumption and \(SE\ge10^{-4}\) are additional assumptions.

   **Exact fix:** replace the concluding probability paragraph with:

   > Conditional on a bootstrap-bound density no greater than that of a normal distribution with standard deviation \(10^{-4}\), a union bound gives approximately \(5\cdot10^{-5}\) for one of six endpoint bounds entering a ±\(10^{-9}\) band. Neither this density condition nor the standard-error lower bound follows from P1. This is an illustrative projection, not a guarantee that numerical inconclusiveness is practically excluded.

The supplied SHA256 matches. RC1–13 are otherwise applied, including the recorded MERGE erratum. I accept the canonical-process identity ruling, H5 wrapper, guard-band labels, and operational-only scope. The ordered-reference/projective argument, measured-discrepancy transfer, route-F predictive envelope, M-ln bound, score bounds, balanced-tree mean bound, ranks, and signed-guard implications check out subject to the fixes above. Verification remained read-only; no experiments, tests, or scientific payload access occurred.