STATUS: FREEZE_READY

The proposed construction uses a 4×3 lattice, a hidden cylinder/Möbius world bit, and one explicit emission matrix shared by both worlds. Three columns form a y-blind seam band; its interior seam column is the precise decision phase.

At every reachable history ending in that interior column, the next-symbol distribution is exactly world-independent. At a short reachable witness, both the two-step joint distribution and the symbol-two-steps-ahead marginal differ between worlds by TV = 1/50.

A stronger pair of reachable histories has identical current coordinate beliefs, including conditional on either world, but world posteriors of 1/4 and 3/4. Their next-symbol laws agree, while their two-step laws differ by TV = 1/100. This isolates the predictive information carried by the world posterior.

Outside-band emissions are noisy, preventing finite-history certainty about the world. The stronger histories are rare; their exact probabilities are reported, and no downstream sampling feasibility is inferred.

The verification protocol reuses the existing world, transition, BayesFilter, and FutureOperator kernels. It adds a small fixture and an independent rational reference. No experiments were run, files changed, or scientific payloads opened. “FREEZE_READY” means ready for the required independent review, not already frozen or numerically verified.

# D-1 protocol: an exact cylinder/Möbius horizon gap

## 1. Authority, scope, and provenance

This protocol addresses owner policy B3-D and charter priority 3:

> Does a process exist in which a world-topology distinction is unnecessary for the next symbol at a reachable decision phase, but necessary for a longer prediction horizon?

Binding inputs:

- [Owner policy](X:/Downloads/projects/topo-pilot/agent-handoff/archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md), B3-D.
- [Owner research charter](X:/Downloads/projects/topo-pilot/agent-handoff/NEXT_RESEARCH_AND_WORKFLOW.md), “Owner research charter.”
- [Planning protocol](X:/Downloads/projects/topo-pilot/agent-handoff/planning/PLANNING_PROTOCOL.md).
- [Prior merged decision](X:/Downloads/projects/topo-pilot/agent-handoff/planning/responses/coord-c1-freeze-readiness-20261014.MERGE.md), “D decision.”
- The prior Codex sufficiency lemma, Claude D-1 sketch, and merge analysis §7.

Source inspected: `topo-pilot-circle-history-k4`, HEAD:

```text
4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c
```

This is a new mathematical construction. It does not reopen B2/D-055 or alter any frozen result.

The present deliverable is planning only. Subsequent implementation and oracle verification belong to the executing coordinator’s existing review and release process. No training, checkpoint access, sampling, activation work, or model evaluation belongs to D-1.

## 2. Claim and essential qualification

The claim is local to an observable, reachable decision phase.

It is **not** true that every history ending anywhere in a y-blind band must have world-independent next-symbol predictions. At an outer band edge, the next step may reach a y-revealing column, and conditional y-beliefs may already differ between worlds.

The theorem therefore uses the band interior, where every one-step destination remains y-blind. This is the qualification required by the prior merged decision.

Two results will be established:

1. For every reachable history in that decision phase, conditioning additionally on the world bit does not change the next-symbol law.
2. Some reachable histories in the same phase require retaining information about the world posterior to determine the two-step law.

Here “retaining the distinction” means retaining its predictive information. An equivalent encoding is allowed; the theorem does not require a neuron or explicit register named “world bit.”

## 3. Exact process construction

### 3.1 State space and world bit

Draw an immutable hidden bit once per episode:

\[
Z\in\{C,M\},\qquad P(Z=C)=P(Z=M)=\frac12.
\]

The coordinate state is

\[
S_t=(X_t,Y_t),\qquad
X_t\in\{0,1,2,3\},\quad Y_t\in\{0,1,2\}.
\]

The full HMM state is \((Z,X_t,Y_t)\), giving 24 states.

Within each world, use state index

\[
i(x,y)=3x+y.
\]

Use mixture index \(12z+3x+y\), with \(z=0\) for C and \(z=1\) for M.

### 3.2 Lattice and gluing

Both worlds have ordinary horizontal edges

\[
(x,y)\leftrightarrow(x+1,y),\qquad x=0,1,2,
\]

and ordinary vertical edges

\[
(x,y)\leftrightarrow(x,y+1),\qquad y=0,1.
\]

The y axis is not glued.

The seam edges are:

\[
C:\quad (3,y)\leftrightarrow(0,y),
\]

\[
M:\quad (3,y)\leftrightarrow(0,2-y).
\]

The associated cubical surfaces are a cylinder and a Möbius strip. In particular, their boundary graphs have respectively two components and one component. Both have absolute Betti numbers \((1,1,0)\); Betti numbers alone do not distinguish them.

Crossing the Möbius seam reflects the transverse coordinate. Crossing the cylinder seam preserves it.

### 3.3 Transition probabilities

Use the existing max-degree lazy walk with

\[
p_{\mathrm{stay}}=\frac15,\qquad D_{\max}=4.
\]

Every edge has probability

\[
a=\frac{1-p_{\mathrm{stay}}}{D_{\max}}=\frac15.
\]

For either world,

\[
T_Z(s,s')=
\begin{cases}
1/5,&s'\text{ is an edge-neighbour of }s,\\
1-\deg(s)/5,&s'=s,\\
0,&\text{otherwise}.
\end{cases}
\]

Thus:

| y row | Degree | Actual self-loop |
|---|---:|---:|
| 0 or 2 | 3 | \(2/5\) |
| 1 | 4 | \(1/5\) |

The configured stay probability is a floor. Boundary self-loops also absorb missing vertical edges.

The projected x walk is identical at every y and in both worlds:

\[
P(X_{t+1}=x-1\bmod4)=a,
\]

\[
P(X_{t+1}=x+1\bmod4)=a,
\]

\[
P(X_{t+1}=x)=c:=1-2a=\frac35.
\]

This identity, including at y boundaries, is central to the proof.

### 3.4 Band and alphabet

Use the three-column band

\[
B=\{2,3,0\}.
\]

It is an asymmetric seam band: two columns on one side of the seam and one on the other. Its interior is

\[
I=\{3\}.
\]

Both x-neighbours of column 3, namely columns 2 and 0, lie in \(B\). Column 1 is outside the band.

The alphabet, in this fixed order, is

\[
\mathcal A=(\sigma_0,\sigma_2,\sigma_3,A,B).
\]

The symbols \(A,B\) identify x=1 and provide a noisy observation of y. Every symbol identifies x exactly.

### 3.5 Explicit common emission array

Rows are ordered by \(3x+y\). Columns use the alphabet order above.

\[
E=
\begin{pmatrix}
1&0&0&0&0\\
1&0&0&0&0\\
1&0&0&0&0\\
0&0&0&3/4&1/4\\
0&0&0&1/2&1/2\\
0&0&0&1/4&3/4\\
0&1&0&0&0\\
0&1&0&0&0\\
0&1&0&0&0\\
0&0&1&0&0\\
0&0&1&0&0\\
0&0&1&0&0
\end{pmatrix}.
\]

Set

\[
E_C=E_M=E
\]

by using the same array, not separately generated arrays.

Inside the band, the emission reveals x and contains no instantaneous information about y. Historical information about y may nevertheless persist.

Outside the band:

\[
P(A\mid x=1,y=0)=3/4,\quad
P(A\mid x=1,y=1)=1/2,\quad
P(A\mid x=1,y=2)=1/4.
\]

These rows are identical across worlds. There is no world-dependent emission label or emission parameter.

Do not call `point_distances`, an overlap-emission builder, or centre-placement code. Those interfaces are unnecessary and can mishandle flipped gluing. With this odd y dimension, the existing periodicity helper can also detect a partial set of straight seam edges and reject it.

### 3.6 Initial law and event order

Use the known initial coordinate

\[
(X_1,Y_1)=(1,0)
\]

in both worlds, with the fair world prior. Thus

\[
\pi_{\mathrm{start}}(C,1,0)
=\pi_{\mathrm{start}}(M,1,0)=\frac12.
\]

Emit \(W_1\) from this state, then transition, then emit again. This matches `BayesFilter`’s emit-then-transition convention.

The transition is time-homogeneous; the initial law is deliberately nonstationary. There is no reset or clock gadget during an episode.

Keep this distinction explicit in implementation:

- `TransitionBuilder`’s uniform stationary `pi` remains its validated stationary law.
- `BayesFilter` receives the separately declared \(\pi_{\mathrm{start}}\).
- Do not overwrite `TransitionSpec.pi` with a nonstationary law or weaken its stationarity validator.

The known initial transverse position supplies an orientation reference. It supplies no information about Z.

The single combined process has

\[
\widetilde T=\operatorname{diag}(T_C,T_M),
\qquad
\widetilde E=\begin{pmatrix}E\\E\end{pmatrix}.
\]

Its topological distinction is the posterior

\[
\rho(h)=P(Z=M\mid W_{1:t}=h).
\]

## 4. Theorem: exact horizon-1 independence

Define the decision-history class

\[
\mathcal H_I=
\{h:\ P(h)>0,\ h\text{ ends in }\sigma_3\}.
\]

The decision occurs immediately after observing the terminal \(\sigma_3\), before another transition.

**Theorem 1.** For every \(h\in\mathcal H_I\), and every world with positive conditional probability,

\[
P(W_{t+1}\mid h,Z=C)
=
P(W_{t+1}\mid h,Z=M)
=
(a,a,c,0,0).
\]

Consequently,

\[
P(W_{t+1}\mid h)=(1/5,1/5,3/5,0,0)
\]

independently of \(\rho(h)\).

**Proof.**

The terminal symbol fixes \(X_t=3\). It does not need to fix y.

From column 3, the projected x probabilities are \(a\) to column 0, \(a\) to column 2, and \(c\) to column 3, for every y and both worlds.

All three destinations lie in the band and emit their x symbols deterministically. A Möbius seam crossing may reflect y, but that reflection cannot change these emissions.

Averaging over arbitrary conditional y-beliefs and over the world posterior therefore leaves the same distribution. ∎

This is stronger than checking one witness: it is a row identity on every hidden state compatible with the decision symbol.

## 5. Theorem: an exact two-step gap at a short reachable history

Consider

\[
h_*=(A,\sigma_2,\sigma_3).
\]

Because every symbol identifies x, this history forces the coordinate path

\[
1\to2\to3.
\]

Both transitions are horizontal and avoid the seam. Therefore, conditional on either world,

\[
P(S_3=(3,0)\mid h_*,Z)=1,
\qquad
\rho(h_*)=\frac12.
\]

Its probability in either world, and hence in the mixture, is

\[
P(h_*)=\frac34 a^2=\frac3{100}.
\]

Define the two-step joint and distant-symbol marginal:

\[
J_Z(i,j\mid h)
=P(W_{t+1}=i,W_{t+2}=j\mid h,Z),
\]

\[
Q_{2,Z}(j\mid h)
=P(W_{t+2}=j\mid h,Z).
\]

Use

\[
\operatorname{TV}(p,q)=\frac12\sum_v|p_v-q_v|.
\]

**Theorem 2.**

\[
\operatorname{TV}(J_C(\cdot\mid h_*),J_M(\cdot\mid h_*))
=
\operatorname{TV}(Q_{2,C}(\cdot\mid h_*),Q_{2,M}(\cdot\mid h_*))
=
\frac1{50}.
\]

**Proof.**

Starting at \((3,0)\), the seam-crossing path

\[
3\to0\to1
\]

has probability \(a^2\). Its first emission is \(\sigma_0\).

At the second destination:

- C has y=0 and emits \((A,B)\) with probabilities \((3/4,1/4)\);
- M has y=2 and emits \((A,B)\) with probabilities \((1/4,3/4)\).

Hence

\[
J_C(\sigma_0,A)-J_M(\sigma_0,A)=a^2/2,
\]

with the opposite difference for \((\sigma_0,B)\).

The other path reaching the outside column in two steps,

\[
3\to2\to1,
\]

does not cross the seam and has the same y=0 readout in both worlds.

All remaining two-step paths end in the band. Their emitted laws agree because the projected x process agrees. Thus no other entries differ, and

\[
\operatorname{TV}(J_C,J_M)=a^2/2=1/50.
\]

Summing over the first symbol preserves the two differences on A and B, so the distant-symbol marginal has the same TV. ∎

The explicit joint arrays are:

\[
J_C=
\begin{pmatrix}
3/25&0&1/25&3/100&1/100\\
0&3/25&1/25&3/100&1/100\\
3/25&3/25&9/25&0&0\\
0&0&0&0&0\\
0&0&0&0&0
\end{pmatrix},
\]

\[
J_M=
\begin{pmatrix}
3/25&0&1/25&1/100&3/100\\
0&3/25&1/25&3/100&1/100\\
3/25&3/25&9/25&0&0\\
0&0&0&0&0\\
0&0&0&0&0
\end{pmatrix}.
\]

Their second-symbol marginals are

\[
Q_{2,C}=(6/25,6/25,11/25,3/50,1/50),
\]

\[
Q_{2,M}=(6/25,6/25,11/25,1/25,1/25).
\]

These arrays are normative reference values for verification.

## 6. Stronger witness: the world posterior alone changes

Comparing two world-conditioned forecasts at one history establishes a conditional horizon gap. The following pair additionally establishes that reachable histories can differ only in their mixture weights while retaining identical conditional coordinate beliefs.

Define

\[
h_A=
(A,\sigma_2,\sigma_3,\sigma_0,A,
 \sigma_2,\sigma_3,\sigma_0,A,\sigma_2,\sigma_3),
\]

\[
h_B=
(A,\sigma_2,\sigma_3,\sigma_0,B,
 \sigma_2,\sigma_3,\sigma_0,A,\sigma_2,\sigma_3).
\]

Both force the same x path:

\[
1,2,3,0,1,2,3,0,1,2,3.
\]

There are ten horizontal transitions and two seam crossings. No vertical transition or stay is compatible with these successive x changes.

After the first winding, C has y=0 and M has y=2. After the second winding, both again have y=0.

For both histories and both worlds,

\[
P(S_{11}=(3,0)\mid h_r,Z)=1.
\]

Their collapsed current coordinate beliefs are therefore identical as well.

The middle readout gives:

\[
\rho(h_A)=\frac14,\qquad
\rho(h_B)=\frac34.
\]

The first and third readouts each have likelihood \(3/4\) in both worlds and do not change these odds.

For either history, its mixture probability is

\[
P(h_r)=\frac9{32}a^{10}
=\frac9{312\,500\,000}
=2.88\times10^{-8}.
\]

World-specific probabilities are:

| History | \(P(h\mid C)\) | \(P(h\mid M)\) |
|---|---:|---:|
| \(h_A\) | \((27/64)a^{10}\) | \((9/64)a^{10}\) |
| \(h_B\) | \((9/64)a^{10}\) | \((27/64)a^{10}\) |

Because the conditional current states are identical, their mixture futures satisfy

\[
J(h_r)=(1-\rho(h_r))J_C+\rho(h_r)J_M.
\]

Therefore,

\[
\operatorname{TV}(J(h_A),J(h_B))
=
|\rho(h_A)-\rho(h_B)|\operatorname{TV}(J_C,J_M)
=
\frac1{100}.
\]

The distant-symbol marginals likewise differ by TV \(1/100\):

\[
Q_2(h_A)=(6/25,6/25,11/25,11/200,5/200),
\]

\[
Q_2(h_B)=(6/25,6/25,11/25,9/200,7/200).
\]

Their next-symbol laws remain identical.

Thus a representation that merges these two histories cannot be exactly sufficient for horizon 2. By the TV triangle inequality, any common two-step prediction has TV error at least \(1/200\) on at least one of the histories.

This establishes necessity of distinguishing their predictive information. It does not establish a unique internal encoding or a topological shape of the representation.

## 7. Sufficiency lemma and boundary qualifications

### 7.1 Why this does not contradict recursive sufficiency

The prior Codex lemma states:

If \(S(h)\) determines the next-symbol law at every reachable history and has a deterministic closed update

\[
S(hw)=u(S(h),w),
\]

then it determines every finite future-string law.

For example, successive factors in

\[
P(w_1,\ldots,w_k\mid h)
=
\prod_{j=1}^k P(w_j\mid h,w_1,\ldots,w_{j-1})
\]

can all be recovered recursively.

D-1 makes no contrary claim. Its one-step equality holds at histories ending in \(\sigma_3\). After the next observation, the process may be at an outer band edge, where one-step prediction can require the distinction.

The projection to “current x only” is therefore locally sufficient at the decision phase, but not globally recursively sufficient.

### 7.2 Band entry

Entry from the outside column can reach column 2 or column 0. Those are outer band edges, not the decision phase.

No equality theorem applies there merely because the emission hides y.

An explicit reachable counterexample is

\[
h_{\mathrm{edge}}
=(A,\sigma_2,\sigma_3,\sigma_0,A,\sigma_2).
\]

At its endpoint, conditional y is 0 in C and 2 in M. A one-step move from x=2 to x=1 reveals that difference, giving

\[
\operatorname{TV}
\bigl(P(W_{t+1}\mid h_{\mathrm{edge}},C),
P(W_{t+1}\mid h_{\mathrm{edge}},M)\bigr)
=a/2=1/10.
\]

This counterexample must be included in verification to catch an accidental “whole-band” overclaim.

### 7.3 Lazy stays

The two-step gap event requires two horizontal moves. A stay cannot belong to that event, so its probability is exactly \(a^2\).

Stays and vertical moves contribute to other future entries and are included in the full arrays.

The frozen choice is \(p_{\mathrm{stay}}=1/5\). With a different \(p<1\), the analogous gap scales as \((1-p)^2/32\), provided the same max-degree construction is retained. At \(p=1\), the gap vanishes. No parameter search is part of D-1.

### 7.4 Non-glued y boundaries

Boundary y rows have larger self-loops, but the x-hold probability remains \(3/5\):

\[
2/5+1/5=3/5
\]

at a boundary, and

\[
1/5+2/5=3/5
\]

at the interior row.

The seam maps boundary row 0 to boundary row 2 in M, preserving degrees and probabilities.

The reflection-fixed row y=1 would not produce the stated witness gap. The specified initial row y=0 avoids that degeneracy.

## 8. Oracle-only verification protocol

Everything below is proposed subsequent work. None was executed in this planning turn.

### 8.1 Required implementations

Use the existing kernels unchanged:

- `QuotientLatticeBuilder`, `CylinderBuilder`, `Identification`, `CubicalComplex`, and boundary checks.
- `TransitionBuilder` with `TransitionConfig(p_stay=0.2)`.
- `oracle.BayesFilter`.
- `oracle.FutureOperator.F1` and `.F2`.

Add:

1. A small D-1 fixture containing the fixed dimensions, common emission array, initial law, token mapping, and witness histories.
2. A fixture-local Möbius builder subclass:
   - `Identification(0, "flipped", flip_axis=1)`;
   - expected Betti numbers \((1,1,0)\) over GF(2) and GF(3).
3. A check entry point using the public oracle kernels.
4. An independently authored rational reference and critical tests.

A fixture-local subclass need not mutate the global world registry. Use graph metrics and validate the returned world explicitly.

Pass arrays directly to the oracle. Do not mislabel this custom emission as an existing overlap mode or weaken an emission-schema validator.

### 8.2 Independent exact reference

Build a separate rational specification directly from the coordinate edge formulas in §3, using `Fraction` values:

\[
a=1/5,\quad T_{ss}=1-\deg(s)/5,
\]

the literal emission array, and the literal initial law.

The reference must not obtain its adjacency or expected probabilities from production outputs.

Compute:

- Unnormalised forward probabilities and posterior normalisation.
- History evidence.
- Next-symbol laws.
- Two-step joint laws by summing legal two-transition paths.
- Distant-symbol marginals by summing the joint law.

This independent arithmetic is justified by the charter’s independent-reference exception. It is a small verification implementation, not a replacement operational oracle.

Do not use exhaustive enumeration over \(24^{11}\) state paths. Sparse forward recursion handles histories; legal two-transition path enumeration handles futures.

The existing `tests/oracle_profile/independent_reference.py::decimal_suffix_posterior` may additionally be reused unchanged to cross-check the actual float64 input arrays at 80 digits. It is not the ideal rational specification: its ordinary float inputs are converted as their exact binary values.

### 8.3 Structural checks

Require:

- 12 states, 20 edges, and 8 faces per world.
- Exact coordinate/state ordering.
- Correct ordinary and seam edges, with no additional edges.
- Degrees 3 at y boundaries and 4 at y=1.
- Integer boundary composition \(d_1d_2=0\).
- Betti numbers \((1,1,0)\) over GF(2) and GF(3).
- Boundary graph: two four-edge cycles in C; one eight-edge cycle in M.
- \(E_C=E_M\) bitwise, including outside-band rows.
- Exact rational stochasticity and legal transition support.
- Identical projected x transition matrices.

Boundary components and the gluing rule provide the topology distinction; equal Betti numbers are an expected result.

### 8.4 Universal one-step check

For each y=0,1,2 in both worlds, use the point belief at \((3,y)\).

Require the exact rational identity

\[
\delta_{(3,y)}T_ZE=(1/5,1/5,3/5,0,0).
\]

Cross-check all six rows with `FutureOperator.F1`.

Linearity then verifies the theorem for arbitrary conditional y-beliefs at the decision phase. Enumerating every possible history is unnecessary.

### 8.5 Bayesian witness checks

Run `BayesFilter` on:

- \(h_*\);
- \(h_A\);
- \(h_B\);
- \(h_{\mathrm{edge}}\).

Run both conditional-world filters and the single 24-state mixture filter.

Require the exact evidence, posteriors, conditional coordinate beliefs, and world weights stated above.

For the three interior witnesses, compute `F1`, `F2`, and

\[
Q_2=\sum_{\text{first symbol}}F2.
\]

Do not confuse `FutureOperator.F2`, a joint distribution, with \(bT^2E\), the distant-symbol marginal.

Require:

- The normative \(J_C,J_M\) arrays.
- World-conditioned joint and marginal TV \(1/50\).
- Mixture pair joint and marginal TV \(1/100\).
- Equality between mixture-filter futures and the world-posterior weighted conditional futures.
- Correct first-symbol marginal:
  \[
  \sum_jF2(i,j)=F1(i).
  \]

### 8.6 Controls that detect invalid claims

Use separate synthetic variants; retain the frozen construction unchanged.

| Control | Required result |
|---|---|
| Replace the Möbius seam with the cylinder seam | Witness horizon gaps vanish |
| Set all outside y rows to \((A,B)=(1/2,1/2)\) | Witness horizon gaps vanish |
| Change the initial y to reflection-fixed y=1 | These witness gaps vanish |
| Evaluate \(h_{\mathrm{edge}}\) | One-step world TV is \(1/10\) |

The first three must cause the positive gap criterion to fail. The fourth must falsify any implementation that applies one-step equality to the entire band.

### 8.7 Numerical tolerances

Exact rational checks use equality, without tolerance.

Float64 acceptance thresholds:

| Quantity | Threshold |
|---|---:|
| Array entries against rational reference converted to float64 | Maximum absolute error \(10^{-12}\) |
| Beliefs, F1, F2, and marginals against reference | Maximum absolute error \(10^{-12}\) |
| Distribution sum residuals | \(10^{-12}\) |
| One-step world/pair difference at interior witnesses | TV at most \(10^{-12}\) |
| Reported TV against \(1/50\), \(1/100\), or \(1/10\) | Absolute error at most \(10^{-12}\) |
| History evidence | Relative error at most \(10^{-10}\) |
| Log evidence | Absolute error at most \(10^{-10}\) |

Evidence needs a relative tolerance because the stronger witness probabilities are small.

Reject nonfinite values or negative probabilities. Preserve genuine zeros; add no smoothing or epsilon. Existing oracle validators remain unchanged even where their internal tolerance is looser.

The floating checks validate the implementation against the proof. Numerical agreement alone is not the proof.

### 8.8 PASS/FAIL criteria

**PASS** requires all structural, exact-arithmetic, Bayesian, numerical, and control checks to pass.

In particular, PASS requires both:

1. The universal one-step row identity at the stated decision phase.
2. The reachable posterior-isolation pair with identical coordinate beliefs and two-step TV \(1/100\).

**FAIL** means any required mathematical or implementation assertion fails. Preserve the discrepancy and its cause.

An interrupted or incomplete run is **NOT_COMPLETED**, not a scientific FAIL. A PASS on only the shorter witness is insufficient for full protocol acceptance.

No sampling uncertainty, confidence interval, learned predictor, or empirical gap estimate is involved.

## 9. Six-field reuse assessment

| Field | Assessment |
|---|---|
| **Existing functions/artifacts** | Reuse world lattice/gluing/complex machinery, graph metrics, transition construction/support validation, BayesFilter, and FutureOperator unchanged. Existing Decimal posterior reference is compatible with these dimensions and histories. No old scientific payload or oracle cache is applicable. |
| **Genuinely missing capability** | The fixed D-1 emission/initialisation fixture, fixture-local flipped world, mixture assembly, boundary-component assertion, and exact reference checks. |
| **Smallest change** | One small fixture/check package plus independently authored verification code. No new sampler, operational filter, future engine, model, or generic runner. |
| **Stable interfaces/invariants** | Row-vector convention; \(T[N,N]\), \(E[N,V]\), \(\pi[N]\); emit-then-transition; C-order states; immutable world bit; common E; explicit nonstationary initial law; no smoothing. All histories fit BayesFilter’s length limit of 33. |
| **Relevant regression checks** | State/seam ordering, y-boundary self-loops, all six interior F1 rows, mixture weighting, evidence and posterior identities, F2 indexing and both marginals, and the four controls above. Run existing affected world/process/oracle checks once after implementation. |
| **Next plausible extension** | A separately reviewed trained-model assay with a specified distribution of reachable decision histories. It can reuse these arrays and oracle targets. No horizon sweep or generic experiment framework is needed now. |

Critical test/reference authors should work from the frozen mathematical contract before production implementation and should be independent of its author.

## 10. Cost, records, and release sequence

The dimensions are small:

- 24 mixture states.
- 5 symbols.
- 25 two-symbol outcomes per belief.
- Maximum witness length 11.
- At most five legal outgoing transitions per state.

No SVD, training, sampled history bank, or exponential future enumeration is needed.

Forecast: ordinary checks should take seconds; allow a conservative **under 300 CPU-seconds** estimate for implementation checks and integration verification. This is an unbenchmarked forecast, not a CPU cap.

Use one thread by default; retain the owner’s limits of at most four threads and 12 GiB RAM, existing usage/STOP controls, disk thresholds, and CPU accounting. Reports should be small and stored on X:.

Proposed sequence:

1. Merge independent planning tracks.
2. Obtain the required clean-context, result-blind review.
3. Freeze the construction, histories, arrays, tolerances, and criteria.
4. Have independent critical tests/reference authored.
5. Implement the minimal fixture and checks.
6. Accept implementation after relevant checks.
7. Release the oracle-only verification.
8. Independently review its evidence and record the scoped result.

The report must contain:

- Frozen protocol/request hashes and implementation/base commits.
- Environment and state/alphabet ordering.
- Rational construction values and float-array identities.
- Structural checks and boundary components.
- Evidence, coordinate beliefs, and world posteriors for each witness.
- Full F1/F2 results, marginals, TV values, and numerical residuals.
- Controls, measured CPU, and PASS/FAIL/NOT_COMPLETED.
- The licensing statement below.

No protected artifact, frozen criterion, or existing result is overwritten.

## 11. Risks and mitigations

### 11.1 Uniform or reflection-symmetric y-beliefs erase the witness

A reflection-symmetric readout belief can remove the gap; y=1 is an explicit example.

**Mitigation:** Freeze the orientation-referenced initial law y=0 and verify its role with the y=1 control. Do not silently substitute the transition builder’s stationary prior. Report this initialisation assumption as part of the construction.

### 11.2 Rare posterior-isolation histories

Each stronger history has probability \(2.88\times10^{-8}\). Natural sampling would be inefficient.

This does not compromise an existence proof: both histories have strictly positive, exactly computed probability.

The decision phase itself is less rare. The projected x walk starts at x=1, so

\[
P(X_3=3)=2a^2=2/25=0.08.
\]

The short witness has probability \(0.03\). The projected x chain has stationary interior-column probability \(1/4\).

**Mitigation:** Use exact calculations now. Require a separate downstream reachability/coverage analysis. Any future phase-enriched or conditional-prefix evaluation must declare its distribution and restrict its claims accordingly. Do not claim that the rare pair represents a typical natural-history population.

### 11.3 World identification becomes a shortcut

Direct world-labelled emissions or noiseless transverse readouts could turn the construction into finite-history world decoding with certainty.

**Mitigation:** The shared outside channel uses probabilities between \(1/4\) and \(3/4\). Both worlds support every feasible finite observed history, and finite histories cannot produce posterior 0 or 1.

More explicitly, with m outside observations, conditional x-path emission probabilities in either world lie between \((1/4)^m\) and \((3/4)^m\). The x-path probability is common, so world likelihood ratios remain between \(3^{-m}\) and \(3^m\).

The stronger pair has nondegenerate posteriors \(1/4\) and \(3/4\), yet its coordinate beliefs are identical.

Long-run identification may still be possible. That is compatible with a phase-specific theorem; do not claim that world information is globally unnecessary.

### 11.4 A static emission difference impersonates topology

**Mitigation:** Use one literal E array and demand bitwise equality across worlds. The only world-dependent operation is the seam gluing.

At stationary uniform coordinate laws, the single-symbol distribution is also identical:

\[
P(\sigma_0)=P(\sigma_2)=P(\sigma_3)=1/4,\qquad
P(A)=P(B)=1/8.
\]

This stationary statement does not imply identical nonstationary observation distributions at every time.

### 11.5 Cancellation or horizon confusion

A signed difference on one path does not always establish a full-law gap, and joint and distant-symbol horizons need not agree.

**Mitigation:** Supply the full arrays and sum them exactly. Here both versions have the stated gap, so no cancellation assumption is needed.

### 11.6 Topological overinterpretation

A finite HMM and a scalar posterior can encode this distinction. Cylinder and Möbius also have equal absolute Betti numbers.

**Mitigation:** Restrict the conclusion to predicting the shared-emission process under different seam gluings. Claim no necessary H1 structure, continuous circular representation, particular architecture, or learned orientability detector.

## 12. What PASS licenses downstream

PASS licenses the following statement:

> A concrete finite process with a hidden cylinder/Möbius world bit has a reachable observable decision phase where world information is exactly irrelevant to next-symbol prediction, while two-step prediction requires distinctions carried by the world posterior. The gap is established by construction and independently checked against the existing oracle kernels.

It licenses drafting a later trained-model protocol. It does not release training automatically.

That later protocol must add:

- A defined training and evaluation distribution, including treatment of the known initial coordinate and rare witnesses.
- A comparison of next-symbol and longer-horizon objectives, with the latter defined as joint prediction, distant-symbol prediction, or both.
- Oracle headroom, coverage, and model-competence gates.
- A representation-level hypothesis distinguishing world-posterior retention from coordinate-belief retention and recent-symbol shortcuts.
- A causal intervention and matched controls if functional use or necessity is claimed.
- Frozen architectures, context lengths, checkpoints, seeds, endpoints, numerical criteria, calibration/validation rules, and fresh-test procedure.
- Independent review and implementation acceptance before result exposure.

A next-symbol-trained model may retain Z because it matters at later positions or other decision phases. Local one-step irrelevance therefore does not predict that such a model will discard world information.

For the original square/cylinder pilot, PASS establishes no horizon gap, no reinterpretation of B2/D-055, and no explanation of E4’s circular representations. D-1 changes the world comparison, alphabet, emissions, and initial law. It supplies an existence result and a controlled future testbed.

# Open questions

No scientific construction choice remains open in this proposal.

Before freeze, independent review must accept the deliberately asymmetric three-column band and nonstationary orientation-referenced initial law, and verify the stronger witness algebra. The coordinator must also bind the common request hash, reviewed base commit, and later implementation/report identities.

A downstream trained-model population remains a separate planning question because the posterior-isolation witnesses are rare.