NOT_CONFIRMED

1. **§3.2 enclosure branch, V4-F4(a), and §16 H3 — the fallback does not check the operational outputs.**

   It compares the two Decimal references but ignores the float64 posteriors whose failed fast-path check selected this branch. An incorrect float64 closed-form result could therefore pass.

   **Exact fix:** append:

   > Construct \(I_D\) and \(I_C\) from the respective Decimal posteriors and their envelopes, using §3.4’s interval construction. Check each operational float64 posterior against its own interval using §3.4’s absolute tolerance \(a=2\cdot10^{-12}\) and \(D_{\rm low}/D_{\rm high}\) rule. Nonfinite operational values are FAIL_TECHNICAL/ORACLE.
   >
   > The branch passes only if both operational checks and the existing Decimal-reference symmetry comparison pass. A definite violation is FAIL_TECHNICAL/ORACLE; an undetermined operational interval comparison is INCONCLUSIVE/NUMERICAL.

   Update §16’s status column and add a synthetic fixture where corrupted float64 closed-form values select this branch while both Decimal references remain correct.

   **The existing \(\beta_C=\texttt{posterior_envelope}(32,N)\) can remain.** Its justification needs more than “same structure”: the intermediate normalization denominator cancels as a common factor. Including its componentwise division rounding, each positive path has at most
   \[
   2+31(N+2)=4528
   \]
   roundings before final normalization, below the envelope’s count \(1+31(2N+2)=8991\). Record this derivation.

2. **§1.3 and §12.1 — the necessary condition stated for \(\theta=1\) is incorrect.**

   A negative control mean can cancel the positive mass correction. Equal masses and zero control mean are sufficient, but are not jointly necessary.

   Replace both occurrences of “θ = 1 only when, in addition, \(E[\overline A_C]=0\)” with:

   > For an oracle-perfect primary probability readout, write
   > \(R_m=\tfrac12\delta_m\log(m_+/m_-)\). Then
   > \[
   > \theta=1\iff E[R_m]+E[\overline A_C]=0.
   > \]
   > Under equal masses almost surely, this reduces to \(E[\overline A_C]=0\). The primary anchor \(\theta_T=1\) holds exactly when the masses are equal almost surely.

3. **§3.2’s opening “Consequences” and §4’s exact-plausibility explanation — these still assume exact emission symmetry.**

   V4 correctly introduces a nonzero stored-emission symmetry defect, but these earlier statements remain unconditional equalities.

   **Exact fix:** introduce the displayed equalities in §3.2 with:

   > Under exact emission equivariance, the following identities hold. For the literal stored weights, their deviations are controlled by \(\epsilon_{\rm sym}\) below; they are not asserted as exact equalities.

   Replace §4’s exact-plausibility explanation with:

   > Under exact emission symmetry, transforming the first 31 symbols preserves their prefix likelihood. For the stored weights,
   > \[
   > \left|\log L(\tau_kH_{1:31})-\log L(H_{1:31})\right|
   > \le31\epsilon_{\rm sym},
   > \]
   > where L is the literal stored-weight prefix likelihood. Donor last-symbol surprisal measures the final-step contribution; the prefix contribution is bounded as above. The operational eligibility rule remains unchanged.

4. **§15.3.5’s constant-leaf annotations — `up(c) ≤ 2` is false for the displayed constant 2.**

   By definition, `up(2)` is the next float above 2. This does not invalidate L5’s \(2^{23}\) leaf limit.

   **Exact fix:** replace both constant-leaf assertions “`up(c) ≤ 2`” / “constants are ≤ 2” with:

   > All upward-rounded constant leaves are less than 3, hence below L5’s \(2^{23}\) leaf limit.

   In the supplementary proof, replace “\(C_n|b|\) is a sub-polynomial of E” with:

   > Its formal monomials are obtained from relevant monomials of E by deleting factors; their count and degree therefore remain within the stated limits.

The supplied SHA256 matches. The seven fixes are otherwise applied correctly. I accept V4-F1, F2, F3, F4(b), F6–F8, and the substantive F5 bounds and expression counts, subject to the annotation correction above. No experiments, tests, or scientific payload access were performed.