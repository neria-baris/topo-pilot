# X6: identifiable invariants and local-to-global consistency

13 October 2026; repository snapshot `f8afc2a5e43309aa4bf2d402f2be4e38470df180`. **Proposal only; no new worlds, estimators, inference or training run.** Labels [R/M/L/H/S] follow [Research Landscape](RESEARCH_LANDSCAPE.md). Reuse [X1–X3 plans](../EXTENSIONS.md) and their configs; a config entry is not an implemented world or completed result.

## Revision after E4

E4 reinforces that belief geometry can align without the registered H1 contrast and that learned location structure can arise from last-symbol statistics. H6-B stays a low-cost **estimator/representation feasibility study** until it adds evidence beyond R1/oracle. Add direct R1 circular and spatial controls at identical selected histories, and retain all concentration/scale/local-manifold requirements. E4 is not evidence of boundary, orientation, monodromy or sheaf recovery.

## Governing question

Which particular invariant can be seen in the observation law, retained by an oracle predictive representation, recovered reliably from finite samples, and connected to a defined predictive computation? These are four separate gates. Failure to detect an invariant in learned activations is uninterpretable if an earlier gate fails.

**[M]** T/E may expose only a graph or an equivalence class of stochastic processes. An arbitrary filled complex is not identifiable from vertex emissions and edge transitions. Assume a restricted known family of complexes and a specified metric/emission rule before interpreting statistical recovery as recovery of a surface invariant. State that assumption in every world comparison. Identifying posterior coordinates within a supplied model is weaker than inferring the latent world's topology from unknown observations.

## Invariant-by-invariant research matrix

All entries describe possible tests, not findings. World invariants below are mathematical ground truth; activation estimators require calibration.

| Invariant | Existing planned comparison and actual separator | Observable/predictive gate | Estimator and prerequisites | Priority / levels |
|---|---|---|---|---|
| H0 / connected components | X2a: T²⊔T² has β=(2,4,2), versus one connected torus | Components with identical observation laws remain indistinguishable. Existing shared alphabet and component-specific organization need sequence discrimination. | Oracle component posterior, calibrated H0 gap on concentration strata; uncertain mixtures can fill between clusters. | Later; B world/oracle audit, C training, D disconnected metric handling |
| H1 | Core square β1=0 vs cylinder β1=1 | O belief/futures show the contrast; P does not reliably do so in the registered direction. | Existing GF2 VR, same history IDs, full diagrams/scale/null controls. | Already E3 evidence; A/B extensions, no new training needed |
| Fundamental group π1 | Torus Z² vs Klein `<a,b \| aba⁻¹=b⁻¹>`; genus g surface relation `∏[ai,bi]=1` | Must expose compositions of distinguished transitions/continuations, not only closed-path existence. | Group/loop-relations estimator after calibrated complexes, not Betti counts. | Reserve; C/D; simpler field/boundary invariants first |
| Contractibility | Square contractible; cylinder/Möbius are homotopy equivalent to S1 and noncontractible | Complete predictive quotient may collapse either world. | Known complex proof; absence of finite-sample bars is not a proof. | Mathematical reference; not a new “no holes” discovery |
| Boundary and local homology | Core square has one boundary circle; cylinder two. X1a cylinder two vs Möbius one | Boundary-conditioned beliefs must distinguish regions; posterior mass need not concentrate enough. | Boundary subset H0/H1 first; optional relative local homology after manifold/density calibration. | First X6 candidate; A/B; local relative estimator D |
| Orientability / w1 | Cylinder orientable, Möbius nonorientable, despite identical ordinary homology and π1. Torus vs Klein also differ. | Restricted-family identification plus coherent local frames or appropriate cohomological operations; position emissions alone may alias gluing. | Orientation determinant cocycle / tangent transport, or validated characteristic-class method. | Defer bands/Klein training; B/C/D |
| Higher homology | X1b torus/Klein over GF2 versus GF3; X3 S², T³, S³ | Oracle image must retain a recoverable higher class; entropy-filtering may select a different support. | H2/H3 with landmarks, matched noisy synthetic embeddings, multiple fields, censoring. | Later; C/D, substantial PH costs |
| Monodromy | X1 flipped gluing transports an orientation line with sign −1 around a generator | Predictively distinguishable transport and a specified bundle/connection; ordinary undirected observations may be insufficient. | Products of learned/inferred transport maps; distinguish nontrivial-cycle sign from local curvature holonomy. | Ambitious; B gate then C/D |
| Local-to-global compatibility | Local predictive charts on a calibrated base/cover | Local fits must encode the same physical quantity and overlap correspondence. | Defined sheaf/local system, overlap residual, cycle relation, global-section space. | Research dependency, not an automatic Transformer property |

### Ground-truth distinctions to preserve

**[M]** Cylinder and Möbius band both have Betti numbers (1,1,0) over GF2/GF3 and π1=Z; ordinary homology cannot distinguish them. Their boundary component counts and tangent orientation differ. One boundary component versus two is not by itself an orientability test across arbitrary surfaces.

Torus: βGF2=βGF3=(1,2,1). Klein bottle: βGF2=(1,2,1), βGF3=(1,1,0), integer H1=Z⊕Z/2. The difference involves torsion and top homology, not “the number of loops” alone. Closed orientable genus-g surfaces have β=(1,2g,1); S² has (1,0,1); T³ has (1,3,3,1); S³ has (1,0,0,1). An acyclic space need not be contractible. Keep H1, π1, homotopy type and tangent-bundle invariants distinct.

## Required identifiability/calibration ladder

1. **Observation law:** establish whether candidate models have distinguishable future distributions at the specified horizon, modulo state/symbol relabeling. Exact symmetries or bisimulation-like equivalences defeat an invariant test. Mere unequal matrices are insufficient because equivalent presentations exist. Use null-space/rank arguments and likelihood/future comparisons; do not infer full process identifiability from a finite rank check alone.
2. **Oracle representation:** calibrate the target invariant on belief and joint-future clouds at the same entropy/density stratum as intended for activations. P failing the original H1 contrast is a warning, not a model failure.
3. **Known complexes:** signed boundaries, ∂²=0, Euler characteristic, expected GF2/GF3 homology; verify the actual boundary subcomplex and its components.
4. **Matched synthetic samples:** same M, ambient dimension128, anisotropy/noise and density gaps; compare positive and negative objects. Twenty independently sampled clouds per reference condition; require ≥19/20 correctly classified at a fixed calibrated scale rule.
5. **Estimator prerequisites:** local dimension, neighborhood occupancy, smoothness/reach/noise where needed, and field/scale stability. If activation neighborhoods do not plausibly form a 2D manifold, do not apply a 2D orientation/local-homology theorem to them.
6. **Learned representations:** frozen checkpoints and fresh histories. Report failures of each earlier gate as inconclusive for learned-topology recovery, with their reason.

Controls N and collapsed beliefs demonstrate non-identifiability. U makes current states observable but still does not supply higher-cell incidence without a family assumption. Global cohomological algorithms cannot repair absent statistical information.

## Minimal X6 experiment: boundary organization without training

**[H6-B, one primary hypothesis]** On fresh cylinder-O histories with oracle boundary posterior mass≥0.8, the trained normalized final representation exhibits the same calibrated two-component boundary organization as the oracle belief cloud, beyond initialization and the last-symbol baseline. Competing explanation: belief uncertainty merges the two boundaries, sparse selection fragments any cloud, or trained symbol statistics explain the entire apparent separation.

This is a *conditional representation* claim about boundary neighborhoods. It is not proof that the complete activation cloud is a cylinder or that the model detects physical boundary states.

### Selection and ground truth

In the known cylinder complex, the boundary vertices have y∈{0,11}, with exactly two boundary loops. For square, the perimeter is one boundary circle. Define `B(h)=Σ_boundary b32(z)` in analysis. Select histories by B(h)≥0.8, never by realized latent z; learner/extractor see unchanged tokens only. Label all boundary-coordinate-derived selection and diagnostics `privileged_eval:boundary` because the boundary set comes from the known world, even though b itself uses only observations.

Use existing E3 clouds for feasibility only. For a prospective test, fix the selection rule and scale calibration before generating a new evaluation pool. Require ≥128 selected histories per512-history panel and at least 32 effective samples associated with each cylinder boundary (posterior mass diagnostics only). A lack of qualifying histories is a failed concentration/coverage gate; do not relax0.8 after looking. If approved, allow a predeclared inference-only larger pool up to 32768 histories per process; evaluate eight fixed panels of 512 selected histories only if the pool meets that stronger requirement. Sampling until a target count is met defines a conditional history distribution and must be reported as such; retain all rejected-history counts.

### Estimator and decision

Reuse direct distances and GF2 VR H0/H1; no kNN geodesic replacement. On calibration references define a dimensionless distance ε*/q95 that falls between within-loop connectivity and cross-boundary merging and survives≥19/20 synthetic draws. One frozen rule per representation metric is allowed only if calibrated independently of learned test outcomes; document whether a common normalized scale band works across oracle/activation clouds. If it does not, test comparison is inconclusive rather than choosing different favorable bands from test.

At the fixed calibrated scale band report β0, H0 death gap, H1 per component and full diagrams. Primary success for a frozen cylinder-O model: two components throughout that band in ≥7/8 eligible panels, with the oracle also passing ≥7/8 and that model exceeding its R0 and R1 pass counts. Require this in each of the three models. Square-O, P and random thinning at the same M are negative/comparison controls; no result in them can rescue the primary failure. Do not count tiny outlier components as boundaries: minimum component mass is 20% of selected rows, prospectively fixed.

Positive: stronger learned conditional boundary organization for this cohort. Negative: after oracle/synthetic gates pass, the model fails the specified improvement or R1 accounts for it. Inconclusive: insufficient boundary mass/coverage, oracle merging, calibration failure, censored PH, or support not resembling two boundary neighborhoods. A negative result in P remains restricted by its information gate.

Statistical model unit: three trained replicates of a fixed process. Evaluation units: independent trajectories; conditional-selection counts and intervals are reported. Panels are subsamples, not 24 independent model replicates. Generate canonical-symbol histories and remap public tokens/targets by each model's emission permutation as specified in X4. Jointly resample canonical trajectory keys with explicit mappings to each run's own history IDs; report 2000-bootstrap trajectory intervals for H0 gaps and pass fractions, plus each model's result. Do not base the main decision on p-values over point pairs or a cross-model bootstrap of only three seeds.

Expected cost: existing-cloud feasibility minutes; fresh filtering/extraction and restricted PH roughly0.5–2 CPU hours, capped at2 hours/8 GB RAM initially. Zero new Transformer training. This is lower priority than the X4 information audit because boundary concentration may fail and incremental novelty is limited.

### Explicit R1/spatial controls and strongest boundary conclusion

Use one-hot last symbol, matching token embedding R1, exact b1, exact b32, and R0 under the same boundary-selection rule and aligned sample IDs. Compare their calibrated H0/H1/pass counts and fit-only spatial/boundary-mass decoding. For circular R1 use the same GF47/mid-lifetime procedure where valid; duplicate embeddings can fail estimator prerequisites, and that failure must be reported rather than scored as absence of symbol information. A supervised symbol→sin/cos baseline and same-symbol residual test provide a complementary information control.

Preserve H6-B's ≥7/8 and R0/R1 superiority criteria. If R1 supplies the same apparent boundary structure, the result is primarily feasibility and ordinary spatial organization; with adequate incremental evidence it supports the specified conditional learned representation. Neither outcome proves the whole cloud is a manifold-with-boundary. Unstable clusters and density holes are not boundary evidence.

## Local homology: assess first, add only if justified

**[M]** For an n-manifold interior point, `Hk(M,M\{x};F)` is F at k=n and zero otherwise. At a boundary point of an n-manifold-with-boundary, all these groups vanish. The square's corners are topological boundary points despite metric nonsmoothness. In finite point clouds the raw point-set topology is discrete; the estimator must use a reconstruction/relative complex, not apply this formula literally to512 points.

A candidate multiscale estimator uses `Kε=VR(X,ε)` and subcomplex `Lε,r` induced by points outside a ball B(x,r), then computes the relative chain groups `H*(Kε,Lε,r)` over a predeclared (ε,r) grid. Compare interior versus boundary references and neighborhood stability. Relative H2 requires the relevant boundary maps, including3-simplices for deaths; increasing Ripser maxdim alone does not supply a relative-homology implementation. Current core PH maxdim1 is insufficient.

**[H6-L, optional separate test]** A frozen local-homology boundary score predicts oracle boundary mass beyond a local-density-only baseline on fresh histories. Candidate score: one minus the fraction of calibration-selected (ε,r) grid cells with relative H2 rank one, provided synthetic/oracle references validate that grid as an interior signature. Define positive/negative targets as boundary posterior mass≥0.8/≤0.2; middle cases are excluded prospectively and counted. Use held-out AUROC≥0.75 and improvement≥0.05 over a fit-only logistic baseline using neighborhood counts/radii in all three O models as proposed practical criteria, with paired trajectory intervals. Validation/reference failure makes it inconclusive. High AUROC alone does not prove topological faithfulness; boundary mass may correlate with entropy, density or symbol identity. Match those controls and R1. This is not bundled into H6-B's success rule; the exact relative estimator/grid is a D design dependency to freeze before its test.

First apply prerequisites to known complexes, matched synthetic samples and oracle clouds, then stored activations. If the oracle/cloud does not have a stable 2D local structure, stop this route. [Local homology inference](https://arxiv.org/abs/1008.3572) supplies methods with assumptions, not a guarantee for these history distributions.

## Deferred orientability, higher invariants and architecture realities

**[R]** Only square/cylinder builders are registered in the inspected implementation. Quotient/flip infrastructure exists, but Möbius, Klein, unions, connected sums and higher-sphere configs are proposals. `QuotientLatticeBuilder` accepts 1–3 axes. The planned S³ boundary of a 4-cube therefore needs a dedicated builder/contract review; it is not currently available by merely selecting its YAML family.

Disconnected metric handling also needs review: cross-component graph distances are infinite, while existing WorldSpec/distance validation expects an appropriate metric payload. Define finite intercomponent analysis distances or explicit componentwise/disconnected contracts; do not fabricate arbitrary bridge edges that change H0.

Cylinder/Möbius: after oracle identification gates, first test boundary-component structure (existing X1a concept), then estimate tangent orientation only if local manifold prerequisites hold. A local-frame orientation sign product can detect w1 if the inferred frames approximate the **tangent orientation bundle**. A circle coordinate alone is insufficient because both bands retract to S1. The [Singer–Wu orientability method](https://pmc.ncbi.nlm.nih.gov/articles/PMC3134361/) is related but does not certify an arbitrary activation cloud.

Torus/Klein: calibrate GF2/GF3 H1/H2 signature on known worlds and matched embeddings before models. Field differences in finite-scale VR can be spurious; need a stable calibrated band. New builders and matched training are Level C/D. [Tinarrage's line-bundle method](https://arxiv.org/abs/2005.12543) requires bundle inputs; [Gang's tangent-class preprint](https://arxiv.org/abs/2503.15854) offers a different cohomology-operations route under closed-manifold shape assumptions. Neither makes sparse orientation recovery automatic.

X2/X3: reuse declared constructions and sizes (disjoint tori288, genus2 surface278, S²152, T³125, S³240) but verify all counts from new builders before inference/training. Different N, V, degree and gap complicate comparisons. Prefer H2 on≤400 landmarks; H3≤150 or explicitly approximate witness complexes, with≤10-minute per-call timeout and all censored results retained. Estimate simplex count/memory first; low ambient dimension alone does not control VR combinatorics. Fundamental-group work is deferred until a loop relation unavailable to simpler homology/boundary tests is predictively observable.

## A precise local-to-global object, and its limits

### Orientation local system

**[M]** Choose the known triangulated surface as base space and a good cover of contractible coordinate neighborhoods, with enough neighborhoods to avoid wrapping an entire generator inside one chart. Its overlap graph/nerve is the computational base. Assign stalk R to each chart vertex and overlap edge. On edge e=(i,j), restrictions are `ρi,e=1` and `ρj,e=sij∈{±1}`, from the determinant sign of the tangent chart transition. A global section satisfies `ai=sij aj` on every overlap.

Cycle product `∏sij` is gauge-invariant under changing local orientations. The orientation cocycle represents w1. A connected orientable base admits a nowhere-zero orientation section; a nonorientable one does not, though the zero section always exists. This is not an obstruction to all sections. In a surface nerve, validate face/cocycle relations before interpreting noncontractible cycles; graph cycles introduced by sampling are not automatically world generators.

### Four distinct levels of local-to-global evidence

1. **Local prediction error:** error of a surrogate against exact/held-out predictions within a chart.
2. **Compatibility residual:** discrepancies on explicitly aligned overlaps for the same physical quantity and gauge.
3. **Cycle inconsistency:** product/composition of overlap maps violates a defined cycle relation.
4. **Genuine obstruction:** a nontrivial class or prescribed-data extension failure in a declared cochain/relative complex, with admissible adjustments and chain relations.

Approximation error, missing overlap, wrong correspondences and unmatched gauges can cause the first three without the fourth. At the final layer one global affine readout restricts compatibly to every chart; the intermediate nonlinear suffix is also globally defined. An inconsistent local affine approximation does not obstruct that actual function. If a fitted sheaf is later justified, define stalks/restrictions/δ/δ² where applicable and approximation-controlled reference calibration first.

### Concrete observable transport task — before any training

**[M/H]** This is a complete future task definition and analytic observability argument, not a run or a finding about current models. Start with a **fixed cylinder base**6×4 (24 vertices), nearest-neighbor symmetric lazy max-degree walk: each base neighbor probability.2, self-loop1−.2degree. This is a new task size, not a change to the12×12 pilot.

Fiber s∈{−1,+1}; hidden state(z,s),48 states. Compare two flat Z2 edge local systems on the **same** base: g_e=+1 everywhere (trivial), versus g_e=−1 only across the x-wrap seam at each y (twisted). Opposite edge directions share the same sign, all face products+1, contractible-loop product+1, winding-generator product−1 in the twisted arm. This is Möbius-type **line-bundle transport over a cylinder**, not a nonorientable cylinder tangent bundle.

For every base move, including self g=+1,

T_lift((z,s),(z',s'))=T_base(z,z')[(1−η)1{s'=g_e s}+η1{s'=−g_e s}], η=.02.

Both arms are connected with uniform stationary law, equal unsigned T_base, movement/boundary/occupancy and noise. Noise prevents “one lift connected, the other disconnected” from becoming the intended separator. Use μ0=π=uniform48. Mathematical transport signs remain exactly flat; noisy trajectories are not themselves exact global sections.

Observations give a unique **anonymous** base symbol w_z. At one interior anchor a=(0,1), emit sign-specific w_a,+ or w_a,− with probability r=.5, otherwise masked w_a; all other vertices emit only w_z. Alphabet26 (24 masked/base symbols +2 sign cues). This intentionally exposes base paths like a U-style positional process while hiding the sign away from the anchor. It is a controlled transport-memory task, not a claim that topology must be learned from unnamed coordinates.

Exact oracle target is Q1 of the next public symbol, especially P(w_a,+|h); joint Q2 optional. Current BayesFilter/FutureOperator numerical kernels can handle lifted T/E, but current WorldSpec vertex count24 and hidden process count48 cannot be silently conflated. A future base↔fiber state adapter/typed metadata must represent this difference. No generalized oracle is necessary for this finite HMM.

**Finite-history witness.** Observe w_a,+ (sets s=+1), follow a six-edge positive winding path around y=1, and return to a with masked w_a. No intermediate visit to a. This has positive probability in both arms. Given the path, E[s_end|h]=(1−2η)^6 ∏_e g_e. Thus the conditional difference in next-step P(w_a,+|h) between trivial and twisted arms is

T_base(a,a) r (1−2η)^7 > 0.

At this interior anchor T_base(a,a)=.2. The formula is an analytical witness, not a computed experimental effect estimate. A length-six contractible rectangle (two x edges, one y edge, return) from the same anchor, avoiding the seam and intermediate anchor, has product+1 in both arms. It ends in the **same last masked symbol**, with the same length and initial sign cue. The two histories distinguish transported information from last-symbol-only prediction.

Stationary observed unigrams and bigrams are **equal** across the same-base pair: a sign is revealed only at a; adjacent double reveals require the anchor self-loop, whose g is+1 in both arms. Uniform fiber prior makes single reveals identical. Longer conditioned paths expose the cycle sign. This controls local observed statistics without pretending to match all future laws (which would remove the target distinction).

**Nulls and limits:** with r=0 the fiber is never visible, and both same-base observation laws are exactly equal. With η=.5 transport memory is lost after a step, also making g unobservable. Either is NO-GO for a transport-learning claim, not a reason to train anyway. A gauge change must transform fiber emission coordinates as well as signs; arbitrary relabeling of one without the other changes the task. A finite-state/one-bit transport predictor and last-symbol/bigram baselines are mandatory. An ordinary memory automaton can solve the task without embedding a Möbius manifold.

Before any neural training, authorize only an exact-oracle audit if this direction is selected: validate lifted kernels/face signs/gauge invariance, prove/check the finite-history conditional gap and equal local laws, estimate how often witness-like histories occur under natural sampling, and freeze natural versus challenge evaluation. Rare-event enrichment changes the evaluation distribution and must not masquerade as natural generalization. Training budget and replication are a later decision, not a default12-run campaign.

### Actual cylinder–Möbius orientability case

For an architectural/world stress case use6×5 bases (30 vertices): cylinder gluing (x+6,y)~(x,y), Möbius gluing (x+6,y)~(x,4−y). Center y=2 is fixed by the flip, so one six-edge winding returns to an interior anchor. Tangent determinant transport around that generator is+ versus−. Lift/base indexing becomes60 states and alphabet32 under the same anchor mechanism; the finite-history witness above applies.

Both bases still have β=(1,1,0), π1=Z. Boundaries are two versus one, and base adjacency differs away from the center: the actual pair is **not** locally observation-law matched globally. Use within-base trivial versus orientation-line transport controls to separate chosen fiber information from boundary/gluing differences; do not launch a four-arm training factorial by default. Validate a registered Möbius builder and signed incidence first. A trained model's transport-memory success would not establish that its activations are nonorientable or that tangent w1 is represented.

### Minimal sheaf/relative-section example

Take the known cycle C_L as base (or a good-cover nerve), stalk R at vertices/edges, restrictions ρ_i,e=1, ρ_j,e=g_e. Define δa_e=a_i−g_e a_j. Global sections are kerδ; nontrivial product−1 allows only zero, whereas product+1 allows a one-dimensional nonzero family. Prescribing a0=1 at the anchor has no compatible extension in the twisted case.

This is a precise constrained extension obstruction. Twisted absolute H1(C_L;R_g) is zero, so it must not be described as a nonzero absolute H1 class. If cohomological reporting is wanted, explicitly construct the relative complex for the anchor subspace: the connecting map from prescribed anchor data to relative H1 carries the extension obstruction. Until that contract/solver is defined, report the algebraic nonextension and monodromy only.

The observable anchor task above couples that known cycle product to a future law. It therefore gives local-to-global mathematics a predictive consequence without imposing a sheaf on arbitrary activations. General O(d) holonomy around contractible loops can come from curvature; the flat Z2 face relations and winding sign here instead expose global transport. Architecture reuse is detailed in [CasesB/D](RESEARCH_HARNESS_ARCHITECTURE.md).

## Interfaces, artifacts and stop rules

| Proposed task | Modules and minimal integration | Level |
|---|---|---|
| Boundary subset test | contracts IDs/access; world boundary incidence in analysis; oracle b; topology existing H0/H1; analysis selection; prediction regret; experiment record/export | A reuse; B fresh histories/extraction |
| Relative local homology | Pure relative-complex adapter in topology, analysis scale/prerequisite calibration; existing learner untouched | D estimator interface, B use |
| Orientation/field comparison | Registered world family; process strategy compatibility; dataset/oracle calibration; topology field tests; learner/activations unchanged architecture | B gates, C models, D builder/estimator |
| Higher/disconnected worlds | World/disconnected-metric contract review; optional PH backend declared explicitly, no silent production use of test-only gudhi | C/D |
| Predictive transport task | Versioned fiber/world/process definition, observable emissions, oracle adapter and transport metadata | C/D after identifiability proof |

Future boundary artifacts need selected history IDs, original panel membership, selection counts/weights, boundary definition/world parent, oracle posterior masses, calibrated scale rule, component assignments, complete diagrams, and bootstrap method/status in MetricRecords. Local methods additionally need anchor IDs, neighborhoods, relative complex/field parameters, calibration parents and failures. Sheaf methods need base/cover IDs, stalk dimensions, restriction maps, face relations, gauges and loop representatives. Keep privileged target definitions out of learner/activations; their outputs are joined only in analysis.

**Stop:** no new training until the oracle and estimator gates pass. If boundaries are not identifiable/recoverable, publish that limitation in the pilot and prioritize X4 instead. If monodromy has no distinguishable observation consequence, abandon that task formulation. Do not initiate any extension as part of preparing this package.


## Shared harness and priority

A holds typed complex/boundary/local-system ground truth; B holds the observation process or future lift; C holds task-specific exact references; D remains the existing Transformer; E/F separate invariant definitions from calibrated estimators; G declares fiber/observation/computation changes; H reports typed evidence with six scoped gates. No universal scalar invariant is introduced.

Boundary H6-B remains optional and cheap after X4, with limited expected novelty after E4. Orientation/transport/sheaves are longer-term: the finite-history argument makes one formulation concrete, but occurrence/power/oracle/indexing/calibration must precede new worlds or training. X5 G1 is the chosen first architectural stress test if a follow-up is approved; local-to-global machinery is deferred.

Strongest possible transport result: the model predicts a finite-history transported-sign consequence beyond last-symbol/local-statistic baselines. Stronger unjustified claim: the model learned the base's abstract orientability, requires nontrivial activation topology, or has a genuine learned sheaf-cohomological obstruction. Failed observational identification permanently stops that formulation until a separately specified task changes the observation mechanism.
