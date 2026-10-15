STATUS: FREEZE_READY

The revised C1 design below resolves the seven listed specification gaps. It fixes the nonlinear probe, defines measured information-damage matching, makes eligibility oracle-only, separates intended semantic changes from damage, specifies one paired ratio endpoint and its precision gate, and binds seeds, charts, checkpoints and panels.

FREEZE_READY means ready for the required independent, result-blind design review. It does not mean frozen, empirically feasible or authorized for execution.

This revision explicitly changes the draft’s target population to a prespecified, oracle-compatible subset. It also replaces the proposed “every state below the calibration 99th percentile” support rule, which would reject part of its own calibration reference by construction.

No files, operational records or Git state were written. The new commit and response SHA must be created by the coordinator after the CLI saves this deliverable; none is claimed here.

# C1: phase-associated centroid state forcing

**Document identity:** `C1-FREEZE-READINESS-v1`, planning request `coord-c1-freeze-readiness-20261014`.

**Authority:** `agent-handoff/archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md`, SHA256 `13160D21CA0F52BEC04CCC9AA73BBE4016842C8A108E32994656F57E5B4E69CA`; `NEXT_RESEARCH_AND_WORKFLOW.md`, section “Owner research charter”; and `planning/PLANNING_PROTOCOL.md`.

**Inputs verified by read-only inspection:**

| Input | Identity |
|---|---|
| Planning request | SHA256 `8761AAF0A55AB9F29D2D929347483EF17E82ED6623F3B9D6E048700F03A2AF8F` |
| Previous planning response | SHA256 `1E101BB62B1A06BB77448BE66BAEAE8656C10397265DBCABBAC1806B21AEBC81` |
| C1 draft | Commit `fc2c1079cfeed32a50f22e13d9aba51bdad6db5a`; SHA256 `1926F39E4C6678E349C30A8815681CAB0C17C315C268F259D4C214BE50134DC0` |
| Inspected research checkout | HEAD `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c` |
| Inspected charter document | SHA256 `2B1BE9E77497ECFF04C90500F90AAB045FEFA4BA5F311F1E7736C83F61C3FD3C` |

These are source identities, not a new freeze or execution release. The coordinator must bind the eventual implementation commit, environment and generated artifacts separately.

## 1. Scientific question and scope

**Question:** At `resid_post_3`, position 32, does movement along a fitted phase-associated centroid curve give lower regret against a specified counterfactual oracle prediction than a fixed randomized direction family matched on displacement and measured recoverability damage?

The competing explanations are:

1. The centroid direction carries a prediction-relevant semantic association.
2. The observed response follows generic displacement, degradation of other information, or unsupported activation states.

The experiment discriminates between these explanations within its measured gates. It does not control every possible nuisance.

Use the original three cylinder-O E4 models, seeds **1729, 2718 and 3141**, step **5000**, the **12 × 12** world, original lazy transition, **36** overlap emissions, and original symbol permutations. No model training, checkpoint selection, site search or alternative intervention is included.

At this final residual site, the experiment tests how the trained downstream readout responds to the forced component. It does not identify how earlier blocks computed that component.

The accepted X4-F conclusion remains **INCONCLUSIVE/FAMILY_UNMATCHED, causal endpoint NOT_RUN**. C1 is a new protocol, not a rescue or reinterpretation of X4-F. E4 G-H FAIL, B2/D-055 NO-GO, K8 FAIL and H5 REJECTED retain their recorded scopes.

## 2. Source histories, donor construction and exact oracle

Let the public source prefix be

\[
H=(w_1,\ldots,w_{32}).
\]

Convert named symbols to canonical symbols using the verified inverse permutation. For canonical symbol \(j=6a+b\), construct \(H'\) by:

\[
6a+b\longmapsto6((a+1)\bmod6)+b
\]

at positions **1–31**, retaining position **32 exactly**. Convert the resulting prefix to each model’s named symbols using its original permutation.

No observed \(w_{33}\) or latent sidecar is an analysis input.

Compute full-prefix posteriors independently:

\[
b_S=P(z_{32}\mid H),\qquad b_D=P(z_{32}\mid H').
\]

The oracle next-symbol targets are

\[
q_S=b_STE,\qquad q_D=b_DTE.
\]

There is exactly **one transition after the final posterior**, followed by emission. Recompute \(b_D\) from \(H'\); do not rotate \(b_S\) and call that the donor posterior. Keeping \(w_{32}\) fixed breaks that shortcut.

Use the existing `BayesFilter` and `oracle_profile.suffix_posterior(..., K=32)`, with the existing independent Decimal reference. Verify their agreement, canonical ordering, prior, likelihood calculation and indexing before model work.

The scientific oracle is the documented normalized likelihood calculation using the frozen stored process weights, as independently referenced. Report its relationship to the documented ideal process and actual sampler threshold law separately, following K4’s operational-versus-ideal distinction. Do not silently replace it with a different process or claim the PRNG produces mathematically independent ideal uniforms.

### Oracle features

For posterior \(b\), save:

- the complete 144-state posterior;
- 12-state \(x\)- and \(y\)-marginals;
- \(h_k(b)=E_b[\exp(2\pi ikx/12)]\), for \(k=1,2,3\);
- radii \(|h_k(b)|\);
- normalized \(y\)-mean and second moment;
- the last public symbol.

The complete posterior prevents first-harmonic agreement from concealing changes in higher harmonics or \(x\)-\(y\) dependence.

## 3. Oracle-only eligibility and population

Eligibility is fixed before calibration and depends only on public prefixes and their oracle calculations. It never depends on a model activation, chart success, patch output or regret.

Define

\[
\delta_O=\operatorname{wrap}(\arg h_1(b_D)-\arg h_1(b_S))
\in(-\pi,\pi].
\]

Define \(R_\delta b\) as circular transport in \(x\), retaining \(y\): for \(t=12\delta/(2\pi)\), \(m=\lfloor t\rfloor\), \(\eta=t-m\), use the convex mixture of circular shifts by \(m\) and \(m+1\), with weights \(1-\eta,\eta\).

A source row is eligible only if all of the following are certified:

1. Both full prefixes have positive likelihood.
2. Mean per-symbol surprise is at most **8 nats** for each prefix.
3. Donor final-symbol surprise, computed from its prefix through position 31, is at most **10 nats**.
4. \(|\log P(H')-\log P(H)|\le5\).
5. Both first-harmonic radii are at least **0.05**.
6. \(\pi/12\le|\delta_O|\le5\pi/6\).
7. \(g=KL(q_D\|q_S)>10^{-4}\) nats.
8. \(TV(b_D,R_{\delta_O}b_S)\le0.10\).
9. \(TV(b_D^y,b_S^y)\le0.02\).

Apply inequalities to certified enclosures in the conservative direction. A boundary that cannot be certified is ineligible, with its reason recorded.

Items 8–9 are the **counterfactual compatibility restriction**: the actual same-last-symbol donor must approximately resemble a phase transport while producing little change in the declared vertical nuisance. They are design assumptions, not established properties of the existing process.

The estimand concerns naturally generated source prefixes **conditional on this eligibility rule**, with the fixed donor transformation. It is not an all-history effect.

### Fixed cohorts and coverage

Generate one fixed candidate cohort for each split:

| Split | Candidate trajectories | Required eligible trajectories |
|---|---:|---:|
| Calibration | 8192 | 4096 |
| Validation | 4096 | 2048 |
| Fresh test | 8192 | 4096 |

Select the first required number of eligible rows in ascending candidate sequence order. Require at least **50%** eligible coverage in each candidate cohort. There is no replenishment, enlarged candidate pool or second seed.

Split the selected calibration rows into:

- **CAL-FIT:** first 3072 rows;
- **CAL-AUDIT:** remaining 1024 rows.

Every selected row must subsequently pass the model-specific assay gates. There is no model-based trimming, replacement or complete-case endpoint.

Insufficient eligibility or coverage produces **INCONCLUSIVE/COUNTERFACTUAL_UNSUPPORTED** before model intervention scoring.

## 4. Chart identity and frozen centroid intervention

### Chart selection

Choose the chart branch at the written-contract freeze, using only recorded artifact availability and chart-stage acceptance:

- **Reuse branch:** Reuse K4’s saved chart and gauge for each original model if they exist, have accepted chart/lift/gauge/extension evidence, and match the checkpoint, hook, position, landmark identities and method. K4 need not pass its separate history-headroom endpoint for an independently accepted chart artifact to be reusable.
- **Construction branch:** If such artifacts are absent, fit exactly the existing K4 chart method on the first **512 CAL-FIT** source activations, ordered by ascending history ID.

Record the branch and artifact identities before C1 feasibility calculations. Do not switch branches after a C1 gate failure.

The construction branch uses `chart.fit_chart`, `fit_gauge`, `extend`, serialization and the K4 cochain kernels unchanged: field **47**, largest positive finite H1 lifetime with existing tie-breaking, midpoint radius, exact integer lift and primitive class, existing smoothing and eight-neighbour extension. Retain the existing algorithmic lift termination settings; they are not an overall CPU allocation.

The gauge uses only the calibration landmarks and their full-prefix oracle first harmonic. No validation/test regret enters chart fitting or orientation.

For a newly constructed chart, fit one diagnostic chart on the first 512 CAL-AUDIT source activations using the same recipe. Require phase agreement at least **0.80**. This diagnostic chart does not replace the frozen intervention chart.

On CAL-AUDIT and validation, require the existing extension support rule, at least **8** source rows in every one of 12 phase bins, and overall source phase resultant at most **0.30**.

No oracle-angle decoder may substitute for a failed learned chart.

### Nuisance adjustment and centroid curve

On CAL-FIT source activations only, fit

\[
L(v)=\text{affine ridge}(v\rightarrow a),
\]

where \(v\) comprises 36 last-symbol indicators and the normalized oracle \(y\)-mean and second moment. Standardize the two continuous covariates on CAL-FIT. Use ridge coefficient **\(10^{-4}\)** and an unpenalized intercept; no hyperparameter selection.

Bin \(a-L(v)\) into **12** equally spaced half-open circular bins. Require at least **32 CAL-FIT source rows per bin**. Save the bin means and obtain \(\mu(\phi)\) by periodic linear interpolation between bin centres.

For source and actual donor activations, obtain \(\phi_S,\phi_D\) through the same saved chart and gauge. Force

\[
a_T=a_S+\mu(\phi_D)-\mu(\phi_S).
\]

Patch only `resid_post_3`, index **32**, in input `[BOS,w1,…,w32]`. Preserve other positions and the recipient prefix. Weights, buffers and evaluation mode remain frozen.

Identity and zero-displacement patches must reproduce the unpatched execution within the existing patch implementation’s verified numerical tolerance. Full donor-state replacement is an engineering check on calibration only; it is excluded from the scientific endpoint.

This is **phase-associated centroid forcing**, not first-harmonic-only forcing or complete semantic isolation.

## 5. Exact nonlinear probe family

Use one fixed nonlinear family for every manipulation, recoverability and nuisance assessment:

**2048-feature Gaussian random-Fourier-feature affine ridge regression.**

For each model:

1. Fit the existing activation standardizer on **unpatched CAL-FIT source activations**, using its existing treatment of columns with standard deviation at most \(10^{-12}\).
2. Fix bandwidth \(\ell=\sqrt{128}\).
3. Generate
   \[
   \Omega\sim N(0,1)^{128\times2048}/\ell,\quad
   \beta\sim U[0,2\pi)^{2048}
   \]
   using the seed map below.
4. Use the existing feature function
   \[
   f(a)=\sqrt{2/2048}\cos(\operatorname{standardize}(a)\Omega+\beta).
   \]
5. Fit affine ridge with coefficient **1.0**, unpenalized intercept, and a **singleton lambda grid**.

Capacity is **2049 coefficients per output**. Standardization, frequencies, phases, bandwidth and lambda are shared across unpatched, primary and all control conditions for that model.

Reuse `standardizer`, `rbf_map`, `rbf_features` and `RidgeProbe` unchanged. Do not use the old X4-F nested-selection orchestration. There is no model, bandwidth, feature-count or lambda selection. A singleton grid cannot choose a configuration from audit performance.

Fit multioutput blocks for:

- complete posterior;
- \(x\)- and \(y\)-marginals;
- first, second and third harmonic real/imaginary coordinates;
- their radii;
- chart unit vector;
- last-symbol one-hot labels.

Last-symbol predictions use argmax, with ties resolved by lowest canonical symbol index. Probability projections, clipping and post-hoc calibration are excluded.

### Two distinct uses

- **Frozen semantic probe \(P_0\):** Fit on unpatched CAL-FIT source activations and source targets. Freeze it before patches are assessed. Use it to measure intended state movement.
- **Recoverability probes \(P_A\):** For each intervention condition \(A\), refit coefficients on that condition’s patched CAL-FIT activations to predict the **original source targets**. Freeze all coefficients before validation.

This distinction prevents a frozen decoder’s response to intended semantic movement from being mislabeled as lost source recoverability.

### Probe adequacy

For continuous block \(B\), let

\[
v_B=E_{\mathrm{CAL-FIT}}\|t_B-\bar t_B\|^2.
\]

Use denominator \(v_B\) when \(v_B>10^{-6}\); otherwise classify the block as nearly constant and use its declared squared natural norm bound: **1** for posterior/marginal/chart blocks and **3** for grouped three-harmonic or three-radius blocks.

Report both normalized and raw losses. Nearly constant blocks do not support claims about recovering their variation.

Require unpatched held-out normalized MSE at most **0.20** for each nonconstant block, raw normalized loss at most **\(10^{-4}\)** for nearly constant blocks, and last-symbol accuracy at least **0.90**, on CAL-AUDIT and validation.

A failed adequacy gate means **INCONCLUSIVE/PROBE_INADEQUATE**. It does not authorize a larger probe or a new feature seed.

## 6. Randomized controls and information-damage matching

For each source row, let

\[
d=\operatorname{wrap}(\phi_D-\phi_S).
\]

For each of the **32** fixed fields, request

\[
\phi_{C_r}=\phi_S+\epsilon_r(H)|d|,\qquad \epsilon_r(H)\in\{-1,+1\}.
\]

Construct its raw displacement through the same curve,

\[
\Delta^0_{C_r}=\mu(\phi_{C_r})-\mu(\phi_S),
\]

then scale it to the primary displacement norm:

\[
\Delta_{C_r}
=\Delta^0_{C_r}
\frac{\|\Delta_T\|_2}{\|\Delta^0_{C_r}\|_2},\qquad
a_{C_r}=a_S+\Delta_{C_r}.
\]

An exactly zero primary displacement requires zero controls. An exactly zero raw control with nonzero primary is unmatched. Tiny nonzero values are not converted to zero.

There are only **two destinations per row**. Approximately half the signs reproduce the primary direction; those coincidences remain in the family and are reported. The family is a fixed mixture of the intended direction and its reflection, not 32 distinct semantic alternatives.

No field rejection, regeneration or increased draw count is allowed.

### Geometric matching

Require on CAL-AUDIT and validation, for every model and field:

- raw Euclidean norm agreement within relative error **\(10^{-8}\)**;
- calibration-whitened norm mismatch at most **5% per row**;
- centred displacement covariance trace mismatch at most **5%**;
- mean squared decoded first-harmonic displacement mismatch at most **5%**;
- variance of that decoded displacement mismatch at most **10%**.

Whitening uses the fixed CAL-FIT covariance regularization specified in section 7.

For an exactly zero reference aggregate, the corresponding control aggregate must also be exactly zero; do not add a denominator floor.

### Information-damage metric

On held-out split \(S\), define

\[
L_B^A(S)=
\frac{E_S\|P_A(a_A)_B-t_{S,B}\|^2}{s_B},
\]

where \(s_B\) is the calibration denominator above and \(t_{S,B}\) is the **original source target**.

Define measured damage

\[
D_B^A(S)=L_B^A(S)-L_B^0(S).
\]

For **every continuous block and every field**, require

\[
|D_B^T(S)-D_B^{C_r}(S)|\le0.02.
\]

For last-symbol accuracy damage, use the difference between unpatched and post-refit accuracy and require primary-control mismatch at most **0.02**.

Additionally:

- \(y\)-marginal recoverability degradation must be at most **0.05** for primary and every control;
- last-symbol accuracy degradation must be at most **0.02** for each condition.

Report absolute source recoverability and damage for all blocks, including the phase-associated blocks. Do not require source phase information to remain unchanged: changing that component is part of the intervention.

These are **empirical matching tolerances on the fixed held-out assay**, not mutual-information estimates or proofs that all information damage is equal.

### Intended changes versus damage

Define primary semantic targets from the **actual donor** posterior and donor chart phase.

For a control, define a diagnostic semantic template

\[
b_{C_r}^{*}=R_{\epsilon_r|\delta_O|}b_S
\]

and its associated moments and marginals. Its chart target is the requested control phase. This transported posterior is a diagnostic template, not a claim that a particular public counterfactual prefix realizes it.

Use \(P_0\) to compare decoded signed changes with these independently prescribed changes:

\[
e_{A,B}=
[P_0(a_A)_B-P_0(a_S)_B]
-[t^*_{A,B}-t_{S,B}].
\]

Require mean squared signed-change error divided by \(s_B\) at most **0.20** for each continuous block. For the \(y\)-marginal, also require

\[
\|\operatorname{mean}e_{A,y}\|/\sqrt{s_y}\le0.10.
\]

For chart and oracle first-harmonic angles, require mean target error at most **\(\pi/12\)** and 95th-percentile error at most **\(\pi/6\)**. If a decoded vector has magnitude below **0.20**, its angle is unresolved and the gate fails.

Require the chart’s source-to-donor angular change to agree with \(\delta_O\) within **\(\pi/12\) per row**.

Thus:

- donor-defined radius, harmonic and small vertical changes are assessed as intended movement;
- error relative to those signed changes is a fidelity failure;
- loss of ability to recover original source labels after refitting is measured damage.

Equal damage alone cannot establish intended state forcing.

### Early-stop rule

Complete adequacy, manipulation, geometry, damage and support gates **before validation regret is used for precision**.

The first nonpassing gate ends feasibility:

- damage/geometric mismatch → **INCONCLUSIVE/FAMILY_UNMATCHED**;
- failed semantic movement → **INCONCLUSIVE/MANIPULATION_INVALID**;
- unsupported states → **INCONCLUSIVE/SUPPORT_FAILED**;
- invalid numerics or integrity → **FAIL_TECHNICAL**.

Retain the failed values. Do not relax tolerances after seeing them.

## 7. Activation support and counterfactual alignment

Oracle eligibility addresses compatibility and prefix plausibility. Activation support supplies a separate model-specific check.

Fit a support reference on unpatched CAL-FIT source **and actual donor** activations:

\[
\Sigma=.99S+.01\,\operatorname{tr}(S)I/128,
\]

where \(S\) is their population covariance. Nonpositive trace or an unresolved factorization stops the assay.

Freeze

\[
\tau=1.25\max_{\mathrm{CAL-FIT\ reference}}
(a-\bar a)^T\Sigma^{-1}(a-\bar a).
\]

Require every selected source, donor, primary and control state on CAL-AUDIT, validation and fresh test to satisfy:

1. the saved K4 chart’s extension support rule; and
2. Mahalanobis score at most \(\tau\).

The same fixed covariance also defines whitened displacement norms.

This replaces the draft’s all-row 99th-percentile rule. A 99th-percentile threshold cannot place every calibration reference row inside support except in degenerate cases.

The support threshold is a declared empirical envelope, not proof of membership in the natural activation manifold. Likewise, oracle positivity does not establish plausibility. Primary semantic alignment must pass the actual-donor checks in section 6.

Unsupported selected rows stop the cohort. They are not discarded.

## 8. Single endpoint and exact interpretation

For row \(i\), model \(j\) and condition \(A\), define counterfactual regret

\[
R_{ij}^{A}=KL(q_{D,i}\|p_{ij}^{A}).
\]

The sole primary endpoint uses

\[
Y_{ij}
=[R_{ij}^{S}-R_{ij}^{T}]
-\frac1{32}\sum_r[R_{ij}^{S}-R_{ij}^{C_r}]
=\frac1{32}\sum_rR_{ij}^{C_r}-R_{ij}^{T}.
\]

Normalize by oracle directional margin:

\[
\theta_j=
\frac{E[Y_{ij}]}{E[g_i]},
\qquad
g_i=KL(q_{D,i}\|q_{S,i}).
\]

Use the **ratio of means**, not the mean of rowwise ratios.

With verified canonical process equality, \(g_i\) is shared across models. Verify this identity rather than assuming it.

The baseline cancels. Therefore \(\theta_j>0\) does **not** establish improvement over the unpatched prediction. Report \(E[R^S-R^T]\), absolute regrets, coincidence rates and control dispersion as descriptive secondary quantities, without additional scientific pass/fail rules.

Use exact expectation under \(q_D\); no sampled next symbol is required.

### Numerical certification

Use finite logits and stable log-softmax. Do not probability-floor, clip or replace nonfinite logits.

Reuse the independent posterior reference and K4 trapping/enclosure machinery. Add a separately tested extension for future probabilities, logarithms and regret differences. Its written mathematical contract must:

- enclose posterior and future arithmetic;
- treat finite recorded logits as the operational model output;
- enclose log-softmax and oracle log terms;
- exploit entropy cancellation when calculating \(Y\);
- propagate row bounds through paired means and ratios.

Use fixed **80-digit Decimal** reference arithmetic for added log/future calculations, with directed enclosures and the existing exceptional-condition traps. Independent test authors must verify the analytical bounds before production.

Required certificate limits:

- oracle predictive-vector \(L^1\) enclosure width at most **\(10^{-10}\)**;
- mean \(G\) enclosure width at most **\(10^{-8}\)** nats;
- each \(Y\) enclosure width at most **\(10^{-6}\)** nats;
- numerical width of each point or bootstrap ratio at most **0.001**.

Reference disagreement is **FAIL_TECHNICAL**; valid but insufficiently narrow certificates are **INCONCLUSIVE/NUMERICAL_PRECISION**. Do not increase precision or change algorithms after fresh exposure.

## 9. Ratio inference, precision gate and decision rule

### Fixed ratio inference

Use **5000 paired whole-source-trajectory bootstrap draws**, shared across all three models and retaining the donor, all 32 controls, numerator and denominator together.

For each draw,

\[
\theta_j^{*(b)}
=\frac{\bar Y_j^{*(b)}}{\bar g^{*(b)}}.
\]

Do not resample controls or models separately. Charts, probes, centroid maps and control functions remain fixed.

Let

\[
\alpha=\frac{0.05}{6}.
\]

Use `inverted_cdf` quantiles:

\[
L_j=Q_\alpha(\theta_j^*),\qquad
U_j=Q_{1-\alpha}(\theta_j^*).
\]

Use the lower ratio enclosures for \(L_j\) and upper enclosures for \(U_j\). Report central 95% intervals separately.

This is a prespecified bootstrap approximation, not an exact finite-sample confidence theorem. The positive-margin eligibility rule prevents zero bootstrap denominators; the headroom gate guards against a weak average denominator.

### Oracle headroom gate

Before activation extraction, require the numerical-adjusted one-sided 95% paired-bootstrap lower bound of \(G=E[g]\) to be **strictly greater than 0.005 nats**, on both selected calibration and validation cohorts.

Failure yields **INCONCLUSIVE/NO_HEADROOM**. K4’s different headroom calculation does not substitute for this gate.

### Validation-only precision

Lock fresh \(N=4096\), practical margin **0.10**, design alternative **0.20**, and required **joint power 0.80**.

After all validation assay gates pass:

1. Compute \(\hat\theta_{V,j}=\bar Y_{V,j}/\bar g_V\).
2. Generate 5000 paired validation resamples of size **4096**.
3. Calculate
   \[
   e_{bj}=
   \frac{\bar Y^{*(b)}_{V,j}}{\bar g_V^{*(b)}}-\hat\theta_{V,j}.
   \]
4. Set \(q_j=Q_\alpha(e_{\cdot j})\).
5. Count projected joint successes:
   \[
   \forall j:\quad 0.20+e_{bj}+q_j>0.10.
   \]
6. Require the exact one-sided **95% Clopper–Pearson lower bound** for the success fraction to be at least **0.80**.

Also calculate the ratio influence variable

\[
Z_{ij}=
\frac{Y_{ij}-\hat\theta_{V,j}g_i}{\bar g_V}.
\]

Use a separate 5000-draw paired validation bootstrap of validation size to obtain the 95th-percentile SD estimate \(s_{U,j}\). Require, for every model,

\[
0.10+
[z_{1-\alpha}+z_{0.80}]
\frac{s_{U,j}}{\sqrt{4096}}
\le0.20.
\]

Both the joint projected-power and influence-SD checks must pass. This fixes the ratio precision method; K4’s mean-only precision function is not used as a substitute.

The power projection is conditional on the observed validation distribution and fixed fitted assay. It is not guaranteed power under every population with \(\theta=0.20\).

Insufficient precision yields **INCONCLUSIVE/UNDERPOWERED**. There is no sample-size increase or alternative endpoint.

### Fresh decision

After all fresh validity gates pass:

- **PASS:** \(L_j>0.10\) for **every** original model.
- **FAIL:** \(U_j<0.10\) for **at least one** original model.
- **INCONCLUSIVE:** every other valid combination, including equality at 0.10.

A validity failure takes precedence and cannot become scientific FAIL.

**PASS licenses:** support for a practical relative directional regret advantage of this fixed centroid intervention over its fixed matched sign family, on the prespecified eligible population.

**FAIL licenses:** scoped lack of support for a margin above 0.10 in at least one original model, under a valid assay. It rejects the all-three-model practical-margin claim.

**Neither licenses:** topology/H1 necessity, complete erasure, a literal internal circle variable, improvement over unpatched prediction, absence of causal use, universal sufficiency, long-memory necessity, other sites/checkpoints/horizons, or generalization to natural-language models.

Fresh validity gates may prevent a conclusion but may not tune it. Report bootstrap bounds as the prespecified unconditional procedure; do not claim selective confidence coverage conditional on passing fresh gates.

## 10. Seeds, identities and genuinely fresh histories

### Seed map

Use existing `SeedTree` derivation and PCG64. Record derived seeds and scopes in the artifact seed map.

| Purpose | Fixed rule |
|---|---|
| Candidate sampling | `SeedTree(520100).generator("C1","data",split,"cylinder","O","1.25")`, with split `calibration`, `validation`, or `fresh` |
| Nonlinear features | `SeedTree(520100).generator("C1","probe",model_id)` |
| Control field \(r\) | Master seed `520200+r`, for \(r=1..32\); `generator("C1","sign",canonical_history_digest)`; one binary draw |
| Oracle headroom bootstrap | `SeedTree(520100).generator("C1","headroom",split)` |
| Validation influence-SD bootstrap | PCG64 **520301** |
| Validation projected-ratio bootstrap | PCG64 **520302** |
| Fresh endpoint bootstrap | PCG64 **520303** |

Each control sign is a fixed function of its seed and canonical history digest. It is shared across models and does not inspect the requested semantic direction. This also avoids treating a row-position sign schedule as an exchangeable conditional control law.

Sampling uses one fixed sampler call per candidate cohort with the stated count. Sampling draw order and runtime versions are frozen. No global RNG, omitted seed, alternate stream or restarted cohort is allowed.

### Existing identities

Bind the following recorded IDs; verify metadata and payload hashes under the later execution release:

| Model | Checkpoint | Original ObservationSet | Original HistoryIndex | Original ActivationSet | EmissionSpec |
|---|---|---|---|---|---|
| 1729 | `c3358e3cb9c352fb` | `2a67b2c947e293ba` | `afb6e7120c9477b1` | `0e001559534ee7ef` | `3633ac27dab50cf4` |
| 2718 | `98b0e703a337d513` | `95c4d118517ecd92` | `908cb61ffbd956c6` | `ec17425cf67f1a54` | `97838b9e13a26f74` |
| 3141 | `036b670743ffbbaf` | `2e2cf22bb4820155` | `7e7d27bd143ebeb5` | `069da84ce363d8f2` | `8c29c329c197c79e` |

Shared WorldSpec: **`21feee1d8ee5422e`**.  
Shared TransitionSpec: **`e4dafc7b9785c172`**.

These old datasets are exposed assets, not fresh test data.

Create distinct C1 source and donor observation/history/activation artifacts. Their identities must bind:

- split, candidate ordinal and selected ordinal;
- source and donor canonical 32-token digests;
- model-specific named token digests;
- explicit source-to-donor pairing;
- panel number and immutable ordered row tables;
- checkpoint, emission, world and transition parents;
- hook, position, model configuration and payload hashes;
- seeds, chart/gauge, centroid, standardizer and probe hashes;
- control rule, implementation commit, dependency and numerical environment identities.

Use ascending history ID for landmark ordering and ascending shared sequence ID for evaluation. Cross-model joins require identical canonical prefixes and donor digests. A mismatch stops; there is no unpaired fallback.

Assign C1 panels of 512 selected rows: calibration panels 1–8, validation panels 1–4 and fresh panels 1–8, under **distinct C1 split identities**.

### Freshness

Before test release, freeze a hash-based exposure registry covering previously consumed training, development, test, diagnostic and planning-feasibility 32-symbol histories, including relevant constructed donors.

Every selected fresh source **and donor** must be absent from that registry and from C1 calibration/validation histories. Different seeds alone do not establish freshness.

Candidate source/donor collisions and novelty exclusions are deterministic identity exclusions, recorded before endpoint access. They do not authorize replenishment; the fixed cohort must still supply 4096 eligible, novel pairs. An incomplete exposure registry blocks the test release.

The existing sampler may generate its normal 33-observation output and latent state array. Analysis consumers receive only the first 32 public symbols; future-token and latent payloads remain sealed.

Fresh histories are generated only after method, implementation and feasibility acceptance. No fresh diagnostic panel is exposed in advance.

## 11. Six-field reuse assessment

### 1. Existing functions and artifacts

Reuse unchanged:

- E4 model architecture and the three fixed checkpoints.
- `dataset.HMMSampler` and existing dataset/contracts/artifact storage.
- `contracts.SeedTree`, token hashing and identity machinery.
- `oracle.BayesFilter`, `FutureOperator` where applicable, and `tools/x4_oracle_profile/oracle_profile.py`.
- `tests/oracle_profile/independent_reference.py`.
- `activations.ActivationExtractor`, explicitly on CPU, and `learner.forward_with_patch`.
- `analysis.x4f_scores.standardizer`, `rbf_map`, `rbf_features`, and `prediction.RidgeProbe`.
- K4 `chart.py`, `cochain.py`, chart serialization, canonical conversion, history digests and cross-model join kernels.
- K4 posterior envelopes, trapping contexts, exact circular features and compatible reference-cache utilities.
- `tools/x4_oracle_profile/{meter,controls,winjob}.py`: descendant CPU accounting, ledger finalization, emergency charges, ownership locks and usage/STOP/HOLD behavior.
- K4 `op_guard.py`; compatible disk checks, stage-spent accounting, environment identity and immutable record helpers.

Reuse accepted oracle caches only for exact matching process/prefix/reference identities. Never reclassify old exposed test panels as fresh.

### 2. Genuinely missing capability

Missing capabilities are:

- deterministic same-last-symbol donor and oracle eligibility tables;
- saved nuisance-adjusted nonlinear centroid forcing;
- fixed semantic-versus-damage assay orchestration;
- paired counterfactual regret ratio, its certificates and precision projection;
- a C1 release/binding layer for fresh data and uncapped CPU policy.

### 3. Smallest change

Add a small C1 experiment package containing:

1. pure counterfactual/eligibility kernels;
2. centroid fit, interpolation and sign-control kernels;
3. probe/gate orchestration using existing estimators;
4. paired ratio/precision kernels and the certificate extension;
5. a thin staged adapter and resource/release binding.

No new sampler, model, oracle filter, activation extractor, patch engine, generic causal framework or independent supervision service is needed.

The existing K4 adapters and runner contain assumptions about original E4 panels and K4 stages. Reuse their public kernels and record mechanisms; add a versioned C1 adapter/stage binding rather than pretending those hardcoded interfaces accept new cohorts unchanged.

### 4. Stable interfaces and invariants

Pure mechanisms take arrays, immutable configuration and injected guards/timers. Keep generation, oracle computation, extraction, fitting, patching, diagnostics and inference separate.

Preserve fixed site/checkpoints, same-last-symbol donors, calibration-only coefficients, canonical joins, sealed future/latent data, immutable artifacts, explicit releases and first-failed-gate termination.

### 5. Relevant regression checks

Independent tests must cover:

- asymmetric HMM indexing and full-prefix donor inference;
- canonical/named permutation roundtrips;
- eligibility, likelihood and exact boundary handling;
- fractional circular transport, wrap and higher-harmonic changes;
- periodic centroid interpolation and empty bins;
- identity patches and frozen weights;
- random-sign independence and retained coincidences;
- norm matching with deliberately unequal recoverability damage;
- frozen semantic probes versus post-intervention source-recovery refits;
- nuisance changes that have the correct magnitude but wrong sign;
- unsupported donor and patched states;
- manual KL cancellation, ratio-of-means versus mean-of-ratios;
- paired numerator/denominator/model resampling;
- numerical interval propagation and strict endpoint boundaries;
- seed, lineage, exposure and panel-access violations;
- STOP/usage/disk guards, descendant accounting, emergency finalization and stage prerequisites.

Use synthetic fixtures only for implementation tests. Test authors must work from the written contract before production implementation and must not be the authors of the critical production kernels.

### 6. Next plausible extension

The saved map, public-prefix counterfactual and paired-ratio interfaces could support one separately reviewed intervention at another already validated site. That is a concrete possible reuse, not a site search or additional arm in C1.

D remains a separate mathematical oracle-only proposal.

## 12. Resource binding and operational guards

The latest owner policy governs: **no total CPU-time cap**, at most **4 threads**, at most **12 GiB RAM**, one scientific job at a time.

Default to **one numerical thread**, preserving existing meter/environment behavior and avoiding oversubscription. Any higher thread count must be explicitly frozen and remain within the aggregate limit.

The old meter and K4 binding hardcode CPU ceilings. Therefore:

- reuse meter, ledger, control and Job Object implementation files unchanged;
- add a C1 binding that rebinds job/session/task/output identities;
- disable inherited cumulative/per-run CPU ceilings and stage allocation ceilings;
- express uncapped policy as JSON `null`, not nonstandard JSON Infinity;
- use in-memory infinity only where the existing meter comparisons require a numeric sentinel;
- preserve every finite measured CPU charge and emergency record;
- bind Job Object memory to **12 GiB** and retain safe termination/drain behavior;
- reuse operation markers and finite algorithm-specific deadlines; these do not create an overall CPU allocation.

The new binding must not import K4’s 3600/3480-second limits or reset any previous ledger. C1 receives its own ledger, with previous ledgers retained unchanged.

Large stores and outputs go to **X:**. Safe STOP applies when C: free space is below **2 GB** or X: below **30 GB**. Real usage limits, STOP, invalid controls and latches take precedence.

Stage estimates below are forecasts, not caps. Freeze a **16 GiB output envelope**; reaching it stops at a safe boundary. Do not discard evidence or silently enlarge it.

## 13. Staged execution plan

| Stage | Required work and exit condition | Rough CPU estimate |
|---|---|---:|
| Written contract and clean review | Freeze methods, formulas, branch rule, identities and interfaces; independent result-blind review accepts the merged document | Under 0.1 CPU-hour |
| Independent test authors | Authors build synthetic critical fixtures from the contract before production code | 0.1–1 CPU-hour |
| Implementation and verification | Implement minimal additions; pass independent tests and affected integration checks; freeze code/environment | 0.5–3 CPU-hours |
| Oracle feasibility | Fixed cal/val candidate generation; identity, eligibility, coverage, references and oracle headroom; stop before model work on failure | 3–30 CPU-hours |
| Calibration and assay feasibility | Extract source/donor states; bind/build chart; fit centroid/probes; pass CAL-AUDIT and validation manipulation, matching and support gates | 2–20 CPU-hours |
| Validation precision | Compute validation regret only after assay gates; pass fixed ratio precision rules; independent feasibility review | 0.1–2 CPU-hours |
| Fresh single-endpoint test | Separate release; new histories, novelty/eligibility, fixed assay gates, then one 4096-row endpoint calculation | 3–30 CPU-hours |
| Final review and records | Immutable evidence export, independent review, scoped decision and coordinator morning report | Under 1 CPU-hour |

The broad estimate is approximately **9–87 CPU-hours**, dominated by all-row Decimal references and repeated nonlinear probe solves. No benchmark or experiment was run for this estimate. The executing coordinator may refine the forecast from metered stage timings without changing sample counts, methods or stopping rules.

Sequence:

1. Written-method contract.
2. Independent clean-context review of the merged planning tracks.
3. Independent synthetic test authors.
4. Production implementation and implementation acceptance.
5. Calibration/validation feasibility release.
6. Oracle, chart, manipulation, matching, support and precision gates.
7. Independent feasibility acceptance and fitted-artifact freeze.
8. Separate fresh-test release.
9. Fresh gate-only pass using saved maps and probes.
10. Unlock sealed endpoint logits only after validity passes.
11. Compute the single endpoint once; export and independently review it.

Fresh damage checks use the saved condition-specific CAL-FIT probes; no fresh refitting occurs.

Scientific gate failures retain their results and terminate this formulation. Technical corrections require explicit coordinator review, preserve prior evidence and cannot become a disguised scientific retry. After fresh exposure, repairs cannot change the method or introduce replacement data.

## 14. Readiness disposition

| Previously unresolved item | Resolution |
|---|---|
| Nonlinear probe family | Fixed 2048-feature RFF ridge, capacity, bandwidth, lambda, split, seed and no-selection rule |
| Information-damage matching | Original-source post-refit loss, blockwise tolerances, nuisance absolute limits and early stop |
| Support/counterfactual alignment | Oracle-only eligibility; actual donor posterior; signed semantic checks; frozen chart and activation support |
| Single endpoint/precision | Explicit ratio of regret advantage to oracle margin; paired bootstrap; fixed validation power and SD gates; strict decisions |
| Seeds/chart/artifact identities | Exact derivation rules, chart reuse/construction branch, checkpoint table, lineage and exposure registry |
| Six-field reuse assessment | Existing code inspected; unchanged reuse and minimal extensions identified |
| Staged resources | Contract → independent tests → implementation → cal/val gates → separate fresh endpoint; uncapped CPU and safety guards |

No scientific-method choice is deferred to fresh data. Missing generated IDs and implementation hashes are ordinary release prerequisites to be filled by the coordinator, not discretionary method choices.

# D: mathematical oracle-only horizon-gap sketches

## 15. Qualification: what “unnecessary at horizon 1” means

A construction must distinguish:

- a gap at a specified **reachable decision phase**; and
- a statistic that is sufficient for next-symbol prediction **at every history**, with a closed recursive update.

If \(S(H)\) determines the next-symbol law and there is a deterministic update \(S(Hw)=u(S(H),w)\), then induction determines every finite future-string law from \(S(H)\). Such a statistic cannot have a later-horizon gap.

The constructions below therefore state their reachable decision phase explicitly. Neither makes a universal recursively sufficient one-step statistic insufficient later.

They change the process by construction and do not reopen B2/D-055’s original cylinder-O horizon-2 screen.

## 16. Construction D1: square/cylinder seam with a delayed readout

**Purpose:** A finite, exact distinction between hidden square and cylinder topology that is irrelevant for the next symbol at a reachable boundary but necessary for the symbol two steps ahead.

Take a path/square lattice and its periodic-\(x\) cylinder counterpart, with \(n=4\) \(x\)-positions and the same vertical interval. Add a three-phase clock:

- **R:** read the current \(x\); emit `A` if \(x=0\), otherwise `B`;
- **S:** reset \(x\) to \(n-1\); emit `#`;
- **C:** apply one positive-\(x\) move; emit `!`.

The cycle is \(R\to S\to C\to R\). At the seam:

- cylinder: \(n-1\mapsto0\);
- square: the positive move holds at \(n-1\).

Use the same readout function and symbols in both worlds. Let an immutable hidden variable \(F\) select square or cylinder, with prior probability \(1/2\). The combined HMM is the disjoint union of the two clocked processes. A uniform clock prior gives a stationary three-phase mixture on the recurrent gadget.

At an `S` boundary, reachable prefixes ending `A,#` and `B,#` identify the two components and retain the same final symbol.

For both posteriors,

\[
P(W_{t+1}=!\mid H)=1.
\]

But

\[
P(W_{t+2}=A\mid H_{\mathrm{cylinder}})=1,
\quad
P(W_{t+2}=B\mid H_{\mathrm{square}})=1.
\]

Thus Q1 is identical, while both the two-step joint law and the distant-symbol marginal differ maximally. Any predictor that discards the component distinction must give the same horizon-2 answer to both histories and cannot be correct for both.

The distinction arises through periodic versus reflecting seam behavior, rather than a topology-dependent emission label.

**Limit:** This proves the necessity of distinguishing the two hidden components for this task. It does not prove that a predictor’s representation needs H1. A single bit can encode the component. The reset/clock gadget also differs materially from the existing lazy walk and uses only a small part of the substrate.

### Oracle-only confirmation

Use exact rational transition/emission matrices:

1. Verify the square and cylinder cubical complexes have their expected Betti numbers using existing world/complex machinery.
2. Exhibit finite positive-probability prefixes reaching the two `S` beliefs, including equal-length prefixes ending in `#`.
3. Calculate \(bTE\), \(bT^2E\), and \(bT\operatorname{diag}(E_{\cdot,!})TE\) exactly.
4. Verify identical Q1 and disjoint horizon-2 predictions.
5. Cross-check floating `BayesFilter`/`FutureOperator` outputs against those exact values.

There is no sampling, training, nearest-neighbour screen or estimated gap.

**Estimated cost:** seconds for the rational gadget; conservatively **under 300 CPU-seconds** including lattice topology and independent synthetic checks.

## 17. Construction D2: circular phase appears only in a future pair

**Purpose:** A stronger continuous construction where the boundary Q1 is constant but the two-symbol future law identifies a circular phase.

Let the hidden phase be \(\theta\in S^1\), fixed during a block. At a public boundary symbol `#`, generate:

1. \(U\) uniformly on \(\{0,1,2\}\);
2. \(V=U+D\pmod3\), where
   \[
   q_0(\theta)=\frac{1+\varepsilon\cos\theta}{3},
   \quad
   q_1(\theta)=\frac{1+\varepsilon\sin\theta}{3},
   \quad
   q_2(\theta)=\frac{1-\varepsilon(\cos\theta+\sin\theta)}{3},
   \]
   with fixed \(\varepsilon=1/4\).

All \(q_d\) are strictly positive and sum to one.

At the boundary,

\[
P(U=u\mid\theta)=1/3.
\]

The individual marginal of \(V\) is also uniform. However,

\[
P(U=u,V=v\mid\theta)
=\frac13q_{(v-u)\bmod3}(\theta).
\]

The pair law identifies

\[
\cos\theta=\frac{3q_0-1}{\varepsilon},
\qquad
\sin\theta=\frac{3q_1-1}{\varepsilon}.
\]

Therefore distinct phases have identical boundary Q1 but distinct Q2.

Make these phase beliefs reachable by including a preceding calibration part of each block that emits \((\cos\theta,\sin\theta)\), followed by `#`. The oracle then reaches \(\delta_\theta\) for every phase. This continuous observation alphabet is an explicit departure from the pilot.

For a finite version close to the existing lattice machinery, use \(\theta_j=2\pi j/12\), twelve phase states and a phase-identifying prelude. The finite construction proves twelve predictive distinctions, but does not establish a continuous topology requirement.

### Topological proof scope

For the continuous version, suppose a sufficient representation \(r(\theta)\) is continuous and determines Q2 exactly. Because Q2 identifies \(\theta\), \(r\) must be injective. A continuous injection from compact \(S^1\) into a Hausdorff representation space has an image homeomorphic to \(S^1\).

This rules out a continuous, globally single-valued real interval coordinate sufficient for the pair law. It does **not** require the ambient representation space to have nonzero H1: a circle can lie in \(\mathbb R^2\), which is contractible. Without continuity, an arbitrary code defeats this topological conclusion.

This construction concerns **joint horizon 2**. Its distant-symbol marginal alone remains uniform.

### Oracle-only confirmation

1. Symbolically verify positivity and normalization of \(q\).
2. Sum the joint law over either symbol and obtain exactly \(1/3\).
3. Verify the inverse expressions for \(\cos\theta,\sin\theta\).
4. Verify the prelude-to-boundary reachable posterior construction.
5. For twelve phases, check values exactly in the algebraic field containing \(\sqrt3\), then compare with the existing future operator.

The gap is an identity and injectivity argument, not an estimate.

**Estimated cost:** **under 300 CPU-seconds** for symbolic/exact finite checks. No real scientific payload is required.

## 18. D recommendation

D1 is the closest finite square/cylinder construction and cleanly answers whether the **world-topology distinction** can matter later while being irrelevant immediately at a specified reachable phase.

D2 supplies the stronger circular-family statement and makes its continuity, alphabet and joint-horizon assumptions explicit.

The coordinator should first commission an independent mathematical review and exact oracle-only contract for one construction. No model experiment, horizon search or reopened B2 screen follows automatically.

# Open questions

There are **no unresolved C1 method choices** in this proposal. Independent review must judge the fixed eligibility, probe capacity and matching tolerances; feasibility remains unmeasured.

For D, the owner should choose the intended meaning of “topological distinction”: distinguishing square from cylinder as in D1, or retaining a continuous circular family of predictive states as in D2.

**Commit/SHA handoff:** The coordinator must save, hash and commit this complete response on `planning-codex-coord-c1-freeze-readiness-20261014`, then record the actual new commit and SHA. This read-only planning track created neither.