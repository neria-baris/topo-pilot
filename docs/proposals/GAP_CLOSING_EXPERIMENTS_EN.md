English translation of docs/proposals/GAP_CLOSING_EXPERIMENTS_HE.md at commit 727af56 (job 0068). The Hebrew original is authoritative.

# Experiment plan for closing the gaps in Topo-Pilot

Date: 15.10.2026. Status: **a new planning proposal; not a frozen protocol and not experiment results.**

The plan builds on the report `output/pdf/topo_pilot_research_report_he.pdf`, especially pages 15–25, and on the local follow-up protocols listed at the end. The numbers under "current state" are reported findings; the thresholds under "design" are new proposals. Writing the plan changes no verdicts, preregistrations or frozen documents. No sampling, training, scientific scoring or intervention was performed for the plan.

## 1. What exactly needs to be decided

| Gap | Current state in the report | Proposed experiment | What will count as closure within the tested domain |
|---|---|---|---|
| Validity of the coordinate | K4 stopped on disconnectedness; the giant-component diagnostic passed, without full certification of the map | M: an out-of-sample validated map | A map with closure and winding certificates, with extension and support reported on fresh data |
| Information beyond short context | Advantage over the last symbol is descriptive; Delta4 was not measured | H: history residual against every function of the length-4 suffix | A positive practical lower bound, or an upper bound smaller than a defined practical threshold |
| Causal use | X4-F did not reach an endpoint; the original C1 is blocked | C: C1′ with a new map and damage controls | Output response to a phase change in the direction the oracle predicts, beyond the controls |
| Information beyond next-step prediction | B2 ruled out a particular practical gap, not exact sufficiency | S: an identification test on the set of reachable beliefs | A validated separation witness, or an approximate sufficiency bound on a defined domain |
| Learning a horizon-dependent distinction | D-1 proved an orientability distinction in the oracle only | D: context and training horizon in trained models | A difference in representation and in joint prediction between training objectives, with controls |
| Speed versus dynamics | H5 was rejected; movement speed is confounded with the kernel change | V: three arms with a speed control | Separation between an average slowdown and additional dynamics effects |
| Generalisation and reproduction | Three replicates in the pilot; reproduction of one training run in the same environment | R: independent confirmation and domain extension | Reproduction of the conclusions in new models, sizes and environment fixed in advance |

No final experiment guarantees a decisive result. Closure means a decision at the defined resolution and domain, or explicit identification of the limitation that prevents it.

## 2. Shared rules

1. **The unit of replication is a trained model.** Panels, distance pairs and windows from the same trajectory are not independent training replicates. For fixed models, the uncertainty is conditional on the weights and the map; it is not a re-confirmation of the training process.
2. **Four separate allocations:** calibration, validation, fresh test, and external reproduction. Before an endpoint is computed, freeze the process identifiers, symbol map, weights, seeds, subpopulations, thresholds and extension algorithm. Check identifiers and also history content against an exposure registry. Content overlap is not proof of leakage, but requires a duplicate policy fixed in advance.
3. **Sample-size planning:** use validation for estimating variance and precision only, with sealed endpoints. Choose once the smallest size on the registered ladder that provides planned power of 80% for the alternative effect. If no size suffices, record UNDERPOWERED before the test is unsealed.
4. **Bootstrap over whole trajectories:** the same indices in paired comparisons; several windows from one trajectory are resampled together. 5,000 resamples, correction for the primary comparisons within each experiment, and intervals published even when there is no decision. Bootstrap intervals are an approximation, not a guarantee of exact coverage.
5. **Three outcome types:** support for the practical effect; exclusion of an effect of the defined size within the tested domain; INCONCLUSIVE due to precision, support, learning or validity. A gate failure is not a null effect. A failure must not be repaired on a test that has already been unsealed.
6. **Documentation:** a hash manifest, an exposure log, separation of public input from hidden states and oracle targets, code and environment version, CPU/RAM time, and the results of all seeds. Copying existing weights for analysis is not independent training.

## 3. M — first turn the map into a valid measuring instrument

**Question:** can a fixed circular phase be measured on a new history, without rebuilding the map on the test data?

**Design:** the three original cylinder-O models, end of training, `resid_post_3`, position 32. No new training. Use the rule proposed for C1′: a fixed H1 bar above F47, the bar's midpoint scale, and the largest connected component containing at least 95% of the landmarks. 512 calibration histories and 512 validation histories per model; the same canonical history is used in all models after the process identities are verified.

**Mandatory validation:** integer lifting, closure on the triangles, primitive winding, rotation/reflection alignment on calibration only, and a fixed out-of-sample extension. Adopt the K4 rules on eight neighbours, duplicates, radius and local resultant. On validation require map agreement ≥0.80, at least eight points in each of 12 phase cells, and an overall resultant ≤0.30. When a direct map is used for a fidelity check, the comparison is made only at points where both maps are defined, and the intersection rate is reported and required to be ≥95%; the primary map is not shifted according to validation.

**Support:** the proposal for C1′ is at least 507 of 512 validation points supported; this threshold is not identical to the 95% threshold for landmarks. A point without a phase cannot serve as a source or donor in the intervention. C1′ will define a support-conditioned population and will also report the natural coverage rate. The effect must not be attributed to the excluded population. In H, lack of support is handled through bounds, not by dropping rows.

**Decision:** all three models must pass. A failure gives INCONCLUSIVE/MEASUREMENT; it does not reject information from history or causal use. This rule is a new version, and does not turn the historical K4 into a success. Before freezing, write the exact delta against C1, including the numerical certificate and the support rates at every gate.

## 4. H — does the circle carry information beyond the last four symbols?

This is **a proposed, separate K4b experiment**, not a rerun of K4. It is not a precondition for the narrow interpretation of C1′, and not an automatic part of it.

**Target:** for the original stationary process, define the circular belief moment `m32`, `m4` computed from the last four symbols with a stationary prior, and `r4 = m32 − m4`. For a map and orientation fixed on calibration:

`Delta4 = E[u(h) · r4(h)]`, where `u = (cos(phi), sin(phi))`.

Every coordinate that is a function of the suffix alone satisfies `Delta4 = 0` in the population, because `E[r4 | suffix4] = 0`. This is stronger than a comparison with a few selected suffix decoders. The identity refers to the full natural population, so rows must not be selected by prefix or by map support while keeping the same interpretation without correction.

**Design:** use the M maps, and allocate a fresh test of size 3,072, 6,144 or 12,288 independent trajectories; choose before it is unsealed, according to validation. No K search: the primary measure is K=4, practical threshold 0.01 and power-planning alternative 0.02. K=1,2,8,16 are secondary analyses, multiplicity-corrected if inference on them is reported. B4 is an oracle headroom gate, not a model result.

On validation, a one-sided 95% lower bound on B4 exceeding 0.01 is required. A numerical error target of ≤1e-4 per score is set; a covering bound for all rows must be proved, in addition to an implementation check against Decimal on selected rows. Agreement on a few reference rows is not a certificate for the whole sample.

**Unsupported points:** the oracle is also computed on every row. On a supported row set `Xminus = Xplus = u·r4`. On a row without a map set `Xminus = −||r4||`, `Xplus = +||r4||`. Thus `[E Xminus, E Xplus]` bounds Delta4 for every possible completion of a unit coordinate on the missing rows. No dropping, no arbitrary phase assignment and no exploitation of selection to create an effect.

**Controls:** a phase from m4; a fixed hash function of the four symbols; a phase from initialisation. The first two are null controls in the population, and are not required to give exactly zero in the sample. They are not subtracted empirically to centre the endpoint. Add a fixed non-linear suffix decoder as a descriptive measure, without claiming that it is a ceiling for every suffix function.

**Decision rule:** for each model separately, a one-sided lower bound at the corrected level 0.05/3 for `E Xminus` must exceed 0.01 plus the numerical-error bound; overall support requires this in all three. If in all three the upper bound for `E Xplus`, plus numerical error, is smaller than 0.01, an effect above that threshold is excluded for this measurement. All other cases are published as mixed findings or INCONCLUSIVE.

**Interpretation:** a positive result identifies a contribution of information earlier than the four symbols to the measured coordinate. It does not establish a maximal memory horizon, necessity for prediction or causal use. A negative result does not exclude other harmonics or a non-circular history representation.

## 5. C — does changing the phase change the output in the right direction?

**Basis:** implement C1′ as a minimal delta to C1-FROZEN-v1. Keep the definition of the intervention, the family of 32 direction controls, the gates and the verified arithmetic; explicitly replace the map dependency with the M rules on fresh histories. The old X4-F failure in the controls is not resolved by more draws of the same eraser.

**Intervention:** change the phase component at the final site in two defined directions; build counterfactual futures `q+`, `q−` according to the exact symmetry of the process. Keep the identity of the last symbol and the nuisance features that the protocol fixes. Do not select donors by output result. Continue through the frozen LayerNorm and output readout.

**Primary measure:** for each row compute the difference between the correct alignment and the reversed alignment of the outputs to the oracle:

`A = 0.5 <q+ − q−, log p+ − log p−>`

`Y = A_target − mean(A_controls)`; `G` is the oracle contrast from C1; test `E[Y − 0.10 G] > 0`. Keep the target definition and the original mass and numerics corrections; theta is not a rate bounded to [0,1], and the direction controls do not cancel every non-linear damage effect.

**Gates:** identity patch; zero patch; a manipulation that really moves the phase; damage and support controls; y-axis leakage; and full-donor replacement as a positive control. A failure of the positive control means the test did not demonstrate sufficient headroom in the model, not that the model uses no information. The test size is chosen on the original ladder of 4,096/8,192/16,384 eligible rows, by validation variance and oracle only.

**Decision:** the original C1 rule, with 5,000 bootstrap resamples and corrected bounds for the three models, including the numerical-error margins. Also publish A of the primary arm, the control mean, G, coverage, damage and per-model measures.

**Interpretation:** a positive result supports a local causal effect of the phase manipulation at the specific site on the output readout. It does not prove that the topology is necessary, that information was removed, that the phase was built from a long history, or that this is the computation mechanism in the earlier layers. Even positive H and positive C together do not prove that the component beyond K4 is precisely the component that the output uses; that requires a further joint experiment.

**Necessity experiment, only at a further stage:** build a defined family of erasures/compressions together with restoration of nuisance factors, an erasure check with fixed linear and non-linear decoders, and matched damage. A linear erasure with a still-successful RBF is not erasure of information. Even such an experiment gives necessity relative to a family of interventions, not a theorem that no alternative representation lacking that topology exists.

## 6. S — is Q1 sufficient, and in what sense?

**Goal:** avoid inferring exact sufficiency from zero witnesses in the B2 sample.

**First track, oracle only:** fix the pilot process and context 32. Define a set of reachable beliefs, a prior policy, a maximal horizon and an error metric. Start with exact enumeration in a small model and at finite history lengths; at pilot size use history branches with probability bounds and numerical containment, if they can be completed within budget.

For every covered pair or cell of histories, validate Q1 and Q2. Report a separation curve planned in advance: the maximal Q2 distance under Q1 distances ≤0, 0.001, 0.005, 0.01, without choosing the successful threshold after the fact. The threshold Q1=0 requires an algebraic/rational proof; "smaller than the float tolerance" is not exact equality.

**Two valid products:**

- A validated reachable witness with identical Q1 and different Q2 proves insufficiency at horizon 2 in the relevant domain.
- To claim approximate sufficiency, a fixed decoder `f(Q1)` and a certificate over the whole covered domain are needed: `distance(Q2,f(Q1)) ≤ epsilon`, together with a bound eta on the mass of uncovered histories. epsilon=0.01 and eta=0.01 are proposed targets for testing, not values achieved. The metric must be stated explicitly and the same metric used in the certificate and in the decision.

If there is no coverage certificate, the product is a bound/limited search or INCONCLUSIVE, even if again no witnesses were found. Sufficiency at horizon 2 is not sufficiency for all futures; a claim for every horizon requires a further check of the closure of the representation under update and for all word lengths in the finite process.

**Model branch, only after oracle headroom is guaranteed:** predict Q2 from activations and from Q1 using decoder families with identical capacity and calibration rules, fixed in advance. An advantage for the activations is evidence of information accessibility for the decoders tested; insufficiency of Q1 must not be inferred from a failure of a decoder restricted to it. For a proven and cleaner horizon gap one can proceed directly to D, without waiting for a full resolution of sufficiency in the pilot process.

## 7. D — move D-1 from the oracle to learning

**Primary question:** does training on the joint future at horizon 2 produce relevant information in the final layer at decision positions, beyond training on the next symbol?

**World:** initially the original 4×3 D-1 construction: a world bit fixed per trajectory, cylinder/Möbius with a half-half prior, the same E and the same start. The oracle is over the joint state world×coordinates. It must not be reset to the pilot's stationary prior. 12×12 is kept for confirmation after success on 4×3, with a new proof of gap and feasibility; the small witness does not carry over to it automatically.

**Axes:** the number of observations since the start of the trajectory `L ∈ {8,32,64}` and the training objective `H ∈ {1,2}`. L must not be called a "memory horizon". In H1, train CE on the next symbol; in H2, train `0.5 CE_next + 0.5 CE_joint2`. Both heads, with 5 and 25 outputs, exist in both arms; the joint head is not trained in H1 and is not used as its performance measure. The backbone, the paired initialisation, the trajectory pool and the batch order are kept between H1 and H2. Increasing the context is an explicit input change, not an undocumented truncation of a long trajectory.

**Scope:** five paired replicates per cell, 30 models in total. Another five H2 models at L32 for the C⊕C control, 35 in total. This is a staged plan: first the two L32 cells plus the control (15 models); the other lengths only after checking the validity of measurement and learning. The L32 result is the primary comparison; the other lengths are a planned extension. No replacement of a failed seed.

**Fixed training:** the pilot backbone with four blocks, d_model=128 and four attention heads, adapted to the D-1 alphabet and to context L; 131,072 training trajectories, 4,096 dev and 5,000 steps at batch size 128. AdamW, rate 0.001, warmup of 200 steps, cosine, weight decay=0.1 and clip=1.0. The two-step targets are joint symbol pairs, not prediction of the second symbol's marginal. The trajectories include targets up to L+2, but the input at position L contains only observations up to L. The loss is averaged over the allowed history positions, under an identical causal mask. The number of trajectories and steps is the same across context lengths, so the total number of symbol targets varies with L; the comparison of H within the same L is the primary identified comparison. After calibration, new seeds and stream names are frozen in the execution document; scientific evaluation does not begin before that.

**Oracle gate within each context:** on natural data, measure the frequency of the decision position, the variance of the world posterior pi(h), the coverage of short suffixes and the size of the Q2 gaps. Locate pairs with the same L, the same coordinate posterior and Q1, but different Q2, and validate them exactly/by independent computation. The existing D-1 pair has size TV=0.01; do not assume it can be padded to every L while preserving its conditions. If no validated pairs are found in a cell, its pair test is not performed.

**Measurement:**

1. Decode pi(h) from `resid_post_3` at the decision position, with ridge regression and with a fixed non-linear family. For example, RBF ridge with a median width from calibration only and a frozen regularisation grid. The skill measure is `1 − MSE/Var(pi)` on the test. Too small a target variance triggers a headroom failure, not an artificial R².
2. A frozen Q2 decoder from the single current activation, in the same family and with the same budget for each training objective. In H2, the original joint head is also checked separately, without post-training fitting.
3. Natural Q1 performance in both arms. A two-symbol autoregressive rollout is reported separately: in H1 it can re-read the history after the first symbol, so success in it does not prove that the information was already in the current activation.
4. The posterior-isolated pair test and the natural sample are reported separately. For a pair with oracle gap `d=TV(Q2a,Q2b)`, a strict target is TV ≤d/4 for each prediction; then the prediction error is smaller than the separation gap. If the pair is too rare, the enriched test must not be converted into an estimate of natural performance.

**Controls:** last symbol; suffixes K=2,4 with fixed capacity; initialisation; target shuffling for decoding; C⊕C. In the C⊕C control the world posterior is constant at 1/2, so R² is undefined. Use the MSE against the constant and a check of inability to predict the hidden sampling bit above the base rate. The future targets serve as labels only, and the mask prevents them from entering the history input.

**Proposed decision for L32:** first, a natural learning gate for each arm by regret relative to a constant baseline and the corresponding oracle gain; do not normalise by the context gain of Q1 at a decision position where it is zero. Then require a pi-decoding skill in H2 ≥0.50 and an H2−H1 skill difference ≥0.10 in all five replicates, with a positive corrected lower bound for the difference over the history sample, and also a pass of the Q2 test on the validated pairs. This is a strict operational claim defined in advance, not a mathematical necessity for decoding pi. Each component is reported separately when the combined rule is not supported.

**Scope of inference:** five replicates test consistency over fixed seeds; the history intervals are conditional on the models. A larger training study is needed for exact inference on the population of training seeds. There is no assumption that skill grows monotonically with L: information accessibility, mixing and the frequency of seam crossings are checked in the oracle.

**Interpretation of results:** H2 succeeding while H1 does not carry the distinction supports dependence on the prediction objective in this domain. Both succeeding leaves open that the information is learned in H1 because it is useful at other positions. Failure of both after passing the learning gate limits the form of measurement/encoding; without passing the learning gate it is a learning failure. H2 need not encode pi explicitly: it may encode another predictive distinction. No result here alone proves Möbius geometry in the activations or causal use of the topology.

## 8. V — separate speed from dynamic structure

**Three-arm design:** the original flat; the original conductance; and a uniformly slowed flat. Speed is defined in advance as `v(T)=E_pi[d(z_t,z_(t+1))²]` in the same metric. If v_conductance≤v_flat, build `T_slow=(1−alpha)I+alpha T_flat` with `alpha=v_conductance/v_flat`. If the ratio is not in [0,1], this comparison is not applicable; the formula is not changed after training.

Keep the world, E and the stationary distribution. Validate exactly the match in the speed measure and also report the movement probability, per-axis displacements, autocorrelation and the spectral gap. Matching one moment is not matching the whole dynamics. Do not use old "speed" values if they were computed under a different definition.

**Scope:** five paired triplets, 15 models, the same optimisation conditions and number of targets. Primary: AUC of oracle-normalised regret over 5,000 steps; proposed practical threshold 5% of the flat-slow AUC. The oracle normalisations are fixed in advance; AUC in nats is also reported, to distinguish a normalisation change from a learning change. Secondary: learning time by three consecutive checks below 0.05, with a checkpoint every 100 steps and visible censoring.

**Decision:** the conductance versus flat-slow comparison is the primary one; the flat-slow versus flat comparison quantifies the effect of the uniform slowdown. Cohort size and precision are planned before training from a technical pilot and from curves of earlier research, without seeing new results. If five triplets do not suffice for the desired precision, the number is updated and frozen before training starts. An effect beyond 5% or equivalence within ±5% requires suitable intervals; otherwise INCONCLUSIVE.

**Interpretation:** a gap remaining after speed matching is a dynamics effect beyond this speed measure. It is still not a curvature effect. A claim about geometry requires a defined geometric manipulator with additional controls. The original H5 remains REJECTED.

## 9. R — staged confirmation and generalisation

**R1, independent reproduction:** reproduce the six original O models in a clean clone and in an independent environment, with structured timing recording from the start of the run. Fix in advance a scientific criterion for reproducing F1 and the prediction/agreement measures, separately from the bit-identity check within the same environment. A finding reproduced scientifically in a new environment does not require bit-for-bit identical weights. The historical G-H remains FAIL; only a new gate with a new identifier can be passed.

**R2, confirmation of the strongest new finding:** after a positive H or C, repeat the same experiment with five training runs and new test data generated from the pilot process. Keeping the old weights and generating new histories is data confirmation for fixed models; new training runs add replication of the learning.

**R3, limits of generalisation:** only after confirmation, compare cylinder/square at sizes 8×8 and 16×16 and in two architectures: the pilot Transformer and a GRU with a similar parameter budget. Five replicates per cell give 40 training runs. Before each cell, re-check identifiability in the oracle and learning quality, with an emission rule defined without model results. A cell in which the oracle does not distinguish is not a valid negative test of the model's ability to learn the difference.

Publish the training contrast by world and the agreement with the belief for each cell. Consistency supports generalisation to these sizes and architectures only. Nothing may be inferred from it about natural-language models or all topologies. X2a and X6 are not required before these core experiments decide, and each of them requires its own protocol.

## 10. Execution order, cost and products

**Recommended order:**

1. M and the oracle feasibility of D-L32. Both can advance separately; no training is needed to establish measurement validity and headroom.
2. C1′ on the existing models. H is a separate study useful for interpreting the origin in history; S is an oracle branch that can advance in parallel, without delaying D.
3. D-L32, and only after it the extension of lengths and 12×12 according to the registered gates.
4. R2 for the central new finding. V and R3 by priority and resources; they extend the answer and are not a precondition for measuring local use in C.
5. R1 should be run before publishing a new central conclusion based on the pilot.

**Cost:** there is no new performance measurement here. The X5 report measured about 0.383 seconds per CPU update on one thread at L32; 5,000 steps are about 32 minutes for a similar training run, before evaluation, oracle and I/O. This is a historical planning basis only.

| Package | New training runs | Conditional estimate/planning rule |
|---|---:|---|
| M/H/C | 0 | Measurement of 512 rows and a synthetic intervention scenario; estimate by the number of maps, rows and arms. PH computations and the numerical certificate may dominate the time |
| S | 0 | Enumeration and certificates can blow up exponentially; fix a time budget and uncovered mass before searching |
| D-L32 and null control | 15 | About 8 hours of training on the historical basis, before the overhead of the joint head, evaluation and oracle |
| Full D | 35 | An initial order of magnitude of 20–50 hours including reserve; the actual cost depends on the context, the head implementation and the evaluation |
| V | 15 | About 8 hours of training on the historical basis, before evaluation and oracle |
| R1 / R2 | 6 / 5 | Measured and estimated separately; R2 is five training runs if only the cylinder is needed, and ten if the finding requires a pair of worlds |
| R3 | 40 | A benchmark is needed for each size and architecture; the pilot estimate must not be copied to all cells |

Before execution, run a technical benchmark without scientific endpoints: loading, 100 updates on synthetic data, batched scoring, map building, and saving products. There is no new run within the frame of this document. A CPU, memory and disk forecast is written for each stage; no time quota is promised on the basis of old training alone.

**Required products for each experiment:** a frozen protocol and manifest; test code against an independent oracle; a gate report; a table of endpoints and uncertainty intervals for each seed; control results; coverage/exclusion data; cost; and a "what was decided and what remains open" paragraph. Historical reports must not be overwritten.

## 11. Reuse and minimal development

| Component | Reuse | Minimal addition | Independent test needed |
|---|---|---|---|
| Identities, data and oracle | ArtifactStore, SeedTree, BayesFilter and symbol maps | an exposure registry and explicit ID links | prevention of target leakage; a rational/Decimal oracle on small examples |
| M/H | K4 code and the diagnostic map | LCC, support delta, bounds for missing rows | closure, primitive winding, duplicates, the zero identity for the suffix, missing-row bounds |
| C | formulas, gates and certificate from C1 | the exact C1′ and implementation of the map rule | identity/zero patch, crossed contrast, control matching, numerical guards |
| D | `tools/d1_seam`, learner/trainer and activation extraction | mixture sampling, variable contexts, joint-2 head and decision-phase measures | no teacher-forcing leakage to the measured position; joint law, not marginal; witnesses at the given length |
| V | kernels, training and X5 measures | flat-slow and a matching check | stationarity, speed by the new definition, censoring and AUC |
| R | manifests and reproduction | an independent environment and a scientific reproduction criterion | full provenance, metrics and tolerances fixed in advance |

The existing working code is not all available through the same paths as in the planning documents: some files/stores are referenced in external worktrees. Before implementation, a validated path and version must be resolved, and a reference in a document must not be assumed to be an available API. This document is scientific planning and does not order dispatch of tasks to other agents or changes to existing research stores.

## 12. Local sources read

- The attached report: `output/pdf/topo_pilot_research_report_he.pdf`, pages 11, 14–26; gap map on page 25.
- `README_HE.md`: E4 status and the follow-up results; used to cross-check the scope of the claims.
- `docs/proposals/CIRCULAR_HISTORY_K4_PROTOCOL_DRAFT.md`: the definition of Delta4, the zero identity, map and precision rules.
- `docs/proposals/planning/responses/C1-FROZEN-v1.md`: the intervention site, the crossed contrast, controls, the 0.10 rule and the numerical certificate.
- `docs/proposals/planning/requests/coord-c1prime-delta-20261015.md`: the LCC rule and the fresh-data requirement for C1′.
- `docs/proposals/planning/requests/coord-d2-trained-lengths-20261015.md`: the question of lengths and training objectives for D-2.
- `tools/d1_seam/OUTPUTS_0020.md` and `tools/d1_seam/d1_seam.py`: the oracle result and the construction of the small process.
- `docs/proposals/X5_G1_TRAINING_PROTOCOL_V4.md`: the learning-time measures, pairing and the historical performance estimate.
- `docs/proposals/planning/INDEX.md`: the status of the plans; planning is not an experiment result.
