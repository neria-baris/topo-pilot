# X4 next experiment — audit first, prospective information test only after GO

13 October 2026. Repository evidence snapshot: `f8afc2a5e43309aa4bf2d402f2be4e38470df180`. **Design only. No rank calculation, sampling, decoder fitting, intervention or training was performed.** This document is an implementation contract for a future authorized task; it grants no authorization. Governing science: [X4](X4_CAUSAL.md); evidence: [revision log](REVISION_AFTER_E4.md); interfaces: [research harness](RESEARCH_HARNESS_ARCHITECTURE.md).

## One recommendation and a hard execution boundary

Approve **Phase B: exact-oracle one-/two-step feasibility audit on existing artifacts only** first. It needs no new Transformer, auxiliary decoder, fresh test histories, PH experiment or intervention adapter. Return GO / NO-GO / INCONCLUSIVE and stop. Phase C is a separately approved prospective H4C-I test, conditional on B. Phase D is the separately approved intermediate causal test in X4; it is not part of the first instruction.

E4 trained activations predict b32 with median test R² 0.829 under O, while exact F1 predicts it with 0.838. These descriptive six-run summaries lower the expected residual effect and raise the probability of a ceiling. They do not measure joint Q2 sufficiency. The O cylinder circular result motivates a possible later target, not functional necessity. The proposed J≥0.10 and causal excess≥0.01 nat remain unchanged practical criteria.

## Frozen inputs and access

Primary world/process: cylinder O, original 12×12, numeric emission σ=1.25, original T/E. Three frozen step-5000 checkpoints, seeds 1729/2718/3141; step-0 counterparts are controls. Square O and both P cells are secondary; none rescues a primary failure. The three models are training replicates of one process, not three independent worlds.

Select the twelve O/P run IDs and their input artifact IDs from stored completed records and metadata, not a glob of the latest file. Relevant verified S7 IDs: dev extraction 13be28a051ce15b1, probes 63ebd7ec1ba5f38a, circular a7a60592e32b26fb, sensitivity baff2c7a1e5294c9. Their immutable parents, configurations and producer commits must be recorded. The current inspection did not find separate RunManifest payloads in the artifact tree; do not invent them. Check actual metadata and explicit run mappings instead.

Required B inputs: TransitionSpec, EmissionSpec, stationary law, ProcessDiagnostics, existing test HistoryIndex and OracleOutputs b32/F1/F2; existing S7 dev history splits for coverage checks. B does not need to load a checkpoint. Required C inputs add matching dev resid_post_3, checkpoints/final-LN weights through the authorized experiment resolver, and new public token datasets. S7 dev extraction stores resid_post_3 only, not every hook or persisted dev F2. Calculate dev b32/Q2 using existing token-only oracle kernels after B execution is authorized.

Privilege rules remain strict: learner/extractor receive public tokens and authorized checkpoints; oracle receives T/E, initial law and tokens, never evaluation sidecars; analysis may join oracle labels and privileged diagnostics. Analysis receives numeric γ/β/WU from an authorized consumer; it must not gain direct Checkpoint access. New labels never enter Transformer training.

Canonical trajectories, rather than public token numbers, are shared between model seeds. Use E_canon=E[:,symbol_perm], remap canonical tokens through each checkpoint's own permutation, and calculate targets in that run's vocabulary. Record canonical sequence keys mapped to each run's actual history IDs. Cross-run pairing on token-hash IDs alone is wrong.

## Phase B: mathematical definitions

Belief b is the posterior after the last visible emission. With row vectors,

Q1(b)=bG1, G1=TE;
Q2(b)[i,j]=b T diag(E[:,i]) T E[:,j].

G1 has shape 144×36; G2 has shape 144×1296 in lexicographic (i,j) order. Q2 is the **joint** law of the next two symbols. It is neither the second-token marginal bT²E nor two separately decoded marginals. Q1 equality, joint-Q2 equality and all-future equivalence are distinct.

Use FutureOperator.F1/F2 and observability_matrices(k_max=2). The method returns a list [O1,O2]: O1 is 36×144; O2 stacks horizons one and two, 1332×144. Extract G2 from its last 1296 rows and transpose, or evaluate F2 on the identity beliefs. Assert ordering and agreement of both routes. Do not build horizon three (36³ entries) merely because an API permits it.

Let B be an orthonormal 144×143 basis of the sum-zero tangent. Set H=BᵀG1. Use the full left singular basis of H, including dimensional null directions; a thin SVD alone omits them. For each relative rank tolerance 10^-8, 10^-10, 10^-12, obtain U0 spanning ker(Hᵀ). Report singular values and norms/ranks of D=U0ᵀBᵀG2. Record residuals ||U0ᵀH||, ||BᵀB−I||, ||1ᵀB||, dimensions and conditioning.

Exact tangent-kernel inclusion ker(G1)⊆ker(G2), with row-vector conventions understood, establishes factorization of Q2 through Q1 on the full simplex. A tangent direction v with vG1=0 and vG2≠0 gives an ambient distinction because beliefs near an interior point can differ by εv. Neither result alone identifies the reachable context-32 set K32. Numerical tolerance is not an exact proof; use analytical symmetry/factorization where possible and report floating-point uncertainty.

Stored test F2 is float32 with schema tolerance 10^-4. For near-equality diagnostics recalculate in float64 from stored b32 and the same kernels; mark this as numerical precision reconciliation, not a new experimental sample. Check rows sum to one (kernel target tolerance 10^-10), nonnegativity within numeric tolerance, and Q2 marginalization to Q1 (target 10^-12 in float64). Compare stored float32 values within their declared tolerance. Never round stored targets to create collisions.

### Reachable-history audit and proposed practical gates

Existing test data are already unblinded: results are exploratory feasibility evidence only. Repeat coverage checks on existing dev pools without using them as untouched confirmation.

Use Hellinger distance H(p,q)=||sqrt(p)−sqrt(q)||₂/√2. Proposed audit settings, to freeze before running B:

- Select 512 anchors in each available pool by a fixed hash of canonical trajectory IDs.
- For each anchor choose its five nearest Q1 neighbors with the same last symbol, excluding itself. Unrestricted neighbors are secondary.
- A near-Q1/distinct-Q2 witness has H(Q1,Q1')≤0.01 and H(Q2,Q2')≥0.05.
- Coverage requires at least 128 anchors with an admissible same-symbol partner. Practical evidence requires at least 5% of eligible anchors to have a witness, in the old test pool and at least two of the three dev pools. Dev pools are repeated evidence for the same process, not independent world replications.
- Record all distances, last-symbol group sizes, posterior entropy/concentration, partner reuse, discarded anchors, and agreement across permutations/numeric tolerances.

These are proposed screening settings, not calibrated constants or additions to the original J success rule. Same-symbol restriction addresses a simple competing explanation without establishing that histories are otherwise matched. Nearest-neighbor pairs are dependent and receive no pair-count p-value.

| Outcome | Required evidence | Permitted next step |
|---|---|---|
| GO | Stable ambient allowance plus practical reachable near-Q1/distinct-Q2 evidence meeting the frozen coverage rule; or a rigorous reachable exact witness with a meaningful target gap | Propose C. Near equality supports a robust-accessibility question, not strict information-theoretic insufficiency. Report the actual subtype of GO. |
| NO-GO | Exact factorization with controlled practical conditioning; or adequate sampled coverage with no material gap under this declared audit, consistently across pools | Stop the horizon-gap branch for this process/horizon/resolution. Sampled NO-GO is not a theorem about every reachable history. |
| INCONCLUSIVE | Tolerance-dependent rank, missing lineage, insufficient near-neighbor coverage, inconsistent pools, or unstable numerical target gaps | Stop and report the specific limitation. Do not create a larger fresh pool or fit decoders automatically. |

An ill-conditioned exact factorization can leave a practically hard inverse and must be classified accordingly; tiny Q1 changes may amplify into Q2 changes without violating exact sufficiency. If ambient allowance is absent and reachable gaps disagree, first diagnose conditioning/precision; do not claim a contradiction to algebra. If a strict reachable witness is unavailable, never relabel near collisions as equal Q1.

The B report must give a separate verdict for (i) ambient algebra, (ii) reachable practical gap, (iii) strict sufficiency, usually unresolved, and (iv) recommendation. Explicitly list evidence that would be needed to change a sampled stop decision.

### Future validation requirements — not tests run now

Known-answer fixtures before trusting B implementation: constant emissions give no future gap; a four-state path with symmetric neighbor probability .4, deterministic A at 0/1/2 and B at 3 has Q1(δ0)=Q1(δ1)=A but Q2(δ0)[AA]=1 and Q2(δ1)[AB]=.16. This fixture proves ambient possibility, not reachability in the pilot. A constructed G2=G1L validates factorization detection; vocabulary permutations must preserve distances and gates. Validate float32/float64 reconciliation, joint ordering and marginalization with fixtures that would catch accidental use of bT²E. Future C additionally validates exact centered-logit null invariance and split isolation.

## Phase C: preserve the primary, add mandatory capacity controls

Only after B GO, owner selection of the protocol and an independent lineage: fit on existing dev 3072 histories, select on its 1024 validation histories per run, evaluate once on 4096 new trajectories per world/condition in eight disjoint 512 panels. All transforms/normalization, hyperparameters, calibration and random seeds are frozen before fresh-test extraction. Original DatasetStage settings reproduce old data; a named SeedTree stream alone is insufficient unless it changes sampling and sequence-ID namespace. Use an HMMSampler/PanelBuilder orchestration adapter with explicit new lineage.

Derive final u=(z−mean(z))/sqrt(var(z)+10^-5). Set A=diag(γ)WUᵀ and C=I−11ᵀ/V; Peff projects onto range(AC). u_null=u(I−Peff). Reuse analysis.readout's existing projector by passing centered WU_effective=C WU and the matching γ; no new general projector API is needed. Reconstruct stored final LN/logits before interpreting features. Never renormalize u_null to assert exact readout equivalence.

Primary affine ridge uses unpenalized intercept, fit-only feature standardization and λ∈{.001,.01,.1,1,10}, validation MSE selection. Target is raw lexicographic joint Q2; loss averages all 1296 coordinates. Compare oracle Q1 vs [oracle Q1,128-coordinate u_null]. Preserve

J=(MSE_Q1−MSE_aug)/MSE_Q1.

Every cylinder-O model must have J≥.10, paired trajectory-bootstrap 95% lower>0, and J above q95 of 20 fixed matched-random-feature J values. Reject the all-three practical claim if any upper bound<.10; otherwise inconclusive. Target variance≤10^-16 or affine-baseline MSE/variance≤.01 gives an information-ceiling/inconclusive outcome. Retain absolute errors even when ratios are unstable. Never compute KL from unnormalized ridge outputs.

**Mandatory nonlinear comparator, secondary to J:** use one-hidden-layer GELU MLP, affine 1296-output head, widths {16,32,64}, AdamW learning rate .001, batch256, at most100 epochs, minimum10, validation patience10; weight decay {0,.001}. Use three predetermined auxiliary fit seeds, select architecture/weight decay on mean validation MSE, and average the three fitted predictions for each selected family. Auxiliary stochastic seeds are not Transformer replicates. Center targets and scale by one global fit-only target standard deviation for optimization; invert this transform and score raw Q2 MSE. No test-based early stopping.

For oracle-Q1 width w, parameter budget P=(36+1296+1)w+1296. The augmented nonlinear input uses oracle Q1 plus coordinates in an orthonormal basis of the effective-null subspace, rank r; this is information-equivalent to all128 null coordinates. Give its width floor((P−1296)/(36+r+1296+1)), requiring achieved counts within 5% of the Q1 budget and no excess parameters. If this cannot be achieved, budget comparison is inconclusive; do not improvise a larger model. Apply the same normalization/optimizer/grid/three-seed ensemble to both. Report all prespecified capacity curves on validation and the selected comparisons on test. Nonlinear-Q1 may be stronger than the affine augmentation; that is a scientifically useful result.

Dimension matching alone is insufficient for affine augmentation controls. Use 20 fixed independent random-feature sets with the same column count128 and fit-only null-feature covariance/rank and marginal scale; independent draws for fit/validation/test, never targets. Report covariance matching and any failures. One-hot R1, initialized nulls, shuffled fit/validation labels, model-produced Q1, and full u remain mandatory controls. Exact belief b32 gives Q2=b32G2 without fitting: a mathematical ceiling. Include oracle b1 and embedding R1 to separate short-context and symbol geometry.

| Results | Strongest conclusion | Stronger conclusion not justified |
|---|---|---|
| J positive, nonlinear Q1 closes gap | Better linear accessibility in the chosen representation | Q1 lacks predictive information |
| Augmentation beats both matched nonlinear families | Future-target information is more accessible than under the tested Q1 families | No Q1 function can recover Q2 |
| Rigorous reachable equal-Q1/different-Q2 witness, augmentation succeeds | Q1 is insufficient on that set and the representation exposes part of the distinction | H1 causes the information advantage |
| All comparisons hit a ceiling | Little residual target error remains at this horizon for this protocol | Representation lacks topology or all longer-horizon utility |
| Controls fail or precision/coverage gates fail | Inconclusive | A negative mechanistic theorem |

The nonlinear family is deliberately finite. If a more expressive family is needed, propose a new prospective protocol; do not widen it in response to fresh-test results. The old S7 O ridge λ at the lower grid edge is a limitation of that completed probe, not permission to refit its result.

## Interface list: immediate versus deferred

| First need | Concrete interface and existing owner | Inputs → outputs | Status |
|---|---|---|---|
| B | experiment read-only input resolver | selected existing IDs + protocol → resolved metadata/arrays, parent graph, errors | Small isolated orchestration adapter; no new artifact schema |
| B | oracle FutureOperator + existing BayesFilter | T/E, existing tokens/beliefs, k=2 → float64 G1/G2/b/Q1/Q2 | Existing numerical kernels unchanged |
| B | analysis horizon feasibility functions | typed numeric arrays + canonical HistoryIndex mapping → rank/coverage tables and scoped verdict/reasons | Small pure analysis functions, no checkpoint access |
| B | analysis/experiment report records | metrics + parent IDs/config/code → immutable records and human-readable gate report | Reuse MetricRecords/store; protocol-local gates, never overwrite G-H |
| C | existing activation extraction + pure readout helper | tokens/checkpoint through authorized consumer; numeric weights → u/null and reconstruction diagnostics | Small orchestration; reuse effective projector construction |
| C | prediction RidgeProbe + explicit small MLP adapter | fit/validation features/targets and frozen budget → fitted predictions/losses/fit provenance | Auxiliary estimator addition; PredictionStage.run_probes is an I/O stub, not a universal runner |
| C | dataset sampler/PanelBuilder lineage adapter | same T/E + new named stream/sequence namespace → public ObservationSets and aligned targets | New histories only after GO and separate approval |
| D only | frozen suffix/patch adapter | public tokens, checkpoint, site/position, precomputed transform → logits and diagnostics | No current resume/patch API; defer |
| Future only | metric augmentation, lifted transport state, local-system/sheaf cochains | property-specific definitions → validated structures/oracles/estimators | Defer all |

Each interface's provenance, validation, dependencies and error states are specified in the [minimal contracts](RESEARCH_HARNESS_ARCHITECTURE.md#minimal-contracts-x4-first). Implement only B rows for the first authorized task. Do not add a general MathematicalObject, GeneralOracle, learner abstraction, new world builder, registry rewrite, DAG scheduler or universal score. Shared six scientific gates are reporting conventions, not mandatory new classes.

## Statistics, costs and artifacts

Model unit: three frozen training replicates. Evaluation unit: trajectory conditional on each model. Use 2000 paired bootstrap draws over canonical keys, mapped to run-specific history IDs; report each model, median/range and conditional intervals. Eight panels and repeated nearest-neighbor pairs are not independent seeds. Three all-positive independent model signs alone give one-sided p=.125; no population-level significance claim.

B estimate: minutes to30 CPU minutes, cap1 CPU hour/8 GB RAM, ≤100 MB added summaries/arrays, roughly1–2 working days for adapter and mathematical validation. C estimate: .5–2 CPU hours extraction/ridge plus1–4 hours auxiliary MLPs, total cap6 CPU hours,8 GB RAM,≤2 GB outputs; roughly2–4 days plus1–2 days for the capacity-controlled comparator. These are unbenchmarked planning estimates. If the cap is reached, report incomplete/inconclusive and stop, with no automatic budget escalation. No GPU/cloud assumption.

Use an independent output store. Identity must include protocol version, source repository commit, producer commit, T/E/initial-law IDs, checkpoint IDs when used, hook/position, horizon/order, precision/rank tolerances, sample selection, feature normalization/decoder budget, canonical mapping/permutations, seeds, and all parent IDs. Derived arrays must be checksummed and versioned in the analysis namespace using existing supported artifact contracts or an explicit reviewed export; do not silently overload a frozen type. Missing lineage is an error, not a reason to substitute a “latest” artifact.

B outputs: rank spectra/residuals; reachable-neighbor distances and coverage; input/provenance table; precision diagnostics; scoped GO/NO-GO/INCONCLUSIVE report; an explicit stopped-after-B statement. C outputs add per-history loss predictions for every baseline, unchanged J verdicts, nonlinear secondary verdicts, control/ceiling failures and runtime. Publish all models and failures.

## Minimal future instruction to the implementation Conductor

> Implement and run only the X4 Phase B feasibility audit described in X4_NEXT_EXPERIMENT.md, after the owner explicitly authorizes it and freezes its screening settings. Reuse existing immutable T/E, ProcessDiagnostics, stored test beliefs/F2 and existing dev tokens. Add only isolated pure analysis and experiment orchestration needed for float64 G1/G2, tangent-kernel and reachable-history diagnostics, with the stated provenance and known-answer validation. Write to a separate output store; preserve all core artifacts and gate verdicts. Do not fit auxiliary decoders, generate new histories, patch models or train Transformers. Return the scoped GO/NO-GO/INCONCLUSIVE report and stop for review.

This is proposed instruction text, **not dispatched or authorized by this planning package**. Native p31 enumeration, causal controls, PH manipulation checks and exploratory Fisher pullbacks remain governed by X4_CAUSAL.md and require later approval.

