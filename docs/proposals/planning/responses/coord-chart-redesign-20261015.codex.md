STATUS: PROPOSAL

**Summary**

K4 established a failure of its frozen chart construction, not a failure of circular structure or history dependence. Persistent H1 can exist in one component while other landmarks remain disconnected. Selecting the longest H1 bar and its midpoint gives no connectivity guarantee.

E4 does **not** provide an independently validated solution to this problem. It uses essentially the same persistence and midpoint choices, but permits disconnected graphs, assigns their components independent offsets through a minimum-norm solve, and does not certify integer closure or primitive winding. Its reported 0.88–0.89 agreements are descriptive panel summaries.

I recommend approving **one diagnostic-only job first**, restricted to model 1729, panel 1. It should reproduce the original distance/persistence calculation and report the selected bar, component sizes, nearest-neighbour distances, connectivity threshold, and float32/float64 filtration differences. It should produce no phases, oracle comparisons, endpoints, or alternative charts.

If the owner subsequently approves a redesign, my preferred candidate retains all landmarks and uses one deterministic scale inside the intersection of the selected bar’s lifetime and the connected-graph regime. If that intersection is empty, stop this route. Retain exact lifting, primitive normalization, extension, and existing substantive validation gates. Do not introduce an automatic component-trimming or denoising fallback.

Every redesigned result on E4 histories remains exploratory. Confirmation should use independently sampled histories after the chart and complete evaluation rule are frozen. C1 needs an explicit successor protocol; its present freeze remains blocked.

This document authorizes no execution and changes no frozen result.

---

# Chart-construction redesign proposal

## 1. Authority, scope, and evidence

This proposal follows the [planning protocol](X:/Downloads/projects/topo-pilot/agent-handoff/planning/PLANNING_PROTOCOL.md), the [owner policy](X:/Downloads/projects/topo-pilot/agent-handoff/archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md), and the “Owner research charter” in [NEXT_RESEARCH_AND_WORKFLOW.md](X:/Downloads/projects/topo-pilot/agent-handoff/NEXT_RESEARCH_AND_WORKFLOW.md).

Owner policy B3-A requires preserving K4’s INCONCLUSIVE result without rescue. B6 requires an owner decision before changing a frozen criterion. A successor study can be scientifically worthwhile, but it must have its own identity, authorization, review, freeze, and results.

The inspected research repository is at `c2046fc7426d25779da4be74b86f92a8119924a5`. Job 0018 executed scientific source `ab2be87`; its subsequent state commit was `c2046fc`.

The authoritative execution evidence is [job 0018 report](X:/Downloads/projects/topo-pilot/agent-handoff/jobs/0018/report.md) and [review](X:/Downloads/projects/topo-pilot/agent-handoff/jobs/0018/review.md):

- Identity and process/reference gates passed.
- Model 1729’s calibration chart reached exact integer lifting successfully.
- Primitive normalization stopped because the selected-scale graph was disconnected.
- No gauge, extension, fidelity, phase-coverage, precision, or scoring result was obtained.
- Models 2718 and 3141 were not charted.
- The selected bar and component counts were not persisted.

[C1-FROZEN-v1 §14](X:/Downloads/projects/topo-pilot/agent-handoff/planning/responses/C1-FROZEN-v1.md) therefore selects its stop branch. Its “construct once” branch cannot be invoked: K4 did attempt chart construction.

During this planning pass, I read source, documents, configuration, reports, and installed dependency source. I did not run Python, tests, diagnostics, sampling, training, or scientific payload access. I made no file or git changes and did not consult the parallel planner’s response.

## 2. Exact comparison of K4 and E4

The relevant implementations are:

- [K4 chart.py](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/tools/x4_circle_history/chart.py)
- [K4 cochain.py](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/tools/x4_circle_history/cochain.py)
- [E4 CircularCoordinates](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/src/topo_pilot/topology/circular.py)
- [E4 correspondence analysis](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/src/topo_pilot/analysis/circular.py)
- [S7 experiment](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/src/topo_pilot/experiment/s7_circular.py)
- [E4 reporting](X:/Downloads/projects/topo-pilot/topo-pilot-circle-history-k4/src/topo_pilot/experiment/report_e4_s7.py)

| Feature | E4 S7 | Frozen K4 |
|---|---|---|
| Input geometry | Raw activation cloud; Euclidean distances | All 512 calibration landmarks; raw 128-dimensional Euclidean distances |
| Persistence | Ripser, H1, F47, cocycles; explicit threshold `D.max()` | Ripser, H1, F47, cocycles; default threshold |
| Bar selection | First `argmax(death-birth)`; no explicit finite/positive filter | Largest strictly positive finite lifetime; ties by birth, death, index |
| Scale | `birth + 0.5*(death-birth)` | `(birth+death)/2` |
| Edge graph | Distances ≤ scale | Distances ≤ scale |
| Initial cochain | Centered, oriented residue representative | Same basic centered, oriented construction |
| Integer closure | Not checked or repaired | Exact closure/congruence checks; bounded integer correction if needed |
| Connectivity | Disconnected graph accepted | Entire landmark graph must be connected |
| Primitive winding | No period-gcd normalization | BFS potential, nonzero period gcd coprime to 47, primitive normalization |
| Smoothing | Dense Laplacian normal equations; minimum-norm `lstsq` | Anchored sparse incidence least squares; explicit residual check |
| Phase sign | Solves approximately \(Bf=\alpha\) | Solves approximately \(Bf=-\beta\) |
| Gauge | Agreement statistic removes one global rotation/reflection | Calibration-only reflection/rotation fitted against the complex moment \(m_{32}\) |
| Out-of-sample map | None | Saved chart and fixed eight-neighbour Gaussian extension |
| Panel handling | New transductive coordinates fitted separately on each panel | Calibration chart fixed before validation; direct validation chart only a comparator |
| Evaluation | Latent-angle agreement and permutation null, descriptive | Belief-residual history endpoint after chart/support/precision gates |

Two qualifications matter.

First, the midpoint formulas are algebraically equivalent but can differ in their final floating-point bit. The persistence thresholds and tie rules also differ. Consequently, one should not claim the two programs necessarily select identical numerical complexes on every input.

Second, when the graph is connected, the centered lift is already closed, the primitive gcd is one, and numerical solves agree, the smoothing constructions are related by reflection, a constant, and an integer-valued vertex potential. In that special case their circle-valued outputs should agree up to gauge. Those premises have not been established for the failed panel.

On a graph with \(c\) connected components, the Laplacian has \(c\) constant-offset freedoms. E4’s minimum-norm convention chooses offsets computationally; the data graph does not identify their relative values. A global agreement statistic removes only one rotation, not arbitrary componentwise rotations.

The published E4 cylinder-O values—approximately 0.884–0.892—summarize per-panel descriptive agreement with the latent angle. They neither certify panel-1 connectivity nor validate extension to new histories. `report_e4_s7.py` aggregates existing metrics; it supplies no additional chart certification.

The mathematical distinction between persistent-class selection, integral lifting, and smoothing is part of the original circular-coordinate construction. [Persistent Cohomology and Circular Coordinates](https://arxiv.org/abs/0905.4887)

## 3. Diagnosis from code and mathematics

### 3.1 The structural explanation

Write the selected bar as \([b,d)\), with midpoint

\[
r_m=(b+d)/2.
\]

Let

\[
r_c=\min\{r:G_r\text{ connects all landmarks}\},
\]

where \(G_r\) contains all edges of length at most \(r\).

For a complete weighted graph, \(r_c\) equals the largest edge weight of a minimum spanning tree. No general inequality forces \(r_c\le r_m\), or even \(r_c<d\).

A dense subset can support a persistent loop while a remote point or separate cluster remains disconnected until after that loop dies. H1 persistence and whole-cloud H0 connectivity measure different properties.

The exact integer lift can therefore succeed on a disconnected complex. K4 stops because its subsequent normalization requires one connected graph, not because disconnection contradicts the lift certificate.

### 3.2 Competing explanations and discriminating observations

| Explanation | Expected diagnostic pattern | Interpretation limits |
|---|---|---|
| A few remote points | One dominant component; a few singleton or small components; large nearest-neighbour distances for their members | Supports sparse peripheral geometry, not a demonstrated heavy-tailed distribution |
| Separated substantial clusters | Several sizeable components; large inter-component bridge distances despite modest within-component nearest-neighbour distances | Indicates a global connectivity bottleneck rather than isolated outliers |
| Uneven sampling around a loop | Several components or a bottleneck consistent with a sparsely sampled region; connectivity may occur later within the bar | Geometry alone cannot establish that the gap corresponds to latent angle |
| Midpoint precedes some points’ first connection | At least one nearest-neighbour distance exceeds \(r_m\) | Directly explains isolated vertices |
| Midpoint precedes cluster merger | Graph disconnected although every point has a neighbour within \(r_m\) | Rules out “isolated points only” as the complete explanation |
| The longest bar is nevertheless short | Small lifetime relative to recorded distance scales; possibly little separation from the next-largest lifetime | “Largest” is a ranking, not a significance or robustness guarantee |
| The selected class describes a local loop | Persistent H1 coexists with several components | Component counts alone cannot identify the semantic meaning of that loop |
| High-dimensional nuisance geometry | Broad local-distance variation or bottlenecks in raw Euclidean space | Does not justify selecting PCA, whitening, or a new metric after inspection |
| Filtration arithmetic differs | Float32 and float64 graphs differ at the recorded threshold; connectivity classifications may differ | A discrepancy must be measured before attributing the failure to rounding |

These possibilities overlap. A cloud can have both a short dominant bar and remote points. A 512-point diagnostic cannot establish a population tail law or identify the latent cause of a geometric gap.

### 3.3 A concrete arithmetic issue

The installed Ripser source converts dense distances to float32 before its persistence backend. K4 computes its subsequent edge graph from float64 `cdist` distances.

Thus the barcode and graph can use slightly different edge-entry values. E4 has the same broad issue. This is an implementation fact, **not an established explanation of job 0018**.

A diagnostic should reproduce the original float64 graph and also report its difference from the graph induced by Ripser’s rounded distances. A successor should explicitly choose consistent filtration arithmetic.

### 3.4 What the diagnostic can settle

It can determine:

- Whether the midpoint graph has isolated points, multiple substantial components, or both.
- Whether whole-cloud connectivity occurs before the selected class dies.
- How much of the selected lifetime remains after connectivity.
- Whether numerical representation changes the connectivity conclusion.
- Whether “largest” denotes a short or weakly separated bar in this sample.

It cannot establish history dependence, causal use, semantic correctness of the selected loop, or the success of any redesigned chart.

## 4. Rules common to any successor

The following should remain unchanged unless separately justified and approved:

- Three E4 cylinder-O models: 1729, 2718, 3141.
- Step 5000, `resid_post_3`, position 32, raw 128-dimensional activation site.
- No training, checkpoint, layer, model, or K search.
- Canonical token conventions and exclusion of \(w_{33}\).
- F47, deterministic ordering, and explicit bar-selection rules where applicable.
- Calibration-only fitting and gauge; immutable chart before validation.
- Fixed extension and duplicate handling unless the option explicitly replaces them.
- All-row evaluation: unsupported rows stop the assay rather than disappearing.
- K4’s substantive support, fidelity, coverage, headroom, precision, endpoint, and numerical safeguards.
- C1’s counterfactual family, matched-control construction, validity gates, endpoint, numerical certificate, and scoped causal interpretation.

A new chart changes \(u\), and therefore changes K4’s operational estimand even when

\[
\Delta_4=E[u(H)\cdot(m_{32}-m_4)]
\]

keeps the same formula.

It also changes C1’s phase regressors, fitted displacement map, interventions, and potentially its control family. C1 cannot merely load a replacement chart and retain previously fitted intervention objects.

Old verdicts remain immutable. Successor outputs may be compared descriptively with clear lineage; they are not interchangeable measurements of the same frozen coordinate.

## 5. Redesign options

The numerical choices below make the alternatives concrete. Only the recommendation in §6 is proposed for adoption. The other alternatives are **not** an authorized search menu.

### 5.1 Option A: largest connected component with a 5% landmark-exclusion gate

**Exact candidate rule**

1. Compute the original full-cloud diagram, selected bar, and midpoint.
2. Find components of that midpoint graph.
3. Choose the component with greatest cardinality; break ties by its lowest landmark ID.
4. Require at least nine retained landmarks and
   \[
   1-|C|/512\le0.05.
   \]
   This permits at most 25 excluded landmarks.
5. Restrict the originally selected cocycle and complex to \(C\). Do not select a different bar or rerun persistence after removal.
6. Require exact lifting and nontrivial primitive normalization on \(C\). Stop if the selected class vanishes there.
7. Fit the gauge and extension bandwidth using retained landmarks.
8. Extend to **all** original calibration, validation, and eventual scoring queries. Excluded landmarks are queries, not discarded evaluation rows.

For a direct validation comparator, apply this same rule and extend its retained chart to all 512 validation rows. Require support for all rows before computing fidelity.

**Identifiability**

There is one chart gauge on the retained connected component. The locations of excluded points on the circle come from extension, not topology on their original components. The 5% gate bounds landmark exclusion only; it does not bound excluded probability mass or distortion.

**K4 consequence**

The full-population endpoint can retain its suffix-only zero benchmark if all evaluation rows remain included and fitting is independent of evaluation. Scoring only the retained component would generally invalidate that benchmark: membership can depend on earlier history.

**C1 consequence**

A successor must validate extension on natural, donor, and forced states and refit all phase-dependent objects. Peripheral states cannot be silently declared ineligible by chart membership.

**Comparability and fitting risk**

Moderate to high fitting risk: trimming directly accommodates the observed failure. Even five excluded points could be scientifically important. A small exclusion fraction does not establish a representative circle.

**Assessment**

A defensible separate exploratory method, but not my first choice.

### 5.2 Option B: connectivity-constrained scale

There are several distinct rules.

**B1: minimum required enlargement**

\[
r=\max(r_m,r_c).
\]

Require \(b<r<d\); otherwise stop. This guarantees connectivity only when a connected scale exists inside the selected lifetime. It provides no positive distance from the connectivity boundary.

**B2: midpoint of the remaining connected interval**

Keep \(r=r_m\) when it already connects the graph. Otherwise require \(r_c<d\) and choose

\[
r=(r_c+d)/2.
\]

This is my preferred scale rule. It introduces no fitted interpolation fraction and gives an interior point of the remaining interval.

**B3: death minus epsilon**

A precise version could use the largest representable number below \(d\). It still needs connectivity and class-validity checks. A fixed absolute epsilon is unit-dependent; a fitted epsilon is a search parameter. Being close to death does not guarantee connectivity and can produce a dense complex.

**Identifiability**

A connected complex removes relative component-offset ambiguity. It does not prove that the selected class is the desired latent circle or that its phase parameterization is canonical.

**K4 consequence**

Retain all landmarks, the exact lift, primitive normalization, gauge, and extension. Apply the identical rule to production and direct-validation charts. Recompute all phase-dependent gates and scores.

**C1 consequence**

Explicitly replace §14/G0 in a successor protocol, bind the accepted new chart identities, and refit phase-dependent calibration. Retain the other causal design requirements.

**Comparability and fitting risk**

Lower structural disruption than trimming or changing geometry, but still a failure-motivated methodological change. Larger scales can add many triangles, change harmonic smoothing, and increase lifting cost. Fresh evaluation is required.

**Assessment**

Best bounded successor candidate, provided the selected class survives until connectivity.

### 5.3 Option C: maxmin landmarks plus extension

**Exact candidate rule**

Within the fixed 512-row calibration pool:

1. Select 256 landmarks.
2. Start with the lowest history ID.
3. Repeatedly choose the unselected point maximizing distance to its nearest selected landmark; break ties by history ID.
4. Sort selected landmarks by ID for chart construction.
5. Apply one predeclared bar/scale rule, exact lifting, and primitive normalization.
6. Extend to every original row and require all-row support.

If combined with Option B, that combination must be declared in advance as one method. Failure of a midpoint version cannot trigger an unregistered scale fallback.

The repository already contains maxmin functionality in `topology/persistence.py`; its public method uses a random first point. Reuse or minimally extend it with a documented deterministic start rather than create an unrelated sampler.

**Identifiability**

The chart describes the selected landmark complex, with other points represented through extension. Greedy coverage does not guarantee connectivity, semantic correctness, or good extension.

**Critical limitation**

Maxmin deliberately selects remote points early. It is not an outlier-removal method and may preserve the very bottleneck causing failure. Keeping all 512 landmarks would only reorder them, not alter connectivity.

**K4/C1 consequences**

Both need new chart identities, bandwidths, and complete validation. All-row endpoints remain possible; C1 must refit its phase-dependent objects.

**Comparability and fitting risk**

Moderate to high: landmark count, pool, start, scale, and extension offer several choices. There is no demonstrated need for computational sparsification at 512 points.

A principled landmark-based coordinate construction exists, but it is a separate method; Gaussian interpolation should not be described as automatically inheriting its guarantees. [Sparse Circular Coordinates via Principal \(\mathbb Z\)-Bundles](https://arxiv.org/abs/1809.09269)

**Assessment**

Not a compelling first response to this failure.

### 5.4 Option D: reuse E4 CircularCoordinates

**Exact candidate rule**

On fixed calibration data, call the existing E4 implementation unchanged with F47. Retain its midpoint, centered representative, minimum-norm Laplacian solve, and component-offset convention. Save the resulting landmark phases and add the already specified K4 extension rule.

That extension wrapper is new capability: E4 itself exposes only transductive `fit_transform(D)`.

**Identifiability**

On disconnected graphs, relative component offsets remain algorithm conventions. Centering a mod-p cocycle does not by itself establish integral closure, and E4 does not normalize primitive winding.

**K4 consequence**

A fixed E4-derived map can define an operational \(\Delta_4\) and preserve the suffix-only zero benchmark on independent evaluation data. The claim would concern that algorithmic coordinate, with weaker topological certification.

**C1 consequence**

Component conventions can influence phase differences and fitted interventions. C1 would require a new justification and complete validation. E4’s latent-angle agreement cannot substitute for those checks.

**Comparability and fitting risk**

Uses established code, but adopting its permissive behavior specifically because the stricter construction stopped risks changing the meaning of “valid chart.” Historical E4 panel fits also remain transductive rather than independently fixed charts.

**Assessment**

Useful for explicitly descriptive work. Not the recommended replacement for certified K4/C1 charts.

### 5.5 Option E: denoising or a kNN-graph chart

These are different methods and should not be bundled as one fallback.

**E1: one-step local averaging**

A concrete rule would replace each calibration vector by the mean of itself and its eight nearest *other* calibration vectors, with ID tie-breaking. Perform exactly one pass, then construct a certified chart on the transformed landmarks.

Transform each query through its eight nearest original calibration landmarks before extension. Define duplicates, bandwidths, and support in the transformed geometry in the contract.

**E2: union-kNN graph**

A concrete graph rule would connect \(i,j\) when either is among the other’s eight nearest neighbours. Form its clique complex, compute H1 over F47, select a nonzero class by an explicitly fixed algebraic ordering, then apply exact lifting, primitive normalization, and smoothing.

This is not the original Euclidean VR persistence rule. Unfilled graph cycles and a basis ordering would replace longest-bar selection unless a new filtration were specified.

**Identifiability**

Denoising can erase genuine variation or connect separate structures. A kNN graph can disconnect, shortcut a loop, or create graph cycles with no corresponding Euclidean persistent feature.

**K4/C1 consequences**

Both require a new geometric definition and new validation. C1 additionally needs a coherent chart map for natural, donor, and off-manifold forced states. Averaging those states changes the interpretation of the manipulated variable.

**Comparability and fitting risk**

High: neighbourhood size, averaging passes, union versus mutual graph, weights, filtration, and query transformation create many degrees of freedom.

**Assessment**

Potentially a separate methods project. Disproportionate before the elementary connectivity diagnostic.

### 5.6 Option F: stop K4/C1 and redirect

**Exact rule**

Preserve K4 INCONCLUSIVE and C1’s blocked status. Perform no chart search. Select the next owner-approved question through the existing planning process.

**Priority 1**

A separately preregistered conditional prediction analysis could ask how much fixed E4 activations improve recovery of belief information beyond the four-symbol suffix. It would concern history information in the representation, not specifically the learned PH circle.

**Priority 2**

An oracle-targeted intervention could study causal efficacy of belief-related state changes. It would require its own matched controls, validity gates, and claim. It would not establish use of the PH circular coordinate.

**Comparability and fitting risk**

Avoids chart-method selection and is entirely consistent with the current frozen outcomes. It leaves the circle-specific questions unanswered.

**Assessment**

Preferable if the selected class dies before whole-cloud connectivity, or if one bounded successor also fails.

## 6. Recommendation: diagnostics, then at most one scale successor

### 6.1 Immediate decision

Approve the diagnostic-only job in §8, if the information would affect the owner’s choice. Do not release a redesigned chart, K4 scoring, or C1 data stages with that approval.

The diagnostic separates two substantially different situations:

1. **The class survives into a connected regime.** A scale successor has a direct mathematical rationale.
2. **It dies before connectivity.** This selected class cannot supply one connected all-landmark chart within its lifetime. Proceeding would require a more substantial change.

No numerical probability of success is supportable from the current records.

### 6.2 Preferred successor rule

Use a new method identity, provisionally `CONNECTED-INTERIOR-v1`.

For each production and direct-validation chart:

1. Preserve all 512 landmarks and their original ordering.
2. Compute float64 raw Euclidean distances \(D\).
3. Define filtration dissimilarities
   \[
   \widetilde D_{ij}=\operatorname{float64}(\operatorname{float32}(D_{ij})).
   \]
   Use these values consistently for persistence, connectivity, edges, and triangles. This makes Ripser’s existing rounding explicit. Extension continues to use raw float64 Euclidean distances.
4. Select the largest strictly positive finite F47 H1 bar with K4’s tie rule.
5. Compute \(r_m=(b+d)/2\) and connectivity threshold \(r_c\) from \(\widetilde D\).
6. Choose
   \[
   r=
   \begin{cases}
   r_m,&r_c\le r_m,\\
   (r_c+d)/2,&r_m<r_c<d.
   \end{cases}
   \]
   If \(r_c\ge d\), stop INCONCLUSIVE/NO_CONNECTED_LIFETIME.
7. Require the computed scale to be strictly inside the bar, the graph to be connected, and the chosen scale to remain an interior representable value. Stop on an unresolved arithmetic boundary.
8. Apply the existing exact lift, congruence/closure checks, primitive normalization, smoothing, gauge, and extension.
9. Retain the existing substantive validation gates and all-three-model requirement.
10. Persist diagnostics before later operations can fail.

This changes **both** the scale rule and explicit skeleton arithmetic. Both changes must appear in the successor contract and review.

The rule does not guarantee meaningful persistence, a stable phase, successful lifting, adequate extension, or agreement across panels. Those remain empirical gates and limitations.

### 6.3 Decision tree

- Diagnostic contradicts the reported failure materially: investigate provenance or arithmetic first; do not choose a rescue chart.
- No connected surviving interval: recommend stopping this all-landmark chart route.
- Connected surviving interval exists: owner may approve the single successor above.
- Any successor chart, support, fidelity, coverage, numerical, headroom, or precision gate fails: preserve the result and stop that successor.
- All gates pass: permit the independently frozen fresh-data evaluation.
- Do not switch automatically to LCC, maxmin, E4 permissive coordinates, or denoising.

### 6.4 Why this is worth a limited attempt

Priority 1 has a focused, still unanswered question. The existing chart failure occurred before that question was tested. A deterministic connectivity-aware scale addresses the mismatch between H1 lifetime selection and an all-landmark connectivity requirement without excluding histories or changing the activation site.

The diagnostic is cheap relative to the existing reference computation and C1 programme. A bounded successor is therefore reasonable.

The case for prolonged chart engineering is weak. E4 agreement does not establish out-of-sample feasibility; denser complexes may introduce new failures; and C1 has substantial additional validity requirements. Passing K4’s chart would enable C1 development, not establish causal interpretability.

My recommendation is therefore **one diagnostic and, conditionally, one successor—not an open-ended chart search**.

## 7. Preregistration, exposure, and downstream interpretation

### 7.1 Freeze before each new computation

Before diagnostics, freeze its exact inputs, outputs, arithmetic comparisons, and prohibition on chart fitting.

Before any successor chart computation, freeze:

- Method identity and deviations from K4.
- Code, dependency, artifact, and contract identities.
- Distance arithmetic, ties, graph construction, and scale formula.
- Failure statuses and construction count.
- Gauge, extension, and all substantive validation thresholds.
- Data allocation, fresh sampling streams, endpoint, controls, uncertainty procedure, and reporting.
- The absence of automatic alternative methods.

The merged successor protocol needs the planning protocol’s clean-context independent review before freeze. A reviewer can be blind to uncomputed results, but cannot make the already exposed failure disappear.

### 7.2 Exploratory feasibility and fresh confirmation

A practical allocation is:

1. **Exploratory successor feasibility:** original panel 1 calibration and panel 2 validation; at most three production plus three direct-validation charts.
2. Save and accept the resulting immutable charts before generating fresh evaluation histories.
3. **Fresh validation:** 512 independent trajectories, shared canonically across models, for the predeclared support, coverage, oracle-headroom, and precision checks. No chart refit.
4. **Fresh test:** 3,072 independent trajectories, generated only after accepted validation; evaluate the frozen endpoint once.

The fresh-data plan must be frozen before generation. A new method namespace must separate its streams from E4 and C1.

“Fresh” means independently generated evaluation trajectories. Coincidentally repeated token strings are not removed: selection on history content can alter the target population.

All E4-panel successor outputs remain exploratory. Fresh outcomes can provide prospective evidence for the selected method on these fixed trained models. They do not establish generalization across training populations or independence from every prior methodological choice.

### 7.3 Priority 1 interpretation

Conditional on independently fixed calibration and chart, the suffix-only benchmark remains

\[
E[g(S_4)\cdot(m_{32}-m_4)]=0
\]

under the stated ideal process law. Retain the existing qualification for stored-process and sampling-law discrepancies.

Positive \(\Delta_4\) supports covariance between this coordinate and first-harmonic belief information unavailable from the last four observations.

It does **not** estimate a percentage of the circle requiring long history. Neither \(\Delta_4/B_4\) nor chart agreement automatically supplies that interpretation. A negative or small result also does not establish universal short-context sufficiency.

### 7.4 Priority 2 interpretation and C1 amendment

C1-FROZEN-v1 remains blocked. A successor must explicitly:

- Replace the K4 dependency branch with the approved successor’s accepted chart records.
- Bind chart hashes, producer commit, contract, gate set, and acceptance record.
- Refit phase-dependent calibration and retain all intervention-validity checks.
- Preserve its existing causal endpoint and scoped efficacy claim.
- Preserve the limitation that C1 does not separate long-memory use from short-context channels.

Fresh K4 and C1 streams should remain separate. C1 should not inherit K4’s fresh outcomes as tuning data.

## 8. Minimal diagnostic-only job

**Purpose:** explain the recorded connectivity failure without fitting or evaluating a replacement chart.

### 8.1 Inputs and authority

- Model 1729 only.
- Original panel 1 only: 512 `resid_post_3`/p32 vectors.
- Original K4 ordering, artifact identities, and scientific source configuration.
- Frozen source and stores remain unchanged.
- No checkpoint loading or model inference.

Whole-payload decoding, if required by the artifact API, must retain the existing distinction between integrity access and scientific access. Only panel-1 activations may enter diagnostics.

### 8.2 Computation

1. Verify provenance, shape, finite values, ordering, and released panel selection.
2. Compute the original float64 Euclidean distance matrix.
3. Run the original Ripser invocation once, including its original cocycle setting.
4. Apply K4’s original bar-selection rule and midpoint arithmetic.
5. Compute the original float64 midpoint graph.
6. Compute a deterministic spanning tree and connectivity threshold.
7. Construct the corresponding float32-rounded filtration representation and report graph differences at the **same original midpoint**.
8. Export diagnostics and stop.

No triangle-system construction, lift solver, primitive normalization, smoothing, gauge, extension, oracle computation, latent labels, endpoints, or alternative chart construction.

### 8.3 Required output

| Output | Purpose |
|---|---|
| Complete H1 birth/death table, selected index, birth, death, lifetime, midpoint | Establish what was selected |
| Sorted lifetimes and top-two lifetime ratio, or explicit undefined status | Describe dominance without introducing a significance gate |
| Midpoint edge count, component count, all component sizes | Distinguish peripheral points from substantial fragmentation |
| Component membership by immutable history ID; singleton IDs | Make the finding reviewable |
| Per-point nearest-neighbour and eighth-neighbour distances | Identify points whose first connection occurs after the midpoint |
| Fixed summaries: min, median, q90, q99, max, with quantile convention stated | Describe local-distance spread |
| Connectivity thresholds for original and rounded distances | Determine the global bottleneck and arithmetic sensitivity |
| Deterministic spanning-tree merge edges and sizes joined | Distinguish singleton attachment from cluster merger |
| \(r_c-r_m\), \(d-r_c\), and \((d-r_c)/(d-b)\) | Determine whether a connected surviving interval exists |
| Float64 versus rounded midpoint-edge disagreement count and component sizes | Test the numerical explanation |
| CPU, wall, memory, operation status, source/input identities | Preserve reproducibility and partial evidence |

Ratios require explicit zero-denominator handling. Spanning-tree ties use edge weight followed by ordered landmark IDs.

The H1 table and H0 merge information describe the original filtration. They must not become an invitation to select another bar or a favourable scale in this diagnostic job.

### 8.4 Interpretation rules fixed in advance

- \(r_c<d\): a connected surviving interval exists in that arithmetic.
- \(r_c\ge d\): it does not.
- Singleton components with nearest-neighbour distance above the midpoint directly establish late first connections.
- Multiple non-singleton components establish a broader merger bottleneck.
- Arithmetic changes connectivity: report both results and investigate before chart redesign.
- Reproduction fails: stop for provenance review.

No inferential claim about heavy tails, history dependence, topology’s semantic meaning, or causal use follows.

## 9. Cost and implementation discipline

### 9.1 Forecasts

These are planning estimates, not measured benchmarks or new CPU caps.

| Work | Forecast and basis |
|---|---|
| Diagnostic | Seconds to a few minutes including artifact loading and export. Job 0018 recorded roughly 0.015 s for distances and 0.078 s for PH; these timings exclude much surrounding work. |
| Successor chart feasibility | Likely minutes for six 512-point constructions, with substantial uncertainty if the increased scale makes complexes dense or lifting difficult |
| Fresh K4 validation/test | Roughly 0.5–2 CPU-hours including model extraction, references, certificates, and resampling; requires a concrete forecast before dispatch |
| Full C1 successor | Retains C1’s separate multi-hour forecast and independent validity risks; not included in chart approval |

At 512 vertices, a complete two-skeleton has over 22 million triangles. A connectivity-aware scale can therefore cost much more than the failed midpoint attempt. Preserve partial reports and enforce existing safety controls.

Owner B4 removes global CPU-time ceilings; metering remains mandatory. Safety constraints remain at most four threads, 12 GiB RAM, one scientific job at a time, outputs on X:, disk STOP thresholds, and existing usage/STOP latches.

Existing algorithmic lift limits must be addressed explicitly. K4’s frozen bounded lift and C1’s separately specified resource override are different contracts; neither should be changed implicitly.

### 9.2 Proportional reuse assessment

| Charter field | Proposed implementation |
|---|---|
| Existing functions/artifacts | K4 adapter, bar selector, cochain kernels, gauge, extension, serialization, gates, oracle/reference cache, certificates, and reporting infrastructure |
| Missing capability | Failure-persistent geometric diagnostics; connectivity threshold; explicit shared filtration arithmetic; successor lineage binding |
| Smallest change | Separate diagnostic entry point and a small successor chart wrapper/configuration; preserve frozen K4 modules |
| Stable interfaces/invariants | Chart/gauge/extension separation, deterministic ordering, exact certificates, all-row support, calibration isolation, immutable artifacts |
| Relevant regression checks | Synthetic connected/disconnected examples; connectivity before versus after death; rounding-boundary cases; duplicate handling; correct cocycle restriction; no fallback; evidence retained on failure |
| Next plausible extension | Reuse accepted immutable charts in a reviewed C1 successor; no general chart-selection framework |

Independent tests should verify mathematical behavior and isolation. Existing frozen tests remain unchanged; no real-data diagnostic belongs in this planning track.

## 10. Proposed owner disposition

The narrow approval I recommend is:

> Authorize one exploratory diagnostic job on model 1729, original panel 1, with the inputs, outputs, and prohibitions in §8. This does not authorize chart construction, K4 scoring, C1 data stages, or changes to frozen methods.

After reviewing that diagnostic, the owner may approve a separately reviewed and frozen `CONNECTED-INTERIOR-v1` successor, or stop the chart route.

K4 remains INCONCLUSIVE. C1-FROZEN-v1 remains blocked. All historical verdicts and their scopes remain unchanged.

---

# Questions for the owner

1. **Approve diagnostics only**, approve planning toward the single connectivity-aware successor as well, or stop this chart route now? My recommendation is diagnostics only first.
2. If connectivity occurs only after the selected class dies, accept stopping this route, or request a separately scoped component/landmark methods proposal?
3. If exploratory successor feasibility passes, approve fresh histories for prospective K4 evaluation before committing to C1 execution? My recommendation is yes.
4. Is the intended Priority 1 finding the scoped \(\Delta_4\) covariance result? Quantifying a literal fraction of the circle that requires long history needs a different estimand and proposal.