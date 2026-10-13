# X4-Causal: predictive information, topology and computation

13 October 2026; snapshot `f8afc2a5e43309aa4bf2d402f2be4e38470df180`. **Preregistration-ready proposal, not an approved preregistration. Nothing has been run.** Evidence labels [R/M/L/H/S] and bibliography are defined in [Research Landscape](RESEARCH_LANDSCAPE.md). Original F1/H2–H4 and X4 decisions are unchanged. The proposed tests were motivated by E3 and revised after the completed E4 review. See [revision log](REVISION_AFTER_E4.md); E4 is published and tagged, with G-H still FAIL.

## Claim and experimental sequence

**[H4C-I, primary immediate hypothesis]** In the three frozen cylinder-O models, the final effective-readout-null representation adds at least 10% held-out reduction in two-symbol-future MSE beyond an affine decoder of oracle F1. This tests *linearly accessible future information*, not topology causation.

Competing explanations: all recoverable future information is already available from F1; added features merely increase decoder capacity; finite sample correlations or inaccurate model F1 create apparent improvement. Controls include exact oracle F1, dimension-matched random features, initialization, last-symbol features, shuffled targets, and the other world/condition cells.

**[H4C-F, primary short follow-up hypothesis]** At a fixed intermediate hook, erasing a prespecified predictive circular coordinate raises oracle-relative one-step regret by more than rank- and displacement-matched random erasure. The primary hypothesis is about this coordinate and this frozen computation. It does not say the abstract invariant H1 is necessary.

The programme has three X4 gates: mathematical observability; held-out auxiliary decoding; then intervention. These map to the common definition/observability/reference, representation and function gates in the [harness](RESEARCH_HARNESS_ARCHITECTURE.md). Failure of an upstream gate stops the corresponding downstream claim. The informative negative result is allowed to be “a loop-bearing representation is dispensable for the measured computation.”

## What E4 changes and what it leaves open

**[R]** Cylinder O trained circular agreement is 0.884–0.892 (oracle median0.915), whereas P is near0.05. This makes a periodic target more plausible under O, without proving intermediate-hook decodability or causal relevance. U-cylinder agreement about0.60 despite zero context gain shows why location structure is not evidence of multi-step history integration. E4 has no direct R1 circular comparison; its permutation null cannot settle that alternative.

**[R]** O activation→b32 medianR²=.829 and exact F1→b32=.838; P .378 versus.382. This weakens the expectation of extra useful information, increases ceiling risk, and makes exact F1/nonlinear-F1/last-symbol controls central. It does not settle Q2. A negative horizon audit is informative about this process/horizon/resolution, not absence of topology or every future use. The O/P H1 contrast and H3′ belief geometry remain separate results; H4 remains rejected.

**[H]** Preserve H4C-I≥10% and H4C-F≥.01 nat. These are proposed practical effects, not universal constants or effects calibrated by E4. There are no new results in this revision.

## Mathematical assumptions and audit

**[M]** Beliefs b refer to the hidden state that emitted the last observed symbol. `Q1=bTE`; `Q2[i,j]=b T diag(E[:,i]) T E[:,j]`. Q2 is a joint distribution of size V²=1296, not the marginal `bT²E`. Let G1 and G2 be these linear maps; `b~k b'` means equal joint length-k laws. The inclusion of equivalence relations is `~(k+1) ⊆ ~k`.

Before auxiliary fitting, inspect existing ProcessDiagnostics singular spectra and the stored F2 arrays. Proposed analysis will compare the sum-zero null space of G1 with G2. Use orthonormal tangent basis B for `{v:v1=0}`, compute singular values of `BᵀG1`, then the norm/rank of G2 restricted to its numerical kernel. Report relative rank thresholds 1e−8, 1e−10 and 1e−12 in float64. If conclusions change with tolerance, report numerical indeterminacy. An exact symmetry proof, where available, has priority over numerical rank.

Full-simplex null directions do not establish reachable collisions. On calibration histories only, examine oracle-F1 distances and Q2 differences with same-last-symbol restrictions. Keep all pairs descriptive; do not test millions of dependent pairs as independent samples. If Q2 factorizes through Q1 on the reachable set, the horizon-specific rationale disappears even when G1 has a large ambient kernel.

**[R]** Oracle F1/F2, `FutureOperator.observability_matrices`, and singular-value calculations already exist. E1's O F2 contrast (0.614 vs 0.216) does not show extra information beyond F1: different diagrams can result from different metrics on the same information.

### Audit-only boundary and explicit outcomes

The first proposed execution is **Phase B only** in [X4_NEXT_EXPERIMENT.md](X4_NEXT_EXPERIMENT.md): float64 G1/G2, full left-null tangent calculation, stored-test and existing-dev reachable diagnostics, complete provenance and a stop report. No decoder fitting, new histories, intervention or training precedes GO.

GO requires stable algebra allowing the gap and a declared practical reachable gap with adequate coverage, or a rigorous reachable witness. NO-GO is exact practically conditioned factorization or no material gap in the adequately covered declared sample; the latter is sample-scoped. Rank instability, missing lineage or insufficient near-neighbor coverage is INCONCLUSIVE. Proposed screening distances/coverage are separate prospective choices, not changes to J. Near-Q1 equality does not prove strict insufficiency. See the implementation-ready document for fixed candidate settings, dimensions, precision reconciliation and known-answer validations.

Existing stored F2 is float32; use the oracle's float64 recalculation from stored b for near-equality diagnostics. observability_matrices(2) returns a list [O1,O2], and O2 stacks one-/two-step rows; do not confuse it with an unstacked G2 or request horizon3 unnecessarily.

### Final effective-null control

Use row-vector convention. Read γ, β and WU from each matching checkpoint and construct `A=diag(γ)WUᵀ`, `C=I−11ᵀ/V`, `Plogit=Proj(range(A))`, and `Peff=Proj(range(AC))`. Reconstruct u from stored `resid_post_3` using actual ε=1e−5. Verify stored `ln_final_out` and logits first.

Define `u_null=u(I−Peff)` and the intervention `u'=uPeff`. Apply it **after** normalization: feed `y'=u' diag(γ)+β` directly to the frozen unembedding. Do not pass u' through LN again. Centered logits and softmax must be unchanged. Proposed tolerances: reconstructed stored logits ≤1e−5 absolute; centered-logit difference ≤1e−8 in float64 algebra; probability difference ≤1e−8. A reconstruction failure invalidates the control.

This transformation may produce vectors outside the natural LN image. That is acceptable for the exact output-equivalence check and must be stated. It cannot be used as evidence for a natural on-manifold mechanism. Recompute PH of the full u, its effective component, and its null component on the same histories; topology may persist in the effective component. Never call projection “destroying the loop” without a measured, calibrated change.

**[M]** Final-null invariance also does not demonstrate stored memory used in native future generation. This model has no recurrent final-vector state; attention keys/values arise upstream. A final post-LN intervention that leaves each conditional distribution unchanged leaves the corresponding autoregressive joint law unchanged too. Another output decoder can access u_null; native later computation need not do so.

## Immediate experiment I: horizon information audit

### Frozen cohort and data

Exploratory reuse (Level A): E3 checkpoints 0/5000, primary and LN hooks, stored logits, OracleOutputs b32/q/F2, HistoryIndex, matching final weights, and X4 MetricRecords for twelve O/P runs. N-1729 supplies a collapse/no-information check, not a threshold.

Confirmatory evaluation (Level B): frozen step-5000 models; use existing dev histories for auxiliary fit/validation only, with 3072 fit and 1024 validation trajectories per run. E4 dev extraction is verified: it contains resid_post_3 only. Reuse it to derive u/null; calculate dev beliefs/Q2 from existing tokens with the exact oracle because dev F2 is not persisted. Extra hooks are a later explicitly scoped extraction. Generate **4096 fresh evaluation trajectories per world/condition**, under a new named SeedTree stream independent of original test and training streams. Share these histories across the three frozen models of that process and all views; form 8 disjoint panels of 512. Fresh sequence/history identifiers must encode the new dataset lineage. No fitting, donor selection, threshold calibration or transform selection touches the fresh test set.

Sharing means the same **canonical-symbol trajectories**: emission symbol permutations differ by training replicate. Follow the existing dataset convention `E_canon=E[:,symbol_perm]`, then map canonical tokens through each checkpoint's matching symbol permutation. Compute oracle targets in that run's public vocabulary; do not feed one replicate's public token IDs to another model. Each run keeps its own token-hash-derived history IDs for within-run joins. Cross-run paired resampling uses canonical trajectory/sequence keys and an explicit mapping to those history IDs. The new lineage must also enter the sequence-ID namespace; simply rerunning DatasetStage with unchanged settings would reproduce the original test set.

The ensemble claim concerns these three independently trained models of each fixed process. New test histories make the evaluation prospective; they do not create new independent training replicates or convert seed-ensemble conclusions into population-level guarantees.

### Decoders and primary metric

Target Y is flattened Q2 in lexicographic `(next1,next2)` order. Fit centered affine ridge decoders with an unpenalized intercept and λ grid `{1e−3,1e−2,1e−1,1,10}` selected on validation MSE, as in S7. Standardize nonconstant feature columns with fit-only statistics. Use exactly the same target, split, loss normalization and λ rule for:

| Decoder | Purpose |
|---|---|
| Oracle Q1 → Y | Primary information baseline, not model's imperfect output |
| [Oracle Q1, u_null] → Y | Primary augmented representation |
| [Oracle Q1, random independent features] → Y | Same number of added columns, independent of Y; 20 fixed seeds |
| [Oracle Q1, step-0 effective-null] → Y | Initialization reference, matched own checkpoint projector |
| [Oracle Q1, one-hot last symbol] → Y | Symbol-only information reference |
| Model Q1 → Y, [model Q1,u_null] → Y | Secondary; improvement may reflect next-token approximation error |
| Full u → Y and oracle b32 → Y | Ceiling/context; not a replacement primary endpoint |
| Augmented model with shuffled fit/validation labels | Leakage/overfitting control; test labels remain unshuffled |

Primary per-run statistic:

\[
J_r=\frac{\mathrm{MSE}(Q_1\to Y)-\mathrm{MSE}([Q_1,u_{null}]\to Y)}{\mathrm{MSE}(Q_1\to Y)}.
\]

MSE averages over histories and 1296 target entries. Define target variance as the mean squared deviation of Y from its fit-set mean. If target variance≤1e−16, or baseline MSE/target variance≤0.01, the proposed “10% gain” is not meaningfully testing a residual horizon gap; report an information-ceiling/inconclusive outcome. These thresholds are prospective design choices, not E3-derived effect estimates. Report absolute MSE, normalized J, and paired history uncertainty. Never compute KL on unconstrained ridge outputs.

**Decision criterion:** H4C-I supported for the fixed cylinder-O cohort iff in every run (i) J≥0.10, (ii) its paired trajectory-bootstrap 95% lower bound exceeds zero, and (iii) J exceeds the 95th percentile of the 20 random-feature-control J values. Other world/condition cells are secondary and cannot rescue a failed primary. If the upper bound is below 0.10 in any run, the stated all-three practical-effect hypothesis is rejected; otherwise classify it inconclusive. Control anomalies invalidate interpretation rather than being excluded.

This affine test can be positive when a nonlinear decoder of Q1 alone would suffice. It establishes added **linear accessibility**, not strict information-theoretic nonsufficiency. The algebraic audit and a **mandatory separately labeled nonlinear-Q1 comparison** address that distinction; do not redefine the primary after seeing the result. [X4_NEXT_EXPERIMENT.md](X4_NEXT_EXPERIMENT.md) specifies the small GELU MLP, identical data/optimizer/validation, parameter budgets and equal-budget nonlinear augmented comparator. A finite tested-family failure cannot prove impossibility. Exact b32G2 is a fit-free ceiling; add oracle b1 and embedding R1. Primary random features must match column count, fit-only rank/covariance and scale, not merely dimension.

## Short experiment F: coordinate-associated causal use

### Coordinate, site and fixed quantities

Primary site: `resid_post_1`, position p=32, immediately after block 1, before blocks 2/3 and final LN. Freeze all weights, earlier activations, visible token sequence and attention mask. Patch only the selected vector; then resume the remaining blocks over the full token-position tensor. Stored position-32 vectors alone are insufficient for this suffix computation.

Primary target for fitting an eraser is the **belief expectation**

\[
m(b)=(\sum_z b_z\cos(2\pi x_z/12),\sum_z b_z\sin(2\pi x_z/12)),
\]

not an arbitrary angle when the resultant is near zero. Fit a linear concept eraser on calibration representations and these two targets, recording rank and norm. Use the precise continuous-target covariance-erasure formulation; validate held-out linear recoverability. LEACE's classification guarantees do not automatically mean nonlinear phase information is erased. The eraser is applied at the primary intermediate site without adding an extra normalization.

Circular-cohomology coordinates of the most persistent class (GF47, mid-lifetime) provide a **secondary measured correspondence**. Fit on calibration clouds and require stable class lifetime, orientation/rotation alignment, and an independently validated out-of-sample extension before using them as intervention targets. Current `fit_transform` supplies no such extension. Completed S7 circular results remain descriptive prerequisites, not confirmatory causal results. They use resid_post_3, not the proposed intermediate site.

### Intervention/control matrix

| Intervention | Precisely fixed or changed | Interpretation |
|---|---|---|
| Identity/resume | Same hook tensor and frozen suffix | Forward reconstruction control, logits ≤1e−5 |
| Belief-circle linear erasure | Erase calibrated sin/cos target at one vector | Primary coordinate-associated causal effect |
| 20 random erasers | Same lost rank and per-history L2 displacement within 5%; use only fit data to set construction | Ordinary damage/capacity control; unmatched comparisons inconclusive |
| Shuffled-target eraser | Same fitter on permuted calibration targets | Specificity control |
| Ordinary predictive eraser | Rank-matched principal oracle-Q1 target directions | Can predictive-information damage explain the effect? |
| Final effective-null projection | Site after final LN, same effective logits | Exact no-effect control from the algebra above |
| Natural donor patch | Donor selected from calibration pool by same last symbol and oracle-belief distance; recipient history unchanged | Natural donor vector; hybrid context may still be off-manifold |
| Circle rotation | Local calibration map fits angle/tangent displacement, then applies fixed ±π/6 with retained nuisance coordinates | Secondary only; rotations preserve circle topology, so test coordinate use rather than loop destruction |
| Frozen versus refitted output head | Primary uses original suffix/head; secondary fits a new affine head on intervened calibration features only | Rescue indicates decoder mismatch or surviving information; failed affine rescue is not proof of irrecoverable loss |

Random directions must also be reported for induced oracle-Q1 decoding loss and effective-logit displacement. Equal L2 norm and rank alone do not imply equal predictive-information loss. If no random-control family can satisfy the matching specification, report that comparison inconclusive and retain the raw damage curves.

**[M] Topology warning:** Smooth rotation of a circle and an invertible affine erasure-adjacent change may preserve its topology. A discontinuous cut/collapse can destroy predictive distinctions and move off support. PH changes under a finite-sample transformation are a manipulation check, not proof of a topology-only intervention. Separate topology-preserving rotations from topology-altering cut/collapse explorations; the latter are not a primary causal claim.

### Additional controls required after E4

Fit all erasers/maps on calibration data; freeze choices before prospective recipients. At the same hook compare: periodic m(b); nonperiodic target E_b[y]/11; local-position target consisting of rank2 fit-only principal coordinates of the belief's local position features; last-symbol target consisting of the two leading fit-only principal components of one-hot last-symbol vectors; and generic predictive rank2 principal Q1 targets. Record lost rank, per-history displacement, predictive decoding loss, entropy/support changes and failure of the proposed5% displacement match. Different targets may require different maps; if their damage cannot be matched, retain the raw effects and withhold specificity.

For local position, use the fixed grid neighborhood occupancy vector b times the known radius-one neighborhood-incidence matrix; learn its principal two directions on calibration only. This is an ordinary spatial nuisance target, not an invariant. For y use its achieved rank (usually1); match the circular eraser to the same rank or supply separate rank1 dose comparison rather than pretending rank1 and rank2 damage are equal.

Add **direct R1 circular correspondence** using the same cohomology/latent-angle statistic on aligned history rows; duplicate token embeddings may make the cocycle estimator degenerate, in which case report the failure and a fit-only symbol→m(b) sin/cos regression baseline. Neither baseline receives extra histories. Require held-out improvement in m(b) recoverability beyond R1, including same-last-symbol residual prediction, before a history-integration claim. Square/P/initialized/U controls remain useful, and do not substitute for direct R1.

Label manipulations separately: A=topology-preserving rotation, B=information erasure, C=calibrated collapse/identification that actually changes the PH signature. Recompute diagrams on the same histories with frozen distance/scale/calibration. Linear erasure is B until shown otherwise. C may destroy ordinary information or move off support; measured PH change plus prediction loss alone does not isolate topology. If no interpretable topology-specific manipulation exists, stop at coordinate-associated information use.

### Outcomes and inference

Primary effect per frozen cylinder-O model:

\[
\Delta R_r=\mathbb E_h[\mathrm{KL}(Q_1(h)\Vert p_I(h))-\mathrm{KL}(Q_1(h)\Vert p(h))].
\]

Hypothesis H4C-F is supported for this cohort if every model's erasure ΔR exceeds the mean rank/norm-matched random ΔR by ≥0.01 nats, with a paired trajectory-bootstrap lower bound above zero for the difference. The 0.01 threshold is an explicit practical-effect choice. Failed alignment, failed forward reconstruction, absent target decodability, unmatched controls or uncalibrated topology give an inconclusive mechanistic result. If validated erasure has an upper bound below this excess threshold in any model, the all-three claim is rejected. All models/results, including failures, stay in the report.

Secondary measurements: ΔR dose curves; oracle-targeted donor changes; decodability of m/b32/Q1/Q2 before and after erasure; raw displacement, centered-logit displacement, norm and local support diagnostics; S and complete diagrams in original and transformed clouds; square/P/R0/R1 comparisons. PH validity must be checked independently of the regret outcome. Do not select an intervention because it happens to make both curves favorable.

Positive outcomes justify “the specified coordinate-associated component participates in this computation.” Negative outcomes may mean redundancy or alternative encoding. Inconclusive outcomes may mean a weak eraser or support mismatch. None alone establishes necessity of H1. Use [amnesic probing](https://doi.org/10.1162/tacl_a_00359), [LEACE](https://arxiv.org/abs/2306.03819), and [divergent-intervention analysis](https://proceedings.iclr.cc/paper_files/paper/2026/hash/133e588e1429f9f1e25b215da145580e-Abstract-Conference.html) within these limits.

## Optional exploratory functional geometry — deferred from the first experiment

**[M/L]** Fisher/Riemannian metrics have established precedent; see [Ollivier, 2013/revised2015](https://arxiv.org/abs/1303.0818). For representation h, logits ℓ(h), p=softmaxℓ, and J=∂ℓ/∂h, the pullback is G_h=Jᵀ[diag(p)−ppᵀ]J. A small perturbation has local output KL approximately ½δhᵀG_hδh. At the post-LN affine readout with row-vector u, G_u=A[diag(p)−ppᵀ]Aᵀ, so the effective-null space has exactly zero local sensitivity when p has positive entries.

An optional calibration-only diagnostic can compare perturbations associated with the circular target against local prediction sensitivity; at intermediate layers use the frozen suffix Jacobian, not the final affine formula. Check finite-step approximation as dose tends to zero and report anisotropy/rank. It is local functional geometry, not a global H1 estimator or necessity test. No new primary endpoint, theorem or novelty claim follows. Automatic differentiation/resume support is a later dependency; do not require it for B/C.

## Native joint prediction: minimal horizon extension

**[R/M]** At p=32, a second prediction after appending a token would require position 33, outside the learned 0..32 position table. Do not silently extrapolate positions, crop/reset histories, or call an auxiliary probe the model's native Q2.

Minimal no-training alternative: evaluate at **p=31**. Existing 33-symbol trajectories supply a 31-symbol prefix. Compute fresh oracle Q1/Q2 at p31 and extract the required hook. For each first symbol i, run `[BOS,w1..w31,i]`, still within 33 input positions. Construct

\[
P_{M,2}(i,j\mid h)=p_M(i\mid h)\,p_M(j\mid h,i).
\]

Use exact enumeration of 36 continuations per history; no sampling is needed for k=2. With an intermediate patch, reapply the same calibrated intervention at the **original prefix position p31** in each continuation branch; leave appended position p32 unpatched. Causality ensures the prefix vector is unchanged before intervention across branches. Compare unpatched and patched joint distributions with the oracle **recipient** Q2. Donor-target comparisons use a separately specified counterfactual and are secondary.

Report total joint regret and its chain-rule decomposition into first-token regret and oracle-weighted conditional second-token regret. A larger total for k=2 is not evidence that topology matters more: there are two opportunities for error. A horizon-specific hypothesis must predeclare excess **second conditional** regret relative to matched controls while first-step changes remain within a declared tolerance (proposed 0.002 nats). Finding those suitable interventions on calibration data is a feasibility gate; if none exist, do not test the selective-horizon claim.

Capacity cost: 4096 histories ×36 continuation passes per run, roughly 4.9M position-tokens; batching makes this plausible on CPU, but no new benchmark has been run. For the primary cylinder-O cohort this is about 14.6M position-tokens plus prefix passes. Start with a timing estimate after approval, use a 2-hour CPU cap, and report censoring. Longer k requires `p+k−1≤32`; cost grows as V^(k−1). Beyond that, a context/generation interface change or additional training is required, rather than a claim about existing p32 checkpoints.

## Statistical discipline, interfaces and resources

Independent model unit: each training replicate, three per fixed world/condition. Independent evaluation unit conditional on a model: trajectory. Panels are within-model subsets; pairs are descriptive. Use 2000 paired trajectory-bootstrap draws; because evaluation trajectories are canonically shared across model seeds, resample canonical sequence keys jointly and map them to each run's own history IDs. Report all three effects, conditional intervals, and median/range; do not use an n=24 panel test or present a three-seed bootstrap as strong population inference. Even all-positive signs over three independent seeds give one-sided sign-test p=0.125. More seeds would be an approved Level C extension, not an unreported replication.

| Capability | Existing component | Minimum proposed addition and level |
|---|---|---|
| IDs, parents, access checks, output table | contracts / MetricRecords | Analysis namespace/config for protocol and intervention metadata; A/B, frozen schema unchanged |
| Oracle Q2 and ranks | oracle / FutureOperator | Reuse kernels at p31/p32; B for new histories |
| Public fresh histories | dataset / HMMSampler, PanelBuilder | New stream/lineage adapter; no train latents persisted; B |
| Final readout algebra | analysis/readout, Checkpoint weights | Center WU as C WU and reuse existing readout_projector; pure analysis; C, not required for B |
| Auxiliary decoders | prediction / RidgeProbe | Fit/validation/test orchestration in experiment, following S7; B; auxiliary fitting is not Transformer retraining |
| Frozen intervention and branch enumeration | learner forward, activations hooks | Proposed `FrozenForwardAdapter` with `(checkpoint, public_tokens, site, position, transform)`; **D** because intervention/resume is not a current public API; execution is B |
| PH | topology / DistancePipeline, PersistenceComputer | Existing tools; circular out-of-sample or relative methods separately D |
| Scheduling | experiment, executors | Separate future stage/job, independent store and manifests; no S4/S7 rerun or overwrite |

Proposed intervention metadata contract: source checkpoint/history IDs; site and position; calibration dataset/fit hashes; target definition; transform seed/rank/dose; original and changed logits/probabilities; displacement/support controls; recipient/donor IDs where applicable; status/reason. Aggregate values can be MetricRecords with complete parent IDs. Per-history intervention arrays need a separate versioned analysis artifact or an auxiliary immutable export: decide before implementation; do not expand frozen contracts silently.

Privileged T/E/belief labels live in oracle/analysis/experiment. The frozen forward adapter accepts public tokens and a precomputed transform only; learner/activations must not acquire world, sidecar or oracle access. A privileged target fits an analysis probe, never trains the learner on latent labels. The oracle never sees sidecars.

Checkpoint loading and weight extraction must use the existing experiment resolver and authorized learner/activations consumers. Pass numeric γ/β/WU arrays to pure analysis helpers; do not give `analysis` new direct Checkpoint access or import analysis/oracle code into learner. Preserve the access policy as well as import boundaries.

Planning estimates: final-null algebra/rank audit minutes to 30 minutes CPU; auxiliary extraction/ridge 0.5–2 hours CPU plus1–4 hours for the mandatory nonlinear comparator, with6-hour combined cap; intermediate intervention 0.5–2 hours before exact Q2 branches; ≤2 GB added artifact space if extraction is streamed. One F2 float32 array for 4096 histories is ~20.3 MiB; six hooks ×4096×128 float32 is ~12 MiB per extraction. PH: restrict secondary scans to declared views, with a 2-hour cumulative cap and 8 GB RAM target. Estimates are not measured extension timings. One working week is credible for the adapter, controls and short test after E4, but does not include broad seed/architecture replication.

**Stop rule:** approve/register the concrete protocol before fresh test extraction; run only the selected stage after E4 review and explicit authorization. This document authorizes no implementation or experiment.


## Harness scope and limits of justified claims

X4 is the reference case for [M1–M8](RESEARCH_HARNESS_ARCHITECTURE.md#minimal-contracts-x4-first); implement only B's M1–M3/M7 first. C and D adapters are conditional. No new world, generalized oracle, learner framework or sheaf structure belongs in the immediate X4 implementation.

Information-test success establishes the specified accessibility advantage; finite nonlinear controls strengthen it only within those tested families. Causal success establishes use of a calibrated coordinate-associated component in this frozen suffix; it does not establish necessity of H1. A calibrated strong no-effect result can establish dispensability under the tested interventions, not the irrelevance of every alternative encoding. All previous native p31 and model/trajectory statistical contracts remain in force.
