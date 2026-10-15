VERDICT: APPROVE_WITH_REQUIRED_CHANGES

1. **Limit A3’s interpretation to the classifier actually tested.**

   A3 compares the full-history Bayes classifier with one fixed block-product classifier. It does not exclude overlapping short-window scores, different block boundaries, reweighted scores, or other combinations of local evidence. Missing evidence at the three block boundaries can itself produce a gap.

   Replace the E2 explanation in §1.2 with:

   > E2: the full joint likelihood improves on the fixed product of four disjoint stationary 8-block likelihood ratios.

   Replace the meaning of GO_P1_NONADDITIVE in §5.9 with:

   > Meets the priority-1 feasibility criteria at context 32 and establishes an accuracy advantage of at least 0.03 over the specified four-block classifier. This does not establish that no other aggregation of short-window evidence could reproduce the advantage.

   Add to §1.4 and apply to every interpretation of A3:

   > NONADDITIVE is an operational label for this frozen four-block comparison. The blocks are dependent in the actual process; the comparator treats them as conditionally independent. Its failure does not, by itself, identify a long-timescale mechanism. The N-local control tests specificity against one comparator mechanism only.

2. **Correct the fallback and STOP licences.**

   Failure to establish a gap of at least 0.03 does not establish equivalence within 0.03. This matters even though the expected Monte Carlo intervals are narrow.

   Replace the GO_P1_ADDITIVE licensed continuation in §1.4 with:

   > “The comparison did not establish a full-history accuracy advantage of at least 0.03 over the specified product of four disjoint 8-block likelihood ratios. The reported interval distinguishes evidence of a small gap from an inconclusive comparison. This fallback label does not establish equivalence or identify an additive mechanism.”

   Add:

   > If U99(D_add) < 0.03, the report may additionally state that the advantage over this comparator is below 0.03 at the stated confidence level. Otherwise it must describe the A3 comparison as inconclusive with respect to that margin.

   Replace the STOP_P1 licensed sentence with:

   > “At t* = 32, this construction did not meet the preregistered feasibility criteria for a later priority-1 study: P3 = … and P4 = …. A threshold-inconclusive result does not establish that the corresponding population criterion fails.”

   Append this exact boilerplate to **each** licensed outcome paragraph, including STOP:

   > “This concerns component identity, not the circular coordinate. Short windows are not blind: I_2 > 0. All pre-run information-size estimates were forecasts; decisions use computed quantities.”

3. **Replace Lemma A(2): conditional independence is sufficient, not necessary.**

   Replace item 2 and its proof sentence with:

   > 2. Conditional independence of the four blocks given c is sufficient for s_add to equal the full-history log-likelihood ratio. More generally, define  
   > R_c(h) := P_c(h) / ∏_{\ell=1}^4 P_c(block_\ell).  
   > Then  
   > LLR_32(h) = s_add(h) + ln R_B(h) − ln R_A(h).  
   > Thus equality holds exactly when R_A(h) = R_B(h), which need not require independence. The blocks in this construction are dependent given c; no calibration or exact-likelihood property is assumed for π_add.

   Replace “π_add is therefore not a calibrated posterior” wherever justified solely by dependence with:

   > π_add is a pseudo-posterior whose calibration is not assumed.

   Identical dependent component laws already provide a counterexample to the original “iff”: both likelihood ratios equal one despite dependence.

4. **Make the tolerance tie rule consistent with the Bayes-accuracy estimand.**

   The credit estimator is correct. However, declaring a tie within τ = 1e-12 defines a classifier that can differ slightly from the exact Bayes classifier.

   Add immediately after the tie rule in Lemma C:

   > Write acc_k^τ for the accuracy of the tolerance-tie classifier. Then  
   > 0 ≤ acc_k − acc_k^τ ≤ τ.  
   > Credit estimates acc_k^τ exactly in expectation. The max-posterior form estimates acc_k. For the additive classifier, the tolerance-tie rule is part of its definition.

   Replace P3’s PASS condition with:

   > L99(D3) − τ ≥ 0.10, where D3 uses the tolerance-tie window classifier and τ = 1e-12.

   Retain its FAIL condition, `U99(D3) < 0.10`. Apply the same adjustment to its Hoeffding robustness calculation.

   Replace G4.7 with:

   > The credit and max forms of acc_8^win differ by at most 4·SE of their paired difference plus 2e-12.

   Add to §5.5:

   > All other G4 sampling-error comparisons include an additional absolute arithmetic allowance of 2e-12; the Hoeffding requirements remain unchanged.

5. **Correct the uncertainty ranges, precision claim, and false-FAIL wording.**

   Replace the range/precision discussion in §6.3 with:

   > For n = 2^20 independent rows, Hoeffding uses the range length of the particular statistic: ln 2 for each entropy-based I_t or I_k; 1/2 for max-posterior accuracy; and 1 for credits, D3 and D_add. At δ = 1e-6 the respective half-widths are 0.001823157, 0.001315130 and 0.002630260. These bounds do not automatically apply to I′, I_add^LB, LLR summaries, or arbitrary differences of information statistics.
   >
   > The corresponding distribution-free SE upper bounds are 0.000338451, 0.000244141 and 0.000488281. A credit-gap 99% normal half-width can therefore reach 0.001257813. The separate-bound P4 expression can require a margin of up to approximately 0.001307774. Smaller empirical SEs may give narrower intervals.

   After the horizon correction below, replace §5.5’s false-FAIL paragraph with:

   > There are 49 four-SE comparisons. Under a normal approximation, a union-bound calculation gives approximately 49 × 6.334e-5 = 0.00310, or 0.31%, for the family’s false-FAIL probability. This is an asymptotic diagnostic, not a finite-sample upper guarantee. A G4 failure invokes S5; there is no increase of n or reseeding.

6. **Make the “all gates at t ≤ 32” statement literally true.**

   As written, it is false: G3, G4 monotonicity and required G5 controls reach t = 33. The scientific decisions themselves already use t ≤ 32.

   Apply these replacements:

   > §5.4 opening: “On the first 2^13 rows of each stratum, for all t ≤ 32 unless stated.”

   > §5.5 G4.6: “Monotonicity: I_{t+1} − I_t ≥ −4·SE of the paired step difference, with the stated arithmetic allowance, for t = 1..31.”

   > §5.8 required controls: “All history-dependent required-control checks use t ≤ 32.”

   > §6.1 full-history filtering: “Run BayesFilter on tokens[:, :32] for all gated calculations. The 33rd sampled symbol remains the next-symbol target. Any posterior calculation that conditions on w_33 is descriptive and cannot alter validity, D, PH labels or the scientific outcome.”

   Add to §5.0:

   > Every history-dependent X2a validity or scientific decision uses at most w_1..w_32. The long-horizon checks are descriptive only. Existing regression-suite tests retain their own interface coverage.

7. **Disclose P-ref’s actual seed source.**

   `draw_axis_permutation(spec)` internally uses `SeedTree(0)`, not `SeedTree(20261015)`. Its issuance is not captured by the main tree’s `.issued`.

   Replace the “Seeds come only…” invariant in §8.2 with:

   > Sampling and surrogate seeds come from SeedTree(20261015). P-ref’s unchanged helper separately uses SeedTree(0).generator("axis_permutation", "_x2a_torus_local"). The report records both seed sources and the resulting sx, sy and state_perm arrays.

   Add this row to §6.2:

   > Master 0; stream ("axis_permutation", "_x2a_torus_local"); P-ref axis permutations; unchanged helper, recorded separately from the main tree’s issued map.

8. **Fix the Decimal selection and specify prefix/log arithmetic.**

   The present “24 histories” rule can select fewer than 24 distinct histories because the extreme rows can overlap the first eight.

   Replace G3.6’s selection sentence with:

   > Select exactly 12 distinct histories per stratum: rows 0..7, followed by the four largest-|LLR_32| rows among indices 8..8191. Break equal-|LLR| ties by smaller row index. Use all 24 selected histories for the 80-digit Decimal comparison.

   Add to §5.4:

   > BayesFilter.log_evidence is terminal evidence, not an evidence curve. For prefix t, obtain log P_c(w_1..w_t) as −cumsum(result_c.ce, axis=1)[:, t−1]; terminal log_evidence may be used at the terminal prefix.

   Add to §4.2:

   > Compute log-odds from separately accumulated positive component masses or component log-evidences, not by subtracting a rounded posterior from one. Evaluate entropy with 0·ln 0 := 0 and evaluate additive log-probabilities using stable log-expit/logaddexp formulas. Do not add epsilon or clip probabilities to manufacture finite log-odds.

   The existing Decimal conversion of the float64 model is otherwise correct.

9. **Repair the PH outcome logic and endpoint convention.**

   `Q2-win fails` does not imply that windows separate the two components. It can mean fragmentation, no retained cluster, or an impure split.

   Replace the Q2 outcome rules in §7.5 with:

   > Let FULL_SPLIT mean that Q2-full has exactly two retained clusters with the stated opposite-label purity in at least 7/8 panels. Let WIN_CONNECTED mean that Q2-win has exactly one retained cluster in at least 7/8 panels. Let WIN_SPLIT mean that Q2-win satisfies the same two-cluster and purity criterion as FULL_SPLIT in at least 7/8 panels.
   >
   > Subject to PH validity:  
   > SEPARATED_FULL_ONLY iff FULL_SPLIT and WIN_CONNECTED;  
   > SEPARATED_BOTH iff FULL_SPLIT and WIN_SPLIT;  
   > WINDOW_UNRESOLVED iff FULL_SPLIT and neither WIN_CONNECTED nor WIN_SPLIT;  
   > NOT_SEPARATED iff FULL_SPLIT fails.  
   > INVALID takes precedence when calibration or a required PH item is invalid.

   Add `WINDOW_UNRESOLVED` to §5.9 and the verdict tests. Replace its reading-rule text with:

   > Full-history beliefs satisfy the retained-cluster split criterion, but the window comparison is unresolved.

   Add:

   > Report the fraction of original points retained by the 26-point filter. Separation statements concern the retained clusters and do not imply that every sampled point belongs to them.

   Replace the H1 spanning definition in §7.2 with:

   > β̂¹(B) := #{H1 bars with birth ≤ inf B and death > sup B}.

   This matches the repository’s `birth ≤ r < death` convention for a closed band.

10. **Correct the timeout contract while preserving PH isolation.**

    The existing `PersistenceComputer` executes these ≤600-point, maxdim≤1 calls directly. That path does not enforce `timeout_s`.

    Add to §7.2:

    > These calls use the existing in-process path. Its timeout_s setting does not enforce a per-call wall-clock timeout. No enforced 600-second timeout is claimed.

    Replace S8 with:

    > A PH call returns CENSORED or raises: mark the affected PH item INVALID. Catch the failure within the PH stage and continue required G5 validity evaluation. PH failure does not change D or the overall validity verdict. Owner STOP and environment interruption retain their separate S7 semantics.

    This needs no production change or additional runner.

11. **Remove the general necessity claim about holonomy.**

    Replace Remark H’s third bullet with:

    > Locally invisible holonomy is one possible route to matching short-window laws while preserving a longer-history distinction; it is not established here as necessary for every HMM construction. If two processes admit emission-preserving Markov projections to the same quotient with the same projected initial law and transition kernel, their complete observation laws coincide. Any proposed quotient/holonomy construction must therefore verify its own projected dynamics, matching window laws and distinguishing witness.

12. **Correct the small numerical illustrations and series remainder.**

    Replace §2.3’s summed-image illustration with:

    > The omitted next image at per-axis distance 5.5 contributes a relative factor exp(−3.84) = 0.0214936 before renormalisation. The normalised one-dimensional probabilities differ by approximately 8.5773e-7. For example, at state (0,0) and centre (6.5,0.5), the two-dimensional emission entries differ by approximately 5.0538e-7.

    Replace test 1’s negative example with:

    > Verify that minimum-image and summed-image two-dimensional fields differ by more than 1e-7 at state (0,0), centre (6.5,0.5).

    Replace the small-r remainder claim in §4.1 with:

    > With terms through r^8, the remainder satisfies  
    > 0 ≤ R_4(r) ≤ r^10/[90(1−r²)] < 1.12e-32 for |r| < 1e-3.  
    > Define φ(±1) = ln 2 explicitly for toy laws and numerical endpoints.

    Replace the scalar-Kalman forecast clause in §7.3 with:

    > For the isotropic A displacement approximation, the scalar steady-state posterior SD is approximately 0.7845 lattice units. This is not a calculation of the exact nonlinear filter’s covariance or of both components’ anisotropic uncertainty.

**Independent re-derivations**

I verified the requested document SHA256, `3EC464481C7EC464D62EDBA8A71D95E410161F269D60B85FDBFCD348A5C3A38F`, and the stated request hash. I read the planning protocol, binding policy, charter, merged decisions and analysis, relevant source-track material, and source code. Main was `ecae1104a11487e18dd7e06ca3ba79962138ad6c`; the specified diff from `c364f95` over `src`, `tools/x4_oracle_profile` and `tests/oracle_profile` was empty. The accepted-history checkout was at `c2046fc`; its BayesFilter file matched main.

No files or git state were written. No Python, tests, sampling, training, checkpoints or scientific payloads were run or opened. Numerical checks below used calculator arithmetic on the displayed finite-sum formulas.

**Construction, Lemma U and T1–T7**

Let \(u\) be uniform on the 144 lattice states and let \(\alpha=1/5\).

- **Construction.** The graph has 144 vertices, 288 edges and 144 squares. Its degree is four, Euler characteristic zero, and torus Betti numbers are \((1,2,1)\). The symmetric lazy kernel preserves \(u\). Two identical transition blocks with uniform mixture start preserve the equal component prior.

  The minimum-image squared distance separates by coordinate, so the two-dimensional softmax factorises into \(e[x,a]e[y,b]\). The twist has determinant one, preserves the lattice, and has operator norm \((1+\sqrt5)/2\). It sends a vertical unit edge to a diagonal, so it is not a grid isometry.

  It is also not an **axis-wise** permutation of the original P form: its first emission coordinate depends on both \(x\) and \(y\). “Row permutation” alone must not be confused with that particular P-world construction.

- **Lemma U.** Under \(u=\phi z\), a displacement \(\delta\) becomes \(\phi\delta\). Thus A’s moves are \(0,\pm(1,0),\pm(0,1)\), while B’s emission-coordinate moves are \(0,\pm(1,0),\pm(1,1)\), each with probability \(1/5\). The transformed start remains uniform and B emits through \(E_A[u]\). Correct.

- **T1.** The identity \(e[x+2,a+1]=e[x,a]\) makes all six column sums equal. Their sum is 12, hence each is two. Every \(E_A\) column consequently sums to four. A row permutation preserves these sums, giving
  \[
  P(W_t=j\mid c)=4/144=1/36.
  \]
  Therefore \(I_1=0\) and one-symbol component accuracy is exactly \(1/2\).

- **T2.** Write \(G_d=\sum_x e[x,0]e[x+d,0]\). Summing over symbols and states factorises, with a factor \(36/144=1/4\). Therefore
  \[
  P_A(\mathrm{rep})=\tfrac14(\alpha G_0^2+4\alpha G_0G_1),
  \]
  \[
  P_B(\mathrm{rep})=\tfrac14(\alpha G_0^2+2\alpha G_0G_1+2\alpha G_1^2).
  \]
  Their difference is
  \[
  \tfrac{\alpha}{2}G_1(G_0-G_1)>0.
  \]
  Positivity follows from positive emissions and strict Cauchy–Schwarz for the nonconstant column and its cyclic shift. Repeat events survive symbol renaming, so the witness also excludes equality of sequence laws after any symbol permutation. Correct.

- **T3 and Lemma R.** Conditional stationarity makes every length-k window have law \(P_c^{(k)}\), regardless of position. With equal component priors, its information is JS divergence. Marginalising earlier observations gives the stationary mixture law at the window boundary, so restarting the filter there is exact. Consequently,
  \[
  I(C;W_{1:t-k}\mid W_{t-k+1:t})=I_t-I_k.
  \]
  Correct.

- **T4.** Information and Bayes accuracy are nondecreasing under additional observations. For each component, the hidden-state/output pair chain is finite, irreducible and aperiodic. The repeat-frequency limits differ by T2; the ergodic theorem therefore supplies disjoint full-measure output events identifying the component. Posterior martingale convergence and bounded convergence give \(I_t\to\ln2\) and \(acc_t\to1\). Correct.

- **T5.** The stated conditional-independence requirement on any extra randomisation gives \(C\to W_{\rm window}\to f\). Data processing bounds information; composition with a classifier bounds accuracy by the window Bayes optimum. The contrapositive is valid for a properly evaluated later probe. Correct.

- **T6.** A grid automorphism preserves the uniform start and every transition probability. Relabelling the latent paths by that automorphism preserves their weights and converts the pulled-back emissions to A’s emissions. Summing paths proves identical observation laws. Correct.

- **T7.** Every emission entry is positive. For any finite string, even one fixed all-stay latent path has positive probability. Thus both component likelihoods are positive and the exact posterior lies strictly inside \((0,1)\). This is a real-arithmetic statement; rounded posteriors need the stable arithmetic specified above.

**Lemmas C, A and P; Proposition N**

For a decision \(d(H)\), conditioning correctness on the full history gives exactly its stated credit. The full-history Bayes credit dominates every alternative credit pointwise. A wrong decision loses \(|2\pi_{32}-1|\); a fair tie loses half that amount. Thus the credit differences lie in \([0,1]\). The tolerance-tie qualification in required change 4 is the only correction needed to identify this exactly with the previously defined Bayes \(acc_8\).

For Lemma A, equal priors give
\[
\operatorname{logit}\pi_\ell^{blk}
=\ln\frac{P_B(block_\ell)}{P_A(block_\ell)}.
\]
Summing proves the block-product formula. Stationarity gives its component-conditional expectation as four times the corresponding eight-symbol expectation. The independence “iff” needs the correction above.

For the information lower bound, let \(S=s_{\rm add}(H)\), \(q(S)=\operatorname{expit}S\), and \(m(S)=P(C=B\mid S)\). Then
\[
I_{\rm add}^{LB}
=I(C;S)-E\,KL(\mathrm{Bern}(m(S))\Vert\mathrm{Bern}(q(S)))
\le I(C;S)\le I_{32}.
\]
Conditioning instead on the full history gives
\[
I_{32}-I_{\rm add}^{LB}
=E\,KL(\mathrm{Bern}(\pi_{32})\Vert\mathrm{Bern}(q(S))).
\]
The proposed Rao–Blackwellised cross-entropy statistic is therefore correct. It may be negative.

For Proposition N,
\[
K=\tfrac34I+\tfrac18R_{+2}+\tfrac18R_{-2}
\]
is positive-preserving and doubly stochastic. Equivariance converts its state shifts into independent symbol-coordinate noise with probabilities \(3/4,1/8,1/8\). Its Fourier multipliers are
\[
\kappa_m=\tfrac34+\tfrac14\cos(4\pi m/12).
\]
They contract at least one nonzero mode of each relevant emission column, strictly reducing the Frobenius norm and excluding a row permutation.

The x-coordinate walk has multiplier
\[
\lambda_m=0.6+0.4\cos(2\pi m/12)>0.
\]
Since K and L commute,
\[
S_A-S_N
=\frac1{144}\sum_m|\hat g_m|^2\lambda_m(1-\kappa_m^2)>0.
\]
The stated proof is correct.

For Lemma P, disjoint probability supports have Bhattacharyya coefficient zero and Hellinger distance one. Below scale one, no cross-component simplex exists, so the Rips complexes are disjoint and their Betti numbers add. Correct.

**Independent arithmetic for the [W] values**

The emission normaliser is
\[
Z=1.5666413125106897.
\]

| d | Unnormalised weight | p(d) |
|---|---:|---:|
| 0.5 | 0.9231163464 | 0.5892327357 |
| 1.5 | 0.4867522560 | 0.3106979575 |
| 2.5 | 0.1353352832 | 0.0863856214 |
| 3.5 | 0.0198410947 | 0.0126647335 |
| 4.5 | 0.0015338107 | 0.0009790439 |
| 5.5 | 0.0000625215 | 0.0000399080 |

The minimum two-dimensional entry is \(1.592647561\times10^{-9}\). The displayed reading second moment is \(1.5624645639\). These agree with the plan’s rounding.

| Quantity | Independently obtained |
|---|---:|
| G(0) | 0.9027045375 |
| G(1) | 0.7692346841 |
| G(2) | 0.4759893403 |
| G(3) | 0.2138778822 |
| G(4) | 0.0698148851 |
| G(5) | 0.0168874337 |
| G(6) | 0.0056870117 |
| A repeat probability | 0.1796221021 |
| B repeat probability | 0.1693551380 |
| Twist repeat gap | 0.0102669641 |
| Repeat-indicator JS, nats | 0.0000914863 |
| Repeat-indicator JS, bits | 0.0001319869 |
| \(\|Kg\|^2\) | 0.7166585369 |
| \(S_A\) | 0.0707763830 |
| \(S_N\) | 0.0573220071 |
| \(S_A-S_N\) | 0.0134543759 |
| N-local repeat probability | 0.1456692768 |
| N-local repeat gap | 0.0339528253 |
| N-local/twist repeat-gap ratio | 3.3069976 |

The float transition entries stated in §2.2 are correct. With unit roundoff \(u=2^{-53}\), \(287u\approx3.19\times10^{-14}\); that is a conservative dot-product error scale, not a proof of the accumulated filter error. The loosened N-iso/N-swap and row-sum tolerances are reasonable before data, with G3 and Decimal validation retained.

The Gaussian displacement covariance calculations also check:

- A: \(0.4I\).
- Twist B: \(\left[\begin{smallmatrix}0.8&0.4\\0.4&0.4\end{smallmatrix}\right]\).
- Both determinants: 0.16.
- Gaussian KL: 0.5 nats in either direction.
- Stronger twist \(s=2\): covariance \(\left[\begin{smallmatrix}2&0.8\\0.8&0.4\end{smallmatrix}\right]\), determinant 0.16, Gaussian KL 2 nats in either direction.

Those KL values concern the **Gaussian displacement approximation**, not the actual observed-symbol process or its discrete step-law KL.

For Gaussian reference distributions,
\[
H_\rho(d)=\sqrt{1-\exp[-d^2/(8\rho^2)]}.
\]

| ρ | \(H_\rho(\sqrt2)\) | \(H_\rho(4)\) |
|---|---:|---:|
| 0.75 | 0.599016 | 0.985614 |
| 1.00 | 0.470318 | 0.929873 |
| 1.25 | 0.384521 | 0.849684 |

The approximate common interval is therefore \([0.599016,0.849684)\), with central half approximately \([0.661683,0.787017]\). The scalar Riccati calculation gives variance approximately 0.615467 and SD 0.784517. These verify the forecast arithmetic, not the exact discrete-kernel diagrams.

For C-world, the two long H1 intervals are \([1,4)\). Below 4, projection onto either coordinate cycle preserves the corresponding generator. At 4, the row or column triangle with coordinates 0,4,8 kills it. Square-cycle bars occupy \([1,\sqrt2)\), persistence approximately 0.414214. Thus the absolute persistence threshold 1.0 correctly isolates the two torus generators.

The normal-tail arithmetic \(50\times6.334\times10^{-5}\approx0.00317\) was numerically correct; the finite-sample “at most” interpretation was not. With the corrected horizon there are 49 comparisons.

For 4,096 independent test histories, a binomial accuracy SE is 0.00625 at accuracy 0.8 and at most 0.0078125. A 0.06 improvement is 9.6 such SEs at 0.8, or 7.68 at the worst-case variance. The plan’s “about 8.6” uses an assumed SE near 0.007; it is a forecast illustration, not a guaranteed power calculation.

The operation-count illustrations check:

- Main dense transition products: approximately \(2.8701\times10^{12}\) MAC.
- Stated 39 window/block steps: approximately \(3.3920\times10^{12}\) MAC.
- Long-horizon 368 steps: approximately \(2.0004\times10^{12}\) MAC, before the extra eight-symbol window.
- One retained batch belief array: 155,713,536 bytes, approximately 156 MB.

These do not validate a wall-clock or peak-memory guarantee. The 30–45 CPU-minute figure remains an unbenchmarked forecast.

**The four §10.2 corrections specifically requested**

- **JS factor:** with \(M=(P_A+P_B)/2\) and \(r=(P_A-P_B)/(P_A+P_B)\),
  \[
  JS=\sum_h\frac{P_A+P_B}{4}
  [(1+r)\ln(1+r)+(1-r)\ln(1-r)].
  \]
  The original coefficient doubled JS. The corrected formula gives ln 2 for disjoint point masses. Its series coefficients are \(r^2/2+r^4/12+r^6/30+r^8/56+\cdots\), subject to the corrected remainder above.

- **acc_add:** its correct estimand is classification accuracy, estimated by credit. Taking the maximum of a pseudo-posterior and its complement estimates confidence, not accuracy.

- **I_add^LB:** the cross-entropy lower bound and its Rao–Blackwellisation are correct, as derived above. Entropy of an uncalibrated pseudo-posterior is not mutual information.

- **Full stratified Hoeffding bound:** all rows are independent and equally weighted despite differing stratum laws. Therefore
  \[
  P(|\hat\mu-\mu|\ge\epsilon)
  \le2\exp(-2n\epsilon^2/R^2),
  \qquad n=2^{20}.
  \]
  Using the full n is valid. At δ = 1e-6, the unit-range half-width is 0.002630260; multiplying by ln 2 gives 0.001823157 nats. The per-stratum information bound is approximately 0.0025783 nats and is conservative for the pooled estimate. These are per-quantity bounds, not simultaneous coverage statements for every reported curve.

**Gates, Monte Carlo and reference validation**

P3 and P4 are substantive feasibility requirements. P4 is stronger than merely demanding positive information beyond eight symbols: it requires at least half the full information to come from conditioning on older history. Its separate-bound implementation is conservative and acceptable. A3 is attainable as a comparator advantage but needs the narrower interpretation above.

The thresholds are mutually compatible with information and accuracy bounds. Full support prevents perfect finite-history discrimination, but does not prevent these margins. The theorems do **not** establish that this particular construction passes them at t = 32; the run must decide that.

The boundary operators are consistent: P3 and A3 include equality at their lower-bound thresholds; P4 includes equality in its PASS inequality; strict opposite inequalities define FAIL. Straddling is not PASS. The ADDITIVE fallback must not be read as an equivalence conclusion.

Exact component stratification, equal weights, independent trajectory units and paired comparisons are correct. The SE formula
\[
SE^2=\tfrac14(s_A^2/n_A+s_B^2/n_B)
\]
is appropriate. Prefix/window validation, label-based information, the increment identity and credit/max comparisons provide useful checks with different failure sensitivities. There is no justification for reseeding or increasing n after a failure.

The control sizes and the 80-digit Decimal precision are reasonable. I approve the 24-history selection after making it distinct and deterministic. This selection probes numerical error; it does not establish universal error bounds over all histories.

After required change 6, all history-dependent gates use t ≤ 32. The t ≤ 128 curve remains descriptive.

**Code reuse and PH**

BayesFilter has no irreducibility requirement and accepts the 288-state block-diagonal process. Its state, predictive and timing conventions match the plan. `suffix_posterior` also has no fixed-state-count or 33-symbol restriction; its scaled emit-first recursion matches the intended stationary restart. `HMMSampler` reads `layout.n_obs`, so the proposed long histories are supported without replacing the sampler.

The explicit doubly periodic emission is necessary: `point_distances` wraps only axis zero. The local unregistered builder, explicit arrays, existing topology stack and independent Decimal reference are appropriate reuse choices. Three module files, each ≤400 lines, are reasonable; they are an implementation constraint, not evidence that the whole scope will fit without escalation.

The PH design correctly keeps PH outside GO_P1. Demoting C-emis to descriptive is justified because its probability coordinates differ from the calibrated belief coordinates. The minimum-image reference kernel is consistent with the construction, and the C-world absolute rule is defensible. K1 still has to succeed on the actual reference diagrams; its forecast is not a substitute.

PH counts remain estimator-and-band statements. Neither a count of two nor P-ref specificity proves that the entire belief cloud is a torus. The corrected Q2 logic, retained-point disclosure and timeout wording are needed to keep its reading rule within that licence.

**Optional suggestions**

- Record the review snapshot as main @ecae110 while retaining c364f95 explicitly as the kernel-compatibility base; the checked kernel diff is empty.
- Report the three block-boundary locations beside A3 so readers can see what the comparator omits.
- In a later, separately frozen study, overlapping-window or shifted-block comparators could test whether A3’s advantage survives richer local evidence. Do not add them adaptively to this run.
- Keep the exposure record in the existing seed/artifact registry if one is already authoritative; a new registry is unnecessary.