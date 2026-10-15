VERDICT: APPROVE_WITH_REQUIRED_CHANGES

The construction works. The gap conjecture is true, and the numerical values requested for independent re-derivation are correct. Freeze requires corrections to structural gates, numerical verification instructions, stop semantics, and downstream wording.

I verified the supplied document SHA256 and code commit `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`. This review used documents, source code, and hand derivations only. No experiments, tests, payload access, or writes occurred.

**Required changes**

1. **§5.2, G0.3 and G0.6 — correct the seam difference and array-identity requirement.**

   Replace the symmetric-difference sentence with:

   > The C and M edge sets share the seam edge {(3,1),(0,1)}. Their symmetric difference contains exactly four edges: C-only edges {(3,0),(0,0)} and {(3,2),(0,2)}, and M-only edges {(3,0),(0,2)} and {(3,2),(0,0)}.

   Replace G0.6 with:

   > E equals the literal array of §2.4 exactly. Construct the mixture emission array once as `vstack((E, E))`. Its two blocks must be bitwise equal to each other and to E (`np.array_equal`). Object identity between stacked slices, or between copies held by oracle instances, is not required.

   The existing “3 C-seam edges plus 3 M-seam edges” criterion would reject the correct construction.

2. **§2.6 — repair the flat-bounds proof.**

   Replace the graph-path and truncation bullets with:

   > Every vertex pair admits a shortest graph path of length at most 4. The cylinder diameter is 4; the Möbius diameter is 3. Such a shortest path lifts to a strip path ending at a copy with k ∈ {−1,0,1}, so its Euclidean endpoint distance is at most its graph length. Hence dist ≤ dist_graph.
   >
   > For each included deck copy, a Manhattan strip path projects to a graph path. Therefore its L1 distance is at least dist_graph, and its L2 distance is at least dist_graph/√2.
   >
   > Every omitted copy with |k| ≥ 2 has horizontal separation at least 5, exceeding √13, the maximum distance using k = 0. Thus the truncation equals the full quotient metric, which satisfies the triangle inequality.

   Arbitrary graph paths are not bounded in length, and 4 is not M’s diameter.

3. **§3.6, CONJ, §5.3, R12, S4, and corresponding summary/changelog references — adopt F as a theorem.**

   Replace the heading and status language with:

   > **Theorem F: decision-phase gap formula.** F1–F3 hold for every history satisfying their stated hypotheses. They have been independently proved before freeze.

   Retain F1–F3 unchanged. The derivation below supplies the independent proof.

   Replace CONJ with:

   > **G2.11: Theorem F.** At every decision-phase node, verify F1 and F2 exactly. Report the number of nodes satisfying |δ_M| > |δ_C|; it must be positive because h_max is enumerated. Verify F3 on the posterior-isolation pair in G3. Every discrepancy is an exact-identity failure.

   Replace S4 with:

   > Any violation of Theorem F invokes S3. There is no post-result conjecture-withdrawal route.

   Remove “reported, not gating” and “CONFIRMED / REFUTED” treatment throughout. Theorem F is now proved; its prescribed exact checks should have the same failure semantics as other theorem checks.

4. **§3.6 consequences, §3.7 lazy-stay discussion, and §4 winding count — state the precise domains.**

   Use this dwell text:

   > Conditional on an observed same-column dwell in a band column, μ′_f = μ_f K/c and δ′_f = (2/3)δ_f at the frozen p_stay = 1/5. This factor does not apply to horizontal steps within the band or to column-1 dwells followed by an A/B observation. If μ_M = R^par μ_C held before the band-column dwell, it continues to hold afterward. For general a = (1−p_stay)/4, the dwell factor is (1−3a)/(1−2a).

   In §4, replace the unrestricted winding-count statement with:

   > For the tabulated range t ≤ 8, an odd winding returning to column 1 has net horizontal displacement ±4. Among k horizontal moves, its number of sign patterns is 2·binom(k,(k+4)/2), for even k ≥ 4. At longer horizons, other odd multiples of 4 must also be included.

5. **§5.2 G5 and §6.2 Decimal trap — make precision handling and trap detection definite.**

   Append to G5:

   > For comparison, convert each returned Decimal directly to Fraction, without passing through float. Compare posterior entries using `abs(Fraction(d) − q) ≤ Fraction(1, 10**45)`. Compute the M-block sum from these Fractions before comparing it with the exact posterior. Alternatively, all conversions, sums, and differences must occur inside an explicitly declared 80-digit local Decimal context.

   Replace the unspecified trap with:

   > Use history (A,A), the production `TransitionBuilder` float64 kernels, the exact dyadic emission array, and the fixed start. With Decimal string inputs representing the rational model, the reference must agree with the exact posterior within 1e−45. With the production float kernels passed directly, at least one mixture-posterior entry must differ from the rational posterior by more than 1e−19. This expected discrepancy is the trap’s success condition.

   Delete the blanket claim that float inputs necessarily disagree near `1e−17`. Float kernels obtained by directly rounding the Fraction entries can have a common transition-scale error that cancels from every posterior. The production-kernel trap above avoids that cancellation.

6. **§5.1, §5.3, §5.2 G6, and S3/S5 — reconcile stopping, controls, and mandatory checks.**

   Replace the operational verdict text with:

   > A baseline gate failure terminates the run with FAIL at the first failed required criterion; remaining gates are recorded as NOT_RUN. FAIL does not require completion of all gates. An inability to evaluate a gate invokes the applicable INVALID rule.
   >
   > Expected rejections inside positive-control harnesses are captured and do not themselves invoke baseline stop rules. L1 evaluates both the emission mismatch and the uninformed-node posterior mismatch independently. L2 evaluates the specified kernel-row identity directly. A missing expected detection is a G6 failure.
   >
   > PASS requires all specified oracle gates and the mandatory regression, new-test, registry-hygiene, geometry-guard, Decimal-trap, and file-size checks in §6.1–§6.2 to pass.

   This resolves the current conflict between “run completed,” first-failure stopping, and controls that deliberately violate baseline identities.

7. **§1.3 and §7.3.3 — remove the claim that a recurrent model must explicitly carry π.**

   Replace the architecture caveat with:

   > A transformer can re-read the history at the next position. A deterministic recurrent state that updates recursively and is sufficient for exact next-symbol prediction at every reachable history must distinguish h_A from h_B, by Lemma D and their differing two-step laws. This requires preserving predictive information that separates the pair; it does not prove an explicit encoding of π or any particular representation geometry. At the relevant band-edge histories, exact next-symbol predictions depend on that information.

   This is the main licence overstatement in the document. The oracle theorem does not establish what an arbitrary trained model learns, stores, or uses.

8. **Open questions 5–6 and §5.4/§6.2 — close the remaining freeze bindings.**

   Bind the proposed choices explicitly:

   > Enumeration depth: K = 8. Module: `tools/d1_seam/d1_seam.py`. Independent test file: `tests/d1_seam/test_d1_seam.py`. Output store: `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`. Base commit: `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`. Request SHA256: `45B0E80152E324D2A0833DC5BC3B75853E1E9FD18B27C152887E41346CEB7528`. The freeze record must contain the amended protocol’s SHA256. G5 covers all reachable histories of lengths 1–5 and all named histories.

   These are existing proposed choices, not new scientific parameters.

**Independent re-derivations**

**Decision-phase gap formula**

Let \(u=\delta_C\), \(v=\delta_M\). Since
\[
e(y)=\frac12+\frac{\mathbf1_{y=0}-\mathbf1_{y=2}}4,
\]
the mean A-readout under \(\mu_f\) is \(1/2+\delta_f/4\).

The only two-step routes from column 3 to column 1 are \(3\to2\to1\) and \(3\to0\to1\), each with probability \(a^2\). Therefore
\[
\begin{aligned}
J_C(\sigma_2,A)&=J_C(\sigma_0,A)=a^2(1/2+u/4),\\
J_M(\sigma_2,A)&=a^2(1/2+v/4),\\
J_M(\sigma_0,A)&=a^2(1/2-v/4).
\end{aligned}
\]
The corresponding B differences are the negatives. Every band-only entry is world-independent. Thus
\[
\operatorname{TV}(J_C,J_M)
=\frac{a^2}{4}\bigl(|u-v|+|u+v|\bigr)
=\frac{a^2}{2}\max(|u|,|v|).
\]

After summing over the first symbol, M assigns \(a^2\) to each of A and B, while C assigns
\[
a^2(1+u/2),\qquad a^2(1-u/2).
\]
Consequently,
\[
\operatorname{TV}(Q^{dist}_{2,C},Q^{dist}_{2,M})
=\frac{a^2}{2}|u|.
\]

For equal conditional beliefs at \(h,h'\),
\[
J(h)-J(h')=(\pi(h)-\pi(h'))(J_M-J_C),
\]
which proves F3. No counterexample exists under the stated hypotheses.

**Enumeration counts**

With column order \((0,1,2,3)\), the given recurrence produces:

| \(t\) | \(v_t\) | Total |
|---|---|---:|
| 1 | (0,2,0,0) | 2 |
| 2 | (2,4,2,0) | 8 |
| 3 | (6,16,6,4) | 32 |
| 4 | (26,56,26,16) | 124 |
| 5 | (98,216,98,68) | 480 |
| 6 | (382,824,382,264) | 1,852 |
| 7 | (1470,3176,1470,1028) | 7,144 |
| 8 | (5674,12232,5674,3968) | 27,548 |

Summing the totals gives **37,190**. Summing the fourth components gives **5,348** histories ending in \(\sigma_3\). The total through length 5 is **646**.

**Decision-phase probability**

The projected x-kernel has Fourier eigenvalues \(1,c,1-4a,c\), namely \(1,3/5,1/5,3/5\). Starting at column 1, the probability of the opposite column is
\[
P(X_t=3)=\frac14\left[1-2(3/5)^{t-1}+(1/5)^{t-1}\right].
\]

For \(t=1,\ldots,8\), this gives
\[
0,\ 0,\ \frac2{25},\ \frac{18}{125},\ \frac{116}{625},\
\frac{132}{625},\ \frac{3542}{15625},\ \frac{18438}{78125}.
\]
Every table entry and its decimal rendering is correct.

At \(t=3\), both shortest routes to column 3 have no dwell. Their endpoint asymmetries have magnitude 1 in both worlds, so all four decision-phase histories have TV \(1/50\).

**Start-law artefact**

For a C-path returning to column 1 at odd seam parity, the A-readout difference is
\[
e(y)-e(Ry)=\tfrac12(\mathbf1_{y=0}-\mathbf1_{y=2}).
\]
The antisymmetric component of \(K\) has eigenvalue \(2/5\). For \(n=t-1\le7\),
\[
D_t=\frac12
\sum_{\substack{4\le k\le n\\ k\ {\rm even}}}
\binom nk\,2\binom{k}{(k+4)/2}\,
a^k(2/5)^{n-k}.
\]

Hence
\[
\begin{aligned}
D_5&=a^4=\frac1{625},\\
D_6&=5a^4(2/5)=\frac2{625},\\
D_7&=15a^4(2/5)^2+6a^6=\frac{66}{15625},\\
D_8&=35a^4(2/5)^3+42a^6(2/5)=\frac{364}{78125}.
\end{aligned}
\]
For \(t\le4\), \(D_t=0\). Band-symbol marginals agree, and the B difference is \(-D_t\), so single-symbol TV is \(|D_t|\).

**Band-edge witness**

For \(h_{\rm edge}\), five horizontal moves contribute \(a^5\). The two A-readouts give
\[
P_C=\frac9{16}a^5,\qquad P_M=\frac3{16}a^5.
\]
Thus
\[
\pi=\frac14,\qquad P(h_{\rm edge})=\frac38a^5=\frac3{25000}.
\]

The stated conditional next-symbol vectors follow from endpoints \((2,0)\) and \((2,2)\). Their TV is \(a/2=1/10\). Mixing with weights \(3/4,1/4\) gives
\[
(0,3/5,1/5,1/8,3/40),
\]
as stated.

**The \(h_{\max}\) probe**

There are six horizontal moves and one column-1 dwell.

In C, the initial and middle A-readouts contribute \((3/4)^2\). The subsequent dwell followed by B has unnormalised y-weights
\[
(2/5)(1/4),\quad (1/5)(1/2),\quad0
=(1/10,1/10,0).
\]
Therefore
\[
P_C=\frac9{80}a^6,\qquad \mu_C=(1/2,1/2,0).
\]

In M, the middle A-readout occurs at row 2 and contributes \(1/4\). The dwell-B weights are \(3/10\) at row 2 and \(1/10\) at row 1. The final seam crossing reflects these:
\[
P_M=\frac3{40}a^6,\qquad \mu_M=(3/4,1/4,0).
\]
Consequently,
\[
\pi=\frac25,\qquad P(h_{\max})=\frac3{32}a^6=\frac3{500000}.
\]

The A-slices are exactly those listed:
\[
\begin{array}{c|cc}
& C&M\\ \hline
\sigma_2&A:\ 5a^2/8&A:\ 11a^2/16\\
\sigma_0&A:\ 5a^2/8&A:\ 5a^2/16
\end{array}
\]
giving joint TV \(3/200\) and distant-marginal TV \(1/100\).

**Dwell shrinkage and the additional [W] claims**

For \(\mu'=\mu K/c\),
\[
\delta'=\frac{(2/5)\mu(0)-(2/5)\mu(2)}{3/5}
=\frac23\delta.
\]
This is specifically an observed band-column dwell. A horizontal band step need not shrink anything: \(h^*\sigma_2\), for example, preserves C’s asymmetry at 1.

The §3.7 band-entry assertion is correct: an uninformed history returning from column 1 cannot have odd parity at that outside observation. Entry without a crossing therefore has even parity and equal conditional beliefs.

For N3’s additional example \((A,A,\sigma_2,\sigma_3,\sigma_0,A)\), starting at \(y=1\),
\[
P_C=\frac7{80}a^4,\qquad P_M=\frac5{80}a^4.
\]
The stated C/M likelihood ratio **7/5** is correct; its world posterior is \(5/12\).

**Proofs A–E**

- **Lemma 1 and A:** Correct. Each horizontal direction has probability \(a\), while vertical moves plus the self-loop have total \(c\). All next columns from column 3 emit band symbols.
- **B:** Correct. The forced column-path probability is shared, and every outside emission lies in \([1/4,3/4]\). Both supports coincide. The coupling sharpens the likelihood-ratio bound to \(3^{\pm m_{\rm odd}}\).
- **C:** Correct. The path map \((x_s,y_s)\mapsto(x_s,R^{par_s}y_s)\) preserves initial and transition weights. Only odd-parity outside emission factors change. Equal starts suffice; reflection symmetry is unnecessary.
- **D:** Correct. Closed recursive one-step sufficiency implies all-horizon sufficiency by the chain rule. D1 also uses the equal initial-symbol laws, which hold here. D2 follows by conditioning on the shared first-symbol law; its KL version is valid as well.
- **E:** Correct. The direct path calculations give the stated arrays and probabilities.

In particular, at \(h^*\),
\[
P(h^*)=(3/4)a^2=3/100,
\]
and only the \((\sigma_0,A/B)\) entries differ, by \(\pm2/100\). Thus both TVs are \(1/50\),
\[
KL=\frac{\ln3}{50},\qquad
I(Z;W_{t+1:t+2}\mid h^*)=\frac{\ln(27/16)}{100}.
\]

For the posterior pair, the likelihoods are \(27a^{10}/64\) versus \(9a^{10}/64\), swapped between the histories. Hence the posteriors are \(1/4,3/4\), each history has probability \(9/312500000\), and pair TV is
\[
(3/4-1/4)(1/50)=1/100.
\]
The \(1/200\) merged-prediction lower bound follows from the triangle inequality.

**Surface and orientability certificates**

The stated cell counts, boundary components, and link examples are correct:

- \(12-20+8=0\).
- Eight boundary edges have one incident square; twelve interior edges have two.
- Boundary-row vertex links are three-node paths; middle-row links are four-cycles.
- C has two boundary 4-cycles; M has one boundary 8-cycle.

For the orientation test, choose each square’s local \((x,y)\) orientation. Ordinary dual adjacencies require equal face signs. C’s seam does too. M’s seam requires the opposite sign across the reflected identification.

The ordinary adjacencies connect all eight faces. Their equations leave one free common coefficient. In C, seam equations preserve it; in M, they impose \(s=-s\). Therefore the interior-edge matrix has:

| Field | C rank / nullity | M rank / nullity |
|---|---|---|
| GF(3) | 7 / 1 | 8 / 0 |
| GF(2) | 7 / 1 | 7 / 1 |

This independently establishes the claimed ranks and orientation obstruction. Full rank modulo 3 also implies full column rank over the rationals.

The **full** boundary matrix has rank 8 in both worlds: boundary-edge equations kill the remaining face coefficient. Together with connectedness, this gives Betti numbers \((1,1,0)\). These are absolute homology ranks; the orientability comparison uses the interior-edge restriction.

**Code facts, tolerances, controls, and stops**

The inspected source supports the reuse plan:

- [`validate_process`](X:/Downloads/projects/topo-pilot/topo-pilot/tools/x4_oracle_profile/oracle_profile.py:69) exists and enforces stationarity at `1e-12`.
- `TransitionSpec.validate` also requires a stationary `pi`.
- [`as_model`](X:/Downloads/projects/topo-pilot/topo-pilot/src/topo_pilot/oracle/_common.py:26) checks stochastic shapes and values but does not require stationarity. The fixed start is therefore accepted by unchanged `BayesFilter`.
- [`BayesFilter`](X:/Downloads/projects/topo-pilot/topo-pilot/src/topo_pilot/oracle/_filter.py:30) uses the stated emit-then-transition convention.
- [`FutureOperator`](X:/Downloads/projects/topo-pilot/topo-pilot/src/topo_pilot/oracle/_futures.py:15) computes F2 as the joint, with shape `[R,V,V]`. Summing axis 1 gives the distant marginal.
- The Decimal reference is [`decimal_suffix_posterior`](X:/Downloads/projects/topo-pilot/topo-pilot/tests/oracle_profile/independent_reference.py:86). Its conversion helper preserves Decimal inputs and otherwise converts through float.
- The local builder avoids registry dispatch as stated. `is_x_periodic` finds precisely one of three straight wrap edges and would raise `INVALID_GLUE`.

For the required Decimal trap, write the production horizontal probability as \(r\) and boundary diagonal as \(d\). At history \((A,A)\), the conditional row-0 posterior is
\[
\frac{3d}{3d+2r},
\]
whose difference from \(3/4\) is
\[
\frac{3(d-2r)}{4(3d+2r)}.
\]
Production float64 arithmetic gives \(d-2r=-2^{-53}\), producing about \(2.6\times10^{-17}\) error in a mixture entry. Conversely, directly rounding exact \(1/5,2/5\) entries preserves their common scale, which cancels in posterior normalisation.

The `1e-15` production-T comparison, `1e-12` predictive comparisons, stated evidence tolerances, and `1e-45` Decimal criterion are reasonable for these small, short computations. No tolerance needs loosening. Numerical acceptance remains unexecuted.

N1, N2, N3, L1, L2, and P1 have the stated outcomes. N3 correctly avoids claiming that all informed histories become world-independent. L2 should remain a direct kernel-row control because its altered alphabet no longer identifies columns as in the baseline.

S0–S2 and S6–S7 are suitable. S3/S5 need the clarified early-failure semantics above; S4 should be replaced after adopting Theorem F. The runtime estimates remain forecasts, not verified measurements.

**Licence**

With required change 7, the licence stays within an orientability existence result for this fixed HMM and decision phase. The posterior-isolation pair proves a need to preserve predictive information separating the histories. It does not prove an explicit posterior code, learned geometry, causal use by trained models, or relevance to the square/cylinder pilot.

**Optional suggestions**

- Deduplicate the G5 history set: there are **650 distinct histories**; 651 calls includes \(h^*\) twice.
- In the report, retain an explicit negative orientation-cycle witness for M, alongside the rank and boundary-component counts.