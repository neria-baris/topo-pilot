STATUS: FREEZE_READY

The replacement below provides a complete certificate procedure and its proofs. It is ready for independent review; it does not authorize freeze or execution.

The recommended route is a small, ordered float64 reference alongside the existing oracle. A projective error analysis gives componentwise relative bounds that grow linearly over the 32 filtering steps. Comparing every operational predictive with this reference removes any accuracy assumption about the operational BLAS implementation. Tiny probabilities do not introduce an inverse-minimum-probability penalty.

Post-logit certification uses a proved exponential approximation and validated scalar logarithms. Outward intervals then cover construction of A, G, Y, Z, and each control-frame mean. A specified balanced-tree mean kernel supplies the bootstrap arithmetic bound. Signed numerical guards apply separately to headroom, V3, and the endpoint.

For ordinary logit ranges and operational discrepancies, the projected row bounds are below approximately \(5\times10^{-10}\) nat; the additional \(10^{-9}\) floor therefore usually dominates. This is six to seven orders below the \(0.001\)–\(0.01\) nat scientific margin. These are conditional forecasts, not measurements.

Both source worktrees resolve to `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`. The merged protocol SHA256 matches `F9F679DC…1257E12F6`. This planning turn used source, document, and metadata reads only.

# Replacement §15.3

### 15.3 Numerical certificate

**Status: proved certificate procedure; independent review required before freeze.**

This section certifies every eligible row used by the headroom, positive-control, precision-mean, and endpoint calculations. Four-row Decimal comparisons remain implementation checks. They do not establish an all-row bound.

The constants \(\eta=10^{-12}\) and \(2^{-44}\) are withdrawn. Neither is used by this certificate.

#### 15.3.1 Exact targets and coverage

For each bound, stored binary64 inputs are interpreted as exact real numbers.

1. The oracle posterior is the exact normalized likelihood calculation using the stored \(T,E,\pi\), with emission before the first transition.
2. The predictive target is exactly
   \[
   q^\pm=b_{32}(H^\pm)\,T\,E.
   \]
   This matches `BayesFilter.q[:,32]` and `FutureOperator.F1`. No predictive renormalization, clipping, or flooring is introduced.
3. The model target is the mathematical log-softmax of each recorded float64 logit vector \(l\):
   \[
   \ell_v(l)=l_v-\log\sum_w e^{l_w}.
   \]
   Recorded logits define the operational model output. This certificate does not approximate an exact-real Transformer forward pass.
4. \(A,G,Y,Z\) are the exact expressions in §§11–12 evaluated from those targets, with coefficients \(1/2\), \(1/32\), \(c=1/10\), and \(c_{\mathrm{full}}=3/10\) interpreted exactly.
5. Each bootstrap target is the exact arithmetic mean of those exact row statistics at the actual resampled indices. Bootstrap randomness and statistical coverage are outside the numerical certificate.

Stored stochastic rows need not sum to one exactly. Consequently, \(b_{32}\) is exactly normalized, whereas the literal stored-weight predictive \(b_{32}TE\) may have a small mass defect. This certificate covers that literal predictive, as specified in §3.3. Any comparison with an ideal stochastic process is separate.

Coverage includes:

- both donor histories on every eligible row;
- every distinct bound process \(T,E,\pi\);
- both arms of every primary pair, all 32 control pairs, and the full-donor pair;
- all three models;
- every row statistic and every bootstrap mean used by the declared numerical guards.

Sharing is permitted only when the relevant process arrays and canonical history bytes are **exactly identical**, with their identities bound by hashes. Approximate equality or the \(10^{-12}\) cross-model check is insufficient for sharing.

#### 15.3.2 Arithmetic assumptions and outward evaluation

The certificate uses the following explicit assumptions.

**Certificate binary64 kernels.** Basic addition, subtraction, multiplication, and division obey IEEE binary64 round-to-nearest, ties-to-even, with gradual underflow. Set
\[
u=2^{-53},\qquad a=2^{-1074},\qquad
\gamma_k=\frac{ku}{1-ku}.
\]
The conservative general operation bound is
\[
|\operatorname{fl}(x\circ y)-(x\circ y)|
\le u|x\circ y|+a.
\]
When the exact result is normal, the usual relative bound applies.

Certificate reductions are explicit, ordered sequences of binary64 additions and multiplications. They do not call BLAS, `einsum`, or an opaque dot-product reduction. Multiplication and addition are separate operations. SIMD execution across independent rows is permitted; reduced precision and fast-math transformations are not.

The runtime identity records the numerical environment and verifies the certificate kernels’ rounding and subnormal prerequisites before data calculations. Such checks support the stated arithmetic assumptions; they do not prove arbitrary library accuracy.

**Operational kernels.** No accuracy assumption is made about the operational oracle BLAS, operational log-softmax, or operational construction of \(A/G/Y/Z\). Their finite recorded results are compared against validated target intervals. Their rounding, reduction order, FMA use, and underflow effects are included in the observed discrepancies.

**Decimal kernels.** `Decimal(float)` is an exact conversion. Decimal basic arithmetic obeys its specified context rounding. Decimal `ln` and `exp` are correctly rounded under `ROUND_HALF_EVEN`, as documented by Python. The implementation and libmpdec versions are pinned. [Python Decimal documentation](https://docs.python.org/3/library/decimal.html)

Use K4’s `trapping_context` settings: explicit precision, exponent limits, clamp setting, and traps. Correctly rounded transcendental results are enclosed by their adjacent representable Decimal neighbors; setting a directed context alone is not treated as directed rounding of `ln` or `exp`.

**Outward bounds.**

- Constants and proofs use exact rationals.
- Precomputed bound constants are evaluated with directed Decimal arithmetic at 80 digits.
- Binary interval operations round each lower endpoint downward and each upper endpoint upward, using correctly rounded operations followed by the appropriate `nextafter`.
- Multiplication considers all endpoint products.
- Division is allowed only when the denominator interval excludes zero.
- Decimal-to-binary endpoint conversion is rounded outward and checked.
- Final error bounds are rounded upward. Threshold comparisons use exact rationals or directed Decimal arithmetic.
- No unexplained safety multiplier is added.

For a positive interval \(Q=[q_L,q_U]\), logarithm enclosure means
\[
\log Q=
[\operatorname{ln}_{\downarrow}(q_L),
 \operatorname{ln}_{\uparrow}(q_U)].
\]
A nonpositive binary lower endpoint triggers the Decimal fallback; it never becomes a clipped probability.

#### 15.3.3 Ordered oracle reference

The scientific oracle remains unchanged. A certificate-only reference computes the same stored-weight target.

For each donor history, the reference performs:

1. \(a_1=\pi\);
2. \(u_t(s)=\operatorname{fl}(a_t(s)E_{s,w_t})\);
3. an ordered sum \(D_t=\operatorname{fl}(\sum_s u_t(s))\);
4. \(b_t^{\rm ref}(s)=\operatorname{fl}(u_t(s)/D_t)\);
5. for \(t<32\), ordered nonnegative dots forming \(a_{t+1}=b_t^{\rm ref}T\).

It also computes an ordered reference \(TE\), then an ordered \(b_{32}^{\rm ref}(TE)^{\rm ref}\).

Exact zero transition entries may be omitted. Let \(d\) be the maximum number of nonzero entries in any row or column of \(T\), checked from the bound stored array. The documented walk has \(d\le5\). A different support uses its actual \(d\), up to \(N=144\); it is never silently approximated.

For a nonnegative dot with at most \(m\) terms, the reference uses the conservative relative envelope
\[
g_m=\gamma_{2m}.
\]
This counts a multiplication and an addition per term, including summation from zero. Positivity makes the relative envelope componentwise, independent of cancellation.

The fast reference requires all relevant positive operands and intermediate results to remain normal and finite. It checks them throughout. An output at least twice the smallest normal value is sufficient to rule out a borderline normal/subnormal rounding ambiguity. Failed fast-path range conditions invoke §15.3.5.

##### Proof: linear growth through normalization

Let \(b_t\) be the exact posterior and consider the ratios
\[
r_t(s)=b_t^{\rm ref}(s)/b_t(s)
\]
on their positive support. Define their projective spread
\[
R_t=\frac{\max_s r_t(s)}{\min_s r_t(s)}.
\]

An exact nonnegative transition maps each output ratio to a weighted average of its input ratios. It therefore cannot increase their spread. Transition-dot rounding enlarges the spread by at most
\[
\frac{1+g_d}{1-g_d}.
\]

Emission multiplication and componentwise division contribute at most two further factors
\[
\frac{1+u}{1-u}.
\]
The computed normalizer is common to every state and cancels from the projective spread. Thus, for \(L\) observations,
\[
R_L\le K_L:=
\left(\frac{1+u}{1-u}\right)^{2L}
\left(\frac{1+g_d}{1-g_d}\right)^{L-1}.
\]

This is the essential distinction from repeatedly applying an absolute posterior-error bound: previous error is not doubled at every normalization.

For the final reference posterior, let \(M=\sum_s b_L^{\rm ref}(s)\), with the sum understood exactly. The final ordered normalizer and divisions give
\[
M_L:=\frac{1-u}{1+\gamma_N}
\le M\le
M_U:=\frac{1+u}{1-\gamma_N}.
\]

Since \(\sum_s b_L(s)=1\), \(M\) is a weighted average of the ratios \(r_L(s)\). Combining this fact with their spread gives
\[
L_b:=M_L/K_L
\le\frac{b_L^{\rm ref}(s)}{b_L(s)}
\le M_UK_L=:U_b.
\]

The reference \(TE\) dots contribute \(g_d\); the final predictive dots contribute \(g_N=\gamma_{2N}\). Therefore
\[
L_q:=L_b(1-g_d)(1-g_N),
\qquad
U_q:=U_b(1+g_d)(1+g_N)
\]
satisfy, componentwise,
\[
L_q\le\frac{q_v^{\rm ref}}{q_v}\le U_q.
\]

Hence the validated predictive enclosure is
\[
\boxed{
q_v\in Q_v:=
\left[\frac{q_v^{\rm ref}}{U_q},
      \frac{q_v^{\rm ref}}{L_q}\right].
}
\]

All displayed constants are evaluated outward. The proof follows the deterministic \(\gamma_k\) arithmetic model; no probabilistic rounding hypothesis is used.

For \(L=32,N=144,d\le5\), the first-order size of the resulting reference relative error is approximately \(1.4\times10^{-13}\). With dense \(d=144\), it remains of order \(10^{-12}\).

##### Operational predictive and logarithm errors

For each actual operational predictive \(\widehat q_v\), record
\[
e^q_v=
\max\{|\widehat q_v-q_{L,v}|,
       |\widehat q_v-q_{U,v}|\}.
\]

A relative error bound is
\[
\rho_v=
\max\left\{
\left|\frac{\widehat q_v}{q_{L,v}}-1\right|,
\left|\frac{\widehat q_v}{q_{U,v}}-1\right|
\right\}.
\]

For its actual recorded oracle logarithm \(\widehat h_v\), record
\[
e^h_v=
\max\{|\widehat h_v-h_{L,v}|,
       |\widehat h_v-h_{U,v}|\},
\qquad
[h_{L,v},h_{U,v}]=\log Q_v.
\]

These are valid all-row bounds regardless of the operational BLAS or logarithm implementation.

Because \(Q_v\) has a relative width, its logarithmic width is
\[
\log(U_q/L_q),
\]
independent of how small \(q_v\) is. The certificate contains no term proportional to \(1/\min(q)\).

#### 15.3.4 Validated post-logit evaluation

For each recorded logit vector, let
\[
m=\max_v l_v,\qquad x_v=l_v-m\le0.
\]
The maximum is selected from the recorded values and is exact. Enclose each exact subtraction \(x_v\) outward.

Compute validated intervals \(E_v\ni e^{x_v}\), then
\[
S=\sum_v E_v,\qquad
\mathcal L_v=X_v-\log S,
\]
using outward arithmetic. One maximum component has exponential exactly one, so the lower bound on \(S\) is positive.

The ordinary path uses the following source-controlled exponential reference, avoiding any accuracy assumption about `np.exp` or Torch.

##### Proved exponential reference

For a binary64 argument \(\widehat x\in[-128,0]\), put \(z=-\widehat x\). Choose the smallest integer \(k\ge0\) for which
\[
y=z\,2^{-k}\le1/8.
\]
Select \(k\) by exact power-of-two comparisons, without logarithms.

For the ordinary polynomial path, \(z>2^{-40}\). Form
\[
P_{12}(y)=\sum_{r=0}^{12}\frac{y^r}{r!}
\]
by the recurrence
\[
t_0=1,\qquad
t_r=\operatorname{fl}\!\left(
\operatorname{fl}(t_{r-1}y)/r\right),
\]
and ordered addition of its positive terms.

A conservative path count gives
\[
|\widehat P/P_{12}-1|\le h:=\gamma_{37}.
\]

Taylor’s theorem gives
\[
0\le e^y-P_{12}(y)
\le \tau:=\frac{2}{8^{13}13!}.
\]
Here \(e^{1/8}<2\), and \(P_{12}\ge1\). Consequently,
\[
\frac{1-h}{1+\tau}
\le\frac{\widehat P}{e^y}\le1+h.
\]

Set \(\widehat e_0=\operatorname{fl}(1/\widehat P)\), followed by \(k\) separately rounded squarings. Then
\[
L_{e,0}=\frac{1-u}{1+h},
\qquad
U_{e,0}=\frac{(1+u)(1+\tau)}{1-h},
\]
and
\[
L_{e,k}=L_{e,0}^{\,2^k}(1-u)^{2^k-1},
\qquad
U_{e,k}=U_{e,0}^{\,2^k}(1+u)^{2^k-1}
\]
satisfy
\[
L_{e,k}\le
\frac{\widehat e_k}{e^{\widehat x}}
\le U_{e,k}.
\]

The permitted range has \(k\le10\), and its ordinary-path intermediates remain normal. They are nevertheless checked.

If \(x\in[\widehat x-\xi,\widehat x+\xi]\), with \(\xi<1\), then
\[
1-\xi\le e^{x-\widehat x}\le\frac1{1-\xi}.
\]
Thus
\[
e^x\in
\left[
\frac{\widehat e_k(1-\xi)}{U_{e,k}},
\frac{\widehat e_k}{L_{e,k}(1-\xi)}
\right],
\]
evaluated outward.

**Small arguments.** For \(0\le z\le2^{-40}\), use the elementary enclosure
\[
1-z\le e^{-z}\le1-z+z^2/2,
\]
with outward interval operations. This avoids tiny polynomial terms.

**Very negative arguments.** If the exact argument’s validated upper endpoint is at most \(-128\), use
\[
e^x\in[0,2^{-128}],
\]
since \(e>2\). This is an enclosure of a negligible contribution, not probability flooring. Boundary cases use the ordinary path or Decimal fallback.

**Exceptional ranges.** Overflow in a binary subtraction, an unmet range condition, or an unsuitable binary interval invokes a directed Decimal computation. Exact float inputs are retained. Very negative Decimal arguments may use the same proved negligible-contribution enclosure, so an unnecessary Decimal exponential underflow is avoided.

##### Logarithms and recorded log-softmax errors

For the positive scalar interval \(S\), evaluate its endpoint logarithms using 40-digit Decimal `ln`, expanded to adjacent Decimal neighbors. Convert the resulting endpoints outward if binary intervals are used.

This requires two scalar logarithms per arm; it does not require a Decimal exponential for every ordinary logit.

For every operational log-softmax component \(\widehat\ell_v\), define
\[
\boxed{
e^\ell_v=
\max\{|\widehat\ell_v-\mathcal L_{L,v}|,
       |\widehat\ell_v-\mathcal L_{U,v}|\}.
}
\]

This bounds post-logit evaluation for that exact recorded vector. Any operational elementary-function error, cancellation, or reduction error is inside the measured discrepancy.

The polynomial constants, cutoff proof, scalar logarithm enclosure, and range branches are frozen source-specific derivations. No universal \(2^{-44}\) claim is made.

#### 15.3.5 Oracle fallback

If the ordered binary reference cannot establish its normal-range prerequisites, certify that donor history using K4’s unchanged 60-digit unnormalized Decimal posterior reference inside the trapping context.

Let \(\beta\) be K4’s proved `posterior_envelope(32,N)`. It establishes
\[
(1-\beta)b_s\le b_s^{\rm dec}\le(1+\beta)b_s.
\]

Compute \(TE\) and the final prediction by ordered Decimal nonnegative dots. With Decimal unit roundoff
\[
u_{60}=\tfrac12\,10^{-59},
\qquad
\gamma^{(60)}_k=\frac{ku_{60}}{1-ku_{60}},
\]
their predictive ratio enclosure is
\[
L_q^{\rm dec}
=(1-\beta)
 (1-\gamma^{(60)}_{2d})
 (1-\gamma^{(60)}_{2N}),
\]
\[
U_q^{\rm dec}
=(1+\beta)
 (1+\gamma^{(60)}_{2d})
 (1+\gamma^{(60)}_{2N}).
\]

Use the same construction \(Q=[q^{\rm dec}/U_q^{\rm dec},q^{\rm dec}/L_q^{\rm dec}]\), retaining Decimal endpoints when binary conversion would destroy positivity.

K4’s path-exponent argument applies: a positive binary64 factor is at least \(2^{-1074}\), and a 32-observation path uses at most 64 factors. Its positive products are therefore far above the Decimal context’s lower exponent limit. C1 also checks the input upper bounds and traps.

This is an exceptional per-history fallback, not a requirement for dense all-row Decimal filtering.

#### 15.3.6 Construction of A, G, Y, Z and frame means

Let interval subtraction give
\[
D_v=Q_v^+-Q_v^-.
\]

For every primary, control, and full-donor pair \(X\), form
\[
\mathcal A(X)=
\frac12\sum_v
D_v\bigl(\mathcal L_{X^+,v}-\mathcal L_{X^-,v}\bigr).
\]

Each arm’s contribution can additionally be enclosed as
\[
\mathcal A_+(X)=\frac12\sum_vD_v\mathcal L_{X^+,v},
\qquad
\mathcal A_-(X)=-\frac12\sum_vD_v\mathcal L_{X^-,v}.
\]
The paired expression is used for the final pair certificate because it retains cancellation before interval multiplication.

Construct
\[
\mathcal G=
\frac12\sum_vD_v
\bigl(\log Q_v^+-\log Q_v^-\bigr),
\]
\[
\mathcal A_C=\frac1{32}\sum_{r=1}^{32}\mathcal A(C_r),
\]
\[
\mathcal Y=\mathcal A(T)-\mathcal A_C,
\qquad
\mathcal Z=\mathcal Y-\frac1{10}\mathcal G,
\]
and
\[
\mathcal Z_{\rm full}
=\mathcal A_{\rm full}-\frac3{10}\mathcal G.
\]

All sums, products, subtractions, and coefficient applications use outward intervals. The rational coefficients \(1/10\) and \(3/10\) are enclosed exactly; their binary64 approximations are not substituted for the target coefficients.

For an operational scalar \(\widehat F\) and its target interval
\(\mathcal F=[F_L,F_U]\), define
\[
b^F=
\operatorname{up}
\left(
\max\{|\widehat F-F_L|,|\widehat F-F_U|\}
\right).
\]

In particular, persist
\[
\boxed{
b^Z_{j,i}=
\operatorname{up}
\left(
\max\{|\widehat Z_{j,i}-Z_{L,j,i}|,
       |\widehat Z_{j,i}-Z_{U,j,i}|\}
\right).
}
\]

Persist corresponding bounds for \(G,A_T,A_{\rm full},A_{C_r},A_C,Y,Z_{\rm full}\). If a per-frame population mean is reported, it receives its own row-bound maximum and mean-arithmetic bound.

##### Proof of construction coverage

Each oracle interval contains its exact predictive component. Each oracle-log interval contains its exact logarithm, and every arm-log interval contains the mathematical log-softmax of its recorded logits.

Interval inclusion is preserved by subtraction, addition, multiplication, and division by a positive constant. Induction over the displayed expression therefore places each exact scalar inside its interval.

Comparison with the **actual recorded scalar** then bounds its complete numerical error. This includes:

- oracle and post-logit input errors;
- products of input errors;
- subtraction and signed cancellation;
- dot-product and summation rounding;
- the 32-frame mean arithmetic;
- final \(Y\) and \(Z\) arithmetic;
- binary representations of the decimal margin coefficients.

No separate arithmetic term is omitted: it is included in the actual-scalar-to-target-interval distance.

The interval construction uses relative predictive enclosures. Its oracle-log uncertainty therefore remains informative for tiny positive probabilities.

#### 15.3.7 Bootstrap-mean arithmetic

Use one source-controlled mean kernel for numerical decision means:

1. gather the recorded row values at the actual bootstrap indices;
2. add them in a fixed balanced binary tree, carrying an unmatched value unchanged;
3. divide the result once by the exactly represented integer draw size.

No opaque `np.mean` or BLAS reduction is used for these decision means. The bootstrap generator, row order, seeds, draw counts, and shared-index semantics remain unchanged.

Let
\[
d_n=\lceil\log_2 n\rceil,\qquad
M_F=\max_i|\widehat F_i|.
\]
The tree has depth at most \(d_n\). Provided no overflow occurs,
\[
\left|
\operatorname{mean}_{\rm tree}(\widehat F_{\mathrm{idx}})
-\frac1n\sum_{a=1}^n\widehat F_{\mathrm{idx}_a}
\right|
\le r^{\rm mean}(F),
\]
where
\[
\boxed{
r^{\rm mean}(F)=
\operatorname{up}\left[
\gamma_{d_n+1}M_F+
\left(
\frac{n-1}{n}(1+u)^{d_n+1}+1
\right)a
\right].
}
\]

For \(d_n\le32\), the additive term may conservatively be replaced by \(4a\).

##### Proof

Each input follows at most \(d_n\) rounded additions. The standard product-of-rounding-factors argument bounds the relative part of the sum error by
\(\gamma_{d_n}\sum_a|\widehat F_{\mathrm{idx}_a}|\).

There are \(n-1\) additions. Each additive underflow error is at most \(a\), and its remaining propagation multiplies it by at most \((1+u)^{d_n}\). The final division contributes one further relative rounding and one additive error at most \(a\). Divide the absolute-sum bound by \(n\) and use
\[
n^{-1}\sum_a|\widehat F_{\mathrm{idx}_a}|\le M_F.
\]
This gives the displayed bound. It remains valid under signed cancellation.

An overflowing tree invokes a validated Decimal mean fallback; a row is never removed to avoid certification.

For model \(j\), define
\[
r^{\rm mean}_j=r^{\rm mean}(Z_j),
\qquad
\boxed{
B_{{\rm num},j}=
\operatorname{up}
\left(\max_i b^Z_{j,i}+r^{\rm mean}_j\right).
}
\]

For each draw, averaging its row errors adds at most \(\max_i b^Z_{j,i}\). Thus every computed bootstrap mean is within \(B_{{\rm num},j}\) of its exact target.

The same formula is applied separately to \(G,Z_{\rm full}\), and reported per-frame means.

For centered precision means, the difference of two certified means receives the sum of their error bounds plus an outward bound for the final subtraction. This covers the mean arithmetic in the centered draws. It does not claim to certify the separate standard-deviation, normal-quantile, or power calculations in `precision_summary`.

##### Bootstrap quantiles

Use `inverted_cdf`, with ranks fixed by exact rational probabilities. For 5000 draws, the one-based ranks are:

- headroom \(1/20\): 250;
- lower \(1/60\): 84;
- upper \(59/60\): 4917.

Validate these ranks against the reused percentile helper. Quantile selection introduces no arithmetic averaging.

If two indexed sample vectors differ componentwise by at most \(B\), their same-rank order statistics differ by at most \(B\): componentwise ordering gives the result in both directions. Therefore the same \(B\) certifies the bootstrap lower and upper quantiles, even when perturbations change their ordering.

#### 15.3.8 Signed numerical guards

The floor
\[
f_{\rm num}=10^{-9}
\]
is an additional conservative guard. It is never evidence of accuracy.

**Headroom.** Let \(\widehat L_G\) be the prescribed lower bootstrap bound, and define
\[
B_G=\operatorname{up}
\left(\max_i b^G_i+r^{\rm mean}(G)\right),
\qquad
F_G=\max(B_G,f_{\rm num}).
\]
H5 passes only if
\[
\boxed{\widehat L_G-F_G>1/100.}
\]
Use the actual \(G\) array bound to H5. If a common array is justified by exact sharing, use the largest applicable process certificate.

**V3.** For each model,
\[
B_{{\rm full},j}=
\operatorname{up}
\left(\max_i b^{Z_{\rm full}}_{j,i}
+r^{\rm mean}(Z_{{\rm full},j})\right),
\quad
F_{{\rm full},j}=\max(B_{{\rm full},j},f_{\rm num}).
\]
V3 passes only if all three models satisfy
\[
\boxed{\widehat L_{{\rm full},j}-F_{{\rm full},j}>0.}
\]

**Endpoint.** Define
\[
F_j=\max(B_{{\rm num},j},f_{\rm num}).
\]
Certified signed endpoint bounds are
\[
L_j^{\rm cert}=\widehat L_j-F_j,
\qquad
U_j^{\rm cert}=\widehat U_j+F_j.
\]
A positive declaration requires \(L_j^{\rm cert}>0\); a negative declaration requires \(U_j^{\rm cert}<0\). Retain §13’s additional near-zero guard on both reported tails.

Perform these comparisons exactly or outward. Ordinary floating subtraction followed by an unguarded comparison is insufficient.

A finite certificate that does not separate a threshold is an INCONCLUSIVE outcome under the relevant gate. Nonfinite scientific inputs, inconsistent bindings, an invalid interval, or a certificate implementation defect are FAIL_TECHNICAL. Valid inputs requiring a fallback remain eligible; unavailable certification after resource exhaustion is INCONCLUSIVE/NUMERICAL.

#### 15.3.9 Magnitude and cost

These are planning estimates, not measurements or replacement acceptance thresholds.

For \(N=144,L=32,d\le5\):

- the fast oracle reference relative envelope is approximately \(1.4\times10^{-13}\);
- logarithm uncertainty from that envelope is of the same order, independently of tiny \(q_v\);
- the exponential reference at the widest ordinary range has relative uncertainty of order \(10^{-11}\) or smaller;
- balanced-tree mean error has size approximately \(16uM_F\) for a cohort of at most 32768 rows.

As an illustrative ordinary case, suppose operational-reference discrepancies are small, logit ranges are at most 128, and oracle log-ratios are of order \(10^2\) or less. Propagating these quantities gives row \(Z\) bounds of order \(10^{-10}\), conservatively below approximately \(5\times10^{-10}\) nat. The \(10^{-9}\) floor then dominates.

For \(G\) of order \(10^{-2}\)–\(10^{-1}\) nat,
\[
0.10G=10^{-3}\text{–}10^{-2}\ {\rm nat}.
\]
The ordinary numerical guard is therefore approximately \(10^6\)–\(10^7\) times smaller than the scientific margin. Numerical INCONCLUSIVE is expected near a threshold or after an abnormal numerical discrepancy, not merely because predictive probabilities are tiny.

For approximately 30000 rows:

- two donor references require approximately \(4\times10^9\) simple binary arithmetic operations for one shared process;
- three genuinely distinct processes multiply the oracle-reference work by three;
- three models with 32 control pairs, a primary pair, and a full-donor pair have at most 6.12 million arm vectors, or about 220 million logit components;
- the exponential reference requires approximately \(10^{10}\) simple vectorizable operations at that upper workload;
- normalizer certification needs approximately 12 million scalar Decimal logarithms, plus oracle-log certification;
- row intervals and bootstrap trees add work of comparable or smaller order.

Chunk the calculations. Retain only required certificates and bindings rather than every transient interval.

A reasonable unmeasured forecast is \(10^3\)–\(10^4\) CPU-seconds for the ordinary certificate workload, with substantial dependence on implementation and scalar-log cost. This is a proportionate hours-scale calculation, rather than mandatory dense 60-digit filtering on every row. CPU remains uncapped; existing thread, RAM, disk, ledger, and operation-guard requirements continue to apply.

Actual cost and fallback frequency are reported during authorized implementation. They do not change scientific thresholds or permit omission of rows.

#### 15.3.10 Binding, isolation, and verification

Certificate records bind:

- source and numerical-kernel versions;
- Python/libmpdec and numerical environment;
- process-array dtype, shape, and content hashes;
- canonical donor-history bytes and sequence IDs;
- model, arm, frame, and recorded-logit identities;
- coefficient values and interval rules;
- reference constants and fallback branch;
- row bounds, mean bounds, quantile ranks, and final guards.

Validation endpoint-bearing bounds and summaries follow the existing sealing rule. Fresh \(A/Y/Z\) intervals are constructed only after T-PRE passes. Oracle/headroom certificates and full-donor V3 certificates run at their already-authorized gates.

Before scientific execution, independent verification must cover:

1. exact-rational small-HMM filtering and prediction, including normalization;
2. the projective recurrence and constants;
3. both fast and Decimal oracle branches;
4. exponential polynomial, squaring, small-argument, cutoff, and Decimal branches;
5. logarithm endpoint expansion and outward conversions;
6. signed products, coefficient representations, and 32-frame averages;
7. cancellation and subnormal cases in mean arithmetic;
8. quantile ranks and order-statistic perturbation;
9. injected operational discrepancies, confirming that the reported bound contains them;
10. complete row/model/arm coverage and sealing order.

These checks validate the implementation of this proof. Selected scientific reference rows are not substituted for it.

# Exact linked edits

## §13, step 2

Replace step 2 with:

> **2. Numerical certificate.** Apply §15.3 to every eligible row, model, and required arm. Define
> \[
> B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j,\qquad
> F_j=\max(B_{{\rm num},j},10^{-9}),
> \]
> with outward evaluation. If certification is unavailable, or for any model
> \[
> |\widehat L_j|\le F_j
> \quad\text{or}\quad
> |\widehat U_j|\le F_j,
> \]
> the outcome is INCONCLUSIVE/NUMERICAL. Certified signed bounds are \(\widehat L_j-F_j\) and \(\widehat U_j+F_j\). A certificate implementation or binding defect is FAIL_TECHNICAL.

Replace step 3 with:

> **3. Per model:** PASS\(_j\) iff \(\widehat L_j-F_j>0\); FAIL\(_j\) iff \(\widehat U_j+F_j<0\); otherwise INC\(_j\). Equalities are INC\(_j\). Step 2 has precedence.

## §16

Add to the conventions:

> Numerical certificate coverage is every-row coverage. A fast-path range failure invokes the specified fallback and does not remove the row. A valid finite certificate that fails to separate a threshold is INCONCLUSIVE; invalid inputs, bindings, intervals, or certificate implementation are FAIL_TECHNICAL. Decision bootstrap means use the §15.3.7 balanced-tree kernel.

Apply these table edits:

| Row | Exact change |
|---|---|
| 3, H3 | Append: “Every eligible donor predictive has the §15.3 oracle and oracle-log enclosures, with process/history bindings. Selected Decimal comparisons remain implementation checks.” |
| 5, H5 | Replace the numerical criterion with “\(\widehat L_G-\max(B_G,10^{-9})>1/100\), using §15.3.8; seed and bootstrap semantics unchanged.” |
| 18, V3 | Replace “all three LB(Z_full) > 0” with “all three \(\widehat L_{{\rm full},j}-\max(B_{{\rm full},j},10^{-9})>0\).” |
| 19, P1 | Append: “Row construction and raw/centered bootstrap-mean arithmetic are certified under §15.3; this certificate does not extend to the separate precision SD/normal-quantile/power calculations.” |
| 20, T-PRE | Replace the headroom and V3 inequalities with the same signed rules used in rows 5 and 18. Append: “Fresh primary/control A/Y/Z intervals are not evaluated before T-PRE passes.” |
| 21, NUM | Replace the criterion with “Complete §15.3 coverage; finite outward row bounds and mean bounds; \(B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j\); both \(|\widehat L_j|\) and \(|\widehat U_j|\) exceed \(\max(B_{{\rm num},j},10^{-9})\).” Remove “proof NOT_READY.” |

Retain the existing scientific failure statuses for H5, V3, and T-PRE when valid certified bounds do not meet their criteria.

## §20, item 14

Replace item 14 with:

> **14.** Symmetry tolerance \(10^{-14}\); the §15.3 numerical certificate with ordered oracle-reference reductions, projective relative envelopes, validated post-logit elementary evaluation, outward A/G/Y/Z intervals, and certified balanced-tree bootstrap means. No universal \(\eta=10^{-12}\) or \(2^{-44}\) constant is used. Per-model \(B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j\). The \(10^{-9}\) floor is an additional guard. Headroom and V3 use signed guards. The proof and implementation specification require independent review before freeze.

## C-19

Replace C-19 with:

> **C-19 (X + W; RC6 replacement).** The certificate targets the stored-weight oracle and mathematical log-softmax of recorded float64 logits. Every eligible row is covered by an ordered reference with a proved componentwise relative envelope, validated elementary-function enclosures, outward construction of A/G/Y/Z and control-frame means, and a specified bootstrap-mean arithmetic bound. Operational BLAS and transcendental errors enter through observed discrepancies. The unsupported \(\eta=10^{-12}\) and \(2^{-44}\) constants remain withdrawn. Define \(B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j\); apply \(\max(B_{{\rm num},j},10^{-9})\) and the signed headroom/V3 guards. Selected reference rows are implementation checks. Independent review is required before freeze.

## Necessary consistency edits

These small edits are required to implement the linked rules without contradicting the rest of v2:

- **§15.2:** replace the rejection of all-row Decimal enclosures with: “The ordinary all-row certificate uses the ordered binary reference of §15.3. Exceptional donor histories use its Decimal fallback. Dense all-row Decimal filtering is not required.”
- **§3.5:** retain the prescribed RNG, seeds, return schema, and percentile helper. Replace the `bootstrap_profile` mean arithmetic through a small C1 wrapper that preserves its index loop and uses the balanced-tree mean kernel. The existing function lacks a mean-kernel parameter; do not monkeypatch NumPy or edit frozen K4 files.
- **§§11 and 12.3:** specify the same balanced-tree kernel for decision bootstrap means and the exact rational quantile ranks.
- **§18:** add the certificate reference, validated elementary helpers, interval construction, and mean wrapper to missing capability; record their source and proof lineage.
- **Header, §17 S0, and §22 F2:** replace “certificate does not yet exist/NOT_READY” with “certificate procedure and proof attached; independent review pending.” Record the review outcome before freeze.

# K4 reuse and new work

| Reuse assessment | Binding decision |
|---|---|
| Existing functionality | Keep `BayesFilter`, `FutureOperator`, model forwards, donor construction, bootstrap RNG semantics, and percentile convention. Reuse K4 `trapping_context`, `u_digits`, `gamma_digits`, `posterior_envelope`, exact discrepancy/comparison ideas, and process-digest conventions. |
| Missing capability | C1 needs predictive and oracle-log enclosures, recorded-logit log-softmax certification, crossed-statistic intervals, and decision-mean bounds. K4’s circular-score certificate does not supply these. |
| Smallest change | Add a certificate-only ordered reference and narrowly scoped elementary/interval/mean helpers. Extract the bootstrap index loop only where the existing public interface cannot accept the certified mean kernel. Frozen K4 files remain unchanged. |
| Stable invariants | Same stored-weight oracle target, histories, logits, arms, frames, seeds, draw counts, row order, and scientific thresholds. Every-row coverage and sealing remain binding. |
| Relevant verification | Reuse exact-rational small-HMM reference machinery and Decimal trap checks. Add verification of the new projective bound, exponential enclosure, crossed expressions, mean tree, and signed guards. |
| Plausible extension | The same certificate can cover another history length or sparse transition support by changing bound dimensions. No generic numerical framework is needed. |

K4’s central reusable principle is **observed operational discrepancy plus a proved reference envelope**, with exact input interpretation, outward bounds, and complete row coverage.

The new contribution is the cheap normalized binary reference and its projective proof. It avoids K4’s dense all-row Decimal cost while retaining K4’s independence from operational-library accuracy.

K4’s process-law bound remains separate. Its idealized independent-uniform sampling assumptions, parameter discrepancy, CDF effects, and TV bound are not added to \(B_{\rm num}\): they compare different laws, whereas this certificate evaluates fixed rows under the already-declared stored-weight target. K4’s process-law result cannot be reused as a C1 causal-control bias bound.

# Open questions

No mathematical question remains open in this proposed certificate.

Independent review must confirm the implementation choices, particularly the ordered reference, validated exponential helper, and small H5 mean wrapper. Authorized implementation must measure cost and fallback frequency and verify the pinned arithmetic prerequisites before scientific execution. No such execution or verification occurred in this planning turn.