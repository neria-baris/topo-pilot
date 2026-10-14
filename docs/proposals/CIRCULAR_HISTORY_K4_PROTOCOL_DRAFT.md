# Learned circular coordinate beyond a four-symbol suffix

DRAFT FOR OWNER REVIEW — 14 October 2026. Planning and metadata inventory only.
No new scientific job, computation budget or execution is authorized by this document.

## Question and scope

Does a fixed circular coordinate extracted from the original learned E4 representation covary with first-harmonic belief information unavailable from the last four observations? This is Priority 1 of the owner charter. Job 0014 found oracle B4 about .067–.070 on its different existing histories, versus B8 about .0093. That motivates K=4; it does not establish learned-model headroom on the E4 rows or rescue the stopped K=8 study.

Use only the three original cylinder-O models, seeds 1729/2718/3141, step 5000, hook `resid_post_3`, position 32. No other layers, checkpoints, K search, new histories, activation extraction, training, interventions or fresh test. Original E4/test panels have been exposed in E4 and the circular audit: all proposed results are exploratory, including rows held out from chart fitting. No old data can become fresh confirmation through this protocol.

## Read-only inventory: what actually exists

Inspected complete artifact metadata and existing source on 14 October; did not load scientific arrays or evaluate an endpoint. Artifact root: `X:/Downloads/projects/topo-pilot/topo-pilot/artifacts/` (protected main, read-only). Resolve this root explicitly in any future frozen manifest.

| Seed | Checkpoint | ActivationSet | ObservationSet | HistoryIndex |
|---|---|---|---|---|
| 1729 | c3358e3cb9c352fb | 0e001559534ee7ef | 2a67b2c947e293ba | afb6e7120c9477b1 |
| 2718 | 98b0e703a337d513 | ec17425cf67f1a54 | 95c4d118517ecd92 | 908cb61ffbd956c6 |
| 3141 | 036b670743ffbbaf | 069da84ce363d8f2 | 2e2cf22bb4820155 | 7e7d27bd143ebeb5 |

All three ActivationSets declare `A[4096,6,128]` float32 and include `resid_post_3`; six hooks, 4096 IDs, complete status. Observations contain 4096 length-33 token rows; only observations w1–w32, array slice `tokens[:, :32]`, may enter this analysis; column `tokens[:, 32]` (w33) is excluded. Indices declare end=32, eight disjoint 512-row panels, one history per trajectory. All ObservationSets are explicitly `split=test`. The existing audit's [input manifest](CIRCULAR_AUDIT_OUTPUTS/inputs.json) records the same activation identities and these payload checksums, respectively:

- `a134e8f3c68b105215834cdf5c4f11fa11eeae354faf71da1399fdca76869db5`
- `d326ac0ae3339e76e3677484977deb12eb12edcbd488bce4ad80d7f83b5af2aa`
- `22fb78ce44a5f54c44192db3589061748ae1990d055f6cf269717b595ea56ad3`

These are declared canonical payload checksums, not newly verified NPZ file hashes. Before execution, independently revalidate metadata, canonical payload checksums, file hashes, parent lineage, ordered IDs, position, token digests and canonical symbol permutations. Verify that corresponding sequence IDs/canonical histories across the three models are identical before paired resampling; mismatch stops this design for review. Equal generation seeds alone are insufficient evidence. Future identity-only verification may decode/checksum the entire immutable artifact (including panels 3–8), because canonical checksums cover the whole payload. That access permits only integrity/join/position checks: no scored numerical preparation, summaries, chart diagnostics, oracle filtering or endpoint. The analysis adapter returns only panels 1–2 until separate scoring release.

The existing 3072/1024 history-origin pools used by Job 0014 have oracle means but no corresponding cached model activations. Their m4/m32 arrays must not be joined to these E4 rows. X4-F used a different site and target; it is not a substitute for the learned PH coordinate.

`src/topo_pilot/topology/circular.py` provides transductive `fit_transform(D)` only; it does not retain a fitted out-of-sample chart or certify integer closure. `src/topo_pilot/experiment/s7_circular.py` reconstructs each panel's coordinates and stores aggregate metrics. Those historical panel scores do not provide an independently fixed chart. The stopped history-feasibility `tools/x4_history_feas/core.py` contains candidate certified lifting and extension code, but its real-data chart gates were never reached. Its runner also samples histories and must not be executed/imported here. Out-of-sample feasibility is UNVERIFIED, not established by this inventory.

## Estimand and fixed data allocation

Let c(z)=(cos(2*pi*x(z)/12),sin(2*pi*x(z)/12)); mK=E[c(z32)|w(33-K):32] under the verified stationary process, restarting the filter at stationary pi for the suffix. Set r4=m32-m4. For each fixed model/chart, the primary endpoint is

`Delta4 = E[u(w1:32) dot r4]`, with `u=(cos(phi),sin(phi))`.

Conditional on calibration, m4=E[m32|S4], hence every suffix-only u=g(S4) has population Delta4=0. Also |Delta4|<=B4=E||r4||. A positive endpoint identifies covariance beyond the four-symbol suffix in this operational circular coordinate. Zero or negative results do not exclude every history-dependent coordinate, higher harmonics, other latent features or causal use.

Freeze panels without inspecting arrays/results: panel 1 (512 rows) is calibration; panel 2 (512) validates chart/support and estimates precision; panels 3–8 (3072) are the scoring set, pending a later release. Use identical trajectory allocation across models after the canonical-history join passes. Verify disjoint trajectory IDs. Keep all scored rows; never remove rows because their prefixes, activations, chart support or oracle residuals look unfavorable. Selection on earlier history can invalidate the zero benchmark. Panels are storage partitions, not independent training replications.

## Proposed feasibility phase: map first, score later

1. Freeze a machine-readable contract, exact input/code/environment identities and independent synthetic test specification before any new numerical work. Run identity/process/reference checks only on calibration/validation inputs; no scored endpoint is inspected. Use named tokens with the corresponding named emission, or canonical tokens with E_named[:,symbol_perm], and independently check equivalence. No w33 or latent evaluation label enters chart fitting.
2. For each model, use all 512 panel-1 activation vectors as landmarks, sorted by history ID, raw Euclidean distances in the original 128 dimensions; no PCA/whitening/tuning. Construct the largest strictly positive finite H1 bar over F47; ties by birth, death, returned index. Use its midpoint scale. There is no fallback bar, field, scale, model or site.
3. Require an exact integer lift: D1*a=47*b; find integer z with D1*z=b, then alpha=a-47*z, verifying closure and congruence independently with oriented triangles. Inherit the bounded search [1,2,4,8,16], 128 solver nodes per bound, at most 30 CPU seconds/chart, exactly two prescribed local L1 passes. Use lowest-ID-root BFS, nonzero cycle-period gcd coprime to 47, primitive normalization and unit-edge smoothing with scaled normal-equation residual <=1e-8. Freeze dependency versions and deterministic ordering. Exhaustion/missing certificate is INCONCLUSIVE, not nonliftability. This is a certified operational construction at the historical E4 site, not a claim to reproduce historical angles exactly.
4. Fit reflection and rotation using only panel-1 m32: maximize modulus of mean exp(i*s*phi)*conj(m32_x+i*m32_y), s=+1/-1 (tie +1), then subtract its argument. Require nonzero finite alignment. Save the chart and gauge before panel 2. Never orient against r4 or evaluation outcomes.
5. Extend using the candidate's eight nearest landmarks, stable distance ties resolved by landmark ID. For calibration landmark i let d8_i be its eighth-smallest distance to the other 511 landmarks (excluding itself only). Set sigma=median(d8_i) and R=2*quantile_.99(d8_i, inverted_cdf); zero sigma is INCONCLUSIVE. For a query use weights w_j=exp(-.5*(distance_j/sigma)^2), z=sum(w_j*exp(i*phi_j))/sum(w_j), extended phase=arg(z) modulo 2*pi in [0,2*pi). Require finite values, |z|>=.2 and eighth-neighbor distance<=R. An exact duplicate means distance exactly zero (no approximate-match tolerance): average exp(i*phi) across ALL exact matches instead of the eight-neighbor formula; if 1-|that mean|>1e-8, fail for conflicting phases. All 512 validation rows must be supported; no trimming or replacements.
6. Construct one separate certified chart on all 512 panel-2 vectors per model, using the same fixed PH rules, solely for extension fidelity. Require A=max over s=+/-1 of |mean exp(i*(phi_extension-s*phi_direct))|>=.80. This diagnostic is invariant to gauge and cannot rotate or replace the saved calibration chart. Require each of 12 equal phase bins [2*pi*j/12,2*pi*(j+1)/12) in the extended validation coordinate to have >=8 rows; separately require the OVERALL 512-row phase resultant |mean(exp(i*phi_extension))|<=.30 (not a within-bin resultant). These are proposed minimum safeguards, not a theorem that the extension preserves topology. Document all chart, gauge and support diagnostics, including failures.
7. On panel 2 only, compute X=u dot r4, B4 and fixed control scores. Practical margin delta=.01 and planning alternative .02 retain the previous absolute alignment scale; .01 is not a universal noise floor. Require a one-sided 95% lower B4 bound >.01 and target numerical error <=1e-4. Use an independent 60-digit reference on four lowest-ID histories per model for K=1,4,32; require max moment discrepancy <=1e-10 and process/stationarity tolerance1e-12. Separately derive and document a propagated per-score numerical-error bound <=1e-4; agreement on selected reference rows alone does not certify a bound for every row.
8. With calibration/chart held fixed, jointly resample the 512 validation trajectories 5000 times using PCG64 seed410201. Use q=.05/3 and 1-.05/3 inverted_cdf bounds on each model's row SD. At N=3072, require every upper-SD normal MDE80=.01+(z_(1-.05/3)+z_.8)*SD_upper/sqrt(N)<=.02; corroborate >=.80 projected power with independent centered validation-empirical resamples of size3072, 5000 draws, PCG64 seed410202, same row indices across models, with e_b=mean(resampled validation X)-mean(validation X), q_alpha=quantile_alpha(e), alpha=.05/3; projected power is mean(.02+e_b+q_alpha>.01), per model. B4 uses the same validation trajectory resamples, one-sided q=.05 lower bound. Projection disagreement/borderline results are INCONCLUSIVE. This is a conditional planning approximation, not observed power or fresh inferential evidence.

There are at most six 512-row PH/chart constructions in this phase. A gate failure ends the phase with preserved evidence; no data replacement, changed threshold, second chart family or run-to-pass. Geometry/support/precision gates must pass for all three models before a scoring request can be proposed. Beyond the expressly permitted identity-only checks, no scored arrays or endpoints enter this phase.

## Controls and later scoring rule (requires separate release)

Fixed controls: unit phase of m1, unit phase of m4 (zero mean -> vector(1,0)), and nonlinear SHA256 suffix phase `2*pi*int.from_bytes(sha256(bytes(canonical_last4)).digest()[:8], 'big')/2**64`. All are suffix-only and have population Delta4=0. Report their scores/intervals rather than treating one control as an estimated ceiling over arbitrary suffix functions. Independently verify the zero identity by exhaustive enumeration in a tiny asymmetric stationary HMM; do not demand exact zero in a finite real sample. No control-based recentering or empirical endpoint retuning.

After owner release, the already saved chart/gauge is extended to ALL 3072 scored rows. Any unsupported or invalid row stops INCONCLUSIVE before mean scoring; no complete-case analysis. No chart refit or evaluation-based gauge change. Compute per-model Delta4, B4, controls and numerical error. Bootstrap whole trajectories jointly across models and controls, calibration/chart fixed, 5000 draws PCG64 seed410203. Report central95% intervals and one-sided Bonferroni bounds at q=.05/3 and 1-.05/3 (inverted_cdf), an approximate conditional uncertainty summary for exposed data.

- Descriptive support at the chosen practical scale: every model's adjusted lower Delta4 bound exceeds .01 plus the certified per-score numerical-error bound.
- Scoped lack of support above that scale: every model's adjusted upper bound plus numerical-error bound is below .01. This is not short-context sufficiency or absence of all history information.
- Otherwise mixed/INCONCLUSIVE; report individual results without selecting winners. Unresolved numerical/integrity defects prevent scientific classification.

The fixed models share one process; they are not three independent worlds. Bootstrap uncertainty excludes training-seed population variation and chart-fitting variation. Exposed-data selection and the feasibility gates limit any nominal confidence interpretation. Positive results do not establish causal use, predictive usefulness, topological necessity or dependence on contexts longer than those examined. Do not add K2/K8 or causal experiments after inspecting outcomes.

## Reuse assessment and authorization boundary

| Required field | Smallest compatible plan |
|---|---|
| Existing code/artifacts | The inventory above; `tools/x4_oracle_profile/oracle_profile.py` pure oracle kernels and separate `tests/oracle_profile/independent_reference.py`; public artifact contracts/HistoryIndex alignment; existing mailbox, process meter and guards. |
| Missing capability | Verified reusable fitted PH chart with exact lift and deterministic transform; adapter for these existing E4 histories; independent tests for chart/decision rules. |
| Smallest change | Reuse pure oracle functions unchanged; add a separate artifact adapter using existing contracts. After review, minimally extract candidate chart functions into one reusable fit/transform component. Never run/copy the old sampling runner or mutate frozen sources. |
| Stable interfaces/invariants | Ordered history-ID join, no w33, stationary suffix convention, read-only inputs, exact lift certificates, calibration-only gauge, complete support, immutable saved chart, terminal gates/ledger. |
| Regression tests | Separate test author before implementation; tiny known cocycle/closure/primitive cases, synthetic out-of-sample circle and duplicate/support cases, isolation from validation labels, asymmetric-HMM zero controls, paired resampling and decision boundary tests. Reuse existing oracle regressions; guard fault tests for any reused wrapper changes. |
| Plausible next extension | Reuse the same saved-chart interface on an owner-approved independent cohort if justified; no speculative framework or additional K now. |

Implementation/computation is delegated to Claude only after owner approval, independent contract/test review and a frozen concrete brief through the EXISTING job/mailbox system. A proposed feasibility cap is 1200 CPU seconds (identity/synthetic100, oracle200, charts650, precision150, export/integrity100), one native thread, 8GiB peak, 128MiB output, 180s native-operation wall cap. This matches the prior six-chart workload proposal, not a measured guarantee; charts were never benchmarked. Count startup/tests/review/supervision/exports and all native CPU, preserve partial output and STOP at the cap. No inherited unused budget, retries, automatic escalation or scoring budget is granted. Exact code reuse, STOP/usage guards and input/output paths must be frozen before dispatch; new output must be separate from all frozen stores.

End of feasibility: verified terminal status, concise positive/negative/failed-gate outcome, authoritative artifact/code/decision links, outstanding actions/approval gate and last-reviewed correspondence cursor in the existing job/coordinator records. No additional memory framework or watcher. Next owner decision is approval or revision of this feasibility proposal; scoring remains separately gated even after feasibility passes.

Static independent design review: profile_contract_review checked identification and then the complete draft. Corrections incorporated: overall rather than within-bin phase resultant, explicit whole-payload identity-only access, fully specified extension/duplicate rules, exact centered-power formula, explicit indexing and the distinction between reference agreement and a propagated error bound. No scientific computation was performed by either reviewer.
