STATUS: FREEZE_READY

## Summary

Use two identical 12×12 torus walks with different emissions. A has a wrapped Gaussian emission field. B applies a small, symmetric blur to that field along one axis:

\[
E_B(z,\cdot)=\tfrac34E_A(z,\cdot)
+\tfrac18E_A(z+2e_x,\cdot)
+\tfrac18E_A(z-2e_x,\cdot).
\]

This construction preserves symbol marginals exactly, remains smooth and periodic, and changes the emission-row multiset. B therefore is not a P-world. A two-symbol correlation proves that the sequence laws differ; finite-history separation remains an empirical question.

Stage 0 measures component-posterior entropy through 512 observations, mutual information from windows of length 1, 2, 4 and 8, and the information gained from earlier history. It also tests the complete 288-dimensional beliefs for two separated clouds, each with two H1 bars, using a preregistered Hellinger metric, reference-derived scale band and null controls.

A later priority-1 study is recommended only if validated bounds give at least 0.8 bits of full-history component information, at most 0.2 bits from eight symbols, and at least 0.6 bits of information beyond that window, together with the required belief-space topology.

Reuse the existing long-window suffix oracle unchanged; cross-check it against `BayesFilter` and independent high-precision calculations. Estimated cost is 2–6 CPU-hours, unbenchmarked, with one thread and no CPU ceiling.

This is a complete proposed protocol for independent review and freeze. No experiments, payload access, file writes or git mutations were performed.

# Corrected X2a Stage 0: oracle feasibility for \(T^2\sqcup T^2\)

## 1. Authority, scope and provenance

Authority is owner overnight authorization B3-E: corrected X2a, Stage 0, oracle only, no training, with X6 excluded from this round. The scientific motivation is charter priority 1: distinguish information supplied by one symbol, short context and earlier history.

This document authorizes no execution by the planning track. Execution remains with the coordinator after merge, independent result-blind review and freeze under `planning/PLANNING_PROTOCOL.md`.

Read-only sources inspected:

| Source | Binding or observation |
|---|---|
| `agent-handoff/planning/PLANNING_PROTOCOL.md` | Independent planning tracks; coordinator merge; third review before freeze |
| `archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md` | SHA256 `13160D21CA0F52BEC04CCC9AA73BBE4016842C8A108E32994656F57E5B4E69CA` |
| `NEXT_RESEARCH_AND_WORKFLOW.md` | SHA256 `2B1BE9E77497ECFF04C90500F90AAB045FEFA4BA5F311F1E7736C83F61C3FD3C` |
| Planning request | SHA256 `4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595` |
| Research checkout | `topo-pilot-circle-history-k4`, HEAD `c2046fc7426d25779da4be74b86f92a8119924a5` |
| D-1 implementation reference | `topo-pilot-d1/tools/d1_seam/`, inspected at branch tip `c364f95` |
| D-1 accepted record | Job 0020 report: PASS, following the two-module amendment |

The research checkout does not contain `tools/d1_seam/`; its implementation was inspected in the separate D-1 checkout. Do not assume those files already exist in the execution base.

Before execution, the coordinator binds the complete execution commit, environment, implementation manifest and frozen protocol hash. A different base requires a documented source compatibility check.

## 2. Scientific question and competing explanations

The primary question is:

> Can long histories identify the component and produce two toroidal exact-belief clouds when one symbol provides no component information and eight-symbol windows provide little?

The competing explanations are:

| Explanation | Discriminating observation |
|---|---|
| Component identity leaks through symbol frequencies | Nonzero \(I(C;W_t)\), or failed marginal verification |
| Short transition patterns already identify the component | Large \(I(C;W_{t-7:t})\), leaving little full-history headroom |
| Earlier history accumulates substantial additional evidence | Large \(I(C;W_{1:512}\mid W_{505:512})\) |
| Component information accumulates, but belief geometry does not display the proposed topology | Information gates pass while PH gates fail |
| Oracle feasibility supports the intended later comparison | Both information and belief-topology gates pass |

No trained representation, architecture, optimization or causal-use claim is tested.

## 3. Frozen construction

### 3.1 States and topology

Let

\[
Z=\{A,B\}\times\mathbb Z_{12}\times\mathbb Z_{12},
\qquad N=288.
\]

Use state order

\[
s(c,x,y)=144\,1[c=B]+12x+y.
\]

Each component has the usual square cubulation with both axes periodic.

Per component:

- 144 vertices;
- 288 edges;
- 144 square faces;
- degree four everywhere;
- Euler characteristic zero;
- Betti numbers \((1,2,1)\) over GF(2) and GF(3).

The disjoint union has Betti numbers \((2,4,2)\).

Build one torus with a local, unregistered `QuotientLatticeBuilder` subclass containing periodic identifications on both axes. Represent the union by explicit block arrays and, for structural verification, a block sum of the component complexes.

Do not register an extension family or manufacture finite inter-component world distances.

### 3.2 Dynamics and start law

On each torus, use

\[
T_0(z,z)=\frac12,\qquad
T_0(z,z\pm e_x)=T_0(z,z\pm e_y)=\frac18.
\]

All other entries are zero. Thus

\[
T=\begin{pmatrix}T_0&0\\0&T_0\end{pmatrix},
\qquad
\pi(s)=\frac1{288}.
\]

The component is selected once and remains fixed. Conditional on either component, the initial position is uniform.

Both components use bitwise-identical copies of \(T_0\). The stay probability is a deliberate Stage 0 setting, not an inherited default.

The process is stationary from its first emission.

### 3.3 Torus metric and alphabet

For either component,

\[
d_T(z,z')^2
=\delta_{12}(x-x')^2+\delta_{12}(y-y')^2,
\quad
\delta_{12}(u)=\min_{m\in\mathbb Z}|u+12m|.
\]

Use \(V=36\) symbols \(v=(a,b)\), with

\[
a,b\in\{0,\ldots,5\},\qquad c_v=(2a,2b).
\]

The public symbol ID is \(6a+b\), identically in both components.

Compute these distances explicitly. Do not call `process/_geometry.point_distances`: its inspected implementation wraps only axis zero.

### 3.4 A: smooth torus Gaussian

Freeze \(\sigma=1.25\).

Use the wrapped Gaussian kernel on the flat torus:

\[
K_\sigma(z,c)
=\sum_{m\in\mathbb Z^2}
\exp\left(-\frac{\|z-c+12m\|^2}{2\sigma^2}\right),
\]

and

\[
E_A(z,v)=
\frac{K_\sigma(z,c_v)}
{\sum_{u=0}^{35}K_\sigma(z,c_u)}.
\]

Periodization makes this a genuinely smooth Gaussian field on the torus. A shortest-distance Gaussian alone has cut-locus derivative discontinuities; it is not the primary construction.

For numerical construction, reduce each coordinate displacement to \([-6,6]\), evaluate image indices \(-2,\ldots,2\) in each axis, and certify the omitted tail. Require an entrywise tail-and-normalization bound below \(10^{-100}\). Use at least 80 decimal digits for the independent construction reference.

Supply the oracle with an explicit float64 \(144\times36\) array.

### 3.5 B: symmetric local blur

Let \(R_\pm\) shift a state by \(\pm2e_x\), modulo 12. Define

\[
K=\tfrac34 I+\tfrac18R_++\tfrac18R_-,
\qquad E_B=K E_A.
\]

Equivalently,

\[
E_B(z,v)=
\tfrac34E_A(z,v)
+\tfrac18E_A(z+2e_x,v)
+\tfrac18E_A(z-2e_x,v).
\]

This is a smooth, periodic, anisotropic change of the emission field. It is a Gaussian mixture rather than a single coordinate warp.

The mixture is applied independently at each emission. It does not select one translated field for an entire trajectory.

Freeze these weights and shifts. There is no parameter sweep or post-result adjustment.

### 3.6 Exact marginal matching

The center grid and torus translations imply

\[
\frac1{144}\sum_z E_A(z,v)=\frac1{36}
\]

for every symbol.

Each \(R_\pm\) is a permutation matrix, so \(K\) is doubly stochastic. Therefore

\[
\frac1{144}\mathbf1^\top E_B
=\frac1{144}\mathbf1^\top E_A.
\]

Consequently, exactly in the mathematical construction,

\[
P(W_t=v\mid C=A)=P(W_t=v\mid C=B)=\frac1{36},
\]

at every position, and

\[
P(C=A\mid W_t=v)=\frac12,\qquad I(C;W_t)=0.
\]

For stored float arrays, verify row sums, stationarity and marginal equality to \(10^{-12}\), and compute the residual one-symbol MI directly. Report the exact identity and numerical residual separately.

No balancing or fitting procedure is needed.

### 3.7 Why B is not a P-world

In the inspected implementation, P preserves A’s emission-row multiset by permuting states.

Here,

\[
\|KE_A\|_F^2<\|E_A\|_F^2.
\]

The inequality is strict because A’s rows vary along the shifted axis and \(K\) averages distinct rows. Thus B does not share A’s row multiset and cannot be obtained by any state-row permutation, including the axis-wise P construction.

Verify the strict inequality with a high-precision enclosure. Report the change in conditional emission entropy as a construction property: the blur introduces a noise difference that may itself be detectable from short sequences. The information gates assess whether that compromises the intended study.

### 3.8 Guaranteed sequence-law distinguishability

Use the observable

\[
f(v)=1[a(v)=0],
\qquad
g(x)=\sum_b E_A((x,y),(0,b)).
\]

Factorization makes \(g\) independent of \(y\). Under B its conditional expectation is \(Kg\).

On functions of \(x\), the walk acts as

\[
L=\tfrac34 I+\tfrac18R_{+1}+\tfrac18R_{-1}.
\]

The two-symbol statistic is

\[
S_A=P_A(a(W_1)=0,a(W_2)=0)
=\frac1{12}g^\top Lg,
\]

\[
S_B=\frac1{12}g^\top K L K g.
\]

The commuting operators have Fourier eigenvalues

\[
\lambda_m=\tfrac34+\tfrac14\cos(2\pi m/12)>0,
\]

\[
\kappa_m=\tfrac34+\tfrac14\cos(4\pi m/12)\in[1/2,1].
\]

Hence \(S_A-S_B\ge0\), with strict inequality whenever \(g\) has a mode outside \(m=0,6\). It does: \(g(0)>g(2)\), since the denominator repeats after two states while the Gaussian centered at zero decreases.

Therefore the two-symbol laws differ.

Numerically verify both \(g(0)>g(2)\) and \(S_A-S_B>0\) with strictly positive interval lower bounds. A certified lower bound above \(10^{-10}\) is the required implementation witness.

Both component processes are stationary and ergodic. Their empirical two-symbol statistics therefore consistently distinguish them as history grows. This establishes asymptotic identifiability, not useful concentration by 512 symbols.

## 4. Oracle estimands

Write

\[
h_t=W_{1:t},\qquad
b_t(s)=P(Z_t=s\mid h_t),
\]

\[
r_t=\sum_{s\in A}b_t(s)=P(C=A\mid h_t).
\]

All primary beliefs retain all 288 coordinates.

### 4.1 Component concentration

At

\[
\mathcal T=\{0,1,2,4,8,16,32,64,128,256,512\},
\]

report:

- mean posterior entropy
  \[
  \mathcal H_t=E[h_2(r_t)]
  \]
  in bits;
- posterior-entropy quantiles;
- Bayes component error \(E[\min(r_t,1-r_t)]\);
- fraction with \(\max(r_t,1-r_t)\ge0.95\);
- classification error against the generating component;
- results conditional on each generating component.

Define the concentration time as the first grid position whose simultaneous upper confidence bound for \(\mathcal H_t\) is at most 0.2 bits. Report the grid interval containing that crossing. If none crosses, report “not reached by 512.”

Posterior entropy decreases in expectation, not necessarily along every trajectory. Do not enforce monotonicity on individual trajectories or smooth estimates into compliance.

### 4.2 Short-window component information

For \(k\in\{1,2,4,8\}\), let

\[
U_{t,k}=W_{t-k+1:t}.
\]

Compute its posterior by restarting from the unconditional stationary prior at the window boundary:

\[
r^{(k)}_t=P(C=A\mid U_{t,k}).
\]

Do not initialize with a posterior carrying information from earlier history.

Report

\[
I_k=I(C;U_{t,k})
=1-E[h_2(r^{(k)}_t)].
\]

Stationarity makes this independent of \(t\ge k\).

Also report

\[
I_{\rm full}(t)=1-\mathcal H_t
\]

and, at 512,

\[
G_8=I(C;W_{1:512}\mid W_{505:512})
=I_{\rm full}(512)-I_8.
\]

This conditional MI is the decisive priority-1 headroom measure.

Report \(G_k=I_{\rm full}(512)-I_k\) for the other requested windows as well.

### 4.3 Exact short calculations

Compute \(I_1=0\) analytically and directly from the supplied arrays.

Compute the entire two-symbol distribution:

\[
J_c(u,v)=
\frac1{144}
E_c[:,u]^\top T_0 E_c[:,v].
\]

There are only 1,296 symbol pairs. Calculate

\[
I_2=\frac12\sum_{c,u,v}J_c(u,v)
\log_2\frac{J_c(u,v)}
{\tfrac12[J_A(u,v)+J_B(u,v)]}.
\]

Use high precision to validate the result and the distinguishing witness.

Lengths four and eight use validated Monte Carlo. No exhaustive \(36^8\) enumeration is proposed.

## 5. Monte Carlo design and uncertainty

### 5.1 Information cohort

Generate exactly 16,384 independent stationary trajectories of length 512 from the joint process. Draw component and initial position through the uniform joint prior.

Use this one cohort for:

- the prefix entropy curve;
- suffix-window estimates at position 512;
- paired information-gap estimates;
- concentration and error summaries.

Positions within a trajectory are not independent observations. Confidence calculations use trajectories as the independent units.

Do not stop early on a favorable result or add samples when a boundary is narrowly missed.

### 5.2 Estimation and confidence bounds

The primary estimator uses the oracle posterior:

\[
\widehat I_k
=1-\frac1n\sum_i h_2(r^{(k)}_i).
\]

This avoids estimating a distribution over observed strings.

Use simultaneous bounded-variable Hoeffding intervals with familywise error at most 0.01. Reserve 64 scalar claims before computation:

\[
\epsilon=
\sqrt{\frac{\log(2\cdot64/0.01)}{2n}}.
\]

For quantities in \([0,1]\), use half-width \(\epsilon\). For paired differences in \([-1,1]\), use half-width \(2\epsilon\). Add the validated numerical error allowance before threshold decisions.

The implementation manifest must list every claim using this allowance and stay within 64. Additional descriptive summaries receive no confirmatory confidence label.

Include these checks:

- exact \(I_2\) lies inside its Monte Carlo interval;
- information is consistent with
  \[
  0=I_1\le I_2\le I_4\le I_8\le I_{\rm full}(512);
  \]
- block-summed joint posteriors agree with component-likelihood calculations on the validation subset.

Do not clip negative estimated gaps to zero before inference. A confidence interval containing zero is an unresolved estimate; a validated contradiction of a mathematical identity is an implementation failure.

### 5.3 Randomness and isolation

Use `SeedTree` with master seed `20261015` and separate namespaces for:

- information histories;
- four PH panels;
- reference perturbations;
- each null family and null replicate;
- numerical-validation history selection.

Freeze the complete namespace-to-seed mapping before sampling.

Reference calibration and PH evaluation histories must be independent of the information cohort.

## 6. Preregistered belief-space PH

### 6.1 Metric and estimator

Use Hellinger distance on complete belief distributions:

\[
d_H(p,q)=\frac{\|\sqrt p-\sqrt q\|_2}{\sqrt2}.
\]

Compute Vietoris–Rips persistence with:

- GF(2) primary;
- `maxdim=1`;
- full pairwise distance matrices;
- filtration through the maximum distance;
- no PCA, learned projection, landmark approximation or fitted metric.

Use the existing `PersistenceComputer`, `Hellinger` and `Summaries`.

GF(3) is a fixed sensitivity analysis on the late panels, not an alternative route to passing.

### 6.2 Reference calibration

Calibrate before evaluating any sampled belief cloud.

First verify world-level VR behavior on the exact torus metric. This is distinct from the exact cubical-homology check.

For the belief-distance scale, build reference distributions

\[
q_{c,z}^{(\rho)}(c',s)
=
1[c'=c]\,
\frac{K_\rho(s,z)}
{\sum_u K_\rho(u,z)},
\]

for all 144 centers in each component and

\[
\rho\in\{0.75,1.0,1.25\}.
\]

These are known toroidal families of localized probability distributions in the same 288-coordinate probability space as the tested beliefs.

For each width, compute:

- each component’s diagram;
- the pooled diagram.

Find the common scale set where all references satisfy:

\[
\beta_0(A)=\beta_0(B)=1,\quad
\beta_1(A)=\beta_1(B)=2,
\]

\[
\beta_0(A\cup B)=2,\quad
\beta_1(A\cup B)=4.
\]

Use diagram endpoints to obtain exact plateau intervals. Choose the longest common interval; break ties by the smaller left endpoint.

Require its raw Hellinger width to be at least 0.08. The evaluation band \(B_{\rm PH}\) is its central half, giving width at least 0.04.

If no such interval exists, record `CALIBRATION_INCONCLUSIVE`. Do not choose another width, metric or scale rule.

Also test five fixed perturbations per reference width by mixing each reference distribution with 1% independently drawn Dirichlet noise within its own component. Report their robustness at the same band; failure blocks a topology GO.

This calibration establishes an operating scale for the estimator. It does not establish the topology of the oracle clouds.

### 6.3 Evaluation panels

Generate four independent panels. Each contains:

- 256 histories generated from A;
- 256 histories generated from B;
- uniform initial position within the selected component;
- 512 observations per history.

At positions 32, 128 and 512, compute the joint 288-dimensional posterior using the unconditional equal-component prior.

The primary late position is 512. Earlier positions are fixed descriptive comparisons.

Use the generating component only to:

- construct balanced evaluation cohorts;
- divide clouds for within-component assessment;
- verify correspondence of discovered connected components.

Do not use latent endpoint coordinates to change beliefs, distances or point locations.

Do not average beliefs into state centroids, condition on posterior confidence, force endpoint coverage or discard apparent bridges. Report latent endpoint coverage and posterior localization as diagnostics.

### 6.4 Topology pass for one panel

Throughout the entire fixed \(B_{\rm PH}\), require:

1. A’s complete-belief cloud has \(\hat\beta_0=1,\hat\beta_1=2\).
2. B’s complete-belief cloud has \(\hat\beta_0=1,\hat\beta_1=2\).
3. The pooled cloud has \(\hat\beta_0=2,\hat\beta_1=4\).

The two bars for each component must individually span the entire band. Report their endpoints, the third-longest persistence and the complete diagrams.

For H0, also compute

\[
r_{\rm conn}
=\max\{\text{largest within-A MST edge},
       \text{largest within-B MST edge}\},
\]

\[
r_{\rm cross}=\min_{i\in A,j\in B}d_H(b_i,b_j).
\]

The required separation is

\[
r_{\rm conn}<\inf B_{\rm PH},
\qquad
r_{\rm cross}>\sup B_{\rm PH}.
\]

Report \(r_{\rm cross}-r_{\rm conn}\). This checks that the two connected clouds correspond to the generating components without imposing clustering.

At least three of the four late panels must pass all requirements. Preserve and report the fourth panel regardless of outcome.

### 6.5 Short-window and conditional-component diagnostics

On the same PH histories at position 512, compute joint beliefs from the last 1, 2, 4 and 8 symbols and evaluate them at the same band.

These results show what geometry is already available to short context. Their PH signatures are descriptive; they do not replace the MI comparison.

As a diagnostic only, compute within-component normalized beliefs

\[
b(s\mid C=c,h).
\]

They can distinguish failure to identify the component from failure to display within-component geometry. They cannot rescue a failed primary test of the complete joint beliefs.

### 6.6 Null controls

**Identical-component null.** Set \(E_B=E_A\), keeping the same dynamics and equal component prior.

For every history,

\[
b_t=\left(\tfrac12p_t,\tfrac12p_t\right),\qquad r_t=\tfrac12.
\]

Require numerical agreement with this identity and zero component information. At the calibrated band, the two generating cohorts must not produce the full component-aligned separation criterion.

**Isometric-copy null.** Set \(E_B(z)=E_A(z+2e_x)\). The sequence laws are identical by translation invariance.

Require posterior component probability one half and zero component MI. This directly catches the defect of treating an isometric copy as distinguishable.

**Uniform-emission null.** Set both emission arrays to \(1/36\). Beliefs must remain the joint stationary prior; the cloud collapses and has no H1 bars.

**Covariance-matched geometric null.** Embed beliefs as \(\sqrt b/\sqrt2\). For each component cloud and panel, use the existing covariance-matched Gaussian null generator. These Euclidean surrogates are geometric controls, not probability distributions.

Generate 19 independent surrogate sets, each containing counterparts for all eight component clouds. Keep \(B_{\rm PH}\) fixed.

For each panel, score the smaller of the two components’ second-largest H1 persistences, assigning zero if either lacks two bars spanning the band. Aggregate with the third-largest panel score, corresponding to the required three-of-four rule.

Require the observed aggregate score to exceed all 19 surrogate scores. Report the rank contrast \((1+\#\text{surrogates}\ge\text{observed})/20\).

This is an auxiliary contrast against this particular Gaussian null, not a universal significance test for torus topology.

A permutation of true component labels leaves the cloud and its PH unchanged. It is therefore not an intrinsic PH null. Likewise, scrambling labels does not invalidate the entropy formula when its posterior still belongs to the original generative model.

## 7. Frozen GO/STOP criteria

All thresholds below are fixed before computation.

### 7.1 Validity prerequisites

Require:

- correct world structure, transition support and start law;
- exact marginal-matching proof and acceptable array residuals;
- certified non-P and sequence-distinguishability witnesses;
- numerical-reference checks;
- successful reference calibration and required controls;
- complete, uncensored primary PH calculations.

A numerical or control contradiction gives `INVALID`, not a scientific negative result. Resource interruption or censored required PH gives `INCONCLUSIVE`.

### 7.2 Priority-1 information gate

Require simultaneous validated bounds:

\[
L[I_{\rm full}(512)]\ge0.8\text{ bits},
\]

\[
U[I_8]\le0.2\text{ bits},
\]

\[
L[G_8]\ge0.6\text{ bits}.
\]

The exact last-symbol information must be zero.

These thresholds define a substantial history-dependent contrast. They are not claims that eight-symbol information is exactly absent.

### 7.3 Belief-topology gate

Require:

- at least three of four late panels pass §6.4;
- required reference and geometric-null checks pass;
- identical, isometric and uniform controls behave as specified.

### 7.4 Verdicts

| Verdict | Meaning |
|---|---|
| `GO_PRIORITY1_CANDIDATE` | Validity, information and topology gates all pass |
| `STOP_SHORT_CONTEXT` | Valid results establish excessive short-window information or insufficient earlier-history headroom |
| `STOP_BELIEF_TOPOLOGY` | Information gate passes, but the proposed complete-belief topology fails |
| `STOP_FINITE_HORIZON` | Component information remains insufficient by 512 |
| `INCONCLUSIVE` | Confidence bounds straddle required thresholds, calibration fails, or required computations are censored/incomplete |
| `INVALID` | Construction, numerical verification, controls or provenance fail |

Report every gate separately when several conditions apply. Do not obscure a scientific finding behind a single aggregate label.

There is no automatic retuning, larger sample, longer horizon or alternative construction following a STOP or INCONCLUSIVE result. Those require a new protocol.

### 7.5 Conditions on a later trained-model study

A Stage 0 GO supports designing a later study; it does not authorize training.

A later protocol must:

- use a context length for which Stage 0 establishes the intended information gap;
- compare full-history representations with exact short-window baselines;
- distinguish component identification from within-component coordinates;
- test prediction quality before interpreting representation geometry;
- preregister representation sites, topology analysis and uncertainty;
- add interventions if functional or causal use is claimed.

Passing only at 512 does not justify a 32-token model study. Report the information available at 32 explicitly.

As a descriptive oracle diagnostic, compare next-symbol predictions from full history and the last eight symbols using existing `FutureOperator.F1`, reporting

\[
E\,D_{\rm KL}(q_{\rm full}\|q_8).
\]

This includes both position and component information. It does not isolate the predictive value of component identity.

## 8. Verification and implementation sequence

The executing coordinator should require the following order.

1. **Freeze and provenance.** Bind the reviewed protocol, execution commit, dependencies, seeds, output location and one-thread settings.
2. **Written API.** Specify construction, oracle inputs, estimands, validation outputs and verdict semantics before implementation.
3. **Independent checks.** Have a clean-context verifier derive tests from the protocol and API.
4. **Structural verification.** Check both periodic seams, cells, boundary identities, homology, degrees, transition support and stationarity.
5. **Emission verification.** Compare explicit arrays with the independent high-precision formula; verify marginals, blur weights and distinguishing witnesses.
6. **Oracle verification.** Complete the checks below before scientific sampling.
7. **Reference PH calibration.** Freeze the derived band using the fixed rule.
8. **Run fixed cohorts and controls.**
9. **Apply frozen decisions and publish a complete report**, including unsuccessful gates, uncertainty and resource use.

### 8.1 Oracle reuse and cross-checks

The inspected `BayesFilter.run` restricts histories to 33 symbols.

The inspected

`tools/x4_oracle_profile/oracle_profile.py::suffix_posterior`

accepts longer histories, performs scaled forward filtering and returns the final posterior. It can operate directly on the joint \(T,E,\pi\).

Use that function unchanged for the main calculations:

- prefix \(t\): pass the prefix with \(K=t\);
- suffix \(k\): pass the sequence with \(K=k\);
- component posterior: sum the corresponding 144 coordinates.

This avoids a new production filter and avoids needing log evidence for the primary entropy estimator.

Cross-check:

- all 36 one-symbol histories;
- all 1,296 two-symbol histories;
- fixed random and structured histories through length 33 against `BayesFilter`;
- component-wise likelihood reconstruction on the validation subset;
- selected long histories against an independent high-precision forward calculation.

The long-history reference may iterate over the five nonzero transitions per state, using unnormalized Decimal arithmetic. Its sparse implementation is justified as an independent numerical reference and must first agree with the existing dense Decimal reference on short cases.

Use at least 80 digits and repeat the reference at 120 digits. Include fixed structured histories, ordinary sampled histories and sampled extreme-posterior histories under a selection rule written before sampling.

Required tolerances:

| Check | Maximum discrepancy |
|---|---:|
| Distribution sums and stationarity | \(10^{-12}\) |
| Float posterior against reference, maximum coordinate error | \(10^{-10}\) |
| Component posterior against reference | \(10^{-9}\) |
| Entropy against reference | \(10^{-8}\) bits |
| Exact short MI numerical enclosure | Width \(10^{-10}\) bits |

An 80/120-digit agreement alone is not a universal floating-point error proof. Combine it with explicit construction-tail bounds, arithmetic error checks and cross-implementation comparisons. Carry a conservative \(10^{-6}\)-bit numerical allowance into the reported information bounds.

Do not label float64 filtering exact arithmetic. It is exact Bayesian inference evaluated numerically.

### 8.2 Regression checks

Before the scientific run, execute the relevant unchanged world, process, oracle and oracle-profile tests, plus new Stage 0 tests covering:

- both torus seams and state ordering;
- absence of inter-component transitions;
- emit-first alignment;
- correct stationary suffix restart;
- block-sum component posterior;
- marginal equality;
- non-P and pair-law witnesses;
- long-history reference agreement;
- null identities;
- deterministic PH scale selection and verdict logic.

Keep frozen historical modules and registry entries unchanged.

## 9. Six-field reuse assessment

| Required field | Assessment |
|---|---|
| **Existing functions and artifacts** | Reuse `QuotientLatticeBuilder`, `Identification`, `CubicalComplex`, `TransitionBuilder`, `HMMSampler`, configurable `SequenceLayout`, long-window `suffix_posterior`, `BayesFilter`, `LastSymbolPosterior`, `FutureOperator`, Hellinger distances, `PersistenceComputer`, `Summaries`, `NullClouds`, `SeedTree`, and the independent Decimal reference. Reuse D-1’s local unregistered-world and explicit-array pattern. |
| **Genuinely missing capability** | This torus-pair configuration, wrapped Gaussian array construction, the local blur, component-information reporting, the fixed PH calibration and experiment-specific orchestration. Existing point-to-center geometry does not supply both periodic axes. |
| **Smallest change** | Add a small experiment-local package and tests. Build one local torus; assemble explicit joint arrays; call existing sampler, suffix oracle and PH utilities. Add only the independent sparse high-precision reference needed for practical long-history verification. |
| **Stable interfaces and invariants** | Row-vector \(T\), emission array \(E\), stationary prior \(\pi\), emit-first ordering, common public symbols, full 288-coordinate beliefs, separate latent labels, deterministic seeds and unchanged historical APIs. |
| **Relevant regression checks** | Existing world/process/oracle/oracle-profile suites, plus the focused checks in §8.2. Preserve registry hygiene, file-size checks and old frozen results. |
| **Next plausible extension** | A separately authorized trained-model comparison at a supported context length. The explicit \(T,E,\pi\) interface also permits a future alternative smooth deformation without a generic extension framework. |

Use multiple clearly scoped files if needed; do not reproduce D-1’s initial single-module size blockage. No broad refactor is required.

## 10. Cost and resource policy

The proposed run is CPU-only, one thread, with no CPU-time ceiling.

Set numerical-library thread counts to one and meter total process-tree CPU, including PH workers. Follow the owner’s disk thresholds and memory limit; target less than 2 GiB working memory and remain below the authorized 12 GiB ceiling.

Use batches of approximately 256 histories and retain only required posterior outputs.

For the unchanged dense suffix oracle, the information cohort over the logarithmic prefix grid requires approximately

\[
16{,}384\times1{,}023\times288^2
\approx1.4\times10^{12}
\]

multiply-accumulates, plus suffix, sampling and validation work.

The PH design entails roughly a few hundred calls, mostly on 144-, 256- or 512-point clouds.

Forecast:

| Work | Estimated one-thread CPU |
|---|---:|
| Construction, references and regression checks | 15–60 minutes |
| Sampling and information calculations | 45–180 minutes |
| PH panels, references and controls | 30–120 minutes |
| **Total planning estimate** | **2–6 CPU-hours** |

These are unbenchmarked estimates, not promises or stopping limits. Report actual CPU and peak memory. A library timeout makes the required result incomplete; it never becomes a passing censored bar.

Do not inherit D-1’s historical CPU ceiling or the older K4 cap.

## 11. Required outputs

The executing implementation should produce:

- frozen configuration, hashes, seeds and environment manifest;
- explicit \(T,E_A,E_B,E,\pi\) arrays with construction-error certificates;
- structural and numerical verification reports;
- exact one- and two-symbol information results and pair-law witness;
- entropy and concentration curves with simultaneous intervals;
- the table \(I_1,I_2,I_4,I_8,I_{\rm full}(32),I_{\rm full}(512),G_8\);
- all PH diagrams, reference-band derivation, H0 gap values and panel outcomes;
- every null result;
- stage verdict, individual gate decisions, CPU ledger and limitations.

Artifacts and scientific stores belong on X:. Preserve failed and inconclusive outputs. Do not access unrelated model checkpoints, payloads or existing training histories.

## 12. Licence and limits

A successful Stage 0 licenses the following statement:

> For this fixed torus pair, one symbol contains no component information, eight-symbol windows contain at most the preregistered amount, and histories through 512 observations provide substantially more. At the calibrated resolution, complete exact-belief clouds display two separated components with two persistent H1 classes each.

It does not establish:

- learning or representation geometry in any model;
- functional or causal use of component identity;
- that a next-symbol objective forces a particular representation;
- an exact topological characterization of the entire reachable belief space;
- the world’s H2 in belief space;
- long-history dependence of every within-component coordinate;
- a general positive or negative result for other emission deformations;
- any revision to E0–E4, K4, K8, X4-F, B2 or H5.

The two worlds have the same topology. The experiment tests history-dependent identification of a component in a disjoint union, alongside recovery of each component’s toroidal signature.

A STOP is scoped to this candidate, horizon, estimator and resolution. Asymptotic sequence distinguishability does not guarantee the finite-horizon information or topology gates.

## Open questions

No scientific parameter choice remains open for this proposed candidate.

Before execution, the coordinator must complete merge, independent result-blind review, execution-commit and environment bindings, and the freeze record. Any later training study requires a separate protocol and authorization.