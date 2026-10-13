# Minimal reusable mathematical research harness

13 October 2026; evidence snapshot f8afc2a5e43309aa4bf2d402f2be4e38470df180. **Architecture proposal only; no implementation or experiment was built.** The harness supports [X4](X4_CAUSAL.md), [X5](X5_GEOMETRY_OPTIMIZATION.md) and [X6](X6_TOPOLOGICAL_INVARIANTS.md), not a new scientific claim. Begin with the [X4 audit](X4_NEXT_EXPERIMENT.md), then stop. The eighth-document amendment supersedes the earlier seven-document deliverable.

## Rationale and scope

The shared question is which structures of a hidden information-generating world are observable, represented, used by predictive computation, and relevant to learning/generalization. Reusing immutable artifact lineage and exact HMM kernels helps answer it; a generic “topology score” would obscure it.

The minimum viable harness is a versioned task/horizon specification, read-only input resolution, existing oracle kernels, two pure X4 diagnostics, and provenance-rich reports using existing contracts. X4 Phase B needs neither a new learner interface nor new sampling, fitting or intervention. C adds only fresh-lineage and estimator adapters; D adds a validated frozen-forward adapter if authorized. The harness remains subordinate to these scientific questions.

A world need not be a manifold: it may be a graph, filled cell complex or other finite structure. Higher cells generally cannot be identified from a stochastic law on the same vertices/edges. Different worlds can have identical observation laws; different processes on one world expose different structures.

## Eight conceptual layers and existing ownership

| Layer | Object, semantics and owner | Boundary to preserve |
|---|---|---|
| A World/Structure | world/contracts: cells/incidence, boundary, indexing; optional metric or local-system metadata | No manifold, metric or sheaf requirement for every world |
| B Generative Process | process/dataset: hidden states, T/E, μ0, π, sampler, optional transport | Hidden process state may differ from base vertices; initial and stationary laws differ |
| C Task/Oracle | oracle/prediction: visible history, horizon/target/order, reference and equivalence | Retain exact HMM kernels; task-specific adapters allowed, no GeneralOracle |
| D Learner/Representation | learner/activations: current Transformer, training, hooks/checkpoints | Token-only access; no unnecessary generic model API |
| E Property/Invariant | analysis/topology/world: definition, ground truth, assumptions and references | Q2 sufficiency, H1, w1, curvature and section obstruction are distinct objects |
| F Estimator/Calibration | prediction/topology/analysis: samples/procedure, scale/budget, uncertainty/failures | Failed calibration is not evidence that the learner lacks a property |
| G Intervention | experiment plus process or frozen-forward adapter | State exactly what changes/fixes; distinguish observation, process and computation changes |
| H Evaluation/Report | prediction/analysis/experiment/executors/contracts: typed metrics/units/parents | Reusable reporting is not a universal score or automatic numeric comparability |

These are responsibilities, not eight proposed classes/directories. Preserve all twelve components and access/import policies. Prediction fits/scores auxiliary estimators; topology owns calibrated structural estimators; analysis joins permitted diagnostics; experiment resolves/orchestrates; executors provide existing optional job support.

~~~mermaid
flowchart LR
    A["A world / optional structure"] --> B["B stochastic process"]
    B --> O["C task-specific oracle"]
    B --> P["Public token histories"]
    P --> D["D current Transformer / hooks"]
    A --> E["E typed property definition"]
    E --> F["F estimator + calibration"]
    O --> F
    D --> F
    G["G specified intervention"] --> B
    G --> D
    O --> H["H metrics / uncertainty / provenance"]
    F --> H
    D --> H
~~~

Privileged A/B metadata enter oracle/analysis, not the learner. G→B is a future process experiment; G→D a computation intervention. No arrow schedules execution.

## Shared scientific gate protocol

| Gate | Question | Stop interpretation |
|---|---|---|
| 1 Definition | Is the property mathematically defined for this object/comparison? | Undefined domain, coefficients, metric or restrictions: stop |
| 2 Observability | Can public finite histories expose the distinction? | Nonidentifiable structure: no learned recovery claim |
| 3 Oracle/reference calibration | Does the reference retain it, and can the estimator detect it? | Failed precision/scale/coverage: inconclusive representation claim |
| 4 Representation | Does the model encode the information or display a calibrated signature? | Recovery alone does not establish computation uses it |
| 5 Function | Does a specified downstream computation use it under interpretable interventions? | Damage confounds may limit the claim to coordinate-associated use |
| 6 Learning/generalization | Does a controlled comparison affect learning or held-out prediction? | Confounds restrict causal and population interpretations |

Experiments can stop at any gate; not all six are obligatory. A failure upstream constrains downstream claims. Oracle exactness/approximation is task-specific. Protocol-local GO/NO-GO/INCONCLUSIVE records do not replace core GateReports or G-H. A sampled observability NO-GO is not a theorem about all reachable histories, a finite decoder failure is not information-theoretic impossibility, and E4 representation results do not pass Gate5.

## Minimal contracts: X4 first

These are protocol/adapter contracts, not universal schemas. Every identity includes protocol/config hash, producer commit and complete parent IDs. If a frozen type cannot represent an output faithfully, review a versioned analysis export rather than silently expanding the core type.

### M1 — task and input manifest: experiment/contracts, first B

**Purpose:** fix conditional task and domain. **Inputs:** selected world/T/E/μ0/π/history/oracle IDs, p32, joint horizon2, lexicographic order, split IDs, canonical↔public mapping, precision/coverage settings. **Outputs/semantics:** versioned protocol and resolved parent map defining the exact future-law comparison. **Validation:** complete immutable parents, shape/index/prior/position agreement, splits and privilege flags. **Identity:** protocol/source hashes. **Dependencies:** current resolver/contracts/HistoryIndex; no checkpoint in B. **Errors:** missing parent, incompatible vocabulary/indexing or unsupported prior; never substitute “latest.” **Change:** small isolated experiment function.

### M2 — HMM future adapter: oracle/experiment, first B

**Purpose:** reuse exact kernels without leakage. **Inputs:** T/E, lawful initial law, stored beliefs or existing public tokens. **Outputs/semantics:** float64 b/Q1/joint Q2/G1/G2 with ordering; stored float32 F2 is separately identified. **Validation:** stochasticity/posterior/joint normalization, nonnegative probabilities, marginalization and precision reconciliation. **Identity:** process/history/horizon/order/precision. **Dependencies:** BayesFilter, FutureOperator.F1/F2/observability_matrices unchanged. **Errors:** invalid shape/alignment or normalization; numeric instability→inconclusive. **Change:** small orchestration wrapper, no new GeneralOracle.

### M3 — horizon feasibility: analysis, first B

**Purpose:** separate ambient algebra from reachable practical evidence. **Inputs:** numeric G1/G2/b/Q1/Q2, canonical mappings and frozen anchor/neighbor settings. **Outputs/semantics:** tangent spectra/null residuals, neighbor gaps/coverage, distinct exact/numerical/practical verdicts and reasons. **Validation:** full null dimensions, sum-zero orthonormal basis, rank tolerance sensitivity, same-symbol coverage, known-answer fixtures. **Identity:** M1/M2 plus selection/tolerance hashes. **Dependencies:** pure linear algebra, no checkpoint/PH/fitting. **Errors:** instability/coverage inconsistency→inconclusive. **Reuse limit:** future tasks with linear predictive maps only; no assumption all oracles have them.

### M4 — representation view: activations plus pure analysis/readout, first C

**Purpose:** aligned final effective/null features. **Inputs:** tokens/checkpoint through authorized consumer, dev resid_post_3, numeric γ/β/WU. **Outputs/semantics:** u/null/Peff/rank and reconstruction diagnostics. **Validation:** ε=10^-5, correct hook/position/weights, final-LN/logit reconstruction and centered-logit invariance. Reuse existing readout_projector with centered WU_effective=C WU. **Identity:** checkpoint/extraction/task/formula hashes. **Dependencies:** current hooks and pure readout math; analysis gets no direct Checkpoint access. **Errors:** missing hook/incorrect reconstruction invalidates view. **Change:** orchestration only; intermediate hooks deferred.

### M5 — estimator bundle: prediction/experiment, first C

**Purpose:** retain primary J and mandatory nonlinear secondary separately. **Inputs:** common split/target ordering, fit-only normalization, ridge grid, matched MLP budgets and random/R1/shuffled controls. **Outputs/semantics:** predictions/losses/parameter counts/hyperparameters/seed lineage and separate decisions. **Validation:** no test selection, raw-MSE semantics, optimizer/parameter/covariance matching. **Identity:** feature/target/split/fitter/config/seed hashes. **Dependencies:** RidgeProbe plus explicit small MLP adapter. PredictionStage.run_probes is currently an I/O stub, not this runner. **Errors:** crash/budget mismatch/ceiling/leakage recorded, never drop a seed. **Change:** auxiliary estimator only; no fitting in B.

### M6 — fresh-lineage sampler: dataset/experiment, first C after GO

**Purpose:** genuinely prospective evaluation. **Inputs:** approved unchanged process, named stream, new sequence-ID namespace, canonical naming,4096 trajectories/process. **Outputs/semantics:** public ObservationSets/HistoryIndex, separate reference outputs, same canonical trajectories across model permutations. **Validation:** disjoint lineage, remapping and oracle equivalence. **Identity:** process/stream/namespace/map hashes. **Dependencies:** HMMSampler/PanelBuilder; no core DatasetStage rewrite. **Errors:** collisions/unproven independence→stop. **Change:** adapter, not automatic sampling in B.

### M7 — typed report bundle: analysis/experiment/contracts, first B

**Purpose:** report scoped claims/uncertainty/provenance. **Inputs:** measurements, protocol-local gates, parent graph, model/trajectory units, runtime/censoring. **Outputs/semantics:** existing MetricRecords plus gate narrative and versioned numeric exports where necessary. Q2 MSE, KL nats, PH diagrams, τ intervals and monodromy signs remain different types. **Validation:** units/normalization, all planned seeds/controls/failures, checksums. **Identity:** source/producer commits, parents/report settings. **Dependencies:** current store/report tools, optional executors. **Errors:** missing lineage/unsupported schema forbids report-level success. **Change:** no core gate recalculation or S7/S8 calls.

### M8 — precise intervention: learner/experiment, first D only

**Purpose:** frozen suffix computation test. **Inputs:** authorized checkpoint, public tensor, site/position, precomputed analysis transform/calibration/dose. **Outputs/semantics:** logits, vector/control diagnostics, aligned losses and metadata. **Validation:** identity reconstruction, one patched vector, fixed context, rank/displacement/predictive-damage/support controls. **Identity:** checkpoint/history/site/position/transform/seed parents. **Dependencies:** new frozen-forward/resume adapter; currently absent. **Errors:** reconstruction/support mismatch→mechanistic inconclusive. **Defer:** native p31 branches must reapply original-prefix patch and leave appended p32 unpatched.

## Experiment compatibility matrix

Future cells are designs, not available implementations. Architectural reuse never substitutes for scientific comparability.

| Requirement | X4 | X5 | Möbius/orientability | Sheaf/local-to-global |
|---|---|---|---|---|
| 1 Unchanged | Core worlds/processes, HMM kernels, frozen model, store/ridge/PH | Cylinder cells/O E, HMM/trainer/extractor/store | Store/trainer/extractor; HMM numeric kernels if finite lift | Store/report/learner; HMM only for finite lifted task |
| 2 Adapter | B audit/report; C lineage/MLP; D patch | Metric payload/weighted T/paired schedules | Flipped builder, base↔fiber indexing/targets | Cover/cochain metadata/exact compatibility |
| 3 New mathematics | Specified tangent audit, no general abstraction | f(y)/curvature/conductance/rate/spectra | Tangent orientation cocycle versus chosen line system | Stalks/restrictions/δ/chain relations/relative obstruction |
| 4 New process | None B; same law new histories C | Explicit metric-coupled symmetric T | (base,sign), noisy transport, anchor cues | Only chosen observable transport/constraint mechanism |
| 5 Oracle | Existing exact oracle | Existing kernels/new process inputs | New state indexing/reference construction; exact lifted HMM | Task-specific solver; transport HMM where valid |
| 6 Estimator | C MLP; later erasers; PH reused | Censored hitting time/rate/mixing; PH calibration | Gauge-invariant cycle signs; tangent methods conditional | Local/overlap/cycle/relative-obstruction diagnostics |
| 7 Intervention | Final null control; intermediate patch later | G0 metadata; G1 T change; rate reference | Same-base trivial/twisted sign system; η=.5/r=0 | Named restriction or anchor change; no arbitrary activation sheaf |
| 8 Training | Zero new Transformers | Six paired models after gates/approval | Deferred until observable/power audit | Deferred; chosen transport study may suffice |
| 9 Validity risk | Ceiling/capacity/unreachable nulls/R1/off-support | Rate/mixing/entropy/GC/censoring/three pairs | Same H1, boundary/adjacency, fiber≠tangent bundle | Approximation≠cohomology; zero section; undefined complex |
| 10 Minimal reuse | Existing-artifact B, conditional C | One paired G1 with current oracle/regret/lineage | Exact finite-history witness + same-base control | Known cycle/restrictions/anchor and exact observable transport |

Numbers require matched task/alphabet/units/target/sampling/calibration. A26/32-symbol transport task cannot be ranked against36-symbol pilot KL by raw numbers. Shared risk reporting does not establish equal Bayes difficulty; shared PH code does not make w1 and H1 interchangeable.

## Four conceptual cases

### A — X4 reference trace

A provides core cylinder/square complexes; B supplies O/P T/E/uniform prior; C supplies p32 exact Q1/Q2; E defines horizon equivalence, not “world topology learned.” Phase B uses M1–M3/M7 through Gates1–3 with existing unblinded test/dev histories and stops.

After GO plus new authorization, M6 creates prospective histories, D/M4 gives frozen representations, F/M5 tests affine/nonlinear accessibility, H reports unchanged J plus secondary capacity results at Gate4. Existing H1 can supply context under calibration but is not required for the Q2 audit. Later G/M8 tests coordinate-associated use at Gate5 with y/local-position/R1/generic-predictive controls. PH alteration is separately measured. Native p31 is conditional; p32 cannot append beyond the learned positions.

### B — actual cylinder versus Möbius band

Both retract to S1 with β=(1,1,0), π1=Z; ordinary H1 cannot distinguish orientability. Actual Möbius needs a validated flipped-boundary builder and tangent signs. Future tractable pair:6×5 bands, seams (x+6,y)~(x,y) versus (x,4−y),30 base vertices. Center row y=2 closes after one6-edge winding. Hidden(base,sign) carries orientation transport, η=.02 noise. Anonymous base emissions reveal sign only at an interior anchor with r=.5.

A cue followed by a winding path and masked return changes the next anchor-sign law. Exact finite lift reuses HMM numeric kernels after adding correct60-state indexing. [X6](X6_TOPOLOGICAL_INVARIANTS.md#concrete-observable-transport-task--before-any-training) gives a finite-history proof and same-base control. Actual bands differ in boundaries/adjacency; compare each against its own trivial/twisted line system before attributing a difference to orientation. A Möbius-type fiber over a cylinder does not make the cylinder tangent bundle nonorientable.

New E/F requirements: orientation cocycle/cycle products and validated gauge changes; tangent-frame estimators require local manifold evidence. Do not infer a Möbius activation structure simply from generator gluing. Training remains deferred.

### C — worked future stress test: X5 G1

Choose **X5 G1** as the first architectural extension if a learning comparison is selected later. It changes a familiar process input while keeping task/oracle semantics. This tests boundaries cheaply and does not authorize training or outrank X4.

A retains12×12 cells; f0=R, fa=R[1+.20cos(2πy/11)], R=12/(2π), equal continuum area132 and K=−f''/f. B defines lhorizontal=f(y)2π/12, lvertical=1, c=1/l², T_off=.8c/Ca and diagonal residual. Both kernels are symmetric/lazy, π=μ0=uniform, E the same numeric O array. This graph walk is not automatically Laplace–Beltrami diffusion.

G0 changes only metric metadata: same T/E/μ0, exactly same law, no duplicate training. G1 changes T/law; G2 changes distance-based E separately. C reuses HMM kernels for entropy/GC/regret; F/H reuse paired oracle-relative learning endpoints/censoring. D trains six new models only after gates/approval.

Measure movement/gap/mixing/correlations/entropy/GC before learning. Scalar speed matching is diagnostic, not a curvature isolation; remaining mismatch limits the conclusion to these coupled processes. Representation geometry requires its own calibration; generalization requires frozen rare/shift rules and the corresponding oracle, not a training-speed inference.

### D — minimal local-to-global predictive example

Base is a known cycle C_L (also a cover nerve); vertex/edge stalks R, restrictions1 and g_e∈{±1}; δa_e=a_i−g_e a_j. Sections satisfy δa=0. Gauge changes transform local coordinates/restrictions; cycle product is invariant. Product+1 gives a1-dimensional section space, product−1 only zero.

Prescribe anchor a0=1: twisted transport has no compatible extension. This is a constrained nonzero-section obstruction, not absence of all sections. Twisted absolute H1 on the cycle over R is zero; do not label it a nonzero absolute H1 class. A defined relative complex including the anchor can express the extension obstruction; otherwise report the proved constrained inconsistency only.

Anchor-sign transport in CaseB/X6 gives an observable predictive consequence. Known restrictions and exact lifted oracle calibrate it against trivial transport, η=.5 and r=0. No fitted activation sheaf is required. Later learned transport must distinguish local error, overlap residual, cycle inconsistency and a genuine class in a declared cochain complex. A global nonlinear Transformer function is not obstructed because local affine surrogates disagree.

## Incremental implementation and deferrals

**Stage1 X4 only:** B=M1–M3/M7, C conditionally M4–M6, D conditionally M8. Preserve oracle/store/access policies. Scientific NO-GO stops the branch; architectural milestones cannot override it.

**Stage2 one extension:** X5 G1 tests world/metric versus process/task separation, adding only metric/weighted-kernel/learning-endpoint adapters. No simultaneous Möbius campaign. If X5 science is not chosen, a separately scoped exact-oracle transport audit can be considered instead; do not build both to demonstrate modularity.

**Stage3 local-to-global, deferred:** only after a precise observable task and exact-reference argument, add base↔fiber state, transport/gauge validation, cover/stalk/restriction/cochain records and constrained-section solver.

For every generalization ask: would postponement simplify X4 without materially increasing later cost? Yes for universal world/metric/property interfaces, multiple-architecture wrappers, GeneralOracle, universal PH/sheaf engine, automatic gate DAG, configuration DSL, cross-task scores, generalized nonuniform occupancy and transport bundles. **Postpone them all.** Protocol fields plus pure numeric functions suffice for B.

## Risks and revision/rejection conditions

Scientific risks: representation≠use, unobservable higher cells, near equality≠strict sufficiency failure, finite PH/density, curvature/process confounds, fiber monodromy≠tangent orientation. Enforce scoped gates and typed results.

Software risks: schema inflation, latent leakage, unauthorized checkpoint access, symbol/history misalignment, stale “latest” parents, shared-store overwrites and analysis imports into learner. Use explicit immutable IDs, existing access/import policies and independent outputs.

Revise the design if X4 cannot be expressed honestly in current artifact semantics, if a concrete second task requires a distinct oracle, or if an existing contract prevents a justified small adapter. Reject an abstraction if it delays B, forces unused fields/classes, bypasses access policy, silently alters core contracts or lacks demonstrated two-case reuse. Reject a scientific formulation when observability fails rather than expanding the platform.

Success means B can give an auditable answer with the pilot untouched, and one later selected task can reuse valid infrastructure without weakening mathematical semantics. No implementation follows automatically.

